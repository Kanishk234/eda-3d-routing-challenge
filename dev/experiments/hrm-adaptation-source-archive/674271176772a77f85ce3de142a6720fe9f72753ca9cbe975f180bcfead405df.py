"""Pretrained HRM color predictions guide secondary tree geometry on real cases.

Whole-net windows only in this first adaptation. No layer collapse or training.
Classical search builds trees; finite-pool selection and official checks accept.
"""
import argparse
import heapq
import json
import time
from pathlib import Path
from branch_repair import Router, Limit
from hrm_cpu_probe import load_cpu
from measure import ROOT, OFFICIAL, digest, save
from run_polish import Instance, Submission, NetRoute, check
from select_tree_pool import solve_pool


def window(router, ids):
    pins = [router.pins[p] for nid in ids for p in router.nets[nid].pins()]
    lo = tuple(min(v[k] for v in pins) for k in range(3))
    hi = tuple(max(v[k] for v in pins) for k in range(3))
    if any(hi[k] - lo[k] >= size for k, size in enumerate((16, 16, 4))):
        return None
    return tuple(max(0, lo[k] - (size - (hi[k] - lo[k] + 1)) // 2)
                 for k, size in enumerate((16, 16, 4)))


def encode(router, ids, origin):
    import torch
    assert 1 <= len(ids) <= 4 and len(set(ids)) == len(ids)
    grid = torch.full((16, 4, 16), 2, dtype=torch.long)
    for y in range(16):
        for z in range(4):
            for x in range(16):
                v = (x + origin[0], y + origin[1], z + origin[2])
                if (router.inst.in_bounds(v) and router.owner.get(v) in [None, *ids]
                        and router.pin_owner.get(v) in [None, *ids]):
                    grid[y, z, x] = 1
    for i, nid in enumerate(ids):
        for pin in router.nets[nid].pins():
            v = router.pins[pin]
            x, y, z = (v[k] - origin[k] for k in range(3))
            assert 0 <= x < 16 and 0 <= y < 16 and 0 <= z < 4
            grid[y, z, x] = 3 + i
    return grid


def guided_tree(router, nid, preferred, group, penalty):
    root = router.pins[router.nets[nid].driver]
    todo = {router.pins[s] for s in router.nets[nid].sinks}
    dist = {root: (0, 0)}; parent = {}; queue = [(0, 0, root)]
    while queue and todo:
        cost, tie, u = heapq.heappop(queue)
        if (cost, tie) != dist[u]: continue
        if router.expansions >= router.work or time.monotonic() >= router.deadline: raise Limit
        router.expansions += 1; todo.discard(u)
        for v, weight in router.neighbors(u):
            if router.pin_owner.get(v, nid) != nid: continue
            owner = router.owner.get(v)
            if owner is not None and owner != nid and owner not in group: continue
            toll = penalty if owner is not None and owner != nid else 0
            candidate = (cost + 16 * weight + toll, tie + int(v not in preferred))
            if candidate < dist.get(v, (10**30, 10**30)):
                dist[v] = candidate; parent[v] = u; heapq.heappush(queue, (*candidate, v))
    if todo: return None
    used = {root}; edges = set()
    for sink in sorted({router.pins[s] for s in router.nets[nid].sinks}):
        u = sink
        while u not in used:
            used.add(u); v = parent[u]; edges.add(tuple(sorted((u, v)))); u = v
    return NetRoute(nid, sorted(edges))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--coverage', type=Path, required=True)
    p.add_argument('--model-dir', type=Path, default=Path('dev/artifacts/hrm-pretrained'))
    p.add_argument('--cases', nargs='+', default=['case_01', 'case_04', 'case_07'])
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args(); assert not a.out.exists(); a.out.mkdir(parents=True)
    import torch
    model, config, manifest = load_cpu(a.model_dir, 2)
    frozen = {str(p.resolve()): digest(p) for p in [Path(__file__), ROOT/'dev/hrm_cpu_probe.py', a.coverage]}
    stage = next(r for r in json.loads(a.coverage.read_text())['rows'] if r['tier'] == 'hard')
    suite = stage['config']['suite']; inventory = json.loads((OFFICIAL/suite/'suite.json').read_text())
    assert set(a.cases) <= {c['name'] for c in inventory['cases']}
    report = dict(status='running', source_sha256=frozen, model_manifest=manifest,
                  scope='First whole-net-window pretrained transfer; physical costs primary, predictions secondary. No training. Matched classical control, extra inference cost reported. Restricted finite-pool selection only.', rows=[])
    save(a.out/'progress.json', report)
    for case in inventory['cases']:
        if case['name'] not in a.cases: continue
        path = OFFICIAL/suite/case['instance_file']
        source = ROOT/'dev/artifacts'/stage['run_id']/'routes'/(case['name']+'.sol.json')
        inst = Instance.load(path); sub = Submission.load(source); before = check(inst, sub); assert before.legal
        router = Router(inst, sub, 3000000, 300, 1)
        eligible = [nid for nid in sorted(router.nets) if window(router, [nid]) is not None]
        groups = []; remaining = list(eligible)
        while remaining and len(groups) < 2:
            ids = [remaining.pop(0)]
            for nid in remaining[:]:
                if len(ids) == 4: break
                if window(router, ids + [nid]) is not None:
                    ids.append(nid); remaining.remove(nid)
            groups.append((ids, window(router, ids)))
        predictions = []; inference_s = 0
        for ids, origin in groups:
            grid = encode(router, ids, origin)
            batch = {'inputs': grid.reshape(1, 1024), 'puzzle_identifiers': torch.zeros(1, dtype=torch.long)}
            start = time.monotonic(); carry = model.initial_carry(batch)
            with torch.inference_mode():
                for _ in range(config['halt_max_steps']): carry, output = model(carry, batch)
                assert torch.isfinite(output['logits']).all()
                pred = output['logits'].argmax(-1)[0].reshape(16, 4, 16)
            inference_s += time.monotonic() - start
            preferred = {}
            for i, nid in enumerate(ids):
                preferred[nid] = {(int(x)+origin[0], int(y)+origin[1], int(z)+origin[2])
                                  for y, z, x in (pred == 3+i).nonzero().tolist()}
            predictions.append((ids, preferred))
        outcomes = []
        for method in ['control', 'hrm']:
            r = Router(inst, sub, 3000000, 60, 1)
            pool = {nid: [] for nid in r.nets}; seen = {nid: set() for nid in r.nets}
            def add(tree):
                if tree is None: return
                key = tuple(sorted(tree.edges)); nid = tree.net
                if key in seen[nid]: return
                checked = check(inst, Submission(inst.name, [tree]))
                nr = next(x for x in checked.nets if x.net == nid); assert nr.legal
                seen[nid].add(key); pool[nid].append((tree, nr.delay, r.vertices(tree)))
            for tree in sub.routes: add(tree)
            limited = False
            try:
                for ids, preferred in predictions:
                    for nid in ids:
                        for toll in [0, 2, 8]: add(guided_tree(r, nid, preferred[nid] if method == 'hrm' else set(), ids, toll))
            except Limit: limited = True
            ids = sorted(pool)
            chosen, stats = solve_pool([[t[1] for t in pool[i]] for i in ids], [[t[2] for t in pool[i]] for i in ids], [0]*len(ids), 10, 1)
            out = Submission(inst.name, [pool[nid][chosen[k]][0] for k, nid in enumerate(ids)])
            after = check(inst, out); assert after.legal and after.total_delay <= before.total_delay
            target = a.out/(case['name']+'-'+method+'.sol.json'); out.save(str(target))
            assert check(inst, Submission.load(target)).total_delay == after.total_delay
            outcomes.append(dict(method=method, delay=after.total_delay, legal=True, expansions=r.expansions,
                                 limited=limited, output_sha256=digest(target), selection=stats))
        report['rows'].append(dict(case=case['name'], case_sha256=digest(path), parent_sha256=digest(source),
                                  before_delay=before.total_delay, eligible_nets=len(eligible), groups=[g[0] for g in groups],
                                  inference_wall_s=inference_s, outcomes=outcomes))
        save(a.out/'progress.json', report); print(case['name'], outcomes, flush=True)
    assert all(digest(Path(p)) == sha for p, sha in frozen.items())
    report['status'] = 'complete'; save(a.out/'progress.json', report)


if __name__ == '__main__': main()
