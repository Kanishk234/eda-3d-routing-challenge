"""Run a bounded declared fresh-construction plan; record every failure."""
import argparse,json,subprocess,sys,time
from pathlib import Path
from measure import ROOT,OFFICIAL,digest,save

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    assert not a.out.exists();a.out.mkdir(parents=True)
    plan=json.loads(a.plan.read_text());sources=[a.plan,Path(__file__),ROOT/'dev/component_router.py',ROOT/'dev/branch_repair.py']
    sources.extend(OFFICIAL/item['suite']/item['case_file'] for item in plan['cases'])
    frozen={str(q.resolve()):digest(q) for q in sources};start=time.monotonic()
    report={'plan':plan,'frozen_sha256':frozen,'status':'running','rows':[],'workers':1,'scope':'Fresh route construction with no warm starts. Every trial retained, failures included. Expansion ceiling and round ceiling do not imply equal CPU. No full-tier competitiveness claim.'}
    save(a.out/'progress.json',report)
    try:
        for item in plan['cases']:
            for seed in plan['seeds']:
                for method in plan['methods']:
                    if (a.out/'STOP').exists():report['status']='stopped';save(a.out/'progress.json',report);return
                    assert all(digest(Path(q))==sha for q,sha in frozen.items())
                    target=a.out/f"{item['suite']}-{Path(item['case_file']).stem}-{seed}-{method}"
                    cmd=[sys.executable,str(ROOT/'dev/component_router.py'),'--case',str(OFFICIAL/item['suite']/item['case_file']),'--method',method,'--seed',str(seed),'--work-budget',str(plan['work_budget']),'--budget',str(plan['budget']),'--rounds',str(plan['rounds']),'--out',str(target)]
                    report['current']={'case':item,'seed':seed,'method':method};save(a.out/'progress.json',report)
                    subprocess.run(cmd,check=True,timeout=plan['budget']+30)
                    assert all(digest(Path(q))==sha for q,sha in frozen.items())
                    m=json.loads((target/'manifest.json').read_text());row={k:m[k] for k in ['legal','delay','expansions','stats','wall_s','output_sha256']}
                    row.update(case=item,seed=seed,method=method,run=str(target.resolve()),manifest_sha256=digest(target/'manifest.json'));report['rows'].append(row);report['elapsed_wall_s']=time.monotonic()-start;save(a.out/'progress.json',report)
        report['status']='complete';report['current']=None;report['elapsed_wall_s']=time.monotonic()-start;save(a.out/'progress.json',report)
    except BaseException as error:
        report['status']='failed';report['error']=repr(error);save(a.out/'progress.json',report);raise

if __name__=='__main__':main()
