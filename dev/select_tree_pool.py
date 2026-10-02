"""Select multiple own candidate trees per net using vertex-disjoint CP-SAT."""
import argparse,json,time,datetime
from collections import defaultdict
from pathlib import Path
import ortools
from ortools.sat.python import cp_model
from measure import ROOT,OFFICIAL,digest,save,REVISION,execute
from run_polish import Instance,Submission,check,score_case,leaderboard
from recombine_routes import ancestor_costs

def solve_pool(costs,resources,base_choices,seconds=30,deterministic=10):
    model=cp_model.CpModel();variables=[];occupied=defaultdict(list)
    for nid,(options,sets) in enumerate(zip(costs,resources)):
        row=[model.new_bool_var(f'n{nid}t{k}') for k in range(len(options))];variables.append(row)
        model.add_exactly_one(row)
        for k,vertices in enumerate(sets):
            for v in vertices:occupied[v].append((nid,row[k]))
        for k,var in enumerate(row):model.add_hint(var,int(k==base_choices[nid]))
    constraints=0
    for usage in occupied.values():
        if len({nid for nid,_ in usage})>1:model.add_at_most_one([var for _,var in usage]);constraints+=1
    objective=sum(c*variables[nid][k] for nid,row in enumerate(costs) for k,c in enumerate(row))
    base_cost=sum(costs[nid][k] for nid,k in enumerate(base_choices));model.add(objective<=base_cost);model.minimize(objective)
    solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=seconds;solver.parameters.max_deterministic_time=deterministic
    solver.parameters.num_search_workers=1;solver.parameters.random_seed=1
    status=solver.solve(model);feasible=status in (cp_model.OPTIMAL,cp_model.FEASIBLE)
    choices=[next(k for k,var in enumerate(row) if solver.value(var)) for row in variables] if feasible else base_choices.copy()
    return choices,{'status':solver.status_name(status),'restricted_optimal':status==cp_model.OPTIMAL,'fallback_base':not feasible,'best_bound':solver.best_objective_bound if feasible else None,'chosen_delay':sum(costs[nid][k] for nid,k in enumerate(choices)),'base_delay':base_cost,'variables':sum(map(len,variables)),'vertex_constraints':constraints,'wall_s':solver.wall_time,'deterministic_time':solver.response_proto.deterministic_time}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists()
    a.out=a.out.resolve();plan=json.loads(a.plan.read_text());a.out.mkdir(parents=True);(a.out/'routes').mkdir()
    sources=[ROOT/'dev/artifacts'/name for name in plan['runs']];manifests=[json.loads((r/'manifest.json').read_text()) for r in sources]
    assert all(m['success'] and m['result']['complete'] and m['config']['suite']==plan['suite'] for m in manifests)
    frozen={str(p.resolve()):digest(p) for p in [a.plan,Path(__file__),*[r/'manifest.json' for r in sources]]}
    extra=None
    if plan.get('extra_candidates'):
        extra_path=ROOT/plan['extra_candidates'];extra=json.loads(extra_path.read_text());assert extra['status']=='complete';frozen[str(extra_path.resolve())]=digest(extra_path)
    inventory=json.loads((OFFICIAL/plan['suite']/'suite.json').read_text());rows=[];scores=[];start=time.monotonic()
    for item in inventory['cases']:
        case=OFFICIAL/plan['suite']/item['instance_file'];inst=Instance.load(case);pins=inst.pin_vertex();nets={n.id:n for n in inst.nets};pool={n.id:[] for n in inst.nets};seen={n.id:{} for n in inst.nets}
        for source_index,(r,m) in enumerate(zip(sources,manifests)):
            route=r/'routes'/(item['name']+'.sol.json');assert digest(route)==m['outputs']['routes/'+route.name]
            sub=Submission.load(route);checked=check(inst,sub);assert checked.legal;delays={n.net:n.delay for n in checked.nets}
            for tree in sub.routes:
                edges=tuple(sorted(tuple(sorted(e)) for e in tree.edges));nid=tree.net
                if edges not in seen[nid]:
                    seen[nid][edges]=len(pool[nid]);vertices={v for edge in tree.edges for v in edge}|{pins[nets[nid].driver]}
                    pool[nid].append({'route':tree,'delay':delays[nid],'vertices':vertices,'sources':[source_index]})
                else:pool[nid][seen[nid][edges]]['sources'].append(source_index)
        if extra:
            record=extra['cases'][item['name']];assert record['case_sha256']==digest(case)
            for extra_index,candidate in enumerate(record['trees']):
                tree=Submission.from_dict({'format':'m3d-submission','instance':inst.name,'routes':[candidate['route']]}).routes[0];nid=tree.net
                individual=check(inst,Submission(inst.name,[tree]));nr=next(n for n in individual.nets if n.net==nid);assert nr.legal and nr.delay==candidate['delay']
                edges=tuple(sorted(tuple(sorted(e)) for e in tree.edges));source_index=len(sources)+extra_index
                if edges not in seen[nid]:
                    seen[nid][edges]=len(pool[nid]);vertices={v for e in tree.edges for v in e}|{pins[nets[nid].driver]};pool[nid].append({'route':tree,'delay':nr.delay,'vertices':vertices,'sources':[source_index]})
                else:pool[nid][seen[nid][edges]]['sources'].append(source_index)
        ids=sorted(pool);costs=[[c['delay'] for c in pool[nid]] for nid in ids];resources=[[c['vertices'] for c in pool[nid]] for nid in ids]
        base=[next(k for k,c in enumerate(pool[nid]) if 0 in c['sources']) for nid in ids]
        chosen,stats=solve_pool(costs,resources,base,plan.get('seconds',30),plan.get('deterministic_time',10))
        sub=Submission(inst.name,[pool[nid][chosen[k]]['route'] for k,nid in enumerate(ids)]);checked=check(inst,sub);assert checked.legal and checked.total_delay==stats['chosen_delay']<=stats['base_delay']
        target=a.out/'routes'/(item['name']+'.sol.json');sub.save(str(target));scores.append(score_case(inst,sub,item['baseline_total']))
        rows.append({'case':item['name'],'case_sha256':digest(case),'output_sha256':digest(target),'gain':stats['base_delay']-checked.total_delay,'selected_sources':{str(nid):pool[nid][chosen[k]]['sources'] for k,nid in enumerate(ids)},**stats});print(item['name'],stats['status'],'gain',rows[-1]['gain'],flush=True)
    assert all(digest(Path(p))==sha for p,sha in frozen.items())
    costs={};missing=set()
    for source in sources:
        known,absent=ancestor_costs(source);costs.update(known);missing.update(absent)
    report={'upstream_revision':REVISION,'run_id':a.out.name,'suite':plan['suite'],'plan':plan,'frozen_sha256':frozen,'ortools_version':ortools.__version__,'cases':rows,'score':leaderboard(scores).to_dict(),'selection_wall_s':time.monotonic()-start,'known_ancestry_runs':costs,'missing_ancestor_artifacts':sorted(missing),'scope':'Restricted finite-pool exact tree selection when solver status OPTIMAL; never global routing optimality. All supplied candidates from declared own runs. Added portfolio effort; missing historical/reference-generation costs remain unknown.'}
    step=execute([str(ROOT/'.venv/bin/python'),'-m','m3d.cli','score-suite','--suite',plan['suite'],'--submission-dir',str(a.out.resolve()/'routes'),'--out',str(a.out.resolve()/'official-rescore.json')],a.out,'official-rescore',180);assert step['exit_code']==0
    official=json.loads((a.out/'official-rescore.json').read_text());assert official['complete'] and official['aggregate_score']==report['score']['aggregate_score'];report['official_rescore_process']=step;save(a.out/'portfolio.json',report)

if __name__=='__main__':main()
