# Ranked optimization experiments

Latest measurement: whole-net spatial prototype screened at5M/20M expansions
on hard01/04/07,seeds1–3 against fine and fine-diverse. It loses6/9 versus
fine at both budgets; keep experimental. Fine-diverse wins7/9 at both caps,
selected for frozen full-hard validation. See spatial-comparison.json and
spatial-5m/20m-screen.json. Next spatial revision should measure group sizes
and try smaller/randomized groups or preserve branches at region boundaries;
current detour-sum ranking favors larger nested regions. These are hypotheses.
The original research motivation follows.
Reubalink metadata/commit history reports window LNS and negotiated repair in
ripped windows, but no custom source is published. Independently checked final
routes score1.362234; predecessor1.267187. Our recorded one-sink total is better,
but multi-sink total is17906 worse, supporting coordinated branching/trunk work.
See reubalink-inspection.json and OPTIMIZATION_FOLLOWUP.md for provenance,
limits, proposed4/8/12 XY boxes, full-net transactional repair, and fixed5M/20M
development comparisons. This is a proposed experiment, not a retained operator
or a claim to reproduce their implementation. Avoid tuning on08/09 or importing
public output geometry/warm starts. Larger budgets and method changes are
confounded in their score progression; no five-hour search performance claim.

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

## Local pipeline diversity diagnosis

`local-hard-basin-comparison.json` officially checks both our adaptive and preserved fine-diverse routes. Totals164235 versus163669 hide9972 delay units favoring the adaptive pipeline and10538 favoring the fine-diverse pipeline across individual nets. This is evidence of distinct ownership/branch layouts, not a legal combined improvement. Both are our local pipelines with explicit ancestry.

Next candidate: propose a target net's alternate tree from the other local pipeline, collect every current owner of its vertices, then transactionally negotiate that full-net group. Accept only a legal reduction in total physical delay. Compare against ordinary diverse proposals under matched expansion budgets on01/04/07; exclude08/09 from selection. Limit group size, retain rollback and account for reading donor routes. This could transfer useful geometry between independently generated basins without assuming their trees can be spliced. Report donor origin and total search costs. A generic engine extension should accept an explicit alternate solution, not hard-code benchmark paths.

A cheaper preceding experiment is composing diverse corridor generation with adaptive dependency groups. Each has measured value separately; their extra searches can compete for the same work cap, so compare the composition against both controls before retaining it. Current spatial windows regress and should remain experimental until smaller group selection is measured.
