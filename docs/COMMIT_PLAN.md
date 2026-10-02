# Reviewed commit groups

The user explicitly authorized the agent to create these four local commits in the latest conversation, overriding the default AGENTS.md restriction for this action. The user handles pushing. Run from the repository root. The following commands define the approved local commit groups. Inspect any already staged files first; these commands do not clear the index.

Includes own solver prototypes/tests, compact experiment evidence, verified incumbent archives, and documentation. Excludes the supplied root PDF, ignored model weights/source, build products, venv, and scratch logs. Existing native solver code is unchanged. 88 development checks passed; 45 canonical routes officially legal and archive hashes verified; final submission freeze pending. Native seeds14/15 completed both rounds; their newer outputs have not replaced the canonical selection in these commits.

## solver: add CPU routing experiments

28 files.

```sh
git add -- \
  dev/adaptive_price_pool.py \
  dev/branch_diagnostic.py \
  dev/branch_repair.py \
  dev/component_router.py \
  dev/ejection_chain.py \
  dev/exact_pair_repair.py \
  dev/exact_tree_repair.py \
  dev/fetch_rest_model.py \
  dev/fresh_construction_screen.py \
  dev/generate_tree_candidates.py \
  dev/learned_fresh_order.py \
  dev/report_tiers.py \
  dev/requirements-ai.txt \
  dev/requirements-exact.txt \
  dev/rest_proposals.py \
  dev/select_tree_pool.py \
  dev/static_cbs.py \
  dev/test_adaptive_price_pool.py \
  dev/test_branch_repair.py \
  dev/test_candidate_trees.py \
  dev/test_component_router.py \
  dev/test_ejection_chain.py \
  dev/test_exact_pair.py \
  dev/test_exact_tree.py \
  dev/test_learned_fresh_order.py \
  dev/test_rest_proposals.py \
  dev/test_static_cbs.py \
  dev/test_tree_pool.py
git diff --cached --stat
git diff --cached --check
git commit -m 'solver: add CPU routing experiments'
```

## experiments: record independent routing trials

94 files.

