# All-tier score improvement

Objective: maximize each of the six official tier scores. Public PR scores are comparisons, not targets.

| Tier | Previous | Current | Improved / cases |
|---|---:|---:|---:|
| intro | 1.050409 | 1.093572 | 20/20 |
| hard | 1.230658 | 1.231296 | 4/9 |
| scale | 1.029924 | 1.040409 | 8/8 |
| congested | 1.090605 | 1.094145 | 4/4 |
| designs | 1.212499 | 1.223681 | 3/3 |
| stress | 1.020434 | 1.020548 | 1/1 |

All45selected outputs independently official-checked; no delay regressions. Fine-price/tight-search stage on four tiers, then a second seed/larger work stage on all six. Added wrapper effort319.189s, excluding previous ancestry and independent rescoring. Attributed official reference ancestry remains in coverage reports; these are incremental improvements, not fresh-generation runtimes.

Evidence:all-tier-advance-comparison.json,tier-all-advance-coverage.json,all-tier-current-bounds.json. Full manifests and routes are ignored artifacts and must be preserved. Current relaxed bounds leave room to investigate all tiers but are not legal constructions or global optimum claims.

Next: integrate concurrent neighborhood work and measure it from these incumbents; then select tier-specific geometry, congestion and throughput experiments. Freeze/regeneration/submission remain pending.
