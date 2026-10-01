"""Phase 1: bounded public-output audit and stage profiles of immutable upstream."""
import argparse
import cProfile
from dataclasses import asdict
import datetime as dt
import json
import os
from pathlib import Path
import platform
import pstats
import shutil
import sys
import time
import urllib.request
from measure import ROOT, OFFICIAL, REVISION, digest, execute, save, source_identity

def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "m3d-phase1-reproduction"})
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)

def new_run(mode, config):
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    out = ROOT / "dev/artifacts" / (stamp + "-" + mode)
    out.mkdir(parents=True)
    m = {"run_id": out.name, "started_utc": stamp, "upstream_revision": REVISION,
         "source": source_identity(), "config": config, "workers": 1, "threads": 1,
         "seed": None, "compiler_flags": None, "warm_start": None, "portfolio_runs": 1,
         "machine": {"hostname": platform.node(), "os": platform.platform(),
                     "python": sys.version, "cpu_count": os.cpu_count(),
                     "affinity_cpus": len(os.sched_getaffinity(0)),
                     "meminfo": Path("/proc/meminfo").read_text()},
         "steps": [], "outputs": {}}
    m["official_hashes"] = {str(p.relative_to(OFFICIAL)): digest(p) for p in OFFICIAL.rglob("*")
                            if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}
    # Recover exact uncommitted development source independently of later edits.
    snapshot = out / "development-source"
    snapshot.mkdir()
    for p in (ROOT / "dev").glob("*"):
        if p.is_file():
            shutil.copyfile(p, snapshot / p.name)
    save(out / "manifest.json", m)
    return out, m

def finish(out, m, success):
    changed = [p for p, h in m["official_hashes"].items() if digest(OFFICIAL / p) != h]
    m["official_inputs_unchanged"] = not changed
    m["changed_official_files"] = changed
    m["success"] = success and not changed
    m["total_subprocess_wall_s"] = sum(s["wall_s"] for s in m["steps"])
    save(out / "manifest.json", m)
    print("manifest:", out / "manifest.json", flush=True)
    return 0 if m["success"] else 1

def profile_worker(args):
    sys.path.insert(0, str(OFFICIAL))
    from m3d.model import Instance, Submission
    from m3d.checker import check
    from m3d.scorer import score_case
    from m3d.baseline import Baseline
    from m3d.negotiated import Negotiated
    out = Path(args.out)
    suite = OFFICIAL / args.suite
    case = suite / (args.case + ".json")
    entry = next(c for c in json.loads((suite / "suite.json").read_text())["cases"]
                 if c["name"] == args.case)
    stages = {}
    start = time.perf_counter()
    inst = Instance.load(case)
    stages["load_s"] = time.perf_counter() - start
    cls = Baseline if args.router == "baseline" else Negotiated
    method = "_build_tree" if args.router == "baseline" else "_route_net"
    original = getattr(cls, method)
    seen = set()
    search = {"calls": 0, "first_calls": 0, "repeated_calls": 0,
              "all_search_s": 0.0, "repeated_search_s": 0.0,
              "capacity_ignoring_probe_calls": 0}
    def wrapped(self, nid, *pos, **kw):
        repeated = nid in seen
        seen.add(nid)
        t0 = time.perf_counter()
        try:
            return original(self, nid, *pos, **kw)
        finally:
            elapsed = time.perf_counter() - t0
            search["calls"] += 1
            search["all_search_s"] += elapsed
            search["repeated_calls" if repeated else "first_calls"] += 1
            if repeated:
                search["repeated_search_s"] += elapsed
            if args.router == "baseline" and kw.get("hard") is False:
                search["capacity_ignoring_probe_calls"] += 1
    setattr(cls, method, wrapped)
    engine = cls(inst)
    profiler = cProfile.Profile()
    start = time.perf_counter()
    sub, stats = profiler.runcall(engine.run)
    stages["route_profiled_s"] = time.perf_counter() - start
    profiler.dump_stats(str(out / "routing.pstats"))
    data = pstats.Stats(profiler)
    hot = [{"file": Path(k[0]).name, "line": k[1], "function": k[2],
            "primitive_calls": v[0], "calls": v[1], "self_s": v[2], "cumulative_s": v[3]}
           for k, v in data.stats.items()]
    hot.sort(key=lambda x: x["self_s"], reverse=True)
    if sub is None:
        save(out / "profile.json", {"legal": False, "router_stats": asdict(stats),
                                    "stages": stages, "search": search, "hot_functions": hot[:25]})
        return 1
    start = time.perf_counter()
    result = check(inst, sub)
    stages["check_s"] = time.perf_counter() - start
    candidate = out / "candidate.sol.json"
    start = time.perf_counter()
    sub.save(str(candidate))
    stages["save_json_s"] = time.perf_counter() - start
    start = time.perf_counter()
    reloaded = Submission.load(str(candidate))
    stages["reload_json_s"] = time.perf_counter() - start
    score = score_case(inst, reloaded, entry["baseline_total"])
    accepted = out / (args.case + ".sol.json")
    success = result.legal and score.legal and result.total_delay == score.total_delay
    if success:
        os.replace(candidate, accepted)
    report = {"case": args.case, "suite": args.suite, "router": args.router,
              "legal": success, "total_delay": result.total_delay, "ratio": score.ratio,
              "baseline_delay": entry["baseline_total"], "router_stats": asdict(stats),
              "stages": stages, "search": search, "hot_functions": hot[:25],
              "timing_note": "cProfile/instrumentation overhead; cumulative timings overlap"}
    save(out / "profile.json", report)
    print(json.dumps(report, indent=2), flush=True)
    return 0 if success else 1

