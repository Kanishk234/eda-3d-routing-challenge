"""Compare fixed resource-price experiments and derive routing capacity metrics."""
import json
import math
from measure import ROOT, save
from run_polish import Submission, route_resources

def main():
    out=ROOT/'docs/evidence/phase3'
    reports={name:json.loads((out/file).read_text()) for name,file in {
        'wide':'resource-pricing-control.json','compact':'compact-screen.json','fanout':'fanout-screen.json'}.items()}
    old={(r['seed'],r['case']):r for r in reports['wide']['rows']}
    summary={'scope':'matched representatives01/04/07,seeds1–3,2s/100 cycles,plateau warm starts;development only','methods':{}}
    for name,report in reports.items():
        warm=ROOT/report['warm_start']
        for row in report['rows']:
            row['before_resources']=route_resources(Submission.load(warm/(row['case']+'.sol.json')))
            row['resources']=route_resources(Submission.load(ROOT/'dev/artifacts'/row['run_id']/'routes'/(row['case']+'.sol.json')))
        data={'wins_vs_wide':sum(r['total_delay']<old[(r['seed'],r['case'])]['total_delay'] for r in report['rows']),
              'losses_vs_wide':sum(r['total_delay']>old[(r['seed'],r['case'])]['total_delay'] for r in report['rows']),
              'seed_aggregates':{},'total_core_wall_s':report['total_core_wall_s'],
              'vertex_use_changes':[{'seed':r['seed'],'case':r['case'],
                  'delta':r['resources']['net_vertex_uses']-r['before_resources']['net_vertex_uses']} for r in report['rows']]}
        for seed in (1,2,3):
            rows=[r for r in report['rows'] if r['seed']==seed]
            data['seed_aggregates'][str(seed)]=math.exp(sum(math.log(r['ratio']) for r in rows)/len(rows))
        summary['methods'][name]=data
        save(out/({'wide':'resource-pricing-control','compact':'compact-screen','fanout':'fanout-screen'}[name]+'.json'),report)
    save(out/'resource-pricing-comparison.json',summary)
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
