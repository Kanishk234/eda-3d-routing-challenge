"""Revalidate and freeze Phase 2 evidence; never alter official inputs."""
import json
import sys
from pathlib import Path
from measure import ROOT, OFFICIAL, REVISION, digest, save, execute
sys.path.insert(0, str(OFFICIAL))
from m3d.model import Instance, Submission
from m3d.checker import check


def main():
    runs=[]
    for p in sorted((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json')):
        m=json.loads(p.read_text())
        assert m['success'] and m['official_inputs_unchanged'], p
        for name,h in m['outputs'].items():
            assert digest(p.parent/name)==h
        runs.append((p,m))
    full=[(p,m) for p,m in runs if m['result']['complete']]
    p,m=full[-1]
    assert all(x['outputs']==m['outputs'] for _,x in full)
    assert digest(ROOT/'dev/solver/exact_polish.cpp')==m['solver_sha256']
    assert digest(ROOT/'dev/artifacts/build/exact_polish')==m['binary_sha256']
    for name,h in m['official_hashes'].items():
        assert digest(OFFICIAL/name)==h
    suite=json.loads((OFFICIAL/'benchmarks_hard/suite.json').read_text())
    for c,r in zip(suite['cases'],m['cases']):
        checked=check(Instance.load(OFFICIAL/'benchmarks_hard'/c['instance_file']),
                      Submission.load(p.parent/'routes'/(c['name']+'.sol.json')))
        assert checked.legal and checked.total_delay==r['total_delay']
    step=execute([sys.executable,'-m','m3d.cli','score-suite','--suite','benchmarks_hard',
                  '--submission-dir',str(p.parent/'routes'),'--out',str(p.parent/'official-rescore.json')],
                 p.parent,'phase2-rescore',60)
    assert step['exit_code']==0
    score=json.loads((p.parent/'official-rescore.json').read_text())
    assert score['aggregate_score']==m['result']['aggregate_score'] and score['n_legal']==9
    baseline=json.loads((ROOT/'dev/artifacts/20261001T171522.463214Z-suite/manifest.json').read_text())
    evidence=ROOT/'docs/evidence/phase2'; evidence.mkdir(exist_ok=True)
    compact=[]
    for path,run in runs:
        compact.append({k:v for k,v in run.items() if k not in ('official_hashes','source','machine')})
        compact[-1].update(manifest_path=str(path.relative_to(ROOT)),manifest_sha256=digest(path),
                          source_identity=run['source']['files_sha256'])
    save(evidence/'runs.json',compact)
    report={'upstream_revision':REVISION,'selected_run':m['run_id'],'result':score,
            'official_rescore':step,'outputs':m['outputs'],
            'kernel_tests':{'log_sha256':digest(ROOT/'dev/artifacts/build/kernel-tests.log'),
                            'log':(ROOT/'dev/artifacts/build/kernel-tests.log').read_text()},
            'budget_comparison':{'shared_envelope_s':600,'workers':1,
               'baseline_generation_wall_s':baseline['steps'][0]['wall_s'],
               'polish_core_wall_s':m['total_core_wall_s'],
               'polish_wrapper_wall_s':m['wrapper_wall_s'],
               'pipeline_wall_s':baseline['steps'][0]['wall_s']+m['wrapper_wall_s'],
               'baseline_score':1.0,'polished_score':score['aggregate_score'],
               'note':'Same machine and common 600s routing envelope; paired baseline warm start reused. Baseline terminates normally and unused budget is not spent. No speedup or fresh independent pipeline timing claimed.'},
            'limitations':['Baseline warm start required; no public warm starts.',
                            'Exact single-net paths with other nets fixed, not global optimality.',
                            'One selected seed/config; repeat checks are not portfolio selection.',
                            'No tuning on hard08/09; validation-only full-tier checks.',
                            'SIGKILL retains pre-search checkpoint; SIGTERM kernel emits completed incumbent.',
                            'Raw routes/logs/source snapshots ignored and require backup.']}
    assert report['budget_comparison']['pipeline_wall_s']<600
    save(evidence/'comparison.json',report)
    print(json.dumps(report['budget_comparison'],indent=2))

if __name__=='__main__':
    main()
