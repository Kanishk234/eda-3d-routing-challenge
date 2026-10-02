"""Matched bounded-group pilot on declared first development cases of larger tiers."""
import argparse,json,math,subprocess,sys
from pathlib import Path
from measure import ROOT,digest,save

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--coverage',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--work-budget',type=int,default=3000000);a=p.parse_args()
    if a.out.exists():p.error('report exists')
    coverage=json.loads(a.coverage.read_text());report={'coverage_sha256':digest(a.coverage),'workers':1,'work_budget':a.work_budget,'rows':[],'complete':False,'scope':'scale/congested case01, designs ctrl;seeds1–3,caps3/7/13','selection_rule':'Per tier retain a smaller cap only if geometric delay ratio versus13 exceeds1 and at least2 of3 seed trials improve. Otherwise13;select greatest ratio among eligible caps.','limitations':'One development case per tier, not generalization evidence. Caps vary maximum transaction size; wide repair retains24 negotiation rounds for every cap. Fixed work limits, no held-out tuning.'}
    save(a.out,report)
    for tier in ('scale','congested','designs'):
        start=next(r for r in coverage['rows'] if r['tier']==tier);case=start['cases'][0]['case'];schedule=(2,4,4) if tier=='congested' else (2,2,2)
        for cap in (13,3,7):
            for seed in (1,2,3):
                before=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))
                command=[sys.executable,str(ROOT/'dev/run_polish.py'),'--suite','benchmarks_'+tier,'--case',case,'--resume-dir',str(ROOT/'dev/artifacts'/start['run_id']/'routes'),'--mode','fanout_fine_adaptive','--budget','60','--work-budget',str(a.work_budget),'--passes','1000','--seed',str(seed),'--group-limit',str(cap),'--present-initial',str(schedule[0]),'--present-step',str(schedule[1]),'--history-step',str(schedule[2])]
                subprocess.run(command,check=True);paths=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))-before;assert len(paths)==1;path=paths.pop();m=json.loads(path.read_text());assert m['success'] and m['official_inputs_unchanged'];c=m['cases'][0];assert c['legal'];hist=c['process']['repair_counters']['group_size_histogram'];assert not any(hist[cap+1:])
                report['rows'].append({'tier':tier,'cap':cap,'seed':seed,'case':case,'run_id':m['run_id'],'manifest_sha256':digest(path),'solver_sha256':m['solver_sha256'],'binary_sha256':m['binary_sha256'],'config':m['config'],'delay':c['total_delay'],'expansions':c['core']['expansions'],'counters':c['process']['repair_counters'],'output_sha256':c['output_sha256'],'wrapper_wall_s':m['wrapper_wall_s']});save(a.out,report)
    report['comparisons']=[];report['selected_caps']={}
    for tier in ('scale','congested','designs'):
        eligible=[]
        for cap in (3,7):
            counts={'wins':0,'ties':0,'losses':0};ratios=[]
            for seed in (1,2,3):
                old=next(x['delay'] for x in report['rows'] if x['tier']==tier and x['cap']==13 and x['seed']==seed);new=next(x['delay'] for x in report['rows'] if x['tier']==tier and x['cap']==cap and x['seed']==seed)
                counts['wins' if new<old else 'losses' if new>old else 'ties']+=1;ratios.append(old/new)
            ratio=math.exp(sum(map(math.log,ratios))/len(ratios));row={'tier':tier,'cap':cap,**counts,'geomean_delay_ratio':ratio};report['comparisons'].append(row)
            if ratio>1 and counts['wins']>=2:eligible.append((ratio,cap))
        report['selected_caps'][tier]=max(eligible)[1] if eligible else 13
    report['total_wrapper_wall_s']=sum(x['wrapper_wall_s'] for x in report['rows']);report['complete']=True;save(a.out,report);print(report['comparisons']);print('selected',report['selected_caps'])

if __name__=='__main__':main()
