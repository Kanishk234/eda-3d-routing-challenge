# Eligibility-aware repair checkpoint

Goal: find useful candidate routes when the initial ideal would displace too many whole nets;compare strong fresh rebuilds against incumbent continuation.

Profile selected-stage counters before implementation:selected-repair-profile.json. Snapshot costs below0.14percent of optimization time;over-cap proposals frequent on scale/designs/congested. These are partial timers,not exclusive CPU attribution. Research scope in research/ELIGIBILITY_AND_RESTARTS.md.

restart_fine combines existing restart with tight A* and16-unit pricing.18legal matched10M trials,seeds1–3 onhard01/designsctrl/congested01:9losses versus neutral adaptive. Hard15freshattempts/5legal rebuilds,larger tiers3attempts each/zero legal rebuilt candidates.47.187s wrapper total. Output legality reflects preserved checkpoints,not all fresh attempts. Reject adoption;no diverse candidate pool exposed.

New escape mode only adds alternative searches when an improving ideal exceeds blocker cap. At most two proposals cumulatively penalize blocker nets' whole-tree vertices;choose fewer displaced owners then physical delay. Foreign terminals,wide priorities,exact physical acceptance and transactional rollback remain intact. These are heuristic proposals,not constrained shortest-path optimality.

Matched18legal exact10M trials:hard3ties/no alternative searches;designs2wins/1loss,geometric delay ratio1.0007174712;congested3wins,ratio1.0017954082.45.449s wrapper. Alternative searches/eligible proposals360/109designs,939/303congested. Retain optional,default adaptive unchanged. Generated eligibility is not accepted-move evidence.

Fixed seed1 all45case follow-up adds109.720s wrapper,38cases improve/7unchanged;all six scores improve. Group13intro/hard/stress,3others;schedules hard2/1/1,congested2/4/4,others2/2/2. Equal group geometry enabled hard/designs/congested only. Full-stage eligible proposals hard57,scale106,congested197,designs116;intro/stress0,so their gains cannot be attributed to fallback. Ordinary polish and repair contribute elsewhere too. Unscreened tier results are fixed exploratory evaluation;no matched whole-tier superiority claim.

Independent pinnedCLI45/45legal: intro1.0999131603791024,hard1.261189538560553,scale1.049271427751818,congested1.1038276065797619,designs1.2385083709435054,stress1.021438627356866. Evidence tier-eligibility-followup-coverage.json;canonical selection retains earlier provenance. Six new source/routes/manifest archives restored with all45original output hashes matching.

Warning-free C++17 build;40focused checks pass. Added explicit over-cap fixture with three blocker trees:alternative-search/eligibility branch executes;caps1/20/100/1000/10000 preserve legal nonworsening checkpoints and identical stdout across2/5second safety budgets. Existing work-cap/mode checks include all escape kernels and restart_fine. Initial fixture failed to exercise fallback because ordinary detour was already cheaper than penalized ideal;corrected fixture,not solver/evaluator behavior. Python syntax and diff checks pass. No new full upstream test claim.

Limits:reference warm starts attributed;missing old ancestors/reference generation costs unknown. Screens and continuation add effort beyond historical generation. No final freeze, complete regeneration, unseen-case/global-best or global-optimality claim.

Next: repeated scale01/08 screen of escape versus adaptive at fixed work,keeping scale08 as validation rather than choosing settings from it;also measure which recovered proposals lead to accepted physical gains before tuning penalty strength. Full-case restarts need more generation budget or smaller perturbations before further adoption.
