"""Restricted exact single-sink net-group repair on an explicit corridor."""
import argparse,json,itertools,heapq
from collections import defaultdict
from pathlib import Path
from ortools.sat.python import cp_model
from measure import ROOT,OFFICIAL,digest,save
from run_polish import Instance,Submission,NetRoute,check
from branch_repair import Router
from generate_tree_candidates import priced_tree

def solve_paths(router,ids,vertices,seconds=5,deterministic=.5,prune=False):
    model=cp_model.CpModel();occupied=defaultdict(list);flows={};weights=[];variables=[]
    baseline=0;bounds={};distances={};caps={};pruned=0
    for nid in ids:
        _,distance,_=router.tree(router.routes[nid]);baseline+=distance[router.pins[router.nets[nid].sinks[0]]]
    if prune:
        def distance_from(start,available):
            dist={start:0};q=[(0,start)]
            while q:
                cost,u=heapq.heappop(q)
                if cost!=dist[u]:continue
                for v,step in router.neighbors(u):
                    if v not in available:continue
                    nxt=cost+step
                    if nxt<dist.get(v,10**30):dist[v]=nxt;heapq.heappush(q,(nxt,v))
            return dist
        for nid in ids:
            n=router.nets[nid];available={v for v in vertices if router.pin_owner.get(v,nid)==nid}
            root=router.pins[n.driver];sink=router.pins[n.sinks[0]]
            forward=distance_from(root,available);backward=distance_from(sink,available)
            bounds[nid]=forward[sink];distances[nid]=(forward,backward)
        for nid in ids:caps[nid]=baseline-sum(bounds[j] for j in ids if j!=nid)
    for nid in ids:
        n=router.nets[nid];assert len(n.sinks)==1
        root=router.pins[n.driver];sink=router.pins[n.sinks[0]]
        available={v for v in vertices if router.pin_owner.get(v,nid)==nid}
        if prune:
            forward,backward=distances[nid]
            available={v for v in available if forward.get(v,10**30)+backward.get(v,10**30)<=caps[nid]}
        assert root in available and sink in available
        incoming=defaultdict(list);outgoing=defaultdict(list);selected={v:model.new_bool_var(f'u{nid}:{v}') for v in available}
        edges={}
        net_objective=[]
        for u in sorted(available):
            for v,cost in router.neighbors(u):
                if v not in available:continue
                if prune and forward[u]+cost+backward[v]>caps[nid]:pruned+=1;continue
                variable=model.new_bool_var(f'e{nid}:{u}:{v}');edges[u,v]=variable
                outgoing[u].append(variable);incoming[v].append(variable);weights.append(cost);variables.append(variable)
                net_objective.append(cost*variable)
        if prune:model.add(sum(net_objective)>=bounds[nid])
        _,_,order=router.tree(router.routes[nid]);parent,_,_=router.tree(router.routes[nid]);base_vertices=set(order)
        for v,var in selected.items():
            occupied[v].append(var);model.add_hint(var,int(v in base_vertices))
            if v==root:model.add(sum(incoming[v])==0);model.add(sum(outgoing[v])==1);model.add(var==1)
            elif v==sink:model.add(sum(incoming[v])==1);model.add(sum(outgoing[v])==0);model.add(var==1)
            else:model.add(sum(incoming[v])==var);model.add(sum(outgoing[v])==var)
        for (u,v),var in edges.items():model.add_hint(var,int(parent.get(v)==u and v!=root))
        flows[nid]=edges
    for used in occupied.values():model.add_at_most_one(used)
    objective=sum(w*v for w,v in zip(weights,variables))
    model.add(objective<=baseline);model.minimize(objective)
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=1;solver.parameters.random_seed=1
    solver.parameters.max_time_in_seconds=seconds;solver.parameters.max_deterministic_time=deterministic
    status=solver.solve(model);result={}
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        for nid,edges in flows.items():
            root=router.pins[router.nets[nid].driver];sink=router.pins[router.nets[nid].sinks[0]]
            next_vertex={u:v for (u,v),var in edges.items() if solver.value(var)}
            path=[];u=root;seen={u}
            while u!=sink:
                v=next_vertex[u];assert v not in seen;seen.add(v);path.append((u,v));u=v
            # Drop disconnected positive-cost flow cycles if a feasible timeout
            # returns them. Root path is unique by in/outdegree conservation.
            result[nid]=NetRoute(nid,path)
    return result,{'status':solver.status_name(status),'restricted_optimal':status==cp_model.OPTIMAL,'baseline':baseline,'bound':solver.best_objective_bound,'objective':solver.objective_value if result else None,'wall_s':solver.wall_time,'deterministic_time':solver.response_proto.deterministic_time,'graph_vertices':len(vertices),'flow_variables':len(variables),'prune_arcs':prune,'pruned_arcs':pruned,'independent_group_bound':sum(bounds.values()) if prune else None}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();a.out.mkdir(parents=True);(a.out/'routes').mkdir()
    plan=json.loads(a.plan.read_text());coverage=json.loads((ROOT/plan['coverage']).read_text());stage=next(r for r in coverage['rows'] if r['tier']==plan['tier']);suite=stage['config']['suite'];rows=[]
    frozen={str(q.resolve()):digest(q) for q in [a.plan,Path(__file__),ROOT/plan['coverage'],Path(__file__).with_name('branch_repair.py'),Path(__file__).with_name('generate_tree_candidates.py')]}
    solver_function=solve_paths
    if plan.get('solver')=='tree':
        from exact_tree_repair import solve_trees
        solver_function=solve_trees;tree_source=Path(__file__).with_name('exact_tree_repair.py');frozen[str(tree_source.resolve())]=digest(tree_source)
    report={'plan':plan,'frozen_sha256':frozen,'status':'running','rows':rows,'workers':1,'scope':'Net groups on restricted corridor, outside routes fixed. Solver optimality is restricted only; full official checker governs accepted output. Own incumbents only.'};save(a.out/'progress.json',report)
    inventory=json.loads((OFFICIAL/suite/'suite.json').read_text())
    for item in inventory['cases']:
        if item['name'] not in plan['cases']:continue
        case=OFFICIAL/suite/item['instance_file'];route=ROOT/'dev/artifacts'/stage['run_id']/'routes'/(item['name']+'.sol.json');inst=Instance.load(case);sub=Submission.load(route);before=check(inst,sub);assert before.legal
        router=Router(inst,sub,plan['proposal_work'],plan['proposal_seconds'],1);proposals=[]
        order=list(router.nets);router.rng.shuffle(order)
        for nid in order:
            if len(router.nets[nid].sinks)!=1 and not plan.get('all_fanouts'):continue
            from branch_repair import Limit
            try:ideal=priced_tree(router,nid,0)
            except Limit:break
            if ideal is None:continue
            counts=defaultdict(int)
            for v in router.vertices(ideal):
                bid=router.owner.get(v,nid)
                if bid!=nid and (len(router.nets[bid].sinks)==1 or plan.get('all_fanouts')):counts[bid]+=1
            for u in router.vertices(router.routes[nid]):
                for v,_ in router.neighbors(u):
                    bid=router.owner.get(v,nid)
                    if bid!=nid and (len(router.nets[bid].sinks)==1 or plan.get('all_fanouts')):counts[bid]+=1
            choices=sorted(counts,key=lambda j:(-counts[j],j))[:plan.get('discovery_options',4)]
            _,old_dist,_=router.tree(router.routes[nid]);sinks=[router.pins[s] for s in router.nets[nid].sinks]
            limited=False
            for size in range(1,plan.get('max_group',2)):
                for companions in itertools.combinations(choices,size):
                    old_owner=router.owner;router.owner={v:j for v,j in old_owner.items() if j not in companions}
                    try:proposal=router.search(nid,sinks,NetRoute(nid,[]),set())
                    except Limit:limited=True;proposal=None
                    finally:router.owner=old_owner
                    if proposal:
                        _,new_dist,_=router.tree(proposal);gain=sum(old_dist[s]-new_dist[s] for s in sinks)
                        if gain>0:proposals.append((gain,nid,companions,proposal))
                    if limited:break
                if limited:break
            if limited:break
        pairs=[];seen=set()
        for gain,nid,companions,ideal in sorted(proposals,key=lambda q:(-q[0],q[1],q[2])):
            ids=[nid,*companions];key=tuple(sorted(ids))
            if key in seen:continue
            seen.add(key)
            if len(pairs)>=plan['pairs_per_case']:break
            selected={v for j in ids for v in router.vertices(router.routes[j])}|router.vertices(ideal)
            for _ in range(plan['margin']):selected|={v for u in list(selected) for v,_ in router.neighbors(u)}
            selected={v for v in selected if router.owner.get(v,ids[0]) in ids}
            options={'strict':plan.get('strict_improvement',False)} if plan.get('solver')=='tree' else {}
            result,stats=solver_function(router,ids,selected,plan['seconds'],plan['deterministic_time'],plan.get('prune_arcs',False),**options);old=router.routes.copy();old_score=check(inst,Submission(inst.name,list(old.values()))).total_delay
            if result:
                router.routes.update(result);checked=check(inst,Submission(inst.name,list(router.routes.values())))
                assert checked.legal and checked.total_delay<=old_score
                actual_gain=old_score-checked.total_delay
                if stats.get('method')=='arborescence physical-distance potentials':assert stats['baseline']-actual_gain==stats['objective']
                if actual_gain:router.reown()
                else:router.routes=old
            else:actual_gain=0
            pairs.append({'nets':ids,'ideal_target_gain':gain,'accepted_gain':actual_gain,**stats});save(a.out/'progress.json',report)
        final=Submission(inst.name,list(router.routes.values()));after=check(inst,final);assert after.legal and after.total_delay<=before.total_delay
        target=a.out/'routes'/(item['name']+'.sol.json');final.save(str(target));assert check(inst,Submission.load(str(target))).total_delay==after.total_delay
        row={'case':item['name'],'case_sha256':digest(case),'start_sha256':digest(route),'output_sha256':digest(target),'before_delay':before.total_delay,'after_delay':after.total_delay,'legal':True,'pairs':pairs,'proposal_expansions':router.expansions};rows.append(row);print(item['name'],'pairs',len(pairs),'gain',before.total_delay-after.total_delay,flush=True);save(a.out/'progress.json',report)
    assert all(digest(Path(q))==sha for q,sha in frozen.items());report['status']='complete';save(a.out/'progress.json',report)

if __name__=='__main__':main()