```sh
git add -- \
  dev/configs/congested-tree-pool.json \
  dev/configs/designs-tree-pool.json \
  dev/configs/exact-pool-checkpoints.json \
  dev/configs/fresh-component-followup.json \
  dev/configs/hard-adaptive-price-pool.json \
  dev/configs/hard-attachment-candidates.json \
  dev/configs/hard-attachment-tree-pool.json \
  dev/configs/hard-cbs-broad-avoid.json \
  dev/configs/hard-cbs-broad-control.json \
  dev/configs/hard-cbs-bypass.json \
  dev/configs/hard-chain-neutral.json \
  dev/configs/hard-chain-strict.json \
  dev/configs/hard-ejection-chain.json \
  dev/configs/hard-exact-groups-pruned.json \
  dev/configs/hard-exact-groups.json \
  dev/configs/hard-exact-pairs.json \
  dev/configs/hard-exact-trees-strict.json \
  dev/configs/hard-exact-trees.json \
  dev/configs/hard-expanded-tree-pool.json \
  dev/configs/hard-lp-price-pool.json \
  dev/configs/hard-priced-candidates.json \
  dev/configs/hard-rest-proposals.json \
  dev/configs/hard-static-cbs-followup.json \
  dev/configs/hard-static-cbs.json \
  dev/configs/hard-tree-pool.json \
  dev/configs/independent-continuation-fourth.json \
  dev/configs/independent-continuation-next.json \
  dev/configs/independent-continuation-third.json \
  dev/configs/independent-continuation.json \
  dev/experiments/source-snapshots/20261002-hard-adaptive-price-pool/adaptive_price_pool.py \
  dev/experiments/source-snapshots/20261002-hard-cbs-broad-avoid/exact_pair_repair.py \
  dev/experiments/source-snapshots/20261002-hard-cbs-broad-avoid/static_cbs.py \
  dev/experiments/source-snapshots/20261002-hard-cbs-broad-control/exact_pair_repair.py \
  dev/experiments/source-snapshots/20261002-hard-cbs-broad-control/static_cbs.py \
  dev/experiments/source-snapshots/20261002-hard-cbs-bypass/exact_pair_repair.py \
  dev/experiments/source-snapshots/20261002-hard-cbs-bypass/static_cbs.py \
  dev/experiments/source-snapshots/20261002-hard-ejection-chain/ejection_chain.py \
  dev/experiments/source-snapshots/20261002-hard-exact-groups-pruned/exact_pair_repair.py \
  dev/experiments/source-snapshots/20261002-hard-exact-groups/exact_pair_repair.py \
  dev/experiments/source-snapshots/20261002-hard-exact-pairs/exact_pair_repair.py \
  dev/experiments/source-snapshots/20261002-hard-exact-trees-strict/exact_pair_repair.py \
  dev/experiments/source-snapshots/20261002-hard-exact-trees-strict/exact_tree_repair.py \
  dev/experiments/source-snapshots/20261002-hard-exact-trees/exact_pair_repair.py \
  dev/experiments/source-snapshots/20261002-hard-exact-trees/exact_tree_repair.py \
  dev/experiments/source-snapshots/20261002-hard-lp-price-pool/adaptive_price_pool.py \
  dev/experiments/source-snapshots/20261002-priced-candidates/generate_tree_candidates.py \
  dev/experiments/source-snapshots/20261002-priced-candidates/select_tree_pool.py \
  docs/evidence/phase3/branch-repair-screen.json \
  docs/evidence/phase3/component-construction-screen.json \
  docs/evidence/phase3/congested-exact-tree-pool.json \
  docs/evidence/phase3/cpu-prototype-environment.json \
  docs/evidence/phase3/designs-exact-tree-pool.json \
  docs/evidence/phase3/exact-pool-checkpoints.json \
  docs/evidence/phase3/exact-pool-restoration.json \
  docs/evidence/phase3/fresh-component-followup.json \
  docs/evidence/phase3/hard-adaptive-price-pool.json \
  docs/evidence/phase3/hard-attachment-tree-pool.json \
  docs/evidence/phase3/hard-branch-edge-diagnostic.json \
  docs/evidence/phase3/hard-cbs-broad-avoid.json \
  docs/evidence/phase3/hard-cbs-broad-control.json \
  docs/evidence/phase3/hard-cbs-bypass.json \
  docs/evidence/phase3/hard-chain-neutral.json \
  docs/evidence/phase3/hard-chain-strict.json \
  docs/evidence/phase3/hard-ejection-chain.json \
  docs/evidence/phase3/hard-exact-groups-pruned.json \
  docs/evidence/phase3/hard-exact-groups.json \
  docs/evidence/phase3/hard-exact-pair-discovery.json \
  docs/evidence/phase3/hard-exact-tree-pool.json \
  docs/evidence/phase3/hard-exact-trees-strict.json \
  docs/evidence/phase3/hard-exact-trees.json \
  docs/evidence/phase3/hard-expanded-tree-pool.json \
  docs/evidence/phase3/hard-lp-price-pool.json \
  docs/evidence/phase3/hard-rest-proposals.json \
  docs/evidence/phase3/hard-static-cbs-followup.json \
  docs/evidence/phase3/hard-static-cbs.json \
  docs/evidence/phase3/independent-continuation.json \
  docs/evidence/phase3/independent-next-restoration.json \
  docs/evidence/phase3/independent-next.json \
  docs/evidence/phase3/independent-restoration.json \
  docs/evidence/phase3/independent-third-restoration.json \
  docs/evidence/phase3/independent-third.json \
  docs/evidence/phase3/learned-fresh-model.json \
  docs/evidence/phase3/learned-fresh-order.json \
  docs/evidence/phase3/prototype-source-snapshots.json \
  docs/evidence/phase3/public-source-audit.json \
  docs/evidence/phase3/rest-model-manifest.json \
  docs/evidence/phase3/three-round-continuation.json \
  docs/evidence/phase3/three-round-restoration.json \
  docs/evidence/phase3/tier-exact-pool-coverage.json \
  docs/evidence/phase3/tier-independent-continuation-coverage.json \
  docs/evidence/phase3/tier-independent-next-coverage.json \
  docs/evidence/phase3/tier-independent-third-coverage.json \
  docs/evidence/phase3/tier-three-round-continuation-coverage.json \
  docs/evidence/phase3/torch-cpu-install.json
git diff --cached --stat
git diff --cached --check
git commit -m 'experiments: record independent routing trials'
```

## results: preserve verified tier incumbents

53 files.

