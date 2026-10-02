"""Exact two-solution tree recombination via minimum-weight closure.

Each input must be a complete legal suite. Exactness is limited to choosing one
of those two trees per net; this is not globally optimal routing.
"""
import argparse,datetime,json,time
from collections import deque
from pathlib import Path
from measure import ROOT,OFFICIAL,REVISION,digest,save,execute
from run_polish import Instance,Submission,check,score_case,leaderboard

def minimum_closure(costs,dependencies):
    n=len(costs);source=n;sink=n+1;graph=[[] for _ in range(n+2)]
    def edge(u,v,cap):
        graph[u].append([v,cap,len(graph[v])]);graph[v].append([u,0,len(graph[u])-1])
    infinity=sum(abs(c) for c in costs)+1
    for u,c in enumerate(costs):
        if c<0:edge(source,u,-c)
        elif c>0:edge(u,sink,c)
    for u,v in sorted(set(dependencies)):
        if u!=v:edge(u,v,infinity)
    flow=0
    while True:
        parent=[None]*len(graph);parent[source]=(-1,-1);q=deque([source])
        while q and parent[sink] is None:
            u=q.popleft()
            for k,(v,cap,_) in enumerate(graph[u]):
                if cap>0 and parent[v] is None:parent[v]=(u,k);q.append(v)
        if parent[sink] is None:break
        amount=infinity;v=sink
        while v!=source:
            u,k=parent[v];amount=min(amount,graph[u][k][1]);v=u
        v=sink
        while v!=source:
            u,k=parent[v];e=graph[u][k];e[1]-=amount;graph[v][e[2]][1]+=amount;v=u
        flow+=amount
    reachable={source};q=deque([source])
    while q:
        u=q.popleft()
        for v,cap,_ in graph[u]:
            if cap>0 and v not in reachable:reachable.add(v);q.append(v)
    selected={u for u in range(n) if u in reachable}
    assert all(u not in selected or v in selected for u,v in dependencies)
    optimum=sum(costs[u] for u in selected)
    assert optimum==flow-sum(-c for c in costs if c<0)
    return selected,{'minimum_delta':optimum,'max_flow':flow,'finite_infinity':infinity}

def recombine(inst,base,donor,prefer_donor=False):
    a=check(inst,base);b=check(inst,donor);assert a.legal and b.legal
    original={r.net:r for r in base.routes};alternate={r.net:r for r in donor.routes};ids=sorted(original);assert ids==sorted(alternate)
    index={j:k for k,j in enumerate(ids)};owner={}
    pins=inst.pin_vertex();nets={n.id:n for n in inst.nets}
    def vertices(j,r):
        n=nets[j]
        return {tuple(v) for e in r.edges for v in e}|{tuple(pins[t]) for t in [n.driver,*n.sinks]}
    for j,r in original.items():
        for v in vertices(j,r):owner[v]=index[j]
    dependencies=set()
    for j,r in alternate.items():
        for v in vertices(j,r):
            other=owner.get(v)
            if other is not None and other!=index[j]:dependencies.add((index[j],other))
    da={n.net:n.delay for n in a.nets};db={n.net:n.delay for n in b.nets};costs=[db[j]-da[j] for j in ids]
    scale=len(costs)+1 if prefer_donor else 1
    weighted=[c*scale-int(prefer_donor) for c in costs]
    chosen,certificate=minimum_closure(weighted,dependencies)
    certificate['weighted_minimum_delta']=certificate['minimum_delta']
    certificate['minimum_delta']=sum(costs[k] for k in chosen)
    certificate['primary_scale']=scale
    certificate['prefer_donor']=prefer_donor
    result=Submission(inst.name,[alternate[j] if index[j] in chosen else original[j] for j in ids]);checked=check(inst,result)
    assert checked.legal and checked.total_delay==a.total_delay+certificate['minimum_delta']
    assert checked.total_delay<=min(a.total_delay,b.total_delay)
    return result,{'base_delay':a.total_delay,'donor_delay':b.total_delay,'total_delay':checked.total_delay,'selected_donor_nets':[ids[k] for k in sorted(chosen)],'dependency_arcs':len(dependencies),'certificate':certificate}

