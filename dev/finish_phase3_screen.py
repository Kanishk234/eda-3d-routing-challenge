"""Freeze fixed-config repair validation and diagnostics without selecting a portfolio."""
import json
import sys
from measure import ROOT, digest, save, execute

def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--mode",choices=["repairsoft","negotiated"],default="repairsoft")
    args=parser.parse_args()
    paths=sorted((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))
    candidates=[p for p in paths if (lambda m:m['config'].get('mode')==args.mode and m['result']['complete'])(json.loads(p.read_text()))]
    p=candidates[-1]; m=json.loads(p.read_text())
    assert m['config']['seed']==1 and m['config']['budget']==2 and m['config']['passes']==5
    assert m['success'] and m['official_inputs_unchanged']
    for name,h in m['outputs'].items(): assert digest(p.parent/name)==h
    step=execute([sys.executable,'-m','m3d.cli','score-suite','--suite','benchmarks_hard',
        '--submission-dir',str(p.parent/'routes'),'--out',str(p.parent/'official-rescore.json')],p.parent,'official-rescore',60)
    assert step['exit_code']==0
    score=json.loads((p.parent/'official-rescore.json').read_text())
    assert score['aggregate_score']==m['result']['aggregate_score']
    diag=json.loads((ROOT/'docs/evidence/phase3/repair-diagnostics.json').read_text())
    sums={}
    for row in diag['rows']:
        for k,v in row['process']['repair_counters'].items(): sums[k]=sums.get(k,0)+v
    report={k:v for k,v in m.items() if k not in ('source','official_hashes','machine')}
    report.update(source_identity=m['source']['files_sha256'],manifest_sha256=digest(p),
                  official_rescore=step,diagnostics_totals=sums,
                  test_log=(ROOT/'dev/artifacts/build/phase3-negotiation-tests.log').read_text(),
                  test_log_sha256=digest(ROOT/'dev/artifacts/build/phase3-negotiation-tests.log'),
                  policy='fixed seed1,penalty4,max4 blockers,5passes,2s/case;12 negotiation rounds max; no per-case portfolio selection',
                  warm_start_cost='Phase2 wrapper3.186s + baseline94.765s; add this repair wrapper. Screening costs reported separately.')
    save(ROOT/'docs/evidence/phase3/soft-validation.json',report)
    print(score['aggregate_score'],'core',m['total_core_wall_s'],'wrapper',m['wrapper_wall_s'])

if __name__=='__main__': main()
