"""Pretrained local branch proposals with connected outside trees preserved.

Each branch has one fixed attachment and all downstream sinks. Neural hints
never replace physical scoring or ownership checks. No new training.
"""
import argparse
import copy
import json
import time
from pathlib import Path
from types import SimpleNamespace
from branch_repair import Router, Limit
from hrm_cpu_probe import load_cpu
from hrm_local_proposals import encode, guided_tree
from measure import ROOT, OFFICIAL, digest, save
from run_polish import Instance, Submission, NetRoute, check
from select_tree_pool import solve_pool


def box(points):
    lo = tuple(min(v[k] for v in points) for k in range(3))
    hi = tuple(max(v[k] for v in points) for k in range(3))
    if any(hi[k]-lo[k] >= size for k, size in enumerate((16, 16, 4))): return None
    return tuple(max(0, lo[k]-(size-(hi[k]-lo[k]+1))//2)
                 for k, size in enumerate((16, 16, 4)))


def branches(router):
    result = []
    for nid in sorted(router.nets):
        parent, dist, order = router.tree(router.routes[nid])
        descendants = {v: {v} for v in order}
        for v in reversed(order[1:]): descendants[parent[v]].update(descendants[v])
        sink_vertices = {router.pins[s] for s in router.nets[nid].sinks}
        best = None
        for cut in order[1:]:
            removed = descendants[cut]; sinks = sorted(sink_vertices & removed)
            if not sinks: continue
            attachment = parent[cut]; points = removed | {attachment}
            if box(points) is None: continue
            gap = 0
            for sink in sinks:
                xy = abs(attachment[0]-sink[0])+abs(attachment[1]-sink[1])
                lower = min(xy*d+router.inst.via_delay*(abs(attachment[2]-z)+abs(sink[2]-z))
                            for z, d in enumerate(router.inst.layer_delay))
                gap += dist[sink]-dist[attachment]-lower
            retained = NetRoute(nid, [e for e in router.routes[nid].edges if not any(v in removed for v in e)])
            entry = dict(nid=nid, attachment=attachment, removed=removed, sinks=sinks,
                         points=points, gap=gap, retained=retained)
            # More exposed geometry is useful even at zero individual gap.
            rank = (gap, len(removed), tuple(attachment), tuple(cut))
            if best is None or rank > best[0]: best = (rank, entry)
        if best: result.append(best[1])
    return sorted(result, key=lambda b: (-b['gap'], -len(b['removed']), b['nid']))


def branch_router(original, group, origin, work=3000000, seconds=60):
    r = copy.copy(original)
    r.owner = dict(original.owner); r.pin_owner = dict(original.pin_owner)
    r.pins = dict(original.pins); r.nets = dict(original.nets)
    r.expansions = 0; r.work = work; r.deadline = time.monotonic()+seconds
    removed = {v for b in group for v in b['removed']}
    # All retained geometry, including same-net geometry, is fixed.
    for v in r.owner:
        if v not in removed: r.owner[v] = -1000000
    for b in group:
        nid = b['nid']; driver = ('attachment', nid)
        sinks = [('sink', nid, i) for i in range(len(b['sinks']))]
        r.pins[driver] = b['attachment']
        for key, v in zip(sinks, b['sinks']): r.pins[key] = v
        keys = [driver, *sinks]
        r.nets[nid] = SimpleNamespace(driver=driver, sinks=sinks, pins=lambda keys=keys: keys)
        r.owner[b['attachment']] = nid; r.pin_owner[b['attachment']] = nid
    neighbors = original.neighbors
    def local_neighbors(v):
        for u, delay in neighbors(v):
            if all(origin[k] <= u[k] < origin[k]+size for k, size in enumerate((16,16,4))):
                yield u, delay
    r.neighbors = local_neighbors
    return r


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--coverage', type=Path, required=True)
    p.add_argument('--model-dir', type=Path, default=Path('dev/artifacts/hrm-pretrained'))
    p.add_argument('--cases', nargs='+', default=['case_01','case_04','case_07'])
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args(); assert not a.out.exists(); a.out.mkdir(parents=True)
    import torch
    model, config, manifest = load_cpu(a.model_dir, 2)
    sources = [Path(__file__), ROOT/'dev/hrm_cpu_probe.py', ROOT/'dev/hrm_local_proposals.py',
               ROOT/'dev/branch_repair.py', ROOT/'dev/select_tree_pool.py', a.coverage]
    frozen = {str(p.resolve()): digest(p) for p in sources}
    for p in sources[:-1]: (a.out/p.name).write_bytes(p.read_bytes())
    stage = next(r for r in json.loads(a.coverage.read_text())['rows'] if r['tier']=='hard')
    suite = stage['config']['suite']; inventory = json.loads((OFFICIAL/suite/'suite.json').read_text())
    assert set(a.cases) <= {c['name'] for c in inventory['cases']}
    report = dict(status='running', frozen_sha256=frozen, model_manifest=manifest, rows=[],
                  scope='Own connected-subtree branch windows,pretrained HRM hints;outside geometry fixed. No training. Restricted candidate-pool exact selection,not globally exact. Extra inference cost disclosed.')
    save(a.out/'progress.json', report)
    for case in inventory['cases']:
        if case['name'] not in a.cases: continue
        path = OFFICIAL/suite/case['instance_file']; inst = Instance.load(path)
        source = ROOT/'dev/artifacts'/stage['run_id']/'routes'/(case['name']+'.sol.json')
        sub = Submission.load(source); before = check(inst, sub); assert before.legal
        original = Router(inst, sub, 3000000, 300, 1)
        candidates = branches(original); groups = []; remaining = candidates[:]
        while remaining and len(groups)<2:
            group = [remaining.pop(0)]
            for b in remaining[:]:
                if len(group)==4: break
                if box(set().union(*(x['points'] for x in group), b['points'])) is not None:
                    group.append(b); remaining.remove(b)
            groups.append((group, box(set().union(*(b['points'] for b in group)))))
        prepared = []; inference_s = 0
        for group, origin in groups:
            r = branch_router(original, group, origin); ids = [b['nid'] for b in group]
            grid = encode(r, ids, origin)
            batch = {'inputs': grid.reshape(1,1024), 'puzzle_identifiers': torch.zeros(1,dtype=torch.long)}
            start=time.monotonic(); carry=model.initial_carry(batch)
            with torch.inference_mode():
                for _ in range(config['halt_max_steps']): carry, output=model(carry,batch)
                assert torch.isfinite(output['logits']).all()
                pred=output['logits'].argmax(-1)[0].reshape(16,4,16)
            inference_s += time.monotonic()-start
            preferred = {nid: {(int(x)+origin[0],int(y)+origin[1],int(z)+origin[2])
                              for y,z,x in (pred==3+i).nonzero().tolist()} for i,nid in enumerate(ids)}
            prepared.append((group,origin,preferred))
        outcomes=[]
        for method in ['control','hrm_tie','hrm_priced']:
            pool={nid:[] for nid in original.nets};seen={nid:set() for nid in original.nets}
            def add(tree):
                key=tuple(sorted(tree.edges));nid=tree.net
                if key in seen[nid]: return
                nr=next(x for x in check(inst,Submission(inst.name,[tree])).nets if x.net==nid)
                assert nr.legal;seen[nid].add(key);pool[nid].append((tree,nr.delay,original.vertices(tree)))
            for tree in sub.routes: add(tree)
            expansions=0;limited=False;search_begin=time.monotonic()
            for group,origin,preferred in prepared:
                r=branch_router(original,group,origin,work=max(1,3000000-expansions));ids=[b['nid'] for b in group]
                try:
                    for b in group:
                        nid=b['nid']
                        for toll in [0,2,8]:
                            tree=guided_tree(r,nid,preferred[nid] if method!='control' else set(),ids,toll,2 if method=='hrm_priced' else 0)
                            if tree: add(NetRoute(nid,sorted({tuple(sorted(e)) for e in [*b['retained'].edges,*tree.edges]})))
                except Limit: limited=True
                expansions+=r.expansions
                if limited: break
            ids=sorted(pool)
            chosen,stats=solve_pool([[t[1] for t in pool[i]] for i in ids],[[t[2] for t in pool[i]] for i in ids],[0]*len(ids),10,1)
            out=Submission(inst.name,[pool[nid][chosen[k]][0] for k,nid in enumerate(ids)])
            after=check(inst,out);assert after.legal and after.total_delay<=before.total_delay
            target=a.out/(case['name']+'-'+method+'.sol.json');out.save(str(target))
            assert check(inst,Submission.load(target)).total_delay==after.total_delay
            outcomes.append(dict(method=method,delay=after.total_delay,legal=True,expansions=expansions,
                                 limited=limited,search_and_selection_wall_s=time.monotonic()-search_begin,
                                 output_sha256=digest(target),selection=stats))
        report['rows'].append(dict(case=case['name'],case_sha256=digest(path),parent_sha256=digest(source),
                                  before_delay=before.total_delay,eligible_branches=len(candidates),
                                  groups=[[dict(nid=b['nid'],gap=b['gap'],removed=len(b['removed']),sinks=len(b['sinks'])) for b in g] for g,_ in groups],
                                  inference_wall_s=inference_s,outcomes=outcomes))
        save(a.out/'progress.json',report);print(case['name'],outcomes,flush=True)
    assert all(digest(Path(p))==sha for p,sha in frozen.items())
    report['status']='complete';save(a.out/'progress.json',report)


if __name__=='__main__':main()
