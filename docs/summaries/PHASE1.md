# Phase 1 — complete

Reproduced selected intro/hard baselines with unchanged official routers: every case legal and each delay exactly matches suite.json, both aggregates1.0. Clean hard run94.765s, peak22,080KiB. Intro quality valid; its55.676s run had about1.3s overlap with an early interrupted hard attempt, so it is not an isolated timing sample. Interrupted45.208s attempt retained/excluded; no hidden search cost.

Validated pinned PR3 output: nine hard routes legal, aggregate1.387366331135629. This is public output quality, not a reproduced solver or our result. No added Python/C++/Rust implementation found in the inspected pinned tree. Public artifacts/provenance retained apart from baseline-only incumbents.

Profiles: hard/case_01 search13.071s of13.109s routing, 431 calls including369 reroutes, peak26,652KiB. Scale/case_08 search133.947s of134.012s routing, 265 calls/no reroutes, peak62,536KiB. cProfile overhead affects these runtimes; checking/serialization are negligible next to search. Evidence supports starting a compiled search kernel, not optimizing JSON or adding GPU infrastructure. Advanced methods remain untested.

Per-case comparisons/manifests/profiles in docs/evidence/phase1/. Raw profiles/routes/source snapshots in ignored dev/artifacts/. Fresh baseline incumbents validated and indexed under dev/artifacts/incumbents/{intro,hard}; public output not adopted. Hard case_08–09 and generated seeds9001–9003 remain excluded from tuning; profiling used hard01/scale08.

Fixed dev/inspect.py stdlib shadowing by rename/main guard; its accidental evidence refresh is disclosed in BUGS.md. No official code/data changed. Phase2 next: exact C++17 single-net tree rerouting, independent correctness checks, safe ownership/rollback and validated incumbent recovery.
