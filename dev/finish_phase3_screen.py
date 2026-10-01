"""Freeze fixed-config repair validation and diagnostics without selecting a portfolio."""
import json
import sys
from measure import ROOT, digest, save, execute

def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--mode",choices=["repairsoft","negotiated","explore","wide"],default="repairsoft")
    args=parser.parse_args()
    paths=sorted((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))
    candidates=[p for p in paths if (lambda m:m['config'].get('mode')==args.mode and m['result']['complete'])(json.loads(p.read_text()))]
    p=candidates[-1]; m=json.loads(p.read_text())
    assert m['config']['seed']==1
    assert (m['config']['budget'],m['config']['passes']) in ((2,5),(10,100))
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
                  test_log=(ROOT/'dev/artifacts/build/neighborhood-tests.log').read_text(),
                  test_log_sha256=digest(ROOT/'dev/artifacts/build/neighborhood-tests.log'),
                  policy={'seed':1,'mode':args.mode,'budget_s':m['config']['budget'],'passes':m['config']['passes'],'blockers':12 if args.mode=='wide' else 4,'rounds':24 if args.mode=='wide' else 12,'portfolio_selection':False},
                  warm_start_cost=('Baseline94.765s + exact wrapper3.186s; add repair wrapper; exploration additionally inherits negotiated wrapper8.233s. Component sum,screen costs separate; not fresh end-to-end timing.'))
    save(ROOT/'docs/evidence/phase3'/({'repairsoft':'soft','negotiated':'negotiated','explore':'plateau','wide':'wide'}[args.mode]+'-validation.json'),report)
    print(score['aggregate_score'],'core',m['total_core_wall_s'],'wrapper',m['wrapper_wall_s'])

if __name__=='__main__': main()
