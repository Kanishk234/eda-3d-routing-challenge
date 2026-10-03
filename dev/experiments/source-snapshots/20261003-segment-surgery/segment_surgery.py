"""Refine branch repair by preserving both sides of a blocked wire segment.
Only a pin-free degree-two connector is replaced. Downstream branches stay
fixed; root-distance-labelled multi-source search reconnects their entry.
"""
from collections import defaultdict
from branch_repair import Router
from run_polish import NetRoute

class SurgeryRouter(Router):
 def __init__(self,*args,**kwargs):
  self.segment_plans={}
  super().__init__(*args,**kwargs)
 def vertices(self,route):
  vertices=super().vertices(route)
  plan=self.segment_plans.get(route.net)
  if plan and route is plan['retained']:vertices|=plan['down_vertices']
  return vertices
 def retained(self,nid,conflicts,whole):
  self.segment_plans.pop(nid,None)
  if whole:return super().retained(nid,conflicts,whole)
  route=self.routes[nid];net=self.nets[nid];parent,dist,order=self.tree(route);root=order[0];adj=defaultdict(list)
  for a,b in route.edges:adj[a].append(b);adj[b].append(a)
  pins={self.pins[p] for p in net.pins()}
  def interior(v):return v not in pins and len(adj[v])==2
  if conflicts and all(interior(v) for v in conflicts):
   start=min(conflicts,key=lambda v:(dist[v],v));a=parent[start]
   while interior(a):a=parent[a]
   chain=[a];u=start
   # Walk the entire degree-two chain from its upstream boundary.
   u=next(v for v in adj[a] if parent.get(v)==a and (v==start or self.is_ancestor(v,start,parent)))
   chain.append(u)
   while interior(u):
    u=next(v for v in adj[u] if parent.get(v)==u);chain.append(u)
   b=chain[-1];removed=set(chain[1:-1])
   if conflicts<=removed:
    down={b}
    for v in order:
     if v!=root and parent[v] in down:down.add(v)
    down_edges=[e for e in route.edges if e[0] in down and e[1] in down]
    removed_edges={tuple(sorted(e)) for e in zip(chain,chain[1:])}
    root_edges=[e for e in route.edges if tuple(sorted(e)) not in removed_edges and not (e[0] in down and e[1] in down)]
    retained=NetRoute(nid,root_edges);sinks=sum(self.pins[s] in down for s in net.sinks)
    self.segment_plans[nid]=dict(retained=retained,down_vertices=down,down_edges=down_edges,entry=b,downstream_sinks=sinks,old_entry_delay=dist[b]);self.stats['segment_plans']+=1;self.stats['preserved_downstream_vertices']+=len(down)
    return retained,[b],len(removed)
  self.stats['segment_fallbacks']+=1
  return super().retained(nid,conflicts,whole)
 @staticmethod
 def is_ancestor(a,v,parent):
  while v!=parent[v]:
   if v==a:return True
   v=parent[v]
  return v==a
 def search(self,nid,sinks,retained,blocked,ignore=False):
  plan=self.segment_plans.get(nid)
  if not ignore and plan and retained is plan['retained']:
   blocked=set(blocked)|(plan['down_vertices']-{plan['entry']});tree=super().search(nid,sinks,retained,blocked,ignore)
   if tree is not None:
    tree.edges+=plan['down_edges'];self.stats['segment_reconnections']+=1
   return tree
  return super().search(nid,sinks,retained,blocked,ignore)
