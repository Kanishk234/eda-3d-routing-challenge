# Phase 3 — in progress

First controlled operator screen: shortest-path blocker-group repair. Start from the validated Phase2 routes, propose exact driver-rooted trees ignoring routing ownership while retaining foreign-pin protection, identify up to4 blocking nets, release the group transactionally, sequentially reroute it and accept only a legal group with lower total physical delay. Failed/expired attempts restore the full ownership snapshot and old group trees. The Python official checker remains the acceptance boundary.

Screen hard01–07 only, seeds1/2/3,2s/case,5passes,one worker:21/21 outputs legal,0 improvements. Core wall sum1.621s, wrapper wall sum11.576s. No portfolio selection, validation-case use or full-tier score claim.15 kernel checks pass; targeted group success/rollback coverage is still limited and should expand before retaining this operator. Evidence: docs/evidence/phase3/repair-screen.json; raw source snapshots/manifests/routes remain ignored.

Reject this implementation as a default optimization: no observed benefit on the development screen. Keep it as an experimental reference. We have not measured how many proposals exceed the group limit, fail sequential repair or lose delay; do not infer the cause from zero improvements. Current best remains Phase2 score1.046629.

Next: add repair outcome counters, independently exercise failed/successful group transactions, then use measured failure distributions to choose bounded alternative paths/windowed groups or congestion negotiation. Root-aware construction and negotiated-congestion controlled comparisons remain open. Phase3 is not complete.

## Occupied-vertex penalty repair retained

Diagnostics of the first operator:1638 proposals,117 no physical gain,1371 exceed4 blockers,150 attempted repairs,54 failed,96 legal but nonimproving. This supports testing less disruptive paths rather than blindly increasing group size. Added a cost4 penalty per occupied vertex in proposal search only. Physical driver-to-sink delay is independently accumulated along predecessor paths and checked officially; penalties never enter reported delay. This is heuristic candidate selection, not an exact physical shortest-path claim.

Matched development screen: same warm start/cases/seeds,2s/case and5passes.18/21 improve; all legal; case02 unchanged for every seed. Full per-run results and process counters in repair-soft-screen.json. Total development core4.104s/wrapper14.327s, excluding earlier diagnostic/screen costs. No per-case seed portfolio selected.

Fixed seed1 config then validated all9 hard cases:8 improve,1 unchanged, aggregate1.0529719287378287 vs Phase2 1.0466292119096317. Reserved hard08 delay29562→29426,hard09 26376→26166. Official CLI independently agrees. Selected run20261001T213751.861916Z-exact-polish; outputs hashed in soft-validation.json. Core2.149s/wrapper3.913s added to earlier baseline-plus-polish97.952s gives summed pipeline101.865s, not fresh end-to-end timing.16 kernel checks pass; successful and failed group attempts additionally checked in benchmark outputs. Keep group fixture coverage limitation explicit.

Retain repairsoft as an optional stage because it improves development and validation without legality/quality regressions under this configuration. No global-optimum, speedup, unseen-case or best-public claim. Phase3 remains open: root-aware construction/negotiation comparisons, richer group transaction fixtures and later controlled methods. Next concrete work is a driver-aware construction ablation and negotiated repair comparison using fixed development budgets.

## Driver-distance construction ablation

Compared three constructions on546 nets across hard01–07 with every other net fixed: exact root Dijkstra, incremental attachment seeded by driver distance, incremental attachment seeded at zero. All546 complete; root-aware costs match exact for every net. Zero-source case sums exceed exact:11794vs11614;18438vs17882;14200vs14070;17611vs17173;20801vs20359;26768vs26176;29997vs29379. These sums are independent-net measurements, not jointly legal solutions or official tier scores. The case06 exact sum below the incumbent illustrates that finite polishing passes need not reach a fixed point. Retain exact root kernel; no benefit shown for replacing it with repeated attachment searches.17 tests pass. Candidate experiment outputs remain original accepted incumbents.

Submission layout rechecked against current upstream3d8948fdcd6f87165d5ca1efbf4b65e8168e8e81: CONTRIBUTING.md and workflow are byte-identical to pinned versions. Submission PR allows only submissions/<tier>/<method>/** plus generated LEADERBOARD.md. Solver/dev/docs stay in development checkout; clean submission checkout is still Phase5. Upstream advanced by Windows UTF-8 fixes in cli.py,verify_submissions.py,test_leaderboard.py; no benchmark/checker/scorer changed. Retain existing experiment pin for comparability, recheck current evaluator before submission.

Next: implement bounded group negotiated-congestion repair with conflicting states internal, safe transaction rollback, and physical scoring only after conflicts are zero. Compare to fixed repairsoft on development cases before validation. Phase3 remains incomplete.
