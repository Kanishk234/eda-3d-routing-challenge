"""Individually checked tree catalog from explicitly declared own fresh outputs."""
import argparse,json
from pathlib import Path
from measure import ROOT,OFFICIAL,digest,save
from run_polish import Instance,Submission,check

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--tier',required=True);p.add_argument('--polish-report',type=Path,required=True);p.add_argument('--fresh-report',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();polished=json.loads(a.polish_report.read_text());fresh=json.loads(a.fresh_report.read_text());assert polished['status']==fresh['status']=='complete';suite='benchmarks' if a.tier=='intro' else 'benchmarks_'+a.tier;inventory=json.loads((OFFICIAL/suite/'suite.json').read_text());report=dict(status='complete',source_sha256=digest(Path(__file__)),source_reports={str(p):digest(p) for p in [a.polish_report,a.fresh_report]},cases={},scope='Original own fresh trees and subsequent own native refinement only. Per-net pool candidates may conflict; final selection/checking separate. Fresh generation cost remains in source reports,not native ancestor sums.')
 for case in inventory['cases']:
  path=OFFICIAL/suite/case['instance_file'];inst=Instance.load(path);sources=[]
  for r in fresh['rows']:
   if r['case']['suite']==suite and Path(r['case']['file']).stem==case['name'] and r['fresh_legal']:
    target=ROOT/r['output'];assert digest(target)==r['output_sha256'];sources.append(target)
  for r in polished['rows']:
   mpath=ROOT/'dev/artifacts'/r['run_id']/'manifest.json';m=json.loads(mpath.read_text());assert digest(mpath)==r['manifest_sha256']
   if m['config']['suite']==suite and r['case']==case['name']:
    target=mpath.parent/'routes'/(case['name']+'.sol.json');assert digest(target)==m['outputs']['routes/'+target.name];sources.append(target)
  row=dict(case_sha256=digest(path),trees=[],source_outputs={});seen={n.id:set() for n in inst.nets}
  for target in sources:
   sub=Submission.load(target);whole=check(inst,sub);assert whole.legal;row['source_outputs'][str(target.relative_to(ROOT))]=digest(target)
   delays={n.net:n.delay for n in whole.nets}
   for tree,encoded in zip(sub.routes,sub.to_dict()['routes']):
    key=tuple(sorted(tuple(sorted(e)) for e in tree.edges))
    if key in seen[tree.net]:continue
    seen[tree.net].add(key);individual=check(inst,Submission(inst.name,[tree]));nr=next(n for n in individual.nets if n.net==tree.net);assert nr.legal and nr.delay==delays[tree.net]
    row['trees'].append(dict(route=encoded,delay=nr.delay,source=str(target.relative_to(ROOT))))
  report['cases'][case['name']]=row
 save(a.out,report);print(a.tier,'catalog trees',sum(len(c['trees']) for c in report['cases'].values()))
if __name__=='__main__':main()
