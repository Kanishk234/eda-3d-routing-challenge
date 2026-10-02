# Independent CPU routing experiments, October2

User constraint: no competitor route warm starts or copied route artifacts. All candidate parents here are our own stages; historical official reference starts remain attributed.

## 1. Reservation-first branch repair

Implemented standalone Python prototype branch_repair.py. Compute an improving ideal target tree, reserve its vertices, find each blocker subtree's least common ancestor of conflict vertices, and reroute only detached sinks from root-distance-labelled retained vertices. Coherent predecessor forest extends a retained tree; candidate group gets full official checking before strict physical acceptance. Limit rollback restores last accepted state. If the cut reaches the root, rebuild that blocker. Compare the same algorithm with whole blockers rebuilt.

18 trials on hard01/04/07,seeds1–3,300K expansions,30s safety: all legal, no improvements in either mode. Branch release1644vertices versus3676whole,34.194s overall. Most proposals exceed the3blocker cap. This quick negative result does not reject all branch algorithms or longer coordinated repairs. Three focused tests cover root distance, ancestor sinks/sibling preservation, deterministic caps/rollback.

## 2. Fresh component construction

Component_router.py clears all incumbent geometry. It merges active sink components using weighted physical delay plus symmetric endpoint vertex prices, randomly selecting a weighted component representative. Project embedded path union onto a rooted physical shortest-path tree to eliminate cycles. Sparse negotiated history/present prices seek vertex legality.

Inspired by Held/Perner: https://arxiv.org/html/2503.04419 and https://www.or.uni-bonn.de/~held/publications/CostDistRouting.pdf . AlgorithmII and practicalIII sections read. Symmetric vertex prices, union projection and the challenge capacity model differ from their edge-cost formulation, so no approximation guarantee transferred. No third-party code copied. New stars are separate per-sink priced root connections, projected coherently; neither method uses reference or competitor route geometry.

Initial18trial1M pilot: six legal tiny intro01 constructions (both methods212/212/208), larger intro05 andhard01 all incomplete. This is not a tier score. Expanded six serial intro05 trials10M/24rounds/120s safety:star3989/3993/3905,merge4185/4183/4207;merge loses3/3. Our existing intro05 incumbent3845beats all of these. Do not adopt or port this particular component builder based on these measurements. Three tests verify hand delay, work interruption and independence from supplied incumbent geometry.

## 3. Finite tree pool with CP-SAT

New exact allocation formulation: choose exactly one candidate tree per net; each vertex may belong to at most one selected tree; minimize the sum of independently checked per-net physical delay. A verified base option ensures a legal fallback. Hint the base and cap objective at its delay. One solver worker, seed1,30s wall/10deterministic seconds per case; record actual status and restricted bound. OPTIMAL means optimal within this candidate pool only.

Official CP-SAT API/status references read: https://developers.google.com/optimization/cp/cp_solver . OR-Tools9.15.6755 installed in project.venv, optional full dependency pins in dev/requirements-exact.txt; no system Python changes.30tiny random finite pools match independent exhaustive enumeration in one focused test.

Declared pool: our three continuation rounds plus preceding checkpoint. Hard9cases all restrictedOPTIMAL,4delay-unit gain on06;score1.2750711365059078. Congested4cases all restrictedOPTIMAL,2gain on03;score1.1206227053047342. Designs3cases restrictedOPTIMAL,zero gain. Whole-tier pinnedCLI checks agree. Native zero-budget checkpoints preserve improvements. Source routes not generated equally or independently; added portfolio selection effort is disclosed.

An initial reporter failed after selection because a relative output path could not be made relative to an absolute workspace root by the measurement helper. It did not alter parent/canonical routes. Normalize output path before execution; rerun in a fresh output directory and retain the failed artifact. Successful rerun is authoritative.

## 4. Expanded generation and allocation, active experiment

Generate coherent driver-rooted priced shortest trees for each net with occupancy penalties0/2/8/32,seed1,up to3M expansions and60s per hard case. Each tree is checked individually with the official checker using the full instance terminal map; other missing nets make that partial submission globally illegal, correctly. Individually legal options may conflict; CP-SAT decides compatibility. This separates geometry generation from global resource allocation. Base remains available, so acceptance cannot worsen delay.

Plans:hard-priced-candidates.json andhard-expanded-tree-pool.json. Exact selection60s/20deterministic seconds percase,one worker. All9cases receive fixed config; no08/09operator selection. Active session78837,log/tmp/expanded-tree-pool.log,candidatefiledev/artifacts/20261002-priced-candidates/trees.json,outputdev/artifacts/20261002-hard-expanded-tree-pool. Source frozen throughout; do not edit generator/selector/branch helper while running. No improvement claim until final whole-suite official validation.

Two additional tests compare candidate physical distance with independent Dijkstra,protect foreign terminals,and enforce work limits. New tests total9pass. Historical49checks are retained evidence and were not rerun here. Some fixed-pool selection overlapped fresh construction, so timings do not support speedup claims.

