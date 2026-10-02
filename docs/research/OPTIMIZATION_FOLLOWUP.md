# Alternative optimization research — October 1, 2026

## Reubalink source/output inspection

Inspected THOMACHAYAN/eda-3d-routing-challenge branches main and reubalink-hard,
submission PR10, metadata, and commit history. No custom solver source was found
in either branch; the submission changes only leaderboard/route JSON/metadata.
Do not mistake the inherited m3d/negotiated.py baseline for their custom solver.
No separate public routing repository was found in the author's repository list.
Method details are author reports, not inspected implementation behavior.

Sources:
- https://github.com/THOMACHAYAN/eda-3d-routing-challenge/blob/d9cddc4cc365290f4c6f4d1752f460c46e03ddbe/submissions/hard/reubalink/meta.json
- https://github.com/THOMACHAYAN/eda-3d-routing-challenge/commit/d9cddc4cc365290f4c6f4d1752f460c46e03ddbe
- https://github.com/THOMACHAYAN/eda-3d-routing-challenge/commit/ca3cb1de2c046546f2ed8fca14576f6056b8488d
- https://github.com/partcleda/eda-3d-routing-challenge/pull/10

Reported progression: detour-ranked LNS from official negotiated_x2 reference
1.0511→1.1503; conflict-based pair search reaches about1.2049; gradient-boosted
ranking of groups skipped by pair search reaches1.2060; shortest-path trees,
fanout-priced negotiation, exact per-net rerouting and window LNS reach1.2672;
negotiated repair inside ripped windows reaches1.3622. Final commit explicitly
says it started from five-hour routes; total final generation/runtime/hardware
are not provided. These are not controlled ablations and do not prove that any
one operator caused an observed increment. No training implementation or window
sizes, boundary rules, acceptance policy or exact negotiation schedule available.

Downloaded only the two final published route revisions, pinned by full SHA.
Original dev/inspect_reubalink.py independently reloads/checks/scores all18
outputs using our immutable official archive. Observed aggregates:
ca3cb1d1.2671868111635183,total159369;
d9cddc4c1.362234270749783,total147825;both9/9legal.
All9 cases improve between revisions. Final routes collectively use1370 fewer
net vertices/edges and385 fewer vias. This does not establish minimizing resource
use as a reliable score surrogate; the coordinated physical objective improved.
Case/input/output hashes and checker results in reubalink-inspection.json.
No competitor code executed/copied; no public route used as a warm start.

Comparison to our recorded GitHub-best1.2306575756801885:
434 one-sink nets total ours35071 versus theirs36257;
315 multiple-sink nets total ours129474 versus theirs111568.
Signed overall gap16720, multi-sink gap17906, one-sink advantage1186.
This is an artifact/objective comparison, not matched runtime or a fresh
reproduction of our unavailable GitHub-best raw routes. It supports further
multi-sink/topology experiments without proving a global packing explanation.

Recommended next original experiment: spatially selected neighborhoods using
our own incumbent and relaxed net bounds. Sample XY boxes of width4/8/12
across all layers; rank boxes by detour of touching multi-sink nets. These sizes
are proposed screens, not recovered competitor settings. Select a bounded
number of nets touching a box, release their complete trees, and reuse our
transactional fine-price/tight-A* negotiated repair with external nets/pins
fixed. Full-net rebuilding avoids ambiguous boundary reconnection in the first
prototype; it is spatial neighborhood selection, not a claim to reproduce
strict within-window repair. Preserve the previous legal incumbent on failure
or nonimprovement; exact polish can follow legal rebuilding.

Compare fine control, fine-diverse blocker groups, and spatial groups on declared
hard01/04/07,seeds1–3,matched5M and20M expansion caps with60s safety ceiling,
same frozen starts and2/1/1 schedule. Report legal delay/gain, failure and
nonimproving counts, expansions, actual CPU/wall time, group size and all
regressions. Do not use public route geometry or per-net gaps to select our
case-specific neighborhoods. Reserve08/09 for subsequent fixed-config validation.
Only after this prototype has evidence consider strict-window repair retaining
outside branches: every cut boundary component/terminal and downstream sink
weight must be accounted for, and reconnections must remain acyclic. Keep
whole-window rejection/rollback and official physical scoring.

