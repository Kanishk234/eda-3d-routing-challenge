"""Matched fine-pricing whole-instance restarts versus incumbent continuation."""
import json,math,subprocess,sys
from pathlib import Path
from measure import ROOT,digest,save
coverage=ROOT/'docs/evidence/phase3/tier-sampling-fusion-followup-coverage.json'
out=ROOT/'docs/evidence/phase3/fresh-fine-screen.json'
assert not out.exists()
source=json.loads(coverage.read_text())
report={'coverage_sha256':digest(coverage),'source_sha256':digest(Path(__file__)),'workers':1,'work_budget':10000000,'rows':[],'complete':False,'limitations':'Matched added expansion ceiling,not equal CPU cost. Three development cases;no unseen-case claim. Restarts discard nonimproving legal candidates and rollback incomplete negotiation;they do not expose a candidate pool.'}
save(out,report)
for tier,case in [('hard','case_01'),('designs','ctrl'),('congested','case_01')]:
 start=next(r['run_id'] for r in source['rows'] if r['tier']==tier)
 schedule=(2,1,1) if tier=='hard' else (2,4,4) if tier=='congested' else (2,2,2)
 for mode in ('fanout_fine_adaptive','restart_fine'):
  for seed in (1,2,3):
   cmd=[sys.executable,str(ROOT/'dev/run_polish.py'),'--suite','benchmarks_'+tier,'--case',case,'--resume-dir',str(ROOT/'dev/artifacts'/start/'routes'),'--mode',mode,'--seed',str(seed),'--passes','1000','--budget','60','--work-budget','10000000','--group-limit','13' if tier=='hard' else '3','--present-initial',str(schedule[0]),'--present-step',str(schedule[1]),'--history-step',str(schedule[2])]
   if mode=='fanout_fine_adaptive':cmd+=['--accept-equal']
   before=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'));subprocess.run(cmd,check=True)
   paths=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))-before;assert len(paths)==1
   p=paths.pop();m=json.loads(p.read_text());c=m['cases'][0]
   assert m['success'] and m['official_inputs_unchanged'] and c['legal'] and c['total_delay']<=c['before_delay']
   report['rows'].append({'tier':tier,'case':case,'mode':mode,'seed':seed,'run_id':m['run_id'],'manifest_sha256':digest(p),'solver_sha256':m['solver_sha256'],'binary_sha256':m['binary_sha256'],'config':m['config'],'before_delay':c['before_delay'],'delay':c['total_delay'],'core':c['core'],'counters':c['process']['repair_counters'],'wrapper_wall_s':m['wrapper_wall_s'],'output_sha256':c['output_sha256']});save(out,report)
report['comparisons']=[]
for tier in ('hard','designs','congested'):
 counts={'wins':0,'ties':0,'losses':0};ratios=[]
 for seed in (1,2,3):
  old=next(r['delay'] for r in report['rows'] if (r['tier'],r['mode'],r['seed'])==(tier,'fanout_fine_adaptive',seed));new=next(r['delay'] for r in report['rows'] if (r['tier'],r['mode'],r['seed'])==(tier,'restart_fine',seed));counts['wins' if new<old else 'losses' if new>old else 'ties']+=1;ratios.append(old/new)
 report['comparisons'].append({'tier':tier,**counts,'geomean_delay_ratio':math.exp(sum(map(math.log,ratios))/3)})
report['complete']=True;report['total_wrapper_wall_s']=sum(r['wrapper_wall_s'] for r in report['rows']);save(out,report);print(report['comparisons'])
