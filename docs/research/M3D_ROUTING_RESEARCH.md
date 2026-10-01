# Partcl M3D Routing Challenge: research and CPU-first strategy

Prepared for Kanishk Sama · Research snapshot: October 1, 2026

## Recommendation

Build a CPU-first C++17 router around **exact single-net shortest-path trees, negotiated congestion, and adaptive large-neighborhood search**. Concentrate development on **hard**, then **designs** and **congested**. Once that foundation is competitive, add **small-group conflict-based search** and **joint candidate-tree selection**. Treat GPU acceleration as a later profiling decision.

This is a recommendation supported by the objective, public results, and routing literature—not a claim that an unimplemented method will win. The leading independently generated public entry already uses much of the basic recipe. Beating it will require better coordinated moves, better search allocation, or substantially more efficient exploration.

The strongest distinguishing experiment I would try is **adaptive neighborhood selection with multiple repair methods**: fast sequential repair for most moves, static conflict-based search for small stubborn groups, and a candidate-tree optimizer for larger groups with reusable alternatives. Measure verified delay improvement per CPU-second for each operator.

## What I actually inspected and checked

- Cloned upstream and inspected its README, contribution rules, scoring, legality checker, baseline, negotiated router, grid representation, benchmark manifests, CI workflow, and leaderboard tests.
- Inspected all **11 PR heads** available in the snapshot: ten open and one closed. Read their descriptions, additional method/provenance files, both public issue comments, and the review-comment endpoint. The issues endpoint contained no standalone issues at retrieval.
- Retrieved the list of **18 forks**, inspected default-branch trees for ten relevant forks, and inspected source present in PR #7 and the `sethupathib` fork. This does not amount to searching every branch or every repository on GitHub.
- Ran the unchanged upstream checker against **380 participant route files**, spanning **47 present tier entries** across the 11 PR heads. All 380 checked route files were legal; all 47 present tier entries were complete. This verifies the output routes, not the claimed internal algorithms or runtime histories.
- Calculated single-net-isolation lower bounds for **all 45 released cases** with a separate C++ A* program that blocks foreign pins but ignores other routed nets. Checked two cases with independent vanilla Python Dijkstra. The bounds match the simpler obstacle-free formula on every tier except four delay units in intro.
- Compiled and ran an existing public C++ router on one hard case, then checked its result with the official evaluator.
- Reviewed primary papers and author-maintained repositories for PathFinder, MAPF-LNS/LNS2, conflict-based search, GRIP, CPU parallel routing, radix heaps, GAMER, InstantGR, CUGR, and differentiable global routing. Some works were inspected through their primary abstracts/repositories rather than complete PDFs; these are identified below.

Upstream commit: `499ad7e2a415a97e9ce9b3396b0477e75ebd13e6`. PR commit hashes and the numerical audit appear in the appendices. Public PRs can change after this snapshot. No PR was submitted and no GitHub account was modified.

## 1. What this competition actually optimizes

The model is a rectangular 3D grid, normally six layers, with pins on the two outer layers. Horizontal/vertical movement within layer z costs `layer_delay[z]`; an adjacent-layer via costs `via_delay`. These values come from the instance and must not be hardcoded. Cells are visual/placement objects: their footprints are **not routing blockages**. Foreign pins are blockages.

Each net has a driver and one or more sinks. Its output must be a connected acyclic tree. Different nets cannot share a 3D vertex or edge. A via consumes its two endpoints as well as the vertical edge. Crossings on separate layers are legal.

The objective is:

\[
D=\sum_n\sum_{s\in S_n}d_{T_n}(r_n,s).
\]

For a rooted tree, the equivalent edge expression is:

\[
D_n=\sum_{e\in T_n}w_e k_e,
\]

where `k_e` is the number of sinks downstream of edge e. A trunk used by eight sinks contributes eight times its physical delay, although it occupies the resource only once.

Consequences:

1. **Minimum wirelength is not the objective.** A compact Steiner tree can have unnecessarily long driver-to-sink paths.
2. **There is no circuit critical-path timing model.** No capacitance, slew, buffering, RC loading, or timing propagation between nets is scored. Importing those features would add work without directly helping this objective.
3. **Every sink matters.** Saving one unit on a shared trunk can save several units of score.
4. **Capacity counts distinct nets, not sink paths.** Treating branches of one net as separate capacity consumers would solve the wrong problem.
5. In this model, enforcing exclusive vertex ownership also prevents cross-net edge sharing. The solver can use vertex occupancy as its central resource model, while the final checker still validates everything.

The tier score is:

\[
A=\exp\left(\frac1N\sum_c\log\frac{B_c}{D_c}\right).
\]

Higher is better. All cases in a tier must be legal; otherwise its aggregate is zero. Each case has equal weight in log-score, so prioritize **fractional improvement**, not just raw delay saved. Within one case, minimizing total raw delay is exactly correct.

For allocating search across cases, the log-score benefit of a change is `log(D_old/D_new)/N`. Dividing this by measured compute time gives a useful scheduling signal. Do not combine all six tiers into an invented official overall score: upstream ranks them separately.

### Submission implications

The published mechanism accepts **route JSON files**, not a solver that judges rerun. Language and hardware are unrestricted. Runtime is optional and separate from the delay ranking; I found no fixed solver runtime limit, hidden-test protocol, prize schedule, or deadline in the inspected repository documents. Do not import rules from the earlier macro-placement competition.

This makes an anytime offline optimizer, checkpointing, and per-case best-of-run selection appropriate under the currently published format. Several PRs also use credited public routes as warm starts, but these remain participant submissions rather than an explicit maintainer ruling on every possible reuse policy. Keep independent-from-scratch results and credited warm-start results separate.

