"""Verify compact source patches and replay one declared best own-case variant."""
import argparse,json,subprocess,shutil,tempfile
from pathlib import Path
from measure import ROOT,OFFICIAL,digest,save
import run_polish as bridge

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--archive',type=Path,required=True);p.add_argument('--case',default='hard/case_04');p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();a.out.mkdir(parents=True);archive=json.loads(a.archive.read_text());matched=0
 for i,e in enumerate(archive['entries']):
  source=ROOT/e['parent_source'];patch=ROOT/e['source_patch'];target=a.out/f'source-{i}.cpp';assert digest(patch)==e['patch_sha256']
  if patch.stat().st_size:subprocess.run(['patch','--batch','--silent','--output',str(target),str(source)],input=patch.read_text(),text=True,check=True,capture_output=True)
  else:shutil.copyfile(source,target)
  assert digest(target)==e['source_sha256'];matched+=1
 best=archive['best_own_cases'][a.case];entry=next(e for e in archive['entries'] if e['source_sha256']==best['source_sha256']);report=json.loads((ROOT/best['report']).read_text());row=next(r for r in report['rows'] if r['variant']==best['variant'] and r['case']==a.case.split('/')[1] and r['seed']==best['seed']);v=next(x for x in report['variants'] if x['name']==best['variant']);index=archive['entries'].index(entry);source=a.out/'solver.cpp';shutil.copyfile(a.out/f'source-{index}.cpp',source);binary=a.out/'solver';flags=v['build_command'][1:-3];cmd=['g++',*flags,str(source),'-o',str(binary)]
 with (a.out/'build.log').open('w') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
 item=next(x for x in report['plan']['cases'] if x['tier']+'/'+x['case']==a.case);coverage=json.loads((ROOT/report['plan']['coverage']).read_text());stage=next(x for x in coverage['rows'] if x['tier']==item['tier']);case=OFFICIAL/stage['config']['suite']/(item['case']+'.json');parent=ROOT/'dev/artifacts'/stage['run_id']/'routes'/(item['case']+'.sol.json');assert digest(case)==row['case_sha256'] and digest(parent)==row['parent_sha256'];inst=bridge.Instance.load(case);sub=bridge.Submission.load(parent);bridge.ENGINE=binary;process,raw=bridge.run_core(a.out/'replay',bridge.encode(inst,sub),report['plan']['budget'],best['seed'],1000,item['mode'],report['plan']['work_budget'],item['settings']);assert process['exit_code']==0;out,core=bridge.decode(inst,raw);checked=bridge.check(inst,out);assert checked.legal;target=a.out/'candidate.sol.json';out.save(str(target));assert digest(target)==best['output_sha256'];save(a.out/'report.json',dict(source_entries_matched=matched,case=a.case,variant=best['variant'],source_sha256=digest(source),binary_sha256=digest(binary),binary_hash_matches_original=digest(binary)==v['binary_sha256'],output_sha256=digest(target),output_hash_matches_original=True,legal=True,total_delay=checked.total_delay,core=core,process=process,scope='Source patches all reconstructed;one exact same-hardware/source/work/config replay. Does not prove all variants or end-to-end ancestry regeneration.'));print('source entries',matched,'case replay delay',checked.total_delay,flush=True)
if __name__=='__main__':main()
