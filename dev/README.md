# CPU development workspace

## Recovery and neighborhood experiments

Neighborhood operators now compose with each search/pricing family:
`fanout_astar_{shuffle,diverse,adaptive}`,
`fanout_tight_{shuffle,diverse,adaptive}`, and
`fanout_fine_{shuffle,diverse,adaptive}`. Tight uses the cached layer-aware
lookahead; fine additionally uses16-unit physical/congestion priorities.
Corridor penalties share those units. Work-budget and present/history schedule
arguments apply to all combinations. These combinations are implemented but
have not been benchmarked; recorded scores remain results of earlier binaries.

The comparison harness accepts `--kernel`, `--work-budget`, `--budget`,
schedule flags, and a new `--out` destination. For a matched fixed-work screen
from the locally available recovered hard routes:

```bash
.venv/bin/python dev/neighborhood_screen.py operators --kernel fanout_fine --work-budget 5000000 --budget 60 --present-initial 2 --present-step 1 --history-step 1 --start dev/artifacts/20261002T001313.450750Z-exact-polish/routes --out docs/evidence/phase3/combined-fine-neighborhood-screen.json
```

This compares fine alone and its three neighborhood operators on01/04/07,
seeds1–3, with the same work cap/schedule/starts. Expanded vertices do not
represent equal CPU work across different operators. Existing report files
cannot be overwritten. GitHub-best1.230658 routes remain unavailable locally;
the example starts from the recovered1.227449 pipeline.

If ignored historical routes are missing, `dev/neighborhood_screen.py recover`
creates a new hard-tier pipeline from attributed official reference routes,
using fixed seed1, fanout A*, 20 seconds/case, and at most1000 cycles. It does
not recreate the historical optimization chain or claim its score. Run
`bash dev/setup.sh` and compile the engine first.

```bash
.venv/bin/python dev/neighborhood_screen.py recover
.venv/bin/python dev/neighborhood_screen.py cycles --start dev/artifacts/RECOVERY_RUN/routes
.venv/bin/python dev/neighborhood_screen.py operators --start dev/artifacts/RECOVERY_RUN/routes
```

These serial screens reserve hard08/09 for subsequent fixed-config validation.
Cycle screening compares100/1000 cycles at10 seconds, seed1, on01/04/07.
Operator screening compares unchanged fanout_astar, fanout_astar_shuffle,
fanout_astar_diverse, and fanout_astar_adaptive at5 seconds/1000 cycles,
seeds1–3, on the same frozen01/04/07 routes. Existing report names are protected
against accidental overwrite. All candidates pass the official checker and
physical-delay agreement before acceptance; raw routes/manifests remain ignored.

Shuffle randomizes negotiation order each round. Diverse adds two proposal
searches with cumulative corridor penalties, selecting an improving proposal
with fewer displaced owners, then lower delay. Adaptive mixes direct blockers,
transitive blockers, and groups augmented with three random nets, capped at13
nets. Weights reward fractional physical-delay improvements, with an exploration
floor; this initial implementation does not normalize rewards by CPU cost.
Both diverse/adaptive also shuffle repair order; compare against shuffle to
separate their additional mechanisms. Experimental modes preserve strict
physical improvement and full transaction rollback; defaults are unchanged.

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

## Where the algorithm lives

- `dev/solver/exact_polish.cpp`:compiled engine and all route-search/tree/ownership/negotiation/repair/restart algorithms;`main` selects the mode.
- `dev/run_polish.py`:official JSONload/check/score,integer bridge to the engine,checkpoint/outputpromotion,case/suite execution,and manifests. It is part of the complete solver pipeline.
- `dev/guided_screen.py`:declared repeated-seed,budget,fresh-start,and discounted-treecost experiments;it chooses configurations but implements no routing.
- `dev/report_tiers.py`:independent officialCLI rescoring of explicitly selected complete runs.

The engine binary reads an integer bridge,not officialJSON directly. Run it through the Pythonwrapper with validated starting routes. Hardinitialroutes were generated by the officialnegotiated router;fourlater tiers use explicitlyattributed officialreferences. Fresh-startmode may search from emptygeometry but retains a validatedfallback. FinalrouteJSONs are separate submissionartifacts.

Fixed-work experiment example (wall cap remains a safety limit):

```bash
.venv/bin/python dev/run_polish.py --suite benchmarks_stress --case case_01 --resume-dir dev/artifacts/20261001T230938.706316Z-exact-polish/routes --mode fanout_astar --budget 45 --passes 100 --work-budget 10000000
.venv/bin/python dev/diagnose_hard_gap.py
.venv/bin/python dev/test_exact.py
```

