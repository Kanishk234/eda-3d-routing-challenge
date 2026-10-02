"""Compare two legal local pipelines per net; never splice their routes."""
import argparse
from pathlib import Path
from measure import OFFICIAL,REVISION,digest,save
from run_polish import Instance,Submission,check

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('left',type=Path);p.add_argument('right',type=Path)
    p.add_argument('--suite',default='benchmarks_hard');p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    if a.out.exists(): p.error('report exists; use a new destination')
    report={'official_revision':REVISION,'left':str(a.left),'right':str(a.right),'cases':[],
            'limitations':'Signed per-net differences diagnose distinct legal packing patterns; per-net routes cannot be independently mixed without ownership checks.'}
    for case in sorted((OFFICIAL/a.suite).glob('case_*.json')):
        inst=Instance.load(case); paths=[directory/(case.stem+'.sol.json') for directory in (a.left,a.right)]
        checked=[check(inst,Submission.load(path)) for path in paths]
        assert all(c.legal for c in checked)
        delays=[{n.net:n.delay for n in c.nets} for c in checked]
        rows=[{'net':n.id,'sinks':len(n.sinks),'left_delay':delays[0][n.id],
               'right_delay':delays[1][n.id],'left_minus_right':delays[0][n.id]-delays[1][n.id]} for n in inst.nets]
        report['cases'].append({'case':case.stem,'case_sha256':digest(case),'route_sha256':[digest(path) for path in paths],
             'left_delay':checked[0].total_delay,'right_delay':checked[1].total_delay,
             'left_better_nets':sum(r['left_minus_right']<0 for r in rows),
             'right_better_nets':sum(r['left_minus_right']>0 for r in rows),
             'right_improvement_mass':sum(max(0,r['left_minus_right']) for r in rows),
             'left_improvement_mass':sum(max(0,-r['left_minus_right']) for r in rows),
             'largest_differences':sorted(rows,key=lambda r:abs(r['left_minus_right']),reverse=True)[:10]})
    save(a.out,report)
    print('left/right total:',sum(c['left_delay'] for c in report['cases']),sum(c['right_delay'] for c in report['cases']))
    print('opposing per-net improvement mass:',sum(c['left_improvement_mass'] for c in report['cases']),sum(c['right_improvement_mass'] for c in report['cases']))

if __name__=='__main__':main()
