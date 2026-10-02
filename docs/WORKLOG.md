# Worklog

## 2026-10-01 — Phase 0 complete (America/Chicago)

Start: native WSL /home/younix/eda-3d-routing-challenge; clean HEAD d887a05b844f9aeda0f656ca4644c58969d41ec5, origin Kanishk234 fork. Read AGENTS.md and existing docs/M3D_ROUTING_RESEARCH.md (requested docs/research path absent). Supporting continuity docs absent. Preserved original research; created byte-identical copy under docs/research/.

Added dev/setup.sh, stdlib-only requirements, dev/measure.py, capture_environment.py, one-time finish_phase0.py, toolchain probe and README; ignore rules for bulk dev artifacts/snapshot; versions/contract/architecture/verification/experiment docs; decisions/bugs/claims; phases 0–5; summary and compact evidence. No official toolkit/data, submissions, leaderboard, Git history/remotes or global Git settings changed.

Current official revision 499ad7e2a415a97e9ce9b3396b0477e75ebd13e6, git ls-remote/API agree. 45 cases: intro20/hard9/scale8/stress1/congested4/designs3. Captured all 11 PR heads/latest10 CI runs; #11 now closed. Research numerical audit not repeated. Licenses/schema in design/CONTRACT.md.

Checks:
- 20261001T165828.977754Z-tests: 43/43 pass; process wall6.338s, RSS21,872KiB. Pre-existing ResourceWarnings logged, no test failures.
- 20261001T165835.673740Z-smoke: baseline/evaluate legal240, ratio1.0; baseline process0.064s, RSS14,976KiB.
- 20261001T165836.044251Z-ci: 26 present seed files legal, negotiated_fast intentionally8/9; leaderboard current. Verification0.366s/check0.466s.
- 20261001T165954.462184Z-smoke: repeat legal240, same route bytes; baseline process0.115s, RSS14,848KiB.
- 20261001T165954.996009Z-smoke: deliberate0.001s timeout, failure recorded, no accepted output, previous runs preserved; RSS unknown.
- GCC13.3.0 C++17 probe compiled/runs, Python syntax verified, all198 archive files match pinned Git blobs and unchanged by checks.

Compact evidence: docs/evidence/phase0/{upstream,environment,inventory,runs,official-input-hashes}.json. Raw logs/manifests/routes: ignored dev/artifacts/<run-id>/. Official archive: ignored dev/upstream/499ad7e2a415a97e9ce9b3396b0477e75ebd13e6. Exact commands in dev/README.md.

Remaining: upstream fixed hard Pareto-test risk and harmless unclosed-file warnings. Sandbox/patch/Node helpers failed; approved WSL/PowerShell fallback worked. Cgroup quotas unknown, CMake absent/unneeded. No custom solver/full-tier reproduction/profiles. No GPU/costs/commits/push/publication/unbounded runs.

Running jobs: none. Phase0 complete; Phase1 first unfinished. Next concrete action: .venv/bin/python dev/measure.py suite --suite benchmarks --router baseline --budget 180; retain per-case agreement, then officially rescore a relevant pinned public hard entry with attribution. Finalize small/large profile cases before tuning, respecting hard case_08–09 and seeds9001–9003 as validation. Do not jump to advanced optimization.

Final review: git diff --check and Python syntax checks pass; official-path diff empty, original research preserved, no running routing jobs. New text reviewed. Pinned upstream HEAD CI push run 36622967607 succeeded, captured in upstream.json. Phase 0 has no outstanding gate blocker; next is the bounded Phase 1 reproduction above.

## 2026-10-01 — Phase 1 active

Continued on user instruction; no transfer to another person/agent. Reproduced intro 20/20 and hard 9/9, every delay exactly matches official normalization and aggregate 1.0. Clean hard suite: 94.765 seconds, 22,080 KiB peak RSS, cap600. Intro suite: 55.676 seconds, 28,572 KiB, cap180; its tail overlapped the first hard attempt by about1.3seconds so runtime is marked non-isolated. Early hard run interrupted after45.208seconds and retained; excluded from claims.

Pinned PR3 hard output audit: 9/9 legal, aggregate1.387366; original public output/provenance retained separately, no public solver executed or copied. Small hard/case_01 profile complete: route13.109seconds under cProfile, 431 searches, 369 repeated calls, 26,652KiB RSS; checking/save/reload are milliseconds. Large scale/case_08 profile currently running, cap300seconds, one worker.

Renamed dev/inspect.py to capture_environment.py after discovering Python stdlib shadowing; added main guard. That bug unintentionally refreshed Phase0 environment/upstream JSON; official data and existing route/score evidence unaffected. Logged in BUGS.md. finish_phase1.py must be run after profiles finish; a premature call stopped on the active manifest after validating/promoting baseline incumbents and writing comparison.json.

Current baseline incumbents: dev/artifacts/incumbents/{intro,hard}, all officially rechecked; no public warm starts. Development source snapshots now retained inside Phase1 run directories. Next: finish large profile, freeze evidence and Phase1 summary, then implement the first C++ exact single-net kernel in Phase2. No optimization launched.

Phase 1 completion: both profiles finished legally, large scale08 route134.012s/search133.947s, peak62,536KiB; no reroutes. finish_phase1.py froze comparison/runs/profiles evidence and verified every output hash plus all official-input hashes. Phase1 checklist/summary complete, no jobs running. Proceeding to Phase2 C++ exact single-net rerouting from verified baseline incumbents; search dominates and justifies compiling the kernel. This is disclosed baseline warm-start work, not from-scratch competitive routing.

## 2026-10-01 — Status and commit audit

Read continuity/design/evidence docs, research summary, development kernel/wrapper/tests and saved run manifests. No solver runs or tests launched during this audit; no Git commits/publication performed. HEAD remains d887a05. All subsequent development is uncommitted. Official toolkit/benchmarks/submissions/leaderboard have no working-tree changes.

Phase0/1 complete. Phase2 is implemented in part despite stale “not started/no solver” text: dev/solver/exact_polish.cpp, run_polish.py and test_exact.py exist, with a built kernel. Saved kernel-tests.log records11 passing checks (0.141s). Full hard run20261001T173145.097188Z-exact-polish records9/9 legal, aggregate1.0466292119096317,547 accepted replacements, core process wall0.555730s and peak4352KiB; repeat173324 records identical case delays/aggregate, wall0.638549s. Config seed1,5passes,10s/case cap, validated official baseline warm starts. This excludes baseline generation (94.765s) and Python wrapper overhead; no from-scratch speedup claim. Saved zero-budget/resume case01 runs succeed. Official-input unchanged checks are true in these manifests.

Remaining: reconcile OVERVIEW/ARCHITECTURE/VERIFICATION/EXPERIMENTS/CLAIMS/PHASE2 and dev/README with these artifacts; freeze compact Phase2 evidence/source and perform gate review before marking completion. Reserved hard08–09 appear in the initial full-tier verification; preserve them from tuning. Phases3–5 not started; no submission prepared. Bulk ignored artifacts need separate backup. No routing jobs observed during audit. Next concrete action: finalize Phase2 evidence and documentation, including total warm-start cost, reproducibility/output hashes, limitations and matched-budget comparison. Suggested user commits: development harness; kernel/wrapper; kernel checks; documentation/evidence.

## 2026-10-01 — Phase 2 complete

Rebuilt C++17 polisher, added disconnected/resource-conflict fixtures (13 checks pass), compiler identity/wrapper wall measurement and exact reloaded-delay acceptance. Fresh full hard runs212729/212755/212816 reproduce earlier output hashes/score1.046629;9/9 legal and every case improves. Zero-budget212759 retains baseline; resume212819 retains accepted improvement. Independent official CLI score-suite executed by finish_phase2.py confirms aggregate; official hashes unchanged. Compact evidence/report in docs/evidence/phase2/, complete summaryPHASE2 and reconciled design/claims/readme. Shared600s routing envelope: paired baseline94.765s plus wrapper3.186s =97.952s; no speedup or fresh end-to-end claim.

No coordinated optimizer, publication or Git commit. No running jobs. Raw artifacts ignored and require backup. Phases0–2 complete for baseline-plus-polish pipeline. Next: Phase3 controlled development on hard01–07, beginning coordinated blocker repair/congestion comparisons while retaining validated incumbent; hard08–09 remain validation-only.

## 2026-10-01 — Authorized commits and Phase3 first screen

User explicitly authorized local commits, overriding the session Git prohibition for this step. Earlier four commits already present: b806c93,c42c912,49d779e,04a429b. Created c3c32b2 for remaining Phase2 completion. Default sandbox Git write failed read-only; approved escalation succeeded. No push/publication.

Implemented experimental max4-blocker group repair with full snapshot rollback, --mode repair and dev/phase3_screen.py.15 kernel checks pass.21 serial runs on hard01–07,seeds1–3,2s/case,5passes:all legal,none improved; core1.621s/wrapper11.576s. Saved compact evidence, negative result and in-progress summary. No validation tuning/public warm starts. Operator rejected as default; cause unmeasured. Phase3 remains active.

No running jobs. Next concrete action: instrument proposal skip/repair/rejection outcomes and independent group transaction fixtures, then choose the next operator from measured failures. Root-aware/negotiation comparisons remain required. Current best hard score1.046629 unchanged. Commit experimental solver/tests/screen and documentation/evidence separately.

## 2026-10-01 — Phase3 measured soft repair gain

Instrumented plain repair:1638 proposals,1371 too-large,150 attempts,54 failures,96 nonimproving. Added penalty4 per occupied vertex for candidate selection, separate physical predecessor-path scoring. Same21 development runs:18 improve,all legal. Fixed seed1/5passes/2s configuration validated all9 hard:8 improve,1 unchanged,aggregate1.0529719287378287. Both reserved cases improve. Official CLI rescore agrees;16 checks pass. Selected run20261001T213751.861916Z-exact-polish,core2.149s,wrapper3.913s; summed generation/polish/repair101.865s. No portfolio seed selection. Compact diagnosis/screen/validation evidence and updated summary/docs. Retain soft repair,plain operator rejected.

No jobs running. Phase3 incomplete: root-aware construction/negotiation controlled comparisons and additional group fixtures next. No public warm starts or publication. Local commits authorized by preceding user instruction; group algorithm/tests/tools and evidence/docs separately. Current accepted run routes remain under ignored artifacts and must be backed up.

## 2026-10-01 — Driver-aware ablation and submission-path recheck

Implemented exact/root-aware/zero-source isolated-net construction ablation.546 nets on hard01–07 complete; root-aware costs match exact per net,zero-source sums worse on7/7 cases. Results are not jointly routable tier scores; incumbent outputs unchanged.17 checks pass. Added attachment-ablation.json and interpretation.

User asked whether dev is appropriate: rechecked live upstream rules/workflow,byte-identical to pin. Current HEAD3d8948f adds Windows UTF-8 fixes only (cli/verify/test). No benchmark/checker/scorer changes. Source/docs belong in development checkout; final route/meta files plus leaderboard in clean submission checkout. Sandbox network failed DNS; approved read-only network check succeeded. Evidence captured.

