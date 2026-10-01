# Architecture

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
