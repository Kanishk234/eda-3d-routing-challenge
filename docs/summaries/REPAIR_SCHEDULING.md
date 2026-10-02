# Repair scheduling experiment

Optional repair-first order moves the existing group sweep before single-net polish. Default unchanged; same A*,prices,work caps,groups and rollback.35focused checks pass,including default/explicit0identity,invalid2rejection,work-limit rollback/repetition.

Repeated seeds1–3 on stress and scale01;current caps13/3 and swapped caps3/13;18official-legal outputs,exact3M expansions,1000cycles,60s safety cap. Repair-first loses overall against current order on both tiers and both caps. No setting passes the declared selection rule;retain experimental only. Stress proposals rise from0to1–13,so repair is reached,but this does not establish better physical routes.

Strongest stress output is controlseed3:delay1121764,54less than prior1121818,score1.0206282248316045. It is retained as explicit selection from9stress candidates,not a method improvement. Independent full coverage confirms45/45legal;otherfive tier outputs unchanged. Screenwrappercost219.389s includes all9stress+9scale runs;inherited generation and independent scoring separate. Stress has no separate held-out case. Archive/canonical selection updated;route restoration checks preserved.

Next:prioritize potential gain per estimated search cost before the sweep;compare with relative-excess and random order. This may complete more useful single-net searches before budget exhaustion. Proxy is a hypothesis;no claimed search-speed/model accuracy. Partial branch repair and per-search interruption require further correctness work.

Fixed original-order scale seed3/group3/3M followup from unchanged eight-case incumbent improves8/8,score1.0471187071837642;addedwrapper18.152s. Independent coverage tier-schedule-seed-followup-coverage.json confirms45/45legal with both updatedtiers;otherfourunchanged. This retains seeddiversity,notrepair-first. Both new scale/stressarchives and canonicalselection preserved.