No routing jobs running. Current best1.052972 unchanged. Next concrete action: bounded group negotiated-congestion repair with transaction rollback; compare against soft sequential repair on hard01–07 before reserved validation. Phase3 remains active,negotiation gate unfulfilled. Local commits authorized; no push/publication.

## 2026-10-01 — Negotiation/public target audit and report repair

Negotiated21-run screen completed:all legal/improve over Phase2,2 case05 regressions vs soft. Full fixed seed1 validation1.0710212727385569,9/9 legal,official rescore,19 checks pass;selected214526 run,core6.594s/wrapper8.233s. Local commits e3c03f2 and774f502 created. Discovered freezer report-path bug:soft report overwritten;restored from4bbf016 and preserved negotiation separately,conditional path fixed. Attempted summary write had stopped before docs;now actual state updated. No affected route/score result.

User requested current best target:read all14 current PRs,13 routing heads including closed,downloaded117 hard outputs and officially rescored. All legal. Highest checked closedPR11 mj97 1.3873941742426144;highest openPR3 1.387366331135629. New12/14 below. Closed11 fork deleted;read preserved upstream commit with fallback. Source heads/hashes/evidence stored separately;no public warm starts.

No running jobs. Measured Phase3 gates satisfied,but continuing optimization before final freeze due gap. Next concrete action:deterministic alternate equal-cost predecessor choices and controlled plateau/neighborhood repair on hard01–07,holding08/09 for validation. Current best1.071021. No publication;authorized local evidence/report repair commits next.

## 2026-10-01 — Alternative basins and parallel research

User requested entirely different approaches/research. Implemented original exact equal-cost tie ranks and sideways legal moves followed by negotiated repair.21 development trials:all improve vs Phase2;18 improve/3 regress vs negotiated;all3 dev aggregates improve. Fixed seed1 explore after negotiated routes,run215550:9/9 legal,all improve,official1.1059077449039443;core9.080s/wrapper10.837s.22 checks pass;stage sum117.023s excluding screens/scorers.

Implemented whole-instance fresh geometry negotiation with100-round cap and rollback.21 dev runs2s/pass5:9 improve;rest preserve original. Separate case01 10s/pass1 pilot215416 improves10854. Fresh-start not default under2s cap. Both screen/validation evidence retained;no per-case seed selection. Literature/public-source inspection overlapped some run time:read-only low-load browsing/downloads,not CPU-heavy competing jobs. Timings remain local samples,not algorithm speedup claims.

Inspected primary PathFinder/SALT/MAPF-LNS2/NDP papers andMIT IrwinJam/m3d-router source0027d807(no execution/copy). Research followup notes alternatives/objective mismatch;next restricted candidate-tree selection/expanded neighborhoods/controlled uphill search. No public warm starts. No jobs running. Phase3 optimization continues,current hard1.105908. Local commits authorized;no publication.

## 2026-10-01 — Autonomous progress,selection/wide screens

User explicitly authorized continued local commits/progress and will push. Implemented bounded compatible candidate-tree selection;21 dev runs9 improve vs Phase2,967 finite-set searches exhausted,most no improvement. Added wide equal-delay/negotiated operator(max12 blockers,24 rounds):21/21 legal/improved vs Phase2,matched caps/seeds. Bundle comparison/regressions retained.25 tests pass. Initial compiler indentation warning fixed.

No screen jobs running. Current full-tier best still1.105908. Next:commit operators/screen evidence,validate fixed seed1 wide stage from current full-tier incumbent,then budget scaling on development before more validation. No push/publication.

## 2026-10-01 — Two-second budget clarified and expanded

Explained2s as local matched screening only. Added dev/budget_screen.py:cases01/04/07 seed1/100 cycles fromplateau starts,2vs10s all longer runs improve4.1–5.3%,all capped. Fixed10s stage validated hard9/9 legal1.1834968761196418,all improve vs1.105908. Official CLI rescore;run220349,core90.135s/wrapper91.845s,component pipeline208.868s excluding screens/scorers. Current best retained under this run/routes. No jobs running. Commit measured budget expansion,then continue legal threshold-walk experiments with separate best-state snapshots. No publication.

## 2026-10-01 — Continued after commits,controlled threshold walk

Createdbd159c1 then continued without permission stop. Implemented walk/descent paired modes,protected best legal nets/owner snapshots. Walk threshold1% group worsening/probability1/4;sideways included.9 representative trials all improve overstarts;6 beat descent,3 regress;226 sideways/uphill accepts. Fixed seed1 extra2s/100 stage after10s wide,run220917:9/9 legal,6 improve/3 unchanged,official1.1868734408645938.26 tests pass;full score independently recomputed. Stagecore18.225s/wrapper20.000s. Added generic screen case/seed/budget/warmstart controls(prohibits08/09),recursive provenance/timing chain in report,component sum228.868s excluding all independent screens/scorers. One missing Path import stopped freezer before writing;fixed and rerun,no route impact.

No jobs running. Current accepted routes220917/routes. User will push,local commits authorized. Next concrete action:compact near-shortest construction/fanout-aware congestion hypotheses under matched development caps,separate best legal checkpoints;broader independent restarts after targeted measurement. No final freeze/publication.

## 2026-10-01 — Resource-price improvement

Added compact(alpha3/4) andfanout(congestionprice/ceil(sqrt(sinks))) groupvariants,keptphysicalscoring separate.27representative outputs legal,matchedwidecontrol:compact3/9wins/allseedaggregates worse;fanout7/9wins/allseedaggregates better. Resourcecounts measured fromretainedroutes;compact7/9 fewervertices yetworse delayillustrates objective mismatch.28 checks pass inclsharedtrunk resourcecount. Fixedseed1 fanout10s/100stage fromwalk,run223212:9/9legal,allimprove,official1.2054914475674077;core90.122s/wrapper91.890s,componentchain320.758s excludesallscreens/scorers.

Currentbest223212/routes. No jobsrunning. Commitmethods/evidence,thencontinue fresh-start initializationwithfanout/compactvariants onrepresentativedevelopment casesbefore anynewfullvalidation. No publication,userpushes.

## Fresh initialization followed by physical polish

Compared original, fanout-priced, compact, and fanout-plus-polish whole-instance restarts on development cases01/04/07, seed1, ten seconds, at most five starts. Polishing each legal fresh state before comparison produced delays9682/15223/28111, versus unpolished fanout9996/15681/28111. Some fresh searches fail to find legal states under this cap; prior verified routes remain the fallback. Internal fresh_legal counters are feasibility observations, not separately officially checked outputs. Evidence: fresh-start-comparison.json.

Fixed configuration then ran after the current fanout incumbents on all nine hard cases. Run20261001T224311.948014Z-exact-polish is officially legal9/9, score1.2093700886234824: case01 improves9966→9682, eight unchanged. Added core84.562s/wrapper86.434s; inherited generation/stage component sum407.192s excludes independent screens/scorers and is not a fresh end-to-end measurement.29 focused checks passed. Retain this as an optional improvement stage; it does not establish reliable independent initialization. Current outputs remain under ignored dev/artifacts; hashes and provenance are tracked in restart-polish-validation.json. No public warm starts or publication.

No jobs running. Next concrete action: compare combining fanout prices with protected threshold walks on development cases under matched caps; preserve all verified incumbents. Phase3 optimization continues before final freeze. Local commits authorized; user handles pushing.

## All-tier initial coverage complete

Official CLI independently confirms45/45 legal outputs across six separate tiers: intro1.0504090271124256,hard1.212967727395428,scale1.0236861228944922,stress1.0026008508372637,congested1.031233699656949,designs1.1215781534720441. Explicit selected-run hashes/config/resource records in tier-coverage.json; stress also in stress-coverage.json. Scale/congested/designs/stress start from official challenge references,attributed,not public competitor routes. Intro starts locally generated baseline;hard inherits recorded optimization chain. No cross-tier aggregate.

Stress retry20261001T225241.212774Z-exact-polish succeeds with60s cap:delay1144904→1141934,core60.051s,wrapper78.918s,peakcore92332KiB. Independent rescore2.778s/228068KiB. Short-cap failure remains recorded separately;reference generation cost unmeasured. No tests added/run this session;previous29-check evidence does not cover new combined mode,official benchmark checks do. Full-tier coverage precedes a final freeze and does not establish independent initialization or end-to-end reproducibility.

No jobs running. Changes:fanout walk/strict comparator,all-suite wrapper,explicit-run official coverage report,scope and architecture corrections. Matched9-run development comparison and full hard validation recorded. Local commits authorized;no push/publication. Next concrete action:profile large-case initialization/validation versus search,then choose targeted tier optimizations and freeze a reproducible six-tier pipeline before Phase4 final evaluation. Preserve current verified artifacts and official inputs.

## Large-case profile and broader measured improvements

Explained lower initial tier scores:unequal optimizer effort and different normalized baselines. Initial scale8/8 hit2s caps;stress short runs could not finish initialization. Instrumented read/validation/optimization. Matched stress60s/seed1/5passes from225241:read44.143→0.424s after tree-local validation,validation43.950→0.250s,searches72→252,delay1141896→1137194. Samecore cap;single-case timing sample,no generalized speedup. Profile/failure evidence retained;official input/checker unchanged.

Screened fanout versus fanout_walk on declared scale01/congested01/designs-ctrl,seed1/5s/100passes:both all improve,fanout lower delay3/3. Chose one fixed fanout config for all scale/congested/designs cases from original coverage routes,not selected per-case representative outputs. Full selected official CLI scores:scale1.0299239499469701,congested1.0406548316718132,designs1.1382735873408656,stress1.0067798458310544;intro1.0504090271124256 andhard1.212967727395428 unchanged.45/45legal;every targeted case improves. Evidence tier-optimized-coverage.json,tier-optimization-comparison.json,coordinated-tier-screen.json,large-case-profile.json. Ancestor optimizer chains/reference attribution now explicit in reporting. No new tests added/run;official checker/scorer checks every selected output. Earlier29 tests do not cover new representation.

Quantum suggestion triaged using primary IBM documentation:tiny restricted simulations may fit CPU/RAM;no quantum access configured or algorithm supplied. Quoted1.0418 below currenthard1.212968;other assessment1.183497 historical. Classical candidate-tree selection already evaluated,9/21 development gains but weaker than negotiated methods. No quantum installation/use or advantage claim. Research note retains references and memory calculations.

No jobs running. Next concrete action:quantify per-tier headroom with independent-net lower bounds and representative budget scaling,then choose further search work from evidence before final freeze/regeneration. Current selected outputs/hashes in tier-optimized-coverage.json;raw artifacts ignored and must be preserved. User authorized local commits and handles push/publication.

## Relaxed headroom,primary-source research,and guided search

Computed analytic obstacle-free pairdelay lower bounds on all45cases,with proof and inputhashes in delay-bounds.json. Optimistic geometric score ceilings:intro1.187031,hard1.761668,scale1.162236,congested1.646832,designs1.811179,stress1.105207. Capacity/foreignpins relaxed;these are upper bounds on attainable score,not jointly achievable results. Higher ceilings motivate congestion/design coordinatedsearch;low sparse-tier scores partly reflect stronger normalized baselines and unequal effort.

