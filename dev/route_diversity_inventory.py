"""Inventory locally verified complete runs by net-labelled edge diversity."""
import argparse,json
from pathlib import Path
from measure import ROOT,digest,save

def edge_set(path):
    d=json.loads(path.read_text())
    return {(r['net'],*min(tuple(a),tuple(b)),*max(tuple(a),tuple(b))) for r in d['routes'] for a,b in r['edges']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--selection',type=Path,default=ROOT/'dev/incumbents/selected.json');p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    if a.out.exists():p.error('report exists')
    selection=json.loads(a.selection.read_text());report={'selection_sha256':digest(a.selection),'metric':'Jaccard distance on net-labelled undirected edges; geometry proxy,not proof of distinct basins','delay_tolerance':1.05,'tiers':{}}
    for tier,case in [('designs','ctrl'),('congested','case_01')]:
        row=next(x for x in selection['tiers'] if x['tier']==tier);current=ROOT/'dev/artifacts'/row['run_id'];m=json.loads((current/'manifest.json').read_text());c=next(x for x in m['cases'] if x['case']==case);best=c['total_delay'];base=edge_set(current/'routes'/(case+'.sol.json'));rows=[]
        for path in sorted((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json')):
            x=json.loads(path.read_text())
            if not x.get('success') or not x['result']['complete'] or x['config']['suite']!='benchmarks_'+tier or x['run_id']==row['run_id']:continue
            y=next((q for q in x['cases'] if q['case']==case),None)
            if not y or y['total_delay']>best*1.05:continue
            route=path.parent/'routes'/(case+'.sol.json')
            if not route.exists():continue
            assert digest(route)==y['output_sha256'];other=edge_set(route);distance=1-len(base&other)/len(base|other)
            rows.append({'run_id':x['run_id'],'delay':y['total_delay'],'distance':distance,'manifest_sha256':digest(path),'output_sha256':y['output_sha256'],'prior_wrapper_wall_s':x['wrapper_wall_s']})
        rows.sort(key=lambda x:(-x['distance'],x['delay'],x['run_id']));assert rows
        report['tiers'][tier]={'case':case,'current_run':row['run_id'],'current_delay':best,'selected':rows[0],'candidates':rows}
    save(a.out,report)
if __name__=='__main__':main()
