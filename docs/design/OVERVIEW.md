# Overview

Goal: legal CPU routing trees with low total driver-to-sink delay and a reproducible route-only entry. Phases 0–2 complete; Phase 3 measured gates satisfied and optimization continuing. A verified compiled routing pipeline exists; current hard score1.205491. Best audited public artifact1.387394 remains higher.

Authoritative pin: 499ad7e2a415a97e9ce9b3396b0477e75ebd13e6, retained for experiment comparability. Rules rechecked at newer upstream3d8948f; see CONTRACT.md. See CONTRACT.md, VERSIONS.md and evidence/phase0/. Supplied research is a hypothesis and historical audit, not new measured evidence.

Initial solver target: hard (9 cases). Intro supports smoke/reproduction; designs/congested are later candidates. Final submission tiers undecided. Scale/stress wait for scaling profiles. C++17 exact polish is implemented and measured; see PHASE2 summary.

Before tuning, reserve hard case_08 and case_09 for validation; case_01–07 may drive development. Future generated development seeds: 1001,1002,1003; validation seeds: 9001,9002,9003. These layouts have not been generated or proven feasible. Released cases are public, not hidden tests. Profiles use hard01/scale08. Generated-case feasibility/protocol remains pending.

Initial one-worker budgets: tests 180 seconds; smoke/CI 60 seconds per subprocess. Proposed Phase 1 intro reproduction: 180 seconds routing and separately scoring; hard reproduction: 600 seconds per step after declaring the next run plan. Intro/hard reproduction, profiles and initial hard polish completed. Quick screens use2s/case;retained wide stage uses10s after measured budget scaling. Longer budgets remain available when evidence justifies them. These are local budgets, not official runtime limits.

Milestones follow phases 0–5: contract → reproduce/profile → reliable CPU engine → measured optimization → full evaluation/freeze → submission preparation. Each checked item needs evidence. User performs commits/publication.