Reviewed primary OpenROAD/FastRoute,VTRconnectionrouter,and NeurIPS2020 generalLNS sources;notes/links/transfer limits in OPTIMIZATION_FOLLOWUP. No externalsource copied/executed. Implemented original consistent A* sink-layer rectangle lookahead with exact g cost and unchanged physicalacceptance. Matched60s/seed1/5passes stress from225241/routes:A*1020searches/126572544expansions versus ordinary252/153841664,legal delay1122096 versus1137194. Score1.0203262465956566,officialCLI agrees. Single timing sample/different completedwork and geometry,no equal-work speedup claim.

Added gap-order variant:repair priority=physicaldelay minus relaxed per-net bound. Matched5s/100passes/seed1 representatives hard01/congested01/designsctrl,three modesfanout/fanout_astar/fanout_gap:both new variants beatordinary3/3;gap beatsA*2/3 and losescongested. Selected one fixed fanout_astar full-tier stage from original representativewarmstarts,not selected per-case outputs. Full officialhard1.220250233796514,congested1.0553607547875163,designs1.164826219486074;all16 cases improve. Stressalsoimproves,17targetedcasegains total. Intro1.050409 andscale1.029924 retained.45/45selected outputs officiallylegal. Evidenceguided-search-screen.json,astar-stress-comparison.json,tier-guided-coverage.json,tier-guided-comparison.json. No new tests added/run;earlier29 checks predate A*/gap variants. Per-caseofficial checking plus independentCLI rescoring performed.

No jobs running. Current selected hashes/routes are in tier-guided-coverage.json. Next concrete action:repeat guided comparisons on development seeds2/3,compare5vs20s budgets on declared representatives,and evaluate combining A* with gap priorities/fresh starts if measured bottlenecks support it. Finalfreeze/regeneration/submissionchecks remain pending. Local commits authorized,user pushes;no publication.

User side-note research list addressed with explicit read/implemented/backlog distinctions. Added CUGR authorpaper/repository review,corrected CPU CUGR versus GPU GAMER,documented abstract-only GAMER access and ALT feasibility inference. No new external code/dependencies executed. Current jobs:none;nextaction remains repeatedseed/budget/guidedfresh comparisons.

## Guided repeats,budget curves,freshstarts,and cost-distance research

Built dev/guided_screen.py for frozen representative starts and serialexplicitconfig screens.18trials repeatseeds2/3:fanout_astar beats ordinaryfanout6/6;A*plusgap priority loses5/6vsA*alone,not retained asdefault. Budgetscreen5vs20s seed1:hard01same9292,100cycles exhaustedabout5.33s;congested64591→62981,designs61266→59844,bothstillcapped. Guidedfresh20s/max5starts improvescongested65617→62163;hard/designs preserveincumbents. All30screenoutputs legal;screenwrappercost223.803s includes rejectedconfigurations,not generationcost.

Read full Held/Perner2025cost-distance paper fromuser's suggestedsource. Prototype discounts existingtreecongestion while retaining fullphysicaldriverdistance/allunit sinkweights. It is a greedyadaptation,not theircomponentmerging algorithm/guarantee. Screenhard9284vsastar9292,congested65459vs64591,designs61712vs61266;rejectasdefaultafter2/3regressions. Researchnotes correct staleinterest snapshot,distinguishmergedboard frompublicPRheads,and keepreferenceattribution;writtenruleswarmstartsilence acknowledged,noissue/comment sent. Sourcecode map addedto dev/README.md inresponsetouser.

Fixed20s/100cycles/seed1fanout_astar fullcongested4/4 anddesigns3/3 allimprove. Optionalcongested restart_astar20s/max5freshstarts afterlongerincumbents adds1casegain/3unchanged. IndependentofficialCLI scorescongested1.0826675712383234,designs1.2124988396182923;hard1.220250,intro1.050409,scale1.029924,stress1.020326 preserved.45/45selectedoutputs legal. Currentselectedroutes/configs/hashes/ancestorcosts in tier-followup-coverage.json;comparisonandscreenmanifests tracked. No newtests added/run;officialper-caseverification plusindependentfulltierCLI rescoring performed.29historicalunitchecks do notcovernew modes. Finalfreeze/workcountdeterminism/regeneration/submissionchecks remainunperformed.

No jobsrunning. Nextconcreteaction:hard developmentcyclelimit/neighborhood comparison(using01/04/07,not08/09),thenbroadercandidate/treecomponent construction if measuredceilings showstagnation;extendfastsearchtointro/scale. Preserveallcurrentlegaloutputs andrawprovenance. Localcommits authorized,userpushes;no publication.

## Review-driven diagnostics, work budgets and property checks

Completed hard cycle screen100vs1000/seed1/20s on01/04/07. Longer cycles improve01 from9292→9264;04 remains14895,07 remains24777. These partial development outputs are not adopted as a complete hard entry;hard aggregate remains1.220250. Evidenceguided-cycles-screen.json. No held-out case tuning.

Added checked per-net public gap analysis with input/output hashes and categories. Local one-sink total35011 beatspublic36177;multi-sink deficit22212 accounts fornet signedgap21046. Top20 positive gaps cover25.33% of positivegap26486. Public routes only analyzed,not used aswarmstarts. This supports multi-sink pricing/construction experiments without proving global packing cause.

Implemented backward-compatible optional expansion cap,exact ceiling in shortest/attach,work-exhaustion diagnostics,expansions/optimization-second KPI,and shortestreset/rebuildtimers. Added user-requested property checks;31 focused tests pass. Stress10M/seed1/100passes repeated under30s/45s safety caps produces identical stdout/routes and legal delay1121978. Uncontendedrepeat234215:optimization3.1144s,reset.123646s,rebuild.0476969s,combined5.50%;other costs stillunmeasured. Earlier10M runbriefly overlappedfocusedtests,disclosedandnotusedfor timingconclusion. No scratch/ownership rewrite performed withoutfullattribution.

Independent CLI selected-tier rescore:tier-work-budget-coverage.json,45/45legal,intro1.050409,hard1.220250,scale1.029924,congested1.082668,designs1.212499,stress1.0204335557381696. Stressselectedrun20261001T234215.165836Z-exact-polish;otherselectedruns unchangedfromtier-followup. Fullrawartifacts/source snapshots ignored;preservethem. Finalfreeze/regeneration/submissionremainpending.

Ranked next experiments in docs/design/NEXT_EXPERIMENTS.md,with gainhypotheses,cost,acceptanceandremainingtests. Review corrections retained:softrepair18/21,notzero;A*geometry canaffectmultinetoutcomes;downstream-price dualboundneedsproof. Nextconcreteaction:isolatedfixed-work profilesofheap/heuristic,snapshots,andnegotiationonstress/congested,thenmatchedtightheuristic/heap-g comparisonbeforeprice-unit tuning. No jobsrunning;localcommitsauthorized,userpushes;no publication.

## Full hard follow-through and search kernel measurements

The fixed seed1/20s/1000-cycle fanout_astar stage from run231330 was applied to all nine hard cases, including reserved08/09 without configuration tuning. Run20261001T234843.075364Z-exact-polish is legal9/9, score1.229451214014938: seven improve and two are unchanged. These are local time allowances, not competition caps.

Added heap entries storing g for direct stale checking and optional tighter layer-aware lookahead. Its table is cached once per engine. Distance to the fixed relaxed sink rectangles is consistent under physical edge costs. Changed queue order can change geometry; official physical delay remains the acceptance criterion. All31 focused tests pass, including random tight-A*/independent-Dijkstra comparisons and tight-mode work-cap rollback.

Serial kernel screen: hard/congested/stress case01, seed1, 5M expansions, two repeats per variant. Stored-g stdout matches control exactly; all repeats are byte-identical. There is no clear timing improvement: mean wall hard .990→1.056s, congested1.115→1.117s, stress1.557→1.598s. Stored g is retained for direct stale checking, with no speedup claim. Tight delays are hard9292→9276, congested61897→61873, stress unchanged1121976. Snapshot/setup/scan counters are small in these hard/congested samples; stress made zero group attempts and supplies no large-group transaction evidence. See search-kernel-screen.json; the control is rebuildable from637a829.

Fixed tight stage seed1/5M expansions/1000 cycles/60s safety cap applied to every hard case from the long-cycle outputs: run20261001T235301.888083Z-exact-polish is legal9/9, score1.2300004741250727, four improve and five are unchanged. Core time .82–.97s/case is an incremental warm-start stage, not a fresh solve. Independent official CLI selected-tier coverage confirms45/45 legal in tier-kernel-coverage.json. Only the selected hard run changes; other five tiers retain prior verified outputs. Final freeze/regeneration remain pending; ancestry and stage costs are recorded.

No jobs running. Next concrete action: controlled fixed-point congestion-price/config comparison on declared multi-sink hard/congested development cases, seeds1–3 and fixed work caps; try adaptive neighborhoods if pricing stagnates. Keep tight lookahead optional, the Dijkstra control and prior incumbents. Local commits are authorized; the user handles pushing. No publication.

## Six research links, DATE identification and fine-price experiment

Audited all six links against durable notes. Previously read PathFinder, CUGR and full cost-distance HTML. Newly reviewed NTHU author page and ICCAD algorithm sections, and Prim-Dijkstra Revisited objective/PD-II/DAS sections. Exact PathFinder host failed; used a university course mirror. DATE archive1157.pdf returned404. User supplied IEEE11539267; IEEE fetch failed/418, but official DATE programme identifies the paper and exposes its abstract. Programme PDF link also404. Read abstract only; do not claim full-text access, CUGR dependence or reproduction. Full coverage, links and limits in OPTIMIZATION_FOLLOWUP.md.

Implemented optional fanout_fine: all shortest physical/search/heuristic units scaled16; scale congestion price before fanout division. Retain exact physical predecessor-tree delay and official acceptance. Priority multiplication checks overflow. Legacy/default and attach units preserved. All31 focused checks pass, including fine work-cap rollback/repetition.

Declared hard/congested case01, seeds1–3, fixed5M expansions/1000cycles/60s safety cap compared fine against tight control serially. Fine4wins/1tie/1loss; congestedseed2 regresses24 versus control. Screen wrapper cost18.201s, separate from generation/full stages. Keep optional, not universal default. No held-out tuning. Reports pricing-screen.json/pricing-comparison.json.

Fixed seed1 full hard stage20261002T000141.903840Z-exact-polish score1.2303243121958916,9/9legal and all improve. Fixed full congested000215.838363 score1.08805956745537,4/4legal and all improve. Stages add search effort; representative matched controls isolate resolution, full-stage gains do not prove universal superiority. Independent official CLI report tier-pricing-coverage.json confirms45/45selected outputs legal. Intro1.050409,scale1.029924,designs1.212499,stress1.020434 unchanged. Ancestor effort/reference attribution recorded; no public warm starts.

No jobs running. Next concrete action: expose present/history negotiation schedules as explicit bounded config, compare a small declared sweep at fixed work on multi-sink development cases and repeated seeds, then choose coordinated topology/neighborhood work if pricing plateaus. Full DATE reading needs an accessible PDF; no author messages sent. Final freeze/regeneration/submission remain pending. Local commits authorized; user pushes; no publication.

