# All-tier score objective

The user's objective is to maximize each tier's official geometric score. There is no cross-tier aggregate to optimize and no target defined by current PRs. Public routes provide diagnosis/comparisons only. Keep legality, ancestry and all search effort explicit.

## Current allocation

Run a bounded first fine-price/tight-lookahead stage on intro, scale, designs and stress, which have not received it. Then apply a fixed second seed and larger work allowance to every tier. Per-stage work caps5M/10M expansions per case,1000cycles,60s safety cap; these are local compute choices, not competition limits. Cases execute serially to keep measurements interpretable. Hard uses2/1/1 schedule, congested2/4/4, other tiers retain2/2/2 pending broader evidence. These are incumbent stages, not fresh solvers.

All candidates are officially checked and physical delay cannot increase. Select complete stage outputs, not undisclosed case/seed portfolios. Reports preserve every unchanged case. Reserve hard08/09 from configuration selection; their fixed-config validation remains allowed.

## Subsequent work by evidence

| Tier | Next diagnostic and candidate |
|---|---|
| intro | Shortest-path packing and equal-delay tree geometry; determine which nets remain above their independent free-grid bounds |
| hard | Multi-sink topology/branch sharing and coordinated blocker/window neighborhoods; expand schedule robustness beyond one representative |
| scale | Search throughput versus completed local repairs; try tight search and ownership/scratch changes only when profiles justify them |
| congested | Nonlinear marginal resource prices, adaptive neighborhoods and additional diversified walks |
| designs | Multi-sink topology and delay-aware sharing; controlled comparison of schedules and restart basins |
| stress | Locality and throughput on huge grids; distinguish single-net polish from successful coordinated repairs |

Use independent seeds/configurations as a recorded portfolio when beneficial, with total generation/search costs disclosed. Eventually compare additional methods against the actual remaining physical-delay gap, not a static public score. Relaxed bounds are not legal constructions. A plateau under one operator is a reason to change approach, not to call the maximum achieved.

Final freeze/regeneration/submission preparation remains a separate gate. This ongoing optimization report does not claim the globally highest possible score.

Repeat a bounded stage sequence from explicit current incumbents without overwriting evidence:

```bash
.venv/bin/python dev/advance_all_tiers.py --coverage docs/evidence/phase3/tier-all-advance-coverage.json --label all-tier-next
```

Each sequence records source/config, per-case results and full-tier official rescoring. Current source/report identities may differ from prior snapshots; regenerate comparisons explicitly rather than assuming a changed binary is the same experiment.
