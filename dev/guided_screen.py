"""Declared serial repeat-seed, budget, and fresh-start development screens."""
import argparse
import json
import subprocess
import sys
from measure import ROOT, digest, save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("screen", choices=["repeat", "budget", "fresh", "treecost", "cycles"])
    args = parser.parse_args()
    coverage = ROOT / "docs/evidence/phase3" / ("tier-followup-coverage.json" if args.screen == "cycles" else "tier-guided-coverage.json")
    entries = json.loads(coverage.read_text())
    starts = {r["tier"]: ROOT / "dev/artifacts" / r["run_id"] / "routes" for r in entries["rows"]}
    representatives = {"hard": "case_01", "congested": "case_01", "designs": "ctrl"}
    configs = {
        "repeat": [(mode, seed, 5, 100) for mode in ("fanout", "fanout_astar", "fanout_astar_gap") for seed in (2, 3)],
        "budget": [("fanout_astar", 1, budget, 100) for budget in (5, 20)],
        "fresh": [("restart_astar", 1, 20, 5)],
        "treecost": [("treecost", 1, 5, 100)],
        "cycles": [("fanout_astar", 1, 20, passes) for passes in (100, 1000)],
    }[args.screen]
    rows = []
    destination = ROOT / "docs/evidence/phase3" / ("guided-" + args.screen + "-screen.json")
    if args.screen == "cycles": representatives = {"hard": ["case_01", "case_04", "case_07"]}
    report = {"screen": args.screen, "scope": {"representatives": representatives, "configs": configs},
              "warm_start_coverage_sha256": digest(coverage), "workers": 1,
              "portfolio_selection": False, "rows": rows,
              "limitations": "Development representatives only; no reserved hard08/09 tuning, no per-case selection, no full-tier score. Wall-time caps can change completed prefixes."}
    for mode, seed, budget, passes in configs:
        for tier, case in ([("hard", "case_01"), ("hard", "case_04"), ("hard", "case_07")] if args.screen == "cycles" else representatives.items()):
            before = set((ROOT / "dev/artifacts").glob("*-exact-polish/manifest.json"))
            subprocess.run([sys.executable, str(ROOT / "dev/run_polish.py"),
                            "--suite", "benchmarks_" + tier, "--case", case, "--mode", mode,
                            "--budget", str(budget), "--passes", str(passes),
                            "--seed", str(seed), "--resume-dir", str(starts[tier])], check=True)
            paths = set((ROOT / "dev/artifacts").glob("*-exact-polish/manifest.json")) - before
            assert len(paths) == 1
            path = paths.pop()
            m = json.loads(path.read_text())
            assert m["success"] and m["official_inputs_unchanged"]
            rows.append({"tier": tier, "mode": mode, "seed": seed, "budget_s": budget,
                         "passes": passes, "run_id": m["run_id"],
                         "manifest_sha256": digest(path), "source_identity": m["source"]["files_sha256"],
                         "case": m["cases"][0], "wrapper_wall_s": m["wrapper_wall_s"]})
            save(destination, report)
    report["complete"] = True
    report["total_wrapper_wall_s"] = sum(r["wrapper_wall_s"] for r in rows)
    save(destination, report)


if __name__ == "__main__":
    main()
