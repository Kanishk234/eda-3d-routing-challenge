"""Retain diverse checked variants, including negative stepping stones.
Preserve compact source patches plus each immutable parent translation unit.
No solver defaults, routing incumbents or submission files are changed.
"""
import argparse,json,difflib
from pathlib import Path
from measure import ROOT,digest,save

def family(report,path):
 names=set(report['plan']['variants'])
 if 'neural_groups' in names:return 'pretrained-neighborhood'
 if any(x.startswith('hotspot') for x in names):return 'hotspot-neighborhood'
 if 'cold_anneal_neutral' in names:return 'history-crossover'
 if any(x.startswith('precision') for x in names):return 'precision'
 if names.intersection({'slice10','slice25','repair_first'}):return 'scheduling'
 if 'dual_release' in names:return 'history'
 return report['plan'].get('mutation_family','basin' if path.name=='evolution-basin.json' else 'ordering')

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--reports',type=Path,nargs='+',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();source_root=ROOT/'dev/experiments/evolution-source-archive';source_root.mkdir(parents=True,exist_ok=True);archive=dict(reports={},entries=[],best_own_cases={},policy='Keep all legal source variants and their observations,including worse exploratory families. Production promotion requires full-tier/validation evidence;no automatic adoption. Score comparisons are within tiers,not summed delay or six-tier aggregate.')
 for path in a.reports:
  r=json.loads(path.read_text());assert r['status']=='complete';archive['reports'][str(path)]=digest(path);parent=next(v for v in r['variants'] if v['name']=='control');parent_cpp=Path(next(x for x in parent['build_command'] if x.endswith('.cpp')));assert digest(parent_cpp)==parent['source_sha256'];parent_target=source_root/(parent['source_sha256']+'.cpp')
  if parent_target.exists():assert digest(parent_target)==parent['source_sha256']
  else:parent_target.write_bytes(parent_cpp.read_bytes())
  for v in r['variants']:
   cpp=Path(next(x for x in v['build_command'] if x.endswith('.cpp')));assert digest(cpp)==v['source_sha256'];binary=Path(v['build_command'][-1]);assert digest(binary)==v['binary_sha256'];patch=source_root/(v['source_sha256']+'.diff');content=''.join(difflib.unified_diff(parent_cpp.read_text().splitlines(True),cpp.read_text().splitlines(True),fromfile='control.cpp',tofile='solver.cpp'))
   if patch.exists():assert patch.read_text()==content
   else:patch.write_text(content)
   rows=[x for x in r['rows'] if x['variant']==v['name']];assert all(x['legal'] for x in rows);comparisons=[x for x in r.get('comparisons',[]) if x['variant']==v['name']];archive['entries'].append(dict(report=str(path),name=v['name'],mutation_family=family(r,path),source_sha256=v['source_sha256'],binary_sha256=v['binary_sha256'],parent_source=str(parent_target.relative_to(ROOT)),source_patch=str(patch.relative_to(ROOT)),patch_sha256=digest(patch),comparisons=comparisons,legal_rows=len(rows),order_changes=sum(x['process']['repair_counters'].get('evolution_order_changes',0) for x in rows),uphill_moves=sum(x['process']['repair_counters'].get('uphill_moves',0) for x in rows),scope=r['scope']))
   for row in rows:
    key=row['tier']+'/'+row['case'];target=Path(row['process']['command'][0]).parent/f'{row["tier"]}-{row["case"]}-{row["seed"]}'/'candidate.sol.json';assert digest(target)==row['output_sha256'];prior=archive['best_own_cases'].get(key)
    if prior is None or row['delay']<prior['delay']:archive['best_own_cases'][key]=dict(delay=row['delay'],case_sha256=row['case_sha256'],output=str(target.relative_to(ROOT)),output_sha256=row['output_sha256'],report=str(path),variant=v['name'],source_sha256=v['source_sha256'],seed=row['seed'],work_budget=r['plan']['work_budget'])
 archive['unique_source_count']=len({x['source_sha256'] for x in archive['entries']});archive['legal_evaluations']=sum(x['legal_rows'] for x in archive['entries']);save(a.out,archive);print('retained',len(archive['entries']),'observed source variants,',archive['unique_source_count'],'distinct sources')
if __name__=='__main__':main()