## Configurable schedules and user-provided DATE PDF

IEEE stamp link failed in browser and direct fetch418; asked the user for an attachment while continuing independent solver work. User added the root PDF. Strict pypdf6.1.1 parsing succeeds on all seven pages; no encryption, every page yields text, metadata title/article match11539267. SHA2568def9e934f4fd06969809868c3d5f23ca5a35dec8c3d89593635851326228c9e,390900bytes. Read complete extracted text. Optional reader installed only in .venv and pinned in dev/requirements-research.txt. Licensed PDF stays user-owned/untracked at root; extracted text only /tmp. Research handoff DATE2026_VIA_CONGESTION.md and integrity report tracked.

Full text explicitly reuses CUGR cost models, while adaptive vias/DP/bidirectional RRR have different industrial overflow/via objectives. Discounted via priorities invalidate the current physical lookahead unless adjusted; directed source-dependent costs require transposed backward search. Printed pseudocode is incomplete as an executable spec. These are research/implementation cautions, not reproduced results or claimed solver methods.

Added NegotiationConfig defaults2/2/2 and bounded key=value engine options/wrapper arguments for present initial/step and history step. Only local negotiated repair is configured; whole restarts and candidate generation retain old schedules.32 focused tests pass, including explicit/default output identity and invalid-key/value rejection.

Four fixed schedules tested serially on hard/congested case01,seeds1–3,5M expansions/1000cycles/60s safety cap. Hard2/1/1 wins3/3 vs default;congested2/4/4 wins3/3. Slower congested schedule regresses two seeds, so separate tier schedules retained. Screen timing overlapped optional reader installation/PDF inspection; timing not used for selection, fixed work determines output comparisons. schedule-screen.json and schedule-comparison.json record all24trials and totalcost.

Fixed seed1 full hard stage20261002T001045.804709Z-exact-polish:legal9/9,score1.2306575756801885,7improve/2unchanged. Congested001141.164841:legal4/4,score1.090605391888499,allimprove. Added search effort remains explicit;no per-case seed selection. Independent official CLI selected coverage in tier-schedule-coverage.json:45/45legal,otherfourtiers unchanged. Final freeze/regeneration/submission still pending.

No jobs running. Next concrete action:broaden schedule robustness checks on declared development cases,then choose nonlinear marginal-overflow pricing or coordinated topology/window repairs based on failure profiles. Preserve current incumbents and root PDF. Local commits authorized;user pushes;no publication.

## Research and submission-location clarification

User requested brainstorming from GitHub and other sources plus the score of entries in submissions/. Inspected local metadata/leaderboard, engine, latest coverage and budget evidence. Tracked submissions are upstream Anthropic reference entries; best complete local listed hard entry negotiated_x2 scores1.0168. Our recorded hard best1.220250233796514 is in tier-followup-coverage.json; its routes were under ignored dev/artifacts, absent from this checkout along with .venv/dev/upstream. No fresh score recomputation or recovery performed.

Reviewed MAPF-LNS2 author source/paper, CUGR author source/paper, Held/Perner component construction, SPRoute README, and CBS publication abstract. Challenge landing page accessible; PR/IrwinJam accesses failed, so standings/source changes not refreshed. Added ranked hypotheses and concrete screens to OPTIMIZATION_FOLLOWUP.md: adaptive/transitive groups, diverse corridors, bounded static CBS, stronger layered A*, component-merging candidates, coarse search. Engine inspection shows fixed within-group negotiation order and per-call history reset; retained hard01 evidence has1935 nonimproving repairs out of2033 attempts. No solver changes, tests, experiments, external code execution, new gains, commits or publication. No jobs running. Next action: recover/regenerate previous artifacts before matched development screens; protect reserved08/09 and current official inputs.

## Recovered environment, neighborhood screens, and new hard best

User authorized proceeding. Restored .venv and exact pinned upstream archive with dev/setup.sh, compiled engine without warnings. Implemented optional shuffled negotiation order, diverse corridor proposals, adaptive direct/transitive/random groups, and1000-cycle ceiling. Added serial explicit-start recovery/cycle/operator harness. Preserved historical reports and unchanged official inputs; no external source copied/executed, no unit tests added/run.

New reference-assisted recovery20s/1000cycles/seed1 fanout_astar gives hard1.2152861382477105,9/9 legal, independently CLI rescored. Six matched10s100vs1000cycle outputs legal; all time-capped, two identical delays, third differs8 with unequal searches. No cycle-limit benefit claim.36 matched5s/1000cycle screens hard01/04/07,seeds1–3 all legal: shuffle wins7/9 versus original, diverse9/9, adaptive5/9 plus2ties/2losses. Diverse beats shuffle6/9 and loses3/9. Adaptive remains experimental; no reward-per-CPU normalization yet. Screens cost260.844s including cycle checks; no held-out tuning or per-case selection.

Fixed seed1 diverse20s/1000cycle full-tier stage from recovered routes: run20261002T001313.450750Z-exact-polish,9/9 legal, all9 improve versus recovery. Independent official CLI score1.2274487880088916, new recorded hard aggregate best (+0.5899% versus1.220250);6 historical case gains/3 regressions. Core180.437s/wrapper182.321s, peak core4736KiB. Two-stage wrapper sum363.756s excludes reference generation, screens, and scorers. Evidence: recovery-recover/cycles/operators.json, recovery-hard-coverage.json, neighborhood-hard-coverage.json, recovered-neighborhood-comparison.json. Selected source/config/output hashes retained. No matched whole-tier algorithm superiority or fresh deterministic regeneration claim.

Latest available hard routes: dev/artifacts/20261002T001313.450750Z-exact-polish/routes. Other tiers retain recorded historical scores but old route artifacts remain missing. submissions/ still holds upstream references; no submission entry/publication prepared. Updated overview, Phase3 summary/checklist, architecture, verification and claims. git diff --check passes. No jobs running, no commits/push/publication. Next concrete action: compare diverse corridors plus localized/random dependency groups against current diverse control on01/04/07, then fixed08/09 validation; stronger layered heuristic/static CBS remain unimplemented research options. Final freeze/regeneration and restoring other-tier artifacts remain pending.

## GitHub pull and local integration

User explicitly requested pulling this fork and resolving conflicts. Fetched origin/main and fast-forwarded main from003133a to38b3a49 (eight commits). Preserved original local patch/untracked files under /tmp/routing-pull-backup-20261002T002343Z and stash named local neighborhood experiments before GitHub pull. Reapplied work; resolved five conflicting files by retaining both solver mode families, work limits/schedules/scaled prices, and both research/evidence histories. Corridor penalties now use the same checked price-unit scaling as physical/occupancy costs. Renumbered local decision additions32–34 after GitHub31.

Current highest recorded scores are GitHub hard1.2306575756801885/congested1.090605391888499,45/45 recorded legal (tier-schedule-coverage.json). Locally available recovered hard routes remain1.227449; GitHub-best raw artifacts were not transferred because ignored. Updated current-state docs to distinguish them. Combined C++ compiles without warnings; Python AST syntax inspection and whitespace/conflict review pass. No tests or new optimization/evaluation runs performed; historical checks do not verify combined operators. No new commit/push/publication. Backup stash retained; local edits remain uncommitted. No jobs running. Next action: controlled fixed-work comparisons of merged neighborhoods with tighter lookahead/fine prices/schedules; preserve existing immutable evidence and incumbent outputs.

## Combine local neighborhoods with current GitHub kernels

User requested integrating local work with the current repo. Exposed all nine shuffle/diverse/adaptive combinations across fanout_astar, fanout_tight and fanout_fine. Tight/fine neighborhoods inherit cached lookahead,16-unit fine prices where selected, expansion budgets, and explicit congestion schedules. Corridor penalties use checked price scaling; physical acceptance and rollback remain unchanged. Extended neighborhood_screen.py with kernel/work/time/schedule controls and protected --out report destinations; controls receive identical declared caps/starts/schedules. Historical screen defaults and reports are retained. Added an exact example for a fixed5M/60s fine+neighborhood comparison from available recovered routes.

Combined C++ builds without warnings; Python syntax/CLI help checks and git diff --check pass. No tests, benchmark runs, new scores, commits or publication. Highest recorded hard remains GitHub1.2306575756801885; locally available recovered hard1.2274487880088916. Raw GitHub-best routes remain missing here. No jobs running. Next action: run the declared combined-fine screen before adopting a combined mode, then fixed-config full-tier validation; keep held-out08/09 out of tuning.

## Reubalink method and artifact inspection

User requested inspecting THOMACHAYAN/reubalink-hard for algorithm ideas. Main and submission branch contain no custom solver source; changes are only routes/leaderboard/metadata. Read PR10, commit messages, metadata, branches and author routing-repo list. Described algorithm uses shortest-path trees, fanout PathFinder, exact reroute, window LNS, then negotiation in ripped windows. Final commit starts from five-hour routes; algorithm/runtime contributions are confounded. Pair search/ML ordering earlier in history are author reports, not source inspection/reproduction.

Downloaded18 pinned route JSONs for analysis only; no external code execution/copy/public warm starts. Original inspect_reubalink.py independently official-checks/scores predecessorca3cb1d1.2671868111635183/159369delay and finald9cddc4c1.362234270749783/147825delay, each9/9legal. All9 improve; final uses1370 fewer net vertices/edges and385 fewer vias. Against our recorded GitHub-best: one-sink ours35071/theirs36257; multi-sink ours129474/theirs111568. Signed gap16720, multi-sink17906. Evidence/source/input/output hashes in reubalink-inspection.json; our side uses existing recorded per-net stats, not fresh regeneration. No unit tests or solver changes.

Added spatial full-net neighborhood experiment plan to NEXT_EXPERIMENTS and research notes: sample proposed4/8/12 XY boxes using only our incumbent/detour bounds, bounded touching-net groups, reuse transactional fine/tight negotiation, frozen external nets/pins, strict physical acceptance. Compare fine/fine-diverse/spatial at5M/20M work and60s safety caps, same starts/seeds/schedules on01/04/07, fixed08/09 only after selection. Window boundary-preserving topology repair and component merging are later hypotheses; no claim to know their unpublished settings. No jobs running, commits or publication. Next action: implement and measure spatial-group prototype; preserve current local routes and immutable reports.

## Requested push, spatial comparison, and selected hard improvement

User explicitly requested pushing resolved work before continuing. Read AGENTS,
inspected diff/index, fetched origin/main: base38b3a49 still current, no
unmerged files or whitespace errors. Committed integrated neighborhood kernels,
tools and research/evidence as d4032d4 and pushed main successfully. Backup
stash retained. No leaderboard/submission changes or competition publication.

Implemented optional spatial group modes for all three fanout kernels. Own
incumbent/detour-ranked target and seeded random vertex anchor4/8/12 XY
boxes across layers. Rank touching neighbors by relaxed-delay excess,cap12
neighbors+target; choose greatest neighbor excess. Whole-tree negotiation may
leave the box; external owners/foreign pins frozen. Existing transaction
rollback/strict physical acceptance reused. Ranking favors large nested boxes;
no actual group-size histogram instrumented. No public warm starts/geometry
or per-net competitor gaps guide routing. No external code copied/executed.

