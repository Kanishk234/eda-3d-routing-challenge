# Public fork and PR review — 2026-10-02

## Scope and evidence

GitHub API snapshot:23 forks,26 open/closed PRs,all advertised branches in each fork (each list under100),34 distinct fetched head-tree records after deduplication. No recursive tree was truncated. Compared non-toolkit source against current upstream, excluding our own fork. Found18 distinct non-toolkit code blobs,including historical Rust versions, and35 distinct changed method/provenance documents. Also inspected Taz33m's unchanged pathfinder_lns metadata and the external IrwinJam/m3d-router repository linked by submission metadata.

Inventory with repository/branch/PR commits,paths and content hashes: docs/evidence/phase3/public-source-audit.json. Raw fetched evidence is /tmp/routing-public-audit; only compact inventory is tracked. PR26's diff endpoint returned HTTP422; its complete recursive head tree was fetched successfully. Diff lists may truncate at100 files; tree discovery determines source coverage. Private solvers,unpublished sources and future updates are outside this snapshot. This is a complete inventory of the returned public network/branches with targeted algorithm review,not a claim that every historical source line was exhaustively audited. No code was executed or copied into our solver; no competitor routes used as inputs.

## What is actually available

| Entry/repository | Inspected evidence | Useful differences | Limit |
|---|---|---|---|
| Taz33m/pathfinder_lns,PR3 | pathfinder-lns branch recursive tree and hard meta.json | C++ fanout-weighted PathFinder,exact per-net rerouting,region/warm-repair LNS | Submission branch publishes routes/metadata; no separate solver implementation located |
| IrwinJam/spt_lns,PR12/25; IrwinJam/m3d-router | core.py,router.py,overnight.py,README,LICENSE | Slow negotiation schedules; annealed ideal/window neighborhoods; transient uphill/neutral states with best restoration; longer repeated fresh/warm CPU chunks | Defaults describe intended use,not proof of actual winning compute; public results not reproduced here |
| kesudh/warm_lns_refinement,PR21 | Current Rust replay kernel,Python crossover/replay,source inventories/historical capability differences,README/meta | Radix/bucket queues; feasible per-sink bounds; random tight-parent extraction; dynamic displacement chains with per-entry pricing; bounded static CBS; specialized on-demand chain tolls | Uses attributed public parent routes; their output gains do not measure independent fresh construction |
| sethupathib fork,two cursor branches | cpp/m3d_route.cpp,submissions/hard/delay-opt/solve.py | Driver SPT construction; additive/multiplicative negotiation; blocker/pair reroute; spatial LNS | Familiar algorithm family; no reproduced performance advantage |
| anveshshekhar,PR7 | my_router.py,merge_best.py | Exact physical SPT with hop tie-break; hard greedy orderings,negotiation,residual polish,adaptive spatial groups | Restricted bbox lower bounds need caution; not a transferable global bound by declaration |
| jay-tau/coordinated_refinement,PR5/24 | Method/provenance READMEs and meta | Min-cut whole-tree crossover; bounded rerouting | Solver source hashes listed but corresponding C++ source not located in inspected tree; output parents attributed |
| reubalink/THOMACHAYAN,PR10 and newer branch | Metadata | Window negotiation and exact chain-flow repair disclosed; no copied public routes claimed by author | Author description,not inspected implementation |
| CarterT27,PR6 | Metadata | Blocker-aware joint groups,annealing | No separate solver implementation located |
| Remaining entry forks/PRs | Recursive branch trees,changed file inventory,available methods/provenance | Some entries select others' whole-case outputs; toolkit-only/unchanged forks offer no new solver | GPU-accelerated label in drama3d metadata is not a reproduced hardware/algorithm result |

The current upstream snapshot also includes tools/evaluator PRs. These are authority changes to review before submission,not opportunities to change our immutable pinned score inputs.

## Implications for our work

No evidence establishes a CPU ceiling. Public CPU code has similar fundamentals but different search trajectories and planned compute allocation. IrwinJam's overnight.py declares 20-minute hard chunks and multi-hour worker campaigns; our recent native stages cap each case at60s. This comparison is of configured budgets,not measured equal-hardware performance.

1. **Dynamic displacement chains:** our previous group selection is static. Implement our own queue that reserves a replacement and dynamically adds displaced nets,with cap/rollback/whole-case checking. Initial prototype gets2 delay units on hard07 via a single-net move; no coordinated chain gain yet. Matched strict/neutral20M followup is running separately.
2. **Slow fresh negotiation:** investigate whether our fresh starts legalize too quickly into bad packing. Compare gradual present/history schedules and longer initial routing with continued incumbents. Requires separate compiled generation experiment; do not transfer public warm-start results into a from-scratch claim.
3. **Delay-neutral tight-parent geometry:** root SPT costs can stay fixed while different shortest-path predecessors change resource packing. Test secondary resource geometry under exact physical distances,then coordinated moves. Our prior static-CBS tie-break helped one restricted proof but did not improve score.
4. **Per-sink feasible bounds and queue speed:** can increase throughput while preserving exact physical shortest paths. Profile before editing compiled engine; current native job freezes that source.
5. **Two-parent crossover:** already implemented in our own code,so source review does not make it a new method for us.

The new adaptive price pool is also measured independently: six subgradient rounds and twelve LP-price rounds on three hard development cases both give zero accepted gain. All final finite-pool selections are OPTIMAL,but that says nothing about geometry outside the pool. LP fractional delay stays at the incumbent in these pools; global pricing alone has not generated complementary alternatives.

## Sources and licensing

- Taz33m exact entry: https://github.com/Taz33m/eda-3d-routing-challenge/blob/c2d9d9f583d2f332ebb84d22592ee511f6e56e33/submissions/hard/pathfinder_lns/meta.json
- IrwinJam solver: https://github.com/IrwinJam/m3d-router ; fetched tree dca18b22954261536106fd87e4abe1e75e1a9185. LICENSE is MIT,Copyright2026 James(IrwinJam). No code adapted.
- kesudh replay: https://github.com/kesudh/eda-3d-routing-challenge/tree/fb2101ee2cc58ac35b4031c904359a603092a029/submissions/intro/warm_lns_refinement/replay
- sethupathib: https://github.com/sethupathib/eda-3d-routing-challenge/tree/cursor/cpp-router-2651
- anveshshekhar: https://github.com/anveshshekhar/eda-3d-routing-challenge/blob/dfbcba48bd762433350aea82cd653af74e7137ac/my_router.py
- Routing column formulation primary paper: https://cseweb.ucsd.edu/classes/fa23/cse248-a/papers/routing/GlobalRouting.pdf . Its congestion/wire objective and rounding guarantees are not our delay objective or prototype guarantees.

Root competition license does not by itself resolve every new author's source attribution. Any future source adaptation needs explicit license inspection/retained notices. Current work uses independent implementations of disclosed concepts.
