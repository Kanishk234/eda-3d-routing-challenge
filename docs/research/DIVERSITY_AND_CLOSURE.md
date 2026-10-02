# Diversified local archives and exact two-parent recombination

## Sources inspected

- [Glover, Laguna and Martí: Scatter Search and Path Relinking](https://www.uv.es/~rmarti/paper/docs/ss7.pdf). Read reference-set construction and neighborhood-space relinking sections. Keep quality and diversity together; multiple solutions can guide local moves. This motivates measuring our archive geometry, not blindly restarting worse solutions. Not a theorem about this contest.
- [Li et al.: Anytime MAPF via LNS](https://www.ijcai.org/proceedings/2021/0568.pdf). Revisited repair/selection experiments: cheaper repair can explore more neighborhoods, and preferred neighborhood sizes differ by instance. Permanent net ownership and branching trees differ from temporal agent collisions.
- [MAPF-LNS2 author repository](https://github.com/Jiaoyang-Li/MAPF-LNS2). Read project overview/build/algorithm context; no source copied or executed. Its time-step model is not directly applicable.
- [Gillard et al.: LNS with Decision Diagrams](https://www.ijcai.org/proceedings/2022/0659.pdf). Read restricted-width compilation and mustKeep sections. Preserving the incumbent path and pruning with a valid bound suggests bounded candidate-tree recombination. Width truncation generally limits optimality to retained candidates; not a global guarantee for our routing.
- [Picard: Maximal Closure of a Graph](https://pubsonline.informs.org/doi/abs/10.1287/mnsc.22.11.1268). Abstract/definition inspected; closure/min-cut reduction also appears in the search excerpt for [Princeton network-flow lectures](https://www.cs.princeton.edu/~wayne/kleinberg-tardos/pdf/07NetworkFlowII-2x2.pdf). The lecture PDF could not be opened by the browser because of its size,so only the search excerpt was available. Implementation below is independent; no third-party code adapted.

## Our restricted recombination derivation

Two independently legal complete solutions supply a base tree A_i and alternate tree B_i for each net i. Both all-A and all-B are mutually vertex-disjoint. Let x_i=1 select B_i. If B_i touches a vertex owned by A_j for another net j, legality requires x_i <= x_j. These directed implications capture every possible cross-parent conflict; same-parent conflicts are absent by verified legality. Terminals, branches and via endpoints all participate as vertices.

Physical cost is sum_i D(A_i)+sum_i x_i*(D(B_i)-D(A_i)). Thus minimize a weighted closed subset: source arcs represent negative deltas, sink arcs positive deltas, and dependency arcs have capacity greater than the sum of absolute finite costs. Source-reachable vertices after max-flow give the minimum delta. Cycles are valid. Python wide integers and residual-flow/closure checks retained. Existing official checker supplies independent per-net delay and validates the result. Exactness covers this two-tree-per-net candidate set only.

## Observations

Inventory selects geometry-diverse complete local runs within5percent delay on designsctrl/congested01. Net-labelled undirected-edge Jaccard distances0.555/0.939 are geometry proxies,not proof of separate local minima. Older own-run generation excluded from matched added-work timings but manifests retained.18legal3M trials,three seeds,25.552s wrapper:alternate continuation loses3/3 on both tiers. Donor guidance designs2wins/1loss,ratio1.00028202;congested3ties. Donor selections39/45 and improving donor-guided repairs2/0 respectively. No public warm starts.

Fixed designs donor/congested adaptive full7case continuation adds10.472s wrapper and improves all7. Designs1.2309315470922892;congested1.0988399406456149. Full designs stage has zero donor-labelled accepted moves; its gains are from ordinary repair/polish despite donor-mode selection. Do not attribute full-tier gain specifically to donor moves.

Maximally diverse two-parent recombination gives no improvement in either tier. Checking all7designs/8congested candidate archives against the fixed best base gives no designs gain and2less delay on congested01. Best pair chosen per case is disclosed portfolio selection; not an exact whole-pool solve. Recombination selection times5.777/10.050s exclude official rescorers; earlier rejected pair costs and all generation are separate. Zero-budget serialized checkpoint preserves the winning congested combination without further search. Final congested1.0988489911881147.200exhaustively enumerated random graphs plus explicit forced-dependency examples pass2 focused checks. Independent pinned CLI validates all45 selected outputs.

## Ranked next experiments

1. Neutral group moves with changed geometry, preserving the best legal checkpoint. Low implementation cost; speculative benefit is crossing equal-delay plateaus. Reject identical-tree no-ops; compare with strict improvement under matched work.
2. Several recent good parents rather than maximum-diversity old parents; iterative closure recombination. Moderate cost; pairwise exact moves do not prove whole-pool optimality.
3. Candidate beam/decision-diagram repair retaining incumbent choices. Higher cost; test small groups only, with explicit restricted scope and independent delay bounds.
4. Partial sink/branch repair with root-distance-aware boundary stitching. Highest correctness cost; requires coherent predecessor/tree contracts and proof of no cycles before timed experiments.
