# Adapting released AI models to our routing problem

October 3 follow-up. User requests investigating adaptations rather than requiring an exact problem match. Initial source inventory: `docs/evidence/phase3/ai-adaptation-source-audit.json`. That inventory preceded downloads and experiments; the completed implementation results are below.

## First experiment: pretrained local 3D proposals

[HRM Chip Router](https://huggingface.co/salvadordabrown/hrm-chip-router-7m) publishes a checkpoint and [source](https://github.com/Brown-Forces-Technology-Studio-Inc/hrm-chip-router). The complete GitHub tree and Hugging Face file list were retrieved directly. Pinned GitHub revision f5e213cb9e405e5728e0414b5d4f7f6d8d3d9a70; model revision 86ac3c59cc0c560e541f380f27a6974a99c89fff. Apache-2.0 is stated by the model card; preserve and inspect the repository license before incorporating source.

Published input is a 16x4x16 grid with four net colors. The public imitation checkpoint reports 3.53% full-puzzle connectivity, roughly 25% per-net connectivity; these are author measurements, not our reproduction. Advertised stronger production results refer to another model. Token accuracy does not measure legal delay quality.

Adaptation hypothesis: take a small window with at most four selected nets; encode fixed external wires and foreign pins as obstacles, and branch boundary terminals as colored endpoints. Keep the real 3D geometry: do not rescale larger windows or collapse layers. Windows exceeding four layers require a separately justified boundary treatment; padded layers must be blocked. Preserve all fixed outside edges and their driver-distance labels.

Use output probabilities as proposal preferences, followed by classical connectivity repair and tree construction. They must not override ownership or become physical delay. A window can contain more boundary terminals than the training distribution: record this transfer explicitly. Test color permutations and XY reflections; do not permute physical layers with different delay values. Reject every proposal whose full-case official check fails or whose physical delay worsens. Preserve useful alternatives for our existing exact candidate selection/fusion.

The inspected evaluator hard-codes CUDA in model construction, checkpoint loading and batch movement. CPU adaptation needs a device parameter throughout, dataset-independent metadata/batch construction, and checking attention/dtype behavior (config uses bfloat16). CPU feasibility and latency remain unmeasured. Download/hash the actual checkpoint before claiming verified weights. First compare a pretrained-guided repair with the same classical repair without guidance, including inference cost, on hard01/04/07; reserve08/09 for subsequent validation. No training initially.

## Second experiment: AI selects destruction, classical engine repairs

[Neural Destruction Search](https://github.com/ahottung/NDS) provides MIT-licensed source and twelve checkpoint paths in its complete pinned tree ca374200f70f1954ec82348d6c4e92ad4aff3168. This is stronger availability evidence than a README promise, but bytes have not been downloaded or loaded. Its learned policy chooses removals and a classical reconstruction evaluates them.

Our proposed transfer is to rank nets/branches for coordinated removal, leaving routing and legality to our engine. The actual encoder takes XY, vehicle demand, current tour neighbors and tour index; our trees and driver-to-sink objective are different. Mapping a net center to a customer, resource footprint to demand, and proximity ordering to a tour is a speculative zero-shot baseline, not a faithful equivalence. Include random, spatial and dual-price selectors under the same total budget. If the frozen weights fail, retain the family and improve feature/structure adaptation before considering limited fine-tuning of an existing architecture. No new training launched.

[NLNS](https://github.com/ahottung/NLNS) also ships pretrained repair models and documents CPU evaluation. It is GPL-3.0 and vehicle-routing-specific. Inspect license implications before copying implementation; its repair architecture is a lead, not a drop-in chip router.

## Third experiment: matrix-conditioned proposals

[Real-routing NCO](https://github.com/ai4co/real-routing-nco) supplies checkpoint download tooling and asymmetric-TSP support. Pairwise free-graph delay/detour matrices could guide a sink visitation order or representative selection. A tour is not a routing tree; materialize it through our driver-distance-aware tree builder and score the final legal tree. This avoids pretending Euclidean wirelength training already represents our delay costs. Checkpoint bytes and CPU inference remain unverified in this audit.

## Decision

Prioritize the HRM local-window CPU feasibility probe because its published representation already includes competing nets and layers. Keep neural destruction as a separate promising control proposal. Missing direct compatibility is an adaptation task; none of these sources yet establishes an improvement on our official tiers. Continue existing native and source-evolution work alongside these probes.

## Completed CPU adaptations

Both released checkpoints have now been downloaded and hashed. Apache-2.0 HRM source and MIT NDS source/licenses are retained under ignored artifacts; their immutable inventories are hrm-model-manifest.json and nds-model-manifest.json. Neither model was trained or fine-tuned. Restricted PyTorch loaders remain enabled; NDS's known configuration/NumPy serialization types are explicitly allowlisted.

HRM loads strictly with 27,271,170 physical parameters and completes all16steps on CPU bfloat16, two threads. Synthetic inference takes24.619s; this is not its GPU claim or a routing-quality result. Three real hard-case screens then complete:

| Adaptation | Scope | Result |
|---|---|---|
| Whole-net windows, secondary geometry ties | Two windows/case,hard01/04/07 | Six legal control/model outputs;zero delay gain;141.274s summed inference |
| Gap-prioritized windows,small neural search toll | Same three cases,two windows/case | Six legal outputs;zero delay gain;144.897s inference |
| Partial branches,connected outside trees retained | Two branch windows/case;control/tie/priced | Nine legal outputs;zero delay gain;200.209s inference |

Partial-branch root attachment and outside geometry are fixed. Predicted color masks feed classical coherent predecessor trees; official full-case delay and restricted candidate-pool selection decide acceptance. GPU is unnecessary for these probes. Timings are concurrent-run observations,not isolated speed comparisons. The bounded screens do not exhaust this model's potential. Historical adapter source snapshots are preserved in dev/experiments/hrm-adaptation-source-archive.

NDS runs strictly on CPU with one thread,using the explicit proxy above. It proposes62/78/94 focal neighborhoods in0.208/0.226/0.309s on hard01/04/07. Its groups contain the focal net plus three distinct selections from12nearby candidates;group indices and actual parent hashes are recorded. A C++ experiment compares these frozen groups with same-size nearest-center groups and the native solver across two seeds,50M routing expansions/run. Eighteen legal outputs complete: neural1win/1tie/4losses versus native,paired geometric ratio0.99953362;spatial3wins/3losses,ratio0.99962945. This is matched routing work,not matched total effort including model preparation.

Own-tree recombination preserves a two-unit hard04 gain from the spatial-control donor. No neural donor contributes an accepted improvement in that fusion. Do not attribute this gain to AI. All families and source variants remain archived rather than discarded after weak first results.

## Reproduction and next refinement

Use the optional pinned dev/requirements-ai.txt in the project venv;the core CPU solver still needs no neural packages. Model files are downloaded through dev/fetch_hrm.py and dev/fetch_nds.py. Run:

```bash
.venv/bin/python dev/fetch_hrm.py
.venv/bin/python dev/fetch_nds.py
.venv/bin/python dev/hrm_cpu_probe.py --out /tmp/hrm-cpu-probe.json
.venv/bin/python dev/hrm_branch_proposals.py --coverage docs/evidence/phase3/tier-neural-group-fusion-coverage.json --out /tmp/hrm-branch-probe
.venv/bin/python dev/nds_net_groups.py --coverage docs/evidence/phase3/tier-neural-group-fusion-coverage.json --out /tmp/nds-groups.json
```

Output targets must be new. To replay the recorded NDS experiment,use its recorded prior coverage and groups file;new canonical parents require regenerated groups and updated plan paths. Retained mutation sources and exact configuration hashes are separate from final routes.

Next prioritize refining NDS's problem representation: real blocker/dual-price relationships instead of nearest-center proxy graph edges,and separately compare footprint versus critical-delay features. Its cheap inference makes these experiments practical. HRM should next use calibrated probability preferences and measured color/reflection diversity in selected branch windows;its inference cost argues for cached proposals and few targeted windows. These are next hypotheses,not performed results. Existing-model fine-tuning remains a later option if the frozen transfers cannot learn the necessary distinction;no new training pipeline was launched.
