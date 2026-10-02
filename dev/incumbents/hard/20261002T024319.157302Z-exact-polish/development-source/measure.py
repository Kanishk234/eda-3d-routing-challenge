"""Bounded serial measurement of untouched official tools; use project .venv."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
REVISION = "499ad7e2a415a97e9ce9b3396b0477e75ebd13e6"
OFFICIAL = ROOT / "dev/upstream" / REVISION

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode().strip()

def save(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n")
    os.replace(temporary, path)

def source_identity():
    tracked = git("ls-files", "--cached", "--others", "--exclude-standard").splitlines()
    extra = ["AGENTS.md"] + [str(p.relative_to(ROOT)) for p in (ROOT / "dev").glob("*.*")]
    files = {p: digest(ROOT / p) for p in sorted(set(tracked + extra))
             if (ROOT / p).is_file()}
    return {"revision": git("rev-parse", "HEAD"), "status": git("status", "--porcelain=v1"),
            "diff_sha256": hashlib.sha256(subprocess.check_output(
                ["git", "diff", "HEAD", "--binary"], cwd=ROOT)).hexdigest(),
            "file_hashes": files,
            "files_sha256": hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()}

def execute(command, out, label, budget):
    log = out / (label + ".log")
    usage = out / (label + ".resources.txt")
    measured = ["/usr/bin/time", "-f", "%e %U %S %M", "-o", str(usage), *command]
    start = time.perf_counter()
    timed_out = interrupted = False
    with log.open("w") as stream:
        process = subprocess.Popen(measured, cwd=OFFICIAL, stdout=stream,
                                   stderr=subprocess.STDOUT, start_new_session=True,
                                   env={**os.environ, "PYTHONHASHSEED": "0", "OMP_NUM_THREADS": "1"})
        try:
            process.wait(timeout=budget)
        except (subprocess.TimeoutExpired, KeyboardInterrupt) as exc:
            timed_out = isinstance(exc, subprocess.TimeoutExpired)
            interrupted = not timed_out
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
    result = {"command": command, "cwd": str(OFFICIAL), "budget_s": budget,
              "wall_s": time.perf_counter() - start, "exit_code": process.returncode,
              "timeout": timed_out, "interrupted": interrupted,
              "log": str(log.relative_to(ROOT)), "peak_rss_kib": None,
              "user_cpu_s": None, "system_cpu_s": None}
    if usage.exists() and usage.read_text().strip():
        fields = usage.read_text().splitlines()[-1].split()
        if len(fields) == 4:
            try:
                result.update(user_cpu_s=float(fields[1]), system_cpu_s=float(fields[2]),
                              peak_rss_kib=int(fields[3]))
            except ValueError:
                pass
    print(f"{label}: exit={process.returncode}, wall={result['wall_s']:.3f}s, "
          f"RSS={result['peak_rss_kib']} KiB", flush=True)
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["tests", "smoke", "suite", "ci"])
    parser.add_argument("--suite", default="benchmarks")
    parser.add_argument("--case", default="case_01")
    parser.add_argument("--budget", type=float, default=60, help="seconds per subprocess")
    parser.add_argument("--router", default="baseline",
                        choices=["baseline", "negotiated", "negotiated_fast", "negotiated2"])
    args = parser.parse_args()
    if not 0 < args.budget <= 1800:
        parser.error("budget must be positive and at most 1800 seconds")
    if Path(sys.prefix).resolve() != (ROOT / ".venv").resolve():
        parser.error("use .venv/bin/python")
    if not OFFICIAL.is_dir():
        parser.error("run bash dev/setup.sh first")
    suites = {"benchmarks", "benchmarks_hard", "benchmarks_scale", "benchmarks_stress",
              "benchmarks_congested", "benchmarks_designs"}
    if args.suite not in suites or Path(args.case).name != args.case:
        parser.error("use an official suite and an unqualified case name")
    if args.mode == "smoke" and args.router != "baseline":
        parser.error("smoke currently supports the official baseline only")
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    out = ROOT / "dev/artifacts" / (stamp + "-" + args.mode)
    out.mkdir(parents=True)
    manifest = {"run_id": out.name, "started_utc": stamp, "upstream_revision": REVISION,
                "source": source_identity(), "config": vars(args),
                "machine": {"hostname": platform.node(), "os": platform.platform(),
                            "python": sys.version, "cpu_count": os.cpu_count(),
                            "affinity_cpus": len(os.sched_getaffinity(0)),
                            "meminfo": Path("/proc/meminfo").read_text()},
                "seed": None, "seed_note": "official routers deterministic; input stores case seed",
                "workers": 1, "threads": 1, "compiler_flags": None, "warm_start": None,
                "portfolio_runs": 1, "steps": [], "outputs": {}}
    official_files = [p for p in OFFICIAL.rglob("*") if p.is_file()
                      and "__pycache__" not in p.parts and p.suffix != ".pyc"]
    manifest["official_hashes"] = {str(p.relative_to(OFFICIAL)): digest(p)
                                  for p in sorted(official_files)}
    manpath = out / "manifest.json"
    save(manpath, manifest)
    python = str(ROOT / ".venv/bin/python")
    def run(label, *command):
        result = execute(list(command), out, label, args.budget)
        manifest["steps"].append(result)
        save(manpath, manifest)
        return result["exit_code"] == 0

    success = True
    if args.mode == "tests":
        success = run("tests", python, "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-v")
    elif args.mode == "ci":
        success = run("verify-submissions", python, "scripts/verify_submissions.py")
        success = run("leaderboard-check", python, "-m", "m3d.cli", "leaderboard-all", "--check") and success
    elif args.mode == "smoke":
        suite = OFFICIAL / args.suite
        case = suite / (args.case + ".json")
        entry = next(c for c in json.loads((suite / "suite.json").read_text())["cases"]
                     if c["name"] == args.case)
        manifest["input"] = {"case": str(case.relative_to(OFFICIAL)), "sha256": digest(case),
                             "case_seed": entry.get("seed"), "baseline_delay": entry["baseline_total"]}
        candidate = out / "candidate.sol.json"
        success = run("baseline", python, "-m", "m3d.cli", "baseline", "--case", str(case),
                      "--out", str(candidate), "--order", "bbox_desc", "--rip-limit", "40",
                      "--ops-factor", "200")
        evaluation = out / "evaluation.json"
        if success:
            success = run("evaluate", python, "-m", "m3d.cli", "evaluate", "--case", str(case),
                          "--sol", str(candidate), "--suite", str(suite), "--out", str(evaluation))
        if success:
            result = json.loads(evaluation.read_text())
            success = result["legal"] and result["total_delay"] > 0
            manifest["result"] = {"legal": result["legal"], "total_delay": result["total_delay"],
                                  "baseline_delay": entry["baseline_total"],
                                  "ratio": entry["baseline_total"] / result["total_delay"]}
            if success:
                accepted = out / (args.case + ".sol.json")
                os.replace(candidate, accepted)
                manifest["outputs"] = {accepted.name: digest(accepted), evaluation.name: digest(evaluation)}
    else:
        routes = out / "routes"
        success = run("run-suite", python, "-m", "m3d.cli", "run-suite", "--suite", args.suite,
                      "--router", args.router, "--out-dir", str(routes))
        score = out / "score.json"
        score_args = ["--suite", args.suite, "--submission-dir", str(routes), "--out", str(score)]
        if (routes / "runtime.json").exists():
            score_args += ["--runtimes", str(routes / "runtime.json")]
        success = run("score-suite", python, "-m", "m3d.cli", "score-suite", *score_args) and success
        if score.exists():
            manifest["result"] = json.loads(score.read_text())
        if routes.exists():
            manifest["outputs"] = {str(p.relative_to(out)): digest(p) for p in sorted(routes.glob("*.json"))}
    changed = [p for p, h in manifest["official_hashes"].items() if digest(OFFICIAL / p) != h]
    manifest["official_inputs_unchanged"] = not changed
    manifest["changed_official_files"] = changed
    manifest["success"] = success and not changed
    manifest["total_subprocess_wall_s"] = sum(s["wall_s"] for s in manifest["steps"])
    save(manpath, manifest)
    print(f"manifest: {manpath}")
    return 0 if manifest["success"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
