# Downstream pricing and continued optimization

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
