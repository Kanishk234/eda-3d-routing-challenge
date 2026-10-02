"""Run fixed complete-tier continuations from an immutable declared plan."""
import argparse,json,subprocess,sys
from pathlib import Path
from measure import ROOT,digest,save

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists()
 plan=json.loads(a.plan.read_text());coverage=ROOT/plan['coverage'];source=json.loads(coverage.read_text());frozen={str(q):digest(q) for q in (coverage,a.plan,ROOT/'dev/solver/exact_polish.cpp',ROOT/'dev/run_polish.py')}
 report={'plan':plan,'plan_sha256':digest(a.plan),'runner_sha256':digest(Path(__file__)),'coverage_sha256':digest(coverage),'workers':1,'rows':[],'complete':False};save(a.out,report)
 for stage in plan['stages']:
  for name,sha in frozen.items():assert digest(Path(name))==sha
  tier=stage['tier'];base=next(r for r in source['rows'] if r['tier']==tier);suite='benchmarks' if tier=='intro' else 'benchmarks_'+tier
  start=stage.get('resume_dir',str(ROOT/'dev/artifacts'/base['run_id']/'routes'))
  command=[sys.executable,str(ROOT/'dev/run_polish.py'),'--suite',suite,'--resume-dir',start]
  for key,value in {**plan.get('common',{}),**stage.get('settings',{})}.items():
   flag='--'+key.replace('_','-')
   if isinstance(value,bool):
    if value:command.append(flag)
   else:command.extend([flag,str(value)])
  before=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'));subprocess.run(command,check=True);paths=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))-before;assert len(paths)==1
  path=paths.pop();m=json.loads(path.read_text());assert m['success'] and m['result']['complete'] and m['official_inputs_unchanged'];assert all(c['legal'] and c['total_delay']<=c['before_delay'] for c in m['cases'])
  counters=[c['process']['repair_counters'] for c in m['cases']]
  report['rows'].append({'tier':tier,'run_id':m['run_id'],'previous_run':base['run_id'],'manifest_sha256':digest(path),'config':m['config'],'score':m['result']['aggregate_score'],'improved_cases':sum(c['total_delay']<c['before_delay'] for c in m['cases']),'n_cases':len(m['cases']),'counters':{k:sum(c.get(k,0) for c in counters) for k in ('eligibility_searches','eligibility_recovered','eligibility_attempts','eligibility_strict','eligibility_neutral','eligibility_gain','eligibility_failed','eligibility_nonimproving','neutral_moves','polish_improvements')},'wrapper_wall_s':m['wrapper_wall_s']});save(a.out,report)
 for name,sha in frozen.items():assert digest(Path(name))==sha
 report['complete']=True;report['total_wrapper_wall_s']=sum(r['wrapper_wall_s'] for r in report['rows']);save(a.out,report)

if __name__=='__main__':main()
