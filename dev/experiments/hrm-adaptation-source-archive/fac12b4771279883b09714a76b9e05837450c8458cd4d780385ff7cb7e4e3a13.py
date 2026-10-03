"""Independent CPU prototype: reserve an ideal tree, relocate blocking branches."""
import argparse,heapq,random,time
from collections import defaultdict
from pathlib import Path
from measure import ROOT,OFFICIAL,digest,save,source_identity
from run_polish import Instance,Submission,NetRoute,check

class Limit(Exception):pass

class Router:
    def __init__(self,inst,sub,work,seconds,seed):
        self.inst=inst;self.pins=inst.pin_vertex();self.nets={n.id:n for n in inst.nets}
        self.routes={r.net:r for r in sub.routes};self.owner={};self.pin_owner={}
        self.expansions=0;self.work=work;self.deadline=time.monotonic()+seconds
        self.rng=random.Random(seed);self.stats=defaultdict(int)
        for n in inst.nets:
            for pin in n.pins():self.pin_owner[self.pins[pin]]=n.id
        self.reown()
    def vertices(self,r):
        return {self.pins[self.nets[r.net].driver]}|{v for e in r.edges for v in e}
    def reown(self):
        self.owner={v:r.net for r in self.routes.values() for v in self.vertices(r)}
    def neighbors(self,u):
        x,y,z=u
        for v in [(x+1,y,z),(x-1,y,z),(x,y+1,z),(x,y-1,z),(x,y,z+1),(x,y,z-1)]:
            if self.inst.in_bounds(v):yield v,self.inst.edge_delay(u,v)
    def tree(self,r):
        root=self.pins[self.nets[r.net].driver];adj=defaultdict(list)
        for a,b in r.edges:adj[a].append(b);adj[b].append(a)
        parent={root:root};dist={root:0};order=[root]
        for u in order:
            for v in adj[u]:
                if v not in parent:parent[v]=u;dist[v]=dist[u]+self.inst.edge_delay(u,v);order.append(v)
        return parent,dist,order
    def search(self,nid,sinks,retained,blocked,ignore=False):
        self.stats['searches']+=1
        parent,dist,_=self.tree(retained);seeds=set(dist);q=[(d,v) for v,d in dist.items()];heapq.heapify(q)
        todo=set(sinks)
        while q and todo:
            cost,u=heapq.heappop(q)
            if cost!=dist[u]:continue
            if self.expansions>=self.work or time.monotonic()>=self.deadline:raise Limit
            self.expansions+=1;todo.discard(u)
            for v,weight in self.neighbors(u):
                if v in seeds or v in blocked:continue
                if self.pin_owner.get(v,nid)!=nid:continue
                if not ignore and self.owner.get(v,nid)!=nid:continue
                new=cost+weight
                if new<dist.get(v,10**30):dist[v]=new;parent[v]=u;heapq.heappush(q,(new,v))
        if todo:return None
        edges={tuple(sorted(e)) for e in retained.edges};included=set(seeds)
        for sink in sinks:
            u=sink
            while u not in included:
                included.add(u);v=parent[u];edges.add(tuple(sorted((u,v))));u=v
        return NetRoute(nid,sorted(edges))
    def retained(self,nid,conflicts,whole):
        old=self.routes[nid];parent,dist,order=self.tree(old);root=order[0]
        if whole:return NetRoute(nid,[]),[self.pins[s] for s in self.nets[nid].sinks],len(order)
        paths=[]
        for c in conflicts:
            chain=[c]
            while chain[-1]!=root:chain.append(parent[chain[-1]])
            paths.append(list(reversed(chain)))
        common=root
        for values in zip(*paths):
            if len(set(values))!=1:break
            common=values[0]
        if common==root:self.stats['root_cut_fallback']+=1;return self.retained(nid,conflicts,True)
        removed={common}
        for v in order:
            if v!=root and parent[v] in removed:removed.add(v)
        edges=[e for e in old.edges if not any(v in removed for v in e)]
        sinks=[self.pins[s] for s in self.nets[nid].sinks if self.pins[s] in removed]
        return NetRoute(nid,edges),sinks,len(removed)
    def run(self,mode,passes):
        try:
            for _ in range(passes):
                order=list(self.nets);self.rng.shuffle(order)
                for nid in order:
                    self.stats['proposals']+=1;n=self.nets[nid];sinks=[self.pins[s] for s in n.sinks]
                    ideal=self.search(nid,sinks,NetRoute(nid,[]),set(),True)
                    if ideal is None:continue
                    _,old_dist,_=self.tree(self.routes[nid]);_,ideal_dist,_=self.tree(ideal)
                    if sum(ideal_dist[s] for s in sinks)>=sum(old_dist[s] for s in sinks):continue
                    blockers=defaultdict(set)
                    for v in self.vertices(ideal):
                        owner=self.owner.get(v,nid)
                        if owner!=nid:blockers[owner].add(v)
                    if len(blockers)>3:self.stats['over_cap']+=1;continue
                    before=self.routes.copy();old_owner=self.owner;self.owner=self.owner.copy()
                    try:
                        for v in self.vertices(self.routes[nid]):self.owner.pop(v,None)
                        plans={}
                        for bid,conflicts in blockers.items():
                            retained,partial_sinks,removed=self.retained(bid,conflicts,mode=='whole')
                            plans[bid]=(retained,partial_sinks)
                            self.stats['released_vertices']+=removed
                            for v in self.vertices(self.routes[bid])-self.vertices(retained):self.owner.pop(v,None)
                        legal=True;reserved=self.vertices(ideal)
                        bids=list(plans);self.rng.shuffle(bids)
                        for bid in bids:
                            retained,partial_sinks=plans[bid]
                            proposal=self.search(bid,partial_sinks,retained,reserved)
                            if proposal is None:legal=False;break
                            self.routes[bid]=proposal
                            for v in self.vertices(proposal):self.owner[v]=bid
                        if legal:
                            self.routes[nid]=ideal
                            candidate=Submission(self.inst.name,list(self.routes.values()));result=check(self.inst,candidate)
                            initial=check(self.inst,Submission(self.inst.name,list(before.values())))
                            if result.legal and result.total_delay<initial.total_delay:
                                self.stats['accepted']+=1;self.stats['gain']+=initial.total_delay-result.total_delay
                                self.reown();continue
                        self.stats['rejected']+=1
                    except Limit:
                        self.routes=before;self.owner=old_owner;raise
                    self.routes=before;self.owner=old_owner
        except Limit:self.stats['limit_reached']+=1
        return Submission(self.inst.name,list(self.routes.values()))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--case',type=Path,required=True);p.add_argument('--start',type=Path,required=True)
    p.add_argument('--mode',choices=['branch','whole'],default='branch');p.add_argument('--seed',type=int,default=1)
    p.add_argument('--work-budget',type=int,default=500000);p.add_argument('--budget',type=float,default=30)
    p.add_argument('--passes',type=int,default=100);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();assert not a.out.exists();assert a.work_budget>0 and a.budget>0
    a.out.mkdir(parents=True);inst=Instance.load(a.case);sub=Submission.load(a.start);before=check(inst,sub);assert before.legal
    frozen={str(q.resolve()):digest(q) for q in [a.case,a.start,Path(__file__)]};started=time.monotonic()
    router=Router(inst,sub,a.work_budget,a.budget,a.seed);candidate=router.run(a.mode,a.passes)
    after=check(inst,candidate);assert after.legal and after.total_delay<=before.total_delay
    candidate.save(str(a.out/'candidate.sol.json'));assert check(inst,Submission.load(str(a.out/'candidate.sol.json'))).total_delay==after.total_delay
    assert all(digest(Path(q))==sha for q,sha in frozen.items())
    save(a.out/'manifest.json',{'config':{k:str(v) if isinstance(v,Path) else v for k,v in vars(a).items()},'source_identity':source_identity(),'frozen_sha256':frozen,'before_delay':before.total_delay,'after_delay':after.total_delay,'legal':after.legal,'expansions':router.expansions,'stats':dict(router.stats),'wall_s':time.monotonic()-started,'output_sha256':digest(a.out/'candidate.sol.json'),'scope':'Independent Python prototype, own incumbent only. Strict legal group improvements; latest legal state restored on search limit. Equal expansions not equal CPU time. No fresh-generation claim.'})

if __name__=='__main__':main()
