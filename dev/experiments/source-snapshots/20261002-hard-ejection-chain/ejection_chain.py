"""Independent dynamic whole-net displacement-chain prototype.

Concept inspected in kesudh's public replay; no code or route data copied.
A bounded chain reserves each replacement and dynamically grows its net group.
"""
import argparse,heapq,json,time
from pathlib import Path
from branch_repair import Router,Limit
from measure import ROOT,OFFICIAL,digest,save
from run_polish import Instance,Submission,NetRoute,check

def search_chain(router,nid,locked,penalty,entry):
    net=router.nets[nid];root=router.pins[net.driver];sinks={router.pins[s] for s in net.sinks};remaining=sinks.copy()
    distance={root:0};parent={};queue=[(0,root)]
    while queue and remaining:
        cost,u=heapq.heappop(queue)
        if cost!=distance[u]:continue
        if router.expansions>=router.work or time.monotonic()>=router.deadline:raise Limit
        router.expansions+=1;remaining.discard(u)
        for v,w in router.neighbors(u):
            owner=router.owner.get(v)
            if router.pin_owner.get(v,nid)!=nid or owner in locked:continue
            toll=0
            if owner is not None and owner!=nid:
                toll=penalty if not entry or router.owner.get(u)!=owner else 0
            proposed=cost+16*w+toll
            if proposed<distance.get(v,10**30):distance[v]=proposed;parent[v]=u;heapq.heappush(queue,(proposed,v))
    if remaining:return None
    used={root};edges=set()
    for sink in sorted(sinks):
        u=sink
        while u not in used:used.add(u);v=parent[u];edges.add(tuple(sorted((u,v))));u=v
    return NetRoute(nid,sorted(edges))

def attempt(router,target,cap,penalty,entry):
    old_routes=router.routes.copy();old_owner=router.owner.copy();before=check(router.inst,Submission(router.inst.name,list(old_routes.values())));assert before.legal
    pending=[target];members={target};locked=set();accepted=False;cursor=0
    def release(nid):
        for v in router.vertices(router.routes[nid]):
            if router.owner.get(v)==nid:router.owner.pop(v)
    release(target)
    try:
        while cursor<len(pending):
            nid=pending[cursor];tree=search_chain(router,nid,locked,penalty,entry)
            if tree is None:break
            vertices=router.vertices(tree);blockers={router.owner[v] for v in vertices if v in router.owner and router.owner[v]!=nid}
            if blockers&locked or len(members|blockers)>cap:break
            for blocker in sorted(blockers):
                assert blocker not in members;members.add(blocker);pending.append(blocker);release(blocker)
            assert all(v not in router.owner for v in vertices)
            router.routes[nid]=tree;router.owner.update({v:nid for v in vertices});locked.add(nid);cursor+=1
        if cursor==len(pending):
            checked=check(router.inst,Submission(router.inst.name,list(router.routes.values())));assert checked.legal
            accepted=checked.total_delay<before.total_delay
            if accepted:return dict(accepted=True,gain=before.total_delay-checked.total_delay,nets=len(members),limited=False)
    except Limit:
        return dict(accepted=False,gain=0,nets=len(members),limited=True)
    finally:
        if not accepted:router.routes=old_routes;router.owner=old_owner
    return dict(accepted=False,gain=0,nets=len(members),limited=False)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();a.out.mkdir(parents=True);(a.out/'routes').mkdir()
    plan=json.loads(a.plan.read_text());stage=next(r for r in json.loads((ROOT/plan['coverage']).read_text())['rows'] if r['tier']==plan['tier']);suite=stage['config']['suite'];frozen={str(p.resolve()):digest(p) for p in [a.plan,Path(__file__),ROOT/'dev/branch_repair.py',ROOT/plan['coverage']]}
    report=dict(plan=plan,status='running',frozen_sha256=frozen,rows=[],workers=1,scope='Dynamic whole-net displacement, bounded heuristic. Own routes, strict official physical improvements only; rollback on all limits. No global-optimality claim.');save(a.out/'progress.json',report)
    for case in json.loads((OFFICIAL/suite/'suite.json').read_text())['cases']:
        if case['name'] not in plan['cases']:continue
        path=OFFICIAL/suite/case['instance_file'];source=ROOT/'dev/artifacts'/stage['run_id']/'routes'/(case['name']+'.sol.json');inst=Instance.load(path);sub=Submission.load(source);before=check(inst,sub);assert before.legal
        router=Router(inst,sub,plan['work_budget'],plan['budget'],plan['seed']);trials=[];limited=False;start=time.monotonic()
        for _ in range(plan['passes']):
            ids=list(router.nets);router.rng.shuffle(ids)
            for nid in ids:
                trial=attempt(router,nid,plan['group_cap'],router.rng.choice(plan['penalties']),plan['entry_price']);trials.append(trial)
                if trial['limited']:limited=True;break
            if limited:break
        out=Submission(inst.name,list(router.routes.values()));after=check(inst,out);assert after.legal and after.total_delay<=before.total_delay;target=a.out/'routes'/(case['name']+'.sol.json');out.save(str(target));assert check(inst,Submission.load(str(target))).legal
        report['rows'].append(dict(case=case['name'],case_sha256=digest(path),start_sha256=digest(source),output_sha256=digest(target),before_delay=before.total_delay,after_delay=after.total_delay,legal=True,expansions=router.expansions,wall_s=time.monotonic()-start,trials=trials));save(a.out/'progress.json',report);print(case['name'],'gain',before.total_delay-after.total_delay,flush=True)
    assert all(digest(Path(p))==sha for p,sha in frozen.items());report['status']='complete';save(a.out/'progress.json',report)
if __name__=='__main__':main()
