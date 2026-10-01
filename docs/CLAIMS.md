# Claims — 2026-10-01

Established:
- Unchanged pinned upstream passes 43 tests on WSL Python 3.12.3 (20261001T165828.977754Z-tests). Other matrix variants not tested.
- Intro/case_01 official baseline legal 240, ratio 1.0; two runs yield identical bytes (20261001T165835.673740Z-smoke, 20261001T165954.462184Z-smoke). One case, not a tier/custom solver claim.
- All 26 present seed routes legal; leaderboard current (20261001T165836.044251Z-ci). negotiated_fast intentionally incomplete.
- Intentional process timeout rejects candidate and preserves previous validated artifacts (20261001T165954.996009Z-smoke); not optimizer-checkpoint evidence.
- CPU environment and C++17 toolchain work; all 198 official archived files match pinned Git blobs and stayed unchanged.
- Current inventory 45 cases/six tiers with hashes; upstream HEAD matches research pin today.

Not claimed: competitive gain, new best, tier result, global optimality, custom solver reproducibility/generalization, GPU speedup, matched public-entry comparison, or solver success on all cases. Research audit/bounds remain historical. Proposed shortest-path/negotiation/advanced repairs await implementation and evidence.

## Phase 2 established claims

Earlier not-claimed tier/custom-solver statements describe Phase0. Current evidence in phase2/comparison.json: all9 hard outputs legal, aggregate1.0466292119096317; all case delays improve over baseline. Repeated seed1/pass5 output hashes agree.13 kernel checks pass; independent official CLI rescore agrees. Baseline warm start required; no public warm starts, global optimality, speedup or unseen-case generalization claimed. Audited PR3 output1.387366 remains better.

Phase3 initial screen:21 development runs (hard01–07,seeds1–3) officially legal/nonworsening,0 improved. No full-tier aggregate, optimization gain or failure-cause claim.15 kernel checks pass; group transaction coverage remains limited.

Phase3 soft repair: fixed seed1/5passes/2s config gives9/9 legal hard score1.0529719287378287;8 improve,1 unchanged vs Phase2. Official CLI rescore agrees. Development seeds1–3:18/21 improved.16 kernel checks pass. Sum baseline+polish+repair wrappers101.865s is component accounting,not fresh end-to-end timing. Evidence: phase3/soft-validation.json.

Driver-aware attachment matches exact costs on546 isolated-net reconstructions; zero-source case sums worse for7/7 development cases. Not tier results.17 checks pass. Current upstream rules/CI rechecked at3d8948f; unchanged vs pin,with Windows encoding-only upstream change per compare metadata.

Negotiated fixed config hard9/9 legal1.0710212727385569,19 tests pass;21/21 development improve vs Phase2,2 regressions vs soft. Independent official rescore. Latest public hard audit13 heads117 legal routes:highest checked closedPR11 mj97 1.3873941742426144;highest openPR3 1.387366331135629. No solver runtime reproduction or adoption as warm starts.

Basin experiment:22 checks pass;fixed seed1 exploration after negotiated improves all9 hard cases,official1.1059077449039443. Three-seed development aggregates improve but3 case regressions vs negotiated exist. Whole restart9/21 gains,rest retained originals. No global-basin diagnosis,novelty,source reproducibility or exact global-selection claim.

Wide10s/100 cycles fixed seed1 hard9/9 legal1.1834968761196418,all improve vs1.105908;official rescore. Longer matched representative budgets show4.1–5.3% delay gains,no convergence. Stage wrapper91.845s,component total208.868s excludes screening/scoring.

Threshold extra stage fixed seed1 hard1.1868734408645938,9/9 legal,6 improve/3 unchanged;official scorer.26 tests pass. Representative matched walk vs descent6 wins/3 regressions;counter includes equal-delay moves. Traced retained component pipeline228.868s excludes all screen/scorer costs;not fresh end-to-end.

Fanout stage fixedseed1 hard9/9 legal1.2054914475674077,allimprove vs1.186873;officialrescore,28 checks. Compact groupconstruction rejected asdefault despiteoftenfewervertices. Traced retained component pipeline320.758s excludes experiments/scorers;no algorithm-speedup or fresh-reproducibility claim.

- Fixed seed1 fanout restart-plus-polish stage yields official hard score1.2093700886234824,9/9 legal,one incremental improvement. Evidence restart-polish-validation.json and fresh-start-comparison.json;29 checks pass. Component generation cost407.192s excludes experiments. No independent-initialization reliability, global optimum, public-best, or final reproducibility claim.
