"""Static vertex-conflict branching with exact driver-rooted tree lower bounds."""
import heapq,time
from collections import defaultdict,Counter
from run_polish import NetRoute

class Budget(Exception):pass

def solve_cbs(router,ids,vertices,seconds=10,unused_deterministic=None,unused_prune=None,work_limit=200000,avoid_ties=False,bypass=False):
    start=time.monotonic();expansions=0;searches=0;nodes=0;cache={};serial=0;bypasses=0
    baseline=0;initial={j:router.routes[j] for j in ids}
    for nid in ids:
        _,d,_=router.tree(initial[nid]);baseline+=sum(d[router.pins[s]] for s in router.nets[nid].sinks)
    adjacency={nid:{u:[(v,w) for v,w in router.neighbors(u) if v in vertices and router.pin_owner.get(v,nid)==nid] for u in vertices if router.pin_owner.get(u,nid)==nid} for nid in ids}
    def low_level(k,forbidden):
        nonlocal expansions,searches
        key=k,forbidden
        if key in cache:return cache[key]
        searches+=1;nid=ids[k];n=router.nets[nid];root=router.pins[n.driver];sinks=[router.pins[s] for s in n.sinks]
        if root in forbidden or any(s in forbidden for s in sinks):cache[key]=None;return None
        # Secondary cost only orders equal physical distances. Static baseline
        # occupancy keeps the constraint cache valid across high-level nodes.
        def secondary(v):
            owner=router.owner.get(v,nid)
            return int(avoid_ties and owner in ids and owner!=nid)
        dist={root:(0,0)};parent={};q=[(0,0,root)];todo=set(sinks)
        while q and todo:
            cost,tie,u=heapq.heappop(q)
            if (cost,tie)!=dist[u]:continue
            if expansions>=work_limit or time.monotonic()-start>=seconds:raise Budget
            expansions+=1;todo.discard(u)
            for v,weight in adjacency[nid][u]:
                if v in forbidden:continue
                nxt=(cost+weight,tie+secondary(v))
                if nxt<dist.get(v,(10**30,10**30)):dist[v]=nxt;parent[v]=u;heapq.heappush(q,(*nxt,v))
        if todo:cache[key]=None;return None
        included={root};edges=set();flow=Counter()
        for sink in sinks:
            u=sink;flow[u]+=1
            while u!=root:u=parent[u];flow[u]+=1
            u=sink
            while u not in included:included.add(u);v=parent[u];edges.add(tuple(sorted((u,v))));u=v
        result=(NetRoute(nid,sorted(edges)),sum(dist[s][0] for s in sinks),included,flow);cache[key]=result;return result
    queue=[];pending=0;proved=False;answer=initial;objective=baseline;seen=set()
    try:
        constraints=tuple(frozenset() for _ in ids);trees=tuple(low_level(k,c) for k,c in enumerate(constraints))
        assert all(t is not None for t in trees) # Verified old trees make graph feasible.
        root_bound=sum(t[1] for t in trees);pending=root_bound
        if root_bound>=baseline:proved=True
        else:heapq.heappush(queue,(root_bound,0,serial,constraints,trees));seen.add(constraints)
        while queue and not proved:
            if time.monotonic()-start>=seconds or expansions>=work_limit:raise Budget
            bound,_,_,constraints,trees=heapq.heappop(queue);pending=bound;nodes+=1
            if bound>=baseline:proved=True;break
            occupied=defaultdict(list)
            for k,t in enumerate(trees):
                for v in t[2]:occupied[v].append(k)
            conflicts=[(v,owners) for v,owners in occupied.items() if len(owners)>1]
            if not conflicts:
                answer={nid:trees[k][0] for k,nid in enumerate(ids)};objective=bound;proved=True;break
            # Priority changes branching order only. No time-step conflicts.
            vertex,owners=min(conflicts,key=lambda item:(-sum(trees[k][3][item[0]] for k in item[1]),item[0]))
            if bypass:
                current_conflicts=sum(len(o)*(len(o)-1)//2 for _,o in conflicts)
                adopted=False
                for k in owners[:2]:
                    replacement=low_level(k,constraints[k]|{vertex})
                    if replacement is None or replacement[1]!=trees[k][1]:continue
                    alternatives=list(trees);alternatives[k]=replacement
                    counts=Counter(v for t in alternatives for v in t[2])
                    if sum(n*(n-1)//2 for n in counts.values())>=current_conflicts:continue
                    # Keep the ORIGINAL constraints: the alternative remains
                    # optimal for them. Thus no feasible subtree is discarded.
                    serial+=1;bypasses+=1;adopted=True
                    heapq.heappush(queue,(bound,sum(map(len,constraints)),serial,constraints,tuple(alternatives)))
                    break
                if adopted:continue
            for k in owners[:2]:
                altered=list(constraints);altered[k]=altered[k]|{vertex};altered=tuple(altered)
                if altered in seen:continue
                seen.add(altered);replacement=low_level(k,altered[k])
                if replacement is None:continue
                new_trees=list(trees);new_trees[k]=replacement;new_trees=tuple(new_trees)
                new_bound=sum(t[1] for t in new_trees)
                if new_bound>=baseline:continue
                serial+=1;heapq.heappush(queue,(new_bound,sum(map(len,altered)),serial,altered,new_trees))
        if not queue and not proved:proved=True
    except Budget:pass
    lower=objective if proved else min(baseline,pending,queue[0][0] if queue else baseline)
    return answer,{'status':'OPTIMAL' if proved else 'FEASIBLE','restricted_optimal':proved,'baseline':baseline,'objective':objective,'bound':lower,'wall_s':time.monotonic()-start,'deterministic_time':None,'graph_vertices':len(vertices),'flow_variables':0,'method':'static vertex-conflict branching','sink_count':sum(len(router.nets[j].sinks) for j in ids),'expansions':expansions,'searches':searches,'branch_nodes':nodes,'cached_constraints':len(cache),'work_limit':work_limit,'avoid_ties':avoid_ties,'bypass':bypass,'bypasses':bypasses}
