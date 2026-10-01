"""Read-only pinned-head public hard-output audit; no public warm starts adopted."""
import concurrent.futures
import datetime as dt
import json
import sys
import urllib.request
from pathlib import Path
from measure import ROOT, OFFICIAL, digest, save
sys.path.insert(0,str(OFFICIAL))
from m3d.model import Instance,Submission
from m3d.scorer import score_case,leaderboard

def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'routing-output-audit'})
    return urllib.request.urlopen(req,timeout=30).read()

def main():
    pulls=json.loads(get('https://api.github.com/repos/partcleda/eda-3d-routing-challenge/pulls?state=all&per_page=100'))
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    out=ROOT/'dev/artifacts'/(stamp+'-public-hard-audit');out.mkdir()
    suite=json.loads((OFFICIAL/'benchmarks_hard/suite.json').read_text())
    report={'time_utc':stamp,'scope':'All available PR heads, hard-tier directories containing changed route files; includes closed PRs. No solver runtimes reproduced.','entries':[],'errors':[]}
    for pr in pulls:
        try:
            changes=json.loads(get(f'https://api.github.com/repos/partcleda/eda-3d-routing-challenge/pulls/{pr["number"]}/files?per_page=100'))
            dirs=sorted({str(Path(f['filename']).parent) for f in changes if f['filename'].startswith('submissions/hard/') and f['filename'].endswith('.sol.json')})
            for folder in dirs:
                target=out/str(pr['number'])/Path(folder).name;target.mkdir(parents=True)
                sha=pr['head']['sha'];repo=(pr['head'].get('repo') or {}).get('full_name','partcleda/eda-3d-routing-challenge')
                def download(c):
                    p=target/(c['name']+'.sol.json')
                    p.write_bytes(get(f'https://raw.githubusercontent.com/{repo}/{sha}/{folder}/{p.name}'))
                    return p
                with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: paths=list(pool.map(download,suite['cases']))
                scores=[score_case(Instance.load(OFFICIAL/'benchmarks_hard'/c['instance_file']),Submission.load(p),c['baseline_total']) for c,p in zip(suite['cases'],paths)]
                result=leaderboard(scores).to_dict()
                entry={'pr':pr['number'],'state':pr['state'],'url':pr['html_url'],'head':sha,'method':Path(folder).name,'result':result,'output_hashes':{p.name:digest(p) for p in paths},'local_routes':str(target.relative_to(ROOT))}
                report['entries'].append(entry)
                print(pr['number'],entry['method'],result['aggregate_score'],result['n_legal'],flush=True)
        except Exception as exc:
            report['errors'].append({'pr':pr['number'],'error':str(exc)});print('error',pr['number'],str(exc),flush=True)
        save(out/'report.json',report)
    report['entries'].sort(key=lambda e:e['result']['aggregate_score'],reverse=True)
    evidence=ROOT/'docs/evidence/phase3';save(evidence/'current-public-hard.json',report)
    print('highest',[(e['pr'],e['method'],e['result']['aggregate_score']) for e in report['entries'][:3]])

if __name__=='__main__':main()
