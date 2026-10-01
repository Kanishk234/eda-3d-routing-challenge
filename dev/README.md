# CPU development workspace

Run in WSL Ubuntu at /home/younix/eda-3d-routing-challenge. This fork is the development checkout; never submit it wholesale. Origin points to Kanishk234's fork. No branch, commit, push or publication performed.

## Setup and build

```bash
bash dev/setup.sh
g++ -O3 -std=c++17 -Wall -Wextra -Wpedantic dev/toolchain_probe.cpp -o dev/artifacts/toolchain_probe
dev/artifacts/toolchain_probe
```

Setup creates project .venv, installs an empty stdlib-only dependency file with networking disabled, and archives upstream 499ad7e2a415a97e9ce9b3396b0477e75ebd13e6 into dev/upstream/499ad7e2a415a97e9ce9b3396b0477e75ebd13e6. This commit is already present; fetch official upstream first if a fresh clone lacks it. Do not silently update the pin. Python 3.12.3 and GCC 13.3.0 were tested. CMake and optional visualization dependencies are unnecessary. The probe checks the compiler; the exact polisher is now implemented; commands below.

## Bounded commands

```bash
.venv/bin/python dev/measure.py tests --budget 180
.venv/bin/python dev/measure.py smoke --suite benchmarks --case case_01 --budget 60
.venv/bin/python dev/measure.py ci --budget 60
# Phase 1 commands; not run in Phase 0:
.venv/bin/python dev/measure.py suite --suite benchmarks --router baseline --budget 180
.venv/bin/python dev/measure.py suite --suite benchmarks_hard --router negotiated --budget 600
```

Budget applies to each subprocess: suites have a routing cap and separate scoring cap, so maximum total can be twice the budget plus 5 seconds termination grace per step. Tests have one step; CI has two. Maximum permitted cap is 1,800 seconds. All runs are serial, one worker/thread, PYTHONHASHSEED=0 and OMP_NUM_THREADS=1. Declare the next-session run plan before the hard suite. Simple-baseline failure is not hard-tier infeasibility.

Unique ignored dev/artifacts/<UTC-run-id>/ directories hold manifests, logs, resource records and routes. Official tools execute inside the pinned archive. Manifests retain revision/dirty identity, source/input/output hashes, config/commands, machine, workers, budgets, wall/CPU time, RSS and results. Smoke candidates are renamed to accepted case files only after official evaluate succeeds. Suite routes remain isolated until the full official score is reviewed. runtime.json records official per-case routing times; process measurements include startup/check/serialization.

## Validate and recover

Use the absolute output path printed by measure.py:

```bash
cd dev/upstream/499ad7e2a415a97e9ce9b3396b0477e75ebd13e6
../../../.venv/bin/python -m m3d.cli evaluate --case benchmarks/case_01.json --sol /ABSOLUTE/RUN/case_01.sol.json --suite benchmarks
../../../.venv/bin/python -m m3d.cli score-suite --suite benchmarks_hard --submission-dir /ABSOLUTE/ROUTES --out /ABSOLUTE/RUN/rescore.json
```

Timeout/Ctrl-C terminates the child process group and preserves logs/manifests and earlier accepted runs. Resume Phase 0/1 with a new bounded run and the last validated output as a reference. Exact polish recovery uses --resume-dir as documented below.

capture_environment.py writes dated environment/inventory/GitHub snapshots into docs/evidence/phase0/. finish_phase0.py is a one-time audit expecting exactly the original five runs (two successful smokes and one timeout); adapt its run selection before rerunning after further experiments. Compact evidence is tracked; snapshots, binaries, routes and raw logs are ignored and must be retained/backed up separately.

## Submission isolation

