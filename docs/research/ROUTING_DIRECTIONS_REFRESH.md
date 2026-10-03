# Routing directions after AI and local-repair screens

## Scope

Research refresh follows actual zero-gain finite-pool, exact-window, chain and pretrained REST screens. Independent fresh construction and driver-to-sink delay remain priorities. Papers use different capacities/objectives: none establishes superiority on this challenge. Sources were read through PDF text/selected sections or repository documentation, not independently reproduced. No entrant route files used.

## Current public implementations

Fresh API inventory still26PRs; PR25 head changed from6bcf44c tode7ef9d. Its complete tree has no extra non-toolkit solver beyond the example. PR body links IrwinJam/m3d-router. Linked solver Git tree remainsdca18b22954261536106fd87e4abe1e75e1a9185. Verified current blobs against cached core.py/router.py/overnight.py/README/LICENSE, then reread implementation. Exact audit: public-pr-refresh.json. This refresh covers PR heads and changed PR25, not a new exhaustive fork/branch scan.

Concrete source observations: negotiation reroutes only nets touching the current overuse mask, with optional periodic full passes. History increases on overuse; present cost grows multiplicatively with cap. LNS mixes window and ideal-blocker groups, sequential seed-first reconstruction and negotiated reconstruction; group congestion strength is randomized. Physical polish precedes annealed acceptance; best legal solution is retained. Overnight defaults use long per-tier chunks and occasional fresh runs. These are inspected behavior/configuration, not measured winning compute. Source/license: https://github.com/IrwinJam/m3d-router . No copied/executed competitor code.

Taz33m pathfinder_lns metadata was previously inspected; no generation source located in the inventoried submission branches. kesudh's available Rust source includes bounded conflicts, chain tolls and fast queues, but relies on credited public parents. Other source availability and limitations: PUBLIC_SOURCE_REVIEW.md. Metadata-only descriptions are not treated as implementation evidence.

## Ranked experiments

| Priority | Direction | Concrete next experiment | Cost / limits |
|---|---|---|---|
| 1 | Fresh negotiation and legalizing conflict groups | Compare gradual/aggressive schedules; add conflict-only rerouting and occasional full rebuild; measure first legal time, delay and diversity | Small CPU screen first; no incumbent geometry; failures included |
| 2 | Context-dependent learned ordering | Train on a broader own feasible curriculum; use current resource congestion/blockers and remaining pins, choose next net sequentially | CPU linear/bandit baseline before a neural policy; disjoint layout seeds; legality reward first |
| 3 | Larger structural moves | Find nets competing for the same narrow XY/layer passage; rebuild complete groups while permitting transient legal uphill states | Different from failed random/bbox groups; hand-check cut capacity using vertices, not edges |
| 4 | Stochastic global proposals | Apply correlated nonnegative region/layer toll perturbations, retain multiple own legal basins and recombine trees | Physical acceptance unchanged; distinguish generation cost from selection cost |
| 5 | Full cost-distance merge | Audit paper enhancements against our simpler component prototype, then implement restricted representative-point routing | Paper objective has independent congestion/delay; no imported guarantee for our vertex adaptation |
| 6 | Exact local repair on better groups | Use cut/blocker structure to select windows, expand boundaries only after restricted failure | Prior CP-SAT/CBS results mostly no gain; UNKNOWN is not infeasibility; exactness restricted |
| 7 | Throughput | Profile current dense resets/snapshots; compact queues; reroute only conflicted nets in fresh generation | Especially scale/stress; benchmark matched expansions and memory, no assumed speedup |
| 8 | Multilevel corridor generation | Plan broad layer/corridor choices then refine on original grid; reserve local pins/capacity | Coarse vertex model must not claim legal output; fine checker remains authority |
| 9 | Differentiable global allocation | Try CPU soft candidate probabilities only after candidate diversity improves | Current finite-pool CP selection already optimal with no gain; gradient optimization of same pool cannot improve its exact optimum |
| 10 | GPU or external AI proposals | Profile transferable DAG batching; optional small high-level proposal generation if justified later | No GPU available; REST mismatch measured; no external general AI endpoint used; no performance promise |

Ranking is engineering judgment, not measured expected gains. Favor new global geometry over repeatedly solving exhausted candidate sets.

## Primary literature and what transfers

### Cost-distance trees

