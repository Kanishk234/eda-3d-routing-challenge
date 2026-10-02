"""Bounded continuation portfolio;each completed round is officially rescored."""
import argparse,datetime,json,os,subprocess,sys,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
from measure import ROOT,digest,save

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();a.out.mkdir(parents=True)
 plan=json.loads(a.plan.read_text());assert 1<=len(plan['seeds'])<=20 and 0<plan['work_budget']<=100000000
 coverage=ROOT/plan['coverage'];initial=json.loads(coverage.read_text());best={r['tier']:{'run_id':r['run_id'],'score':r['score']['aggregate_score']} for r in initial['rows']}
 paths=[coverage,a.plan,Path(__file__),ROOT/'dev/solver/exact_polish.cpp',ROOT/'dev/run_polish.py',ROOT/'dev/artifacts/build/exact_polish']
 frozen={str(q.resolve()):digest(q) for q in paths}
 workers=plan.get('workers',1);assert 1<=workers<=2 and workers<=len(os.sched_getaffinity(0))
 state={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'plan':plan,'frozen_sha256':frozen,'workers':workers,'status':'running','completed_rounds':0,'current':None,'best':best,'stages':[],'round_coverages':[],'limitations':'Added portfolio search,not matched-budget superiority. No publication or automatic canonical-selection edits. Stops between tiers if STOP file appears or frozen source/binary changes. Missing historical/reference-generation costs remain unknown.'};save(a.out/'progress.json',state)
 start=time.perf_counter()
 try:
  def run_stage(item,seed,round_index):
    if (a.out/'STOP').exists():return None
    for name,sha in frozen.items():
     if digest(Path(name))!=sha:raise RuntimeError('Frozen input changed: '+name)
    tier=item['tier'];previous=best[tier].copy();suite='benchmarks' if tier=='intro' else 'benchmarks_'+tier
    command=[sys.executable,str(ROOT/'dev/run_polish.py'),'--suite',suite,'--resume-dir',str(ROOT/'dev/artifacts'/previous['run_id']/'routes'),'--seed',str(seed),'--passes','1000','--budget','60','--work-budget',str(plan['work_budget'])]
    for key,value in item['settings'].items():
     flag='--'+key.replace('_','-')
     if isinstance(value,bool):
      if value:command.append(flag)
     else:command.extend([flag,str(value)])
    log=a.out/f'round-{round_index}-{tier}.log'
    with log.open('w') as output:subprocess.run(command,stdout=output,stderr=subprocess.STDOUT,check=True)
    found=[line.removeprefix('manifest: ') for line in log.read_text().splitlines() if line.startswith('manifest: ')];assert len(found)==1;path=Path(found[0]);m=json.loads(path.read_text())
    for name,sha in frozen.items():
     if digest(Path(name))!=sha:raise RuntimeError('Frozen input changed: '+name)
    assert m['success'] and m['result']['complete'] and m['official_inputs_unchanged'];assert all(c['legal'] and c['total_delay']<=c['before_delay'] for c in m['cases']);score=m['result']['aggregate_score'];assert score>=previous['score']
    return {'round':round_index,'tier':tier,'seed':seed,'run_id':m['run_id'],'previous_run':previous['run_id'],'manifest_sha256':digest(path),'score':score,'improved_cases':sum(c['total_delay']<c['before_delay'] for c in m['cases']),'wrapper_wall_s':m['wrapper_wall_s']}
  for round_index,seed in enumerate(plan['seeds'],1):
   state['current']={'round':round_index,'seed':seed,'scheduled_tiers':[x['tier'] for x in plan['tiers']]};save(a.out/'progress.json',state)
   with ThreadPoolExecutor(max_workers=workers) as executor:
    jobs=[executor.submit(run_stage,item,seed,round_index) for item in plan['tiers']]
    for job in as_completed(jobs):
     row=job.result()
     if row is None:continue
     best[row['tier']]={'run_id':row['run_id'],'score':row['score']};state['best']=best;state['stages'].append(row);state['elapsed_wall_s']=time.perf_counter()-start;save(a.out/'progress.json',state)
   if (a.out/'STOP').exists():state['status']='stopped';state['current']=None;save(a.out/'progress.json',state);return 0
   target=a.out/f'round-{round_index}-coverage.json'
   subprocess.run([sys.executable,str(ROOT/'dev/report_tiers.py'),*[str(ROOT/'dev/artifacts'/best[item['tier']]['run_id']) for item in plan['tiers']],'--out',str(target)],check=True)
   state['round_coverages'].append({'round':round_index,'path':str(target.resolve()),'sha256':digest(target)});state['completed_rounds']=round_index;state['current']=None;save(a.out/'progress.json',state)
  state['status']='complete';state['elapsed_wall_s']=time.perf_counter()-start;save(a.out/'progress.json',state)
 except BaseException as error:
  state['status']='failed';state['error']=repr(error);state['elapsed_wall_s']=time.perf_counter()-start;save(a.out/'progress.json',state);raise

if __name__=='__main__':raise SystemExit(main())
