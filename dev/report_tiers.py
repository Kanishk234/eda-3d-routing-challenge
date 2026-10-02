"""Officially rescore explicitly selected complete runs; no best-of selection."""
import argparse
import json
import sys
from pathlib import Path
from measure import ROOT, OFFICIAL, REVISION, digest, execute, save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", nargs="+", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    rows = []
    for directory in args.runs:
        directory = directory.resolve()
        manifest_path = directory / "manifest.json"
        m = json.loads(manifest_path.read_text())
        assert m["success"] and m["result"]["complete"]
        assert m["official_inputs_unchanged"]
        for name, checksum in m["outputs"].items():
            assert digest(directory / name) == checksum
        suite = m["config"]["suite"]
        step = execute([sys.executable, "-m", "m3d.cli", "score-suite",
                        "--suite", suite, "--submission-dir", str(directory / "routes"),
                        "--out", str(directory / "coverage-rescore.json")],
                       directory, "coverage-rescore", 180)
        assert step["exit_code"] == 0
        score = json.loads((directory / "coverage-rescore.json").read_text())
        assert score["complete"]
        assert score["aggregate_score"] == m["result"]["aggregate_score"]
        warm = Path(m["warm_start"]["directory"])
        official_reference = warm == OFFICIAL / suite / "reference"
        chain = []
        ancestor = m
        while True:
            chain.append({"run_id": ancestor["run_id"],
                          "mode": ancestor["config"].get("mode", "polish"),
                          "wrapper_wall_s": ancestor["wrapper_wall_s"]})
            origin = Path(ancestor["warm_start"]["directory"])
            parent = origin.parent / "manifest.json"
            if not parent.exists():
                break
            ancestor = json.loads(parent.read_text())
        portfolio_path = origin.parent / "portfolio.json"
        inherited_portfolio = json.loads(portfolio_path.read_text()) if portfolio_path.exists() else None
        ancestry_available = origin.exists()
        reference_ancestor = (origin == OFFICIAL / suite / "reference") if ancestry_available else None
        if inherited_portfolio: reference_ancestor = None
        rows.append({"tier": "intro" if suite == "benchmarks" else suite.removeprefix("benchmarks_"),
                     "run_id": m["run_id"], "manifest_sha256": digest(manifest_path),
                     "source_identity": m["source"]["files_sha256"],
                     "config": m["config"], "score": score,
                     "warm_start": m["warm_start"],
                     "official_reference_warm_start": official_reference,
                     "official_reference_ancestor": reference_ancestor,
                     "initial_route_artifact_available": ancestry_available,
                     "inherited_case_portfolio": inherited_portfolio,
                     "known_total_optimizer_wall_s": sum(x["wrapper_wall_s"] for x in chain) + (inherited_portfolio["known_ancestry_wrapper_wall_s"] if inherited_portfolio else 0),
                     "attribution": "Official challenge reference routes followed by local optimization" if reference_ancestor else ("Locally validated pipeline; see ancestor manifests" if ancestry_available else "Inherited archive; older artifacts unavailable, consult original coverage evidence"),
                     "optimizer_chain": list(reversed(chain)),
                     "recorded_optimizer_chain_wall_s": sum(x["wrapper_wall_s"] for x in chain),
                     "initial_route_source": str(origin),
                     "wrapper_wall_s": m["wrapper_wall_s"],
                     "core_wall_s": m["total_core_wall_s"],
                     "peak_core_rss_kib": max(c["process"].get("peak_rss_kib") or 0 for c in m["cases"]),
                     "cases": [{**c,"core":{k:v for k,v in c.get("core",{}).items() if k!="net_delays"}} for c in m["cases"]], "outputs": m["outputs"], "official_rescore": step})
        print(rows[-1]["tier"], score["aggregate_score"], flush=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    save(args.out, {"upstream_revision": REVISION, "rows": rows,
                    "portfolio_selection": any(r["inherited_case_portfolio"] is not None for r in rows),
                    "limitations": "Separate tier scores, no cross-tier aggregate. Reference warm starts are attributed and their generation cost was not reproduced. Stage timings exclude inherited generation, experiments and rescorers. No final freeze or end-to-end regeneration claim."})


if __name__ == "__main__":
    main()
