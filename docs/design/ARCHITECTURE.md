# Architecture

After GitHub integration, each shuffle/diverse/adaptive neighborhood operator
can use legacy fanout A*, cached tight lookahead, or fine16-unit pricing.
All families retain the shared expansion ceiling and negotiation schedule
configuration. Corridor prices are checked/scaled in the same units as
physical costs before queue insertion; physical tree scoring stays unscaled.
The screen harness forwards the selected kernel, work/time budgets and schedule
to controls and candidates equally, with separately named protected reports.
Combined families are compiled but have no new benchmark/unit-test evidence.

Neighborhood experiments add optional seeded negotiation-order shuffling,
two repelled-corridor ideal-tree proposals, and adaptive direct/transitive/random
groups. Corridor penalties are nonnegative search costs only; target proposals
must lower physical delay and selected group replacements must lower total
physical delay. Transitive groups inspect displaced nets' ideal routes; random
groups add at most three nets. Both are capped at13 nets with full ownership/tree
rollback. Adaptive weights reward fractional group-delay reduction with a small
exploration floor, not reduction per CPU second. Separate group RNG avoids
altering legacy-mode RNG initialization. Accepted pass ceiling is1000; defaults
remain bounded. Official output checking and serialization agreement are still
required; latest modes have benchmark evidence, not new unit-test evidence.

Setup, measurement, official verification and C++ exact single-net polish are implemented. See PHASE2 summary.

Immutable evaluation boundary: exact Git archive dev/upstream/499ad7e2a415a97e9ce9b3396b0477e75ebd13e6. All 198 archived files verified against pinned Git blobs; wrapper hashes inputs before/after. Development in dev/, engine in dev/solver/, bulk outputs under ignored dev/artifacts/. Never edit scorer/benchmarks to improve results.

Implemented C++17 engine: packed ID=(z*height+y)*width+x, implicit six neighbors, int64_t physical totals and safe infinity/overflow checks. Keep physical delay, congestion penalties and priorities separate. Driver-rooted coherent predecessor tree supplies terminal paths; remove irrelevant nonterminal leaves. Ownership counts a vertex once per net; foreign pins always reserved.

Current interface: immutable parsed instance + explicit seed/config/budget + optional attributed verified incumbent → candidate trees, statistics and termination status. Net/group replacement must release ownership and support complete rollback. Conflicting negotiation states stay internal. The current polisher leaves the old route untouched until a complete improving candidate is ready; rejected searches preserve ownership. Group repair and whole-instance restart are implemented with transaction rollback; protected threshold walks restore the best legal snapshot.

Output follows model.py/FORMATS.md: version-1 m3d-submission, matching instance, one route per net, integer adjacent-vertex edges. Official independent reloading/checking/scoring is required before acceptance.

Implemented wrapper: unique run directories; smoke candidate written then officially evaluated, accepted output atomically renamed. Previous runs survive timeout. Suite outputs stay isolated and are not automatically promoted. run_polish.py supports --resume-dir and preserves a validated pre-search checkpoint; completed candidates are officially checked before replacement.

Resource-pricing variants:fanout scales search congestion prices only;compact attachment is heuristic3/4 driver seeding using integer-scaled priorities. Root-to-sink physical distances are accumulated separately and officially checked. Accepted-output resource metrics count each net vertex once(including via endpoints),edges and vias independently of delay.

Initial tree validation uses compact local indices over each tree's sorted vertices. Adjacency/distance arrays scale with tree size rather than grid size per net. Global pins/owners remain dense and unchanged. Measured stage timers separate read(including initial validation) from optimization;whole-core deadline includes initialization.

Optional exact A* priority adds a consistent physical lower bound to g,retaining g as physical-plus-congestion searchcost. The bound is distance to the union of static sink-layer XY rectangles in a graph with every horizontal edge at the cheapest layercost. All sinks have h=0;goal rectangles remain static after sinks finish. Costs/ownership/predecessor trees remain unchanged in meaning. Changed queue order can change equal-cost geometry and subsequent multi-net outcomes. Gap-order mode sorts repair proposals by physical delay minus obstacle-free per-net bound;this is a heuristic for allocating search,not a physical score modification.

Experimental discounted-treecost groupconstruction:multi-source roots seeded with fullphysical driverdistance;existingtree congestioncost is already paid,so only newvertices add congestionprice. Samefanout discount as control. Trees remain acyclic by joining a newpath once to the existingtree;physicalrootdist separately accumulates. This is a greedyheuristic,not Held/Perner's componentmerging algorithm or guarantee. Prototype was not retained asdefault after representative regressions.

Optional `astar_tight`/`fanout_tight` use a cached layer-pair/XY-distance table:minimum over transit layer k of XY*layer[k]+via*(abs(start_z-k)+abs(goal_z-k)). Distance to the same static sink-layer rectangles is consistent because it is shortest physical distance to a goal set in the obstacle-free graph. All sinks have zero heuristic. It strengthens the cheapest-layer bound without making all nets' paths jointly feasible. Stored heap g permits direct stale checking; the queue still orders by priority, tie rank and vertex first.

Additional profiles measure repair owner-copy time and negotiated-group setup/conflict-scan time. They omit uphill best-state snapshots and restricted-candidate setup. Zero group attempts give no evidence on transaction scaling.

Experimental `fanout_fine` uses16 integer search units per physical unit in shortest search. Physical moves, occupied-resource penalties and A* bounds are all scaled consistently; congestion history/present price is scaled before fanout division. Thus fractional penalties survive to1/16 resolution. The physical predecessor-tree delay accumulator remains unscaled. Priority multiplication rejects overflow. Compact/discounted attach modes retain their existing units; fine mode uses shortest-based group routing only.

Negotiated local repair now uses `NegotiationConfig`:present_initial/present_step/history_step, defaults2/2/2. Present cost in round i is initial+step*i; excess vertex use increments history by history_step per extra owner. Engine accepts `key=value` fields after optional WORK_LIMIT; wrapper exposes `--present-initial`, `--present-step`, `--history-step`. Each is bounded0..64; duplicates, malformed values and unknown engine keys fail before loading routes. Defaults preserve prior behavior. These fields apply to local negotiated repairs, not the separate whole-instance restart schedule or finite candidate generation. Mode presets remain for historical reproducibility; this is the first explicit-config migration, not removal of the entire mode chain.

Spatial prototype selects whole nets by regions, rather than clipping branches.
The selected target is detour-ranked; a seeded random vertex anchors nested
4/8/12 XY boxes spanning all layers. Up to12 touching neighbors ranked by
relaxed-delay excess join the target; region score sums their excess. This
ranking tends to choose large boxes; it is not normalized by group size.
External ownership and all foreign pins remain blocked; existing transaction
snapshots restore failed, expired and nonimproving repairs. Fine-diverse
outperforms this prototype on matched development screens; no strict-window
repair, boundary stitching or unpublished competitor reproduction implemented.
