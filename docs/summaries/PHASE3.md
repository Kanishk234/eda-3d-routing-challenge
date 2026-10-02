# Phase 3 — in progress

GitHub synchronization brought eight further commits through38b3a49. Best
recorded hard is1.230658/congested1.090605 in tier-schedule-coverage.json;
locally available recovered hard routes score1.227449. Work-budget, cached
lookahead, fine-pricing and schedule controls coexist with neighborhood modes.
The merged implementation has compiled and syntax checks only, not a new
benchmark or unit-test result. Historical raw GitHub artifacts remain unavailable.

## Latest: recovered incumbents and diverse neighborhoods

Restored .venv/pinned archive and rebuilt C++17 engine after ignored historical
artifacts were missing. A new fixed20s/1000cycles/seed1 fanout A* run from
official hard references gives1.215286,9/9 legal. This is a new assisted recovery
pipeline, not regeneration of historical routes.

Implemented optional shuffled negotiation order, two corridor-repulsion
proposals, and adaptive direct/transitive/random repair groups. Matched hard
01/04/07, seeds1–3,5s screens: shuffle wins7/9 versus original; diverse9/9;
adaptive5/9 with two ties/two losses. Diverse beats shuffle6/9 and loses3/9.
All36 screen outputs legal. Six10s100vs1000cycle runs all hit time caps;
two delays identical and the third differs by8, so no causal cycle-limit gain.

Selected fixed seed1 diverse20s/1000cycle stage from recovered routes, without
per-case seed/config selection. Run20261002T001313.450750Z-exact-polish is
officially legal9/9 and independently rescored1.2274487880088916. All9 improve
over recovery; versus historical1.220250,6 improve/3 regress, score up0.5899%.
Two-stage wrapper sum363.756s excludes reference generation and260.844s screens,
plus separate scorers; selected stage core180.437s/wrapper182.321s. No speedup
or unit-test claim. Source/config/route hashes and ancestry in
neighborhood-hard-coverage.json and recovered-neighborhood-comparison.json.

Current hard artifacts exist locally; other tiers' old routes remain unavailable.
Final freeze/regeneration/submission checks remain pending. Next measured work:
combine corridor diversity with localized random/transitive groups, retaining a
matched shuffle/diverse control and protected held-out08/09 validation.

First controlled operator screen: shortest-path blocker-group repair. Start from the validated Phase2 routes, propose exact driver-rooted trees ignoring routing ownership while retaining foreign-pin protection, identify up to4 blocking nets, release the group transactionally, sequentially reroute it and accept only a legal group with lower total physical delay. Failed/expired attempts restore the full ownership snapshot and old group trees. The Python official checker remains the acceptance boundary.

Screen hard01–07 only, seeds1/2/3,2s/case,5passes,one worker:21/21 outputs legal,0 improvements. Core wall sum1.621s, wrapper wall sum11.576s. No portfolio selection, validation-case use or full-tier score claim.15 kernel checks pass; targeted group success/rollback coverage is still limited and should expand before retaining this operator. Evidence: docs/evidence/phase3/repair-screen.json; raw source snapshots/manifests/routes remain ignored.

Reject this implementation as a default optimization: no observed benefit on the development screen. Keep it as an experimental reference. We have not measured how many proposals exceed the group limit, fail sequential repair or lose delay; do not infer the cause from zero improvements. Current best remains Phase2 score1.046629.

Next: add repair outcome counters, independently exercise failed/successful group transactions, then use measured failure distributions to choose bounded alternative paths/windowed groups or congestion negotiation. Root-aware construction and negotiated-congestion controlled comparisons remain open. Phase3 is not complete.

## Occupied-vertex penalty repair retained

Diagnostics of the first operator:1638 proposals,117 no physical gain,1371 exceed4 blockers,150 attempted repairs,54 failed,96 legal but nonimproving. This supports testing less disruptive paths rather than blindly increasing group size. Added a cost4 penalty per occupied vertex in proposal search only. Physical driver-to-sink delay is independently accumulated along predecessor paths and checked officially; penalties never enter reported delay. This is heuristic candidate selection, not an exact physical shortest-path claim.

Matched development screen: same warm start/cases/seeds,2s/case and5passes.18/21 improve; all legal; case02 unchanged for every seed. Full per-run results and process counters in repair-soft-screen.json. Total development core4.104s/wrapper14.327s, excluding earlier diagnostic/screen costs. No per-case seed portfolio selected.

