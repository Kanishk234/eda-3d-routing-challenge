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
