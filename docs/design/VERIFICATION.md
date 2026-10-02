# Verification

Latest neighborhood session:60 officially checked case outputs (9 recovery,
6 cycle screen,36 operator screen,9 fixed full-tier followup), all legal and
nonworsening against their explicit starts. Core total/per-net delay and saved
JSON reloading agree with the pinned official checker. Independent official CLI
rescoring confirms recovery1.215286 and selected hard1.227449. Official input
hashes unchanged; C++ compilation has no warnings; git diff --check passes.
No unit tests added/run; historical29 checks do not cover the new operators.
Final submission/regeneration checks remain pending. Evidence:
recovery-operators.json, neighborhood-hard-coverage.json, recovered-neighborhood-comparison.json.

Authority: CONTRACT.md; commands: dev/README.md.

Performed Phase 0:
- 43 unchanged upstream tests pass, run 20261001T165828.977754Z-tests; process wall 6.338 seconds, peak RSS 21,872 KiB; unittest reported 6.190 seconds.
- Official baseline intro/case_01 (16×16×6, 6 nets, seed 741772126) legal, delay 240 vs baseline 240, ratio 1.0. CLI evaluate invokes independent checker.check/scorer.score_case.
- Repeat identical config: legal 240, byte-identical route SHA256 4dc529988bacf55df471330bc2196ff748e5822cdc2c3e22ed9e1bc5c1ca3db2.
- Official verify_submissions.py: 26 present seed files legal; negotiated/negotiated_x2 9/9 complete; negotiated_fast intentionally 8/9.
- leaderboard-all --check current; no leaderboard regeneration.
- C++17 probe compiles/runs; Python development scripts syntax checked.
- Intentional 0.001-second timeout terminates child group, records failure, creates no accepted output and leaves earlier accepted outputs intact.
- All 198 archived files equal pinned Git blobs; official inputs unchanged during checks.

Compact evidence: docs/evidence/phase0/runs.json, official-input-hashes.json, inventory.json. Raw logs/manifests/routes ignored under dev/artifacts/<run-id>/.

Unperformed: full baseline reproduction, participant-route audit/source inspection, small/large profiles, custom solver correctness, other OS/Python CI variants, final selected-tier/submission checks.

Phase 2 fixtures must independently cover nonuniform costs, foreign-pin escape, shared vertices/via endpoint collision, cyclic/disconnected routes, shared-trunk sink sums, failed-repair ownership rollback, parser/serializer consistency, interruption checkpoint recovery. Compare kernel to independent small Dijkstra and hand-calculated costs; avoid formula-mirroring tests. No upstream expected results changed.

Final review: git diff --check passes; no official code/data/submission/leaderboard changes; original research preserved. New development text reviewed for syntax/encoding/trailing whitespace. Pinned upstream HEAD has successful published CI run 36622967607; local results remain WSL-only.

## Phase 2 update

Phases1/2 are complete; earlier “unperformed” statements describe Phase0 only. Authoritative current evidence: docs/evidence/phase2/comparison.json and runs.json; PHASE2 summary covers checks, deterministic outputs, budgets, baseline provenance and limits.13 kernel checks pass and official CLI rescore confirms9/9 legal, aggregate1.046629. Baseline-plus-wrapper sum97.952s is a paired same-machine comparison within600s, not a fresh end-to-end timing or speedup. Generated validation seeds and final submission checks remain unperformed.

## Current Phase3 evidence

All45selectedoutputs independentlyofficialCLIrescored in tier-followup-coverage.json,withper-casehash/legality/delay agreement. Repeated/budget/fresh/treecost benchmarks officiallychecked beforepromotion. No newunitchecks runforlatestmodes;29-check historicallog predatesA*/gap/treecost additions. Finalfreeze/regeneration/currentworkflow submissionverification remain pending. Officialinputs unchanged.

## A* and work-budget properties

User-requested focused suite now passes31 tests. New checks cover30 random small layered/foreign-pin instances comparing A* and ordinary shortest costs with independent coordinate Dijkstra and the official checker;20 mode/work-cap combinations compare complete stdout under2s/5s safety caps, enforce expansion ceilings and legal rollback. Existing tests retain timeout/rollback/serializer coverage. Large stress fixed10M runs also yield identical stdout across30s/45s safety caps. Evidence:work-budget-profile.json. This does not establish all-config determinism or explicit internal owner consistency after every accepted move; that instrumentation remains pending.

Schedule configuration:32 focused tests pass. New parser property checks implicit versus explicit defaults give identical stdout; unknown, negative, oversized, duplicate and malformed keys are rejected. Prior random shortest-cost, work-cap, timeout and legal rollback tests retained. Evidence schedule-comparison.json. No upstream expected results modified.
