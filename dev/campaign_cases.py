"""Bounded independent own-case walks; preserve every checked result and cost."""
import argparse,json,os,subprocess,sys,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
from measure import ROOT,OFFICIAL,digest,save

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out=a.out.resolve();assert not a.out.exists();a.out.mkdir(parents=True);plan=json.loads(a.plan.read_text());coverage=json.loads((ROOT/plan['coverage']).read_text());workers=plan['workers'];affinity=len(os.sched_getaffinity(0));available=int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))*1024
 assert 1<=workers<=max(1,affinity-4);assert available>=plan['per_worker_ram_reservation']*workers+2*1024**3;assert 0<plan['budget']<=300 and 0<plan['work_budget']<=500000000
 for item in plan['cases']:
  stage=next(x for x in coverage['rows'] if x['tier']==item['tier']); names={x['name'] for x in json.loads((OFFICIAL/stage['config']['suite']/'suite.json').read_text())['cases']};assert item['case'] in names, f"Unknown {item['tier']} case: {item['case']}"
 frozen={str(p.resolve()):digest(p) for p in [a.plan,Path(__file__),ROOT/plan['coverage'],ROOT/'dev/run_polish.py',ROOT/'dev/solver/exact_polish.cpp',ROOT/'dev/artifacts/build/exact_polish']};tasks=[(item,seed) for item in plan['cases'] for seed in plan['seeds']];start=time.monotonic();report=dict(complete=False,status='running',plan=plan,source_sha256=frozen,workers=workers,available_ram_bytes=available,affinity_cpus=affinity,rows=[],errors=[],planned_max_core_seconds=len(tasks)*plan['budget'],scope='Independent own incumbent walks,matched per-task ceilings; added parallel portfolio effort,not isolated timings. All candidates officially checked. No automatic canonical promotion.');save(a.out/'progress.json',report)
 def task(item,seed):
  if (a.out/'STOP').exists():return None
  assert all(digest(Path(p))==h for p,h in frozen.items());stage=next(x for x in coverage['rows'] if x['tier']==item['tier']);args=[sys.executable,str(ROOT/'dev/run_polish.py'),'--suite',stage['config']['suite'],'--case',item['case'],'--resume-dir',str(ROOT/'dev/artifacts'/stage['run_id']/'routes'),'--seed',str(seed),'--passes','1000','--budget',str(plan['budget']),'--work-budget',str(plan['work_budget'])]
  for k,v in item['settings'].items():
   flag='--'+k.replace('_','-')
   if isinstance(v,bool):
    if v:args.append(flag)
   else:args.extend([flag,str(v)])
  log=a.out/f'{item["tier"]}-{item["case"]}-{seed}.log'
  with log.open('w') as f:subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=plan['budget']+45)
  paths=[Path(x.removeprefix('manifest: ')) for x in log.read_text().splitlines() if x.startswith('manifest: ')];assert len(paths)==1;m=json.loads(paths[0].read_text());assert m['success'] and m['official_inputs_unchanged'];c=m['cases'][0];assert c['legal'] and c['total_delay']<=c['before_delay'];assert all(digest(Path(p))==h for p,h in frozen.items())
  return dict(tier=item['tier'],case=item['case'],seed=seed,run_id=m['run_id'],manifest_sha256=digest(paths[0]),before_delay=c['before_delay'],after_delay=c['total_delay'],expansions=c['core']['expansions'],legal=True,wrapper_wall_s=m['wrapper_wall_s'],peak_core_rss_kib=c['process']['peak_rss_kib'])
 try:
  with ThreadPoolExecutor(max_workers=workers) as executor:
   for job in as_completed([executor.submit(task,item,seed) for item,seed in tasks]):
    try:row=job.result()
    except Exception as error:
     report['errors'].append(repr(error));report['elapsed_wall_s']=time.monotonic()-start;save(a.out/'progress.json',report);continue
    if row:report['rows'].append(row);report['elapsed_wall_s']=time.monotonic()-start;save(a.out/'progress.json',report);print(row['tier'],row['case'],row['seed'],'gain',row['before_delay']-row['after_delay'],flush=True)
  report.update(complete=len(report['rows'])==len(tasks),status='complete' if len(report['rows'])==len(tasks) else ('failed' if report['errors'] else 'stopped'),elapsed_wall_s=time.monotonic()-start);save(a.out/'progress.json',report)
 except BaseException as e:report.update(status='failed',error=repr(e));save(a.out/'progress.json',report);raise
if __name__=='__main__':main()
