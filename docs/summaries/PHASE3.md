# Phase 3 — in progress

First controlled operator screen: shortest-path blocker-group repair. Start from the validated Phase2 routes, propose exact driver-rooted trees ignoring routing ownership while retaining foreign-pin protection, identify up to4 blocking nets, release the group transactionally, sequentially reroute it and accept only a legal group with lower total physical delay. Failed/expired attempts restore the full ownership snapshot and old group trees. The Python official checker remains the acceptance boundary.

Screen hard01–07 only, seeds1/2/3,2s/case,5passes,one worker:21/21 outputs legal,0 improvements. Core wall sum1.621s, wrapper wall sum11.576s. No portfolio selection, validation-case use or full-tier score claim.15 kernel checks pass; targeted group success/rollback coverage is still limited and should expand before retaining this operator. Evidence: docs/evidence/phase3/repair-screen.json; raw source snapshots/manifests/routes remain ignored.

Reject this implementation as a default optimization: no observed benefit on the development screen. Keep it as an experimental reference. We have not measured how many proposals exceed the group limit, fail sequential repair or lose delay; do not infer the cause from zero improvements. Current best remains Phase2 score1.046629.

Next: add repair outcome counters, independently exercise failed/successful group transactions, then use measured failure distributions to choose bounded alternative paths/windowed groups or congestion negotiation. Root-aware construction and negotiated-congestion controlled comparisons remain open. Phase3 is not complete.
