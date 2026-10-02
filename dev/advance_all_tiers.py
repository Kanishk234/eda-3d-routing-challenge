"""Bounded serial all-tier improvement stages with explicit incumbent ancestry."""
import argparse,json,re,subprocess,sys
from pathlib import Path
from measure import ROOT,digest,save


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--coverage',type=Path,default=ROOT/'docs/evidence/phase3/tier-schedule-coverage.json')
    parser.add_argument('--label',default='all-tier-advance')
    args=parser.parse_args()
    if not re.fullmatch(r'[a-z0-9-]+',args.label): parser.error('label must use lowercase letters, digits and hyphens')
    coverage=args.coverage
    destination=ROOT/'docs/evidence/phase3'/(args.label+'.json')
    score_report=ROOT/'docs/evidence/phase3'/('tier-'+args.label+'-coverage.json')
    if destination.exists() or score_report.exists(): parser.error('use a new label to preserve prior evidence')
    starting=json.loads(coverage.read_text())['rows']
    selected={r['tier']:r['run_id'] for r in starting}
    schedules={'hard':(2,1,1),'congested':(2,4,4)}
    report={'input_coverage_sha256':digest(coverage),'workers':1,'scope':'All six separately scored tiers. Two bounded stages; fixed configs per tier, no public warm starts or per-case candidate selection.',
            'rows':[],'selected_runs':selected,'limitations':'Incremental incumbent improvement, not fresh generation or a globally optimal score claim. All experiments/stages count toward total search effort.'}
    stages=[(1,5000000,('intro','scale','designs','stress')),(2,10000000,('intro','hard','scale','congested','designs','stress'))]
    for seed,work,tiers in stages:
        for tier in tiers:
            previous=selected[tier];cfg=schedules.get(tier,(2,2,2))
            suite='benchmarks' if tier=='intro' else 'benchmarks_'+tier
            before=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))
            command=[sys.executable,str(ROOT/'dev/run_polish.py'),'--suite',suite,'--resume-dir',str(ROOT/'dev/artifacts'/previous/'routes'),
                '--mode','fanout_fine','--seed',str(seed),'--passes','1000','--budget','60','--work-budget',str(work),
                '--present-initial',str(cfg[0]),'--present-step',str(cfg[1]),'--history-step',str(cfg[2])]
            subprocess.run(command,check=True)
            paths=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))-before
            assert len(paths)==1;path=paths.pop();m=json.loads(path.read_text())
            assert m['success'] and m['result']['complete'] and m['official_inputs_unchanged']
            assert all(c['total_delay']<=c['before_delay'] for c in m['cases'])
            selected[tier]=m['run_id']
            report['rows'].append({'tier':tier,'previous_run':previous,'run_id':m['run_id'],'manifest_sha256':digest(path),
                'config':m['config'],'score':m['result'],'cases':[{**c,'core':{k:v for k,v in c.get('core',{}).items() if k!='net_delays'}} for c in m['cases']],'wrapper_wall_s':m['wrapper_wall_s'],
                'source_identity':m['source']['files_sha256']})
            save(destination,report)
    report['complete']=True;report['total_wrapper_wall_s']=sum(r['wrapper_wall_s'] for r in report['rows']);save(destination,report)
    subprocess.run([sys.executable,str(ROOT/'dev/report_tiers.py'),*[str(ROOT/'dev/artifacts'/selected[tier]) for tier in ('intro','hard','scale','congested','designs','stress')],
        '--out',str(score_report)],check=True)


if __name__=='__main__':main()
