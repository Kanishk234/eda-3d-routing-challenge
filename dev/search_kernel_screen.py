"""Serial matched-work search-kernel comparison; control binary must be supplied."""
import argparse,json,subprocess,time
from pathlib import Path
from run_polish import ENGINE,Instance,Submission,encode,decode,check,OFFICIAL
from measure import ROOT,digest,save,source_identity


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--control',type=Path,required=True);a=p.parse_args()
    coverage=json.loads((ROOT/'docs/evidence/phase3/tier-work-budget-coverage.json').read_text())
    rows=[]
    for tier in ('hard','congested','stress'):
        row=next(r for r in coverage['rows'] if r['tier']==tier)
        suite=json.loads((OFFICIAL/row['config']['suite']/'suite.json').read_text())
        case=next(c for c in suite['cases'] if c['name']=='case_01')
        inst=Instance.load(OFFICIAL/row['config']['suite']/case['instance_file'])
        warm=ROOT/'dev/artifacts'/row['run_id']/'routes/case_01.sol.json';sub=Submission.load(warm)
        data=encode(inst,sub);outputs={}
        for label,binary,mode in [('control',a.control,'fanout_astar'),('heap_g',ENGINE,'fanout_astar'),('tight',ENGINE,'fanout_tight')]:
            for repeat in range(2):
                command=[str(binary),'60','1','1000',mode,'5000000']
                start=time.perf_counter();run=subprocess.run(command,input=data,text=True,capture_output=True,timeout=65)
                wall=time.perf_counter()-start;assert run.returncode==0,run.stderr
                out,stats=decode(inst,run.stdout);verified=check(inst,out);assert verified.legal and verified.total_delay==stats['total_delay']
                counters=json.loads(run.stderr.splitlines()[-1]);outputs.setdefault(label,[]).append(run.stdout)
                rows.append({'tier':tier,'variant':label,'repeat':repeat,'command':command,'binary_sha256':digest(binary),
                             'warm_sha256':digest(warm),'case_sha256':digest(OFFICIAL/row['config']['suite']/case['instance_file']),'wall_s':wall,'stats':stats,'counters':counters})
                print(tier,label,repeat,verified.total_delay,round(wall,3),flush=True)
        assert outputs['control']==outputs['heap_g'], 'heap g changed geometry/work'
        assert all(v[0]==v[1] for v in outputs.values())
    save(ROOT/'docs/evidence/phase3/search-kernel-screen.json',{'source':source_identity(),'rows':rows,'scope':'case_01 hard/congested/stress, fixed5M expansions, seed1, two serial repeats','heap_g_stdout_matches_control':True,'all_repeats_byte_identical':True,'limitations':'Same expansions are not equal CPU cost; tight lookahead can change geometry and completed searches. Representative outputs only, not complete tiers.'})


if __name__=='__main__':main()
