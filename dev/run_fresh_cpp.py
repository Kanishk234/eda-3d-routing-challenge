"""Bounded compiled fresh negotiation screen with official physical checks."""
import argparse,json,subprocess,time,resource
from pathlib import Path
from measure import ROOT,OFFICIAL,digest,save
from run_polish import Instance,Submission,check,encode,decode
BINARY=ROOT/'dev/artifacts/build/fresh_probe'
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out=a.out.resolve();assert not a.out.exists();a.out.mkdir(parents=True);plan=json.loads(a.plan.read_text());coverage=json.loads((ROOT/plan['coverage']).read_text());frozen={str(p.resolve()):digest(p) for p in [a.plan,Path(__file__),BINARY,ROOT/'dev/solver/fresh_probe.cpp',ROOT/'dev/solver/exact_polish.cpp',ROOT/plan['coverage']]};report=dict(status='running',plan=plan,source_sha256=frozen,compiler_flags=['-std=c++17','-O3','-DNDEBUG','-Wall','-Wextra'],compiler_version=subprocess.check_output(['g++','--version'],text=True).splitlines()[0],rows=[],workers=1,scope='Fresh geometry ignores all supplied incumbent edges. Input remains legal recovery only. Fixed-point64 congestion and ceil sqrt fanout differ from Python probe. Each fresh result officially checked; incomplete states use input fallback and are not labeled fresh. No matched-budget comparison against long incumbent portfolios.');save(a.out/'progress.json',report);start=time.monotonic()
 for case in plan['cases']:
  inst_path=OFFICIAL/case['suite']/case['file'];inst=Instance.load(inst_path);tier='intro' if case['suite']=='benchmarks' else case['suite'].removeprefix('benchmarks_');parent=next(x for x in coverage['rows'] if x['tier']==tier);base=ROOT/'dev/artifacts'/parent['run_id']/'routes'/(inst.name+'.sol.json');sub=Submission.load(base);before=check(inst,sub);assert before.legal
  for seed in plan['seeds']:
   for setting in plan['variants']:
    cmd=[str(BINARY),str(plan['budget']),str(seed),str(plan['rounds']),str(plan['work_budget']),setting['schedule'],str(int(setting['conflict_only'])),str(plan['polish_passes'])];begin=time.monotonic();p=subprocess.run(cmd,input=encode(inst,sub),text=True,capture_output=True,timeout=plan['budget']+10);assert p.returncode==0,p.stderr
    out,core=decode(inst,p.stdout);checked=check(inst,out);assert checked.legal and checked.total_delay==core['total_delay'];fresh=next(x for x in p.stderr.splitlines() if x.startswith('FRESH ')).split();success=bool(int(fresh[1]));target=None
    if success:
     target=a.out/f'{tier}-{inst.name}-{seed}-{setting["schedule"]}-{int(setting["conflict_only"])}.sol.json';out.save(str(target));assert check(inst,Submission.load(str(target))).legal
    else:assert out.to_dict()==sub.to_dict()
    row=dict(case=case,case_sha256=digest(inst_path),input_sha256=digest(base),seed=seed,variant=setting,fresh_legal=success,delay=checked.total_delay if success else None,selected_delay=before.total_delay,rounds=int(fresh[2]),routed_nets=int(fresh[3]),expansions=core['expansions'],core=core,wall_s=time.monotonic()-begin,output_sha256=digest(target) if target else None,output=str(target.relative_to(ROOT)) if target else None);report['rows'].append(row);save(a.out/'progress.json',report);print(tier,inst.name,seed,setting,success,row['delay'],'selected',before.total_delay,flush=True)
 assert all(digest(Path(p))==h for p,h in frozen.items());report.update(status='complete',wall_s=time.monotonic()-start,wrapper_peak_rss_kb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);save(a.out/'progress.json',report)
if __name__=='__main__':main()
