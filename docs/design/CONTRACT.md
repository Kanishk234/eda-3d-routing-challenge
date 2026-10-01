# Official contract — checked October 1, 2026

Upstream main pin: 499ad7e2a415a97e9ce9b3396b0477e75ebd13e6. git ls-remote and GitHub commit API agree. Local fork HEAD initially d887a05b844f9aeda0f656ca4644c58969d41ec5; clean native WSL Git status. Only committed differences from upstream were research and an AGENTS.md ignore rule. Official code/data unchanged.

Sources: pinned [README](https://github.com/partcleda/eda-3d-routing-challenge/blob/499ad7e2a415a97e9ce9b3396b0477e75ebd13e6/README.md), [CONTRIBUTING](https://github.com/partcleda/eda-3d-routing-challenge/blob/499ad7e2a415a97e9ce9b3396b0477e75ebd13e6/CONTRIBUTING.md), [workflow](https://github.com/partcleda/eda-3d-routing-challenge/blob/499ad7e2a415a97e9ce9b3396b0477e75ebd13e6/.github/workflows/leaderboard.yml), [checker](https://github.com/partcleda/eda-3d-routing-challenge/blob/499ad7e2a415a97e9ce9b3396b0477e75ebd13e6/m3d/checker.py), [scorer](https://github.com/partcleda/eda-3d-routing-challenge/blob/499ad7e2a415a97e9ce9b3396b0477e75ebd13e6/m3d/scorer.py), model.py, grid.py, suite.py, cli.py and docs/FORMATS.md. Recheck before submission.

## Model and scoring

Integer vertices (x,y,z) lie within grid bounds. Neighbor X/Y steps cost layer_delay[z]; fixed-XY adjacent-layer vias cost via_delay. Read dimensions/delays from each instance. Cell rectangles are not blockages; foreign pins are unavailable. Different nets cannot share vertices or edges; vias occupy both endpoints. A net's own branches may share a trunk.

Exactly one route per net, connected acyclic tree spanning all terminals. Checker rejects duplicate/self-loop/non-neighbor/out-of-bounds edges, missing/unknown/duplicate nets, cycles, disconnections, foreign-pin traversal and shared resources. Illegal case total_delay is null.

D = sum over nets/sinks of driver-to-sink tree-path delay. Trunks count per downstream sink; wirelength/congestion costs are different quantities. Legal positive-delay ratio = baseline_total / D. Tier aggregate = exp(mean(log(ratio))) over all manifest cases. Missing/illegal cases give zero aggregate. Tiers rank separately; runtime never enters primary delay score. Baseline normalization comes from committed suite.json.

## Released inventory

evidence/phase0/inventory.json records all case names/seeds/grids/delays/baseline totals and case/reference SHA256.

- intro: benchmarks, case_01–20; 20 cases; 1,536–50,784 vertices; 6–139 nets.
- hard: benchmarks_hard, case_01–09; 9 cases; 3,456–9,600 vertices; 62–104 nets.
- scale: benchmarks_scale, case_01–08; 8 cases; 60,000–146,016 vertices; 170–265 nets.
- stress: benchmarks_stress, case_01; 1 case; 1,685,400 vertices; 901 nets.
- congested: benchmarks_congested, case_01–04; 4 cases; 24,576–80,736 vertices; 166–302 nets.
- designs: benchmarks_designs, ctrl/int2float/router; 3 cases; 35,574–66,150 vertices; 182–344 nets.

Total 45. Generic README/CLI “20 cases” wording refers to intro; evaluator iterates each actual manifest. suite.py synthetic TIERS excludes designs; cli.py adds it separately.

## Submission and CI

Route JSON only; judges do not execute solver. Schema: format=m3d-submission, version=1, instance=case name, routes=[{net: integer ID, edges: pairs of integer vertex triples}]. Emit correct integer coordinates/version/name even where parser validation is permissive; do not exploit coercion.

Layout: submissions/<tier>/<method>/<case>.sol.json for every required case, meta.json (author/method/url/date template), optional runtime.json mapping case names to seconds. verify_submissions.py permits missing files but only complete legal tiers rank. Existing negotiated_fast seed is intentionally 8/9 complete.

Contribution rules: method files and regenerated LEADERBOARD.md only. Workflow path guard activates on a submissions/ change and permits only submissions/** and LEADERBOARD.md. CI runs stdlib tests on Ubuntu/macOS Python 3.9/3.12, verifies present routes and checks leaderboard. Locally verified WSL Python 3.12.3 only; other matrix environments unrun.

Any language/hardware allowed. No fixed solver runtime cap, deadline, prize or hidden-test protocol found in inspected rules. This is an observation about current documents, not future policy. Runtime is optional/separate. Public-output reuse requires attribution and separate from-scratch claims; no participant route was reused here.

## License and public evidence

Toolkit MIT, copyright 2026 Partcl, Inc. Vendored EPFL BLIF designs MIT; preserve designs/EPFL_LICENSE.txt and PROVENANCE.md. No third-party router adapted/downloaded.

evidence/phase0/upstream.json captures all 11 PR heads (no further page): 9 open, 2 closed (#6,#11), none merged. Heads agree with research; #11 is now closed. Research scores were not re-audited. Latest 10 CI runs captured include failure/action_required states; metadata alone does not establish their causes or every entrant's CI acceptance. Recheck relevant jobs before relying on results. Fixed Pareto-test risk in BUGS.md.

Final CI check: the pinned upstream HEAD's push workflow completed successfully, [run 36622967607](https://github.com/partcleda/eda-3d-routing-challenge/actions/runs/36622967607). This differs from recent participant PR runs. Evidence: api.pinned_head_actions in upstream.json.

Current-rules recheck October1: upstream3d8948fdcd6f87165d5ca1efbf4b65e8168e8e81; contribution/workflow bytes match pin. New commits fix Windows UTF-8 I/O in cli/verify/test files; benchmark/checker/scorer unchanged. Experiment authority remains pinned499ad7e. Evidence in phase3/submission-contract-recheck.json and upstream-change-recheck.json.
