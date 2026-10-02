# Polish ordering and current all-tier status

Area-normalized excess delay prioritizes whole-net exact searches. Relative excess is an alternative; default remains seeded random. Ordering changes allocation of finite work, not shortest-path costs or physical acceptance. Cached scalar priorities ensure a strict stable comparator. Engine and wrapper record configuration and completed/improving searches.

36 focused checks pass; warning-free C++17 build. Matched stress/scale01 screen: three seeds, three orders,3M expansions each,18 officially legal trials,225.483s wrapper total. Area ordering wins3/3 stress seeds,geometric delay ratio1.0002354; relative wins3/3 with1.0001153. Both lose2/3 scale seeds, so retain scale random. Area ordering completes332 stress searches versus15–39 controls. This is work allocation evidence, not a measured CPU speedup. Bounding-box area remains a proxy, not a calibrated predictor.

Fixed seed1 stress3M area pilot followed by20M continuation yields delay1120960,score1.0213602626320297. Continuation costs32.684s wrapper,12.177s core and20M expansions. This adds effort and is not a matched-budget whole-tier comparison. Stress has only one case and no held-out validation.

Independent pinned CLI validates all45 selected routes: intro1.0974025183797085,hard1.2564870553234753,scale1.0471187071837642,congested1.0984083343517812,designs1.2297437228340384,stress1.0213602626320297. Other five outputs unchanged. Evidence: polish-order-screen.json and tier-polish-order-followup-coverage.json. Canonical selection and compact stress archive preserve original bytes/source/manifest; prior archives retained. Older missing ancestors and reference-generation costs remain unreproduced. No freeze, global-best, unseen-generalization or end-to-end regeneration claim.

Next: measure actual per-net search effort to refine scheduling; compare targeted partial-branch repairs against retained whole-net controls before full-tier adoption. Final freeze and submission remain pending.
