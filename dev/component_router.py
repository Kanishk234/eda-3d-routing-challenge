"""Fresh CPU construction with sink-component merging and sparse negotiation."""
import argparse,heapq,json,time
from collections import Counter,defaultdict
from pathlib import Path
from branch_repair import Router,Limit
from run_polish import Instance,Submission,NetRoute,check
from measure import digest,save

class ComponentRouter(Router):
    def connect(self,nid,start,targets,weight,prices):
        dist={start:0};parent={};q=[(0,start)]
        while q:
            cost,u=heapq.heappop(q)
            if cost!=dist[u]:continue
            if self.expansions>=self.work or time.monotonic()>=self.deadline:raise Limit
            self.expansions+=1
            if u in targets:
                edges=[];v=u
                while v!=start:edges.append(tuple(sorted((v,parent[v]))));v=parent[v]
                return cost,u,edges
            for v,delay in self.neighbors(u):
                if self.pin_owner.get(v,nid)!=nid:continue
                # Symmetric vertex-price approximation; both directions pay alike.
                nxt=cost+2*weight*delay+prices.get(u,0)+prices.get(v,0)
                if nxt<dist.get(v,10**30):dist[v]=nxt;parent[v]=u;heapq.heappush(q,(nxt,v))
        return None
    def build(self,nid,prices,method):
        n=self.nets[nid];root=self.pins[n.driver];sinks=[self.pins[s] for s in n.sinks]
        active={s:1 for s in sinks if s!=root};edges=set()
        while active:
            choices=[]
            for u,weight in active.items():
                targets={root}|{v for v,w in active.items() if v!=u and w>=weight}
                if method=='star':targets={root}
                found=self.connect(nid,u,targets,weight if method=='merge' else 1,prices)
                if found:choices.append((found[0],u,found[1],found[2]))
            if not choices:return None
            _,u,v,path=min(choices,key=lambda x:(x[0],x[1],x[2]));edges.update(path)
            if v==root:del active[u]
            else:
                wu,wv=active.pop(u),active.pop(v)
                representative=u if self.rng.randrange(wu+wv)<wu else v
                active[representative]=wu+wv
            self.stats['component_connections']+=1
        # Embedded path unions can have cycles. Root-SPT projection creates one
        # legal coherent tree and recomputes physical sink delays independently.
        adjacency=defaultdict(list)
        for a,b in edges:adjacency[a].append(b);adjacency[b].append(a)
        dist={root:0};parent={};q=[(0,root)]
        while q:
            cost,u=heapq.heappop(q)
            if cost!=dist[u]:continue
            for v in adjacency[u]:
                nxt=cost+self.inst.edge_delay(u,v)
                if nxt<dist.get(v,10**30):dist[v]=nxt;parent[v]=u;heapq.heappush(q,(nxt,v))
        retained={root};result=set()
        for s in sinks:
            if s not in dist:return None
            u=s
            while u not in retained:retained.add(u);v=parent[u];result.add(tuple(sorted((u,v))));u=v
        return NetRoute(nid,sorted(result))
    def construct(self,method,rounds):
        # No incumbent edges enter construction; only terminal ownership does.
        self.routes={nid:NetRoute(nid,[]) for nid in self.nets};self.owner={}
        history=Counter();usage=Counter(v for r in self.routes.values() for v in self.vertices(r));best=None;best_delay=None
        try:
            for iteration in range(rounds):
                order=list(self.nets);self.rng.shuffle(order)
                for nid in order:
                    for v in self.vertices(self.routes[nid]):usage[v]-=1
                    prices={v:history[v]+(2+2*iteration)*max(0,usage[v]) for v in set(history)|set(usage) if history[v] or usage[v]>0}
                    r=self.build(nid,prices,method)
                    if r is None:return best
                    self.routes[nid]=r
                    for v in self.vertices(r):usage[v]+=1
                # Count resources exactly once per owning net, root included.
                usage=Counter(v for r in self.routes.values() for v in self.vertices(r))
                conflicts={v:c for v,c in usage.items() if c>1}
                self.stats['rounds']+=1;self.stats['conflicting_vertices']+=len(conflicts)
                if not conflicts:
                    sub=Submission(self.inst.name,list(self.routes.values()));checked=check(self.inst,sub)
                    assert checked.legal
                    if best_delay is None or checked.total_delay<best_delay:best=sub;best_delay=checked.total_delay
                for v,c in conflicts.items():history[v]+=2*(c-1)
        except Limit:self.stats['limit_reached']+=1
        return best

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--case',type=Path,required=True)
    p.add_argument('--method',choices=['merge','star'],default='merge');p.add_argument('--seed',type=int,default=1)
    p.add_argument('--work-budget',type=int,default=1000000);p.add_argument('--budget',type=float,default=30)
    p.add_argument('--rounds',type=int,default=24);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();assert not a.out.exists();assert a.work_budget>0 and a.budget>0 and a.rounds>0;a.out.mkdir(parents=True)
    frozen={str(q.resolve()):digest(q) for q in [a.case,Path(__file__),Path(__file__).with_name('branch_repair.py')]}
    inst=Instance.load(a.case);empty=Submission(inst.name,[NetRoute(n.id,[]) for n in inst.nets]);start=time.monotonic()
    router=ComponentRouter(inst,empty,a.work_budget,a.budget,a.seed);candidate=router.construct(a.method,a.rounds)
    result=check(inst,candidate) if candidate else None
    if candidate:candidate.save(str(a.out/'candidate.sol.json'));assert check(inst,Submission.load(str(a.out/'candidate.sol.json'))).legal
    assert all(digest(Path(q))==sha for q,sha in frozen.items())
    save(a.out/'manifest.json',{'config':{k:str(v) if isinstance(v,Path) else v for k,v in vars(a).items()},'frozen_sha256':frozen,'legal':bool(result and result.legal),'delay':result.total_delay if result else None,'expansions':router.expansions,'stats':dict(router.stats),'wall_s':time.monotonic()-start,'output_sha256':digest(a.out/'candidate.sol.json') if candidate else None,'scope':'Fresh construction, no route warm start. Independent Python component-merging heuristic inspired by Held/Perner; symmetric vertex prices and shortest-tree projection change formulation. No approximation guarantee claimed. Incomplete construction produces no candidate.'})

if __name__=='__main__':main()
