"""Matched strict-versus-neutral adaptive repair on two development cases."""
import argparse,json,math,subprocess,sys
from pathlib import Path
from measure import ROOT,digest,save
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work-budget',type=int,default=3000000);p.add_argument('--out',type=Path,default=ROOT/'docs/evidence/phase3/hard-neutral-screen.json');a=p.parse_args();assert a.work_budget>0
coverage=ROOT/'docs/evidence/phase3/tier-neutral-followup-coverage.json'
out=a.out;assert not out.exists()
source=json.loads(coverage.read_text());report={'coverage_sha256':digest(coverage),'workers':1,'work_budget':a.work_budget,'rows':[],'complete':False,'limitations':'Hard01/04/07 development only;08/09 reserved. Equal expansion effort is not equal CPU time. Neutral moves change geometry but not physical total delay;future usefulness requires measured gains.'}
save(out,report)
for tier,case in [('hard','case_01'),('hard','case_04'),('hard','case_07')]:
 start=next(r['run_id'] for r in source['rows'] if r['tier']==tier);cfg=(2,1,1)
 for equal in (False,True):
  for seed in (1,2,3):
   cmd=[sys.executable,str(ROOT/'dev/run_polish.py'),'--suite','benchmarks_'+tier,'--case',case,'--resume-dir',str(ROOT/'dev/artifacts'/start/'routes'),'--mode','fanout_fine_adaptive','--seed',str(seed),'--passes','1000','--budget','60','--work-budget',str(a.work_budget),'--group-limit','13','--present-initial',str(cfg[0]),'--present-step',str(cfg[1]),'--history-step',str(cfg[2])]
   if equal:cmd+=['--accept-equal']
   before=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'));subprocess.run(cmd,check=True);paths=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))-before;assert len(paths)==1
   p=paths.pop();m=json.loads(p.read_text());c=m['cases'][0];assert m['success'] and c['legal'] and m['official_inputs_unchanged'] and c['total_delay']<=c['before_delay']
   report['rows'].append({'tier':tier,'case':case,'equal':equal,'seed':seed,'run_id':m['run_id'],'manifest_sha256':digest(p),'solver_sha256':m['solver_sha256'],'binary_sha256':m['binary_sha256'],'config':m['config'],'delay':c['total_delay'],'core':c['core'],'counters':c['process']['repair_counters'],'wrapper_wall_s':m['wrapper_wall_s'],'output_sha256':c['output_sha256']});save(out,report)
report['comparisons']=[];counts={'wins':0,'ties':0,'losses':0};ratios=[]
for case in ('case_01','case_04','case_07'):
 for seed in (1,2,3):
  old=next(r['delay'] for r in report['rows'] if (r['case'],r['equal'],r['seed'])==(case,False,seed));new=next(r['delay'] for r in report['rows'] if (r['case'],r['equal'],r['seed'])==(case,True,seed));counts['wins' if new<old else 'losses' if new>old else 'ties']+=1;ratios.append(old/new)
ratio=math.exp(sum(map(math.log,ratios))/9);report['comparisons'].append({'tier':'hard',**counts,'geomean_delay_ratio':ratio});report['selected']={'hard':ratio>1 and counts['wins']>=5};report['complete']=True;report['total_wrapper_wall_s']=sum(r['wrapper_wall_s'] for r in report['rows']);save(out,report);print(report['comparisons']);print(report['selected'])
