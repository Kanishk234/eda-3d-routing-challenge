# Partial branch repair research, 2026-10-02

Reading scope: CUHK institutional abstract of Tu/Pui/Young (2018), https://research.cuhk.edu.hk/en/publications/simultaneous-timing-driven-tree-surgery-in-routing-with-machine-l-3/ . The authors describe topology surgery with global congestion-aware optimization; full paper not read. Their timing model/results do not transfer to this challenge.

CUGR project overview and source directory inspected: https://github.com/cuhk-eda/cu-gr . Its pattern/layer assignment and multi-level maze stages address detailed routability; no source copied and no claimed performance transfer. Cost-distance paper sections revisited: https://arxiv.org/html/2503.04419 . Implemented old-tree pricing is our separate heuristic.

Next proposed experiment: detach one rooted branch of a blocking tree, preserve the rest, and route the branch from a root-distance-labelled attachment frontier. Account for every downstream sink in physical objective; reject attachments into the detached component; protect retained terminals and reconstruct an acyclic tree. Roll back ownership on failure. Compare against whole-net repair with identical work ceilings on hard01/04/07, seeds1–3, retaining reserved08/09. First establish an independent tiny-tree oracle and legal interruption checks. This remains unimplemented; do not call it a measured improvement.
