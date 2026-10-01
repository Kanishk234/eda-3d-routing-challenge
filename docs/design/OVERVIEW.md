# Overview

Goal: legal CPU routing trees with low total driver-to-sink delay and a reproducible route-only entry. Phase 0 complete; Phase 1 next. No competitive solver exists yet.

Authoritative pin: 499ad7e2a415a97e9ce9b3396b0477e75ebd13e6, verified against current upstream October 1, 2026. See CONTRACT.md, VERSIONS.md and evidence/phase0/. Supplied research is a hypothesis and historical audit, not new measured evidence.

Initial solver target: hard (9 cases). Intro supports smoke/reproduction; designs/congested are later candidates. Final submission tiers undecided. Scale/stress wait for scaling profiles. CPU-first C++17/Python direction remains unmeasured.

Before tuning, reserve hard case_08 and case_09 for validation; case_01–07 may drive development. Future generated development seeds: 1001,1002,1003; validation seeds: 9001,9002,9003. These layouts have not been generated or proven feasible. Released cases are public, not hidden tests. Phase 1 must finalize representative small/large profile cases and the generation protocol.

Initial one-worker budgets: tests 180 seconds; smoke/CI 60 seconds per subprocess. Proposed Phase 1 intro reproduction: 180 seconds routing and separately scoring; hard reproduction: 600 seconds per step after declaring the next run plan. No suite or optimization launched. Future C++ screening can start at 10 seconds/case, seeds 1,2,3, after correctness/profile gates. These are local budgets, not official runtime limits.

Milestones follow phases 0–5: contract → reproduce/profile → reliable CPU engine → measured optimization → full evaluation/freeze → submission preparation. Each checked item needs evidence. User performs commits/publication.
