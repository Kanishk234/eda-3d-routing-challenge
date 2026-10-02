"""Relax all ownership/pin obstacles to bound delay, not construct legal routes."""
import argparse
import json
import math
import sys
from pathlib import Path
from measure import ROOT, OFFICIAL, REVISION, digest, save


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coverage",type=Path,default=ROOT/"docs/evidence/phase3/tier-optimized-coverage.json")
    parser.add_argument("--out",type=Path,default=ROOT/"docs/evidence/phase3/delay-bounds.json")
    args=parser.parse_args()
    coverage = json.loads(args.coverage.read_text())
    tiers = []
    for row in coverage["rows"]:
        suite = row["config"]["suite"]
        manifest = json.loads((OFFICIAL / suite / "suite.json").read_text())
        current = {c["case"]: c["total_delay"] for c in row["cases"]}
        cases = []
        for c in manifest["cases"]:
            path = OFFICIAL / suite / c["instance_file"]
            inst = json.loads(path.read_text())
            pins = {p["id"]: p for p in inst["pins"]}
            delay = inst["delay"]
            bound = 0
            for net in inst["nets"]:
                driver = pins[net["driver"]]
                for sink_id in net["sinks"]:
                    sink = pins[sink_id]
                    xy = abs(driver["x"] - sink["x"]) + abs(driver["y"] - sink["y"])
                    bound += min(xy * cost + delay["via_delay"] *
                                 (abs(driver["z"] - z) + abs(sink["z"] - z))
                                 for z, cost in enumerate(delay["layer_delay"]))
            assert 0 < bound <= current[c["name"]]
            cases.append({"case": c["name"], "case_sha256": digest(path),
                          "baseline_delay": c["baseline_total"], "current_delay": current[c["name"]],
                          "relaxed_delay_lower_bound": bound,
                          "optimistic_score_ceiling": c["baseline_total"] / bound,
                          "current_over_bound": current[c["name"]] / bound})
        ceiling = math.exp(sum(math.log(c["optimistic_score_ceiling"]) for c in cases) / len(cases))
        tiers.append({"tier": row["tier"], "current_score": row["score"]["aggregate_score"],
                      "optimistic_score_ceiling": ceiling, "cases": cases})
        print(row["tier"], "current", row["score"]["aggregate_score"], "ceiling", ceiling)
    save(args.out,
         {"upstream_revision": REVISION, "coverage_sha256":digest(args.coverage), "tiers": tiers,
          "formula": "min_k ManhattanXY*layer_delay[k] + via_delay*(abs(driver_z-k)+abs(sink_z-k))",
          "proof": "Any path visits a cheapest layer k, uses at least ManhattanXY horizontal steps and at least abs(driver_z-k)+abs(sink_z-k) vias. Moving horizontally on k attains that bound when obstacles are removed.",
          "limitations": "Foreign pins and competing nets are ignored. Pairwise optimum sums are lower bounds only; their score ceilings need not be jointly achievable. No global optimum or legal construction claim."})


if __name__ == "__main__":
    main()
