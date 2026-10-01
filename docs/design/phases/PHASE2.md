# Phase 2 — Reliable CPU solver

Status: complete for the declared baseline-plus-polish pipeline; see docs/summaries/PHASE2.md and docs/evidence/phase2/.

- [x] Pinned I/O and officially legal outputs on all9 hard cases — selected run212816, independent CLI rescore.
- [x] Shortest paths, terminal protection, ownership, trees, sink delays and serialization —13 independent kernel checks; official total/per-net agreement and reload.
- [x] Deterministic seed/config, bounded search, safe interruption and incumbent recovery — repeat output hashes, SIGTERM fixture, zero-budget and explicit resume manifests. Abrupt termination preserves the pre-search checkpoint.
- [x] Baseline comparison under common600s envelope — paired baseline-plus-polish97.952s vs baseline94.765s; quality1.046629 vs1.0; all cases improve. Added runtime and baseline reuse disclosed; no speedup claim.

This phase establishes a reliable pipeline requiring baseline warm starts. Coordinated routing/competitive optimization remains Phase3; final regeneration/freeze remains Phase4.
