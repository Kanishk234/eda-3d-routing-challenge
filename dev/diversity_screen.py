"""Compare existing local archive diversity with matched continuation work."""
import json,math,subprocess,sys
from measure import ROOT,digest,save
inventory=ROOT/'docs/evidence/phase3/diversity-inventory.json'
out=ROOT/'docs/evidence/phase3/diversity-screen.json'
assert not out.exists()
i=json.loads(inventory.read_text())
report={'inventory_sha256':digest(inventory),'workers':1,'work_budget':3000000,'rows':[],'complete':False,'limitations':'Equal additional expanded-vertex effort,not equal CPU time or matched historical generation. Alternative starts selected by edge geometry within5percent case delay. Older local generation cost excluded from these stage timings but manifests retained. One development case per tier; no claim that Jaccard distance proves distinct local minima.'}
save(out,report)
for tier,entry in i['tiers'].items():
 for label in ('current','alternate','donor'):
  for seed in (1,2,3):
   start=entry['selected']['run_id'] if label=='alternate' else entry['current_run']
   schedule=(2,4,4) if tier=='congested' else (2,2,2)
   cmd=[sys.executable,str(ROOT/'dev/run_polish.py'),'--suite','benchmarks_'+tier,'--case',entry['case'],'--resume-dir',str(ROOT/'dev/artifacts'/start/'routes'),'--mode','fanout_fine_donor' if label=='donor' else 'fanout_fine_adaptive','--seed',str(seed),'--passes','1000','--budget','60','--work-budget','3000000','--group-limit','3','--present-initial',str(schedule[0]),'--present-step',str(schedule[1]),'--history-step',str(schedule[2])]
   if label=='donor':cmd+=['--donor-dir',str(ROOT/'dev/artifacts'/entry['selected']['run_id']/'routes')]
   before=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'));subprocess.run(cmd,check=True)
   paths=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))-before;assert len(paths)==1
   p=paths.pop();m=json.loads(p.read_text());c=m['cases'][0];assert m['success'] and m['official_inputs_unchanged'] and c['legal'];assert c['core']['expansions']<=3000000
   report['rows'].append({'tier':tier,'case':entry['case'],'label':label,'seed':seed,'run_id':m['run_id'],'manifest_sha256':digest(p),'solver_sha256':m['solver_sha256'],'binary_sha256':m['binary_sha256'],'config':m['config'],'delay':c['total_delay'],'core':c['core'],'counters':c['process']['repair_counters'],'output_sha256':c['output_sha256'],'wrapper_wall_s':m['wrapper_wall_s']});save(out,report)
report['comparisons']=[];report['selected']={}
for tier in i['tiers']:
 eligible=[]
 for label in ('alternate','donor'):
  counts={'wins':0,'ties':0,'losses':0};ratios=[]
  for seed in (1,2,3):
   b=next(r for r in report['rows'] if (r['tier'],r['label'],r['seed'])==(tier,'current',seed));n=next(r for r in report['rows'] if (r['tier'],r['label'],r['seed'])==(tier,label,seed))
   counts['wins' if n['delay']<b['delay'] else 'losses' if n['delay']>b['delay'] else 'ties']+=1;ratios.append(b['delay']/n['delay'])
  ratio=math.exp(sum(map(math.log,ratios))/3);report['comparisons'].append({'tier':tier,'label':label,**counts,'geomean_delay_ratio':ratio})
  if ratio>1 and counts['wins']>=2:eligible.append((ratio,label))
 report['selected'][tier]=max(eligible)[1] if eligible else 'current'
report['complete']=True;report['total_wrapper_wall_s']=sum(r['wrapper_wall_s'] for r in report['rows']);save(out,report);print(report['comparisons']);print(report['selected'])
