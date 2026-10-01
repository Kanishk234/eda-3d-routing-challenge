# Experiment protocol

Environment in VERSIONS.md and dated evidence/phase0/environment.json: 16 WSL schedulable CPUs; RAM 16,435,576,832 bytes (~15.3 GiB). Available RAM varies. cgroup cpu.max/memory.max files unavailable; separate quotas unknown. No GPU assumed. Start one serial worker; measure memory before increasing concurrency.

Budgets/reservations in OVERVIEW.md. Tests capped 180 seconds, smoke/CI 60 seconds per subprocess; one intentional 0.001-second timeout. No suite/optimization launched. Process time includes startup/serialization/check overhead; CLI internal rounded time is separate. GNU time captures user/system CPU and peak RSS; timeout run RSS unknown because termination prevented recording.

Manifest fields: source HEAD/status/binary-diff SHA256/source-file hashes, official revision/input hashes, commands/cwd/config, case seed/hash for smoke, worker/thread counts, start/budget/wall/CPU/RSS, legality/delay, output hashes, provenance. Python compiler flags null; compiled runs must add build identity/flags. Compact Phase 0 evidence in runs.json; full hash dictionaries/raw logs in ignored run directories. No warm starts, portfolio selection or multi-run best-of result used.

Observed results reproduce one small case only: legal 240, ratio 1.0, two matching outputs. No tier aggregate or algorithm-speed claim. Two runtimes vary and research-container timings are not matched laptop comparisons.

Phase 1 onward: freeze inputs/config, finalize small/large representatives without tuning reserved validation cases, compare under matched hardware/budgets, report every case/failure, seeds and total restart/portfolio cost. Use official geometric mean only for complete tiers. Keep physical delay distinct from wirelength/occupancy/congestion. Label public warm starts separately.

Wrapper offers bounded run-suite/score-suite and optional official per-case runtime.json; stage profiles, expansion counters and custom solver measurement remain unimplemented Phase 1/2 work. Avoid stress baseline without a separate explicit bounded plan.

## Phase 2 update

Phases1/2 are complete; earlier “unperformed” statements describe Phase0 only. Authoritative current evidence: docs/evidence/phase2/comparison.json and runs.json; PHASE2 summary covers checks, deterministic outputs, budgets, baseline provenance and limits.13 kernel checks pass and official CLI rescore confirms9/9 legal, aggregate1.046629. Baseline-plus-wrapper sum97.952s is a paired same-machine comparison within600s, not a fresh end-to-end timing or speedup. Generated validation seeds and final submission checks remain unperformed.

Budget expansion October1:2s/case was a local matched screen,not official limit or final budget. Six serial representative runs(cases01/04/07,seed1,100-cycle ceiling) compared2vs10s from identical plateau starts;longer budgets improved every case. Full-tier fixed10s/100-cycle wide validation launched after development selection. Per-stage search and total portfolio/screen costs remain separate;no two-second ceiling is assumed.

## Broad-tier optimization plan

All-tier initial coverage had unequal search effort:hard inherited427.357s of generation/stages;other tiers had only a single exact polish stage(2s/case,stress60s) after attributed baseline warm starts. Cross-tier ratios normalize different baselines and do not measure equal difficulty. Profile scale08/designs-router/stress with read,initial validation,and optimization timers before changing hot code.

Stress matched performance comparison starts both60s runs from225241/routes,seed1,5passes. Dense initial validation measured43.950s;replace whole-grid per-net adjacency/cost storage with tree-local storage,retain physical/legality checks. Subsequent representative screen declares scale01,congested01,designs-ctrl,seed1,5s/100passes for fanout versus fanout_walk. Use one fixed chosen mode for full-tier validation;no per-case seed/config selection. Timings remain serial,one worker;failedshort profiles remain separate.

## Guided-search comparison

Relaxed analytic distance bounds cover all45 released cases,ignoring ownership and foreign pins;optimistic ceilings are not achievable targets without jointly legal construction. Matched stress A* versus ordinarypolish uses same225241/routes,seed1/5passes/60s whole-core cap. Three-method screen declares hard01/congested01/designs-ctrl,seed1/5s/100passes from tier-optimized-coverage.json starts. A* beats ordinaryfanout3/3;gap-order beats ordinary3/3 and A*2/3,but loses congested representative. Select fixed fanout_astar for fullhard/congested/designs validation from those original starts. No per-case selected artifacts,nohard08/09 tuning. Further seeds/budget curves remain next work;single-seed comparisons do not prove general superiority.