def audit_worker(args):
    out = Path(args.out)
    # Explicit pinned public output comparison, never an original-work incumbent.
    pr = get_json("https://api.github.com/repos/partcleda/eda-3d-routing-challenge/pulls/3")
    expected = "4e21227867ee1f8f72c9f4d9ad446e05c20fe452"
    if pr["head"]["sha"] != expected:
        raise RuntimeError("PR head changed; review and repin before downloading")
    repo = pr["head"]["repo"]["full_name"]
    tree = get_json(f"https://api.github.com/repos/{repo}/git/trees/{expected}?recursive=1")
    if tree.get("truncated"):
        raise RuntimeError("incomplete public tree; do not infer source availability")
    files = {p["path"]: p for p in tree["tree"] if p["type"] == "blob"}
    official_files = {str(p.relative_to(OFFICIAL)) for p in OFFICIAL.rglob("*") if p.is_file()}
    extra_source = [p for p in files if p not in official_files and
                    Path(p).suffix in (".py", ".cpp", ".cc", ".h", ".hpp", ".rs")]
    provenance = {"pr": pr["html_url"], "head": expected, "repository": repo,
                  "state": pr["state"], "method": "pathfinder_lns",
                  "retrieved_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                  "description": pr["body"], "extra_source_paths": extra_source,
                  "scope": "hard-tier route artifacts; no solver execution or reproduction"}
    routes = out / "public-hard"
    routes.mkdir()
    prefix = "submissions/hard/pathfinder_lns/"
    man = json.loads((OFFICIAL / "benchmarks_hard/suite.json").read_text())
    paths = [prefix + c["name"] + ".sol.json" for c in man["cases"]]
    paths += [p for p in files if p.startswith(prefix) and Path(p).suffix == ".json"
              and not p.endswith(".sol.json")]
    downloaded = {}
    for p in paths:
        if p not in files:
            raise RuntimeError("public required route absent: " + p)
        url = f"https://raw.githubusercontent.com/{repo}/{expected}/{p}"
        req = urllib.request.Request(url, headers={"User-Agent": "m3d-phase1-reproduction"})
        with urllib.request.urlopen(req, timeout=20) as response:
            content = response.read(5_000_001)
        if len(content) > 5_000_000:
            raise RuntimeError("unexpectedly large public file")
        target = routes / Path(p).name
        target.write_bytes(content)
        downloaded[p] = {"url": url, "sha256": digest(target), "git_blob": files[p]["sha"]}
    provenance["files"] = downloaded
    save(out / "public-provenance.json", provenance)
    print(json.dumps({k: v for k, v in provenance.items() if k not in ("description", "files")}, indent=2))
    return 0

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode", choices=["profile", "audit"])
    p.add_argument("--suite", default="benchmarks_hard")
    p.add_argument("--case", default="case_01")
    p.add_argument("--router", choices=["baseline", "negotiated"], default="negotiated")
    p.add_argument("--budget", type=float, default=180)
    p.add_argument("--worker", action="store_true")
    p.add_argument("--out")
    args = p.parse_args()
    if Path(sys.prefix).resolve() != (ROOT / ".venv").resolve():
        p.error("use project .venv")
    if not 0 < args.budget <= 600:
        p.error("budget must be positive and at most 600 seconds")
    if args.suite not in ("benchmarks", "benchmarks_hard", "benchmarks_scale") or Path(args.case).name != args.case:
        p.error("invalid case/suite")
    if args.worker:
        return profile_worker(args) if args.mode == "profile" else audit_worker(args)
    out, m = new_run(args.mode, vars(args))
    python = str(ROOT / ".venv/bin/python")
    cmd = [python, str(Path(__file__).resolve()), args.mode, "--worker", "--out", str(out),
           "--suite", args.suite, "--case", args.case, "--router", args.router, "--budget", str(args.budget)]
    result = execute(cmd, out, args.mode, args.budget)
    m["steps"].append(result)
    success = result["exit_code"] == 0
    if args.mode == "audit" and success:
        for label, directory in [("public-score", out / "public-hard"),
                                 ("reference-score", OFFICIAL / "benchmarks_hard/reference")]:
            cmd = [python, "-m", "m3d.cli", "score-suite", "--suite", "benchmarks_hard",
                   "--submission-dir", str(directory), "--out", str(out / (label + ".json"))]
            result = execute(cmd, out, label, 60)
            m["steps"].append(result)
            success = success and result["exit_code"] == 0
    if args.mode == "profile" and (out / "profile.json").exists():
        m["result"] = json.loads((out / "profile.json").read_text())
        case = OFFICIAL / args.suite / (args.case + ".json")
        m["input"] = {"case": str(case.relative_to(OFFICIAL)), "sha256": digest(case),
                      "case_seed": json.loads(case.read_text())["seed"]}
    m["outputs"] = {str(f.relative_to(out)): digest(f) for f in out.rglob("*")
                    if f.is_file() and f.name != "manifest.json"}
    return finish(out, m, success)

if __name__ == "__main__":
    raise SystemExit(main())
