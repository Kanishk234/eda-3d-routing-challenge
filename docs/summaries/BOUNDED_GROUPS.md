# Bounded complete-net repairs

Pilot:scale/congested case01,designs ctrl,seeds1–3,caps3/7/13,3M expansions/1000cycles/60s. Every trial legal. Cap3 beats13 in all9 comparisons; cap7 has regressions on scale/congested and insufficient wins on designs. Select3 for these three tiers by the declared rule; retain13 elsewhere. Wide negotiation keeps24 rounds regardless of cap. No partial-branch repair implemented.

|Tier|Selected score|
|---|---:|
|intro|1.097402518|
|hard|1.256487055|
|scale|1.045720179|
|congested|1.098408334|
|designs|1.229743723|
|stress|1.020579096|

All45selected outputs officially legal;five tiers improve,stress unchanged. Additional wrapper costs:pilot57.584s;full stages97.754s. Inherited portfolio/generation and scoring separate.34focused checks pass; default13 output identity and invalid-limit rejection checked; observed transaction histograms stay within each cap. Pilot has one development case per tier, so no generalization or universal default claim.

Stress:16searches exhaust3M work with0repair proposals across a901-net instance. Source order polishes the entire net list before proposing groups. Next candidate is repair-first/interleaved scheduling, measured against unchanged order at fixed work; reducing group size alone cannot help when repair is never reached. All six selected outputs archived;restore verifies45original route hashes. Missing earlier incoming generation remains a limitation.
