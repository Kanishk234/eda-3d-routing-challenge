"""Independent per-net physical progress accounting between frozen complete runs."""
import argparse,json
from pathlib import Path
from collections import defaultdict
from measure import ROOT,OFFICIAL,digest,save
from run_polish import Instance,Submission,check

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--before',type=Path,required=True);p.add_argument('--after',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists()
 before=json.loads(a.before.read_text());after=json.loads(a.after.read_text());rows=[];groups=defaultdict(lambda:{'nets':0,'improved_nets':0,'regressed_nets':0,'before_delay':0,'after_delay':0,'before_vertices':0,'after_vertices':0});leading=[]
 for stage in after['rows']:
  tier=stage['tier'];old=next(r for r in before['rows'] if r['tier']==tier);suite=old['config']['suite'];inventory=json.loads((OFFICIAL/suite/'suite.json').read_text())
  for item in inventory['cases']:
   case=OFFICIAL/suite/item['instance_file'];inst=Instance.load(case);paths=[ROOT/'dev/artifacts'/r/'routes'/(item['name']+'.sol.json') for r in (old['run_id'],stage['run_id'])];subs=[Submission.load(q) for q in paths];checks=[check(inst,s) for s in subs];assert all(c.legal for c in checks);assert checks[1].total_delay<=checks[0].total_delay
   costs=[{n.net:n.delay for n in c.nets} for c in checks];resources=[]
   for sub in subs:
    resources.append({r.net:len({v for edge in r.edges for v in edge}) for r in sub.routes})
   rows.append({'tier':tier,'case':item['name'],'case_sha256':digest(case),'before_run':old['run_id'],'after_run':stage['run_id'],'before_output_sha256':digest(paths[0]),'after_output_sha256':digest(paths[1]),'before_delay':checks[0].total_delay,'after_delay':checks[1].total_delay})
   for n in inst.nets:
    fanout=len(n.sinks);band='1' if fanout==1 else '2-4' if fanout<=4 else '5-8' if fanout<=8 else '9+'
    d0,d1=costs[0][n.id],costs[1][n.id];key=tier+':fanout'+band;g=groups[key];g['nets']+=1;g['improved_nets']+=d1<d0;g['regressed_nets']+=d1>d0;g['before_delay']+=d0;g['after_delay']+=d1;g['before_vertices']+=resources[0][n.id];g['after_vertices']+=resources[1][n.id]
    leading.append({'tier':tier,'case':item['name'],'net':n.id,'fanout':fanout,'physical_gain':d0-d1})
 save(a.out,{'before_sha256':digest(a.before),'after_sha256':digest(a.after),'source_sha256':digest(Path(__file__)),'cases':rows,'groups':dict(groups),'largest_net_gains':sorted(leading,key=lambda x:x['physical_gain'],reverse=True)[:30],'largest_net_regressions':sorted((x for x in leading if x['physical_gain']<0),key=lambda x:x['physical_gain'])[:30],'limitations':'Observed legal per-net differences after additional search and tuning. Nets can regress while total delay improves. Group totals do not prove operator causality,independent improvement potential or unseen-case generalization.'})

if __name__=='__main__':main()
