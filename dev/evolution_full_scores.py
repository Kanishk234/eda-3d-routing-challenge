"""Officially rescore every complete tier/seed/variant in an evolution report."""
import argparse,json,shutil,statistics
from pathlib import Path
from measure import ROOT,OFFICIAL,digest,save,execute

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--reports',nargs='+',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out=a.out.resolve();assert not a.out.exists();a.out.mkdir(parents=True);result=dict(reports={},rows=[],summaries=[],complete=False,scope='Complete within-tier official geometric scores by seed and source variant. Seed mean/spread are descriptive;no six-tier aggregate.');save(a.out/'report.json',result)
 for path in a.reports:
  r=json.loads(path.read_text());assert r['status']=='complete';result['reports'][str(path)]=digest(path)
  for tier in sorted({x['tier'] for x in r['rows']}):
   suite='benchmarks' if tier=='intro' else 'benchmarks_'+tier;inventory=json.loads((OFFICIAL/suite/'suite.json').read_text());expected={x['name'] for x in inventory['cases']}
   for variant in r['plan']['variants']:
    for seed in r['plan']['seeds']:
     rows=[x for x in r['rows'] if (x['tier'],x['variant'],x['seed'])==(tier,variant,seed)];assert {x['case'] for x in rows}==expected and len(rows)==len(expected);folder=a.out/path.stem/tier/variant/str(seed);routes=folder/'routes';routes.mkdir(parents=True)
     for row in rows:
      source=Path(row['process']['command'][0]).parent/f'{tier}-{row["case"]}-{seed}'/'candidate.sol.json';assert row['legal'] and digest(source)==row['output_sha256'];shutil.copyfile(source,routes/(row['case']+'.sol.json'))
     check=execute([str(ROOT/'.venv/bin/python'),'-m','m3d.cli','score-suite','--suite',suite,'--submission-dir',str(routes.resolve()),'--out',str((folder/'official-rescore.json').resolve())],folder,'official',180);assert check['exit_code']==0;scored=json.loads((folder/'official-rescore.json').read_text());assert scored['complete'];result['rows'].append(dict(report=str(path),tier=tier,variant=variant,seed=seed,score=scored['aggregate_score'],official_rescore_sha256=digest(folder/'official-rescore.json'),process=check));save(a.out/'report.json',result)
   for variant in r['plan']['variants']:
    values=[x['score'] for x in result['rows'] if x['report']==str(path) and x['tier']==tier and x['variant']==variant];result['summaries'].append(dict(report=str(path),tier=tier,variant=variant,mean=statistics.mean(values),minimum=min(values),maximum=max(values),stdev=statistics.stdev(values) if len(values)>1 else 0,seeds=len(values)))
 result['complete']=True;save(a.out/'report.json',result);print(result['summaries'])
if __name__=='__main__':main()
