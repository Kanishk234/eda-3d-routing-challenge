"""Select whole legal cases from explicitly supplied local runs, with provenance."""
import argparse,datetime,json,shutil,time
from pathlib import Path
from measure import ROOT,OFFICIAL,REVISION,digest,save,execute
from run_polish import Instance,Submission,check,score_case,leaderboard

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('runs',type=Path,nargs='+');p.add_argument('--suite',default='benchmarks_hard')
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    if a.out.exists():p.error('report exists; choose a new destination')
    start=time.perf_counter();runs=[r.resolve() for r in a.runs]
    manifests=[json.loads((r/'manifest.json').read_text()) for r in runs]
    if any(not m['success'] or not m['result']['complete'] or m['config']['suite']!=a.suite for m in manifests):p.error('all candidates must be successful complete runs of the same suite')
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    out=ROOT/'dev/artifacts'/(stamp+'-case-portfolio');(out/'routes').mkdir(parents=True)
    report={'upstream_revision':REVISION,'suite':a.suite,'artifact_directory':str(out),'portfolio_selection':True,
            'sources':[{'directory':str(r),'manifest_sha256':digest(r/'manifest.json'),'score':m['result']['aggregate_score']} for r,m in zip(runs,manifests)],
            'cases':[],'limitations':'Case portfolio, not a single fixed-seed solver run or same-budget algorithm comparison. Entire case routes are selected; no net splicing. Available generation ancestry is deduplicated; missing raw ancestors and reference generation costs remain unknown.'}
    costs={};missing=set()
    for directory,m in zip(runs,manifests):
        while True:
            key=m['run_id'];costs[key]=m['wrapper_wall_s']
            ancestor=Path(m['warm_start']['directory']);parent=ancestor.parent/'manifest.json'
            if not parent.exists():
                if not ancestor.exists():missing.add(str(ancestor))
                break
            m=json.loads(parent.read_text())
    suite=OFFICIAL/a.suite/'suite.json';inventory=json.loads(suite.read_text());scores=[]
    for c in inventory['cases']:
        case=OFFICIAL/a.suite/c['instance_file'];inst=Instance.load(case);candidates=[]
        for i,(r,m) in enumerate(zip(runs,manifests)):
            name='routes/'+c['name']+'.sol.json';path=r/name
            assert digest(path)==m['outputs'][name]
            sub=Submission.load(path);checked=check(inst,sub);assert checked.legal
            candidates.append((checked.total_delay,i,path,sub))
        delay,index,path,sub=min(candidates,key=lambda x:(x[0],x[1]))
        target=out/'routes'/path.name;shutil.copyfile(path,target)
        scores.append(score_case(inst,sub,c['baseline_total']))
        report['cases'].append({'case':c['name'],'case_sha256':digest(case),'total_delay':delay,'source_index':index,'source_run':manifests[index]['run_id'],'output_sha256':digest(target),'candidate_delays':[x[0] for x in candidates]})
    report['score']=leaderboard(scores).to_dict();report['known_ancestry_wrapper_wall_s']=sum(costs.values());report['known_ancestry_runs']=costs;report['missing_ancestor_artifacts']=sorted(missing)
    report['selection_wall_s']=time.perf_counter()-start
    report['official_rescore_process']=execute([str(ROOT/'.venv/bin/python'),'-m','m3d.cli','score-suite','--suite',a.suite,'--submission-dir',str(out/'routes'),'--out',str(out/'official-rescore.json')],out,'official-rescore',180)
    assert report['official_rescore_process']['exit_code']==0
    rescored=json.loads((out/'official-rescore.json').read_text());assert rescored['complete'] and rescored['aggregate_score']==report['score']['aggregate_score']
    save(out/'portfolio.json',report);save(a.out,report)
    print('portfolio score:',report['score']['aggregate_score'],'routes:',out/'routes')

if __name__=='__main__':main()
