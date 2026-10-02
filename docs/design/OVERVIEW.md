# Overview

Goal: legal CPU routing trees with low total driver-to-sink delay and a reproducible route-only entry. Phases 0–2 complete; Phase 3 measured gates satisfied and optimization continuing. A verified compiled routing pipeline exists; best recorded hard score1.230658. Best historically audited public artifact1.387394 remains higher; standings were not refreshed in the latest session.

Locally available hard score is1.227449; GitHub-best route artifacts are not
present here. Latest available hard routes: dev/artifacts/20261002T001313.450750Z-exact-polish/routes,
with official rescore/hashes in evidence/phase3/neighborhood-hard-coverage.json.
Missing historical ignored artifacts required a new official-reference recovery
chain; this is not regeneration of the former pipeline. Other tiers' historical
scores and the higher GitHub hard result are recorded in tier-schedule-coverage.json, but those route artifacts
are unavailable in this checkout. Environment and pinned archive are restored.

Authoritative pin: 499ad7e2a415a97e9ce9b3396b0477e75ebd13e6, retained for experiment comparability. Rules rechecked at newer upstream3d8948f; see CONTRACT.md. See CONTRACT.md, VERSIONS.md and evidence/phase0/. Supplied research is a hypothesis and historical audit, not new measured evidence.

Initial solver target: hard (9 cases). User now requests coverage across all six tiers; intended scope is intro/hard/scale/stress/congested/designs, subject to complete official validation. Hard remains the optimization focus. Initial broader runs use attributed official reference warm starts for scale/stress/congested/designs; independent generation/runtime reproduction remains separate work. C++17 exact polish is implemented and measured; see PHASE2 summary.

Before tuning, reserve hard case_08 and case_09 for validation; case_01–07 may drive development. Future generated development seeds: 1001,1002,1003; validation seeds: 9001,9002,9003. These layouts have not been generated or proven feasible. Released cases are public, not hidden tests. Profiles use hard01/scale08. Generated-case feasibility/protocol remains pending.

Initial one-worker budgets: tests 180 seconds; smoke/CI 60 seconds per subprocess. Proposed Phase 1 intro reproduction: 180 seconds routing and separately scoring; hard reproduction: 600 seconds per step after declaring the next run plan. Intro/hard reproduction, profiles and initial hard polish completed. Quick screens use2s/case;retained wide stage uses10s after measured budget scaling. Longer budgets remain available when evidence justifies them. These are local budgets, not official runtime limits.

Milestones follow phases 0–5: contract → reproduce/profile → reliable CPU engine → measured optimization → full evaluation/freeze → submission preparation. Each checked item needs evidence. Local commits are explicitly authorized in this session; user performs pushing/publication.