Matched serial fine/fine-diverse/spatial screens on01/04/07,seeds1–3 at5M
and20M expansions,60s safety cap,1000cycles,schedule2/1/1,same frozen
recovered starts:54/54 official-legal, all exact work caps reached. Diverse
beats fine7/9 at both budgets,2 losses; relative geomeans1.000583/1.002586.
Spatial vs fine2wins/1tie/6loss at5M,3wins/6loss at20M. Spatial retained only
experimental. Spatial5M131 repairs/2gains/89fail/40nonimproving;20M564/17/315/232.
Screens cost278.214s wrapper, excluding inherited generation/build/scorers.
Reports spatial-5m-screen.json,spatial-20m-screen.json,spatial-comparison.json.

Frozen fine-diverse/seed1/20M/1000cycles/60s/2/1/1 full-hard followup from
recovered1.227449: run20261002T022353.079439Z-exact-polish,all9 improve,9/9
legal,score1.234984066216333 independently official CLI rescored. Relative
previous recorded GitHub1.230658:+0.35156%,six case gains/three regressions
(01/02/08); do not claim all improve that historical baseline. Reserved08/09
validated only after selection; no tuning afterward. Core62.106s/wrapper63.995s,
peak4736KiB; full stage allcases20M expansions. Ancestry+hashes retained in
fine-diverse-hard-coverage.json. Additional search effort does not establish
same-budget whole-tier superiority; no best-of-cases or seeds selection.

Compilation warning-free, Python syntax inspection and git diff --check pass.
No unit tests added/run. Latest available routes are this full-stage routes
directory; other-tier historical artifacts remain missing. New experiment
changes remain uncommitted after requested pre-work checkpoint push. No jobs
running. Next action: instrument group sizes and try bounded smaller/randomized
spatial groups or boundary-preserving branch repair; retain fine-diverse and
current best. Final freeze, other-tier artifact recovery/regeneration and
submission preparation remain pending.

## Publish remaining experiment work

User requested pushing all remaining work. Fetched origin/main; HEAD aligned
with d4032d4, no unmerged entries and git diff --check clean. Preserved latest
full-hard routes, original manifest, independent rescore and development-source
snapshot under dev/incumbents/hard/20261002T022353.079439Z-exact-polish.
Verified every copied route against original output SHA256; narrow ignore
exception includes these route files. This avoids losing the current1.234984
result with ignored scratch artifacts. Ancestor reconstruction remains a
separate limitation; no binaries/bulk scratch logs or competition entry added.
Commit/push all solver, experiment, evidence, documentation and incumbent
archive changes as requested. No new optimization or unit-test runs. No jobs
running; next action remains smaller spatial groups or branch repair.

## Optimize every tier and inspect concurrent work

User clarified the objective: maximize each separately scored tier, independent of current public PRs. Extended fine pricing/tight search to intro/scale/designs/stress with fixed seed1/5M expansions, then applied seed2/10M to all six tiers.1000cycles/60s safety caps; serial workers, no public warm starts or undisclosed per-case selection. Hard schedule2/1/1,congested2/4/4,others2/2/2. Ten stages add319.189s wrapper effort; ancestry remains explicit.

Independent official CLI confirms45/45selected outputs legal: intro1.0935715066916682,hard1.2312958441734672,scale1.0404093962466106,congested1.0941448397359423,designs1.2236812513939086,stress1.0205481649985917. All six tier scores improve;40cases improve and5hard cases are unchanged. Reports all-tier-advance.json,all-tier-advance-comparison.json,tier-all-advance-coverage.json. Compact reports omit redundant per-net arrays; full original manifests remain under ignored artifacts with recorded hashes. User PDF remains untracked/preserved.

Added resumable bounded all-tier stage orchestration with explicit coverage/new report labels and refreshed relaxed bounds from selected outputs. Bounds remain optimistic, not jointly routable scores. All-tier goal/next hypotheses in ALL_TIER_OPTIMIZATION.md. No new solver code or tests in this optimization chunk; prior32 focused checks do not claim to test the new orchestration. Official checking verifies every selected output. Final freeze/regeneration/submission remain pending.

User asked to inspect possible concurrent pushes and resolve conflicts. Read-only fetch initially failed because automatic approval review timed out before execution; retry succeeded. Found one incoming commit d4032d4 by Krithik4, adding nine composed neighborhood modes, corridor proposals, adaptive groups, scripts and evidence. Its highest recovered hard output is1.227449 and its raw artifacts were unavailable in that checkout; our newer45-case outputs are present here. No equivalence between that recovery chain and our incumbents claimed. Save current edits before merging; review/test composed operators against our own latest routes.

No jobs running. Next concrete action: merge d4032d4 without discarding either research/evidence history, resolve current-state overview to the actual available six-tier incumbents, then compile and check combined neighborhoods. Local commits and requested conflict integration authorized; user pushes. No publication.

## Integrate concurrent neighborhood commit and verify combined engine

Merged incoming d4032d4 with local db0e257; resolved WORKLOG and OVERVIEW conflicts by retaining both histories and making the current state reflect our available45-case artifacts. Incoming changes add shuffled negotiation, diverse corridor proposals and adaptive blocker groups, composed with existing A*/tight/fine kernels. Other contributor's recovered artifacts and public-output analysis remain distinct from our local generation chain.

Combined C++ builds warning-free. All32 focused checks pass, expanded to all nine composed modes and actual three seeds in the crossing check (previously the loop omitted the seed argument). Six representative fine-mode comparisons against the saved premerge binary produce byte-identical routes, independently official-checked. Evidence merge-kernel-verification.json and reproducible helper verify_merged_kernels.py. These equivalence checks cover the original mode, not superiority of new modes.

Matched merged fine-neighborhood screen on hard01/04/07, seeds1–3,5M expansions/1000cycles/60s safety cap, schedule2/1/1:36/36 legal,87.360s wrapper effort. Against control shuffle6wins/3ties, diverse5wins/4ties, adaptive6wins/3ties, no losses in these comparisons. Adaptive has the largest across-trial geometric delay ratio1.0017884; individual best results differ by seed/mode. Evidence merged-fine-neighborhood-screen.json. Pilot gains are not a full-tier score or a universal default recommendation. Next step: fixed seed1 adaptive full-hard stage, independent scoring, then broader tier measurements and spatial-neighborhood prototype. User PDF remains untouched/untracked; no publication.

Fixed seed1 adaptive full-hard stage20261002T022919.965005Z-exact-polish completed:9/9 legal,8 improve/1 unchanged,score1.2333571857577519 versus1.2312958441734672. Added wrapper effort 19.521138629992492s, separate from inherited generation and87.360s screen. Configuration5M expansions/1000cycles/60s safety cap,schedule2/1/1. Held-out08/09 were evaluated after selection and both improve; no held-out tuning. Independent six-tier coverage is tier-merged-neighborhood-coverage.json; other five selected runs unchanged. No jobs running after rescoring. Next action: measure these optional neighborhoods outside hard, then prototype spatial full-net repair. Final freeze/regeneration/submission remain pending.

## Integrate second concurrent push236cc84

Fetched the newly reported push and merged spatial-repair prototype, matched-screen evidence and preserved hard incumbent archive. Solver changes merge cleanly; WORKLOG/OVERVIEW conflicts resolved preserving both histories and actual six-tier availability. Incoming spatial screens regress versus controls, so retain experimental mode only. Fresh official pinned CLI rescore verifies incoming archived hard routes9/9legal,score1.234984066216333, above our separate adaptive1.2333571857577519. Preserve both pipelines and provenance; no per-case portfolio silently selected. Other five tier incumbents unchanged. Combined C++ warning-free and all32 focused checks pass, including composed spatial modes through the shared mode list. No running jobs; next action compare/continue the two legal hard pipelines and measure neighborhood operators across the other tiers. Final freeze/regeneration/submission remain pending. User PDF preserved; local merge only, no push/publication.

## Continue adaptive optimization on all six tiers

Extended advance_all_tiers.py with explicit mode/single-stage/seed/work caps and preserved hard-start directory. Starting hard uses incoming local archive1.234984; other five use existing selected routes. Fixed adaptive fine seed1/5M expansions/1000cycles/60s cap,serial,schedules hard2/1/1,congested2/4/4,others2/2/2. Independent CLI confirms45/45legal; all six scores improve.

intro 1.0955758162466702, 14 improve/6 unchanged; run 20261002T023420.807032Z-exact-polish.
hard 1.2375216859738483, 7 improve/2 unchanged; run 20261002T023506.922949Z-exact-polish.
scale 1.0427841747061612, 8 improve/0 unchanged; run 20261002T023529.212154Z-exact-polish.
congested 1.0956995301333292, 4 improve/0 unchanged; run 20261002T023556.952369Z-exact-polish.
designs 1.2264569927913178, 3 improve/0 unchanged; run 20261002T023612.135172Z-exact-polish.
stress 1.0205499844007666, 1 improve/0 unchanged; run 20261002T023621.680402Z-exact-polish.

Added wrapper effort 139.726s; inherited generation, prior screens and rescorers separate. Adaptive-all-tier reports retain source/config/case/output hashes and all unchanged cases. Stress gains just2delay units. Archived ancestor availability now explicit in coverage reporter rather than labeling missing origin as known local generation; scores/hashes unaffected. Python syntax inspection and git diff --check pass; no new solver changes/tests this chunk.

Added generic official local-route comparison helper: adaptive versus incoming fine-diverse totals164235/163669 hide9972/10538 opposing per-net savings. This diagnoses distinct packing, not legal splicing. Proposed transactional donor groups/composed diverse-adaptive screen in NEXT_EXPERIMENTS. Relaxed bounds refreshed; not jointly achievable score targets. No running jobs. Next concrete action: implement optional composed diverse/adaptive proposals and compare against both controls at matched work on01/04/07,seeds1–3,then fixed validation if retained. Final freeze/regeneration/submission pending; user PDF untouched; local commits authorized, no publication.

## Research, composed proposals, and disclosed case portfolio

User clarified keep-going means pursue substantial improvement and outside methods. Reviewed MSPD author repo/construction/source-selection paper sections, BoxRouter README/config (source-directory access failed), and revisited Held/Perner practical component/Steiner-placement sections. No third-party source copied/executed. TOPOLOGY_AND_PORTFOLIO_FOLLOWUP.md distinguishes skew/wire/resource objectives from our summed sink delay and records partial reading limits.

Implemented optional hybrid modes for all three kernels, composing diverse corridor proposals and adaptive groups.32 focused checks pass with hybrid coverage via shared modes;warning-free build. Matched hard01/04/07,seeds1–3,5M/1000cycles/60s,2/1/1:27legal outputs,cost62.691s. Hybrid versus diverse5wins/1tie/3losses,ratio1.000207;versus adaptive3wins/1tie/5losses,ratio0.999690. Reject as default,keep experimental. No08/09 tuning.