Held/Perner combine congestion cost and weighted driver distances, with iterative weighted component merges. They also describe practical improvements beyond the core randomized merging algorithm. Our existing Python prototype reconstructs a physical SPT from an embedded path union and uses approximate symmetric vertex prices; its three losses do not disprove the paper's complete algorithm. Set bifurcation penalties to zero for this challenge. Adaptation must separately justify vertex pricing and merged-path sharing. [Author PDF](https://www.or.uni-bonn.de/~held/publications/CostDistRouting.pdf).

### Learned decisions

The IJCAI2025 transformer paper models net ordering with a graph/attention/pointer policy, rewarding wirelength, vias and violations. We need legality and actual sink-delay rewards. XRoute exposes net-ordering/routing environments with separate regional tasks; useful experiment structure, not a compatible pretrained solver. The DR-ALNS paper instead learns search controls, including acceptance/operator decisions. That motivates a small contextual policy with randomized exploration before expensive full RL. [IJCAI paper](https://www.ijcai.org/proceedings/2025/1055.pdf), [XRoute](https://github.com/xrouting/xroute_env), [DR-ALNS](https://arxiv.org/abs/2211.00759). Vehicle-routing evidence does not imply chip-routing benefit.

### Differentiable allocation

DGR constructs topology/path candidates, optimizes continuous choice probabilities and uses stochastic Gumbel-softmax with temperature annealing before layer assignment/postprocessing. Useful idea: coordinate many nets simultaneously. Our exact finite tree-pool selection already finds its restricted optimum, so the immediate need is richer candidates or a different factorization, not replacing exact selection with gradients. Do not transfer its wirelength/via/overflow objective or GPU claims to our score. [Author PDF](https://wadmes.github.io/cv/raw/DAC24.pdf).

### GPU and hierarchical search

InstantGR uses routing DAGs, congestion-driven DAG augmentation and net/node parallelism; its repository requires CUDA compilation and is BSD3licensed. A CPU adaptation could test restricted DAG proposals and independent batches, retaining unrestricted exact polishing. Its published metric includes wirelength, vias and overflow, unlike ours. Source reviewed at documentation/paper level; implementation not audited or executed. [Paper](https://shijulin.github.io/files/1239_Final_Manuscript.pdf), [repository](https://github.com/cuhk-eda/InstantGR). Multilevel routing offers resource reservation and coarse-to-fine refinement; MARS is a historical primary example, not our chosen implementation. Only its indexed abstract was accessible in this refresh; full PDF fetch timed out. [MARS paper](https://www.cecs.uci.edu/~papers/compendium94-03/papers/2002/iccad02/pdffiles/01c_2.pdf).

## Implemented probe in this refresh

`dev/fresh_negotiation.py` independently builds coherent driver-rooted priced shortest-path trees from empty geometry. Other nets' terminals remain forbidden; conflicting intermediate trees never become accepted outputs. Present/history schedules and fanout toll scaling are configurable in explicit plans. Seeded geometry, global expansions/time/round ceilings, per-round conflicts, official legality and saved-output hashes are recorded. Four focused checks pass, including conflict-only termination: independent hand delay22, interruption without accepted conflict, fixed-work small-instance determinism. This is a Python feasibility experiment, not a compiled performance change or reproduction of another solver.

Synthetic training-only screen:24layouts,one seed,two schedules,250Kexpansions/10s safety and80round ceiling. Aggressive15legal; gradual0legal. At320rounds under unchanged work/time caps, aggressive16legal and gradual6legal. Original records retained. Official intro05/hard01 screen:two seeds,3Mexpansions/30s safety/180round ceiling. Aggressive intro05 delays4025/3887;gradual incomplete twice. Both schedules incomplete on hard01 for both seeds. All eight attempts reached3M expansions; no wall cap was reached. See fresh-negotiation evidence for completed results. Construction is fresh; no improvement is claimed without comparison to our own incumbent. Existing toy validation seeds9001–9024 remain untouched.

Conflict-only followup on hard01, same two seeds and3M/30s ceilings: aggressive produced legal fresh delays10010/10218; gradual remained incomplete twice. All-net counterpart was incomplete on all four. This shows increased fresh feasibility on this case only; our own incumbent9068 is better, so no score gain/adoption claimed. Evidence fresh-negotiation-conflict.json. Old all-net source preserved under dev/experiments/source-snapshots/20261002-fresh-negotiation-all-nets. Next combine conflict-only construction with exact physical polish and generate a broader own curriculum before training another model.

Additional cost-distance details read: the paper discounts already-owned component edges, tracks end-component-specific labels, uses a two-level heap and relocates Steiner representatives. These are absent from our simplified representative-merging probe and need a faithful objective-aware experiment. This reinforces that rejecting the simple probe is not rejecting the full method.
