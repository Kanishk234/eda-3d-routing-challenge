"""Evaluate licensed pretrained REST geometry as routing proposals on CPU.

REST predicts 2D wirelength-oriented topology. We use its XY corridors only
as secondary shortest-path tie preferences. Physical distance stays primary;
finite tree-pool allocation plus the official checker determines acceptance.
"""
import argparse,json,heapq,time,sys,resource
from pathlib import Path
from branch_repair import Router,Limit
from measure import ROOT,OFFICIAL,digest,save
from run_polish import Instance,Submission,NetRoute,check
from select_tree_pool import solve_pool

def template(points,indices):
    preferred=set(points)
    for a,b in zip(indices[::2],indices[1::2]):
        x,y=points[a];xx,yy=points[b]
        preferred.update((x,k) for k in range(min(y,yy),max(y,yy)+1))
        preferred.update((k,yy) for k in range(min(x,xx),max(x,xx)+1))
    return preferred

def tree_with_template(router,nid,preferred,penalty):
    n=router.nets[nid];root=router.pins[n.driver];todo={router.pins[s] for s in n.sinks};dist={root:(0,0)};parent={};queue=[(0,0,root)]
    while queue and todo:
        d,tie,u=heapq.heappop(queue)
        if (d,tie)!=dist[u]:continue
        if router.expansions>=router.work or time.monotonic()>=router.deadline:raise Limit
        router.expansions+=1;todo.discard(u)
        for v,w in router.neighbors(u):
            if router.pin_owner.get(v,nid)!=nid:continue
            toll=penalty if router.owner.get(v,nid)!=nid else 0
            candidate=(d+16*w+toll,tie+int(v[:2] not in preferred))
            if candidate<dist.get(v,(10**30,10**30)):dist[v]=candidate;parent[v]=u;heapq.heappush(queue,(*candidate,v))
    if todo:return None
    used={root};edges=set()
    for sink in sorted({router.pins[s] for s in n.sinks}):
        u=sink
        while u not in used:used.add(u);v=parent[u];edges.add(tuple(sorted((u,v))));u=v
    return NetRoute(nid,sorted(edges))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--model-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();a.out.mkdir(parents=True);(a.out/'routes').mkdir()
    import numpy as np,torch
    torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.manual_seed(1)
    manifest=json.loads((a.model_root/'manifest.json').read_text())
    for file in manifest['files']:assert digest(a.model_root/file['path'])==file['sha256']
    sys.path.insert(0,str(a.model_root.resolve()));from models.actor_critic import Actor
    # Legacy checkpoint includes a NumPy scalar evaluation metric. Keep the
    # restricted loader and allow only these known NumPy numeric types.
    with torch.serialization.safe_globals([(np._core.multiarray.scalar,'numpy.core.multiarray.scalar'),np.dtype,type(np.dtype('float64'))]):
        checkpoint=torch.load(a.model_root/'save/DAC21/rsmt5b.pt',map_location='cpu',weights_only=True)
    actor=Actor(5,torch.device('cpu'));actor.load_state_dict(checkpoint['actor_state_dict']);actor.eval()
    plan=json.loads(a.plan.read_text());stage=next(r for r in json.loads((ROOT/plan['coverage']).read_text())['rows'] if r['tier']==plan['tier']);suite=stage['config']['suite']
    sources=[a.plan,Path(__file__),ROOT/'dev/branch_repair.py',ROOT/'dev/select_tree_pool.py',ROOT/plan['coverage']];frozen={str(p.resolve()):digest(p) for p in sources}
    report=dict(status='running',plan=plan,model_manifest=manifest,torch_version=torch.__version__,cpu_threads=1,source_sha256=frozen,rows=[],scope='Existing REST5-terminal weights; adapted XY topology tie preferences. Multi-sink3D delay not training objective; degree2-5 transfer experimental. No competitor routes. Restricted finite-pool selection only.');save(a.out/'progress.json',report)
    for case in json.loads((OFFICIAL/suite/'suite.json').read_text())['cases']:
        if case['name'] not in plan['cases']:continue
        path=OFFICIAL/suite/case['instance_file'];source=ROOT/'dev/artifacts'/stage['run_id']/'routes'/(case['name']+'.sol.json');inst=Instance.load(path);sub=Submission.load(source);before=check(inst,sub);assert before.legal
        router=Router(inst,sub,plan['work_budget'],plan['budget'],1);pool={n.id:[] for n in inst.nets};seen={n.id:set() for n in inst.nets};neural_calls=0;start=time.monotonic();limited=False
        def add(tree):
            key=tuple(sorted(tuple(sorted(e)) for e in tree.edges));nid=tree.net
            if key in seen[nid]:return
            nr=next(r for r in check(inst,Submission(inst.name,[tree])).nets if r.net==nid);assert nr.legal;seen[nid].add(key);pool[nid].append((tree,nr.delay,router.vertices(tree)))
        for tree in sub.routes:add(tree)
        try:
            for n in inst.nets:
                pins=[router.pins[p] for p in n.pins()];degree=len(pins)
                if not 2<=degree<=5:continue
                points=[v[:2] for v in pins];coords=np.array([[x/inst.width,y/inst.height] for x,y in points],dtype=np.float32);actor.degree=degree
                for swap in [False,True]:
                    inputs=coords[:,::-1].copy() if swap else coords
                    with torch.inference_mode():indices,_=actor(inputs[None],True)
                    neural_calls+=1;prefer=template(points,indices[0].tolist())
                    if swap:prefer=template([(y,x) for x,y in points],indices[0].tolist());prefer={(y,x) for x,y in prefer}
                    for penalty in plan['penalties']:
                        tree=tree_with_template(router,n.id,prefer,penalty)
                        if tree:add(tree)
        except Limit:limited=True
        ids=sorted(pool);chosen,stats=solve_pool([[t[1] for t in pool[i]] for i in ids],[[t[2] for t in pool[i]] for i in ids],[0]*len(ids),10,2)
        out=Submission(inst.name,[pool[i][chosen[k]][0] for k,i in enumerate(ids)]);after=check(inst,out);assert after.legal and after.total_delay<=before.total_delay;target=a.out/'routes'/(case['name']+'.sol.json');out.save(str(target));assert check(inst,Submission.load(str(target))).legal
        report['rows'].append(dict(case=case['name'],case_sha256=digest(path),start_sha256=digest(source),output_sha256=digest(target),before_delay=before.total_delay,after_delay=after.total_delay,legal=True,neural_calls=neural_calls,expansions=router.expansions,limited=limited,selection=stats,wall_s=time.monotonic()-start));save(a.out/'progress.json',report);print(case['name'],'gain',before.total_delay-after.total_delay,flush=True)
    assert all(digest(Path(p))==sha for p,sha in frozen.items());report.update(status='complete',peak_rss_kb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);save(a.out/'progress.json',report)
if __name__=='__main__':main()