Generic select_case_portfolio.py selects complete route files from explicit successful local pipelines with official input/output hashes and independently rescored legality; no individual-net mixing. Adaptive current pipeline and prior other-basin adaptive pipeline produce hard1.2491377321487542,9/9legal,versus stronger individual1.2375216859738483. This deliberately changes the earlier no-portfolio policy to an explicit disclosed portfolio for final-route quality. Deduplicated available generation costs and missing ancestors recorded; not a matched-budget algorithm improvement.

Fixed seed4 adaptive10M/1000cycles/60s/2/1/1 followup from portfolio:run20261002T024319.157302Z-exact-polish,all9improve,9/9legal,hard1.25196491393671,wrapper32.593s. Independent six-tier CLI rescore confirms45/45legal in tier-portfolio-followup-coverage.json; otherfive scores unchanged. Inherited portfolio and known total costs are embedded by coverage reporter. Preserved byte-identical new hard routes/original manifest/source/rescore and inherited portfolio under dev/incumbents/hard/20261002T024319.157302Z-exact-polish;hashes allmatch. This preserves outputs,not end-to-end regeneration of missing ancestors. No running jobs. Next concrete action: prototype donor-tree transactional groups and compare against adaptive at matched work on01/04/07 before further full-tier stages; pursue component/partial-branch rebuilding if dependency repair plateaus. Final freeze/regeneration/submission pending. User PDF untouched;local commits authorized;no push/publication.

## Alternate local trees guide transactional blocker repairs

Implemented optional fine donor mode. Wrapper officially validates alternate routes, records donor path/hash/delay per case, and appends a second encoded instance. Engine validates donor trees and matching grid/costs/net terminals, then compares improving donor geometry to ideal-path geometry by displaced-owner count/physical delay. Selected geometry defines blockers; existing adaptive expansion and full-group negotiation perform repair. Donor routes are not inserted blindly or used as immutable constraints. Frozen ownership/pins, rollback and physical acceptance retained. Generic CLI has no benchmark-specific donor paths.

Warning-free C++ build;33 focused checks pass, including missing/mismatched donor rejection, work caps, legality and output repetition across seeds/budgets.18matched trials hard01/04/07,seeds1–3,5M/1000cycles/60s,2/1/1 alllegal:donor5wins/4losses versus adaptive,geomean1.0006623,cost42.639s. Keep optional,not universal default. Four screen source snapshots briefly captured an uncompiled read_s-only edit; binary remained constant and edit was reverted. Actual compiled source hash/affected run IDs explicitly retained in screen caveat and BUGS. Quality/work results unaffected; do not claim affected snapshots alone regenerate that binary.

Fixed full-hard seed1 donor5M stage from latest preserved portfolio-followup:run20261002T031034.943763Z-exact-polish,score1.2543945794120073,7improve/2unchanged,9/9legal,wrapper16.294s. Otherfive tier outputs unchanged;independent pinnedCLI confirms45/45legal in tier-donor-followup-coverage.json. Donor comes from our own prior adaptive pipeline,already included in inherited portfolio generation;no public warm starts. Raw incoming older ancestors remain unavailable. No full-tier matched superiority claim.

Added compact incumbent archiver: checks original output hashes, stores byte-identical routes/manifest/source/rescore with deterministic tar metadata/gzip timestamp,reads every member back for byte equality. Latest hard archive under dev/incumbents/hard plus member hashes;avoid accumulating expanded route diffs. Python syntax inspection/git diff --check pass. No running jobs. Next concrete action:instrument actual donor selection/group sizes,try both local donor basins under matched work,then develop boundary-preserving component/branch rerouting if blocker repairs plateau. Continue other tiers with measured useful operators. Final freeze/regeneration/submission pending;PDF untouched;local commits authorized,no publication.

## Measure donor activity, diversify every tier, and preserve all selected routes

Added observational donor eligibility/selection/improving-group counters and repair size2/3/13 buckets. Corrected read_s to include donor parsing/validation before compiling; no solver/wrapper edits during active experiments. Counter invariants covered by existing donor check;33 focused checks pass and build warning-free. Python syntax/diff review pass.

Fixed seed5 adaptive3M/1000cycles/60s serial all-six stages add98.095s wrapper;all6scores improve,35cases improve/10unchanged at this stage. Existing schedules retained. Scale/congested/designs attempt32/16/12groups;stress0,versus intro907/hard638. Under this cap, large cases spend much work outside completed dependency repairs; no precise profiling attribution or CPU speed claim from counts alone.

New explicit two-donor harness: frozen improved hard starts,01/04/07,seeds1–3,3M expansions each,1000cycles/60s,2/1/1. All27trials legal and exactly3M work. Old adaptive donor2wins/2ties/5losses vs adaptive;fine-diverse6wins/1tie/2losses,ratio1.0002413. Fine-diverse334eligible/230selected proposals and8improving donor-guided group repairs;oldadaptive362/244/2. Screencost40.646s. Donor remains optional,not universal default. Original donor generation part of inherited local case portfolio;not public warm starts.

Fixed fine-diverse donor seed1 fullhard3M stage 20261002T032017.366965Z-exact-polish improves8/unchanged1,score1.2563066799749418,wrapper12.729s. No08/09 tuning;fixed held-out evaluation after donor choice. Independent coverage tier-two-donor-followup-coverage.json confirms45/45legal. Selectedscores intro1.0966221349244722,hard1.2563066799749418,scale1.0444737801995665,congested1.097029151793132,designs1.2281799145202401,stress1.0205790957178438. Ancestry/portfolio/missing raw ancestors remain explicit.

Archived every selected tier,not only hard:byte-identical routes/manifest/source/rescore,archive/member hashes and canonical dev/incumbents/selected.json. New restore helper verifies archive/member hashes,rejects existing destinations and restores atomically per run. Manual restore to/tmp/routing-selected-restoration-20261002T0321 verifies all45original output hashes. No missing-generation reconstruction claim. No running jobs. Next concrete action:implement smaller partial sink/branch repairs or bounded dependency groups to reduce large-tier search cost; compare with current adaptive3M controls,then continue full tiers if retained. Summaries DONOR_BASINS_AND_ALL_TIERS.md. Finalfreeze/regeneration/submission pending;PDF preserved;local commits authorized,no publication.

## Bound repair groups and diagnose stress scheduling

Added bounded group_limit2–13(default13) to engine/wrapper;all initial blockers must fit,adaptive additions constrained,rollback/frozen ownership retained. Keep original wide24round schedule before clipping group size. Full transaction-size histogram logged.34focused checks pass,including explicit/default13 identity,invalid1/14rejection and group-cap legality;warning-free build. No source edits during active runs.

Pilot firstscale/congested cases anddesignsctrl,seeds1–3,caps3/7/13,3M:27legal,all exact3M. Cap3 wins9/9 vs13;selected for these tiers by predeclared2/3wins+GM>1rule. Cap7 not selected. Across three seeds cap13vs3 attempts scale13vs72,congested26vs131,designs7vs56;physical comparison,not CPU speed claim. Pilotcost57.584s. One-case-per-tier limitation explicit.

Fixed seed1 adaptive3M fullsix stage uses selectedcaps3,others13:five tiers improve,stress unchanged,45/45officiallegal. Added wrapper97.754s;source/config/ancestry/hashes in tier-bounded-groups-all-tiers-coverage.json. Current intro1.0974025183797085,hard1.2564870553234753,scale1.0457201790330146,congested1.0984083343517812,designs1.2297437228340384,stress1.0205790957178438. Missing earlier raw ancestors/inheritedportfolio costs remain disclosed. Archive allsix selected outputs;restore to/tmp/routing-bounded-groups-restoration-20261002T0330 verifies45original output hashes.

Stress has901nets;16searches consume3M expansions and0repair proposals. Inspection shows explore completes whole-net polish sweep before repair,explaining no neighborhood attempts under this cap. Next concrete action:optional repair-first/interleaved schedule,matched stress/control work and rollback checks before full-tier use. Group-size reduction alone cannot resolve this scheduling bottleneck. Full summary BOUNDED_GROUPS.md. No running jobs;finalfreeze/regeneration/submission pending. PDF untouched,local commits authorized,no publication.

## Repair-first scheduling rejected; retain stronger stress control seed

Added optional repair_first0/1 engine/wrapper config,moving existing group sweep ahead of single-net polish without changing exact search ortransaction logic. Default0unchanged;35focused checks pass with explicit/default output identity,invalid2rejection and work-limit legal checkpoint/repetition. Buildwarningfree;source frozen throughout screen.

Frozen currentstress andscale01 starts,seeds1–3,currentcaps13/3,repair-firstsamecap andswapped3/13,3M/1000cycles/60s:all18legal,all exact3M. Repair-first loses overall on bothtiers/caps;nonepassespredeclared2of3wins+GM>1rule. Stress proposalsnow1–13 versus0controls,so scheduling reaches repair butdoesnotimprovequality overall. Keepexperimental,notdefault. Total screenwrapper219.389s includes9stress+9scale trials,notjustselectedoutput;inheritedgeneration/scoringseparate.

Retain strongeststress candidate controlseed3,run20261002T033712.792138Z-exact-polish,delay1121764(score1.0206282248316045),54less thanprior. Explicit selectionfrom9scheduling/seed candidates,notrepair-firstgain. Stresshasnoheldoutcase. IndependentCLIcoverage tier-repair-schedule-coverage.json confirms45/45legal;otherfiveoutputs unchanged. Selectioncontext incoverage/canonicalincumbents,archiveoriginalbytes/source/manifest/rescore. Missingolderancestors/referencegenerationremainunknown. SummaryREPAIR_SCHEDULING.md.

Next concrete action:gain-over-estimated-search-cost single-net ordering,withbboxareaproxy vsrelativeexcess vsrandom,matchedstress/scale starts/work/repeatedseeds. Preservecurrentroutes acrossfailedhypotheses;partialbranch/localcancellationlater. No runningjobs;finalfreeze/regeneration/submissionpending. PDFuntouched;localcommitsauthorized;nopublication.

Original-order scale controlseed3 is strongest developmentcase01 control too;fixed full8case followup20261002T034757.054852Z-exact-polish,3M/group3,improvesall8,score1.0471187071837642,wrapper18.152s. Independent coverage tier-schedule-seed-followup-coverage.json confirms45/45legal withscale+stress gains;otherfour unchanged. Archives/canonicalselection updated with explicit selectioncontexts. Finalrestoreverification coversall45routes. Nojobsrunning;nextactionremainsgain-per-estimated-cost ordering.

## Prioritize stress polish by delay headroom


Area-normalized excess delay prioritizes whole-net exact searches. Relative excess is an alternative; default remains seeded random. Ordering changes allocation of finite work, not shortest-path costs or physical acceptance. Cached scalar priorities ensure a strict stable comparator. Engine and wrapper record configuration and completed/improving searches.

36 focused checks pass; warning-free C++17 build. Matched stress/scale01 screen: three seeds, three orders,3M expansions each,18 officially legal trials,225.483s wrapper total. Area ordering wins3/3 stress seeds,geometric delay ratio1.0002354; relative wins3/3 with1.0001153. Both lose2/3 scale seeds, so retain scale random. Area ordering completes332 stress searches versus15–39 controls. This is work allocation evidence, not a measured CPU speedup. Bounding-box area remains a proxy, not a calibrated predictor.