Sources: [README](https://github.com/partcleda/eda-3d-routing-challenge/blob/499ad7e2a415a97e9ce9b3396b0477e75ebd13e6/README.md), [rules](https://github.com/partcleda/eda-3d-routing-challenge/blob/499ad7e2a415a97e9ce9b3396b0477e75ebd13e6/CONTRIBUTING.md), [checker](https://github.com/partcleda/eda-3d-routing-challenge/blob/499ad7e2a415a97e9ce9b3396b0477e75ebd13e6/m3d/checker.py), [scorer](https://github.com/partcleda/eda-3d-routing-challenge/blob/499ad7e2a415a97e9ce9b3396b0477e75ebd13e6/m3d/scorer.py).

## 2. What the public competition already tells us

The merged upstream leaderboard still contains only reference entries. Reading it alone badly understates the competitive target. The PRs contain much stronger legal routes.

| PR | Method | Hard aggregate, locally recomputed | What matters |
|---|---|---:|---|
| [#1](https://github.com/partcleda/eda-3d-routing-challenge/pull/1) | `lns_negotiated` | 1.226653 | Rust, negotiation, exact net polishing, blocker-based ruin/recreate |
| [#2](https://github.com/partcleda/eda-3d-routing-challenge/pull/2) | `erikqu_root_aware_portfolio` | 1.274475 | Heuristic/neural candidate selection and local MILP; explicitly reports neural method underperformed on fresh layouts |
| [#3](https://github.com/partcleda/eda-3d-routing-challenge/pull/3) | `pathfinder_lns` | 1.387366 | Best detailed independently generated six-tier entry found; C++17, single-threaded runs, parallel portfolio |
| [#4](https://github.com/partcleda/eda-3d-routing-challenge/pull/4) | `shivaahir158` | 1.050750 | Greedy tree construction, sink-order alternatives, iterative rerouting |
| [#5](https://github.com/partcleda/eda-3d-routing-challenge/pull/5) | `coordinated_refinement` | 1.385765 | Credited refinement of an older PR #3 snapshot; includes bounded conflict search and neighborhood repair |
| [#6](https://github.com/partcleda/eda-3d-routing-challenge/pull/6) | `carter-group-routing` | 1.163739 | Closed PR; coordinated group routing, laptop experiment |
| [#7](https://github.com/partcleda/eda-3d-routing-challenge/pull/7) | `anvesh` | 1.186303 | Public Python SPT/negotiation/LNS implementation present in branch |
| [#8](https://github.com/partcleda/eda-3d-routing-challenge/pull/8) | `drama3d-portfolio` | 1.112073 | Reports GPU sweep routing, GPU LP relaxation, continuous refinement; output trails CPU-led PR #3 |
| [#9](https://github.com/partcleda/eda-3d-routing-challenge/pull/9) | `warm_lns_refinement` | 1.385765 | Credited PR #5 continuation; tiny verified improvements on five cases, no hard-tier gain |
| [#10](https://github.com/partcleda/eda-3d-routing-challenge/pull/10) | `reubalink` | 1.267187 | SPT, fanout scaling, window LNS; description claims its own runs |
| [#11](https://github.com/partcleda/eda-3d-routing-challenge/pull/11) | `mj97` | 1.387394 | Metadata says selection from public portfolios; five tiers present despite six-tier PR claim |

These scores do **not** establish a controlled CPU-versus-GPU comparison. The algorithms and compute budgets differ. They do establish that lack of GPU access is not preventing a very strong entry in the current public field.

PR #3 describes fanout-scaled congestion, exact root-aware A*, single-net optimal rerouting, window/blocker LNS, multistart continuation, and later radix-queue search. Its author reports about 30 core-hours for the hard tier. The actual router source is described as available on request; I did not find it in the PR tree or that fork's default branch. Reading its route output is not equivalent to auditing its implementation.

PR #2 is especially useful negative evidence for a machine-learning-first plan: its own method notes describe fresh-layout validation where the neural variant lost to the heuristic. PR #8 is also evidence against assuming more sophisticated GPU machinery automatically yields better competition scores.

PR #5 and #9 show diminishing returns from repeatedly polishing strong public incumbents. This suggests investing in better neighborhood generation and repair, rather than expecting another ordinary single-net polishing pass to find a large gain.

### Source code you can actually inspect

**Public C++ implementation:** [sethupathib/eda-3d-routing-challenge, cpp/m3d_route.cpp](https://github.com/sethupathib/eda-3d-routing-challenge/blob/22f3c69395f5b933d015b280aa1bdd1d951d291d/cpp/m3d_route.cpp). I inspected its 1,426-line implementation. It includes a JSON reader, driver-rooted Dijkstra, multiple congestion schedules, polishing, pair/group moves, LNS, and case-level threading. It uses materialized adjacency and a binary heap, so it is not the compact A* architecture recommended later.

I compiled it unchanged and ran `hard/case_01`, seed 1, requested search budget 5 seconds. It produced a legal route with delay **9,996** versus baseline **11,938**: ratio **1.1943**. Reported elapsed time was **5.485 seconds**, showing its budget is not a hard deadline. The container's CPU model was AMD EPYC 9V74; this was one serial case, not a laptop benchmark or a full-suite performance claim. PR #3's same case is **8,666**, so the public implementation is a useful starting point, not already the winning implementation.

**Public Python implementation:** [PR #7 `my_router.py`](https://github.com/anveshshekhar/eda-3d-routing-challenge/blob/dfbcba48bd762433350aea82cd653af74e7137ac/my_router.py). Useful for understanding the pipeline. One detail to fix before relying on mathematical claims: its search restricts to a bounding box and expands globally only on failure. A successful restricted search is not automatically globally shortest. Its similarly restricted isolation calculation is not automatically a certified lower bound on arbitrary new layouts. This observation does not invalidate the independently checked route scores.

## 3. Where there is actually room to improve

I computed a lower bound by routing each net independently, retaining foreign pins as obstacles but removing other nets' wires. One rooted shortest-path tree attains that net's minimum sum of sink distances. Adding these independent optima gives a valid lower bound on a whole case, although those trees may conflict with one another.

| Tier | PR #3 score | Optimistic score ceiling from isolation bounds | PR #3 total delay | Isolation lower bound | Maximum possible reduction from PR #3 raw total implied by this bound |
|---|---:|---:|---:|---:|---:|
| intro | 1.150825 | 1.187013 | 342,012 | 329,320 | 3.71% |
| hard | 1.387366 | 1.761668 | 145,097 | 114,031 | 21.41% |
| scale | 1.127225 | 1.162236 | 537,654 | 521,786 | 2.95% |
| stress | 1.091066 | 1.105207 | 1,049,344 | 1,035,918 | 1.28% |
| congested | 1.308329 | 1.646832 | 491,527 | 389,539 | 20.75% |
| designs | 1.432794 | 1.811179 | 209,561 | 164,853 | 21.33% |

**These are bounds, not forecasts.** Much of the remaining gap on contended cases may be unavoidable because isolated shortest trees compete for the same vertices. Neither a 1.76 hard score nor a 20% further delay reduction is promised or known feasible. The last column is based on raw sums; it is not a geometric-mean score improvement percentage.

The evidence still strongly favors hard as the development tier: its largest grid has only 9,600 vertices, yet its tradeoffs are genuinely coupled. Stress has 1,685,400 vertices but comparatively little remaining quality headroom. Use stress mainly to test scaling after the algorithm works.

For focused experiments, hard/case_02, hard/case_06–08, and designs/int2float have larger isolation gaps. Do not tune only these: maintain performance on every case and evaluate a small held-out set of freshly generated layouts separately.

### A useful exact obstacle-free distance

For points u and t, let `m = |x_u-x_t| + |y_u-y_t|`. With uniform within-layer costs and constant via delay v:

\[
h(u,t)=\min_{0\le z<L}\left[m\,d_z+v\left(|z_u-z|+|z_t-z|\right)\right].
\]

This is the exact distance with no obstacles. To see why, take the cheapest layer visited by any proposed path: all its horizontal movement costs at least m times that layer's cost, and its vertical movement must reach that layer and the destination. Conversely, traveling vertically to the chosen layer, horizontally there, then vertically to the destination realizes the expression.

It is therefore an admissible, consistent A* heuristic when obstacles are added and physical edge weights are unchanged or increased by nonnegative penalties. Evaluate all layers; choosing the middle unconditionally is wrong for short same-die routes. For the common `[6,4,2,2,4,6]` profile and via cost 3, an outer-layer route costs `6m`, while a route via layer 2 on the same die costs `2m+12`. The latter is beneficial when `m>3`; congestion can change the preferred choice.

For the released suite the pin-aware lower bound matched the obstacle-free sum except intro, where foreign pins added four units. That is a measured property of these cases, not a general guarantee.

## 4. The router I would build

### A. Exact single-net kernel

Start with one **driver-rooted Dijkstra**, stop after every sink is settled, and extract the union of predecessor paths to the sinks. Positive edge costs make the predecessor structure acyclic. Remove irrelevant nonterminal leaves.

With other nets fixed as obstacles, this minimizes every sink distance simultaneously, hence their sum. This claim is exact because the objective is additive and the net has no internal resource-capacity limit. It would not automatically hold for RC timing or minimum-wirelength objectives.

Then implement the faster equivalent using sequential A* attachments. Seed the existing tree at each vertex's **distance from the driver**, not zero. If every existing root path is shortest under the same static edge weights, this preserves the shortest-path property. Test against full Dijkstra before making it the default. Preserve the same weights during an exact call; changing penalties midconstruction changes the problem.

Use physical delays for exact polishing. Negotiation can use heuristic penalties, but a penalized shortest-path tree is not necessarily a physical-delay-optimal tree.

### B. Initial legal construction

On sparse cases, try hard-capacity greedy routing with several orders: fanout, distance, estimated blockage/regret, and seeded randomized orders. On contended cases, use PathFinder-style negotiation: temporarily permit non-pin resource conflicts, raise present/history prices, and reroute affected nets until legal.

A starting heuristic to ablate is:

`cost_n(u,v) = physical_delay(u,v) + alpha_n * (history[v] + pressure * other_net_occupancy[v])`

with `alpha_n = fanout_n^(-beta)`, initially trying beta in `{0, 0.5, 1}`. This is a heuristic, not an exact derivation: it lets high-fanout trunks resist displacement. PR #3 uses related fanout scaling. Track each net once per occupied vertex, even if multiple sinks share the vertex.

Avoid treating one congestion schedule as universally best. Try slow versus faster pressure growth, plateau-triggered history decay, and bounded/restarted negotiation. Preserve the best legal state separately. A failed routing attempt is not proof an instance is infeasible; the released references establish feasibility.

### C. Exact coordinate descent

After legalization, repeatedly remove one entire net, recompute its physical shortest-path tree with every other net fixed, and keep a better route. Stop a pass when no strict improvements remain. Order candidate nets by excess delay above their isolation bound, but periodically revisit all affected nets.

This establishes a meaningful local optimum. It does not solve mutually blocking nets: sometimes one route must worsen temporarily to allow a larger improvement elsewhere.

Equal-delay alternatives matter. Different shortest trees consume different vertices. Explore tie-breaks that prefer fewer occupied vertices, avoid scarce pin-escape regions, or introduce reproducible randomized diversity. Minimizing hop count independently to each sink does not prove minimum total tree footprint; use actual occupied-vertex count when comparing complete alternatives. Use lexicographic priorities rather than arbitrary floating epsilon additions if exact delay ordering matters.

### D. Adaptive large-neighborhood search

Maintain the current legal solution, best-ever legal solution, a small archive of geometrically diverse incumbents, and operator statistics. For each move:

1. Select a seed net with high excess delay or recent failed improvement attempts.
2. Compute a promising route with some neighboring routes temporarily ignored.
3. Identify the actual blocking nets, including short low-cost nets that could cheaply yield a corridor.
4. Expand a small group using blockers, a spatial window, a common layer bottleneck, or a randomized conflict-graph walk.
5. Remove the group, keep outside nets fixed, repair, and run exact polish inside the group.
6. Commit legal improvements; optionally allow bounded worsening in a separate search trajectory while retaining the best-ever state.

Try neighborhood sizes such as 2, 4, 8, 16 and occasionally 32; these are experimental settings, not proven optima. Pure random groups are a useful baseline, but blocker groups directly target why a route is long. Avoid making group selection solely proportional to net size: a small blocking route can unlock a large gain.

Adapt operator selection to **verified gain per CPU-second**, with exploration retained for operators that have not been tried much. Stagnation should trigger larger/different neighborhoods or a different incumbent, not just endlessly more identical iterations.

## 5. The most promising extensions beyond the basic public recipe

### First extension: static conflict-based search for small groups

This is my highest-priority exact repair experiment, though bounded conflict-based group repair is already mentioned in PR #5. The opportunity is a better implementation and integration, not claiming the idea is entirely new.

With outside nets fixed, initially compute each group's independently optimal tree. If nets a and b both occupy vertex q, every legal repair must exclude q from a or exclude q from b. Create those two branches, recompute only the constrained net, and explore the branch with the lowest sum of exact single-net costs first. Cache repeated net/forbidden-vertex states and prune nodes that cannot beat the incumbent group cost.

This adapts CBS from multi-agent pathfinding, but the semantics must change: these are **permanent spatial exclusions**, not conflicts at a time step. There is no waiting or time-expanded graph, and the low-level object is a multi-sink tree rather than a single moving-agent path.

Because an exact SPT is an exact low-level solver for this objective, unrestricted best-first CBS on the finite graph can certify a selected group's optimum with outside nets fixed. Practical node/time caps turn it into an anytime repair; a timed-out run proves no optimum. Restricted corridors only certify results within those corridors. Use two-net and small-group experiments first; full-instance CBS can explode combinatorially.

A useful refinement is to branch on conflicts whose two exclusions both raise the corresponding exact net cost. These are more informative than conflicts that disappear under a free equal-delay alternative. Measure the extra low-level search overhead before enabling this broadly.

### Second extension: candidate-tree selection with CP-SAT or MIP

Save diverse legal-within-net trees produced during search, including promising trees from globally conflicting states. For a chosen group, let `x[n,k]` choose candidate k for net n:

\[
\min\sum_{n,k}D_{nk}x_{nk},\quad
\sum_kx_{nk}=1,\quad
\sum_{n,k:v\in T_{nk}}x_{nk}\le1.
\]

Filter candidates that conflict with frozen outside routes or foreign pins. Each candidate must already be an acyclic tree spanning its pins. Include every incumbent route so that the restricted problem remains feasible. The candidate cost is its exact summed driver-to-sink delay, not wirelength.

This lets several nets switch jointly and can exploit complementary moves generated by different workers. Boolean candidate selection fits OR-Tools CP-SAT; HiGHS is an alternative for a mixed-integer model. Start with roughly 4–12 nets and 8–32 diverse candidates each, then tune from measured model size and success.

A solved candidate model is optimal **only over its candidate pool**. Even the restricted pool's LP optimum is not automatically a lower bound for the unrestricted routing problem. Full column-generation guarantees require correct pricing or another proof. Resource-price-guided candidate generation is useful heuristically without pretending it supplies such a certificate.

### Third extension: local vertex-ownership/flow MILP

For a small bottleneck group, binary variable `y[n,v]` assigns vertex v to net n. Let continuous nonnegative directed flow `f[n,u,v]` deliver one unit to each sink. Net n with K sinks supplies K units at its driver. Impose:

- flow conservation: supply K at the root, demand 1 at each sink, zero elsewhere;
- `sum_n y[n,v] <= 1`;
- `f[n,u,v] <= K*y[n,u]` and `f[n,u,v] <= K*y[n,v]`;
- required pins assigned to their own nets, foreign pins/frozen outside vertices unavailable;
- objective `sum physical_delay(u,v)*f[n,u,v]`.

The important modeling distinction is that vertex capacity is per net while delay is per flow unit. Shared trunks carry several flow units but have one owner.

Under this challenge's positive additive costs, a solution can be converted into one shortest-path tree inside each net's assigned vertices without increasing its objective: flow decomposes into root-to-sink deliveries plus removable cycles, and each sink's shortest assigned-vertex path is no longer than its delivered-flow average. Conversely, any legal tree gives a feasible flow by sending downstream-sink counts through its edges. Thus this ownership formulation can represent the correct group optimum, with tree extraction performed afterward. This equivalence is my model-based reasoning, not a tested competition solver result.

Use a mixed-integer solver supporting continuous flow, such as HiGHS. CP-SAT would need an integer-flow formulation. Avoid a full stress-grid MILP. Include incumbent corridors, broaden if stalled, and report restricted-domain optimality honestly. PR #2 already reports a related six-net local MILP saving ten delay units, so this is a selective repair method rather than evidence of a likely huge gain.

### Additional hypotheses worth controlled experiments

- **Trunk-aware priority:** downstream sink count is the actual marginal value of an edge. Use it to select trunk repairs and identify cheaply displaced competitors. Net fanout alone is a coarse approximation.
- **Regret-based allocation:** estimate how much each net loses if denied a bottleneck. Give scarce vertices to routes with expensive alternatives, not simply the longest net.
- **Pin-escape scarcity:** nets with few usable initial escape directions can benefit from early attention or local resource prices.
- **Short-path DAG compaction:** choose among equal-delay predecessor edges to reduce footprint or avoid costly regions while preserving exact distances.
- **Cross-incumbent recombination:** collect candidate trees from diverse complete solutions and solve compatible combinations; do not blindly union routes from different solutions.
- **Safe corridor pruning:** if a candidate driver-to-sink path must cost at most U, vertices with `h(driver,v)+h(v,sink)>U` can be excluded from that path. Derive U from a valid incumbent and lower bounds, not an arbitrary geometric box. Multi-sink trees require care because different branches serve different sinks.

## 6. How to make it fast without a GPU

The hard tier is small enough to support aggressive CPU exploration. The largest stress grid is large enough that implementation choices dominate. Make speed buy more candidate moves and better final scores.

| Change | Why it helps here | Main caution |
|---|---|---|
| C++17 compiled core, Python orchestration | Removes interpreter/dictionary overhead from repeated graph searches | Do not rewrite the independent Python checker |
| Packed vertex IDs and dense arrays | Predictable memory access for regular grids | Reset only touched entries or use generation stamps |
| Implicit six-neighbor graph | Avoids storing millions of adjacency objects | Benchmark coordinate arithmetic versus compact lookup tables |
| Layer-aware A* heuristic | Strong lower bound; avoids broad Dijkstra exploration on sparse long routes | Keep heuristic admissible for the actual search cost |
| Radix/bucket queues where appropriate | Physical costs are positive integers | Radix A* requires monotone keys; restart the queue when goals/heuristics change |
| Integer physical distances, 64-bit total scores | Exact comparisons and scoring consistency | Prove bounds before using smaller numeric types |
| Region-first search with certified/global fallback | Limits expansions on local repairs | A found route in a small box is not proof of global shortestness |
| Reuse scratch buffers; avoid per-node allocation | Many thousands of small searches | Account for each worker's private memory |
| Independent cases and multistart workers | Simple CPU parallelism with little synchronization | Report wall time and total CPU work separately |
| Incremental route/occupancy updates | Avoids reconstructing the whole state after every accepted move | Final files still go through the official checker |

A 32-bit array over stress's 1,685,400 vertices costs about **6.74 MB** in decimal units. Several arrays, queues, saved routes, and multiple workers add up. This is much more manageable than Python objects per graph element, but worker count should be selected from measured peak memory, not blindly set to all logical cores.

Start with one worker per physical core only if memory and CPU quotas permit. On a small laptop, fewer workers can be more productive than oversubscribing. Independent seed portfolios are easier than concurrent mutation of one occupancy map. Later, spatially separated neighborhood repairs can run concurrently if their resource domains are provably disjoint or proposals are rechecked before commit.

Use a binary heap first. Introduce radix queues after a profile identifies queue operations as a bottleneck and correctness has been compared against Dijkstra. Avoid caching enormous all-pairs distance tables: the small-layer analytic heuristic is cheap, and occupancy changes between searches.

### When GPU access would become useful

GAMER-style sweeps and InstantGR demonstrate that GPU acceleration can help large maze-routing workloads. Consider this only after profiling shows that batched shortest-path work dominates, there is enough regular parallel work to fill the device, and host/device movement does not dominate.

The current hard-tier search is small, irregular, and full of adaptive decisions. A GPU is not a prerequisite for C++ A*, local CBS, candidate CP-SAT, or local MILP. More CPU search throughput and better search moves are the first investment. No GPU purchase or rental is needed to start this plan.

## 7. Research reading list, ranked by usefulness

| Source | What transfers to this challenge | Limitation |
|---|---|---|
| [PathFinder — McMurchie and Ebeling, FPGA 1995](https://janders.eecg.utoronto.ca/1387_2015/readings/pathfinder.pdf) | Present/history congestion prices; resource negotiation; delay-aware tree seeds | Original timing-criticality objective differs from this sum-of-sinks objective |
| [Anytime MAPF via LNS — Li et al., IJCAI 2021](https://www.ijcai.org/proceedings/2021/0568.pdf) | Delay/blocker neighborhoods, adaptive operator selection, fast prioritized repair | MAPF has time; this routing has permanent spatial ownership |
| [MAPF-LNS2 — Li et al., AAAI 2022](https://ojs.aaai.org/index.php/AAAI/article/view/21266) and [code](https://github.com/Jiaoyang-Li/MAPF-LNS2) | Repair conflicts by repeatedly replanning selected groups | Use the ideas with a custom tree kernel; not a drop-in executable |
| [Conflict-Based Search — Sharon et al., AAAI 2012](https://ojs.aaai.org/index.php/AAAI/article/view/8140/7998), [2015 journal record](https://digitalcommons.du.edu/computer_science_faculty/7/) | Split a shared-resource conflict into exclusion constraints, use exact low-level costs | Apply to small groups; tree-based static adaptation is required |
| [GRIP — Wu, Davoodi, Linderoth, DAC 2009](https://jlinderoth.github.io/papers/Wu-Davoodi-Linderoth-09.pdf), [journal preprint](https://jlinderoth.github.io/papers/Wu-Davoodi-Linderoth-10-PP.pdf) | Candidate route selection, resource prices, region decomposition | Original wire/via objective and edge capacities must be replaced |
| [CPU parallel FPGA routing — Zang et al., GLSVLSI 2024](https://arxiv.org/html/2407.00009v1), [code](https://github.com/xszang/parallel-routing) | Spatial scheduling and adaptive congestion updates | FPGA resource graph and reported speedups are not this benchmark |
| [Faster Algorithms for the Shortest Path Problem — Ahuja et al., JACM 1990](https://www.princeton.edu/~alaink/Orf467F11/AhujaRadixHeap.pdf) | Radix-heap shortest-path implementation | Integer-key and monotonicity requirements matter |
| [GAMER — Lin et al., TCAD 2023, primary abstract](https://research.cuhk.edu.hk/en/publications/gamer-gpu-accelerated-maze-routing-3/) | Sweep-based GPU maze routing if needed later | Speeds up search; does not by itself improve neighborhood choices |
| [InstantGR — ICCAD 2024 paper](https://shijulin.github.io/files/1239_Final_Manuscript.pdf), [code](https://github.com/cuhk-eda/InstantGR) | GPU routing organization and parallel processing | Higher integration burden; evaluate after a CPU baseline |
| [CUGR](https://github.com/cuhk-eda/cu-gr), [CUGR2](https://github.com/cuhk-eda/cu-gr-2) | Mature routing architecture and pattern/maze concepts | Detailed-routability model and objectives differ; not plug-and-play |
| [NVIDIA Differentiable Global Router](https://github.com/NVlabs/Differentiable-Global-Router) | Continuous candidate-pattern optimization as an optional experiment | Dependencies and CUGR2 integration; relaxed solutions still need legalization |

The LNS paper contains a particularly relevant caution: faster prioritized repair often outperformed expensive exact repair in its tested anytime setting because it explored more neighborhoods. Therefore use CBS/MIP selectively, and measure the whole optimizer's progress, not just the quality of one repair. This is evidence from a related problem, not a measured result on M3D.

For solver APIs, consult [OR-Tools CP-SAT](https://developers.google.com/optimization/cp/cp_solver) and [HiGHS](https://highs.dev/). Candidate selection is a natural integer model; the ownership formulation mixes binary and continuous variables.

I would not start by integrating a full production global/detailed router, a reinforcement-learning policy, a neural net that predicts complete routes, or a full-grid MILP. Those directions face objective mismatch, legalization work, training burden, or combinatorial size before they improve the actual score.

## 8. Concrete build and experiment plan

### Milestone 1 — correct, measurable CPU foundation

Pin upstream; import all cases; implement exact scoring in the router and compare with the unchanged official checker. Build the isolation lower-bound table. Either adapt the inspected C++ fork with attribution or implement a compact core using the upstream model as reference. Keep solver development separate from the route-only submission branch.

Acceptance: legal routes on every hard case, no discrepancy with official delay calculations, measured time/memory, deterministic seeded runs where possible, and persistent best-route checkpoints.

### Milestone 2 — establish a strong ordinary heuristic

Add root-aware A*, multiple initial orders, fanout-scaled negotiation, physical-delay polishing, blocker/window LNS, plateau tie moves, and independent starts. Keep a small diversity archive instead of restarting every worker from the exact same incumbent.

Acceptance: a repeatable gain over the reference and the public starting implementation at matched CPU budgets. Compare each case to PR #3. Do not mistake beating 1.0 for beating the competition.

### Milestone 3 — test the distinctive repair methods

Add small-group CBS, then candidate-tree CP-SAT. Record gains by operator and neighborhood size. If neither improves delay per CPU-hour over ordinary LNS, disable it rather than preserving complexity for its own sake. Test ownership-flow MILP only on bottlenecks where those methods stall.

Acceptance: a measured advantage on repeated runs across hard and at least one design/congested case. Keep separate score tables for generated-from-scratch and publicly warm-started runs.

### Milestone 4 — expand compute and finalize output

Tune sparse tiers for throughput; run designs/congested at useful budgets; test stress once memory/search scaling is ready. Continue promising incumbents, allocate time using fractional gain per second, independently validate every final route, then generate the leaderboard and submission files.

### Ablations worth running

| Experiment | Controlled comparison | What it answers |
|---|---|---|
| Root-aware kernel | Baseline zero-seeded attachment versus exact SPT | Is objective alignment delivering the expected improvement? |
| A* | Same obstacles/ties, Dijkstra versus analytic A* | Does speed improve without changing exact cost? |
| Fanout scaling | beta 0, 0.5, 1 at equal budgets | Does scarce-layer allocation improve? |
| Neighborhoods | Random, spatial, blockers, adaptive mix | Are selected groups actually useful? |
| Repair | Sequential, local negotiation, capped CBS, candidate selection | Which yields more score gain per CPU-second? |
| Tie handling | Strict improvements only versus equal-delay diversity | Are plateaus blocking progress? |
| Parallel policy | Independent seeds versus occasional incumbent sharing | Does sharing help or destroy diversity? |
| Generalization | Released cases versus fresh generated cases | Is the improvement structural or narrowly tuned? |

For an initial screening pass, use small equal budgets such as 10, 60, and 300 seconds per hard case, with three to five seeds. These are experiment suggestions, not competition limits. Continue only the promising variants at longer budgets.

Log: repository/solver commit, case hash, seed, configuration, legal status, exact delay, lower bound, wall time, total CPU work, peak memory, number of search expansions, operator attempts/successes, and provenance of every warm start. Runtime measurements from different machines and portfolios are not directly comparable.

## 9. Submission traps and interpretation limits

**CI frontier bug.** At the pinned upstream commit, `tests/test_leaderboard.py` requires the hard-tier Pareto set to equal exactly the two reference entries. A new competitive submission with runtime data can change that set and fail the test despite legal routes. PR #4's comment confirms this failure; PR #3 omits hard-tier runtime data for this reason. Optional runtime omission is supported by the documented format; keep honest measurements in your own results. A proper fix belongs in a separate toolkit PR. Do not alter tests inside a route submission.

**PR path guard.** If a PR touches submissions, current CI only allows `submissions/**` and `LEADERBOARD.md`. Source files should live in a separate solver branch/repository. PR #7's head includes source outside those paths, so its legal output should not be confused with guaranteed submission-CI acceptance.

**PR #11 coverage.** Its description says six tiers and reports stress, but the inspected head has no `submissions/stress/` entry. Its five present tiers are complete and legal. Its method metadata identifies public-portfolio selection, so it is not evidence of a new from-scratch solver.

**No checker gaming.** Optimize valid route geometry and retain the independent evaluator. A parser loophole or malformed tree is not a robust routing result.

**No unearned optimality claims.** Exact one-net rerouting is conditional on fixed outside routes and unrestricted/certified search. Exact group optimization is conditional on the frozen outside. Candidate-pool and corridor optima have additional restrictions. Isolation lower bounds deliberately ignore conflicts.

**No invented hardware requirements.** The repository accepts CPU outputs. The strongest described public approach already uses CPU search. GPU availability is a later engineering choice, not a gate to starting.

## 10. My proposed first implementation decision

Use **C++17 for routing and Python for experiments and verification**. Start with hard-tier exact SPT + negotiation + blocker LNS. Keep the inspected public C++ router as a comparison implementation. Once the new core can match ordinary LNS at equal CPU budgets, add **two-net/small-group static CBS** and **candidate-tree recombination**.

The most valuable innovation is likely deciding **which routes should move together and how to redistribute the cheap middle-layer vertices**, while keeping the shortest-path engine cheap enough to try many alternatives. The current evidence does not support spending the first phase on GPU infrastructure or neural training.

---

## Appendix A. Recomputed public PR scores

The following tables are generated from the local unchanged-checker audit. A dash means that tier was absent, not that its present route files were illegal. Scores are rounded to six decimal places. Every present entry shown below passed legality and completeness for its tier.

| PR | intro | hard | scale | stress | congested | designs |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 1.093744 | 1.226653 | 1.068219 | 1.066889 | 1.098148 | 1.253282 |
| 2 | — | 1.274475 | — | — | — | — |
| 3 | 1.150825 | 1.387366 | 1.127225 | 1.091066 | 1.308329 | 1.432794 |
| 4 | 1.027406 | 1.050750 | 1.010842 | — | 1.054867 | 1.059295 |
| 5 | 1.149519 | 1.385765 | 1.124838 | 1.090630 | 1.304213 | 1.425696 |
| 6 | — | 1.163739 | — | — | — | — |
| 7 | 1.106895 | 1.186303 | 1.082092 | — | — | 1.252049 |
| 8 | 1.083010 | 1.112073 | 1.040909 | 1.020123 | 1.016038 | 1.136909 |
| 9 | 1.149532 | 1.385765 | 1.124846 | 1.090632 | 1.304324 | 1.425696 |
| 10 | — | 1.267187 | — | — | — | — |
| 11 | 1.150878 | 1.387394 | 1.127225 | — | 1.308329 | 1.432794 |

## Appendix B. Per-case lower bounds and leading independent entry

PR #3 is used as the consistent six-tier comparator. Lower bounds include foreign-pin obstacles and ignore other nets’ routed wires. The difference is not necessarily recoverable.

| Tier / case | Baseline delay | PR #3 delay | Isolation lower bound | PR #3 excess |
|---|---:|---:|---:|---:|
| intro/case_01 | 240 | 206 | 206 | 0 |
| intro/case_02 | 1,190 | 1,030 | 1,006 | 24 |
| intro/case_03 | 1,757 | 1,611 | 1,595 | 16 |
| intro/case_04 | 2,162 | 1,980 | 1,936 | 44 |
| intro/case_05 | 4,197 | 3,687 | 3,563 | 124 |
| intro/case_06 | 6,155 | 5,189 | 5,023 | 166 |
| intro/case_07 | 5,855 | 5,267 | 5,087 | 180 |
| intro/case_08 | 8,549 | 7,487 | 7,249 | 238 |
| intro/case_09 | 9,728 | 8,144 | 7,972 | 172 |
| intro/case_10 | 11,969 | 10,551 | 10,205 | 346 |
| intro/case_11 | 14,142 | 12,200 | 11,868 | 332 |
| intro/case_12 | 18,509 | 16,093 | 15,647 | 446 |
| intro/case_13 | 22,599 | 19,593 | 18,837 | 756 |
| intro/case_14 | 24,481 | 21,197 | 20,489 | 708 |
| intro/case_15 | 27,648 | 23,938 | 23,002 | 936 |
| intro/case_16 | 37,902 | 32,866 | 31,526 | 1,340 |
| intro/case_17 | 49,554 | 41,622 | 39,678 | 1,944 |
| intro/case_18 | 53,805 | 44,601 | 42,739 | 1,862 |
| intro/case_19 | 45,488 | 40,024 | 38,512 | 1,512 |
| intro/case_20 | 51,660 | 44,726 | 43,180 | 1,546 |
| hard/case_01 | 11,938 | 8,666 | 7,156 | 1,510 |
| hard/case_02 | 18,910 | 13,156 | 9,976 | 3,180 |
| hard/case_03 | 14,724 | 11,074 | 8,744 | 2,330 |
| hard/case_04 | 18,077 | 13,059 | 10,253 | 2,806 |
| hard/case_05 | 21,051 | 15,211 | 12,129 | 3,082 |
| hard/case_06 | 27,134 | 19,786 | 15,332 | 4,454 |
| hard/case_07 | 31,341 | 21,295 | 16,461 | 4,834 |
| hard/case_08 | 30,886 | 21,432 | 16,576 | 4,856 |
| hard/case_09 | 27,802 | 21,418 | 17,404 | 4,014 |
| scale/case_01 | 45,088 | 39,308 | 38,066 | 1,242 |
| scale/case_02 | 51,828 | 45,458 | 43,786 | 1,672 |
| scale/case_03 | 62,452 | 56,440 | 54,966 | 1,474 |
| scale/case_04 | 66,106 | 57,086 | 55,030 | 2,056 |
| scale/case_05 | 74,371 | 66,215 | 64,295 | 1,920 |
| scale/case_06 | 86,553 | 78,155 | 75,995 | 2,160 |
| scale/case_07 | 96,835 | 86,427 | 84,503 | 1,924 |
| scale/case_08 | 121,175 | 108,565 | 105,145 | 3,420 |
| stress/case_01 | 1,144,904 | 1,049,344 | 1,035,918 | 13,426 |
| congested/case_01 | 71,049 | 54,077 | 43,171 | 10,906 |
| congested/case_02 | 122,534 | 95,660 | 76,758 | 18,902 |
| congested/case_03 | 216,835 | 164,165 | 128,571 | 35,594 |
| congested/case_04 | 234,127 | 177,625 | 141,039 | 36,586 |
| designs/ctrl | 73,148 | 50,026 | 40,580 | 9,446 |
| designs/int2float | 152,284 | 90,634 | 69,186 | 21,448 |
| designs/router | 82,491 | 68,901 | 55,087 | 13,814 |

## Appendix C. Exact PR snapshots

Each source was inspected at the head below. This table distinguishes the report’s fixed snapshot from mutable PR descriptions.

| PR | State at retrieval | Head commit |
|---|---|---|
| [1](https://github.com/partcleda/eda-3d-routing-challenge/pull/1) | open | `5b5be704578623c0430fedbd8d3c382d8b90caed` |
| [2](https://github.com/partcleda/eda-3d-routing-challenge/pull/2) | open | `607bb91f497a105942ce6ed14e01fb39150036d3` |
| [3](https://github.com/partcleda/eda-3d-routing-challenge/pull/3) | open | `4e21227867ee1f8f72c9f4d9ad446e05c20fe452` |
| [4](https://github.com/partcleda/eda-3d-routing-challenge/pull/4) | open | `cd057ed79c2f91b0da1ab173b1d106ea28c39651` |
| [5](https://github.com/partcleda/eda-3d-routing-challenge/pull/5) | open | `4533580ce9a84b83c9c80b831d92f2fbac2bdac9` |
| [6](https://github.com/partcleda/eda-3d-routing-challenge/pull/6) | closed | `bc8a8a942eb4dca9f06bb58585667a9a91c92af1` |
| [7](https://github.com/partcleda/eda-3d-routing-challenge/pull/7) | open | `dfbcba48bd762433350aea82cd653af74e7137ac` |
| [8](https://github.com/partcleda/eda-3d-routing-challenge/pull/8) | open | `e2a01b990f3044f0650697ef4e963c579d107126` |
| [9](https://github.com/partcleda/eda-3d-routing-challenge/pull/9) | open | `06eab75bb49c07c050f9b6720157b844f9a5a56c` |
| [10](https://github.com/partcleda/eda-3d-routing-challenge/pull/10) | open | `ca3cb1de2c046546f2ed8fca14576f6056b8488d` |
| [11](https://github.com/partcleda/eda-3d-routing-challenge/pull/11) | open | `93b6c420ef38b6a0294e8bf9727eb60dc4d89d62` |

## Appendix D. Reproducing the audit and bounds

To retrieve a PR without merging or changing upstream, fetch its head into a local research ref:

```bash
git fetch origin refs/pull/3/head:refs/remotes/origin/pr/3
```

For each submission directory at that pinned ref, score its files against canonical upstream instances using `m3d.checker.check`, then aggregate `baseline_total / total_delay` with `m3d.scorer.leaderboard`. Do not trust the submitted leaderboard numbers. Count required cases from the tier manifest, which also avoids the README’s generic “20 cases” wording being misapplied to other tiers.

The audit enumerated participant `submissions/<tier>/<method>/*.sol.json` files in each PR tree, excluding seeded reference methods; loaded every file with `Submission.load`; matched the canonical instance; called `check`; tested all-case completeness against the manifest; and recomputed each geometric mean. Total: 380 files, 47 present complete tier entries.

For the lower bound, perform this calculation for every canonical case:

```text
total = 0
for net in instance.nets:
    block the pins belonging to every other net
    ignore every routed wire, including reference routes
    for sink in net.sinks:
        total += exact_shortest_path_cost(net.driver, sink)
```

A shared shortest-path predecessor tree attains these sink distances simultaneously for an isolated net, so summing individual paths does not impose an infeasible within-net requirement. The implementation used the analytic layer-aware heuristic, six implicit neighbors, integer distances, and no bounding-box restriction. Independent vanilla Dijkstra agreed on intro/case_01 (206) and hard/case_01 (7,156). These checks support the calculation but do not constitute a formal verification of the analysis program.

The public C++ smoke experiment used source at `22f3c69395f5b933d015b280aa1bdd1d951d291d`:

```bash
g++ -O3 -std=c++17 -pthread cpp/m3d_route.cpp -o m3d_route
./m3d_route --case benchmarks_hard/case_01.json --out sample --seconds 5 --seed 1
python -m m3d.cli evaluate --case benchmarks_hard/case_01.json --sol sample/case_01.sol.json --suite benchmarks_hard
```

The measured 9,996-delay result is a single run and its time-budgeted search can vary with machine load. I did not run a new competitive optimizer or claim a new leaderboard result.
