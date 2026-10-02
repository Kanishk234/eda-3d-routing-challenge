# Eligibility and restart experiments

## Research inspected

[Iterated Local Search: Framework and Applications](https://iridia.ulb.ac.be/~stuetzle/publications/LouMarStu10.pdf): inspected perturbation strength/adaptation sections3.2.1–3.2.3 and acceptance interaction discussion. Perturbation size and acceptance depend on problem structure; small perturbations may return to the same solution, while full restarts can waste useful structure. This motivates a matched whole-case rebuild screen and conditional alternative proposals. No routing guarantee or reproduction of the chapter's reported experiments claimed.

[Iterated Local Search with Linkage Learning](https://arxiv.org/abs/2410.01583): abstract only. Weighted variable interactions guide perturbations in pseudo-Boolean problems. Possible future analogue: use observed net blocker interactions to select groups. No linkage learner implemented and no pseudo-Boolean guarantees transferred to routing trees. No third-party source copied or executed.

## Profile and hypotheses

Existing selected-stage timers summarized in selected-repair-profile.json. Owner snapshot fraction is below0.14percent on every tier;these observations do not support making snapshot removal the next change for these runs. Profiles omit some operations and are not an exclusive CPU attribution. Over-cap proposals:scale109/210,congested908/1630,designs476/1013;hard77/6399. This motivates trying alternatives specifically for over-cap proposals, rather than weighting repeatedly rejected seeds.

restart_fine adds current16-unit congestion pricing and consistent tight A* to the existing whole-instance transactional restart,including three exact polish passes on legal rebuilds. Matched hard01/designsctrl/congested01,seeds1–3,10M:18legal outputs,9restart losses against neutral adaptive continuation. Hard15attempts/5legal rebuilt candidates but no incumbent gains;larger cases3attempts per tier/zero complete legal rebuilds.47.187s wrapper total. Incomplete/worse candidates restore originals. This mode remains experimental;no candidate pool is exposed.

Escape mode: when a physically improving ideal tree exceeds the blocker cap, generate at most two alternatives with cumulative nonnegative penalties on vertices of its current blocker nets. Foreign pins remain protected. Prefer fewer blocker owners,then physical delay;only a physically improving proposal that fits the cap reaches existing negotiated repair. This is a proposal heuristic;physical acceptance, ownership rollback and output checking are unchanged. Added searches count toward the same expansion cap. Default adaptive mode is unchanged. Tests and measured results are recorded separately in eligibility-screen.json and the session summary.

Matched escape screen18legal exact10M outputs:hard3ties(no fallback searches),designs2wins/1loss geometric delay ratio1.0007174712,congested3wins ratio1.0017954082. Alternative searches/recovered eligible proposals:designs360/109,congested939/303. Eligibility is not acceptance or scored improvement;existing group repair and single-net polish also contribute.45.449s total wrapper. Retain optional for designs/congested,default unchanged. All-tier fixed follow-up is added effort and exploratory outside the screened representatives.