```sh
git add -- \
  dev/incumbents/congested/20261002T185248.178956Z-exact-polish.tar.gz \
  dev/incumbents/congested/20261002T185248.178956Z-exact-polish.tar.gz.json \
  dev/incumbents/congested/20261002T191540.158533Z-exact-polish.tar.gz \
  dev/incumbents/congested/20261002T191540.158533Z-exact-polish.tar.gz.json \
  dev/incumbents/congested/20261002T201415.549181Z-exact-polish.tar.gz \
  dev/incumbents/congested/20261002T201415.549181Z-exact-polish.tar.gz.json \
  dev/incumbents/congested/20261002T212424.874084Z-exact-polish.tar.gz \
  dev/incumbents/congested/20261002T212424.874084Z-exact-polish.tar.gz.json \
  dev/incumbents/congested/20261002T222650.280317Z-exact-polish.tar.gz \
  dev/incumbents/congested/20261002T222650.280317Z-exact-polish.tar.gz.json \
  dev/incumbents/designs/20261002T185252.774030Z-exact-polish.tar.gz \
  dev/incumbents/designs/20261002T185252.774030Z-exact-polish.tar.gz.json \
  dev/incumbents/designs/20261002T201428.044861Z-exact-polish.tar.gz \
  dev/incumbents/designs/20261002T201428.044861Z-exact-polish.tar.gz.json \
  dev/incumbents/designs/20261002T212431.902414Z-exact-polish.tar.gz \
  dev/incumbents/designs/20261002T212431.902414Z-exact-polish.tar.gz.json \
  dev/incumbents/designs/20261002T222707.707138Z-exact-polish.tar.gz \
  dev/incumbents/designs/20261002T222707.707138Z-exact-polish.tar.gz.json \
  dev/incumbents/hard/20261002T185038.204620Z-exact-polish.tar.gz \
  dev/incumbents/hard/20261002T185038.204620Z-exact-polish.tar.gz.json \
  dev/incumbents/hard/20261002T191538.264265Z-exact-polish.tar.gz \
  dev/incumbents/hard/20261002T191538.264265Z-exact-polish.tar.gz.json \
  dev/incumbents/hard/20261002T201028.781037Z-exact-polish.tar.gz \
  dev/incumbents/hard/20261002T201028.781037Z-exact-polish.tar.gz.json \
  dev/incumbents/hard/20261002T212215.870187Z-exact-polish.tar.gz \
  dev/incumbents/hard/20261002T212215.870187Z-exact-polish.tar.gz.json \
  dev/incumbents/hard/20261002T222232.599549Z-exact-polish.tar.gz \
  dev/incumbents/hard/20261002T222232.599549Z-exact-polish.tar.gz.json \
  dev/incumbents/intro/20261002T185038.207918Z-exact-polish.tar.gz \
  dev/incumbents/intro/20261002T185038.207918Z-exact-polish.tar.gz.json \
  dev/incumbents/intro/20261002T201028.775038Z-exact-polish.tar.gz \
  dev/incumbents/intro/20261002T201028.775038Z-exact-polish.tar.gz.json \
  dev/incumbents/intro/20261002T212215.853546Z-exact-polish.tar.gz \
  dev/incumbents/intro/20261002T212215.853546Z-exact-polish.tar.gz.json \
  dev/incumbents/intro/20261002T222232.588647Z-exact-polish.tar.gz \
  dev/incumbents/intro/20261002T222232.588647Z-exact-polish.tar.gz.json \
  dev/incumbents/scale/20261002T185148.098596Z-exact-polish.tar.gz \
  dev/incumbents/scale/20261002T185148.098596Z-exact-polish.tar.gz.json \
  dev/incumbents/scale/20261002T201231.674547Z-exact-polish.tar.gz \
  dev/incumbents/scale/20261002T201231.674547Z-exact-polish.tar.gz.json \
  dev/incumbents/scale/20261002T212325.649656Z-exact-polish.tar.gz \
  dev/incumbents/scale/20261002T212325.649656Z-exact-polish.tar.gz.json \
  dev/incumbents/scale/20261002T222455.757361Z-exact-polish.tar.gz \
  dev/incumbents/scale/20261002T222455.757361Z-exact-polish.tar.gz.json \
  dev/incumbents/selected.json \
  dev/incumbents/stress/20261002T185317.392730Z-exact-polish.tar.gz \
  dev/incumbents/stress/20261002T185317.392730Z-exact-polish.tar.gz.json \
  dev/incumbents/stress/20261002T201509.054661Z-exact-polish.tar.gz \
  dev/incumbents/stress/20261002T201509.054661Z-exact-polish.tar.gz.json \
  dev/incumbents/stress/20261002T212455.155885Z-exact-polish.tar.gz \
  dev/incumbents/stress/20261002T212455.155885Z-exact-polish.tar.gz.json \
  dev/incumbents/stress/20261002T222753.207504Z-exact-polish.tar.gz \
  dev/incumbents/stress/20261002T222753.207504Z-exact-polish.tar.gz.json
git diff --cached --stat
git diff --cached --check
git commit -m 'results: preserve verified tier incumbents'
```

## docs: record routing research and status

14 files.

```sh
git add -- \
  dev/README.md \
  docs/BUGS.md \
  docs/CLAIMS.md \
  docs/COMMIT_PLAN.md \
  docs/DECISIONS.md \
  docs/WORKLOG.md \
  docs/design/OVERVIEW.md \
  docs/design/phases/PHASE3.md \
  docs/research/AI_ROUTING_EXPERIMENTS.md \
  docs/research/BRANCH_REPAIR_NEXT.md \
  docs/research/CPU_EXPLORATION.md \
  docs/research/LEARNED_SEARCH_NEXT.md \
  docs/research/PUBLIC_SOURCE_REVIEW.md \
  docs/summaries/CPU_EXPLORATION.md
git diff --cached --stat
git diff --cached --check
git commit -m 'docs: record routing research and status'
```

These are development commits, not a route-only upstream submission diff. Review the full staged diff before each commit. Publication remains the user’s responsibility.
