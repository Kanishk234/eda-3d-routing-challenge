"""Own fresh driver-SPT negotiation; compares gradual and aggressive pricing.
No incumbent geometry, foreign-pin conflicts, or temporarily conflicting output
is accepted. Multi-sink pricing is heuristic; physical score is checked separately.
"""
import argparse,heapq,json,math,time
from collections import Counter
from pathlib import Path
from branch_repair import Router,Limit
from run_polish import Instance,Submission,NetRoute,check
from learned_fresh_order import synthetic
from measure import ROOT,OFFICIAL,digest,save

def priced_tree(r,nid,usage,history,present,divisor):
 n=r.nets[nid];root=r.pins[n.driver];todo={r.pins[s] for s in n.sinks};dist={root:0.0};parent={};q=[(0.0,r.rng.random(),root)]
 while q and todo:
  d,_,u=heapq.heappop(q)
  if d!=dist[u]:continue
  if r.expansions>=r.work or time.monotonic()>=r.deadline:raise Limit
  r.expansions+=1;todo.discard(u)
  for v,w in r.neighbors(u):
   if r.pin_owner.get(v,nid)!=nid:continue
   candidate=d+w+(history[v]+present*usage[v])/divisor
   if candidate<dist.get(v,math.inf):dist[v]=candidate;parent[v]=u;heapq.heappush(q,(candidate,r.rng.random(),v))
 if todo:return None
 edges=set();included={root}
 for s in sorted({r.pins[p] for p in n.sinks}):
  u=s
  while u not in included:included.add(u);v=parent[u];edges.add(tuple(sorted((u,v))));u=v
 return NetRoute(nid,sorted(edges))

def construct(inst,seed,work,seconds,settings,rounds):
 empty=Submission(inst.name,[NetRoute(n.id,[]) for n in inst.nets]);r=Router(inst,empty,work,seconds,seed)
 routes={};usage=Counter();history=Counter();best=None;best_delay=None;trace=[];limited=False;start=time.monotonic()
 try:
  for iteration in range(rounds):
   ids=list(r.nets)
   if settings.get('conflict_only') and iteration:
    over={v for v,c in usage.items() if c>1}
    if not over:break
    if iteration % settings.get('full_every',10):ids=[nid for nid in ids if r.vertices(routes[nid]) & over]
   r.rng.shuffle(ids);present=min(settings['cap'],settings['initial']*settings['multiplier']**iteration)
   for nid in ids:
    if nid in routes:usage.subtract(r.vertices(routes[nid]))
    divisor=max(1,len(r.nets[nid].sinks))**settings['fanout_power']
    tree=priced_tree(r,nid,usage,history,present,divisor)
    if tree is None:return best,dict(expansions=r.expansions,rounds=trace,limited=False,wall_s=time.monotonic()-start,unreachable=True)
    routes[nid]=tree;usage.update(r.vertices(tree))
   # Recompute ownership counts to independently guard incremental accounting.
   exact=Counter(v for tree in routes.values() for v in r.vertices(tree))
   assert +usage==exact
   conflicts={v:c for v,c in exact.items() if c>1};usage=exact
   row=dict(iteration=iteration,present=present,conflicting_vertices=len(conflicts),expansions=r.expansions)
   if not conflicts:
    out=Submission(inst.name,[routes[i] for i in sorted(routes)]);checked=check(inst,out);assert checked.legal;row['delay']=checked.total_delay
    if best_delay is None or checked.total_delay<best_delay:best=out;best_delay=checked.total_delay
   trace.append(row)
   for v,c in conflicts.items():history[v]+=settings['history']*(c-1)
 except Limit:limited=True
 return best,dict(expansions=r.expansions,rounds=trace,limited=limited,wall_s=time.monotonic()-start,unreachable=False)

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();a.out.mkdir(parents=True)
 plan=json.loads(a.plan.read_text());sources=[a.plan,Path(__file__),ROOT/'dev/branch_repair.py',ROOT/'dev/learned_fresh_order.py'];frozen={str(p.resolve()):digest(p) for p in sources};report=dict(status='running',plan=plan,source_sha256=frozen,rows=[],workers=1,scope='Own fresh geometry; heuristic multi-sink tolls; matched expansion/time ceilings. Every failure retained. No full-tier claim.');save(a.out/'progress.json',report)
 for case in plan['cases']:
  if 'synthetic_seed' in case:inst=synthetic(case['synthetic_seed']);case_hash=None
  else:path=OFFICIAL/case['suite']/case['file'];inst=Instance.load(path);case_hash=digest(path)
  for seed in plan['seeds']:
   for name,settings in plan['schedules'].items():
    out,stats=construct(inst,seed,plan['work_budget'],plan['budget'],settings,plan['rounds']);legal=False;delay=None;sha=None
    if out:
     target=a.out/f'{inst.name}-{seed}-{name}.sol.json';out.save(str(target));checked=check(inst,Submission.load(str(target)));assert checked.legal;legal=True;delay=checked.total_delay;sha=digest(target)
    report['rows'].append(dict(case=case,case_sha256=case_hash,seed=seed,schedule=name,legal=legal,delay=delay,output_sha256=sha,**stats));save(a.out/'progress.json',report);print(inst.name,seed,name,legal,delay,flush=True)
 assert all(digest(Path(p))==h for p,h in frozen.items());report['status']='complete';save(a.out/'progress.json',report)
if __name__=='__main__':main()
