# Exact recent-state memory for neutral group exploration

Hypothesis: accepted equal-delay moves can revisit a recent full routing geometry;rejecting those returns may leave more expanded-vertex effort for useful alternatives. This is a bounded tabu-style experiment,not a guarantee of escaping a local minimum.

Optional neutral_tabu0..64(default0) stores exact canonical integer descriptions of every net's ID,root,and sorted undirected edges. It uses exact vector equality,not probabilistic fingerprints. Initialize on first repair,remember accepted group states,and clear history after a strict group improvement. Only registered equal-delay candidate revisits are rejected. Foreign pin protection,physical acceptance and rollback remain unchanged. Ordinary polish may change geometry outside this history;finite memory does not eliminate all cycles. Existing legacy uphill presets are outside the measured experiment.

Memory grows with history size times current route edges. A legal state has at most2Mvertices under the engine contract,so64descriptions may require about1GB of integer storage in the worst supported case,plus other buffers. Current screen uses small hard/designs/congested representatives and records actual peak RSS,history bytes,and bookkeeping time. Disabled default stores nothing and does not alter route output.

Focused crossing property exercises actual repeated-state rejection;histories1/8/32,workcaps1/20/100/1000/10000,2/5second safety budgets preserve deterministic stdout and official legal/nonworsening rollback. Default/explicit0match;negative/65rejected.42focused engine checks pass before the screen. Compare0/8/32 onhard01/designsctrl/congested01,seeds1–3,10M each from the frozen priced checkpoint. Predeclared gate requires2wins and geometric delay ratio>1. Rejected candidates and bookkeeping overhead are not proof of a score improvement.

Measured result: neutral-tabu-screen.json has18 ties across history8/32 versus0 on three representatives/seeds. Reject adoption.