Fixed seed1 config then validated all9 hard cases:8 improve,1 unchanged, aggregate1.0529719287378287 vs Phase2 1.0466292119096317. Reserved hard08 delay29562→29426,hard09 26376→26166. Official CLI independently agrees. Selected run20261001T213751.861916Z-exact-polish; outputs hashed in soft-validation.json. Core2.149s/wrapper3.913s added to earlier baseline-plus-polish97.952s gives summed pipeline101.865s, not fresh end-to-end timing.16 kernel checks pass; successful and failed group attempts additionally checked in benchmark outputs. Keep group fixture coverage limitation explicit.

Retain repairsoft as an optional stage because it improves development and validation without legality/quality regressions under this configuration. No global-optimum, speedup, unseen-case or best-public claim. Phase3 remains open: root-aware construction/negotiation comparisons, richer group transaction fixtures and later controlled methods. Next concrete work is a driver-aware construction ablation and negotiated repair comparison using fixed development budgets.

## Driver-distance construction ablation

Compared three constructions on546 nets across hard01–07 with every other net fixed: exact root Dijkstra, incremental attachment seeded by driver distance, incremental attachment seeded at zero. All546 complete; root-aware costs match exact for every net. Zero-source case sums exceed exact:11794vs11614;18438vs17882;14200vs14070;17611vs17173;20801vs20359;26768vs26176;29997vs29379. These sums are independent-net measurements, not jointly legal solutions or official tier scores. The case06 exact sum below the incumbent illustrates that finite polishing passes need not reach a fixed point. Retain exact root kernel; no benefit shown for replacing it with repeated attachment searches.17 tests pass. Candidate experiment outputs remain original accepted incumbents.

