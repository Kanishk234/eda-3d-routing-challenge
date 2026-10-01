"""Matched coordinated-rerouting screen on three declared tier representatives."""
import json
import subprocess
import sys
from measure import ROOT, digest, save


def main():
    coverage = json.loads((ROOT / "docs/evidence/phase3/tier-coverage.json").read_text())
    starts = {r["tier"]: ROOT / "dev/artifacts" / r["run_id"] / "routes" for r in coverage["rows"]}
    representatives = {"scale": "case_01", "congested": "case_01", "designs": "ctrl"}
    rows = []
    for mode in ("fanout", "fanout_walk"):
        for tier, case in representatives.items():
            before = set((ROOT / "dev/artifacts").glob("*-exact-polish/manifest.json"))
            subprocess.run([sys.executable, str(ROOT / "dev/run_polish.py"),
                            "--suite", "benchmarks_" + tier, "--case", case,
                            "--mode", mode, "--budget", "5", "--passes", "100",
                            "--seed", "1", "--resume-dir", str(starts[tier])], check=True)
            created = set((ROOT / "dev/artifacts").glob("*-exact-polish/manifest.json")) - before
            assert len(created) == 1
            path = created.pop()
            m = json.loads(path.read_text())
            assert m["success"] and m["official_inputs_unchanged"]
            rows.append({"tier": tier, "mode": mode, "run_id": m["run_id"],
                         "manifest_sha256": digest(path), "source_identity": m["source"]["files_sha256"],
                         "warm_start": m["warm_start"], "case": m["cases"][0],
                         "wrapper_wall_s": m["wrapper_wall_s"]})
    save(ROOT / "docs/evidence/phase3/coordinated-tier-screen.json",
         {"scope": {"representatives": representatives, "seed": 1, "budget_s": 5, "passes": 100},
          "rows": rows, "workers": 1, "portfolio_selection": False,
          "note": "Single-seed development comparison on declared representatives; no full-tier score or generalization claim."})


if __name__ == "__main__":
    main()
