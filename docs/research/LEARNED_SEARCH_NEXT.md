# Learned search hypothesis

User asks whether an AI could route this challenge. Plausible first experiment: a small CPU model chooses target net, repair operator and neighborhood size; existing routing engine constructs geometry and official checker gates incumbents. Learned net ordering and neighborhood selection have primary research precedent,not evidence of improvement on our challenge.

Sources inspected:
- Sonnerat et al.,Learning a Large Neighborhood Search Algorithm for Mixed Integer Programs,abstract: https://arxiv.org/abs/2107.10201 . Learns neighborhood choice and delegates optimization; objective/domain different.
- Zhou et al.,Transformer-based Reinforcement Learning for Net Ordering in Detailed Routing,2025,primary PDF: https://www.ijcai.org/proceedings/2025/1055.pdf . Uses net relationships/ordering for detailed-routing costs and violations; not our driver-to-sink score.
- Liao et al.,A Deep Reinforcement Learning Approach for Global Routing,abstract: https://arxiv.org/abs/1906.08809 . Not a benchmark or guarantee for this repository.

Plan after current frozen experiments:
1. Instrument own move attempts with target features: fanout,physical excess,bbox,cross-layer terminals,blocker count,local occupancy,operator,group cap and recent outcomes. Current aggregate logs alone are not a sufficiently rich training dataset.
2. Reward actual officially accepted physical delay reduction per measured work; account for deferred effects of neutral moves separately.
3. Start with a CPU contextual bandit or small regression/ranking model and random/handwritten controls. No GPU dependency or large neural training pipeline yet.
4. Hold out cases/layouts/seeds;45 released cases are limited diversity. Separate tuning from reported evaluation; generate/validate additional feasible training cases where appropriate.
5. Compare final delay under identical total expansion and safety budgets,including model inference overhead; disclose offline training/data generation cost separately.

Neither a model nor training is implemented in this checkpoint. No learned-method score benefit claimed. Competitor routes remain excluded; own move traces and official inputs permitted. Direct LLM edge-by-edge output is not the preferred experiment for exact legal large-grid routing; code/research assistance remains separate from learned routing policy.

## Basin escape and pretrained systems

User correctly points out a local training-data trap. A learned selector trained only on incumbent-local successful moves can perpetuate current packing. Broad exploration requires multiple fresh constructions,diverse schedules/layouts and seeds,large reconstruction actions,unsuccessful examples and rewards for eventual outcomes. A policy cannot reach a topology its action set never proposes. Separate global construction from local search and compare both against own incumbents.

Existing systems are worth assessing before bespoke training. Public EDA-AI contains learned routing implementations PRNet,HubRouter andDSBRouter; root README verified,but no compatible pretrained endpoint/checkpoint for this challenge verified yet. HubRouter README specifies ISPD07 input and NCTU-derived training targets plus separate hub and pin-connection training; a checkpoint directory listing is not proof of downloadable usable weights. AlphaChip's official project focuses on floorplanning,so pretrained availability there does not supply our routing action/objective. General hosted language models can propose algorithm/global-topology experiments with tool feedback; existing broad training does not certify valid route geometry or improved weighted multi-sink delay.

Sources: https://github.com/Thinklab-SJTU/EDA-AI ; https://raw.githubusercontent.com/Thinklab-SJTU/EDA-AI/main/HubRouter/README.md ; https://github.com/google-research/circuit_training/blob/main/README.md . DSBRouter/README.md direct fetch returned404;directory/source/checkpoint compatibility audit remains next work,not completed.
