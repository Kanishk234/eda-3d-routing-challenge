"""Generate coordinated tree alternatives with adaptive capacity prices.

This is a heuristic pricing oracle for multi-sink trees, not exact column
 generation or a certified Lagrangian bound. Final selection is exact only
within its finite tree pool when CP-SAT reports OPTIMAL.
"""
import argparse,heapq,json,time
from collections import Counter
from pathlib import Path
from branch_repair import Router,Limit
from measure import ROOT,OFFICIAL,digest,save
from run_polish import Instance,Submission,NetRoute,check
from select_tree_pool import solve_pool

def fractional_prices(ids,pool):
    from ortools.linear_solver import pywraplp
    solver=pywraplp.Solver.CreateSolver('GLOP');assert solver is not None
    capacities={};owners={};variables=[]
    for nid in ids:
        equality=solver.Constraint(1,1);row=[]
        for k,(tree,cost,vertices) in enumerate(pool[nid]):
            variable=solver.NumVar(0,1,f'n{nid}t{k}');equality.SetCoefficient(variable,1)
            solver.Objective().SetCoefficient(variable,16*cost);row.append((variable,vertices))
            for v in vertices:owners.setdefault(v,set()).add(nid)
        variables.extend(row)
    for v,used in owners.items():
        if len(used)>1:capacities[v]=solver.Constraint(0,1)
    for variable,vertices in variables:
        for v in vertices:
            if v in capacities:capacities[v].SetCoefficient(variable,1)
    solver.Objective().SetMinimization();status=solver.Solve();assert status==solver.OPTIMAL
    # <= capacity has a nonpositive dual in a minimization model. Keep float
    # prices through oracle search; integer rounding would alter reduced costs.
    return {v:max(0,-c.dual_value()) for v,c in capacities.items()},solver.Objective().Value()/16

def priced(router,nid,prices):
    n=router.nets[nid];root=router.pins[n.driver];todo={router.pins[s] for s in n.sinks}
    divisor=max(1,len(todo));dist={root:0};parent={};q=[(0,root)]
    while q and todo:
        cost,u=heapq.heappop(q)
        if cost!=dist[u]:continue
        if router.expansions>=router.work or time.monotonic()>=router.deadline:raise Limit
        router.expansions+=1;todo.discard(u)
        for v,w in router.neighbors(u):
            if router.pin_owner.get(v,nid)!=nid:continue
            nxt=cost+16*w+prices.get(v,0)/divisor
            if nxt<dist.get(v,10**30):dist[v]=nxt;parent[v]=u;heapq.heappush(q,(nxt,v))
    if todo:return None
    included={root};edges=set()
    for sink in sorted({router.pins[s] for s in n.sinks}):
        u=sink
        while u not in included:included.add(u);v=parent[u];edges.add(tuple(sorted((u,v))));u=v
    return NetRoute(nid,sorted(edges))

def generate(router,rounds,step,pricing='subgradient'):
    ids=sorted(router.nets);pool={i:[] for i in ids};seen={i:set() for i in ids};prices={};history=[]
    def add(tree):
        nid=tree.net;key=tuple(sorted(tuple(sorted(e)) for e in tree.edges))
        if key in seen[nid]:return
        nr=next(r for r in check(router.inst,Submission(router.inst.name,[tree])).nets if r.net==nid)
        assert nr.legal;seen[nid].add(key);pool[nid].append((tree,nr.delay,router.vertices(tree)))
    for nid in ids:add(router.routes[nid])
    limited=False
    for iteration in range(rounds):
        completed=0
        try:
            order=ids.copy();router.rng.shuffle(order)
            for nid in order:
                tree=priced(router,nid,prices)
                if tree:add(tree)
                completed+=1
        except Limit:limited=True
        # Selection here is intentionally allowed to conflict: it drives prices,
        # never becomes an incumbent. Vertex toll paid once per owning tree.
        chosen=[min(pool[i],key=lambda t:16*t[1]+sum(prices.get(v,0) for v in t[2])) for i in ids]
        usage=Counter(v for tree,cost,vertices in chosen for v in vertices)
        conflicts=sum(max(0,c-1) for c in usage.values())
        history.append(dict(round=iteration+1,generated_nets=completed,conflicts=conflicts,relaxed_physical_delay=sum(t[1] for t in chosen),expansions=router.expansions))
        if pricing=='lp':
            prices,bound=fractional_prices(ids,pool);history[-1]['restricted_fractional_delay']=bound
        else:
            for v in set(prices)|set(usage):
                value=max(0,prices.get(v,0)+step*(usage.get(v,0)-1))
                if value:prices[v]=value
                else:prices.pop(v,None)
        if limited:break
    return ids,pool,history,limited

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('plan',type=Path);parser.add_argument('--out',type=Path,required=True);a=parser.parse_args();assert not a.out.exists();a.out.mkdir(parents=True);(a.out/'routes').mkdir()
    plan=json.loads(a.plan.read_text());coverage=json.loads((ROOT/plan['coverage']).read_text());stage=next(r for r in coverage['rows'] if r['tier']==plan['tier']);suite=stage['config']['suite']
    frozen={str(p.resolve()):digest(p) for p in [a.plan,Path(__file__),ROOT/plan['coverage'],ROOT/'dev/branch_repair.py',ROOT/'dev/select_tree_pool.py']}
    report=dict(plan=plan,status='running',frozen_sha256=frozen,rows=[],workers=1,scope='Adaptive heuristic pricing; no multi-sink oracle exactness or global lower bound. Own baseline always retained; final finite-pool CP selection plus full official checker.')
    save(a.out/'progress.json',report)
    for item in json.loads((OFFICIAL/suite/'suite.json').read_text())['cases']:
        if item['name'] not in plan['cases']:continue
        case=OFFICIAL/suite/item['instance_file'];source=ROOT/'dev/artifacts'/stage['run_id']/'routes'/(item['name']+'.sol.json');inst=Instance.load(case);sub=Submission.load(source);before=check(inst,sub);assert before.legal
        router=Router(inst,sub,plan['work_budget'],plan['budget'],plan['seed']);start=time.monotonic();ids,pool,rounds,limited=generate(router,plan['rounds'],plan['price_step'],plan.get('pricing','subgradient'))
        chosen,stats=solve_pool([[t[1] for t in pool[i]] for i in ids],[[t[2] for t in pool[i]] for i in ids],[0]*len(ids),plan['solve_seconds'],plan['solve_deterministic'])
        out=Submission(inst.name,[pool[i][chosen[k]][0] for k,i in enumerate(ids)]);checked=check(inst,out);assert checked.legal and checked.total_delay<=before.total_delay
        target=a.out/'routes'/(item['name']+'.sol.json');out.save(str(target));assert check(inst,Submission.load(str(target))).total_delay==checked.total_delay
        report['rows'].append(dict(case=item['name'],case_sha256=digest(case),start_sha256=digest(source),output_sha256=digest(target),before_delay=before.total_delay,after_delay=checked.total_delay,legal=True,rounds=rounds,limit_reached=limited,expansions=router.expansions,wall_s=time.monotonic()-start,selection=stats));save(a.out/'progress.json',report);print(item['name'],'gain',before.total_delay-checked.total_delay,'rounds',len(rounds),flush=True)
    assert all(digest(Path(p))==sha for p,sha in frozen.items());report['status']='complete';save(a.out/'progress.json',report)
if __name__=='__main__':main()
