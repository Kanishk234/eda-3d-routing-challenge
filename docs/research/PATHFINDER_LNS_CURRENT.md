# Current pathfinder_lns comparison

Live PR3 head c2d9d9f583d2f332ebb84d22592ee511f6e56e33, updated2026-10-02T00:55:12Z, closed at inspection. Author-reported tier scores: intro1.1514,hard1.3884,scale1.1277,stress1.0914,congested1.3111,designs1.4354. Current outputs were not independently rescored in this check. Corrects earlier chat mapping: congested is not ahead, designs has1.4354 rather than stress. No global leaderboard supremacy claim.

Description: incremental root-distance-seeded A*, fanout-scaled negotiated congestion, exact fixed-owner reroute, seed-net excess-bound priority, small-window rip-up, seed-first routing and conflict-driven repair, nonincreasing physical acceptance, continuation of several distinct solutions, integer radix queue. Hard runtime author-reported34core-hours; cannot compare algorithm efficiency with our short recent passes. No compiled solver source in recursive submission tree; author offers source on request. No contact made and no routes imported as warm starts.

Our whole-net adaptive blocker groups differ from the described window-selected conflict-driven reconstruction. Next concrete experiment: select a small window around a detoured seed branch, free affected whole nets transactionally, route the seed first, repair displaced nets, exact-polish and accept only nonworse total physical delay. Compare against existing adaptive controls with matched work and repeated seeds; retain diverse local incumbents for continuation. This remains a proposed experiment, not implemented evidence. Partial branches require an additional coherent tree/boundary contract.

Source: https://github.com/partcleda/eda-3d-routing-challenge/pull/3 . Snapshot: docs/evidence/phase3/pathfinder-lns-current-description.json.
