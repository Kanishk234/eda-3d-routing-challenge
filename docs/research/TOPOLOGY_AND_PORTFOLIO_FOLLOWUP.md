# Topology and portfolio follow-up

## Sources inspected

- [Multi-Source Prim-Dijkstra author repository](https://github.com/TILOS-AI-Institute/Multi-Source-Prim-Dijkstra) and [ISQED2023 paper](https://vlsicad.ucsd.edu/Publications/Conferences/397/c397.pdf): read the source-selection and construction sections, not a reproduced implementation. Candidate starts use distributed/cluster-representative terminals; initialization connects chosen sources to the physical root. The reported objective combines wire cost and skew, which differs from our summed sink delay. Repository lists BSD3 license; no code copied or executed. Inference: clustered sink representatives could diversify congestion-priced topologies. Do not copy zero-distance source initialization into our driver-delay metric, or increase short paths merely to reduce skew.

- [BoxRouter author repository](https://github.com/UTDA-group/BoxRouter): inspected README/config descriptions; source-directory browser access failed. It documents progressive box/ILP variants, margin-limited maze search, topology input, checkpointing and congestion-cost escalation after stagnation. These suggest measured smaller-window and stagnation-triggered repair hypotheses. Our failed spatial screen does not disprove boundary-preserving branch repair. Old dependencies and objective differ; no installation/copy/execution or BoxRouter performance claim.

- [Held/Perner cost-distance paper, sectionsIII-A/D](https://arxiv.org/html/2503.04419v1): revisited component reuse and Steiner placement. Existing component connection cost may be discounted while physical driver distance remains charged. Separate component labels prevent cross-component misuse; branch placement balances root and downstream weighted paths. Our blunt fanout divisor is not this construction. Inference: downstream-aware component rebuilding is a stronger new-topology direction, but requires coherent predecessor/tree ownership checks. No theoretical guarantee transferred to current solver.

## Measured local changes

Hybrid diverse proposals plus adaptive dependency selection tested against each separate control on hard01/04/07,seeds1–3,5M expansions/1000cycles/60s,schedule2/1/1. All27 outputs legal. Hybrid versus diverse5wins/1tie/3losses,geomean1.000207; versus adaptive3wins/1tie/5losses,geomean0.999690. Keep optional; not a default or claimed improvement. The proposal overhead consumes the same expansion cap.

Two independently generated local pipelines have complementary complete-case strengths. Selecting a full route file for each case preserves legality; mixing individual nets need not. The explicit two-run hard portfolio scores1.2491377321487542, independently CLI verified9/9legal. This is additional portfolio resource usage, not superiority of one solver under matched budget. Original generation/ancestry records remain essential; missing incoming ancestors and reference generation are unknown costs. No participant outputs used as warm starts.

Next: transactional alternate-tree proposals from our own donor pipeline; component/branch topology work based on cost-distance ideas; smaller boundary-preserving spatial groups. Retain the strongest complete-case incumbents and run fixed additional stages from them, recording portfolio provenance.
