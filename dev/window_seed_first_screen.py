"""Matched whole-net window seed-first repair versus adaptive controls."""
import json,math,subprocess,sys
from pathlib import Path
from measure import ROOT,digest,save
coverage=ROOT/'docs/evidence/phase3/tier-polish-order-followup-coverage.json'
out=ROOT/'docs/evidence/phase3/window-seed-first-screen.json'
assert not out.exists()
c=json.loads(coverage.read_text());r=next(x for x in c['rows'] if x['tier']=='hard')
report={'coverage_sha256':digest(coverage),'workers':1,'work_budget':3000000,'rows':[],'complete':False,'limitations':'Whole-net windows spanning all layers; fixed seed during negotiated repair. Not partial-branch routing or a reproduction of unavailable competitor source. Development hard01/04/07 only;08/09 untouched.'}
save(out,report)
for mode in ('fanout_fine_adaptive','fanout_fine_window'):
 for case in ('case_01','case_04','case_07'):
  for seed in (1,2,3):
   before=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))
   cmd=[sys.executable,str(ROOT/'dev/run_polish.py'),'--suite','benchmarks_hard','--case',case,'--resume-dir',str(ROOT/'dev/artifacts'/r['run_id']/'routes'),'--mode',mode,'--budget','60','--work-budget','3000000','--passes','1000','--seed',str(seed),'--group-limit','13','--present-initial','2','--present-step','1','--history-step','1']
   subprocess.run(cmd,check=True)
   paths=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))-before;assert len(paths)==1
   p=paths.pop();m=json.loads(p.read_text());t=m['cases'][0];assert m['success'] and t['legal'] and m['official_inputs_unchanged']
   report['rows'].append({'mode':mode,'case':case,'seed':seed,'run_id':m['run_id'],'manifest_sha256':digest(p),'binary_sha256':m['binary_sha256'],'solver_sha256':m['solver_sha256'],'config':m['config'],'delay':t['total_delay'],'core':t['core'],'counters':t['process']['repair_counters'],'output_sha256':t['output_sha256'],'wrapper_wall_s':m['wrapper_wall_s']});save(out,report)
counts={'wins':0,'ties':0,'losses':0};ratios=[]
for b in report['rows'][:9]:
 n=next(x for x in report['rows'][9:] if (x['case'],x['seed'])==(b['case'],b['seed']))
 counts['wins' if n['delay']<b['delay'] else 'losses' if n['delay']>b['delay'] else 'ties']+=1;ratios.append(b['delay']/n['delay'])
report['comparison']={**counts,'geomean_delay_ratio':math.exp(sum(map(math.log,ratios))/len(ratios))};report['total_wrapper_wall_s']=sum(x['wrapper_wall_s'] for x in report['rows']);report['complete']=True;save(out,report);print(report['comparison'])
