"""Matched donor/control trials from one frozen incumbent and explicit local donors."""
import argparse,json,math
from pathlib import Path
from measure import digest,save
from neighborhood_screen import run

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--start',type=Path,required=True);p.add_argument('--donor',type=Path,action='append',required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--work-budget',type=int,default=3000000)
    a=p.parse_args()
    if a.out.exists():p.error('report exists')
    report={'start':str(a.start.resolve()),'start_hashes':{f.name:digest(f) for f in a.start.glob('*.sol.json')},'donors':[{'directory':str(d.resolve()),'hashes':{f.name:digest(f) for f in d.glob('*.sol.json')}} for d in a.donor],
            'workers':1,'work_budget':a.work_budget,'rows':[],'complete':False,'limitations':'Hard01/04/07 development only; same starts/seeds/work caps/schedule. Added screen effort; no held-out tuning, per-case portfolio or universal method claim.'}
    configurations=[('control',None),*[(f'donor_{i}',d) for i,d in enumerate(a.donor)]]
    save(a.out,report)
    for label,donor in configurations:
        mode='fanout_fine_adaptive' if donor is None else 'fanout_fine_donor'
        for seed in (1,2,3):
            for case in ('case_01','case_04','case_07'):
                path,m=run(case,mode,60,1000,seed,a.start,a.work_budget,{'present_initial':2,'present_step':1,'history_step':1},donor)
                c=m['cases'][0]
                report['rows'].append({'label':label,'seed':seed,'case':case,'run_id':m['run_id'],'manifest_sha256':digest(path),'solver_sha256':m['solver_sha256'],'binary_sha256':m['binary_sha256'],'source_identity':m['source']['files_sha256'],'config':m['config'],'total_delay':c['total_delay'],'legal':c['legal'],'output_sha256':c['output_sha256'],'counters':c['process']['repair_counters'],'expansions':c['core']['expansions'],'searches':c['core']['searches'],'budget_reached':c['core']['budget_reached'],'wrapper_wall_s':m['wrapper_wall_s']})
                save(a.out,report)
    report['comparisons']=[]
    for label,_ in configurations[1:]:
        counts={'wins':0,'ties':0,'losses':0};ratios=[]
        for c in (r for r in report['rows'] if r['label']==label):
            control=next(r for r in report['rows'] if r['label']=='control' and r['seed']==c['seed'] and r['case']==c['case'])
            before=control['total_delay'];after=c['total_delay'];counts['wins' if after<before else 'losses' if after>before else 'ties']+=1;ratios.append(before/after)
        report['comparisons'].append({'label':label,**counts,'geomean_delay_ratio':math.exp(sum(map(math.log,ratios))/len(ratios))})
    report['total_wrapper_wall_s']=sum(r['wrapper_wall_s'] for r in report['rows']);report['complete']=True;save(a.out,report)
    print(report['comparisons'])

if __name__=='__main__':main()
