# Sampling and fusion follow-up

## Primary sources inspected

- [Reevaluation of Large Neighborhood Search for MAPF](https://arxiv.org/html/2407.09451), abstract, neighborhood/overhead discussion and RandomWalkProb appendix. Repeated delay-weighted agent sampling motivates our repeated gap-weighted net proposals. Static vertex-disjoint routing trees differ from temporal MAPF; performance findings do not transfer automatically. [Author repository](https://github.com/ChristinaTan0704/mapf-lns-unified) overview inspected; no code copied or executed.
- [Selecting Nets to Rip Up and Reroute via SAT](https://www.cse.cuhk.edu.hk/~byu/papers/J166-TCAD2026-SATRoute.pdf), abstract/introduction and net-selection formulation inspected. Candidate conflicts could guide restricted selection. Its overflow/design-rule objective differs from sink delay. Our incumbents have no overflow; candidate-route conflicts would be needed. No SAT implementation or result claimed.
- [Fusion Moves for Markov Random Field Optimization](https://pubmed.ncbi.nlm.nih.gov/20558873/), abstract inspected. Author PDF request timed out; no full-paper reading claim. Combining candidate solutions motivates repeated restricted tree fusion.
- [Fast Approximate Energy Minimization via Graph Cuts](https://www.cs.cornell.edu/rdz/Papers/BVZ-pami01-final.pdf), opening abstract/introduction and metric conditions inspected. Large candidate moves motivate repeated two-parent closure solves. Their approximation guarantees do not apply to our hard capacity constraints.
- [CUGR multi-net directory](https://github.com/cuhk-eda/cu-gr/tree/master/src/multi_net), directory inventory only.

## Implemented hypotheses and evidence

Repair sampling0 preserves the unique shuffled sweep. Modes1/2 draw seeds with replacement, weighted by positive relaxed-delay gap plus0.01, optionally divided by route footprint. Group membership retains a separate unique ordering. Weights refresh per pass; footprint is an uncalibrated cost proxy. Defaults and physical acceptance remain unchanged. Weighted screen18legal exact10M trials: designs both modes lose3/3; congested gap-only loses3/3 and normalized mode wins1/loses2. Reject adoption on both tiers. Fewer attempted groups and many over-cap groups suggest checking eligibility/cost before further bias; counts are not profiling proof.

Fusion tie preference uses delta*(n+1)-1 per alternate label. A unit physical improvement dominates all n secondary label rewards, so minimum physical delay is preserved within the two-parent candidate set. It maximizes selected donor labels among primary optima, including identical trees; this is not a changed-tree count. Independent exhaustive lexicographic oracles cover140 additional random dependency graphs. Two sweeps over the same frozen archive pools yield10 less delay on congested03 with strict fusion; preferring donor labels yields no additional physical gain. Designs gains zero. Neither restricted exactness nor bounded sweeps proves global routing or pool optimality; neutral cycles remain possible.

Hard neutral screen:5wins/4losses at matched10M work across01/04/07,seeds1–3; optional retention, mixed outcomes. Fixed full-tier continuation improves7/9; reserved08unchanged/09improves. Follow-up designs/congested uses ordinary shuffled seeds and existing neutral adaptive repairs. Full-tier continuation adds effort and does not establish matched-budget superiority.

Next: profile eligible group formation and repair cost, then compare a bounded diversified fresh-start portfolio against continued incumbent search. Candidate compatibility/SAT selection remains a separate unimplemented option.
