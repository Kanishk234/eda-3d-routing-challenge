"""Exact pairwise archive recombination with disclosed per-case selection."""
import json,datetime,time,sys
from pathlib import Path
from recombine_routes import recombine
from measure import ROOT,OFFICIAL,REVISION,digest,save,execute
from run_polish import Instance,Submission,check,score_case,leaderboard
inventory=ROOT/'docs/evidence/phase3/diversity-inventory.json'
followup=json.loads((ROOT/'docs/evidence/phase3/diversity-followup.json').read_text())
for tier,entry in json.loads(inventory.read_text())['tiers'].items():
 reportpath=ROOT/'docs/evidence/phase3'/(tier+'-archive-recombination.json');assert not reportpath.exists()
 start=time.perf_counter();base=ROOT/'dev/artifacts'/next(x['run_id'] for x in followup['rows'] if x['tier']==tier)
 donors=[ROOT/'dev/artifacts'/x['run_id'] for x in entry['candidates']];runs=[base,*donors];manifests=[json.loads((r/'manifest.json').read_text()) for r in runs]
 assert all(m['success'] and m['result']['complete'] and m['config']['suite']=='benchmarks_'+tier for m in manifests)
 out=ROOT/'dev/artifacts'/(datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')+'-archive-recombination');(out/'routes').mkdir(parents=True)
 report={'upstream_revision':REVISION,'suite':'benchmarks_'+tier,'artifact_directory':str(out),'portfolio_selection':True,'inventory_sha256':digest(inventory),'sources':[{'directory':str(r),'manifest_sha256':digest(r/'manifest.json')} for r in runs],'cases':[],'limitations':'Each pair optimized exactly for its two candidate trees per net. Best pair chosen per case;not global optimization over the whole archive or fresh routing. All historical candidate-generation costs count separately.'}
 scores=[];inputs={}
 for c in json.loads((OFFICIAL/('benchmarks_'+tier)/'suite.json').read_text())['cases']:
  case=OFFICIAL/('benchmarks_'+tier)/c['instance_file'];inputs[str(case)]=digest(case);inst=Instance.load(case);name='routes/'+c['name']+'.sol.json'
  assert digest(base/name)==manifests[0]['outputs'][name]
  original=Submission.load(base/name);best=original;delay=check(inst,original).total_delay;chosen=None;trials=[]
  for index,(donor,m) in enumerate(zip(donors,manifests[1:])):
   assert digest(donor/name)==m['outputs'][name]
   result,row=recombine(inst,original,Submission.load(donor/name));trials.append({'donor_index':index+1,**row})
   if row['total_delay']<delay:best=result;delay=row['total_delay'];chosen=index+1
  best.save(out/name);scores.append(score_case(inst,best,c['baseline_total']))
  report['cases'].append({'case':c['name'],'case_sha256':digest(case),'total_delay':delay,'base_delay':check(inst,original).total_delay,'chosen_source_index':chosen,'trials':trials,'output_sha256':digest(out/name)})
  print(tier,c['name'],'recombination gain',report['cases'][-1]['base_delay']-delay,flush=True)
 assert all(digest(Path(path))==sha for path,sha in inputs.items())
 costs={};missing=set()
 for r,m in zip(runs,manifests):
  while True:
   costs[m['run_id']]=m['wrapper_wall_s'];origin=Path(m['warm_start']['directory']);parent=origin.parent/'manifest.json'
   if not parent.exists():
    if not origin.exists():missing.add(str(origin))
    break
   m=json.loads(parent.read_text())
 report.update(score=leaderboard(scores).to_dict(),known_ancestry_wrapper_wall_s=sum(costs.values()),known_ancestry_runs=costs,missing_ancestor_artifacts=sorted(missing),selection_wall_s=time.perf_counter()-start,source_sha256=digest(Path(__file__)),closure_source_sha256=digest(ROOT/'dev/recombine_routes.py'))
 report['official_rescore_process']=execute([str(ROOT/'.venv/bin/python'),'-m','m3d.cli','score-suite','--suite','benchmarks_'+tier,'--submission-dir',str(out/'routes'),'--out',str(out/'official-rescore.json')],out,'official-rescore',180)
 assert report['official_rescore_process']['exit_code']==0;official=json.loads((out/'official-rescore.json').read_text());assert official['complete'] and official['aggregate_score']==report['score']['aggregate_score']
 save(out/'portfolio.json',report);save(reportpath,report)
 print('score',tier,report['score']['aggregate_score'],flush=True)
