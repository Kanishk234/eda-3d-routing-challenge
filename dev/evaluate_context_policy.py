"""Frozen CPU learned policies on official development cases; all failures kept."""
import argparse,json,time,resource
from pathlib import Path
from learned_context_order import run_policy
from run_polish import Instance,Submission,check
from measure import ROOT,OFFICIAL,digest,save

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();a.out.mkdir(parents=True)
 import torch
 torch.set_num_threads(1)
 plan=json.loads(a.plan.read_text());folder=ROOT/plan['model_root'];metadata=json.loads((folder/'model.json').read_text());assert digest(folder/'mlp.pt')==metadata['mlp_sha256'];report_model=json.loads((folder/'progress.json').read_text());assert report_model['status']=='complete';assert digest(folder/'model.json')==report_model['model_sha256']
 mlp=torch.nn.Sequential(torch.nn.Linear(16,32),torch.nn.Tanh(),torch.nn.Linear(32,1));mlp.load_state_dict(torch.load(folder/'mlp.pt',map_location='cpu',weights_only=True));mlp.eval();model=dict(static_weights=metadata['static_weights'],context_weights=metadata['context_weights'],mlp=mlp)
 frozen={str(p.resolve()):digest(p) for p in [a.plan,Path(__file__),ROOT/'dev/learned_context_order.py',ROOT/'dev/branch_repair.py',folder/'model.json',folder/'mlp.pt']};report=dict(status='running',plan=plan,source_sha256=frozen,rows=[],workers=1,cpu_threads=1,scope='Fixed own curriculum models; one sequential construction per development case/method/seed. Failures retained. No tier claim or model tuning on these results.');start=time.monotonic();save(a.out/'progress.json',report)
 for case in plan['cases']:
  path=OFFICIAL/case['suite']/case['file'];inst=Instance.load(path)
  for seed in plan['seeds']:
   for name in plan['methods']:
    out,stats=run_policy(inst,name,model,seed,plan['work_budget'],plan['budget']);stats['legal']=out is not None
    if out:
     target=a.out/f'{case["suite"]}-{inst.name}-{seed}-{name}.sol.json';out.save(str(target));checked=check(inst,Submission.load(str(target)));assert checked.legal;stats['output_sha256']=digest(target)
    report['rows'].append(dict(case=case,case_sha256=digest(path),seed=seed,method=name,**stats));save(a.out/'progress.json',report);print(case['suite'],inst.name,name,stats['legal'],stats.get('delay'),stats['completed_nets'],flush=True)
 assert all(digest(Path(p))==h for p,h in frozen.items());report.update(status='complete',wall_s=time.monotonic()-start,peak_rss_kb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);save(a.out/'progress.json',report)
if __name__=='__main__':main()