Submission layout rechecked against current upstream3d8948fdcd6f87165d5ca1efbf4b65e8168e8e81: CONTRIBUTING.md and workflow are byte-identical to pinned versions. Submission PR allows only submissions/<tier>/<method>/** plus generated LEADERBOARD.md. Solver/dev/docs stay in development checkout; clean submission checkout is still Phase5. Upstream advanced by Windows UTF-8 fixes in cli.py,verify_submissions.py,test_leaderboard.py; no benchmark/checker/scorer changed. Retain existing experiment pin for comparability, recheck current evaluator before submission.

Next: implement bounded group negotiated-congestion repair with conflicting states internal, safe transaction rollback, and physical scoring only after conflicts are zero. Compare to fixed repairsoft on development cases before validation. Phase3 remains incomplete.

## Negotiated repair checkpoint

Bounded12-round negotiation uses hard external-net/pin constraints,group usage/history penalties and transaction rollback. Only conflict-free groups with lower total physical delay commit. Same development warm starts/seeds/cases,2s/case,5passes:21/21 improve over Phase2,all legal. Against sequential soft repair,19 improve and2 regress(case05 seeds2/3:20091→20145 and19633→20029). Fixed seed1 full hard9/9 legal score1.0710212727385569;all9 beat sequential including reserved08/09. Official CLI confirms;19 checks pass. Core6.594s/wrapper8.233s;baseline+polish+negotiation component total106.185s excludes screen/scoring costs and is not freshly timed end-to-end. Starts at Phase2 routes,not sequential-soft outputs.

Controlled comparison exit evidence now exists for all listed Phase3 methods. Further optimization continues before final freeze because the competitive gap remains large. No final submission freeze selected. Next: plateau/tie exploration and larger coordinated neighborhoods,controlled on development cases.

Public hard re-audit October1:13 route-submission PR heads(open and closed),117 routes all legal. Highest checked artifact is closedPR11 mj97 score1.3873941742426144;highest open is PR3 pathfinder_lns1.387366331135629. NewPR12 1.3608582696910276 andPR14 1.0799588344034654. These are pinned-output quality,not reproduced solver/runtime or global/current-private best claims. Evidence current-public-hard.json includes heads and output hashes. No public outputs adopted as warm starts.

Report-writing bug:negotiation freezer initially overwrote soft-validation.json. Restored original soft report from4bbf016,preserved negotiation report as negotiated-validation.json and corrected mode-dependent filename. Route outputs and their official scores unaffected. Earlier attempted phase-exit doc write stopped before updating docs; subsequent commit title overstated documentation completion. This section records the actual state.

## Basin escape and research checkpoint

Implemented exact equal-cost tie diversity and legal equal-delay moves followed by negotiated repair. Development21-run screen:all improve over Phase2,18 improve/3 regress vs negotiated;all three seven-case aggregate scores improve. Fixed seed1 stage after negotiated warm start:full hard9/9 legal,all cases improve,official score1.1059077449039443. Extra wrapper10.837s;component pipeline sum117.023s.22 checks pass. Whole-instance geometry-free restarts screened separately:9/21 improve under2s cap;not retained as default. Raw pilot manifest215416 and source/research provenance retained.

Read PathFinder/SALT/MAPF-LNS2/node-disjoint-path primary sources andMIT public m3d-router source(pinned0027d807),no code copied/executed. Findings/transfer limits/next alternatives in docs/research/OPTIMIZATION_FOLLOWUP.md. Next candidate:restricted compatible-tree selection and broader destroy/rebuild,not only more sweeps of current greedy groups. No final freeze or global optimum claim.

## Joint selection and broader neighborhoods

Implemented candidate-tree selection:original plus up to6 root-shortest variants per net with tied predecessors and occupancy penalties0/2/4. Groups at most5 nets,external owners/pins fixed. Branch-and-bound picks a compatible combination with minimum physical delay inside generated candidates;time-limited searches preserve any improving feasible combination. Screen21 dev runs:9 improve over Phase2,many worse than negotiated methods.967 searches exhausted generated sets,21301 nodes;944 yielded no legal improving combination. No global optimum claim. Not default.

Implemented wide exploration:equal-delay moves plus max12 blockers(13 nets) and24 negotiation rounds vs previous4 blockers/12 rounds. Same21 runs/caps:all legal,all improve over Phase2;per-seed aggregates and regressions in neighborhood-comparison.json. Changes to group size and round cap bundled;do not attribute gains solely to either.25 checks pass. Selected fixed seed1 config for full-tier validation after current incumbents,next. No public warm starts.

## Budget scaling and full-tier wide validation

Two-second cap is only local screening,not official rule. Matched representative cases01/04/07,seed1,100-cycle ceiling fromplateau starts:2→10s reduces delays10524→10094,15909→15063,27797→26663;allruns hit cap. Fixed10s/100-cycle wide configuration then validates hard9/9 legal1.1834968761196418;all cases improve vs plateau1.105908. Official CLI agrees. Run220349;core90.135s/wrapper91.845s;component pipeline sum208.868s excluding all screens/scorers. Not fresh end-to-end timing or convergence proof.25 checks pass. Current incumbent paths/hashes in wide-validation.json. Next:controlled legal threshold acceptance with immutable best state,matched development comparison.

## Controlled threshold walk

Implemented legal temporary worsening:group delta may be at most1% of its old delay and acceptance probability1/4;zero-delta moves use the same rule. Separate full-route/ownership best snapshot updates only on lower total delay and is restored on normal/signal timeout exit. Conflicting negotiated states remain transactional and never output. Counter named uphill_moves includes sideways moves. No annealing/optimality claim.

Matched representatives01/04/07,seed1–3,2s/100 passes fromplateau starts:walk9/9 improve vs starting routes,6 better/3 worse than strict otherwise-identical descent.226 sideways/uphill accepts;no output worsens its starting incumbent. Fixed seed1 extra2s stage after wider10s current routes:9/9 legal,6 improve/3 unchanged,official1.1868734408645938.26 checks pass. Run220917;core18.225s/wrapper20.000s. Reports now recursively trace warm-start stages;component pipeline228.868s excludes independent screens/scorers and is not fresh end-to-end timing.

Retain this short extra stage as incremental improvement;do not silently replace longer search with2s or select seeds per case. Current routes in220917/routes. Next:compact near-shortest tree/fanout-aware congestion hypotheses to reduce routing resource use,then bounded initialization/restart allocation. Candidate selection remains experimental,not default.

## Compact/fanout resource-price results

Matched representative01/04/07,seeds1–3,2s/100 cycles fromplateau routes:all27 outputs legal/nonworsening vs starts. Compact group construction(alpha3/4) wins3/9 vswide,worsens aggregate for everyseed;7/9 use fewervertices thanstarts. Reject asdefault. Fanout group present/history prices divided byceil(sqrt(sinks)) win7/9 vswide,allseed aggregates improve. Some outputs use morevertices;delay alone selects incumbents. Added per-net uniquevertex uses,edges andvias towrapper;counts include viaendpoints andsharedtrunk once.28 checks pass.

Selected fixed seed1 fanout10s/100 cycles extra stage afterwalk:9/9 legal,allimprove,official1.2054914475674077 vs1.186873. Run223212;core90.122s/wrapper91.890s;traced component pipeline320.758s(excludes independent screens/scorers,not fresh end-to-end). Price scaling is heuristic;physicaltotal/per-net delays still officiallychecked. Next:independent fresh-start initialization withthese price/shape variants;no publicwarmstarts.

## Fresh initialization followed by physical polish

Compared original, fanout-priced, compact, and fanout-plus-polish whole-instance restarts on development cases01/04/07, seed1, ten seconds, at most five starts. Polishing each legal fresh state before comparison produced delays9682/15223/28111, versus unpolished fanout9996/15681/28111. Some fresh searches fail to find legal states under this cap; prior verified routes remain the fallback. Internal fresh_legal counters are feasibility observations, not separately officially checked outputs. Evidence: fresh-start-comparison.json.

Fixed configuration then ran after the current fanout incumbents on all nine hard cases. Run20261001T224311.948014Z-exact-polish is officially legal9/9, score1.2093700886234824: case01 improves9966→9682, eight unchanged. Added core84.562s/wrapper86.434s; inherited generation/stage component sum407.192s excludes independent screens/scorers and is not a fresh end-to-end measurement.29 focused checks passed. Retain this as an optional improvement stage; it does not establish reliable independent initialization. Current outputs remain under ignored dev/artifacts; hashes and provenance are tracked in restart-polish-validation.json. No public warm starts or publication.

## Fanout walk and expanded tier coverage

Added fanout_walk and fanout_descent modes, combining existing search prices with existing wide-group protected best snapshots. Matched representatives01/04/07,seeds1–3,2s/100passes from prior best:walk4 wins/4ties/1loss versus strict descent,5/9 improve start. Fixed seed1 full-hard run20261001T225003.513464Z-exact-polish officially legal9/9,score1.212967727395428,4 improve/5 unchanged. Wrapper20.165s; inherited component chain427.357s excludes experiments/rescorers. No new unit checks run; earlier29-check result predates these modes, while every new benchmark output was officially checked and rescored.

User clarified desired scope:aim for all six tier entries,each scored independently. Runner now accepts all official suites. Initial exact-polish coverage uses locally generated intro incumbents and attributed official reference routes for scale/congested/designs/stress. Official rescoring confirms intro20/20 score1.050409,scale8/8 score1.023686,congested4/4 score1.031234,designs3/3 score1.121578. These are baseline-assisted output improvements,not reference-runtime or independent-construction reproductions. Stress short-cap failure recorded in BUGS;successful longer retry recorded below. Final freeze and submission preparation remain unperformed.

## All-tier initial coverage complete

Official CLI independently confirms45/45 legal outputs across six separate tiers: intro1.0504090271124256,hard1.212967727395428,scale1.0236861228944922,stress1.0026008508372637,congested1.031233699656949,designs1.1215781534720441. Explicit selected-run hashes/config/resource records in tier-coverage.json; stress also in stress-coverage.json. Scale/congested/designs/stress start from official challenge references,attributed,not public competitor routes. Intro starts locally generated baseline;hard inherits recorded optimization chain. No cross-tier aggregate.

Stress retry20261001T225241.212774Z-exact-polish succeeds with60s cap:delay1144904→1141934,core60.051s,wrapper78.918s,peakcore92332KiB. Independent rescore2.778s/228068KiB. Short-cap failure remains recorded separately;reference generation cost unmeasured. No tests added/run this session;previous29-check evidence does not cover new combined mode,official benchmark checks do. Full-tier coverage precedes a final freeze and does not establish independent initialization or end-to-end reproducibility.

## Large-case profile and broader measured improvements

Explained lower initial tier scores:unequal optimizer effort and different normalized baselines. Initial scale8/8 hit2s caps;stress short runs could not finish initialization. Instrumented read/validation/optimization. Matched stress60s/seed1/5passes from225241:read44.143→0.424s after tree-local validation,validation43.950→0.250s,searches72→252,delay1141896→1137194. Samecore cap;single-case timing sample,no generalized speedup. Profile/failure evidence retained;official input/checker unchanged.

Screened fanout versus fanout_walk on declared scale01/congested01/designs-ctrl,seed1/5s/100passes:both all improve,fanout lower delay3/3. Chose one fixed fanout config for all scale/congested/designs cases from original coverage routes,not selected per-case representative outputs. Full selected official CLI scores:scale1.0299239499469701,congested1.0406548316718132,designs1.1382735873408656,stress1.0067798458310544;intro1.0504090271124256 andhard1.212967727395428 unchanged.45/45legal;every targeted case improves. Evidence tier-optimized-coverage.json,tier-optimization-comparison.json,coordinated-tier-screen.json,large-case-profile.json. Ancestor optimizer chains/reference attribution now explicit in reporting. No new tests added/run;official checker/scorer checks every selected output. Earlier29 tests do not cover new representation.

Quantum suggestion triaged using primary IBM documentation:tiny restricted simulations may fit CPU/RAM;no quantum access configured or algorithm supplied. Quoted1.0418 below currenthard1.212968;other assessment1.183497 historical. Classical candidate-tree selection already evaluated,9/21 development gains but weaker than negotiated methods. No quantum installation/use or advantage claim. Research note retains references and memory calculations.

## Relaxed headroom,primary-source research,and guided search

Computed analytic obstacle-free pairdelay lower bounds on all45cases,with proof and inputhashes in delay-bounds.json. Optimistic geometric score ceilings:intro1.187031,hard1.761668,scale1.162236,congested1.646832,designs1.811179,stress1.105207. Capacity/foreignpins relaxed;these are upper bounds on attainable score,not jointly achievable results. Higher ceilings motivate congestion/design coordinatedsearch;low sparse-tier scores partly reflect stronger normalized baselines and unequal effort.

Reviewed primary OpenROAD/FastRoute,VTRconnectionrouter,and NeurIPS2020 generalLNS sources;notes/links/transfer limits in OPTIMIZATION_FOLLOWUP. No externalsource copied/executed. Implemented original consistent A* sink-layer rectangle lookahead with exact g cost and unchanged physicalacceptance. Matched60s/seed1/5passes stress from225241/routes:A*1020searches/126572544expansions versus ordinary252/153841664,legal delay1122096 versus1137194. Score1.0203262465956566,officialCLI agrees. Single timing sample/different completedwork and geometry,no equal-work speedup claim.

Added gap-order variant:repair priority=physicaldelay minus relaxed per-net bound. Matched5s/100passes/seed1 representatives hard01/congested01/designsctrl,three modesfanout/fanout_astar/fanout_gap:both new variants beatordinary3/3;gap beatsA*2/3 and losescongested. Selected one fixed fanout_astar full-tier stage from original representativewarmstarts,not selected per-case outputs. Full officialhard1.220250233796514,congested1.0553607547875163,designs1.164826219486074;all16 cases improve. Stressalsoimproves,17targetedcasegains total. Intro1.050409 andscale1.029924 retained.45/45selected outputs officiallylegal. Evidenceguided-search-screen.json,astar-stress-comparison.json,tier-guided-coverage.json,tier-guided-comparison.json. No new tests added/run;earlier29 checks predate A*/gap variants. Per-caseofficial checking plus independentCLI rescoring performed.