Next: inspect expanded-pool restricted gaps, candidate coverage and legality; preserve accepted gains. If allocations improve, prioritize generating diverse capacity-efficient trees and price-feedback rounds before more random incumbent walks. If not, diagnose which nets lack viable alternative geometry before porting or expanding compute.

## Expanded pool result and sharing experiment

First expanded priced-rooted-SPT pool finished.3548 unique candidate variables across9hardcases,all restrictedOPTIMAL; score1.2750711365059078,exactly the prior4-unit parent fusion gain. New shortest-tree alternatives add no further scored gain. Evidence hard-expanded-tree-pool.json. Preserve generator/selector snapshots for this run under dev/artifacts/20261002-priced-candidates/source/ before subsequent edits.

Next changed candidate construction: add sinks onto an existing rooted tree, charging congestion only on new path vertices. Use retained physical root distances as frontier labels scaled8/12/16 against16-unit new-edge delay, with penalties2/8. Scales below16 intentionally trade some delay for sharing capacity; all physical sink delays are recomputed by the official checker. This is a candidate generator, not accepted single-net polish, and is related to earlier compact attachment prototypes. Its new role is to expose capacity-sharing choices to global exact selection. Keep all prior rooted-SPT and verified parent options in the pool.

Active session90585: generator then CP-SAT; plans hard-attachment-candidates.json andhard-attachment-tree-pool.json; log/tmp/attachment-tree-pool.log; outputdev/artifacts/20261002-hard-attachment-tree-pool. Fixed all9case config,3M/60s percase generation and60s/20deterministic seconds percase selection. One worker each, sequential. Sources frozen. One added test verifies physical sinksum6 on hand two-sink instances across all3frontier scales and interruption. New checks now10total; historical49notrerun.

## Exact geometry and static conflict search followup

All earlier attachment/pool jobs are complete. Expanded attachment pool added no geometry gain. Restricted path models were screened on15 groups, with and without safe physical-distance pruning; neither improved. Multi-sink rooted arborescences enforce one parent and positive physical root-distance potentials and minimize the sum of sink distances:15 short solves yielded no gain. Six stronger strict-improvement solves all returned UNKNOWN. Those limits are not proof that no improvement exists.

Static CBS (dev/static_cbs.py) adapts conflict branching to static disjoint routing vertices. Each low-level rooted shortest-path tree minimizes all driver-to-sink delays for its constraints. A shared vertex yields two children forbidding that vertex to either conflicting net. This preserves completeness inside the restricted corridor when unbounded; current runs are explicitly bounded. Initial six-group screen: one restricted optimum, five budget-limited, zero gains. Four hand checks pass, including a two-layer crossing and safe interruption. A2M/group followup is recorded separately. Primary paper read: https://webdocs.cs.ualberta.ca/~nathanst/papers/sharon12cbs.pdf ; no time-step collision semantics imported.

Stronger static CBS followup completed: all6 group solutions remain legal and unchanged,4 restricted OPTIMAL,2 budget-limited at2M expansions. Two unresolved group lower bounds1276/1348 and1274/1316 leave headroom but do not imply achievable gains. Repeated small-group repair is insufficient on these four certified groups. Next geometry work should enlarge corridors/groups or construct alternative global packing, measured against the current incumbents.

## Broader static search and physical-cost-preserving alternatives
Own seed7/8 continuation completed and improved every tier: intro1.108328672,hard1.280425383,scale1.057294493,congested1.125891351,designs1.269834309,stress1.024344767. All45 legal, archived and restored; tier-independent-continuation-coverage.json. This is more search effort, not a new algorithm comparison.

Broader fixed screen uses up to4 nets, margin2,1M expansions/group,hard01/04/07. Lexicographic distance/occupancy tie-break on/off produces no scored gains. Two groups proven restricted-optimal in each variant;four budget-limited. One group's equal-cost geometry reduces expansions518910→13520; another16301→7402. Other unresolved groups remain limited, so this is not universal superiority. Two native tier workers overlapped these Python prototypes; avoid wall-speed claims. Source snapshots and full reports retained.

Read full primary ICBS paper: https://www.ijcai.org/Proceedings/15/Papers/110.pdf . Its bypass concept motivates trying an equal-physical-cost tree with fewer conflicts before branching. Our static adaptation keeps original forbidden-vertex constraints and requires strictly decreasing pairwise conflict count; no delay tradeoff or time-step semantics. Tests independently enumerate all simple disjoint path pairs for20 seeded3×3 layouts, comparing both tie options with the optimal physical total where feasible. Bypass benchmark report recorded separately.

Bypass screen completed: six legal unchanged group outputs, four1M-limited/two restrictedOPTIMAL. First four groups executed260/224/533/285 bypasses but no accepted physical gain. Reject adoption as a quality improvement. It does not fix the broader packing problem at this budget. Evidence hard-cbs-bypass.json. All26 focused prototype tests pass together. Next work should change the global construction/packing proposal family rather than repeatedly tuning these six repairs.
