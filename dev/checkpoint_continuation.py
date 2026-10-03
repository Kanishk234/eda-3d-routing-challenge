"""Archive, restore and select a completed officially rescored continuation."""
import argparse,json,subprocess,sys
from pathlib import Path
from measure import ROOT,digest,save

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('progress',type=Path);p.add_argument('--label',required=True);p.add_argument('--restore-out',type=Path,required=True);a=p.parse_args();assert not a.restore_out.exists();state=json.loads(a.progress.read_text());assert state['status']=='complete' and state['completed_rounds']==len(state['plan']['seeds']);coverage_source=Path(state['round_coverages'][-1]['path']);assert digest(coverage_source)==state['round_coverages'][-1]['sha256'];coverage=json.loads(coverage_source.read_text());old=json.loads((ROOT/'dev/incumbents/selected.json').read_text());assert {x['tier'] for x in old['tiers']}=={x['tier'] for x in coverage['rows']};evidence=ROOT/'docs/evidence/phase3';state_target=evidence/(a.label+'.json');coverage_target=evidence/('tier-'+a.label+'-coverage.json');assert not state_target.exists() and not coverage_target.exists();save(state_target,state);save(coverage_target,coverage);selected=dict(coverage=str(coverage_target.relative_to(ROOT)),tiers=[])
 for row in coverage['rows']:
  assert row['score']['complete'];prior=next(x for x in old['tiers'] if x['tier']==row['tier']);assert row['score']['aggregate_score']>=prior['score'];run=row['run_id'];target=ROOT/'dev/incumbents'/row['tier']/(run+'.tar.gz')
  if not target.exists():subprocess.run([sys.executable,str(ROOT/'dev/archive_incumbent.py'),str(ROOT/'dev/artifacts'/run),'--out',str(target)],check=True)
  inventory=json.loads(Path(str(target)+'.json').read_text());assert digest(target)==inventory['archive_sha256'];selected['tiers'].append(dict(tier=row['tier'],run_id=run,score=row['score']['aggregate_score'],archive=str(target.relative_to(ROOT)),archive_sha256=digest(target),selection_context=dict(stage=str(state_target.relative_to(ROOT)),scope=state['plan'].get('scope','Own additional continuation effort;not matched-budget algorithm superiority.'),previous_selection_context=prior.get('selection_context'))))
 selection_path=a.restore_out.parent/(a.restore_out.name+'-selection.json');save(selection_path,selected);subprocess.run([sys.executable,str(ROOT/'dev/restore_incumbents.py'),'--selection',str(selection_path),'--out',str(a.restore_out)],check=True);count=0
 for row in selected['tiers']:
  inventory=json.loads((ROOT/(row['archive']+'.json')).read_text())
  for name,sha in inventory['members'].items():assert digest(a.restore_out/row['run_id']/name)==sha;count+=int(name.startswith('routes/'))
 assert count==sum(len(list((ROOT/'dev/artifacts'/row['run_id']/'routes').glob('*.sol.json'))) for row in selected['tiers']);save(ROOT/'dev/incumbents/selected.json',selected);save(evidence/(a.label+'-restoration.json'),dict(routes_matched=count,all_archive_members_matched=True,selection_sha256=digest(ROOT/'dev/incumbents/selected.json'),source_sha256=digest(Path(__file__))));print([(x['tier'],x['score']) for x in selected['tiers']])
if __name__=='__main__':main()
