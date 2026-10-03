"""Select legal own experimental outputs into complete reproducible tier archives.
This is whole-case portfolio selection, not promotion of a solver default.
"""
import argparse,json,shutil,subprocess,sys
from pathlib import Path
from measure import ROOT,OFFICIAL,digest,save
from run_polish import Instance,Submission,check

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--coverage',type=Path,required=True);p.add_argument('--reports',nargs='+',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--label',required=True);p.add_argument('--select',action='store_true');a=p.parse_args();a.out=a.out.resolve();assert not a.out.exists();a.out.mkdir(parents=True);base=json.loads(a.coverage.read_text());old=json.loads((ROOT/'dev/incumbents/selected.json').read_text());pool={};report_hashes={};search_cost=0
 for path in a.reports:
  r=json.loads(path.read_text());assert r['status']=='complete';report_hashes[str(path)]=digest(path)
  for row in r['rows']:
   search_cost+=row['process']['wall_s'];key=(row['tier'],row['case']);source=Path(row['process']['command'][0]).parent/f'{row["tier"]}-{row["case"]}-{row["seed"]}'/'candidate.sol.json';assert row['legal'] and digest(source)==row['output_sha256'];variant=next(v for v in r['variants'] if v['name']==row['variant']);cpp=Path(next(x for x in variant['build_command'] if x.endswith('.cpp')));assert digest(cpp)==variant['source_sha256'];entry=dict(row=row,report=str(path),route=source,source=cpp,variant=variant)
   if key not in pool or row['delay']<pool[key]['row']['delay']:pool[key]=entry
 result=dict(complete=False,coverage_sha256=digest(a.coverage),reports=report_hashes,known_experimental_core_wall_s=search_cost,rows=[],scope='Best legal whole-case portfolio from own completed source-variant trials and previous own coverage. Added search and per-case selection,not uniform-budget solver comparison. No competitor routes. Inherited search costs remain separate/partly unknown.');save(a.out/'report.json',result);runs=[]
 for stage in base['rows']:
  tier=stage['tier'];suite=stage['config']['suite'];inv=json.loads((OFFICIAL/suite/'suite.json').read_text());warm=a.out/tier/'warm';warm.mkdir(parents=True);selections=[];base_manifest=json.loads((ROOT/'dev/artifacts'/stage['run_id']/'manifest.json').read_text())
  for case in inv['cases']:
   name=case['name'];inst=Instance.load(OFFICIAL/suite/case['instance_file']);source=ROOT/'dev/artifacts'/stage['run_id']/'routes'/(name+'.sol.json');assert digest(source)==base_manifest['outputs']['routes/'+name+'.sol.json'];before=check(inst,Submission.load(source));assert before.legal;chosen=pool.get((tier,name));metadata=dict(case=name,previous_run=stage['run_id'],previous_delay=before.total_delay,selected_delay=before.total_delay,changed=False)
   if chosen and chosen['row']['delay']<before.total_delay:
    row=chosen['row'];assert digest(OFFICIAL/suite/case['instance_file'])==row['case_sha256'];checked=check(inst,Submission.load(chosen['route']));assert checked.legal and checked.total_delay==row['delay'];source=chosen['route'];metadata.update(changed=True,selected_delay=row['delay'],experiment_report=chosen['report'],variant=row['variant'],seed=row['seed'],source_sha256=chosen['variant']['source_sha256'],output_sha256=row['output_sha256'],work_expansions=row['core']['expansions'])
   shutil.copyfile(source,warm/(name+'.sol.json'));selections.append(metadata)
  log=a.out/tier/'checkpoint.log'
  with log.open('w') as stream:subprocess.run([sys.executable,str(ROOT/'dev/run_polish.py'),'--suite',suite,'--resume-dir',str(warm),'--budget','0','--work-budget','1','--passes','1'],stdout=stream,stderr=subprocess.STDOUT,check=True)
  manifests=[Path(x.removeprefix('manifest: ')) for x in log.read_text().splitlines() if x.startswith('manifest: ')];assert len(manifests)==1;path=manifests[0];m=json.loads(path.read_text());assert m['success'] and m['result']['complete'];assert m['result']['aggregate_score']>=stage['score']['aggregate_score'];m['evolution_selection']=dict(reports=report_hashes,coverage_sha256=result['coverage_sha256'],cases=selections,known_experimental_core_wall_s=search_cost,scope=result['scope']);save(path,m)
  for selected in selections:
   if selected['changed']:
    candidate=pool[(tier,selected['case'])];target=path.parent/'development-source'/('evolved-'+candidate['variant']['source_sha256']+'.cpp');shutil.copyfile(candidate['source'],target)
  runs.append(path.parent);result['rows'].append(dict(tier=tier,run_id=m['run_id'],score=m['result']['aggregate_score'],previous_score=stage['score']['aggregate_score'],improved_cases=sum(x['changed'] for x in selections),cases=selections));save(a.out/'report.json',result)
 assert all(digest(Path(path))==sha for path,sha in report_hashes.items());assert digest(a.coverage)==result['coverage_sha256']
 coverage=a.out/'coverage.json';subprocess.run([sys.executable,str(ROOT/'dev/report_tiers.py'),*[str(x) for x in runs],'--out',str(coverage)],check=True);result['complete']=True;result['coverage_sha256_result']=digest(coverage);save(a.out/'report.json',result);evidence=ROOT/'docs/evidence/phase3';evidence_report=evidence/(a.label+'.json');evidence_coverage=evidence/('tier-'+a.label+'-coverage.json');assert not evidence_report.exists() and not evidence_coverage.exists();shutil.copyfile(a.out/'report.json',evidence_report);shutil.copyfile(coverage,evidence_coverage)
 if a.select:
  chosen=dict(coverage=str(evidence_coverage.relative_to(ROOT)),tiers=[])
  for row in result['rows']:
   prior=next(x for x in old['tiers'] if x['tier']==row['tier']);assert row['score']>=prior['score'];target=ROOT/'dev/incumbents'/row['tier']/(row['run_id']+'.tar.gz');subprocess.run([sys.executable,str(ROOT/'dev/archive_incumbent.py'),str(ROOT/'dev/artifacts'/row['run_id']),'--out',str(target)],check=True);chosen['tiers'].append(dict(tier=row['tier'],run_id=row['run_id'],score=row['score'],archive=str(target.relative_to(ROOT)),archive_sha256=digest(target),selection_context=dict(stage=str(evidence_report.relative_to(ROOT)),scope=result['scope'],previous_selection_context=prior.get('selection_context'))))
  selection=a.out/'selection.json';save(selection,chosen);restore=a.out/'restored';subprocess.run([sys.executable,str(ROOT/'dev/restore_incumbents.py'),'--selection',str(selection),'--out',str(restore)],check=True);count=0
  for row in chosen['tiers']:
   inventory=json.loads((ROOT/(row['archive']+'.json')).read_text())
   for name,sha in inventory['members'].items():assert digest(restore/row['run_id']/name)==sha;count+=int(name.startswith('routes/'))
  assert count==45;save(ROOT/'dev/incumbents/selected.json',chosen);save(evidence/(a.label+'-restoration.json'),dict(routes_matched=count,all_archive_members_matched=True,selection_sha256=digest(ROOT/'dev/incumbents/selected.json'),source_sha256=digest(Path(__file__))))
 print([(x['tier'],x['score'],x['improved_cases']) for x in result['rows']])
if __name__=='__main__':main()
