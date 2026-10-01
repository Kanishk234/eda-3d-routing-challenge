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