def ancestor_costs(directory):
    """Deduplicate recorded optimizer stages,including an inherited portfolio."""
    costs={};missing=set();visited=set()
    m=json.loads((directory/'manifest.json').read_text())
    while True:
        if m['run_id'] in visited:raise ValueError("cyclic optimizer ancestry")
        visited.add(m['run_id']);costs[m['run_id']]=m['wrapper_wall_s']
        origin=Path(m['warm_start']['directory']);parent=origin.parent/'manifest.json'
        if not parent.exists():
            inherited=origin.parent/'portfolio.json'
            if inherited.exists():
                p=json.loads(inherited.read_text());costs.update(p.get('known_ancestry_runs',{}));missing.update(p.get('missing_ancestor_artifacts',[]))
            if not origin.exists():missing.add(str(origin))
            break
        m=json.loads(parent.read_text())
    return costs,missing

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('base',type=Path);p.add_argument('donor',type=Path);p.add_argument('--suite',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    if a.out.exists():p.error('report exists')
    start=time.perf_counter();runs=[a.base.resolve(),a.donor.resolve()];manifests=[json.loads((r/'manifest.json').read_text()) for r in runs]
    assert all(m['success'] and m['result']['complete'] and m['config']['suite']==a.suite for m in manifests)
    out=ROOT/'dev/artifacts'/(datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')+'-net-recombination');(out/'routes').mkdir(parents=True)
    report={'upstream_revision':REVISION,'suite':a.suite,'artifact_directory':str(out),'portfolio_selection':True,'method':'Exact two-parent per-net tree closure/mincut','sources':[{'directory':str(r),'manifest_sha256':digest(r/'manifest.json')} for r in runs],'cases':[],'limitations':'Exact restricted candidate-set recombination,not global routing optimality. All inherited generation and missing ancestry limitations retained.'}
    inventory=json.loads((OFFICIAL/a.suite/'suite.json').read_text());scores=[];inputs={}
    for c in inventory['cases']:
        case=OFFICIAL/a.suite/c['instance_file'];inputs[str(case)]=digest(case);inst=Instance.load(case);name='routes/'+c['name']+'.sol.json';subs=[]
        for r,m in zip(runs,manifests):assert digest(r/name)==m['outputs'][name];subs.append(Submission.load(r/name))
        sub,row=recombine(inst,*subs);target=out/name;sub.save(target);scores.append(score_case(inst,sub,c['baseline_total']))
        report['cases'].append({'case':c['name'],'case_sha256':digest(case),'output_sha256':digest(target),**row})
    assert all(digest(Path(path))==sha for path,sha in inputs.items())
    costs={};missing=set()
    for r in runs:
        known,unavailable=ancestor_costs(r)
        for name,value in known.items():
            if name in costs:assert costs[name]==value
            costs[name]=value
        missing.update(unavailable)
    report.update(score=leaderboard(scores).to_dict(),known_ancestry_wrapper_wall_s=sum(costs.values()),known_ancestry_runs=costs,missing_ancestor_artifacts=sorted(missing),selection_wall_s=time.perf_counter()-start,source_sha256=digest(Path(__file__)))
    report['official_rescore_process']=execute([str(ROOT/'.venv/bin/python'),'-m','m3d.cli','score-suite','--suite',a.suite,'--submission-dir',str(out/'routes'),'--out',str(out/'official-rescore.json')],out,'official-rescore',180)
    assert report['official_rescore_process']['exit_code']==0;official=json.loads((out/'official-rescore.json').read_text());assert official['complete'] and official['aggregate_score']==report['score']['aggregate_score']
    save(out/'portfolio.json',report);save(a.out,report);print('recombined',report['score']['aggregate_score'],out)
if __name__=='__main__':main()
