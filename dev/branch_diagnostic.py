"""Measure exact one-edge subtree exchanges inside existing legal net vertices."""
import argparse,json
from pathlib import Path
from collections import Counter,defaultdict
from measure import ROOT,OFFICIAL,digest,save
from run_polish import Instance,Submission,check

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--coverage',type=Path,required=True)
    p.add_argument('--tier',default='hard')
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();assert not a.out.exists()
    coverage=json.loads(a.coverage.read_text())
    stage=next(r for r in coverage['rows'] if r['tier']==a.tier)
    suite=stage['config']['suite'];inventory=json.loads((OFFICIAL/suite/'suite.json').read_text())
    rows=[]
    for item in inventory['cases']:
        case=OFFICIAL/suite/item['instance_file'];inst=Instance.load(case)
        route=ROOT/'dev/artifacts'/stage['run_id']/'routes'/(item['name']+'.sol.json')
        sub=Submission.load(route);assert check(inst,sub).legal
        pins={p.id:p.vertex() for p in inst.pins};nets={n.id:n for n in inst.nets}
        best=[];flow_histogram=Counter();branches=0
        for r in sub.routes:
            n=nets[r.net];root=pins[n.driver];adj=defaultdict(list)
            for u,v in r.edges:adj[u].append(v);adj[v].append(u)
            parent={root:root};distance={root:0};order=[root]
            for u in order:
                for v in adj[u]:
                    if v not in parent:
                        parent[v]=u;distance[v]=distance[u]+inst.edge_delay(u,v);order.append(v)
            counts=Counter(pins[s] for s in n.sinks)
            size={v:1 for v in order}
            for v in reversed(order[1:]):counts[parent[v]]+=counts[v];size[parent[v]]+=size[v]
            # DFS intervals make an ancestor check constant time.
            tin={};tout={};stack=[(root,False)];clock=0
            while stack:
                u,exit_node=stack.pop()
                if exit_node:tout[u]=clock;continue
                tin[u]=clock;clock+=1;stack.append((u,True))
                stack.extend((v,False) for v in adj[u] if parent.get(v)==u and v!=u)
            winner=None
            for v in order[1:]:
                branches+=1;flow_histogram[str(counts[v])]+=1
                x,y,z=v
                for u in [(x+1,y,z),(x-1,y,z),(x,y+1,z),(x,y-1,z),(x,y,z+1),(x,y,z-1)]:
                    if u not in parent or u==parent[v] or tin[v]<=tin[u]<tout[v]:continue
                    gain=counts[v]*(distance[v]-distance[u]-inst.edge_delay(u,v))
                    if gain>0 and (winner is None or gain>winner['gain']):
                        winner={'net':n.id,'gain':gain,'downstream_sinks':counts[v],'subtree_vertices':size[v],'remove':[parent[v],v],'add':[u,v]}
            if winner:
                # Validate each net's best move in isolation in the entire solution.
                changed=Submission.from_dict(sub.to_dict())
                target=next(q for q in changed.routes if q.net==n.id)
                old={tuple(winner['remove'][0]),tuple(winner['remove'][1])}
                target.edges=[e for e in target.edges if set(e)!=old]+[(tuple(winner['add'][0]),tuple(winner['add'][1]))]
                result=check(inst,changed);original=check(inst,sub)
                assert result.legal and original.total_delay-result.total_delay==winner['gain']
                best.append(winner)
        rows.append({'case':item['name'],'case_sha256':digest(case),'route_sha256':digest(route),'cut_edges':branches,'downstream_sink_histogram':dict(flow_histogram),'individually_verified_moves':best})
    save(a.out,{'tier':a.tier,'run_id':stage['run_id'],'coverage_sha256':digest(a.coverage),'source_sha256':digest(Path(__file__)),'rows':rows,'scope':'Read-only diagnostic. Each positive move independently officially validated. Moves across nets use unchanged own vertex sets; no competitor inputs. Restriction: one adjacent existing-tree attachment edge, not general branch rerouting or global optimality.'})

if __name__=='__main__':main()