## Guided repeats,budget curves,freshstarts,and cost-distance research

Built dev/guided_screen.py for frozen representative starts and serialexplicitconfig screens.18trials repeatseeds2/3:fanout_astar beats ordinaryfanout6/6;A*plusgap priority loses5/6vsA*alone,not retained asdefault. Budgetscreen5vs20s seed1:hard01same9292,100cycles exhaustedabout5.33s;congested64591→62981,designs61266→59844,bothstillcapped. Guidedfresh20s/max5starts improvescongested65617→62163;hard/designs preserveincumbents. All30screenoutputs legal;screenwrappercost223.803s includes rejectedconfigurations,not generationcost.

Read full Held/Perner2025cost-distance paper fromuser's suggestedsource. Prototype discounts existingtreecongestion while retaining fullphysicaldriverdistance/allunit sinkweights. It is a greedyadaptation,not theircomponentmerging algorithm/guarantee. Screenhard9284vsastar9292,congested65459vs64591,designs61712vs61266;rejectasdefaultafter2/3regressions. Researchnotes correct staleinterest snapshot,distinguishmergedboard frompublicPRheads,and keepreferenceattribution;writtenruleswarmstartsilence acknowledged,noissue/comment sent. Sourcecode map addedto dev/README.md inresponsetouser.

