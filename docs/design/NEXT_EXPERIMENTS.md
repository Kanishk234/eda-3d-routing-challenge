# Ranked optimization experiments

Current evidence: hard-gap-diagnosis.json, work-budget-profile.json, guided-cycles-screen.json under docs/evidence/phase3. Rankings are hypotheses, not predicted numeric gains. Tune on declared development cases; report held-out hard08/09 only after configuration selection. Final all45-case reporting must not drive another tuning round.

| Rank | Experiment | Expected benefit | Cost and acceptance evidence |
|---|---|---|---|
| 1 | Measure shortest search-loop, ownership snapshot, negotiation scans and attach allocations on stress/congested representatives | Identify the actual throughput bottleneck | Low; isolated fixed-work profiles, repeated timing, memory |
| 2 | Store g in heap entries and compare tighter obstacle-free layer lookahead | Less heuristic work and fewer expansions | Low/moderate; independent Dijkstra equality and matched work/cap results, include geometry regressions |
| 3 | Fine fixed-point congestion prices; explicit config fields | Better multi-sink packing; avoid rounded-zero prices | Moderate; overflow checks and dev seeds1–3, matched-work controls; retain current units as control |
| 4 | Generation-stamped search buffers or touched resets, then ownership undo log if profiles justify it | More repairs per CPU-second on local groups | Moderate; rollback/owner invariant tests before replacing snapshots; preserve byte-identical fixed-work output where semantics unchanged |
| 5 | Successive-halving parameter sweep | Measured price/history/neighborhood schedules | Moderate/high; serial pilot then memory-bounded independent workers, disclose total tuning cost |
| 6 | Zero-price shortest-DAG compaction, then iterative downstream-count pricing | Preserve individual shortest delays while releasing resources; improve multi-sink trees | High; coherent predecessor tree, checker validation, physical-delay acceptance. Priced shortest distances do not prove physical-delay neutrality |
| 7 | Adaptive spatial/blocker neighborhoods and diversified independent walks | Escape remaining global packing limitations | High; reward per CPU-second, repeated seeds and hit rates; parallel ownership mutation deferred |

Already done: public per-net gap diagnosis; expansion budgets; A*/Dijkstra and fixed-work output checks; first reset/rebuild profile. Pending: explicit owner consistency after every accepted move, detailed other-tier profiles, broader fixed-work seed statistics. No claimed implementation of all review suggestions.

Do not delete soft repair: it improved18/21 development trials. Keep ordinary Dijkstra as an experimental control. Historical weak operators may be archived after their reproducing configurations are preserved. For a dual bound, current-tree downstream counts do not automatically bound an alternative tree; prove the resource-price inequality before reporting it. Fixed per-net fanout divisors provide a weaker defensible route to a bound.
