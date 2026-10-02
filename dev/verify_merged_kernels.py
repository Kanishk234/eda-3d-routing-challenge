"""Check unchanged default search outputs across six tier representatives."""
import argparse,json,subprocess,sys
from pathlib import Path
from run_polish import ENGINE,Instance,Submission,encode,decode,check,OFFICIAL
from measure import ROOT,digest,save


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--control',type=Path,required=True);a=p.parse_args()
    coverage=ROOT/'docs/evidence/phase3/tier-all-advance-coverage.json'
    records=[]
    for row in json.loads(coverage.read_text())['rows']:
        suite=json.loads((OFFICIAL/row['config']['suite']/'suite.json').read_text());case=suite['cases'][0]
        inst=Instance.load(OFFICIAL/row['config']['suite']/case['instance_file'])
        path=ROOT/'dev/artifacts'/row['run_id']/'routes'/(case['name']+'.sol.json')
        data=encode(inst,Submission.load(path));outputs=[];stats=[]
        for binary in (a.control,ENGINE):
            command=[str(binary),'60','1','1000','fanout_fine','1000000',
                     *[f'{k}={row["config"][k]}' for k in ('present_initial','present_step','history_step')]]
            run=subprocess.run(command,input=data,text=True,capture_output=True,timeout=65)
            assert run.returncode==0,run.stderr
            out,counters=decode(inst,run.stdout);verified=check(inst,out)
            assert verified.legal and verified.total_delay==counters['total_delay']
            outputs.append(run.stdout);stats.append(counters)
        assert outputs[0]==outputs[1],row['tier']
        records.append({'tier':row['tier'],'case':case['name'],'case_sha256':digest(OFFICIAL/row['config']['suite']/case['instance_file']),
                        'warm_sha256':digest(path),'delay':stats[1]['total_delay'],'expansions':stats[1]['expansions'],'stdout_identical':True})
        print(row['tier'],'identical',flush=True)
    save(ROOT/'docs/evidence/phase3/merge-kernel-verification.json',{'coverage_sha256':digest(coverage),'control_binary_sha256':digest(a.control),
        'merged_binary_sha256':digest(ENGINE),'cases':records,'tests':{'command':'.venv/bin/python dev/test_exact.py','passed':32,
        'log':Path('/tmp/merged-neighborhood-tests.log').read_text(),'source_sha256':digest(ROOT/'dev/test_exact.py')},
        'limitations':'One representative per tier, unchanged fanout_fine preset, fixed1M expansions. Does not prove equivalence of every config or optimality of neighborhood operators.'})


if __name__=='__main__':main()