Fixed20s/100cycles/seed1fanout_astar fullcongested4/4 anddesigns3/3 allimprove. Optionalcongested restart_astar20s/max5freshstarts afterlongerincumbents adds1casegain/3unchanged. IndependentofficialCLI scorescongested1.0826675712383234,designs1.2124988396182923;hard1.220250,intro1.050409,scale1.029924,stress1.020326 preserved.45/45selectedoutputs legal. Currentselectedroutes/configs/hashes/ancestorcosts in tier-followup-coverage.json;comparisonandscreenmanifests tracked. No newtests added/run;officialper-caseverification plusindependentfulltierCLI rescoring performed.29historicalunitchecks do notcovernew modes. Finalfreeze/workcountdeterminism/regeneration/submissionchecks remainunperformed.

## Review-driven follow-up

Public hard geometry comparison concentrates the signed deficit in multi-sink nets;single-sink aggregate locally wins. Top20 positive gaps explain only25.33% of positive gap. Longer hard cycles improve one representative only. Added expanded-vertex budgets and shortest reset/rebuild profiles;31 focused tests pass,including randomA*/Dijkstra and work-cap rollback/repetition. Large stress10M repeat isbyte-identical across safetycaps and improvesofficialscoreto1.020434. Selected45/45routes independentlychecked in tier-work-budget-coverage.json. Uncontendedstressreset/rebuild totals5.5%ofoptimization;other proposedcosts notyetisolated. Rankednextwork inNEXT_EXPERIMENTS.md. Fullreviewbacklog,finalfreeze,regeneration,and submissionremainunfinished.

