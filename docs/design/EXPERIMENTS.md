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

## Repeated seeds,budget scaling,and guarded fresh starts

`dev/guided_screen.py repeat|budget|fresh|treecost` freezes starts to tier-guided-coverage.json,representatives hard01/congested01/designsctrl,serialoneworker,explicitmode/seed/cap/pass configs and per-run provenance.18repeated trials seed2/3,6budget trials seed1,3fresh trials,3treecost trials;none selects per-casebest. Fullstages choose fixedseed1/20s/100cycles fanout_astar forcongested/designs,then fixedcongested restart_astar20s/max5starts with3single-netpolishpasses. Screen/generation/finalstage costs remain separate. No newunitchecks implied by benchmark verification.

## Deterministic expanded-vertex budgets

`dev/run_polish.py --work-budget N` caps cumulative popped non-stale search vertices across shortest/attach calls; zero disables this cap. Wall budget includes initialization and remains a safety cap. Engine accepts optional fifth positional value after MODE, preserving existing calls. Work exhaustion rolls back an unfinished search/group and retains the legal incumbent; a search reaching the cap exactly may be discarded before reconstruction. `work_exhausted` distinguishes this condition in stderr diagnostics; legacy stdout timeout bit means any termination budget exhausted. Determinism applies when the work cap wins before wall time or interruption and inputs/config/compiled implementation match. Expansion count is a reproducibility unit, not equal CPU cost across algorithms.

Stress fixed10M expansions/seed1/100passes from230938 routes:30s and45s safety caps produce identical C++ stdout and route bytes, legal delay1121978. Use uncontended234215 for timings;234147 briefly overlapped focused tests. Reset/rebuild timers currently cover shortest only. Both repeated runs, source/binary hashes and limitations are in work-budget-profile.json. All selected tiers independently rescored in tier-work-budget-coverage.json.
