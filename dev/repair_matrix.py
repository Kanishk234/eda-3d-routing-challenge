"""Run an immutable declared repair matrix serially, preserving every outcome."""
import argparse,json,math,subprocess,sys
from pathlib import Path
from measure import ROOT,digest,save

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('matrix',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 assert not a.out.exists();cfg=json.loads(a.matrix.read_text());coverage=ROOT/cfg['coverage'];source=json.loads(coverage.read_text());base_sha=digest(coverage)
 frozen={str(q):digest(q) for q in (ROOT/'dev/solver/exact_polish.cpp',ROOT/'dev/run_polish.py',a.matrix)}
 report={'matrix':cfg,'matrix_sha256':digest(a.matrix),'coverage_sha256':base_sha,'runner_sha256':digest(Path(__file__)),'workers':1,'rows':[],'complete':False,'scope':'Declared matrix;all results retained. Development and validation comparisons separate. Expansion ceilings are not CPU equality;inherited generation excluded from added-stage time.'};save(a.out,report)
 for item in cfg['cases']:
  tier=item['tier'];start=next(r['run_id'] for r in source['rows'] if r['tier']==tier);suite='benchmarks' if tier=='intro' else 'benchmarks_'+tier
  for label,variant in cfg['variants'].items():
   for seed in cfg['seeds']:
    for name,sha in frozen.items():assert digest(Path(name))==sha
    assert digest(coverage)==base_sha
    command=[sys.executable,str(ROOT/'dev/run_polish.py'),'--suite',suite,'--case',item['case'],'--resume-dir',str(ROOT/'dev/artifacts'/start/'routes'),'--seed',str(seed),'--passes','1000','--budget','60','--work-budget',str(cfg['work_budget'])]
    settings={**cfg.get('common',{}),**item.get('settings',{}),**variant}
    for key,value in settings.items():
     flag='--'+key.replace('_','-')
     if isinstance(value,bool):
      if value:command.append(flag)
     else:command.extend([flag,str(value)])
    before=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'));subprocess.run(command,check=True);paths=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))-before;assert len(paths)==1
    path=paths.pop();m=json.loads(path.read_text());c=m['cases'][0];assert m['success'] and c['legal'] and m['official_inputs_unchanged'];assert c['total_delay']<=c['before_delay'] and c['core']['expansions']<=cfg['work_budget']
    report['rows'].append({'tier':tier,'case':item['case'],'role':item['role'],'label':label,'seed':seed,'run_id':m['run_id'],'manifest_sha256':digest(path),'solver_sha256':m['solver_sha256'],'binary_sha256':m['binary_sha256'],'config':m['config'],'before_delay':c['before_delay'],'delay':c['total_delay'],'core':c['core'],'counters':c['process']['repair_counters'],'wrapper_wall_s':m['wrapper_wall_s'],'output_sha256':c['output_sha256']});save(a.out,report)
 report['comparisons']=[]
 for item in cfg['cases']:
  rows=[r for r in report['rows'] if r['tier']==item['tier'] and r['case']==item['case']]
  for label in cfg['variants']:
   if label==cfg['control']:continue
   counts={'wins':0,'ties':0,'losses':0};ratios=[]
   for seed in cfg['seeds']:
    old=next(r['delay'] for r in rows if (r['label'],r['seed'])==(cfg['control'],seed));new=next(r['delay'] for r in rows if (r['label'],r['seed'])==(label,seed));counts['wins' if new<old else 'losses' if new>old else 'ties']+=1;ratios.append(old/new)
   report['comparisons'].append({'tier':item['tier'],'case':item['case'],'role':item['role'],'label':label,**counts,'geomean_delay_ratio':math.exp(sum(map(math.log,ratios))/len(ratios))})
 for name,sha in frozen.items():assert digest(Path(name))==sha
 assert digest(coverage)==base_sha
 report['complete']=True;report['total_wrapper_wall_s']=sum(r['wrapper_wall_s'] for r in report['rows']);save(a.out,report);print(report['comparisons'])

if __name__=='__main__':main()