## Hard-tier update and tighter lookahead

Hard now1.2300004741250727 afterfixedlong-cyclefull-tierstage(1.229451)andoptional5M-expansiontight-lookaheadstage.9/9legal,independentselectedsix-tierreport45/45legal(tier-kernel-coverage.json). Kernelcontrolcomparisons byte-identical forstoredg and repeatable;no measuredheapgspeedup. Tightbound improveshard/congestedrepresentatives andtiesstress.31focusedtests passincludingtightlookaheadcostequivalence/rollback. Profilingdoesnotjustifybroadownershiprewrite yet. Next:fixed-pointmulti-sinkcongestionpricesundercontrolledworkbudgets. Finalfreeze/regeneration/submissionstillpending.

## Six-source audit and finer congestion prices

Confirmed prior PathFinder/CUGR/cost-distance coverage; reviewed NTHU algorithm sections and PD-II/DAS objectives/pseudocode. DATE paper identified through the user's IEEE ID; only official programme abstract accessible, both conference PDF links404. Research notes distinguish reading from implementation.

Original16-unit price experiment preserves finer fractional congestion penalties with checked scaled priorities and unscaled physical delays. Matched5M representative trials:4wins/1tie/1loss. Fixed seed1 full hard/congested stages improve all13 incumbents. Official selected-tier report45/45 legal: hard1.230324,congested1.088060,others unchanged.31 focused tests pass. Next: configurable history/present schedules and controlled small tuning sweep; final freeze/regeneration/submission remain pending.

## Explicit negotiation schedules and complete DATE reading

Added bounded local-negotiation config with existing defaults preserved. Four schedules on declared hard/congested case01, seeds1–3,5M expansions select2/1/1 forhard and2/4/4 forcongested;both beat default3/3 within their representative tier. Fixed seed1 full-tier stages yieldhard1.230658 andcongested1.090605. Independentselected-tierreport45/45legal;32focusedtests pass.

User PDF parses all7pages and full text was read. Research analysis notes explicit CUGR cost reuse, adaptive via-discount/A* consistency requirements, directed backward costs and incomplete printed search specification. No source/model blindly imported; licensed PDF remains uncommitted. Next:broader development robustness and nonlinear-price/coordinated-topology experiment. Final freeze/regeneration/submission still pending.
