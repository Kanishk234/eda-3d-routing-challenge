"""Fixed all-tier continuation after the eligibility development screen."""
import json,subprocess,sys
from measure import ROOT,digest,save
coverage=ROOT/'docs/evidence/phase3/tier-sampling-fusion-followup-coverage.json';out=ROOT/'docs/evidence/phase3/eligibility-followup.json';assert not out.exists()
source=json.loads(coverage.read_text());report={'coverage_sha256':digest(coverage),'workers':1,'rows':[],'complete':False,'scope':'Added fixed seed1 10M continuation. Escape retained optional after designs2wins/1loss,congested3wins;other tiers fixed exploratory evaluation,no matched superiority claim.'};save(out,report)
for row in source['rows']:
 tier=row['tier'];suite='benchmarks' if tier=='intro' else 'benchmarks_'+tier;cfg=(2,1,1) if tier=='hard' else (2,4,4) if tier=='congested' else (2,2,2)
 cmd=[sys.executable,str(ROOT/'dev/run_polish.py'),'--suite',suite,'--resume-dir',str(ROOT/'dev/artifacts'/row['run_id']/'routes'),'--mode','fanout_fine_escape','--seed','1','--passes','1000','--budget','60','--work-budget','10000000','--group-limit','3' if tier in ('scale','designs','congested') else '13','--present-initial',str(cfg[0]),'--present-step',str(cfg[1]),'--history-step',str(cfg[2])]
 if tier in ('hard','designs','congested'):cmd+=['--accept-equal']
 before=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'));subprocess.run(cmd,check=True);paths=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))-before;assert len(paths)==1
 p=paths.pop();m=json.loads(p.read_text());assert m['success'] and m['result']['complete'] and m['official_inputs_unchanged'];assert all(c['legal'] and c['total_delay']<=c['before_delay'] for c in m['cases'])
 report['rows'].append({'tier':tier,'run_id':m['run_id'],'previous_run':row['run_id'],'manifest_sha256':digest(p),'config':m['config'],'score':m['result']['aggregate_score'],'improved_cases':sum(c['total_delay']<c['before_delay'] for c in m['cases']),'eligibility_searches':sum(c['process']['repair_counters']['eligibility_searches'] for c in m['cases']),'eligibility_recovered':sum(c['process']['repair_counters']['eligibility_recovered'] for c in m['cases']),'wrapper_wall_s':m['wrapper_wall_s']});save(out,report)
report['complete']=True;report['total_wrapper_wall_s']=sum(r['wrapper_wall_s'] for r in report['rows']);save(out,report)
