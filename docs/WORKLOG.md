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
