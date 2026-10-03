# Keep refining the routing families

User direction: do not abandon a family after a weak first screen. Preserve diverse legal variants as stepping stones, diagnose behavior, refine them, and compare again. This does not require promoting a worse default. Existing coding-model proposals plus measured compiled execution implement an independent GR-Evolve-inspired loop; no training or external paid API is used.

## Ordering family

First10M screen: conflict-first/last both0wins,6ties,3losses on hard01/04/07,seeds1–3. Retained both. At50M, added delayed ordering,sink-flow-weighted conflict priority and cyclic order. Instrumentation confirms thousands of actual order changes, not an inactive code path.

| Variant | Dev wins/ties/losses | Dev score ratio | Reserved08/09 score ratio |
|---|---|---:|---:|
| Conflict first | 0/6/3 | 0.99991631 | Not screened |
| Conflict last | 3/5/1 | 1.00009812 | 0.99962541 |
| Delayed conflict first | 3/3/3 | 1.00002450 | 1.00040213 |
| Flow-weighted conflict first | 3/5/1 | 1.00008739 | 0.99945067 |
| Rotate order | 2/4/3 | 1.00005398 | 0.99950112 |

Ratios are geometric means of candidate/control case scores (control/candidate delay), equally weighted across declared cases/seeds, not summed physical delay. These are small effects and limited-seed observations. No significance or universal superiority claim. Delayed ordering passed the first reserved screen and is undergoing a matched full9case/3seed hard evaluation. Transfer screen: designs1.00015691 (4wins/2losses), congested0.99999561 (2wins/3ties/1loss); only2cases per tier. No combined six-tier metric.

## Acceptance/basin family

Adapted existing fine-price repair to allow bounded legal temporary worsening, restoring its best legal checkpoint.40M devscreen: fine-uphill1win/4ties/4losses, fine-anneal2/3/4,warmer anneal1/4/4; ratios slightly below control. Each produced actual uphill moves. Retained for refinement.

Crossover50M on two additional development seeds: conflict-last4wins/2ties/0losses and flow-first2/3/1; ordering+anneal interactions mixed. No hybrid beats its pure ordering parent on the aggregate screen. Exact source patches retained in evolution-archive.json and dev/experiments/evolution-source-archive/.

Source diagnosis: uphill repair updates its checkpoint only when total delay strictly improves, then restores that checkpoint. Equal-best but changed geometry is consequently discarded at the end of a repair pass. New refinement retains equal-best geometry, compares against original anneal and control, and combines with delayed ordering.60M,three devcases,seeds16–18. This is a search hypothesis, not a correctness fix or claimed score gain.

## Exact arborescence family

Retained restricted exact tree repair; tightened its coupled per-sink delay bounds. Let B be the group's legal incumbent delay and L the sum of its independent sink shortest-path lower bounds in the restricted graph. Every sink's delay is at most its own lower bound plus slack B−L in any nonworsening solution. A useful tree vertex/arc must be able to reach at least one sink within that allowance. This prunes arcs and tightens distance-variable domains without excluding an improving tree; unused dangling branches can be removed. These are restricted-graph statements, not global optimality.

Five hand checks pass,including a competing two-layer multi-sink case with independent optimum9 and legal incumbent11. Matched30s/3deterministic-time strict screens on30groups: no gains; refined model proves4restricted groups cannot improve versus3for original. Most others unresolved. Non-strict hard04followup allows incumbent hints: eight groups,60s/15deterministic caps,7FEASIBLE plus1OPTIMAL for both; no gains, remaining restricted bound gaps recorded. Keep bounds refinement as a useful model reduction, not a score improvement.

## Branch family

Existing branch_repair.py already reroutes detached sinks from a retained root-labelled tree. New segment_surgery.py preserves the downstream component and replaces only a pin-free degree-two connector. Physical changes account for all downstream sinks. Root component labels remain actual driver distance; no zero-cost attachment shortcut. Three initial hand checks pass; added priced-proposal check confirms congestion prices do not leak into physical score.

Matched3M nine comparisons: allties; hundreds of actual segment plans/reconnections. Rather than stop, requester proposals now cycle mild ownership prices0/1/2/4, with the same mixture for original branch and segment reconstruction.6M followup underway. Exact unpriced source snapshot retained.

## Selection and provenance

Keep all checked variant families in the archive, including worse candidates. Full-tier legality and official scoring govern output selection. Positive narrow screens do not automatically change production defaults. Preserve immutable parent/source patches, compilation flags,work/timecaps,seeds,process resources,case/output hashes and complete results. Concurrent workers rule out isolated wall-speed claims. Native continuation separately adds search effort; final-route portfolio gains are not matched-budget algorithm gains.

## Full-tier checkpoint, October 3 20:10 UTC

All native ninth rounds (seeds26..30) completed;45 officially legal routes archived and restored with identical member hashes. Own added-effort scores: intro1.1144103126,hard1.2996823079,scale1.0645416543,congested1.1392614298,designs1.2887443624,stress1.0329842847. This continuation is separate from matched source-variant comparisons.

