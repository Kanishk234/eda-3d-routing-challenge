"""Bounded own-tree comparison of legacy merge, reuse and relocation.
Every alternative is individually checked; restricted CP selection then checks
whole-case legality. Incumbents are preserved and never overwritten.
"""
import argparse,json,time,resource
from pathlib import Path
from component_reuse import ReuseRouter
from branch_repair import Limit
from measure import ROOT,OFFICIAL,digest,save
from run_polish import Instance,Submission,check
from select_tree_pool import solve_pool

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();a.out.mkdir(parents=True);(a.out/'routes').mkdir();plan=json.loads(a.plan.read_text());stage=next(x for x in json.loads((ROOT/plan['coverage']).read_text())['rows'] if x['tier']=='hard');suite=stage['config']['suite'];frozen={str(q.resolve()):digest(q) for q in [a.plan,Path(__file__),ROOT/plan['coverage'],ROOT/'dev/component_reuse.py',ROOT/'dev/component_router.py',ROOT/'dev/branch_repair.py',ROOT/'dev/select_tree_pool.py']};report=dict(status='running',plan=plan,source_sha256=frozen,rows=[],scope='Own parent trees; independently implemented vertex-price component hypotheses,not paper guarantee. Restricted CP optimality only. Each method gets separate equal work/time ceilings;not isolated wall timings.');save(a.out/'progress.json',report)
 for name in plan['cases']:
  path=OFFICIAL/suite/(name+'.json');source=ROOT/'dev/artifacts'/stage['run_id']/'routes'/(name+'.sol.json');inst=Instance.load(path);sub=Submission.load(source);before=check(inst,sub);assert before.legal;seed_router=ReuseRouter(inst,sub,1,1,plan['seed']);delays={r.net:r.delay for r in before.nets};pool={n.id:[] for n in inst.nets};seen={n.id:set() for n in inst.nets}
  def add(tree):
   key=tuple(sorted(tuple(sorted(e)) for e in tree.edges))
   if key in seen[tree.net]:return False
   nr=next(x for x in check(inst,Submission(inst.name,[tree])).nets if x.net==tree.net);assert nr.legal;pool[tree.net].append((tree,nr.delay,seed_router.vertices(tree)));seen[tree.net].add(key);return True
  for tree in sub.routes:add(tree)
  def gap(n):
   root=seed_router.pins[n.driver];lower=0
   for s in n.sinks:
    v=seed_router.pins[s];d=abs(root[0]-v[0])+abs(root[1]-v[1]);lower+=min(d*inst.layer_delay[z]+inst.via_delay*(abs(root[2]-z)+abs(v[2]-z)) for z in range(inst.layers))
   return delays[n.id]-lower
  nets=sorted([n for n in inst.nets if 2<=len(n.sinks)<=plan['max_sinks']],key=lambda n:(-gap(n),n.id))[:plan['nets']];methods=[]
  for method in ['merge','reuse','relocated']:
   router=ReuseRouter(inst,sub,plan['work_budget'],plan['budget'],plan['seed']);started=time.monotonic();limited=False;generated=0;attempts=0
   try:
    for n in nets:
     for penalty in plan['penalties']:
      prices={v:penalty for v,owner in router.owner.items() if owner!=n.id};attempts+=1;tree=router.build(n.id,prices,'merge') if method=='merge' else router.build_reuse(n.id,prices,method=='relocated')
      if tree:generated+=int(add(tree))
   except Limit:limited=True
   methods.append(dict(method=method,attempts=attempts,unique_trees_added=generated,expansions=router.expansions,limited=limited,wall_s=time.monotonic()-started))
  ids=sorted(pool);chosen,stats=solve_pool([[t[1] for t in pool[i]] for i in ids],[[t[2] for t in pool[i]] for i in ids],[0]*len(ids),10,2);out=Submission(inst.name,[pool[i][chosen[k]][0] for k,i in enumerate(ids)]);after=check(inst,out);assert after.legal and after.total_delay<=before.total_delay;target=a.out/'routes'/(name+'.sol.json');out.save(str(target));assert check(inst,Submission.load(target)).legal
  report['rows'].append(dict(case=name,case_sha256=digest(path),parent_sha256=digest(source),output_sha256=digest(target),before_delay=before.total_delay,after_delay=after.total_delay,legal=True,selected_nets=[n.id for n in nets],methods=methods,selection=stats));save(a.out/'progress.json',report);print(name,'gain',before.total_delay-after.total_delay,flush=True)
 assert all(digest(Path(q))==h for q,h in frozen.items());report.update(status='complete',peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);save(a.out/'progress.json',report)
if __name__=='__main__':main()
