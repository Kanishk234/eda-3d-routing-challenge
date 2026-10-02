"""Generate individually checked priced trees; global compatibility is deferred."""
import argparse,heapq,json,random,time
from pathlib import Path
from measure import ROOT,OFFICIAL,digest,save
from run_polish import Instance,Submission,NetRoute,check
from branch_repair import Router,Limit

def priced_tree(router,nid,penalty):
    n=router.nets[nid];root=router.pins[n.driver];sinks={router.pins[s] for s in n.sinks};todo=sinks.copy()
    dist={root:0};parent={};q=[(0,root)]
    while q and todo:
        cost,u=heapq.heappop(q)
        if cost!=dist[u]:continue
        if router.expansions>=router.work or time.monotonic()>=router.deadline:raise Limit
        router.expansions+=1;todo.discard(u)
        for v,delay in router.neighbors(u):
            if router.pin_owner.get(v,nid)!=nid:continue
            price=penalty if router.owner.get(v,nid)!=nid else 0
            nxt=cost+16*(delay+price)
            if nxt<dist.get(v,10**30):dist[v]=nxt;parent[v]=u;heapq.heappush(q,(nxt,v))
    if todo:return None
    included={root};edges=set()
    for sink in sorted(sinks):
        u=sink
        while u not in included:included.add(u);v=parent[u];edges.add(tuple(sorted((u,v))));u=v
    return NetRoute(nid,sorted(edges))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists()
    plan=json.loads(a.plan.read_text());source=[a.plan,Path(__file__),Path(__file__).with_name('branch_repair.py')];frozen={str(q.resolve()):digest(q) for q in source};out={'plan':plan,'frozen_sha256':frozen,'status':'running','cases':{},'scope':'Trees individually official-checked against full terminal map; may conflict across nets. Not a legal suite or a claimed score until exact pool selection plus whole-case checking. All seed routes are our own recorded incumbents.'};save(a.out,out)
    start=time.monotonic()
    try:
        inventory=json.loads((OFFICIAL/plan['suite']/'suite.json').read_text())
        for item in inventory['cases']:
            assert all(digest(Path(q))==sha for q,sha in frozen.items())
            case=OFFICIAL/plan['suite']/item['instance_file'];route=ROOT/'dev/artifacts'/plan['run_id']/'routes'/(item['name']+'.sol.json')
            inst=Instance.load(case);sub=Submission.load(route);assert check(inst,sub).legal
            router=Router(inst,sub,plan['work_budget'],plan['budget'],plan['seed']);trees=[];before={str(case):digest(case),str(route):digest(route)}
            try:
                for penalty in plan['penalties']:
                    order=list(router.nets);router.rng.shuffle(order)
                    for nid in order:
                        tree=priced_tree(router,nid,penalty)
                        if tree is None:continue
                        individual=check(inst,Submission(inst.name,[tree]));result=next(n for n in individual.nets if n.net==nid);assert result.legal
                        trees.append({'net':nid,'penalty':penalty,'delay':result.delay,'route':{'net':nid,'edges':[[list(u),list(v)] for u,v in tree.edges]}})
            except Limit:pass
            assert all(digest(Path(q))==sha for q,sha in before.items())
            out['cases'][item['name']]={'case_sha256':digest(case),'start_sha256':digest(route),'trees':trees,'expansions':router.expansions};out['elapsed_wall_s']=time.monotonic()-start;save(a.out,out);print(item['name'],len(trees),'trees',router.expansions,'expansions',flush=True)
        assert all(digest(Path(q))==sha for q,sha in frozen.items())
        out['status']='complete';out['elapsed_wall_s']=time.monotonic()-start;save(a.out,out)
    except BaseException as error:out['status']='failed';out['error']=repr(error);save(a.out,out);raise

if __name__=='__main__':main()
