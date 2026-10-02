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

Update: cached tighter lookahead and stored-g comparison completed (search-kernel-screen.json);fullhardnow1.230000. Snapshot/setup/scan counters added;stressrepresentative madezerogroupattempts,so large-group profile remainsopen. Nextpriority is fine fixed-point congestion-price/config comparison. Storedg has no clear timingwin;avoid claiming one.

Fine-price stage is now measured:4/6 representative wins,1tie,1loss at matched5M expansions. Full hard1.230324/congested1.088060. Next: explicit configurable present/history schedules and modest parameter sweep, then coordinated topology/neighborhood work if repeated seeds show a plateau. DATE abstract suggests adaptive via search penalties as another controlled candidate; preserve physical scorer weights.

Explicit schedule config and four-schedule repeated-seed pilot completed:hard2/1/1,congested2/4/4 selected on case01;each beats default in all3 seeds of its tier. Current hard1.230658/congested1.090605 after full fixed stages. Next: broaden declared development cases to check schedule robustness, then evaluate either nonlinear marginal-overflow prices or coordinated topology/window repairs. Full DATE reading is now available; adaptive via discount requires a matching admissible lookahead and physical-delay acceptance.
