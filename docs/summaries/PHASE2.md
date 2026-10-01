# Phase 2 — complete

Built an original C++17 exact single-net tree polisher with a versioned Python bridge to the pinned official model/checker/scorer. The reliable pipeline starts from freshly reproduced official negotiated baseline routes. It does not construct routes independently from scratch or use another entrant's outputs.

All nine hard cases are officially legal and improved: aggregate1.0466292119096317 vs baseline1.0. Identical seed1/pass5 repeats produce identical output hashes, including a fresh build this session. Independent official CLI rescore agrees. Compact comparison, per-case results, hashes and run manifests are in docs/evidence/phase2/. Selected run20261001T212816.474321Z-exact-polish.

Thirteen kernel tests pass, including hand-calculated nonuniform costs/shared trunks,30 random comparisons against independent Dijkstra, foreign pins/via endpoints, disconnected/cyclic/conflicting routes, wide integers, unchanged ownership after rejected replacement, truncated output and signal/zero-budget recovery. Wrapper validates before search, persists an initial legal checkpoint, compares total/per-net delay with the official checker, reloads serialized output and promotes atomically. Explicit resume succeeds. Abrupt child failure retains the pre-search checkpoint; it may lose improvements since that checkpoint.

Paired comparison uses one worker on the same WSL machine and a common600s routing envelope. Baseline generation94.765s; current polishing core1.243s and wrapper3.186s; summed pipeline97.952s. Both methods terminate naturally within the envelope; baseline does not consume spare budget. Baseline generation was reused, so the sum is not a freshly timed end-to-end execution. No speedup claim. Earlier core timings0.56–0.64s vary; wall measurement includes polling overhead. All cases improve; runtime increases by wrapper cost. Public PR3 score1.387366 is better, with unmatched/unreproduced solver runtime.

Limits: fixed-other-net shortest paths are exact single-net results, not global optimum. Five passes need not reach a full fixed point. One seed/config, no portfolio selection or validation-case tuning. Generated reserved seeds remain ungenerated; final freeze/submission reproducibility is Phase4. Raw artifacts need separate backup. No official toolkit/input changes, commits or publication.

Next Phase3: controlled comparison of driver-aware construction, congestion negotiation and coordinated legal repair. Preserve the accepted legal routes and reserve hard08–09 for validation.