Fixed seed1 stress3M area pilot followed by20M continuation yields delay1120960,score1.0213602626320297. Continuation costs32.684s wrapper,12.177s core and20M expansions. This adds effort and is not a matched-budget whole-tier comparison. Stress has only one case and no held-out validation.

Independent pinned CLI validates all45 selected routes: intro1.0974025183797085,hard1.2564870553234753,scale1.0471187071837642,congested1.0984083343517812,designs1.2297437228340384,stress1.0213602626320297. Other five outputs unchanged. Evidence: polish-order-screen.json and tier-polish-order-followup-coverage.json. Canonical selection and compact stress archive preserve original bytes/source/manifest; prior archives retained. Older missing ancestors and reference-generation costs remain unreproduced. No freeze, global-best, unseen-generalization or end-to-end regeneration claim.

Next: measure actual per-net search effort to refine scheduling; compare targeted partial-branch repairs against retained whole-net controls before full-tier adoption. Final freeze and submission remain pending.

No source edits during active runs. User PDF untouched; local commits authorized, no push or publication. No jobs remain after archival checks.

## Correct current pathfinder_lns tier mapping


Live PR3 head c2d9d9f583d2f332ebb84d22592ee511f6e56e33, updated2026-10-02T00:55:12Z, closed at inspection. Author-reported tier scores: intro1.1514,hard1.3884,scale1.1277,stress1.0914,congested1.3111,designs1.4354. Current outputs were not independently rescored in this check. Corrects earlier chat mapping: congested is not ahead, designs has1.4354 rather than stress. No global leaderboard supremacy claim.

Description: incremental root-distance-seeded A*, fanout-scaled negotiated congestion, exact fixed-owner reroute, seed-net excess-bound priority, small-window rip-up, seed-first routing and conflict-driven repair, nonincreasing physical acceptance, continuation of several distinct solutions, integer radix queue. Hard runtime author-reported34core-hours; cannot compare algorithm efficiency with our short recent passes. No compiled solver source in recursive submission tree; author offers source on request. No contact made and no routes imported as warm starts.

Our whole-net adaptive blocker groups differ from the described window-selected conflict-driven reconstruction. Next concrete experiment: select a small window around a detoured seed branch, free affected whole nets transactionally, route the seed first, repair displaced nets, exact-polish and accept only nonworse total physical delay. Compare against existing adaptive controls with matched work and repeated seeds; retain diverse local incumbents for continuation. This remains a proposed experiment, not implemented evidence. Partial branches require an additional coherent tree/boundary contract.

Source: https://github.com/partcleda/eda-3d-routing-challenge/pull/3 . Snapshot: docs/evidence/phase3/pathfinder-lns-current-description.json.

Read-only public API inspection; no solver runs or background jobs. Scores remain independently verified local incumbents from previous checkpoint.

# Seed-first whole-net window repair

Independent prototype uses existing4/8/12 XY windows across all layers to select whole nets. Route the seed first, freeze its ownership, negotiate the remaining selected nets, then exact-polish every net. Replacement paths can leave the selection window; external nets and all foreign terminals remain protected. Outer snapshot restores failed, expired or nonimproving transactions. This is not partial-branch stitching or a reproduction of unavailable competitor source.

Warning-free build;37 focused checks pass, including new crossing work-cap/checkpoint repetition at1/20/100/1000 expansions with repair-first enabled. Existing crossing checks now include window kernels. Source/engine wrapper frozen during timing runs.

Matched hard01/04/07,seeds1–3,3M expansions each,schedule2/1/1:18 officially legal trials,all reach exactworkcap;window2wins/6ties/1loss versus adaptive,geometric delay ratio1.00007837. Adaptive851 attempts/3acceptedgrouprepairs versus window107/2. Screen wrapper30.267s. Keep experimental,not universal/default. No unseen-case superiority or CPU speed claim.

Fixed seed1 full9case window3M continuation costs12.098s wrapper and improves06by34delay,07by10;seven unchanged including reserved08/09. Hard1.256758876094034. Critically, zero accepted window repairs in this stage: gains came from ordinary single-net polish. Do not attribute full-tier gain to the new operator. Added continuation effort is separate from the matched screen.

Pinned CLI independently verifies45/45 selected outputs in tier-window-followup-coverage.json. Otherfive scores unchanged. Canonical selection stores scope,ancestry,archive hashes;original source/manifests/routes retained. Missing older ancestors/reference-generation cost remain unknown; no final freeze or complete regeneration claim.

Next concrete experiment: target windows around seed ideal-path conflicts rather than random incumbent vertices, compare conflict-driven group expansion and retained adaptive controls. Existing window scoring favors large nested boxes; partial branches need a coherent boundary/tree contract. Keep multi-start distinct-basin continuation as a separate direction.

No running optimization jobs; archive restoration checked separately. PDF untouched, no push/publication.

# Conflict-centered whole-net windows

The new conflict mode finds an improving ideal seed tree while protecting foreign pins, includes every displaced owner and rejects over-cap groups. A seeded4/8 XY window around a conflicting ideal vertex adds up to three local nets across all layers. Exact seed-first fixed-owner reconstruction, negotiated repair and final exact polish use existing transactional rollback. No unselected owner is displaced; routes can leave the selection window. Whole-net rebuilding remains a limitation; no partial-branch stitching or competitor-source reproduction.

Warning-free C++17 build;37 focused checks pass, including crossing work-cap checkpoints/repetition at1/20/100/1000 expansions with conflict repair first. Engine/wrapper frozen throughout experiments.

Matched hard01/04/07,seeds1–3,3M work,schedule2/1/1:27 legal outputs,all exact3M expansions,45.355s total wrapper. Existing window2wins/7ties/0losses,geometric delay ratio1.00011580 versus adaptive. Conflict-window2wins/5ties/2losses,ratio1.00029718. Group attempts/accepted:adaptive877/2,window108/2,conflict275/2. Conflict mode has higher aggregate ratio but mixed outcomes; both remain experimental,default unchanged. No universal superiority or CPU speed claim.

Fixed seed1 conflict-window full-six continuation,3M per case,group3 for scale/congested/designs and13 elsewhere; schedules hard2/1/1,congested2/4/4,others2/2/2. Added96.787s wrapper,not a matched full-tier comparison.31cases improve/14unchanged;all six aggregates improve. Accepted group moves intro23,hard1,scale11,congested1,designs1,stress0. Single-net polish also improves these outputs;stress gain comes from polish only. Reserved hard08/09 evaluated with frozen config; both unchanged.

Current independent pinned CLI scores,45/45legal: intro1.098317782147403,hard1.256997693901798,scale1.0479000969718766,congested1.098592335143899,designs1.2303118137738096,stress1.02137484120527. Evidence conflict-window-screen.json,conflict-window-all-tiers.json,tier-conflict-window-all-tiers-coverage.json. Canonical selection and six compact archives preserve route/source/manifest bytes; earlier selection history retained. Missing older ancestors/reference-generation costs remain unknown;no final freeze or end-to-end regeneration claim.

Next concrete action: compare continuation from distinct local basins with single-incumbent continuation under matched effort on designs/congested,where competitor gaps remain substantial. Seed freezing and whole-net reconstruction can prevent cooperative improvements; consider reversible seed release or coherent branch repair only after this comparison.

No optimization jobs running. User PDF untouched;local commits authorized,no push/publication.

# Archive diversity and graph-cut recombination

Researched scatter-search/path-relinking author sections,MAPF-LNS experiments,MAPF-LNS2 repository overview and restricted decision-diagram LNS sections. Detailed source/scope notes in docs/research/DIVERSITY_AND_CLOSURE.md. No third-party code copied/executed. Developed a two-parent tree recombination reduction to minimum-weight closure: alternate tree conflicts imply selecting the corresponding alternate owners; exact max-flow minimizes summed physical delay within those candidate sets. Every terminal/branch/via endpoint participates. This is restricted exactness,not global routing optimality.

Inventory freezes locally generated complete alternative runs within5percent delay on designsctrl/congested01. Geometry diversity does not prove different basins. Three matched seeds,current/older/donor,3M each:18legal,all exactworkcap,25.552s wrapper. Older continuation loses3/3 on both tiers. Donor designs2wins/1loss,ratio1.00028202;congested3ties. Selected fixed seed1 full designs donor/congested adaptive stages improve all7cases,add10.472s wrapper. Full designs gains have zero donor-labelled accepted moves;ordinary repair/polish attribution retained.

Independent graph-cut routine passes2focused checks including exhaustive subset enumeration on200random graphs and explicit dependency examples. Maximally divergent pair gives no gain. All7designs/8congested frozen candidate archive pairs checked against new fixed base,with best pair selected per case. Designs no gain;congested01 gains2delay units and all other cases unchanged. Recombination selection5.777/10.050s excludes rescorers,initial rejected pairs and historical generation. Zero-budget checkpoint retains winning congested mixture unchanged. Known archive generation deduplicated in inherited portfolio;missing ancestors/reference-generation remain unknown.

Current selected scores: intro1.098317782147403,hard1.256997693901798,scale1.0479000969718766,congested1.0988489911881147,designs1.2309315470922892,stress1.02137484120527. Independent pinnedCLI confirms45/45legal. Latest coverage tier-diversity-recombination-coverage.json,canonical selected.json and compact new designs/congested archives. Otherfour routes unchanged. No final freeze/global-best/end-to-end regeneration claim.

Next concrete action: optional neutral group acceptance only when geometry changes,with best legal checkpoint retained; compare against strict-improvement controls on designs/congested repeated seeds. This can explore equal-delay plateaus without uphill submitted scores. Candidate-pool/branch alternatives remain ranked in research notes.

No optimization jobs running. PDF untouched;local commits authorized,no push/publication.

# Neutral geometry moves and score interpretation

Official liveREADME inspected2026-10-02 ranks separately per tier. Aggregate means geometric mean of case ratios within that tier;there is no official combined six-tier aggregate. Runtime/Pareto comparison remains separate. Source https://github.com/partcleda/eda-3d-routing-challenge#leaderboard;local scorer/leaderboard-all also inspected. No private all-tier metric is presented as official.

Added accept_equal0/1(default0),wrapper --accept-equal. Accept a legal equal-total-delay group only when at least one sorted tree edge set changes. Reject identical no-ops;rollback failed/expired candidates. Ordinary exploration stays physically nonincreasing,thus retains best score. Legacy uphill modes still restore their best snapshot. neutral_moves counted separately;accepted_replacements now includes neutral moves when enabled. Adaptive rewards still use strict physical gain. No tabu or cycle-prevention claim.

Warning-free build;38focused checks pass,including default/explicit0identity,invalid2rejection,crossing neutral moves,work1/20/100/1000checkpoints,repetition and official legality/nonworsening. Source/wrapper frozen through timing runs.

Two matched designsctrl/congested01 screens,seeds1–3,group3,schedules2/2/2 and2/4/4:12legal outputs at3M,18.106s wrapper;12legal at10M,37.201s. Every output reaches exact declared expansion cap. At3M:designs1win/1tie/1loss,ratio0.999988697;congested2wins/1loss,ratio0.999967020. Both rejected at this budget. At10M:designs2wins/1loss,ratio1.000667555;congested3wins,ratio1.000418665. Retain optional mode at longer budgets for these tiers;no universal/default claim. Neutral counts3M31/72,10M97/223 are exploratory activity,not improvement evidence by themselves. Equal expansion work is not equal CPU cost.

