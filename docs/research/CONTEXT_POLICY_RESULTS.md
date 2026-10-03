# Context-dependent ordering and fresh basins

## Actual AI implementation

`dev/learned_context_order.py` builds own synthetic curricula with4/6/up to10nets, retains all generated layouts including failed teacher sampling, and selects the lowest-delay legal sampled own order. For128training layouts,24orders each:99layouts have feasible teachers,519decision examples,1237268sampled-search expansions. Teacher replay,feature extraction and learner fitting add effort. Input features combine nine net features with current occupied bbox density,pin-neighbor freedom,nearby ownership,remaining foreign pins,total occupancy and remaining-net fraction. No incumbent/competitor geometry or labels.

Two pairwise policies: sixteen-feature linear model; CPU PyTorch MLP16→32→1 with tanh. Static nine-feature imitation, pressure ordering,short-first and random are controls. CPU one thread; optional torch2.8.0+cpu. Training/model/report/code hashes recorded. Compact own MLP checkpoint and model.json saved under docs/evidence/phase3; external REST weights remain ignored.

## Held-out results

Fixed models,one fresh sequential construction per layout/method,1M/30s ceilings.64curriculum held-out seeds12001–12064;24denser original-generator seeds19001–19024. Distinct from training2001–2128 and all earlier validation seeds. No tuning on these reports.

| Policy | Curriculum legal/64 | Denser legal/24 |
|---|---:|---:|
| Context linear |42|7|
| Context MLP |42|8|
| Static linear |42|8|
| Pressure |42|7|
| Short-first |42|9|
| Random |36|6|

MLP vs random on jointly legal curriculum cases:13wins/10ties/9losses; on jointly legal denser cases:5wins/0ties/1loss. Against short-first curriculum:15wins/11ties/11loss; denser:3wins/2ties/2loss. Different feasible sets prevent averaging successful-only delay to claim overall superiority. This improves on random feasibility in this toy distribution but does not dominate simple controls or establish unseen official-case competitiveness. Not adopted as production default.

Official development screen,frozen models and3M/30s: intro05all six policies legal,delays context linear4149,MLP4065,static4221,pressure4085,short4335,random3999. Every hard01attempt incomplete; completed-net counts differ but are not scores. No official-tier model gain. Evidence learned-context-order.json,learned-context-official.json,learned-context-model.json and own MLP checkpoint.

## Fresh construction plus native refinement

Own Python fresh aggressive conflict-only hard01:10010/10218. Twenty-million-expansion native refinement reduces these to9206/9140;selected9068 still better at that comparison checkpoint. Intro05fresh4025/3887 reduces to3813/3765,beating selected3825. Own generation and refinement costs both count; not a uniform-budget comparison.

Separate compiled `fresh_probe.cpp` reuses our parser/search/checker via inclusion without modifying production engine. Fixed-point64 prices,rounded gradual increments,ceil-sqrt fanout,tight A*,first-legal construction followed by3polish passes. Original route input serves checked recovery only; all geometry is cleared before successful fresh construction. Incomplete attempts restore input and are explicitly labeled failures. This differs from Python floating-price/sqrt/search ordering; no speed comparison claimed.

Compiled screen:3development cases,two seeds,four combinations of aggressive/gradual and all-net/conflict-only,20M/30s each,1000round ceiling. Aggressive11/12freshlegal;gradual0/12. Each individually verified fresh result remains worse than our selected incumbent. Only three development cases,not a full-tier solver comparison. Actual expansions,rounds and failures are in fresh-cpp-screen.json. Shared timing with native workers invalidates isolated wall-speed claims.

## Exact selection and retained improvement

Generated per-net catalogs from own compiled fresh trees and own Python-fresh native refinements. Global CP-SAT enforces one tree/net and vertex-disjointness; base is newest complete native16/17tier output. Full hard9 and intro20 outputs officially rescored. All finite-pool selections OPTIMAL:hard0gain,intro60units from case05. Optimality is restricted to this candidate pool. Output intro score1.1126608486711733; no global bound claimed. Lower-cost fresh intro basin is retained through a zero-budget native checkpoint/archiving; all construction and selection provenance explicitly disclosed.

## Verification and next work

Five context-policy checks,three compiled-fresh checks plus existing four Python-fresh checks;100development tests pass together.41route hashes from earlier fresh probes previously checked; newest canonical45routes archived/restored/hash-matched. Production C++ source unchanged. First compiled-screen reporting attempt hit relative-path normalization error after legal checking; partial artifact retained,new absolute-output run completed,no incumbent harmed.

Next: improve fresh candidate quality rather than only ordering feasibility; test faithful cost-distance component reuse,then bounded native refinement from new basins. Learned policy should eventually choose repair groups/operators with whole-case legality and true-delay rewards. Current learned models are exploratory. Independent native continuation18/19 continues from newest selected outputs under declared75M/case60s caps.
