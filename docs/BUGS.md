# Bugs and limitations

Latest recovery comparison initially reused the historical
neighborhood-comparison.json filename. Detected during final diff review;
restored that file byte-for-byte from the initially clean HEAD and retained the
new report as recovered-neighborhood-comparison.json. Updated only latest
references, preserving historical wide-screen references. Route artifacts,
manifests, scores and solver behavior were unaffected. Screen harness protects
its named reports from overwrites; ad hoc reports also need unique destinations.

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

## Phase3 freezer overwrote comparison report(fixed)

Mode-aware report selection incorrectly retained soft-validation.json as destination. Negotiated metadata overwrote sequential-soft metadata;route artifacts unchanged. Restored soft report from4bbf016,preserved negotiation report separately,corrected destination conditional. Both9-case official score artifacts retained. No solver result invalidation required.

## Stress coverage: short outer watchdog exhausted

Initial stress polish run20261001T225201.888682Z-exact-polish used2s core cap plus5s wrapper allowance. Process terminated at7.004s with no completed core result; wrapper correctly retained the officially legal reference checkpoint(delay1144904,ratio1.0) and marked success false. Do not count this as a successful solver run. Retrying with60s allows measurement of the large-case initialization/search overhead. Dense per-net validation allocates whole-grid adjacency/cost buffers; this is a suspected scaling cost from code inspection, not a measured profile attribution. Raw failed manifest/log retained.

Stress followup:60s retry225241 completes successfully;official CLI confirms improved legal delay1141934. No watchdog change required to obtain initial coverage. Initialization/validation profiling remains next work;do not infer allocation speed from this result.

## Stress profile needs larger completion envelope

Instrumented stress profile225637 with20s core/25s outer cap did not complete;verified incumbent remained unchanged and run success false. Scale08/designs-router profiles completed with stage timers. Retrying stress at previously successful60s cap to measure read/validation/search separately;failure is not an improvement result or a measured stage attribution.

Stress initialization cause measured and repaired:initial per-net whole-grid adjacency/cost allocation consumed43.950s validation in60s run225727. Tree-local compact indexing in225922 cuts validation to0.250s/read0.424s;legal improved output1137194 verified by official checker. Global vertex ownership/foreign-pin checking retained. Historical timeouts/results stay recorded;independent CLI rescore follows. No tests run this session.

Coverage ancestry reporting initially assumed every ancestor config contains mode;historical Phase2 manifest omits it. Default historical ancestor to polish;rerun completes six official scores. Failure stopped report before writing;route outputs/scores unaffected.

## Merged neighborhood checks: seed argument omitted (fixed)

The existing crossing property check looped over three seed labels without passing the seed to the engine. It therefore repeated the default seed. Pass the actual seed and include all nine composed neighborhood modes in the existing crossing and fixed-work rollback/determinism checks. All32 focused checks pass. This affected test coverage only; experiment wrappers already passed their recorded seeds, so no official route results are invalidated.

## Archived incumbent ancestry availability

Continuing a tracked archive can reach an original warm-start path absent from this checkout. The coverage reporter previously classified that as a known locally generated origin. Record artifact availability and unknown reference ancestry explicitly when the chain stops at a missing artifact; retain original incoming coverage evidence for the longer recorded chain. Route hashes, legality and physical scores are unaffected.

## Donor screen source snapshot instrumentation mismatch

A read_s-only edit was briefly saved while the screen binary was already running, then reverted without recompilation. Affected run IDs and actual compiled source hash are explicitly listed in donor-neighborhood-screen.json. All trials used the same binary; routes/priorities/work counts are unaffected. Original manifests/snapshots remain intact. Affected snapshots contain an uncompiled timer edit and alone do not reproduce that exact binary; use the recorded actual compiled source hash. The actual read_s metric excludes donor parsing; wrapper/core wall measurements include it. Freeze source during active experiments, including instrumentation edits.

## Nested portfolio generation costs in basic recombination reports

The basic recombination CLI stopped at an inherited portfolio and omitted its known optimizer-stage cost dictionary. Its physical routes/scores were unaffected;the reported known ancestry cost could undercount available recorded stages. Updated CLI to inherit/deduplicate recorded portfolio costs and missing-ancestor markers,with cycle protection. Historical reports remain byte-original and are partial cost records;do not reinterpret them as total generation costs. Archive-sweep helper already inherited these dictionaries. New output costs still exclude unmeasured reference generation and unrecovered historical artifacts;selection cost remains separate.

## Prototype pool reporter relative output path

Initial CP-SAT selection completed but measurement helper rejected relative log path against absolute workspace root. No parent or canonical routes changed; partial raw artifact retained. Normalize output path at CLI entry; fresh rerun independently checks allhard9cases and preserves complete portfolio report. Physical solve logic unaffected.

### Exact-pool ancestry reporter compatibility
New exact-pool manifests recorded ancestry as a run-cost dictionary without the pre-summed aggregate field. report_tiers now accepts either representation and sums the dictionary when needed. Initial archive attempt failed before writing archives; rerun successfully rescored all45 routes and archived/restored both improved hard/congested runs. No evaluator or benchmark input changed.
