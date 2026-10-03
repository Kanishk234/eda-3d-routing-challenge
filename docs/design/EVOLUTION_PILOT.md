# Existing LLM algorithm-evolution pilot

## Objective

Maximize each official tier's score independently. For case i, score_i = baseline_delay_i / candidate_delay_i. Tier score = exp(mean(log(score_i))) across all cases in that tier. An illegal/incomplete tier has no ranked positive result under the pinned evaluator.

Compare variant versus control with exp(mean(log(control_delay_i / variant_delay_i))). This equals the variant/control tier-score ratio when case coverage/weighting are identical. A pilot uses three hard development cases and three seeds each, equally weighted; its ratio is a development signal, not an official full-tier score. Keep per-seed and per-case wins/ties/losses. Do not substitute total delay across cases for tier score or invent an aggregate across six tiers. All routes must be legal.

## Existing AI role

The existing coding model in this session proposes source changes. No custom model training, new pretrained weights, child agent launch or paid endpoint is required for this pilot. This is an independent adaptation inspired by [GR-Evolve](https://github.com/ASU-VDA-Lab/GR-Evolve), not running its OpenROAD stack or reproducing its published performance. The AI's output is a source variant; compiled routing and official checking measure the result.

## Bounded first generation

- Parent: exact_polish.cpp snapshot from current workspace; source hash and dirty identity retained.
- Three variants: byte-identical recompiled control; most-conflicted local repair nets first; least-conflicted local repair nets first.
- Change only negotiation order. Keep physical costs, capacity semantics, legal acceptance and rollback.
- Hard01/04/07; seeds1/2/3; same parent per attempt,10M expansions,60s safety,one worker. Require every run to reach identical expansion ceiling; reject budget-capped mismatches.
- Preserve source,binary,build commands,case/parent/output hashes,official delays,core counters,CPU/RSS and process metadata.
- No canonical promotion. Even a winning development variant requires held-out hard08/09 comparisons and broader tier checks before adoption. Runtime comparisons require isolated runs; native continuation runs concurrently.

Runner: dev/evolution_pilot.py. Plan: dev/configs/evolution-pilot.json. Artifacts: dev/artifacts/20261003-evolution-pilot. Log: /tmp/evolution-pilot.log.

The first two proposals are hypotheses, not established improvements. If they lose/tie, record that outcome and propose a different algorithmic change from the measured failure; do not call more iterations an improvement by themselves.
