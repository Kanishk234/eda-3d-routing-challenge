# Capacity-aware delay bounds

`dev/dual_bound.py` builds an isolated analysis translation unit from the frozen native engine. It does not change solver defaults or submit its relaxed paths. Own legal routes supply an upper bound and input encoding;other-net ownership is then relaxed while foreign pins remain unavailable. Nonnegative vertex tolls are the coupling device. All shortest-path heuristics remain admissible.

## Why the bound is valid

Let λ_v≥0. For any legal full solution,each vertex belongs to at most one net,so D≥Σ_n min_T[D_n(T)+Σ_{v∈T}λ_v]−Σ_vλ_v. Computing the per-net tree minimum exactly is hard;we bound it from below in two ways:

1. Uniform allocation:for m sinks,sum independent shortest-path costs using physical delay plus λ_v/m on each arriving vertex. Any real tree uses each vertex in at most m sink paths,so these allocated tolls never exceed its full tree toll.
2. Critical sink:for each sink s,its shortest path with the full toll,plus all other sinks' independent physical shortest paths. This is also at most any real tree's delay-plus-toll objective. Take the maximum across s and the uniform bound.

The maximum of valid lower bounds remains valid. Subtract all vertex tolls after summing per-net bounds. Driver toll omission only weakens the bound. Terminal tolls are kept zero. Prices use either whole units or sixteenths;physical priorities use1024fixed units. Flooring per-edge allocated tolls is conservative. The global toll subtraction is exact because1024is divisible by16. Taking a ceiling of the resulting bound is valid because physical delay is integral.

The projected update is a heuristic for finding useful prices,not a certified exact dual optimizer. Fractional prices and adaptive steps avoid the initial integer-price overshoot. The strongest recorded bound is preserved across iterations;weak subsequent iterates cannot erase it.

## Checks and observed results

Three independent hand checks pass:single-net two-sink optimum8;slow-layer plus vias optimum14;contested multi-sink instance with independent lower bound7 and independently checked restricted optimum9. Both uniform and critical-sink models remain below9. Work-slice interruption tests are separate.

Initial24iterations with coarse prices did not improve the empty-price bound.32iterations with critical-sink allocation likewise overshot.64iterations with fractional prices and adaptive steps improved hard01from7156to7793,hard04from10253to11265,hard07from16461to17825. These are **lower bounds on delay**,not better legal routes. Their implied score ceilings are upper bounds,not reachable targets.

Full9hardcase report: `docs/evidence/phase3/dual-routing-bounds-full-hard.json`. It records the official geometric score ceiling,the weaker independent-path ceiling,incumbent score and every price-iteration trace. No six-tier aggregate is formed. These bounds are specific to the pinned published cases and do not establish a global optimality gap as small as the observed price optimization permits;stronger relaxations may close more of it.

## Next refinement

Use high-price cuts to guide neighborhood selection,then measure actual legal delay gains. Add richer per-net capacity relaxations or exact small-net priced-tree solves before assuming CPU search has reached a quality cap. The bound itself is an analysis tool and should not be counted as an algorithm score gain.