Second hypothesis: a congestion-aware component-merging tree constructor with
unit sink weights and once-per-net vertex prices could supply more compact
shared trunks to spatial repair. Earlier greedy treecost rejection does not
evaluate that full construction. ML ordering is lower priority: the author's
reported ML increment is small and confounded, and no training data/model is
published. No new algorithm implementation, gains, tests or score from this
research session.

Goal: escape routing geometry inherited from the official baseline and improve hard-tier delay. Literature is a source of hypotheses, not evidence of gains on this challenge.

## Primary sources inspected

- [PathFinder, McMurchie/Ebeling](https://janders.eecg.utoronto.ca/1387_2015/readings/pathfinder.pdf): negotiation permits temporary resource conflicts and uses present/history costs. Transfer the conflict-resolution mechanism; this challenge sums all sink delays rather than timing critical paths. Our group negotiation is already related to this established approach; no novelty claim.
- [SALT, Chen/Tu/Young, ICCAD 2017](https://www.cse.cuhk.edu.hk/~fyyoung/paper/ICCAD17_SALT.pdf) and [author repository](https://github.com/chengengjie/salt): trade root path length against total tree weight. Hypothesis here: slightly worse individual paths may free capacity and lower other nets' delay. Not a drop-in exact optimizer: our 3D layer costs, fixed obstacles and multi-net ownership matter. No SALT code copied or executed.
- [MAPF-LNS2, AAAI 2022](https://ojs.aaai.org/index.php/AAAI/article/view/21266): select conflicting subsets and repair them. Transfer neighborhood selection only. Static routing forbids shared vertices altogether; time-step collision rules do not apply.
- [Chuzhoy/Kim/Nimavat, node-disjoint paths](https://arxiv.org/abs/1805.09956): multicommodity-flow relaxation can have large integrality gaps even in grids. This cautions against treating fractional flows as realizable routing quality. Their boundary-source/max-routed-pair setting differs from our multi-sink/all-nets objective.
- [IrwinJam/m3d-router](https://github.com/IrwinJam/m3d-router/tree/0027d80768b69c52ba96e673d46967f3a6cf6fc3), MIT, copyright James (IrwinJam) 2026. Inspected source without execution or copying. Uses Numba search, ideal-tree blocker neighborhoods up to12 nets, sequential/negotiated repair, sideways/uphill acceptance with best-state restoration. This supports broader moves as a hypothesis. Its source-search tie modifiers mean exactness comments require independent checking before reuse. PR12 output was audited separately; source was not reproduced. Stored ignored source/license under dev/artifacts/research-m3d; compact revision record in public-source-inspection.json.

## Measurements from this session

Implemented original deterministic hash ranks among equal-cost Dijkstra queue entries. Physical distances remain exact; alternative coherent predecessor trees change geometry. `explore` accepts legal equal/lower-delay single-net trees, then negotiated repair, up to5 cycles under2s/case. Same Phase2 starts/cases/seeds as prior screen:21/21 improve over Phase2; versus negotiated,18 improve and3 regress. Seven-case geometric means by seed:

| Seed | Negotiated | Equal-delay exploration |
|---|---:|---:|
| 1 | 1.072784 | 1.083164 |
| 2 | 1.066987 | 1.087974 |
| 3 | 1.065078 | 1.098174 |

These are development-only aggregates, not official complete tier scores. No per-case best seed selection.

Fixed seed1 exploration then applied to previously validated negotiated full-tier routes:9/9 legal,all cases improve,official hard score1.1059077449039443. Extra core9.080s/wrapper10.837s; summed baseline→polish→negotiated→explore components117.023s. Search costs of all earlier screens/restarter trials are separate. Not fresh end-to-end timing. Evidence plateau-validation.json retains warm-start path/output hashes. Deadline-based termination may change route bytes near the cap; final reproducibility remains Phase4 work.

Also implemented geometry-free whole-instance negotiation: release all ownership, start every net empty, negotiate up to100 rounds, restore incumbent on failure/timeout/worse result. Same2s/5passes/three-seed development screen:9/21 improve;others retain legal originals. Broad restart is not yet a reliable default under this budget. One separate case01 seed1,10s/1pass pilot improved11614→10854; pilot and21-run screen are separate costs. No public warm starts or copied solver code.

## Next alternatives and experiments

1. Generate several candidate trees per selected net (original, shortest with alternate ties, compact near-shortest), then choose a mutually compatible combination by bounded branch-and-bound. Physical delay is additive per tree; vertex conflicts supply exclusions. Exact inside this finite candidate set only, not global optimum. Initial group size4–8 and2s repair cap; protect frozen nets/pins.
2. Broader destroy/rebuild with local windows and adaptive group selection. Avoid depending on a single ideal tree. Compare to the retained exploration stage from identical legal starts and budgets.
3. Controlled legal uphill exploration with immutable best checkpoint. Only retain after independent rollback/interruption fixtures and measured benefit. Compare to zero-temperature baseline.
4. Longer fresh-start negotiation with compact/fanout-aware trees. Treat it as an independent initialization portfolio, disclose generation/search cost and source attribution.

Keep development hard01–07 and validation hard08–09 separate; no validation-driven parameter selection. No proof that observed stagnation is a particular basin; improved equal-delay results are evidence that route geometry matters.

Followup implementation:joint finite candidate selection weak(9/21 gains),wide groups strong;budget expansion10s improves all representativecases. Legal1% threshold walk with protected best checkpoint gives small extra gains. Current full-tier1.186873. Next hypothesis is compact/fanout-aware group construction;all extrapolations remain unmeasured.

Resource-pricing followup:compact3/4 driver-distance seeds reduce vertex uses in7/9 representatives,butworsen aggregate vs exactwide for everyseed. Fanout penalty scaling1/ceil(sqrt(sinks)) wins7/9 delay comparisons despiteoftenmorevertices. This rejects wirelength/occupancyalone as a reliable score surrogate. Selection based on official delay;full-tier fixedconfig validation pending at timeofthis note.

## Quantum suggestion: feasibility triage

User supplied an unattributed online suggestion claiming hard score at least1.0418 and ambiguous“19xxx1”. No method,paper,encoding,runtime,or quantum hardware evidence supplied;link requested asynchronously. Existing CPU hard1.212968 already exceeds quoted score. No quantum provider access configured/used;no package installation/hardware booking performed.

Primary IBM QAOA tutorial:https://quantum.cloud.ibm.com/docs/en/tutorials/quantum-approximate-optimization-algorithm ; simulator resource authority:https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html . Aer documents CPU methods and dense statevector memory16*2^n bytes. Calculation:26qubits1GiB,28qubits4GiB,30qubits16GiB before workspace/OS;recorded machine RAM15.3GiB. Therefore small classical simulations of restricted repair encodings may be feasible,not a demonstrated full-case quantum advantage. Alternative tensor representations have different limits;dense bound is not a universal quantum limit. A proposed experiment must specify legal-tree/delay encoding and compare against classical candidate selection/branch-and-bound under disclosed resource costs. Do not divert competitive pipeline on a bare assurance.

User supplied another assessment suggesting candidate-tree binary selection solved classically first. This matches the already implemented select operator;21 development trials9 improve,finite-set search weaker than negotiated methods(see selection-screen/neighborhood-comparison). Its quoted current1.183497 is historical;hard current1.212968. Revisit richer candidate generation/objective encodings if evidence supports it;changing to quantum optimization alone does not fix weak candidate sets.

## Headroom-guided research followup

Computed obstacle-free driver/sink distances exactly in relaxed graph:minimum over traversed horizontal layerk of ManhattanXY*delay[k]+via*(|driverZ-k|+|sinkZ-k|). Sum lower-bounds legal multi-net delay;capacity/pin relaxation may be unattainable. Current optimistic tier score ceilings:intro1.1870,hard1.7617,scale1.1622,congested1.6468,designs1.8112,stress1.1052. This changes resource allocation:higher potential congestion/design optimization,with sparse large tiers benefiting from faster search. Not a global-optimum claim.

Inspected primary sources,original implementation only:no downloaded code executed/copied:
- OpenROAD/FastRoute documentation:https://github.com/The-OpenROAD-Project/OpenROAD/blob/master/src/grt/README.md . Critical nets can receive preference during congestion iterations. Transfer idea:order by excess totalphysical delay above relaxed lower bound,rather than timing slack absent from this challenge. Capacity/RC/parasitic models differ;do not add those constraints.
- VTR connection-router documentation:https://docs.verilogtorouting.org/en/latest/api/vprinternals/router_connection_router/ . Lookahead guides maze search;zero A* factor corresponds to Dijkstra. Implement exact admissible/consistent heuristic in our own grid model;do not copy nonadmissible timing heuristics or spatial clipping.
- Song/Lanka/Yue/Dilkina,NeurIPS2020,“A General Large Neighborhood Search Framework for Solving Integer Linear Programs”:https://papers.nips.cc/paper_files/paper/2020/file/e769e03a9d329b2e864b4bf4ff54ff39-Paper.pdf . Fix unaffected variables and repair selected neighborhoods. Transfer decomposition/group-selection ideas;no training pipeline or claim their ILP results transfer to routing.

A* candidate heuristic:distance in graph with all horizontal edges at cheapest layercost,to union of XY sinkbounding rectangles grouped by sinklayer. Lower bound survives obstacles and nonnegative congestion;consistent via triangle inequality;zero at every sink. Keep goal rectangles static even after a sink pops. Thus each popped sink has shortest penalized path cost;physical distances independently rescored. Geometry/tie order may change global outcomes despite exact individual searches;compare matchedcaps.

## User search-list coverage and CUGR followup

Covered/read:PathFinder,present/history congestion,RRR,VTR/VPRmaze routing,Dijkstra,multisource root-aware attachment,exactA*,SALT/shallowlight tradeoffs,OpenROAD/FastRoute,MAPF-LNS2/generalLNS,netordering,and finitecandidate selection. Implemented original related mechanisms;did not reproduce every cited externalsolver or paper. Still unevaluated:ALTlandmarks,NTHU-Route,NCTUgr,SPRoute,fullcontest survey,dual decomposition/windowILP/CP-SAT,bidirectionalsearch/contractionhierarchies,delta-stepping/GPUmethods,learning-basedordering/rl/GNN,and fullM3Dtaxonomy. These are a research backlog,not claims of implementations.

Read CUGR authorrepository https://github.com/cuhk-eda/cu-gr and author-hosted DAC2020paper https://cwpui.com/doc/c10.pdf . Repository uses CPUmultithreading/eight-thread experiments;CUGR itself is not a GPUrouter. Its probabilisticresource model,3Dpattern routing,multilevelmaze search and detailedroutingguides target a different model/objective. Potentialtransfer:coarse-to-fine candidatecorridors with fullgraph fallback,not importing preferred-directions/spacing/blockages or claiming coarse legalguides are legal routes. No sourcecopy/build/execution. GAMER publisherabstract https://ieeexplore.ieee.org/abstract/document/9799536/ identifies GPUmaze routing integratedintoCUGR;fullpaper open returnederror,so no claim to haveread/reproduced its implementation. No GPU available/used.

ALT triage(inference):relaxed layeredgrid pair distances have a cheap analytic formula;landmark tables might be less useful than direct geometric lowerbounds here. Actual ownershipgraph changes acrossnet/group reroutes;precomputed distances must remain lowerbounds after graphchanges. Evaluate landmark memory/setup/runtime only if profiles justify it. No blanket rejection or implementation claim.

## Cost-distance paper and external assessment checked

Read full HTML of Held/Perner2025,“Cost-Distance Steiner Trees for Timing-Constrained Global Routing”:https://arxiv.org/html/2503.04419v1 . Objective adds congestion onceper treeedge and weighted driver-to-sink delay. Its main algorithm merges components with weightdependent distances;existing-component costs discounted,goal-directed searches suggested. Sinkweights are timingcriticalities from their Lagrangean timingconstraint formulation,not automatically “delay lost if displaced.” This challenge's physicalweights are all1. Do not add bifurcation/RC penalties to scoring.

Original prototype treecost uses existing root-aware incrementalattach,full physicaldriverdistance seed4/4,and congestioncharges on newly added vertices only,with samefanout price scaling as control. It discounts reusedtrunks while summing physicalpathdelay foreachsink. This is a greedy adaptation,not paperalgorithm reproduction and not its approximationguarantee. Five-second seed1 screen:hard9284vsastar9292,congested65459vs64591,designs61712vs61266. Reject asdefault after2/3regressions;retain experimental method forfuturecandidategeneration.

Externalassessment's mergedleaderboard totals/1.0168 remain accurate:https://github.com/partcleda/eda-3d-routing-challenge/blob/main/LEADERBOARD.md . It omits publiclyaudited PRheads(nowhistoricalpublicaudit1.387394). LiveGitHubpage displayed11PRs/19forks;old2PR/4fork snapshot outdated;starcount not readable in returnedpage so not claimed. “Tiny margins” was speculation contradicted by measuredhard1.22025 and relaxedceiling1.7617. Introrelaxedceiling1.187 also meansbaseline not provennearoptimal. No claim alloptimisticheadroom achievable.

CurrentwrittenCONTRIBUTING re-read:https://github.com/partcleda/eda-3d-routing-challenge/blob/main/CONTRIBUTING.md . Route-onlydiff,anylanguage/hardware,completelegalper-tier requirements unchanged in displayedtext. No explicitreferencewarmstart provision/prohibition found;disclose references and distinguish assistedoutput improvement from independentgeneration. No maintainerclarification obtained,noissue/message sent. Recheck before finalsubmission.

## Six-link audit and pricing follow-up

Checked the user's six URLs against the existing notes and fetched missing primary material. Reading status is distinct from implementation or reproduction.

| Source | Prior coverage and this follow-up | Transfer and limits |
|---|---|---|
| [PathFinder](https://www.esa.informatik.tu-darmstadt.de/archive/twiki/pub/Lectures/AlgorithmenImChipEntwurfDe/router-pathfinder.pdf) | Previously reviewed. Exact host unavailable through browser; revisited the [University of Toronto course mirror](https://janders.eecg.utoronto.ca/1387_2015/readings/pathfinder.pdf), especially congestion/delay algorithm sections. | Present/history negotiation and delay-aware seeds are relevant. Their critical-path slack weights differ from our all-sinks sum. Our implementation is related, not a reproduction. |
| [NTHU-Route](https://cs.nthu.edu.tw/~tcwang/nthuroute) | Previously backlog. Read author [www-host page](https://www.cs.nthu.edu.tw/~tcwang/nthuroute/) and algorithm sections of [ICCAD2008 paper](https://www.cecs.uci.edu/~papers/iccad08/PDFs/Papers/05A.1.pdf). | Adaptive base/congestion schedules and congestion-region/reroute ordering are promising experiments. Their layer-projection/via proxy does not replace our physical edge delays. Source requires an application; no request, download, copying or execution performed. |
| [CUGR](https://github.com/cuhk-eda/cu-gr) | Previously read author README and DAC2020 paper; reopened README. | Probabilistic resource costs, 3D pattern candidates and multilevel maze corridors. CPU router; its detailed-routing guides and objectives differ from legal trees scored here. Not compiled or reproduced. |
| [DATE2026 /1157.pdf](https://past.date-conference.com/proceedings-archive/2026/DATA/1157.pdf) | No confirmed reading. Browser access failed; direct authorized network fetch returned HTTP404. | Do not attribute a method or claimed result to this unavailable document. A working mirror or title is needed to identify it reliably. |
| [Cost-Distance Steiner Trees](https://arxiv.org/abs/2503.04419) | Previously read full author [HTML](https://arxiv.org/html/2503.04419v1); revisited abstract/HTML. | Weighted driver-to-sink delay plus tree congestion is a close conceptual match. Our discarded greedy treecost prototype does not implement their component-merging algorithm or inherit its guarantee. |
| [Prim-Dijkstra Revisited](https://vlsicad.ucsd.edu/Publications/Conferences/355/c355.pdf) | Not previously documented as read. Read objective, PD-II edge swaps, DAS pseudocode, experiment setup and conclusion sections. | Sum-of-sink detour objective makes multi-sink topology/branch weights relevant. Their wirelength constraints and Manhattan plane differ from our layered occupied graph. Fixed-other-net shortest trees are already delay-optimal; useful changes must free resources or coordinate nets, not claim single-net branch swaps beat an exact shortest tree. |

Next experiment is original fixed-point congestion pricing: multiply all shortest-search physical/priced priorities and A* bounds by16, then divide congestion price by fanout divisor. This retains fractional price increments lost by integer division, to1/16 resolution. Actual physical tree delays stay unscaled. It is not a reproduction of NTHU-Route, PathFinder, PD-II or the cost-distance paper. Default modes retain their old price units; experiment mode is fanout_fine.

### DATE paper identified from the user's IEEE link

User supplied [IEEE document11539267](https://ieeexplore.ieee.org/abstract/document/11539267). IEEE access failed through the browser and direct fetch returned418. Found the paper title/authors and abstract on the [official DATE2026 programme](https://date26.date-conference.com/programme), sessionTS18.7: *An Adaptive Cost-based Via and Congestion Co-optimization Framework for VLSI Global Routing*, Zhaoyi Wu, Haishan Huang, Jianli Chen and Zhifeng Lin. The programme's own Download Paper link points to date26.date-conference.com/proceedings-archive/2026/DATA/1157.pdf and also returns404.

Read the official abstract only, not full text. It describes a 2D via-aware spine tree, maze routing, congestion-aware layer assignment, then iterative RRR using3D bidirectional A* and adaptive via costs. The abstract reports results on overflow/via count with approximately preserved wirelength, not this challenge's sink-delay score. It does not establish that the implementation builds on CUGR, as the earlier third-party assessment suggested. Possible transfer: adaptive search-only via/congestion penalties and optional bidirectional repair search, followed by unchanged official physical-delay checks. Full algorithm details, implementation and independent result reproduction remain unperformed.

Pricing experiment result: fine units win4/6 matched case/seed comparisons, tie1 and lose1. Fixed seed1 full hard and congested stages improve all13 outputs from their incumbents; official scores1.2303243121958916 and1.08805956745537. This is incremental optimization with extra search effort; universal price-schedule superiority is not established. See pricing-comparison.json and tier-pricing-coverage.json.

### Full DATE PDF now supplied and read

The user provided a root PDF after the IEEE stamp link also failed/418. Strict pypdf parsing succeeds on all7pages; metadata matches11539267. Read the complete extracted text. This supersedes the earlier abstract-only access status. See DATE2026_VIA_CONGESTION.md and date-paper-integrity.json for hash, access scope and method-transfer cautions. CUGR cost-model reuse is explicitly stated in the full text. The exact construction/DP/search concerns and the distinction between industrial overflow/via results and our sink-delay scoring are now documented. No licensed PDF/text included in commits.

## October 1 handoff research: next experiments, not measured gains

Inspected current local engine and retained guided-budget evidence, the MAPF-LNS2 author repository/source and paper, CUGR author paper/repository, and Held/Perner cost-distance paper. No external code copied or executed. Challenge repository landing page was accessible; PR pages and the previously inspected IrwinJam source failed through browsing, so public standings/source changes were not refreshed.

Submission clarification: all three tracked hard entries identify Anthropic (reference). Local LEADERBOARD.md lists negotiated_x2 at 1.0168, negotiated at 1.0, and negotiated_fast incomplete (8/9). Our recorded hard best is 1.220250233796514 in tier-followup-coverage.json, not in submissions/. This checkout has no .venv, dev/upstream, or dev/artifacts; prior best route files and raw provenance must be recovered or regenerated before optimization. Recorded scores are historical official evaluations, not fresh rescores this session.

Evidence for changing repair proposals: repair() selects blockers of one ideal tree, inserts blockers in net-index order, and negotiate() retains that group order across rounds. History is reset per repair call. In the retained hard01 five-second guided run, 2033 attempts include 1935 nonimproving legal repairs and 91 failures; the twenty-second run stops after about 5.29 seconds at the 100-cycle ceiling with the same delay9292. This does not prove optimality or imply that extra cycles alone help.

Ranked proposals:

1. Adaptive neighborhood selection: alternate ideal-tree blockers, transitive blocker groups, spatial hotspots, and random groups; use bounded group sizes and reward actual physical-delay reduction per search cost. Cache unsuccessful proposals only while relevant local ownership remains unchanged. Repeated failures can trigger a different group rather than another identical repair. MAPF-LNS2 combines neighborhood strategies and tracks their success; transfer static dependency selection, not time-dependent collision semantics. Sources: https://github.com/Jiaoyang-Li/MAPF-LNS2 ; https://raw.githubusercontent.com/Jiaoyang-Li/MAPF-LNS2/master/src/LNS.cpp ; https://researchmgt.monash.edu/ws/portalfiles/portal/409305616/408475878_oa.pdf . Source main branch is mutable, not a pinned reproducibility input.

2. Diverse corridor proposals: generate several improving/near-improving ideal trees using explicit penalties for previously chosen corridor vertices, different transit layers, and alternative displaced owners. Rank by predicted target gain and measured relocation cost of blockers. Current six candidate variants mainly change prices/ties against the same usage map; richer candidates could address the earlier weak finite-selection results. Diversity helps only if compatible legal combinations lower total physical delay.

3. Restricted static conflict-based search for 2–6 nets: independently compute exact driver-rooted trees with frozen external owners; when two trees share vertexv, branch on forbidding v for one net or the other, then replan that net. Rooted shortest-path trees minimize summed sink distance in each fixed allowed graph, providing a local bound. Exhaustive completed search can certify the chosen frozen-net subproblem; timeouts cannot. Enforce strict node/time caps and preserve incumbent. Mechanism source: https://ojs.aaai.org/index.php/SOCS/article/view/18222 . This adaptation removes all time dimensions and is not a reproduced MAPF solver.

4. Stronger exact A* heuristic: current heuristic charges every horizontal step at the cheapest layer, even if reaching that layer needs extra vias. For each static sink-layer rectangle, minimize over transit layerk: XY-distance-to-rectangle*layer_delay[k] + via_delay*(abs(z-k)+abs(k-goal_z)). This is distance to the same goal set in the obstacle-free layered graph, hence a consistent lower bound with nonnegative congestion charges. Minimum over actual sinks is tighter but more expensive. Prove/check implementation independently and compare expansions, overhead, and final legal delay; no speedup measured yet.

5. Tree topology with resource prices: implement a genuine component-merging candidate constructor with unit sink weights and vertex-capacity prices, rather than treating the rejected greedy treecost prototype as a test of the full paper. Paper reports stronger results on large-fanout instances, but its physical/bifurcation models differ. All challenge sink weights remain1, bifurcation penalties remain0. Source: https://arxiv.org/html/2503.04419v1 . Prioritize after cheaper neighborhood experiments.

6. Coarse corridor search for scale/stress: CUGR plans on a coarsened 3D graph, then searches fine grids in proposed boxes. Adapt for candidate generation with widening/full-grid fallback; unrestricted exactness is not preserved by corridor clipping alone. Source: https://cwpui.com/doc/c10.pdf ; https://github.com/cuhk-eda/cu-gr . SPRoute source repository https://github.com/asyncvlsi/SPRoute supports parallel global routing, but its README warns current code differs from publication versions. First parallelize independent seeds/cases after measuring RAM; measure total portfolio cost.

Suggested experiment order after artifact recovery: controlled 100-vs-1000-cycle screen at fixed budgets; randomized repair order; adaptive/diverse groups; restricted conflict-based repair; stronger heuristic; component construction. Use hard01/04/07 and declared congested/design representatives, seeds1–3, matched starts and budgets, held-out hard08/09 only after selection. Track proposals, failed/nonimproving repairs, group size, gain per CPU second, expansions, peak RAM, and official legality/delay. Current congested/design runs still improve with longer caps, so larger bounded budgets there have more direct evidence than hard-only brute-force extension. No new score, implementation, test, or advantage claim from this research session.

### Spatial prototype measured

Original full-tree spatial selection implemented and screened against fine and
fine-diverse on hard01/04/07,seeds1–3,5M/20M expansions,60s safety cap,
schedule2/1/1, same available local incumbent.54/54 outputs official-legal;
all hit exact work caps. Fine-diverse wins7/9 versus fine at each cap, relative
development geomean1.000583/1.002586. Spatial wins2/ties1/loses6 at5M and
wins3/loses6 at20M versus fine; relative geomean0.999350/0.999372. Spatial
versus diverse wins2/loses7 then wins3/loses6. No tuning on08/09.

Spatial repair counts:5M131 attempts/2 gains/89 failures/40 nonimprovements;
20M564/17/315/232. Diverse1323/41/138/1144 then5349/109/516/4724. These
are group counters, separate from per-net exploration. Actual group-size
histogram was not instrumented; maximum13. Total wrapper screen cost278.214s
excludes inherited incumbent generation, compilation, final stage and scorers.
Equal expansions are not equal CPU work; timings recorded.

Keep spatial optional; do not claim spatial LNS in general failed. Nested
boxes scored by a nonnegative detour sum favor larger groups. Smaller or
randomized groups, boundary-preserving repair and shared-trunk construction
remain unmeasured options. Neither public geometry nor per-net competitor gaps
were used to choose moves. Fine-diverse selected for fixed all-hard followup.
