"""Matched strict-versus-neutral adaptive repair on two development cases."""
import argparse,json,math,subprocess,sys
from pathlib import Path
from measure import ROOT,digest,save
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work-budget',type=int,default=3000000);p.add_argument('--out',type=Path,default=ROOT/'docs/evidence/phase3/weighted-seed-screen.json');a=p.parse_args();assert a.work_budget>0
coverage=ROOT/'docs/evidence/phase3/tier-neutral-followup-coverage.json'
out=a.out;assert not out.exists()
source=json.loads(coverage.read_text());report={'coverage_sha256':digest(coverage),'workers':1,'work_budget':a.work_budget,'rows':[],'complete':False,'limitations':'One development case per tier;gap/vertices is an uncalibrated cost proxy. Equal expansion effort is not equal CPU time. Neutral moves change geometry but not physical total delay;future usefulness requires measured gains.'}
save(out,report)
for tier,case in [('designs','ctrl'),('congested','case_01')]:
 start=next(r['run_id'] for r in source['rows'] if r['tier']==tier);cfg=(2,4,4) if tier=='congested' else (2,2,2)
 for sampling in (0,1,2):
  for seed in (1,2,3):
   cmd=[sys.executable,str(ROOT/'dev/run_polish.py'),'--suite','benchmarks_'+tier,'--case',case,'--resume-dir',str(ROOT/'dev/artifacts'/start/'routes'),'--mode','fanout_fine_adaptive','--seed',str(seed),'--passes','1000','--budget','60','--work-budget',str(a.work_budget),'--group-limit','3','--present-initial',str(cfg[0]),'--present-step',str(cfg[1]),'--history-step',str(cfg[2])]
   cmd+=['--accept-equal','--repair-sampling',str(sampling)]
   before=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'));subprocess.run(cmd,check=True);paths=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))-before;assert len(paths)==1
   p=paths.pop();m=json.loads(p.read_text());c=m['cases'][0];assert m['success'] and c['legal'] and m['official_inputs_unchanged'] and c['total_delay']<=c['before_delay']
   report['rows'].append({'tier':tier,'case':case,'sampling':sampling,'seed':seed,'run_id':m['run_id'],'manifest_sha256':digest(p),'solver_sha256':m['solver_sha256'],'binary_sha256':m['binary_sha256'],'config':m['config'],'delay':c['total_delay'],'core':c['core'],'counters':c['process']['repair_counters'],'wrapper_wall_s':m['wrapper_wall_s'],'output_sha256':c['output_sha256']});save(out,report)
report['comparisons']=[];report['selected']={}
for tier in ('designs','congested'):
 eligible=[]
 for sampling in (1,2):
  counts={'wins':0,'ties':0,'losses':0};ratios=[]
  for seed in (1,2,3):
   old=next(r['delay'] for r in report['rows'] if (r['tier'],r['sampling'],r['seed'])==(tier,0,seed));new=next(r['delay'] for r in report['rows'] if (r['tier'],r['sampling'],r['seed'])==(tier,sampling,seed));counts['wins' if new<old else 'losses' if new>old else 'ties']+=1;ratios.append(old/new)
  ratio=math.exp(sum(map(math.log,ratios))/3);report['comparisons'].append({'tier':tier,'sampling':sampling,**counts,'geomean_delay_ratio':ratio})
  if ratio>1 and counts['wins']>=2:eligible.append((ratio,sampling))
 report['selected'][tier]=max(eligible)[1] if eligible else 0
report['complete']=True;report['total_wrapper_wall_s']=sum(r['wrapper_wall_s'] for r in report['rows']);save(out,report);print(report['comparisons']);print(report['selected'])
