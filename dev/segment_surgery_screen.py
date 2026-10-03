"""Matched refinement of existing partial-branch repair on our own routes."""
import argparse,json,time,math,resource
from pathlib import Path
from segment_surgery import SurgeryRouter,PricedBranchRouter
from branch_repair import Router
from run_polish import Instance,Submission,check
from measure import ROOT,OFFICIAL,digest,save,source_identity

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();a.out.mkdir(parents=True);plan=json.loads(a.plan.read_text());coverage=json.loads((ROOT/plan['coverage']).read_text());stage=next(r for r in coverage['rows'] if r['tier']=='hard');suite=stage['config']['suite'];files=[a.plan,Path(__file__),ROOT/'dev/segment_surgery.py',ROOT/'dev/branch_repair.py',ROOT/'dev/generate_tree_candidates.py',ROOT/plan['coverage']];frozen={str(p.resolve()):digest(p) for p in files};report=dict(status='running',plan=plan,source_identity=source_identity(),frozen_sha256=frozen,workers=1,rows=[],scope='Own routes,whole-case official validation; degree-two connector geometry versus existing partial-branch reconstruction. Preserves downstream component/driver root labels. Equal work caps,not equal CPU time;no competitor inputs.');save(a.out/'progress.json',report)
 for name in plan['cases']:
  path=OFFICIAL/suite/(name+'.json');parent=ROOT/'dev/artifacts'/stage['run_id']/'routes'/(name+'.sol.json');inst=Instance.load(path);sub=Submission.load(parent);before=check(inst,sub);assert before.legal
  for seed in plan['seeds']:
   for mode,cls in [('branch',PricedBranchRouter),('segment',SurgeryRouter)]:
    folder=a.out/f'{name}-{seed}-{mode}';folder.mkdir();start=time.monotonic();router=cls(inst,sub,plan['work_budget'],plan['budget'],seed,proposal_penalties=plan.get('penalties',[0]));out=router.run('branch',200);after=check(inst,out);assert after.legal and after.total_delay<=before.total_delay;target=folder/(name+'.sol.json');out.save(str(target));assert check(inst,Submission.load(target)).total_delay==after.total_delay;report['rows'].append(dict(case=name,seed=seed,mode=mode,before_delay=before.total_delay,after_delay=after.total_delay,case_sha256=digest(path),parent_sha256=digest(parent),output=str(target),output_sha256=digest(target),legal=True,expansions=router.expansions,reached_work_cap=router.expansions==plan['work_budget'],stats=dict(router.stats),wall_s=time.monotonic()-start));save(a.out/'progress.json',report);print(name,seed,mode,'gain',before.total_delay-after.total_delay,flush=True)
 assert all(digest(Path(p))==h for p,h in frozen.items());pairs=[]
 for row in report['rows']:
  if row['mode']=='segment':
   base=next(x for x in report['rows'] if x['mode']=='branch' and (x['case'],x['seed'])==(row['case'],row['seed']));pairs.append((base['after_delay'],row['after_delay']))
 report.update(status='complete',comparisons=dict(wins=sum(a>b for a,b in pairs),ties=sum(a==b for a,b in pairs),losses=sum(a<b for a,b in pairs),geomean_score_ratio=math.exp(sum(math.log(a/b) for a,b in pairs)/len(pairs)),all_work_caps_reached=all(r['reached_work_cap'] for r in report['rows'])),peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);save(a.out/'progress.json',report)
if __name__=='__main__':main()
