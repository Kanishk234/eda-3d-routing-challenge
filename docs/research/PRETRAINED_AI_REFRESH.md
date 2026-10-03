# Existing AI routing tools: October 3 refresh

User preference: reuse existing AI and published models before considering custom training. No new training pipeline is authorized by this research direction; earlier own toy models remain experimental, not production defaults.

## Candidates and evidence

| Tool | What is available | Fit and action |
|---|---|---|
| [REST](https://github.com/cuhk-eda/REST) | Original licensed source and published weights for several terminal counts; CPU actor inference works locally. README documents eight symmetry transformations. | 2D wirelength objective. Tested eight symmetry proposals from the five-terminal model; hard01/04/07 zero gains. Downloaded original ten-terminal model to cover more fanouts; completed three-case screen with zero gains. No retraining. |
| [OAREST](https://github.com/Thinklab-SJTU/EDA-AI/tree/main/OAREST) | Obstacle-aware actor implementation and inference config. | Potentially closer geometric proposals; still wirelength. Config references logs/.../last.ckpt. No OAREST checkpoint found in complete current tree or repository releases. Availability elsewhere remains unknown. |
| [HubRouter](https://github.com/Thinklab-SJTU/EDA-AI/tree/main/HubRouter) | Hub generation and connection code, dataset preprocessing/training/inference instructions. | No ready hub-generation weights located in inspected tree; README's checkpoint directory listing does not prove weights are shipped. Needs image/capacity-to-3D-vertex adaptation. |
| [DSBRouter](https://github.com/Thinklab-SJTU/EDA-AI/tree/main/DSBRouter) | Diffusion routing code; inference expects explicit checkpoint. Published REST weights are bundled under util/REST_tool/pretrained. | Bundled REST weights are not a trained diffusion model. No diffusion checkpoint located in inspected tree/releases. Training instructions use eight processes; no training or GPU installation launched. |
| [GR-Evolve](https://github.com/ASU-VDA-Lab/GR-Evolve) | Published framework and [paper](https://arxiv.org/html/2604.22234v1) describing existing LLMs proposing router source variants with evaluation feedback. | Promising workflow: evolve algorithms using true physical-delay feedback. Published results target post-detailed-routing wirelength and OpenROAD, not this challenge. No claimed transfer gain, no external paid model invocation or Docker launch. |

Current EDA-AI revision fd9d3a3df1cf53b6828528bab8925d35abdfa7c8, complete/nontruncated recursive tree; release API returned empty. Exact relevant blob inventory in pretrained-routing-source-inventory.json. Absence findings cover this tree/releases, not every link, branch or private artifact.

## Actual experiments

- Eight-transform REST5: source/hashes/config, CPU one-thread inference, 15M expansions/90s per case, three hard development cases. Official whole-case legality and restricted candidate-selection checks; zero gain. Evidence hard-rest-eight.json.
- REST10: published 28,683,630-byte rsmt10b.pt, Git blob b6407ae2cb9e35bcd4ccfd8cd92ffde36a95ee5d verified from bytes; SHA256 manifest rest10-model-manifest.json. Original license retained. REST10 made496/624/752 neural calls on hard01/04/07,2,961,627/5,712,336/10,057,638 expansions,162.464s summed per-case wall time under concurrent runs. All three outputs officially legal, restricted selections OPTIMAL, zero gains; no work limit triggered. Evidence hard-rest10-eight.json. Degree2–10 transfer is experimental. Actor proposals guide equal-cost geometry; primary physical delay/pricing remain independent. This tests a limited adaptation, not the full potential of pretrained routing.
- Independent component reuse/representative relocation screen: eight selected multi-sink nets/case, two vertex-price settings, three methods, equal 2M/30s ceilings each. Individually legal alternatives, restricted CP selection, three officially legal cases, zero gain. This screen does not establish the paper's full algorithm or approximation guarantee. Evidence hard-component-reuse.json.

## Next decisions

Prioritize pretrained obstacle-aware proposal generation if a licensed checkpoint becomes available. For a general LLM, use measured algorithm evolution: generate a small number of isolated implementation changes, evaluate matched fixed-work development runs, retain only legally checked improvements, then validate reserved cases. No need to train a new model for this loop. Complete and review the broader-fanout REST result first.

## Framework source inspection

Read GR-Evolve's actual GeneticRunCodex.sh (Git blob591ba2a3fdb0cc84acf55cff74128fcc1bd71658), not only its abstract. It invokes an existing agent wrapper in75 serial iterations with logs and a process lock. The loop itself is a restart driver; candidate selection resides in agent context/evaluation, not an independent learned router. No script copied or executed. Our adaptation should keep immutable parent variants, matched fixed-work results, official legality and true physical delay; a general pretrained coding model proposes changes, and existing experiment wrappers evaluate them. The source loop's set-e behavior exits on a failed command before later handling, so do not import it unchanged.
