"""Serial fixed-work negotiation-schedule screen on declared representatives."""
import json,subprocess,sys
from measure import ROOT,digest,save


def main():
    coverage=ROOT/'docs/evidence/phase3/tier-pricing-coverage.json'
    selected=json.loads(coverage.read_text())['rows']
    destination=ROOT/'docs/evidence/phase3/schedule-screen.json'
    report={'coverage_sha256':digest(coverage),'workers':1,'work_budget':5000000,'wall_safety_cap':60,'rows':[],
            'scope':'Hard/congested case01; seeds1–3; matched5M expanded vertices; four declared present/history schedules. Reserved hard08/09 excluded from selection.',
            'limitations':'Expanded vertices do not equate CPU cost. Incremental warm starts; no full-tier score or guaranteed congestion-cost optimization.'}
    for tier in ('hard','congested'):
        start=next(r for r in selected if r['tier']==tier)
        for seed in (1,2,3):
            for schedule in ((2,2,2),(2,1,1),(2,4,4),(2,2,8)):
                mode='fanout_fine'
                before=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))
                subprocess.run([sys.executable,str(ROOT/'dev/run_polish.py'),'--suite','benchmarks_'+tier,
                    '--case','case_01','--resume-dir',str(ROOT/'dev/artifacts'/start['run_id']/'routes'),
                    '--present-initial',str(schedule[0]),'--present-step',str(schedule[1]),'--history-step',str(schedule[2]),
                    '--mode',mode,'--seed',str(seed),'--passes','1000','--budget','60','--work-budget','5000000'],check=True)
                paths=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))-before
                assert len(paths)==1;path=paths.pop();m=json.loads(path.read_text());assert m['success'] and m['official_inputs_unchanged']
                report['rows'].append({'tier':tier,'seed':seed,'mode':mode,'run_id':m['run_id'],'manifest_sha256':digest(path),
                    'schedule':schedule,'source_identity':m['source']['files_sha256'],'case':m['cases'][0],'wrapper_wall_s':m['wrapper_wall_s']})
                save(destination,report)
    report['complete']=True;report['total_wrapper_wall_s']=sum(r['wrapper_wall_s'] for r in report['rows'])
    save(destination,report)


if __name__=='__main__':main()
