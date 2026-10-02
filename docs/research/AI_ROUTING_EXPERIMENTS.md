# CPU AI experiments

## Own learned fresh ordering

Implemented `dev/learned_fresh_order.py`: train a small pairwise priority model on our own fresh synthetic constructions, rather than incumbent route geometry. Twenty-four training layouts; nine had a legal sampled teacher construction. Twenty-four distinct held-out layouts, one construction per method. Learned completed11/24; random12/24. Learned beat random7/tied2/lost2 on eleven jointly legal cases. This is a toy experiment, not an official-tier improvement or proof of generalization. Evidence: learned-fresh-order.json and learned-fresh-model.json. Not adopted.

## Pretrained REST on CPU

Original licensed source and published five-terminal weights: https://github.com/cuhk-eda/REST. The source targets2D rectilinear wirelength, not our3D sum of driver-to-sink delays. Original CU-SD license retained alongside downloaded files. No competitor route inputs. Inference uses CPU-only PyTorch2.8.0+cpu, one thread. Pinned Git tree and exact blob/content hashes in rest-model-manifest.json; model/source cache ignored by Git.

`dev/rest_proposals.py` converts actor topology into XY corridors used as secondary shortest-path preferences. Primary costs retain physical delay plus explicit ownership penalties. Coherent predecessor trees, foreign-pin protection, finite candidate-set CP-SAT selection, and official checks preserve legal incumbents. Terminal counts2–5 and both XY orientations are experimental transfers from the five-terminal model. Restricted optimal selection is not global optimality.

Hard01/04/07:104/130/150 model calls;593769/1129021/1789513 expansions; approximately5.21/9.81/16.48 seconds per case. All three selections restricted OPTIMAL; no delay gains. No work limit triggered. Evidence: hard-rest-proposals.json. This corridor adaptation is not adopted as a quality improvement.

First load failed because the legacy checkpoint stores a NumPy scalar metric. Restricted weights-only loading succeeds after explicitly allowing NumPy scalar/dtype/float64 classes; unrestricted pickle loading was not used. Failed first attempt remains in ignored artifacts.

Reproduce (project venv; optional dependencies):

```sh
.venv/bin/python -m pip install -r dev/requirements-ai.txt
.venv/bin/python dev/fetch_rest_model.py --out dev/artifacts/pretrained-rest-reproduction
.venv/bin/python dev/rest_proposals.py dev/configs/hard-rest-proposals.json --model-root dev/artifacts/pretrained-rest-reproduction --out dev/artifacts/rest-reproduction
```

Probe requires the selected own native run folders restored/present under dev/artifacts. Archive-restoration alone does not place them there automatically. Model inference is separate from solver regeneration; final freeze is pending.

## Next experiment

Learn global construction decisions with broader feasible synthetic training data, explicitly reward whole-case legality and physical delay, and compare against randomized fresh construction under matched work budgets. Explore congestion-dependent ordering and neighborhood selection rather than only tie preferences. These are proposals, not completed implementations. An external general AI model has not been called for route generation; no paid endpoint or GPU hardware is assumed.
