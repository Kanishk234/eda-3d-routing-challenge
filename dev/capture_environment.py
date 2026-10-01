"""Capture bounded upstream/environment/inventory evidence with stdlib only."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import urllib.request
from measure import ROOT, OFFICIAL, REVISION, digest, save

def main():
    out = ROOT / "docs/evidence/phase0"
    out.mkdir(parents=True, exist_ok=True)
    report = {"checked_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
              "upstream_revision": REVISION, "api": {}}
    for name, endpoint in [
        ("repository", ""), ("head", "/commits/HEAD"),
        ("pulls", "/pulls?state=all&per_page=100"),
        ("actions", "/actions/runs?per_page=10")]:
        url = "https://api.github.com/repos/partcleda/eda-3d-routing-challenge" + endpoint
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "m3d-phase0-audit"})
            with urllib.request.urlopen(request, timeout=20) as response:
                data = json.load(response)
                report["api"][name] = {"url": url, "status": response.status,
                                       "date_header": response.headers.get("Date"),
                                       "pagination": response.headers.get("Link")}
            if name == "head":
                report["api"][name]["sha"] = data["sha"]
            elif name == "repository":
                report["api"][name].update(default_branch=data["default_branch"],
                                           license=data.get("license"))
            elif name == "pulls":
                report["api"][name]["entries"] = [
                    {"number": p["number"], "title": p["title"], "state": p["state"],
                     "head": p["head"]["sha"], "updated_at": p["updated_at"],
                     "merged_at": p.get("merged_at"), "url": p["html_url"]}
                    for p in data]
            else:
                report["api"][name]["entries"] = [
                    {key: r.get(key) for key in ("id", "name", "head_sha", "event", "status",
                                                "conclusion", "created_at", "html_url")}
                    for r in data["workflow_runs"]]
                report["api"][name]["total_count"] = data["total_count"]
        except Exception as exc:
            report["api"][name] = {"url": url, "error": str(exc)}
    save(out / "upstream.json", report)
    commands = {
        "cwd": ["pwd"], "git_status": ["git", "status", "--short"],
        "git_head": ["git", "rev-parse", "HEAD"],
        "upstream_head": ["git", "ls-remote", "https://github.com/partcleda/eda-3d-routing-challenge.git", "HEAD"],
        "fork_diff": ["git", "diff", REVISION, "HEAD", "--stat"],
        "os": ["uname", "-a"], "cpu": ["lscpu"], "memory": ["free", "-b"],
        "nproc": ["nproc"], "compiler": ["g++", "--version"], "make": ["make", "--version"],
        "python": [sys.executable, "--version"], "pip": [sys.executable, "-m", "pip", "--version"],
        "packages": [sys.executable, "-m", "pip", "freeze"], "disk": ["df", "-B1", "."],
    }
    environment = {}
    for name, cmd in commands.items():
        result = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=30)
        environment[name] = {"command": cmd, "exit_code": result.returncode, "output": result.stdout}
    for name in ["/etc/os-release", "/sys/fs/cgroup/cpu.max", "/sys/fs/cgroup/memory.max",
                 "/proc/self/status"]:
        p = Path(name)
        environment[name] = p.read_text() if p.exists() else "unavailable"
    save(out / "environment.json", environment)
    inventory = {"revision": REVISION, "tiers": {}, "total_cases": 0}
    for tier, folder in [("intro", "benchmarks"), ("hard", "benchmarks_hard"),
                         ("scale", "benchmarks_scale"), ("stress", "benchmarks_stress"),
                         ("congested", "benchmarks_congested"), ("designs", "benchmarks_designs")]:
        suite = OFFICIAL / folder
        manifest = json.loads((suite / "suite.json").read_text())
        entries = []
        for case in manifest["cases"]:
            path = suite / case["instance_file"]
            data = json.loads(path.read_text())
            reference = suite / case["reference_file"]
            entries.append({"name": case["name"], "grid": data["grid"],
                            "n_vertices": data["grid"]["width"] * data["grid"]["height"] * data["grid"]["layers"],
                            "n_nets": len(data["nets"]), "n_pins": len(data["pins"]),
                            "seed": data["seed"], "delay": data["delay"],
                            "baseline_delay": case["baseline_total"],
                            "case_sha256": digest(path), "reference_sha256": digest(reference),
                            "instance_file": case["instance_file"], "reference_file": case["reference_file"]})
        inventory["tiers"][tier] = {"directory": folder, "n_cases": len(entries),
                                    "suite_sha256": digest(suite / "suite.json"), "cases": entries}
        inventory["total_cases"] += len(entries)
    save(out / "inventory.json", inventory)
    print(json.dumps({"total_cases": inventory["total_cases"],
                      "tiers": {k: {"cases": v["n_cases"],
                                     "vertices_min": min(c["n_vertices"] for c in v["cases"]),
                                     "vertices_max": max(c["n_vertices"] for c in v["cases"]),
                                     "nets_min": min(c["n_nets"] for c in v["cases"]),
                                     "nets_max": max(c["n_nets"] for c in v["cases"])}
                                for k, v in inventory["tiers"].items()},
                      "api": report}, indent=2))


if __name__ == "__main__":
    main()