Delayed-order full-tier comparisons, independently rescored by the pinned official CLI for every variant/seed, show small mixed effects:

| Tier | Control mean | Delayed mean | Candidate/control geometric ratio |
| --- | ---: | ---: | ---: |
| Hard,3seeds | 1.29702569 | 1.29661530 | 0.99968357 |
| Scale,2seeds | 1.06349777 | 1.06357287 | 1.00007061 |
| Congested,2seeds | 1.13760403 | 1.13758251 | 0.99998108 |
| Designs,2seeds | 1.28626260 | 1.28667837 | 1.00032317 |
| Stress,2seeds | 1.03149430 | 1.03149430 | 1.00000000 |

Scores are each tier's official geometric mean,then arithmetic seed means only for descriptive summaries. Raw seed scores/spreads and official CLI process records are evolution-full-tier-scores.json. No combined score or statistical significance claim. Full hard result does not confirm its initial two-case validation gain. Retain delayed ordering as a candidate rather than make it an unconditional default.

**Stress mechanism limitation:** its50M control profile had zero repair proposals,attempts or negotiation rounds:the initial polish used the entire budget. Equality here does not evaluate negotiation-order efficacy. New repair-first scheduling comparison gives coordinated repair access to the same50M budget. This is a measured bottleneck in search allocation,not evidence that stress has no further headroom.

Neutral-best annealing refinement60M:1win/5ties/3losses,geometric ratio1.00004833 against control over three devcases/seeds16..18. Original strict-checkpoint annealing0.99968782 in the same screen;other hybrids mixed. Reserved08/09 followup launched. Small development observation only.

Priced segment surgery6M followup:all9comparisons tie,actualworkcaps reached. Preserve connector surgery and baseline source snapshots;no claimed quality gain. Exact repair still has unresolved restricted gaps rather than a global optimum certificate.

All25archived source entries reconstruct exactly. Best hard04rotate variant replay matches original executable and output SHA256,official delay13967. This verifies one same-machine fixed-work replay;it does not reconstruct every inherited parent or prove whole-pipeline reproducibility. Evidence evolution-source-replay.json.

OpenEvolve's primary repository documents archives,islands and diverse/exploratory parent sampling: https://github.com/algorithmicsuperintelligence/openevolve . These motivate retaining weaker stepping stones;our small checked source archive is not an execution of OpenEvolve or a full MAP-Elites implementation. No new AI training,paid API or competitor route input. Existing model in this coding session proposes code;official checks judge resulting routes.

Further running refinements:fixed-point precision64/256/1024 versus16;unused-resource price release/decay versus monotone history;repair-first budget scheduling;intro natural-completion comparison. Source variants compile separately. All physical acceptance remains official per-sink delay,not congestion tolls.

## Final comparison results from the sustained session

Intro full20case/two-seed ordering followup completed80legal runs,ratio1.00001258 (6wins/29ties/5losses). Same50Mceiling/1000pass limit;smallcases naturally end before the work cap. This is a common-ceiling comparison,not exact equal-work for every intro case. Failed strict intro attempt and invalid10000pass attempt retained,excluded from positive claims.

Neutral-best annealing full9hard/two-seed screen completed36runs:3wins/12ties/3losses,ratio0.99996356. Control mean1.29994372,annealmean1.29989636;oneannealseed achieves1.30004937. Full-tier mixed evidence prevents unconditional default adoption;useful routes still retained.

Finer congestion units64/256/1024 all yielded the same physical results in the60run precision screen;hardratio0.99964785 despite3wins/4ties/2losses. Designs/congested representative cases tied. All source variants remain archived;no claim higher precision is generally better.

History release60runs:hard dual_release1.00006323,cold_decay1.00008636,cycle_history0.99976646. Congested cycle positive1.00006791;othercongested/designsscreensnegative. These are representative-case samples,not complete-tier comparisons. New-parent crossover24runs:cold decay1.00001463,fineannealneutral1.00007699,hybrid1.00001463;nonew pure-parent replacement justified. No family discarded.

Repair-first scheduling24runs:scale representative ratio1.00007875,stress0.99985046;hard/designsnegative. Stress repair-first spent essentially all work on three coordinated attempts and little polish. Capped-repair refinement24runs:stress10percent0.99996306,25percent1.00000811;scale10percent0.99994504,25percent0.99986028. Four scale comparisons won under each slice but larger losses outweighed them in the geometric score. Five focused dual/slice checks pass and full123developmentchecks pass. These small mixed results motivate budget allocation refinement,not a universal scheduler change.

All original controls and weaker stepping stones are kept. Final source archive distinguishes method families,source identities and observations;best own whole-case selection and bounded two-parent tree fusion additionally test whether individually useful trees combine. Fusion is exact only between two frozen parents,not across the whole candidate pool or global routing space.
