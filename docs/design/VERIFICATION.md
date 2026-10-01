# Verification

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
