# DATE2026 via/congestion paper: full-text review

Source: user-provided root PDF, `An_Adaptive_Cost-based_Via_and_Congestion_Co-optimization_Framework_for_VLSI_Global_Routing.pdf`.
IEEE11539267, DOI10.23919/DATE69613.2026.11539267. Authors: Zhaoyi Wu, Haishan Huang, Jianli Chen, Zhifeng Lin.

## Integrity and access

390900 bytes, SHA256 `8def9e934f4fd06969809868c3d5f23ca5a35dec8c3d89593635851326228c9e`.
`pypdf6.1.1` parses all seven pages in strict mode without errors; the file is not encrypted and all pages yield text. Header/trailer are present; metadata title and IEEE article ID match. This is a successful parser/content check, not a forensic certificate of every graphical element. Read all seven extracted pages. Optional reader pinned in dev/requirements-research.txt and installed only in .venv. The user's licensed PDF is preserved at the root and excluded from our commits; extracted text remains temporary under /tmp.

## What the full paper adds

The flow first builds a wirelength-oriented tree and reconstructs a spine topology to reduce bends; then routes its segments with a deque/priority-queue hybrid, assigns layers with tree DP, and performs3D RRR. It explicitly adopts CUGR wire/via cost models in initial routing and layer assignment. This narrows the earlier uncertainty: CUGR cost reuse is stated, but it does not prove the entire implementation is a fork of CUGR.

The final search combines historical congestion with nonlinear marginal overflow and a capacity-spreading penalty. Its via cost is discounted according to source congestion; the described maximum discount is50%. Some layers can disable the discount. The experimental objective is overflow/via count with similar wirelength. Neither the full paper's tables nor its claimed improvements measure this challenge's sum of driver-to-sink delay. Results are the authors' measurements, not reproduced here.

## Transfers worth testing

1. **Marginal overflow prices.** Compare a bounded nonlinear penalty with our linear present/history schedule. Map this to unit vertex capacity, not industrial track capacity. Paper thresholds35%/50% of capacity collapse for capacity-one discrete vertices and need a justified spatial-demand adaptation.
2. **Adaptive via search penalties.** Treat discounted via cost as a proposal heuristic; evaluate true physical delay and accept only legal improvements. A discount below physical via delay invalidates our existing physical A* bound unless the relaxed bound is reduced accordingly. Keep per-search costs fixed while searching or give an explicit dynamic-search correctness argument.
3. **Topology/layer DP.** Tree-segment delay should be multiplied by downstream sink count to target our objective, while resource price is consumed once per net. Restricted topology/layer optimality is not global routing optimality. Shared vertices, pin protection, path unions and acyclicity still need checking.
4. **Local two-terminal bidirectional repair.** It may help long branches; it is not a drop-in replacement for our multi-sink shortest tree. Via costs depending on the departure cell are directed, so backward search must use transposed costs.

## Implementation cautions

The printed bidirectional pseudocode shows only forward expansion despite the surrounding text describing alternating fronts; it is not a complete executable specification. Its stop conditions and heuristic assumptions need independent derivation before claiming exact search. The deque hybrid also does not establish ordinary Dijkstra/A* optimality for arbitrary weighted costs. We should not import these algorithms and label them exact based only on the paper's prose.

This reading informs hypotheses. No source copied, implementation reproduced, industrial result independently checked, or global-optimality claim made. Current controlled schedule sweep remains our original additive-price experiment; it does not implement this paper's nonlinear/discounted model.
