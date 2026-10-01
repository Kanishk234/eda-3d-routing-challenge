# Architecture

Setup, measurement, official verification and C++ exact single-net polish are implemented. See PHASE2 summary.

Immutable evaluation boundary: exact Git archive dev/upstream/499ad7e2a415a97e9ce9b3396b0477e75ebd13e6. All 198 archived files verified against pinned Git blobs; wrapper hashes inputs before/after. Development in dev/, future engine in dev/solver/, bulk outputs under ignored dev/artifacts/. Never edit scorer/benchmarks to improve results.

Implemented C++17 engine: packed ID=(z*height+y)*width+x, implicit six neighbors, int64_t physical totals and safe infinity/overflow checks. Keep physical delay, congestion penalties and priorities separate. Driver-rooted coherent predecessor tree supplies terminal paths; remove irrelevant nonterminal leaves. Ownership counts a vertex once per net; foreign pins always reserved.

Current interface: immutable parsed instance + explicit seed/config/budget + optional attributed verified incumbent → candidate trees, statistics and termination status. Net/group replacement must release ownership and support complete rollback. Conflicting negotiation states stay internal. The current polisher leaves the old route untouched until a complete improving candidate is ready; rejected searches preserve ownership. Group repair remains unimplemented.

Output follows model.py/FORMATS.md: version-1 m3d-submission, matching instance, one route per net, integer adjacent-vertex edges. Official independent reloading/checking/scoring is required before acceptance.

Implemented wrapper: unique run directories; smoke candidate written then officially evaluated, accepted output atomically renamed. Previous runs survive timeout. Suite outputs stay isolated and are not automatically promoted. run_polish.py supports --resume-dir and preserves a validated pre-search checkpoint; completed candidates are officially checked before replacement.
