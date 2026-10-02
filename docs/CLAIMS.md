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

- Initial six-tier output coverage:45/45 officially legal; scores intro1.050409,hard1.212968,scale1.023686,stress1.002601,congested1.031234,designs1.121578. Evidence tier-coverage.json. Four tiers use attributed official reference warm starts;reference generation cost unmeasured. Separate scores,not independent initialization,final submission readiness,global optimum,or end-to-end reproducibility.

- Updated45/45legal tier outputs:scale1.029924,congested1.040655,designs1.138274,stress1.006780;intro/hard unchanged. Official tier-optimized-coverage.json. All16 newly targeted cases improve over initial coverage. Additional optimizer stages/single-seed screen/reference starts disclosed;no global optimum or equal-resource superiority claim.
- Matched stress initialization improvement44.143→0.424s,validation43.950→0.250s;252vs72 searches inside same60s cap. Single-case measured result only;large-case-profile.json.

- Current officialhard1.220250,congested1.055361,designs1.164826,stress1.020326;intro1.050409/scale1.029924 unchanged,45/45legal,tier-guided-coverage.json.17 incrementalcasegains. Seed1 fixedconfigs,siblings/inheritedcost and officialreference warmstarts disclosed.
- Relaxed analytic score ceilings(delay-bounds.json)are not achievable targets without legalconstruction. A*stress1020vs252searches under matched60s is unequalcompletedwork;no globaloptimality/general speedup claim.

- Currentcongested1.082668/designs1.212499 aftermeasured20sA*stageandoptionalcongestedfreshstage;all7targetedcasesimprove overprioroutputs. Officialtier-followup-coverage.json andcomparison,45/45all-tierlegal. Repeatedseeds supportA*6/6vssingleordinarycontrol representatives,not unseen-case/general superiority. Screencost223.803s separatefrom generation/stages. No newunitcheckclaim.

- Fixed10M expansion stress repeats produce identical C++ stdout and officially legal delay1121978, score1.0204335557381696. Independent selected-tier CLI rescore confirms45/45 legal;other tiers unchanged. Evidence tier-work-budget-coverage.json/work-budget-profile.json.31 focused tests pass. Determinism is conditional on identical implementation/config/inputs and no earlier wall/signal interruption.
- Public gap diagnosis is a checked geometry comparison, not proof of attainable per-net gains. Hard signed deficit21046;multi-sink nets contribute22212 whileone-sink aggregate is1166 lower locally. No public warm starts adopted.

- Currenthard1.2300004741250727,officiallylegal9/9;selectedalltiers45/45legal,otherfiveunchanged. tier-kernel-coverage.json andhard-long_cycles-validation.json/hard-tight_stage-validation.json. Sevenlongstagecasegains,fourtightstagecasegains;fixedconfigs,attributedancestorcosts,no fresh-runtime/globaloptimalityclaim.
- Storedgkerneloutputidenticaltocontrol,buttimingdoesnotestablishspeedup. Optionaltightlookahead lowershard/congestedrepresentativedelayatfixed5M expansions,stress unchanged. Two repeats/onecasepertieronly.31focusedtests pass;explicitper-moveownerinvariantsstillpending.

- Current hard1.2303243121958916 and congested1.08805956745537 after optional fine-price stage; all13 cases improve their preceding incumbents. Other four selected tiers unchanged; independently rescored45/45 legal in tier-pricing-coverage.json. Matched representative screen4wins/1tie/1loss; no universal superiority claim.31 focused checks pass, including fine-mode work-cap rollback/repetition.
- DATE11539267 identified and official abstract read; full text remains inaccessible. No claim of implementing or reproducing that paper. Six-link coverage and source-access limits in OPTIMIZATION_FOLLOWUP.md.

- Current hard1.2306575756801885 and congested1.090605391888499 after fixed tier-specific schedule stages. Independent tier-schedule-coverage.json verifies45/45selected outputs legal;otherfourtiers unchanged. Hard7gains/2unchanged,congested4gains.32focusedtests pass. No universal tuning optimum or fresh-generation runtime claim.
- User DATE PDF strict-parses all7pages and full extracted text was read. Source hash/content identity in date-paper-integrity.json; no pixel-level integrity or paper-implementation reproduction claim. Earlier abstract-only access status is superseded.
