"""Refined exact arborescence with coupled per-sink slack bounds."""
import heapq
from collections import defaultdict
from ortools.sat.python import cp_model
from run_polish import NetRoute

def solve_trees(router,ids,vertices,seconds=10,deterministic=1,prune=True,strict=False):
    def distances(seeds,available):
        d={v:0 for v in seeds};q=[(0,v) for v in seeds];heapq.heapify(q)
        while q:
            cost,u=heapq.heappop(q)
            if cost!=d[u]:continue
            for v,step in router.neighbors(u):
                if v not in available:continue
                new=cost+step
                if new<d.get(v,10**30):d[v]=new;heapq.heappush(q,(new,v))
        return d
    baseline=0;data={};bounds={}
    for nid in ids:
        n=router.nets[nid];root=router.pins[n.driver];sinks={router.pins[s] for s in n.sinks}
        available={v for v in vertices if router.pin_owner.get(v,nid)==nid}
        forward=distances([root],available);backward=distances(sinks,available)
        old_parent,old_dist,_=router.tree(router.routes[nid]);baseline+=sum(old_dist[router.pins[s]] for s in n.sinks)
        bounds[nid]=sum(forward[router.pins[s]] for s in n.sinks)
        per_sink={s:distances([s],available) for s in sinks}
        data[nid]=(root,sinks,available,forward,backward,old_parent,old_dist,per_sink)
    slack=baseline-sum(bounds.values());assert slack>=0
    model=cp_model.CpModel();occupancy=defaultdict(list);trees={};objective=[];pruned=0
    for nid in ids:
        root,sinks,available,forward,backward,old_parent,old_dist,per_sink=data[nid]
        cap=baseline-sum(bounds[j] for j in ids if j!=nid)
        # Any useful vertex belongs to at least one terminal path. Its relaxed
        # root→vertex→terminal cost cannot exceed this net's entire delay cap.
        # Each sink's excess over its independent bound consumes shared slack.
        sink_caps={s:forward[s]+slack for s in sinks}
        available={v for v in available if any(forward.get(v,10**30)+per_sink[s].get(v,10**30)<=sink_caps[s] for s in sinks)}
        upper={v:min(cap,max(sink_caps[s]-per_sink[s].get(v,10**30) for s in sinks)) for v in available}
        used={v:model.new_bool_var(f'u{nid}:{v}') for v in available}
        delay={v:model.new_int_var(0,upper[v],f'd{nid}:{v}') for v in available}
        incoming=defaultdict(list);edges={}
        for v,var in used.items():
            occupancy[v].append(var);model.add(delay[v]==0).only_enforce_if(var.Not())
            model.add(delay[v]>=forward[v]).only_enforce_if(var)
            model.add_hint(var,int(v in old_dist));model.add_hint(delay[v],old_dist.get(v,0))
        for u in sorted(available):
            for v,step in router.neighbors(u):
                if v not in available or v==root:continue
                if not any(forward[u]+step+per_sink[s].get(v,10**30)<=sink_caps[s] for s in sinks):pruned+=1;continue
                arc=model.new_bool_var(f'e{nid}:{u}:{v}');edges[u,v]=arc;incoming[v].append(arc)
                model.add(arc<=used[u]);model.add(arc<=used[v])
                model.add(delay[v]==delay[u]+step).only_enforce_if(arc)
                model.add_hint(arc,int(old_parent.get(v)==u and v!=root))
        model.add(used[root]==1);model.add(delay[root]==0)
        for v in available:
            if v!=root:model.add(sum(incoming[v])==used[v])
        for sink in sinks:
            model.add(used[sink]==1);model.add(delay[sink]<=sink_caps[sink])
        net_delay=sum(delay[router.pins[s]] for s in router.nets[nid].sinks)
        model.add(net_delay>=bounds[nid]);objective.append(net_delay);trees[nid]=edges
    for used in occupancy.values():model.add_at_most_one(used)
    model.add(sum(objective)<=baseline-int(strict));model.minimize(sum(objective))
    if strict:
        improvement=[]
        for k,nid in enumerate(ids):
            better=model.new_bool_var(f'better{nid}')
            old_dist=data[nid][6];old_cost=sum(old_dist[router.pins[s]] for s in router.nets[nid].sinks)
            model.add(objective[k]<=old_cost-1).only_enforce_if(better)
            model.add_hint(better,int(k==0));improvement.append(better)
        model.add_bool_or(improvement)
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=1;solver.parameters.random_seed=1
    solver.parameters.max_time_in_seconds=seconds;solver.parameters.max_deterministic_time=deterministic
    status=solver.solve(model);result={}
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        for nid,edges in trees.items():
            parent={v:u for (u,v),var in edges.items() if solver.value(var)};root=data[nid][0];retained={root};selected=set()
            for s in router.nets[nid].sinks:
                v=router.pins[s];seen=set()
                while v not in retained:
                    assert v not in seen;seen.add(v);retained.add(v);u=parent[v];selected.add(tuple(sorted((u,v))));v=u
            result[nid]=NetRoute(nid,sorted(selected))
    no_gain=strict and status==cp_model.INFEASIBLE
    bound=baseline if no_gain else min(baseline,solver.best_objective_bound)
    return result,{'status':solver.status_name(status),'restricted_optimal':status==cp_model.OPTIMAL or no_gain,'proved_no_improvement':no_gain,'strict_improvement':strict,'baseline':baseline,'bound':bound,'solver_bound':solver.best_objective_bound,'objective':solver.objective_value if result else None,'wall_s':solver.wall_time,'deterministic_time':solver.response_proto.deterministic_time,'graph_vertices':len(vertices),'flow_variables':sum(len(v) for v in trees.values()),'pruned_arcs':pruned,'independent_group_bound':sum(bounds.values()),'method':'arborescence physical-distance potentials','bound_model':'per-sink coupled excess slack','group_slack':slack,'sink_count':sum(len(router.nets[j].sinks) for j in ids)}
