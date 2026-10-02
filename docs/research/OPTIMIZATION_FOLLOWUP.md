# Alternative optimization research — October 1, 2026

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
