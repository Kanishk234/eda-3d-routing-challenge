"""Bounded independent full-tier comparisons; scores remain separate by tier."""
import argparse,json,subprocess,sys,os,time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from measure import ROOT,OFFICIAL,digest,save

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out=a.out.resolve();assert not a.out.exists();a.out.mkdir(parents=True);plan=json.loads(a.plan.read_text());assert 1<=plan['workers']<=3 and plan['workers']<=len(os.sched_getaffinity(0))//2;available=int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))*1024;assert available>=2*1024**3+plan['workers']*512*1024**2;frozen={str(q.resolve()):digest(q) for q in [a.plan,Path(__file__),ROOT/'dev/evolution_pilot.py',ROOT/'dev/solver/exact_polish.cpp',ROOT/'dev/run_polish.py',ROOT/plan['coverage']]};report=dict(status='running',plan=plan,frozen_sha256=frozen,workers=plan['workers'],rows=[],scope='Independent within-tier source-variant comparisons. All cases in each requested tier,two declared seeds;no combined six-tier ranking,no automatic incumbent adoption. Concurrent jobs invalidate isolated wall timing.');save(a.out/'progress.json',report);start=time.monotonic()
 def task(item):
  tier=item['tier'];suite='benchmarks' if tier=='intro' else 'benchmarks_'+tier;cases=json.loads((OFFICIAL/suite/'suite.json').read_text())['cases'];settings=item['settings'].copy();mode=settings.pop('mode');settings={k:int(v) if isinstance(v,bool) else v for k,v in settings.items()};child=dict(coverage=plan['coverage'],variants=plan['variants'],seeds=plan['seeds'],work_budget=plan['work_budget'],budget=60,cases=[dict(tier=tier,case=x['name'],mode=mode,settings=settings) for x in cases],scope='Full '+tier+' matched delayed-order comparison,allcases,two seeds,50M/case;fixed parent.');path=a.out/(tier+'-plan.json');save(path,child);folder=a.out/tier
  with (a.out/(tier+'.log')).open('w') as log:subprocess.run([sys.executable,str(ROOT/'dev/evolution_pilot.py'),str(path),'--out',str(folder)],stdout=log,stderr=subprocess.STDOUT,check=True)
  r=json.loads((folder/'progress.json').read_text());assert r['status']=='complete';assert all(digest(Path(p))==h for p,h in frozen.items());return dict(tier=tier,report=str(folder/'progress.json'),report_sha256=digest(folder/'progress.json'),comparisons=r['comparisons'])
 try:
  with ThreadPoolExecutor(max_workers=plan['workers']) as pool:
   for job in as_completed([pool.submit(task,x) for x in plan['tiers']]):
    row=job.result();report['rows'].append(row);save(a.out/'progress.json',report);print(row['tier'],row['comparisons'],flush=True)
  report.update(status='complete',wall_s=time.monotonic()-start);save(a.out/'progress.json',report)
 except BaseException as error:report.update(status='failed',error=repr(error),wall_s=time.monotonic()-start);save(a.out/'progress.json',report);raise
if __name__=='__main__':main()