`--work-budget 0` preserves wall-budget behavior. Counters include expansions per optimization second and shortest reset/reconstruction timing. Ranked follow-up experiments:docs/design/NEXT_EXPERIMENTS.md.

Tighter physical lookahead is optional:use `--mode fanout_tight` for negotiated exploration or `--mode astar_tight` for fixed-other-net polish. Example measured hard follow-up:

```bash
.venv/bin/python dev/run_polish.py --suite benchmarks_hard --resume-dir dev/artifacts/20261001T234843.075364Z-exact-polish/routes --mode fanout_tight --budget 60 --passes 1000 --work-budget 5000000
```

`dev/search_kernel_screen.py --control PATH` compares a rebuilt637a829 control binary with the current engine serially atfixed5M expansions. Treat those outputs as development measurements;this script doesnotcreatecompleteentries.

Price-resolution experiment: `--mode fanout_fine` combines tight lookahead with16 search units per physical unit. Compare against `fanout_tight` at matching work budgets. Defaults retain original units. `dev/pricing_screen.py` runs the declared hard/congested case01 comparison on seeds1–3 serially and records manifests; it does not select complete entries or use held-out cases for tuning.

Explicit local-negotiation schedule example:

```bash
.venv/bin/python dev/run_polish.py --suite benchmarks_hard --resume-dir dev/artifacts/20261002T000141.903840Z-exact-polish/routes --mode fanout_fine --budget 60 --passes 1000 --work-budget 5000000 --present-initial 2 --present-step 1 --history-step 1
.venv/bin/python dev/schedule_screen.py
```

Defaults2/2/2 preserve prior behavior; values are bounded0..64. These settings control negotiated repair groups, not whole-instance restart/candidate algorithms. Optional PDF reader requirements are in dev/requirements-research.txt.

## Spatial group prototype

Optional `{fanout_astar,fanout_tight,fanout_fine}_spatial` modes select a
random incumbent vertex of a detour-ranked target, examine centered4/8/12 XY
regions across all layers, and take up to12 touching neighbors ranked by
physical excess over the obstacle-free bound. Choose the region with greatest
neighbor excess (ties favor the smaller region). Rebuild whole trees with
shuffled negotiation; external ownership and foreign pins remain frozen.
Replacement routes may leave the region. Strict physical improvement and
transaction rollback protect the incumbent. This is an original group-selection
prototype, not a reproduction of an unpublished entrant solver.

Matched screen (hard01/04/07,seeds1–3,fine/fine-diverse/spatial):

```bash
.venv/bin/python dev/neighborhood_screen.py spatial --kernel fanout_fine --work-budget 5000000 --budget 60 --present-initial 2 --present-step 1 --history-step 1 --start dev/artifacts/20261002T001313.450750Z-exact-polish/routes --out docs/evidence/phase3/NEW-spatial-screen.json
```

Use a new report destination for every run; `--work-budget 20000000` supplies
the second declared comparison. Outputs are independently checked through the
pinned official checker/scorer by the wrapper before acceptance. Development
comparisons are not full-tier scores.

Continue a fixed adaptive stage across all six tiers, using the preserved incoming hard run:

```bash
.venv/bin/python dev/advance_all_tiers.py --coverage docs/evidence/phase3/tier-merged-neighborhood-coverage.json --label adaptive-all-tiers --single-stage --mode fanout_fine_adaptive --seed 1 --work-budget 5000000 --hard-start dev/incumbents/hard/20261002T022353.079439Z-exact-polish
```

Use a new label for subsequent stages. `--hard-start` names a run directory with manifest and routes. Older archived ancestors may be unavailable; the new report states that limitation. Compare local routing patterns without combining their nets:

```bash
.venv/bin/python dev/compare_local_routes.py LEFT_ROUTES RIGHT_ROUTES --out NEW_REPORT.json
```

Experimental `fanout_fine_hybrid` composes diverse corridor proposals with adaptive blocker groups. The repeated-seed5M development screen loses to adaptive alone overall; keep it optional. Run matched controls with `neighborhood_screen.py hybrid`.

Select complete legal case outputs from explicit local complete runs:

```bash
.venv/bin/python dev/select_case_portfolio.py RUN_A RUN_B --suite benchmarks_hard --out NEW_REPORT.json
```

This creates a separate `*-case-portfolio/routes` directory and portfolio provenance, not a fabricated single solver-run manifest. Official hashes/checking and independent CLI scoring guard every selected case. Resume through `run_polish.py --resume-dir` and disclose both pipelines' effort. Do not mix individual nets independently.
