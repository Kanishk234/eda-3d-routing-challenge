# Bugs and limitations

## 2026-10-01 — Pre-existing unclosed-file warnings (observed)

Unchanged tests print ResourceWarnings in tests/test_leaderboard.py:24 and m3d/cli.py:251,321. Cause: open(...).read()/json.load(open(...)) without context managers. All 43 tests pass; no affected delay/legality result observed. No upstream fix made. Context-manager fix would belong to separate toolkit work. Evidence: 20261001T165828.977754Z-tests/tests.log.

## 2026-10-01 — Fixed hard Pareto frontier assertion (source-confirmed risk)

test_seed_hard_entries_score_as_expected loads all submissions/hard entries and requires the Pareto set equal exactly negotiated/negotiated_x2. A valid new runtime-bearing entry can change the frontier and fail this assertion. Pristine tests pass; a new entrant-triggered failure was not reproduced here. Historical research reports are separate evidence.

No evaluator/test patch or fabricated runtime made. Before Phase 5 inspect current code/CI; if triggered, seek clarification/separate fix or omit optional runtime only if current rules permit, retaining honest local measurements.

## 2026-10-01 — Host tool transport errors (resolved fallback)

Sandbox exec/Node helper failed before command launch; apply_patch rejected WSL reparse path. Windows Git dubious ownership. Authorized WSL Git/execution and PowerShell writes succeeded; no global Git settings changed. No automatic-review rejection occurred.

Remaining unknown/unperformed work: solver, checkpoint/rollback/resume, full-suite reproduction, participant audit, small/large profiles, cgroup quotas. Timeout run RSS unknown. CMake absent/unnecessary.

## 2026-10-01 — Development inspect module shadowed Python stdlib (fixed)

Adding pstats to the Phase 1 harness caused dataclasses to import dev/inspect.py instead of stdlib inspect. Its top-level audit executed unintentionally, refreshing phase0 environment/upstream evidence at 17:17 UTC, then raising AttributeError for get_annotations. Renamed it capture_environment.py; source docs updated. Earlier raw run manifests, official inputs and route/score results were unaffected. Phase0 environment/upstream JSON now reflect this later capture, not the original 16:58 UTC capture; historical facts remain in the worklog. Keep evidence-producing code under a main guard in future. Regression: import pstats/inspect resolves stdlib and the audit harness executes normally.

Phase2 audit: stale no-solver/unfinished-profile statements above describe earlier stages. Current state is in PHASE2 summary. Tightened serialization acceptance to compare reloaded physical delay as well as legality; no affected earlier outputs found (official rescore agrees). Group rollback and unseen generated cases remain future work.