Fixed seed1 full7case neutral10M continuation adds20.547s wrapper;all7improve. Designs116neutral+32strict group moves,congested160neutral+30strict group moves;single-net polish also contributes. Designs1.233660171993183;congested1.100430490710471. No matched full-tier superiority claim;added effort and pilot costs separate from historical generation. Otherfour selected outputs unchanged:intro1.098317782147403,hard1.256997693901798,scale1.0479000969718766,stress1.02137484120527. PinnedCLI independently confirms45/45legal in tier-neutral-followup-coverage.json. Canonical selection,newcompactarchives and restored original hashes retained. Missingolderancestors/reference-generation limitations remain;no finalfreeze/globalbest/end-to-end regeneration claim.

Next concrete action:matched longer-budget hard01/04/07screen with strict controls before any hard full-tier adoption;record regressions and neutral cycles,consider short tabu history if geometry cycling wastes work. Keep reserved08/09 out of operator selection.

No optimization jobs running. PDF untouched;local commits authorized,no push/publication.

# Weighted seeds, hard neutral exploration and iterative fusion

Completed checkpoint detailed in docs/summaries/SAMPLING_FUSION.md and docs/research/SAMPLING_AND_FUSION_FOLLOWUP.md. Read primary MAPF reevaluation, SAT net selection, fusion/graph-cut sources with reading scope documented;no third-party source copied. Repair sampling0/1/2 defaults0 and preserves unique group membership. Matched weighted trials reject adoption on both tested tiers. Optional donor-preference closure tie-breaking passes exhaustive lexicographic checks but adds no scored gain. Strict iterative fusion saves10delay on congested03.

Hard neutral10M matched pilot5wins/4losses;fixed full9case continuation improves7/unchanged2. Designs/congested retained shuffled neutral continuation improvesall7. Added full-stage wrapper20.242s hard and22.282s others;pilot47.293s hard/44.347s weighted and42.819s fusion selection separate from historical generation/rescorers. All engine/wrapper versions frozen during each timing run.

Latest independent pinned CLI45/45legal: intro1.098317782147403,hard1.258790632279399,scale1.0479000969718766,congested1.1021197794267317,designs1.2361933015773814,stress1.02137484120527. Coverage tier-sampling-fusion-followup-coverage.json;canonical selected.json updated with history. Three new compact archives and45restored route hashes verified.39engine checks/3closure checks pass;warning-free build and Python syntax checks. Missing older ancestors/reference generation remain unknown;no final freeze/regeneration/global-best claim.

Next concrete action: profile eligible blocker-group formation and repair cost,then compare bounded diversified fresh candidate generation against incumbent continuation under matched effort. SAT compatibility selection and partial-branch repair remain unimplemented research options.

No optimization jobs running. Root PDF untouched. Local commits authorized;user pushes/publication.

# Eligibility-aware blocker avoidance

Profiled existing selected-stage timer/counter records;owner snapshots below0.14percent of optimization,frequent over-cap proposals onscale/designs/congested. Research primary ILS perturbation/acceptance sections and linkage-learning abstract;scope in ELIGIBILITY_AND_RESTARTS.md,no third-party source copied.

Added restart_fine with tight A*/16-unit pricing;matched18legal10M trials lose9/9 versus neutral adaptive,47.187s wrapper. Some hard legal rebuilt candidates but no incumbent improvement;larger cases incomplete rollback. Keep experimental.

Added escape operator:only on improving over-cap ideals,at most two alternative searches penalize blocking owners' full route vertices. Match18legal10M trials:hard3ties(no alternatives),designs2wins/1loss,ratio1.0007174712;congested3wins,ratio1.0017954082.45.449s wrapper. Optional retention,default unchanged. Full seed1 fixed45case continuation adds109.720s,38improve/7unchanged,all six aggregates improve. Intro/stress fallbackneverexecutes,gainsordinarypolish/repair;otherstage gains also mixed.

PinnedCLI confirms45/45legal: intro1.0999131603791024,hard1.261189538560553,scale1.049271427751818,congested1.1038276065797619,designs1.2385083709435054,stress1.021438627356866. tier-eligibility-followup-coverage.json;selected.json preserves contexts,6newcompactarchives retain originals,45restoredroutehashesmatch.40focused checks pass,warning-free build,Python syntax/diffchecks. Initial over-cap test fixture did not invoke branch;corrected geometry makes it execute without changing solver/evaluator. All timed runs frozen core/wrapper.

Next concrete action: matched scale01 repeated-seed escape/adaptive comparison,then fixed configuration validation on08;measure recovered-proposal physical acceptance before penalty tuning. Research smaller structured perturbations instead of immediate further full restarts. Final freeze/regeneration remain pending;missingolderancestors/referencegenerationlimitations retained.

No running jobs. Root PDF untouched. Local commit authorized,no push/publication.

# In progress: escape attribution and calibration

Current session extends eligibility counters to classify recovered-group attempts/strict/neutral/failed/nonimproving outcomes and summed strict physical group gains. Defaults preserve prior output: repeated designsctrl10M old/new binary stdout identical. Counter gain is associated with selected group repairs,not an incremental causal attribution versus another algorithm. Added escape penalty/options configuration and mandatory-blockers-only option;default4/2/false unchanged.41focused checks pass before screens.

Scale screen complete12legal10M trials,seeds1–3:development01escape2wins/1loss but geometric ratio0.9999375134;validation08threewins ratio1.0001078334. Reject promotion based on declared development gate;validation does not select settings.64.99998s added wrapper. Recovered strict improvements observed on both cases. Current canonical selections remain unchanged until full-stage verification.

Running serial escape calibration matrix ondesignsctrl/congested01,seeds1–3,10M each;default versuspenalty2/penalty8/fouroptions/mandatoryonly. Frozen core/wrapper throughout. Report escape-tuning-screen.json;log /tmp/escape-tuning-screen.log. Next choose only qualifying optional configuration from development,run fixed complete-tier followup,then explore downstream-aware resource pricing separately.

Escape calibration complete30legal10M trials,134.199s wrapper. Declared gate selectsdesigns penalty8(3wins) andcongestedmandatoryonly(2wins/1loss,largestqualifyingratio). Fixedfull7case continuation adds34.367s andimprovesall7:designs1.2405097243072432,congested1.1055495435969123. Tagged recoveredgroupstrict counts19/28 andgrossphysicalgain116/566;notcausalincrementalcomparison. These candidates are retained in raw artifacts pending combined finalcoverage/archive promotion.

Nowrunning serial27trial downstream-price screen,hard01/designsctrl/congested01,seeds1–3,10M each,uniform versusold-tree downstream modes1/2. Tree-local sinkcounts checkedagainst3handexamples/100independentindividualpathoracles;41existing+2newfocusedchecks pass. Source/wrapper frozen;logs /tmp/tree-pricing-screen.log,report tree-pricing-screen.json. This is a new topology-aware pricing hypothesis,not the component-merging paper algorithm or guarantee. Current canonical selection unchanged until finalverification.

Downstream screen complete27legal exact10M trials,119.681s wrapper. Selecthard model2(3wins),designsmodel1(3wins),congestedmodel1(2wins/1loss),keepingdefault0. Flow setup about6.3percent of hard optimization and1.2percent large representatives;expandedwork does not account for this CPU overhead. Added fixedall45case20M stage improves39/unchanged6,all6scores. Strict two-parent fusion saves4delay onhard04;other two tiers nofusiongain. Zero-budget checkpoint preserves hardfusion. Independent pinnedCLI45/45legal in tier-tree-pricing-followup-coverage.json. Current candidate scores intro1.1027993426079046,hard1.266947801241802,scale1.0517563683407252,congested1.1115412514063856,designs1.2507253940346224,stress1.0216409732905487. Canonical archive selection will be promoted after current experiment.

Continuing exact recent-geometry memory trial:neutral_tabu0/8/32,three seeds/three representatives/10M.42focused engine checks pass,including actual repeated-neutral-state rejection and legal deterministic work-cap recovery.4closure checks pass including inherited portfolio cost repair. Running serial neutral-tabu-screen.json with frozen core/wrapper;log /tmp/neutral-tabu-screen.log. Finite exact memory is optional and does not prevent all cycles. Next choose measured optional setting or reject,then preserve best complete tiers and restore hashes.

# Downstream pricing checkpoint and active continuation


Current selected routes are legal on all 45 cases, verified with the pinned evaluator and the current upstream model/checker/scorer/CLI modules. Current upstream revision: `0a8e052944432de0c657f3d45d6838394e627d63`. All 96 current benchmark files match the pinned Git blob hashes. Parser changes reject malformed coordinates; score aggregation now uses math.fsum. Saved scores agree. Current contribution rules allow generated README leaderboard changes and require derived_from metadata for public route reuse. No competitor routes were adopted.

## Measurements

Downstream pricing screen: 27 legal 10M-expansion trials, seeds 1–3. Retain model2 on hard (3 wins), model1 on designs (3 wins) and congested (2 wins/1 loss). Default remains0. This is old-tree resource reweighting, not the cost-distance paper's component-merging algorithm. Equal expansion ceilings do not equal CPU cost.

Escape tuning: 30 legal trials; designs penalty8 and congested mandatory-only meet development gates. Scale escape fails its development geometric-mean gate; retain adaptive. Reserved validation cases did not select settings.

Full 45-case 20M continuation improves39 cases, leaves6 unchanged. Two-parent closure fusion saves4 delay units on hard04. Neutral memory screen: all18 candidate comparisons tie; reject adoption. Larger hard groups: cap24 wins4/9 and cap40 wins3/9, both geometric means below1; retain cap13.

Whole-case portfolio selects among the declared local trial pool and complete stages. Its scores are output competitiveness measurements with extra seed/configuration selection effort, not uniform solver benchmarks. Six zero-budget checkpoints preserve selected routes. All45 archived route hashes restore correctly. Current focused checks:43 engine,2 flow and4 closure checks pass. No full upstream test rerun claimed.

## Scores

- intro: 1.1027993426
- hard: 1.2687429717
- scale: 1.0517899453
- congested: 1.1120190457
- designs: 1.2520683047
- stress: 1.0216409733

## Running continuation

Three rounds, seeds4/5/6, 20M expansions per case,60s safety cap, two independent tier workers. Plan: dev/configs/downstream-continuation.json. Progress/logs: dev/artifacts/20261002-ongoing-downstream-portfolio/progress.json and /tmp/ongoing-downstream-portfolio.log. Session69273. Each completed round is officially rescored; canonical selections are not edited automatically. Create STOP inside the artifact directory to stop between stages. Source/wrapper/binary are frozen while running.

Older missing ancestors and reference-generation costs remain unknown. Phase3 continues; final regeneration/freeze/submission preparation remain pending. User handles publication.

Next: review completed continuation rounds and preserve improvements; prototype partial-branch rerouting after profiling whole-net group failures.