Phase 5 needs a separate clean checkout based on then-current official upstream. Only submissions/<tier>/<method>/** and generated LEADERBOARD.md enter the submission diff. Never include dev/, development docs/, ignore changes or AGENTS.md. No submission checkout/method entry exists yet.

## Phase 2 build, run and resume

```bash
g++ -O3 -std=c++17 -Wall -Wextra -Wpedantic dev/solver/exact_polish.cpp -o dev/artifacts/build/exact_polish
.venv/bin/python dev/test_exact.py > dev/artifacts/build/kernel-tests.log 2>&1
.venv/bin/python dev/run_polish.py --budget 10 --seed 1 --passes 5
.venv/bin/python dev/run_polish.py --case case_01 --budget 0
.venv/bin/python dev/run_polish.py --case case_01 --resume-dir /ABSOLUTE/PREVIOUS/RUN/routes
.venv/bin/python dev/finish_phase2.py
```

Baseline incumbents must first exist from Phase1 reproduction/finish_phase1.py. Fresh baseline generation cost is part of the pipeline. Budgets are per-case core caps; input processing/validation/wrapper overhead and up to5s watchdog grace are additional. Defaults10s,seed1,5passes,one worker. Core signal handling emits completed incumbent; abrupt failure preserves pre-search checkpoint. No coordinated repair yet. Phase2 evidence freezer expects all stored runs successful and repeat full-tier hashes equal; adapt run selection before future optimization, rather than applying it to different configs.

## Phase 3 experimental screen

```bash
.venv/bin/python dev/run_polish.py --mode repair --case case_01 --budget 2 --seed 1 --passes 5 --resume-dir dev/artifacts/20261001T212816.474321Z-exact-polish/routes
.venv/bin/python dev/phase3_screen.py
```

Screen runs only hard01–07, seeds1–3, serially; preserves every manifest and makes no best-of selection. Initial repair operator showed no gain and is experimental. finish_phase2.py is a historical freezer and must not be run on mixed Phase3 manifests/configurations.

Occupied-vertex penalty variant (retained, fixed config):

```bash
.venv/bin/python dev/phase3_screen.py --mode repairsoft --label repair-soft-screen
.venv/bin/python dev/run_polish.py --mode repairsoft --budget 2 --passes 5 --seed 1 --resume-dir dev/artifacts/20261001T212816.474321Z-exact-polish/routes
.venv/bin/python dev/finish_phase3_screen.py
```

`repairsoft` uses proposal penalty4 per foreign occupied vertex and max4 blockers. All accepted groups use official physical delay; exact search mode/polish remain physical-cost searches. Diagnostics in stderr are captured in manifests. Screen labels preserve prior comparisons.

Driver-distance ablation (candidate outputs remain unchanged):

```bash
.venv/bin/python dev/phase3_screen.py --mode ablation --label attachment-ablation
```

Reconstructs each net independently with other nets fixed. Compare exact costs to driver-aware/zero-source attachment. Reported sums are not jointly routable scores. Submission paths were rechecked at current upstream3d8948f; development sources remain here and final routes/metadata go in a clean submission checkout.

Negotiated comparison and public-output audit tools:

```bash
.venv/bin/python dev/phase3_screen.py --mode negotiated --label negotiated-screen
.venv/bin/python dev/finish_phase3_screen.py --mode negotiated
.venv/bin/python dev/audit_public_hard.py
```

Public audit downloads routes solely for comparison,including closed PR heads. It does not execute public solvers or promote public outputs. Network required;results pinned by head/output hashes. Current negotiated validation starts from Phase2 warm routes under seed1,5passes,2s/case and max12 negotiation rounds.

Alternative initialization and geometry exploration:

```bash
.venv/bin/python dev/phase3_screen.py --mode explore --label plateau-screen
.venv/bin/python dev/phase3_screen.py --mode restart --label global-restart-screen
.venv/bin/python dev/run_polish.py --mode explore --budget 2 --passes 5 --seed 1 --resume-dir dev/artifacts/20261001T214526.246570Z-exact-polish/routes
.venv/bin/python dev/finish_phase3_screen.py --mode explore
```

Explore varies equal-cost queue ranks,accepts legal equal/lower-delay geometry,then negotiates groups. Restart rebuilds all nets from empty geometry,up to100 negotiation rounds/start,restores prior legal incumbent on failure/timeout/nonimprovement. Mode-specific search costs and pipeline warm-start cost are separate. Research source is ignored and never executed/copied;see OPTIMIZATION_FOLLOWUP.md.

Next operators(screened before full validation):

```bash
.venv/bin/python dev/phase3_screen.py --mode select --label candidate-selection-screen
.venv/bin/python dev/phase3_screen.py --mode wide --label wide-neighborhood-screen
```

Select is bounded branch-and-bound over original plus6 candidate variants,at most5 nets. Complete means optimal within generated candidate sets only. Wide uses equal-delay exploration,max12 blockers and24 negotiation rounds. Physical/legal acceptance and rollback remain unchanged.25 checks pass;candidate selector not default.

Budget scaling and selected wider-stage validation:

```bash
.venv/bin/python dev/budget_screen.py
.venv/bin/python dev/run_polish.py --mode wide --budget 10 --passes 100 --seed 1 --resume-dir dev/artifacts/20261001T215550.921679Z-exact-polish/routes
.venv/bin/python dev/finish_phase3_screen.py --mode wide
```

Two seconds is a screening cap only. This comparison keeps100-cycle ceiling/seed/warm start fixed on development cases01/04/07. The subsequent full-tier ten-second stage is selected from those measurements;actual cumulative generation and prior-stage costs remain part of the pipeline.

Controlled temporary worsening experiments:

```bash
.venv/bin/python dev/phase3_screen.py --mode walk --label threshold-walk-screen --budget 2 --passes 100 --cases 1,4,7 --resume-dir dev/artifacts/20261001T215550.921679Z-exact-polish/routes
.venv/bin/python dev/phase3_screen.py --mode descent --label threshold-descent-screen --budget 2 --passes 100 --cases 1,4,7 --resume-dir dev/artifacts/20261001T215550.921679Z-exact-polish/routes
.venv/bin/python dev/run_polish.py --mode walk --budget 2 --passes 100 --seed 1 --resume-dir dev/artifacts/20261001T220349.074348Z-exact-polish/routes
.venv/bin/python dev/finish_phase3_screen.py --mode walk
```

Walk temporarily accepts legal group worsening up to1% with probability1/4(and equal-delay moves),but returns the independently protected best snapshot. Descent differs only in this acceptance rule. Reports trace all warm-start component timings. Raw manifests/source snapshots/route hashes retained. Phase3 screen options only accept development01–07.

Resource-pricing comparisons:

```bash
.venv/bin/python dev/phase3_screen.py --mode compact --label compact-screen --budget 2 --passes 100 --cases 1,4,7 --resume-dir dev/artifacts/20261001T215550.921679Z-exact-polish/routes
.venv/bin/python dev/phase3_screen.py --mode fanout --label fanout-screen --budget 2 --passes 100 --cases 1,4,7 --resume-dir dev/artifacts/20261001T215550.921679Z-exact-polish/routes
.venv/bin/python dev/compare_resource_prices.py
.venv/bin/python dev/run_polish.py --mode fanout --budget 10 --passes 100 --seed 1 --resume-dir dev/artifacts/20261001T220917.515539Z-exact-polish/routes
.venv/bin/python dev/finish_phase3_screen.py --mode fanout
```

Compact group attachment uses3/4 driver-distance seeds,heuristic andnotretained asdefault. Fanout divides group history/present congestionprices byceil(sqrt(sinks)),physicaldelay unaffected. Retain onlyofficiallylegal/nongrowingdelay incumbents. Resource metrics countnetvertices once,edges andvias;not score surrogates.

## All-tier coverage

`run_polish.py --suite` accepts benchmarks, benchmarks_hard, benchmarks_scale, benchmarks_stress, benchmarks_congested, and benchmarks_designs. Supply `--resume-dir` with verified route files for each selected tier. Official `reference/` routes are permitted as explicitly attributed warm starts; their generation cost is not included in wrapper timing. Stress needs a separately declared larger cap than quick hard screens.

Rescore selected complete runs without best-of selection:

```bash
.venv/bin/python dev/report_tiers.py dev/artifacts/RUN_ID --out docs/evidence/phase3/tier-coverage.json
```

Each tier has its own score; no all-tier aggregate is reported. Coverage is preliminary until final solver/config freeze, regeneration, current-rules recheck, and clean route-only submission checks.

Guided search: `--mode astar` applies exact single-net polish with consistent physical lookahead; `fanout_astar` combines it with wide fanout-priced exploration. `fanout_gap` prioritizes repair proposals by excess delay over a relaxed bound. All use official verification and preserve the incumbent. `dev/delay_bounds.py` writes relaxed,non-achievable-in-general tier score ceilings from the recorded initial optimized coverage. See tier-guided-coverage.json for newer selected outputs.
