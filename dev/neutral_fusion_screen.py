"""Matched archive sweeps: strict fusion versus neutral donor-preferring fusion."""
import datetime,json,time
from measure import ROOT,OFFICIAL,REVISION,digest,save,execute
from run_polish import Instance,Submission,check,score_case,leaderboard
from recombine_routes import recombine
selection=ROOT/'dev/incumbents/selected.json';inventory=ROOT/'docs/evidence/phase3/diversity-inventory.json'
s=json.loads(selection.read_text());i=json.loads(inventory.read_text());reportpath=ROOT/'docs/evidence/phase3/neutral-fusion-screen.json';assert not reportpath.exists()
report={'selection_sha256':digest(selection),'inventory_sha256':digest(inventory),'workers':1,'rounds':2,'rows':[],'complete':False,'limitations':'Same fixed archive,order and rounds; no new path search. Exactness only per two-parent fusion,not whole-pool/global optimization. Neutral fusion can cycle;two sweeps bound effort.'};save(reportpath,report)
for tier in ('designs','congested'):
 base=ROOT/'dev/artifacts'/next(x['run_id'] for x in s['tiers'] if x['tier']==tier)
 donors=[ROOT/'dev/artifacts'/x['run_id'] for x in i['tiers'][tier]['candidates']];runs=[base,*donors];manifests=[json.loads((r/'manifest.json').read_text()) for r in runs]
 cases=json.loads((OFFICIAL/('benchmarks_'+tier)/'suite.json').read_text())['cases'];inputs={};instances={};parents={}
 for c in cases:
  path=OFFICIAL/('benchmarks_'+tier)/c['instance_file'];inputs[str(path)]=digest(path);instances[c['name']]=Instance.load(path);name='routes/'+c['name']+'.sol.json'
  parents[c['name']]=[]
  for r,m in zip(runs,manifests):assert digest(r/name)==m['outputs'][name];parents[c['name']].append(Submission.load(r/name))
 for preference in (False,True):
  start=time.perf_counter();out=ROOT/'dev/artifacts'/(datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')+'-neutral-fusion');(out/'routes').mkdir(parents=True)
  portfolio={'upstream_revision':REVISION,'suite':'benchmarks_'+tier,'artifact_directory':str(out),'portfolio_selection':True,'prefer_donor':preference,'rounds':2,'sources':[{'directory':str(r),'manifest_sha256':digest(r/'manifest.json')} for r in runs],'cases':[],'limitations':report['limitations']};scores=[]
  for c in cases:
   inst=instances[c['name']];original=parents[c['name']][0];current=original;trace=[]
   for sweep in range(2):
    for k,donor in enumerate(parents[c['name']][1:],1):
     candidate,row=recombine(inst,current,donor,preference);trace.append({'sweep':sweep,'source_index':k,**row});current=candidate
   name='routes/'+c['name']+'.sol.json';current.save(out/name);checked=check(inst,current);assert checked.legal and checked.total_delay<=check(inst,original).total_delay
   scores.append(score_case(inst,current,c['baseline_total']));portfolio['cases'].append({'case':c['name'],'case_sha256':inputs[str(OFFICIAL/('benchmarks_'+tier)/c['instance_file'])],'base_delay':check(inst,original).total_delay,'total_delay':checked.total_delay,'output_sha256':digest(out/name),'trace':trace})
   print(tier,preference,c['name'],'gain',portfolio['cases'][-1]['base_delay']-checked.total_delay,flush=True)
  assert all(digest(__import__('pathlib').Path(path))==sha for path,sha in inputs.items())
  costs={};missing=set()
  for r,m in zip(runs,manifests):
   while True:
    costs[m['run_id']]=m['wrapper_wall_s'];origin=__import__('pathlib').Path(m['warm_start']['directory']);p=origin.parent/'manifest.json'
    if not p.exists():
     inherited=origin.parent/'portfolio.json'
     if inherited.exists():costs.update(json.loads(inherited.read_text()).get('known_ancestry_runs',{}))
     if not origin.exists():missing.add(str(origin))
     break
    m=json.loads(p.read_text())
  portfolio.update(score=leaderboard(scores).to_dict(),known_ancestry_wrapper_wall_s=sum(costs.values()),known_ancestry_runs=costs,missing_ancestor_artifacts=sorted(missing),selection_wall_s=time.perf_counter()-start,source_sha256=digest(ROOT/'dev/neutral_fusion_screen.py'),closure_source_sha256=digest(ROOT/'dev/recombine_routes.py'))
  portfolio['official_rescore_process']=execute([str(ROOT/'.venv/bin/python'),'-m','m3d.cli','score-suite','--suite','benchmarks_'+tier,'--submission-dir',str(out/'routes'),'--out',str(out/'official-rescore.json')],out,'official-rescore',180)
  assert portfolio['official_rescore_process']['exit_code']==0;official=json.loads((out/'official-rescore.json').read_text());assert official['complete'] and official['aggregate_score']==portfolio['score']['aggregate_score']
  save(out/'portfolio.json',portfolio);report['rows'].append({'tier':tier,'preference':preference,'artifact_directory':str(out),'score':portfolio['score']['aggregate_score'],'selection_wall_s':portfolio['selection_wall_s'],'portfolio_sha256':digest(out/'portfolio.json'),'cases':portfolio['cases']});save(reportpath,report)
report['complete']=True;report['total_selection_wall_s']=sum(r['selection_wall_s'] for r in report['rows']);save(reportpath,report)
