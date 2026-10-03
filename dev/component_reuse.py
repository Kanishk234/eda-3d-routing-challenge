"""Cost-distance component reuse and representative relocation prototypes.
Independent adaptation to vertex prices. Physical SPT projection and restricted
candidate selection are separate; no paper approximation guarantee imported.
"""
import heapq,time
from collections import defaultdict
from component_router import ComponentRouter
from branch_repair import Limit
from run_polish import NetRoute

class ReuseRouter(ComponentRouter):
 def connect_pair(self,nid,start,target,weight,prices,free):
  dist={start:0};parent={};q=[(0,start)]
  while q:
   cost,u=heapq.heappop(q)
   if cost!=dist[u]:continue
   if self.expansions>=self.work or time.monotonic()>=self.deadline:raise Limit
   self.expansions+=1
   if u==target:
    path=[u]
    while path[-1]!=start:path.append(parent[path[-1]])
    return cost,list(reversed(path))
   for v,delay in self.neighbors(u):
    if self.pin_owner.get(v,nid)!=nid:continue
    extra=(0 if u in free else prices.get(u,0))+(0 if v in free else prices.get(v,0))
    nxt=cost+2*weight*delay+extra
    if nxt<dist.get(v,10**30):dist[v]=nxt;parent[v]=u;heapq.heappush(q,(nxt,v))
  return None
 def project(self,nid,edges):
  root=self.pins[self.nets[nid].driver];adj=defaultdict(list)
  for a,b in edges:adj[a].append(b);adj[b].append(a)
  dist={root:0};parent={};q=[(0,root)]
  while q:
   cost,u=heapq.heappop(q)
   if cost!=dist[u]:continue
   for v in adj[u]:
    nxt=cost+self.inst.edge_delay(u,v)
    if nxt<dist.get(v,10**30):dist[v]=nxt;parent[v]=u;heapq.heappush(q,(nxt,v))
  result=set();used={root}
  for sink in sorted(self.pins[s] for s in self.nets[nid].sinks):
   if sink not in dist:return None
   u=sink
   while u not in used:used.add(u);v=parent[u];result.add(tuple(sorted((u,v))));u=v
  return NetRoute(nid,sorted(result))
 def relocate(self,root,vertices,edges,sinks,candidates):
  adj=defaultdict(list)
  for a,b in edges:adj[a].append(b);adj[b].append(a)
  totals={v:0 for v in vertices}
  for sink in sinks:
   dist={sink:0};q=[(0,sink)]
   while q:
    cost,u=heapq.heappop(q)
    if cost!=dist[u]:continue
    if self.expansions>=self.work or time.monotonic()>=self.deadline:raise Limit
    self.expansions+=1
    for v in adj[u]:
     nxt=cost+self.inst.edge_delay(u,v)
     if nxt<dist.get(v,10**30):dist[v]=nxt;heapq.heappush(q,(nxt,v))
   for v in totals:totals[v]+=dist.get(v,10**30)
  def lower(v):
   d=abs(root[0]-v[0])+abs(root[1]-v[1])
   return min(d*self.inst.layer_delay[z]+self.inst.via_delay*(abs(root[2]-z)+abs(v[2]-z)) for z in range(self.inst.layers))
  return min(candidates,key=lambda v:(totals[v]+len(sinks)*lower(v),v))
 def build_reuse(self,nid,prices,relocated=False):
  net=self.nets[nid];root=self.pins[net.driver];active={self.pins[s]:dict(weight=1,vertices={self.pins[s]},edges=set(),sinks={self.pins[s]}) for s in net.sinks};root_component=dict(vertices={root},edges=set());all_edges=set()
  active.pop(root,None)
  while active:
   choices=[]
   for u,a in active.items():
    for v,b in [(root,root_component),*[(v,b) for v,b in active.items() if v!=u and b['weight']>=a['weight']]]:
     result=self.connect_pair(nid,u,v,a['weight'],prices,a['vertices']|b['vertices'])
     if result:choices.append((result[0],u,v,result[1]))
   if not choices:return None
   _,u,v,path=min(choices,key=lambda c:(c[0],c[1],c[2]));new_edges={tuple(sorted(e)) for e in zip(path,path[1:])};all_edges.update(new_edges);a=active.pop(u)
   if v==root:
    root_component['vertices'].update(a['vertices']|set(path));root_component['edges'].update(a['edges']|new_edges)
   else:
    b=active.pop(v);merged=dict(weight=a['weight']+b['weight'],vertices=a['vertices']|b['vertices']|set(path),edges=a['edges']|b['edges']|new_edges,sinks=a['sinks']|b['sinks'])
    representative=u if self.rng.randrange(merged['weight'])<a['weight'] else v
    if relocated:
     candidates=set(path)-set(active)-{root}
     if candidates:representative=self.relocate(root,merged['vertices'],merged['edges'],merged['sinks'],candidates)
    active[representative]=merged
   self.stats['component_connections']+=1
  return self.project(nid,all_edges)
