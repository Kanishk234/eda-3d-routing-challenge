"""Select verified whole-case outputs from a frozen declared local experiment pool."""
import argparse,datetime,json,shutil,time
from pathlib import Path
from measure import ROOT,OFFICIAL,REVISION,digest,save,execute
from run_polish import Instance,Submission,check,score_case,leaderboard
from recombine_routes import ancestor_costs

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--coverage',type=Path,required=True);p.add_argument('--reports',nargs='+',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists()
 coverage=json.loads(a.coverage.read_text());pool=set(r['run_id'] for r in coverage['rows'])
 for report in a.reports:
  data=json.loads(report.read_text());assert data['complete'];pool.update(r['run_id'] for r in data['rows'])
 manifests={run:json.loads((ROOT/'dev/artifacts'/run/'manifest.json').read_text()) for run in pool}
 for m in manifests.values():assert m['success'] and m['official_inputs_unchanged'] and m['upstream_revision']==REVISION
 report={'coverage_sha256':digest(a.coverage),'pool_reports':{str(q):digest(q) for q in a.reports},'source_sha256':digest(Path(__file__)),'pool_manifests':{run:digest(ROOT/'dev/artifacts'/run/'manifest.json') for run in sorted(pool)},'rows':[],'complete':False,'limitations':'Best whole-case output across declared local trials,including partial-suite development trials;benchmark-specific seed/config selection disclosed. Not a matched-budget algorithm comparison or unseen-case result. No public competitor warm starts.'};save(a.out,report)
 for base in coverage['rows']:
  start=time.perf_counter();tier=base['tier'];suite=base['config']['suite'];inventory=json.loads((OFFICIAL/suite/'suite.json').read_text());stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');out=ROOT/'dev/artifacts'/(stamp+'-case-portfolio');(out/'routes').mkdir(parents=True);scores=[];cases=[];relevant=[run for run in sorted(pool) if manifests[run]['config']['suite']==suite]
  for item in inventory['cases']:
   selected=base['run_id'];delay=next(c['total_delay'] for c in manifests[selected]['cases'] if c['case']==item['name'])
   for run in relevant:
    candidate=next((c for c in manifests[run]['cases'] if c['case']==item['name']),None)
    if candidate and candidate['legal'] and candidate['total_delay']<delay:selected,delay=run,candidate['total_delay']
   path=OFFICIAL/suite/item['instance_file'];inst=Instance.load(path);name='routes/'+item['name']+'.sol.json';source=ROOT/'dev/artifacts'/selected/name;m=manifests[selected];c=next(c for c in m['cases'] if c['case']==item['name']);assert c['case_sha256']==digest(path) and digest(source)==m['outputs'][name]
   sub=Submission.load(source);checked=check(inst,sub);assert checked.legal and checked.total_delay==delay;shutil.copyfile(source,out/name);scores.append(score_case(inst,sub,item['baseline_total']));cases.append({'case':item['name'],'source_run':selected,'source_manifest_sha256':report['pool_manifests'][selected],'source_config':m['config'],'case_sha256':digest(path),'total_delay':delay,'output_sha256':digest(out/name),'changed_source':selected!=base['run_id']})
  costs={};missing=set()
  for run in relevant:
   known,absent=ancestor_costs(ROOT/'dev/artifacts'/run)
   for key,value in known.items():
    if key in costs:assert costs[key]==value
    costs[key]=value
   missing.update(absent)
  portfolio={'upstream_revision':REVISION,'suite':suite,'artifact_directory':str(out),'portfolio_selection':True,'method':'Best verified whole-case route across frozen declared local trials','pool_manifests':{run:report['pool_manifests'][run] for run in relevant},'cases':cases,'score':leaderboard(scores).to_dict(),'known_ancestry_runs':costs,'known_ancestry_wrapper_wall_s':sum(costs.values()),'missing_ancestor_artifacts':sorted(missing),'selection_wall_s':time.perf_counter()-start,'source_sha256':digest(Path(__file__)),'limitations':report['limitations']+' Inherited reference-generation costs and missing ancestors remain unknown;selection time excludes independent CLI rescoring.'}
  step=execute([str(ROOT/'.venv/bin/python'),'-m','m3d.cli','score-suite','--suite',suite,'--submission-dir',str(out/'routes'),'--out',str(out/'official-rescore.json')],out,'official-rescore',180);assert step['exit_code']==0;scored=json.loads((out/'official-rescore.json').read_text());assert scored['complete'] and scored['aggregate_score']==portfolio['score']['aggregate_score'];portfolio['official_rescore']=step;save(out/'portfolio.json',portfolio)
  report['rows'].append({'tier':tier,'artifact_directory':str(out),'score':scored['aggregate_score'],'previous_score':base['score']['aggregate_score'],'case_sources_changed':sum(c['changed_source'] for c in cases),'selection_wall_s':portfolio['selection_wall_s'],'portfolio_sha256':digest(out/'portfolio.json')});save(a.out,report);print(tier,scored['aggregate_score'],flush=True)
 report['complete']=True;report['total_selection_wall_s']=sum(r['selection_wall_s'] for r in report['rows']);save(a.out,report)

if __name__=='__main__':main()
