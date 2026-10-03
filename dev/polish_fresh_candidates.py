"""Apply bounded native refinement to individually verified own fresh layouts."""
import argparse,json,subprocess,sys,shutil,time
from pathlib import Path
from measure import ROOT,OFFICIAL,digest,save
from run_polish import Instance,Submission,check,ENGINE

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();a.out.mkdir(parents=True);plan=json.loads(a.plan.read_text());frozen={str(p.resolve()):digest(p) for p in [a.plan,Path(__file__),ROOT/'dev/run_polish.py',ROOT/'dev/solver/exact_polish.cpp',ENGINE,ROOT/plan['coverage']]};report=dict(status='running',plan=plan,source_sha256=frozen,rows=[],workers=1,scope='Own fresh inputs with disclosed prior generation plus added native refinement. Comparisons to selected incumbents not matched end-to-end budgets. No automatic promotion.');start=time.monotonic();save(a.out/'progress.json',report)
 for item in plan['items']:
  name=item['case'];inst=Instance.load(OFFICIAL/item['suite']/(name+'.json'));source=ROOT/item['source'];before=check(inst,Submission.load(source));assert before.legal
  directory=a.out/(name+'-'+str(item['seed']))/'routes';directory.mkdir(parents=True);shutil.copyfile(source,directory/(name+'.sol.json'))
  log=a.out/(name+'-'+str(item['seed'])+'.log');cmd=[sys.executable,str(ROOT/'dev/run_polish.py'),'--suite',item['suite'],'--case',name,'--resume-dir',str(directory.resolve()),'--mode','fanout_fine_escape','--seed',str(item['seed']),'--work-budget',str(plan['work_budget']),'--budget',str(plan['budget']),'--passes','1000','--tree-prices','2','--history-step','1','--present-step','1','--accept-equal']
  with log.open('w') as output:subprocess.run(cmd,stdout=output,stderr=subprocess.STDOUT,check=True,timeout=plan['budget']+30)
  paths=[Path(line.removeprefix('manifest: ')) for line in log.read_text().splitlines() if line.startswith('manifest: ')];assert len(paths)==1;m=json.loads(paths[0].read_text());assert m['success'] and m['official_inputs_unchanged'];case=m['cases'][0];assert case['legal'] and case['total_delay']<=before.total_delay
  covered=json.loads((ROOT/plan['coverage']).read_text());tier='intro' if item['suite']=='benchmarks' else item['suite'].removeprefix('benchmarks_');current=next(x for x in covered['rows'] if x['tier']==tier);inc=next(x for x in current['cases'] if x['case']==name)
  report['rows'].append(dict(case=name,seed=item['seed'],source=str(source),source_sha256=digest(source),source_generation_report=item['generation_report'],before_delay=before.total_delay,after_delay=case['total_delay'],selected_delay=inc['total_delay'],run_id=m['run_id'],manifest_sha256=digest(paths[0]),legal=True,expansions=case['core']['expansions'],process=case['process']));save(a.out/'progress.json',report);print(name,item['seed'],before.total_delay,case['total_delay'],'selected',inc['total_delay'],flush=True)
 assert all(digest(Path(p))==h for p,h in frozen.items());report.update(status='complete',wall_s=time.monotonic()-start);save(a.out/'progress.json',report)
if __name__=='__main__':main()
