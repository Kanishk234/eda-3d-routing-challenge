"""Compare random, gain-per-area and relative-excess net orderings."""
import argparse,json,math,subprocess,sys
from pathlib import Path
from measure import ROOT,digest,save

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--coverage',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--work-budget',type=int,default=3000000);a=p.parse_args()
    if a.out.exists():p.error('report exists')
    coverage=json.loads(a.coverage.read_text());report={'coverage_sha256':digest(a.coverage),'workers':1,'work_budget':a.work_budget,'rows':[],'complete':False,'selection_rule':'Select ordered configuration only if geometric physical-delay ratio versus existing order>1 and at least2of3seeds improve; choose greatest ratio;otherwise keep control.','limitations':'Stress has one official case and no separate held-out case; scale uses development case01. Bounding-box area is a hypothesis for search cost, not a measured predictive model. All additional screens/generation effort disclosed; no generalization or universal scheduling claim.'}
    save(a.out,report)
    for tier in ('stress','scale'):
        original=next(x for x in coverage['rows'] if x['tier']==tier);case=original['cases'][0]['case'];cap=13 if tier=='stress' else 3
        configs=[('control',0,cap),('gain_area',1,cap),('relative_excess',2,cap)]
        for label,order,group in configs:
            for seed in (1,2,3):
                before=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'));command=[sys.executable,str(ROOT/'dev/run_polish.py'),'--suite','benchmarks_'+tier,'--case',case,'--resume-dir',str(ROOT/'dev/artifacts'/original['run_id']/'routes'),'--mode','fanout_fine_adaptive','--budget','60','--work-budget',str(a.work_budget),'--passes','1000','--seed',str(seed),'--group-limit',str(group)]
                command+=['--polish-order',str(order)]
                subprocess.run(command,check=True);paths=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))-before;assert len(paths)==1;path=paths.pop();m=json.loads(path.read_text());assert m['success'] and m['official_inputs_unchanged'];c=m['cases'][0];assert c['legal'];assert c['core']['expansions']<=a.work_budget
                report['rows'].append({'tier':tier,'label':label,'seed':seed,'case':case,'group_limit':group,'polish_order':order,'run_id':m['run_id'],'manifest_sha256':digest(path),'solver_sha256':m['solver_sha256'],'binary_sha256':m['binary_sha256'],'config':m['config'],'delay':c['total_delay'],'expansions':c['core']['expansions'],'searches':c['core']['searches'],'counters':c['process']['repair_counters'],'wrapper_wall_s':m['wrapper_wall_s'],'output_sha256':c['output_sha256']});save(a.out,report)
    report['comparisons']=[];report['selected_configs']={}
    for tier in ('stress','scale'):
        eligible=[]
        for label in ('gain_area','relative_excess'):
            counts={'wins':0,'ties':0,'losses':0};ratios=[]
            for seed in (1,2,3):
                old=next(x['delay'] for x in report['rows'] if x['tier']==tier and x['label']=='control' and x['seed']==seed);candidate=next(x for x in report['rows'] if x['tier']==tier and x['label']==label and x['seed']==seed);new=candidate['delay'];counts['wins' if new<old else 'losses' if new>old else 'ties']+=1;ratios.append(old/new)
            ratio=math.exp(sum(map(math.log,ratios))/len(ratios));report['comparisons'].append({'tier':tier,'label':label,**counts,'geomean_delay_ratio':ratio})
            if ratio>1 and counts['wins']>=2:eligible.append((ratio,label,candidate['polish_order']))
        report['selected_configs'][tier]={'polish_order':max(eligible)[2] if eligible else 0,'group_limit':13 if tier=='stress' else 3}
    report['total_wrapper_wall_s']=sum(x['wrapper_wall_s'] for x in report['rows']);report['complete']=True;save(a.out,report);print(report['comparisons']);print(report['selected_configs'])

if __name__=='__main__':main()
