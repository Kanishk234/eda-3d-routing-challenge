"""Recover fixed hard incumbents and compare declared development neighborhoods."""
import argparse
import json
import math
import subprocess
import sys
from pathlib import Path
from measure import ROOT, OFFICIAL, digest, save


def run(case, mode, budget, passes, seed, start, work_budget, negotiation, donor=None):
    before = set((ROOT / "dev/artifacts").glob("*-exact-polish/manifest.json"))
    command = [sys.executable, str(ROOT / "dev/run_polish.py"), "--mode", mode,
               "--budget", str(budget), "--passes", str(passes), "--seed", str(seed),
               "--resume-dir", str(start)]
    command += ["--work-budget", str(work_budget)]
    for key, value in negotiation.items():
        command += ["--" + key.replace("_", "-"), str(value)]
    if mode.endswith("_donor"):
        command += ["--donor-dir",str(donor)]
    if case:
        command += ["--case", case]
    subprocess.run(command, check=True)
    paths = set((ROOT / "dev/artifacts").glob("*-exact-polish/manifest.json")) - before
    if len(paths) != 1:
        raise RuntimeError("ambiguous run discovery")
    path = paths.pop()
    manifest = json.loads(path.read_text())
    if not manifest["success"] or not manifest["official_inputs_unchanged"]:
        raise RuntimeError("failed or changed evaluation inputs")
    return path, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["recover", "cycles", "operators", "spatial", "hybrid", "donor"])
    parser.add_argument("--start", type=Path)
    parser.add_argument("--donor-dir",type=Path)
    parser.add_argument("--kernel", choices=["fanout_astar", "fanout_tight", "fanout_fine"], default="fanout_astar")
    parser.add_argument("--work-budget", type=int, default=0)
    parser.add_argument("--budget", type=float, help="per-case wall safety cap; stage defaults are20/10/5 seconds")
    parser.add_argument("--out", type=Path, help="new report destination; existing files are protected")
    for key in ("present_initial", "present_step", "history_step"):
        parser.add_argument("--" + key.replace("_", "-"), type=int, default=2)
    args = parser.parse_args()
    if not 0 <= args.work_budget < 2**64 or (args.budget is not None and not 0 <= args.budget <= 600):
        parser.error("invalid budget")
    if args.stage=="donor" and (not args.donor_dir or args.kernel!="fanout_fine"): parser.error("donor screen requires fine kernel and explicit donor directory")
    negotiation = {key: getattr(args, key) for key in ("present_initial", "present_step", "history_step")}
    if any(not 0 <= value <= 64 for value in negotiation.values()):
        parser.error("schedule values must be0..64")
    if args.stage != "recover" and not args.start:
        parser.error("explicit frozen --start required")
    destination = args.out or ROOT / "docs/evidence/phase3" / ("recovery-" + args.stage + ".json")
    if destination.exists():
        parser.error("report exists; choose a new report name before rerunning")
    report = {"stage": args.stage, "workers": 1, "rows": [], "complete": False,
              "kernel": args.kernel, "work_budget": args.work_budget, "negotiation": negotiation,
              "scope": "hard01/04/07 development; full hard only for fixed recovery",
              "limitations": "New reference-assisted recovery, not historical output recovery. No per-case portfolio selection. Time caps may alter completed work. Reference generation cost unmeasured."}
    if args.stage == "recover":
        start = OFFICIAL / "benchmarks_hard/reference"
        cases = [None]
        configs = [(args.kernel, 20, 1000, 1)]
    else:
        start = args.start.resolve()
        cases = ["case_01", "case_04", "case_07"]
        configs = ([(args.kernel, 10, passes, 1) for passes in (100, 1000)]
                   if args.stage == "cycles" else
                   [(mode, 5, 1000, seed) for mode in
                    (args.kernel, *(args.kernel + "_" + op for op in (("diverse", "spatial") if args.stage == "spatial" else ("shuffle", "diverse", "adaptive"))))
                    for seed in (1, 2, 3)])
    if args.stage == "hybrid":
        configs=[(args.kernel+"_"+op,5,1000,seed) for op in ("diverse","adaptive","hybrid") for seed in (1,2,3)]
    if args.stage == "donor":
        configs=[(args.kernel+"_"+op,5,1000,seed) for op in ("adaptive","donor") for seed in (1,2,3)]
    if args.budget is not None:
        configs = [(mode, args.budget, passes, seed) for mode, _, passes, seed in configs]
    report["donor_directory"] = str(args.donor_dir) if args.donor_dir else None
    report["start"] = str(start)
    report["start_hashes"] = {p.name: digest(p) for p in start.glob("*.sol.json")}
    report["configs"] = configs
    save(destination, report)
    for mode, budget, passes, seed in configs:
        for case in cases:
            path, manifest = run(case, mode, budget, passes, seed, start, args.work_budget, negotiation,args.donor_dir)
            report["rows"].append({"run_id": manifest["run_id"], "manifest_sha256": digest(path),
                                   "source_identity": manifest["source"]["files_sha256"],
                                   "source_revision": manifest["source"]["revision"],
                                   "dirty_diff_sha256": manifest["source"]["diff_sha256"],
                                   "solver_sha256": manifest["solver_sha256"],
                                   "binary_sha256": manifest["binary_sha256"],
                                   "config": manifest["config"], "cases": manifest["cases"],
                                   "score": manifest["result"], "outputs": manifest["outputs"],
                                   "wrapper_wall_s": manifest["wrapper_wall_s"]})
            save(destination, report)
    report["complete"] = True
    report["total_wrapper_wall_s"] = sum(r["wrapper_wall_s"] for r in report["rows"])
    if args.stage != "recover":
        summaries = []
        for mode, budget, passes, seed in configs:
            records = [r["cases"][0] for r in report["rows"] if
                       (r["config"]["mode"], r["config"]["budget"], r["config"]["passes"], r["config"]["seed"]) ==
                       (mode, budget, passes, seed)]
            summaries.append({"mode": mode, "budget_s": budget, "passes": passes, "seed": seed,
                              "development_geomean": math.exp(sum(math.log(r["ratio"]) for r in records)/len(records)),
                              "delays": {r["case"]: r["total_delay"] for r in records}})
        report["development_summaries"] = summaries
        if args.stage in ("operators", "spatial", "hybrid"):
            comparisons = []
            for mode in (args.kernel + "_" + op for op in (("hybrid",) if args.stage == "hybrid" else (("diverse", "spatial") if args.stage == "spatial" else ("shuffle", "diverse", "adaptive")))):
                for control in ((args.kernel+"_diverse",args.kernel+"_adaptive") if args.stage == "hybrid" else ((args.kernel, args.kernel + "_diverse") if args.stage == "spatial" else (args.kernel, args.kernel + "_shuffle"))):
                    if mode == control:
                        continue
                    counts = {"wins": 0, "ties": 0, "losses": 0}
                    ratios = []
                    for seed in (1, 2, 3):
                        candidate = next(s for s in summaries if s["mode"] == mode and s["seed"] == seed)
                        baseline = next(s for s in summaries if s["mode"] == control and s["seed"] == seed)
                        for name, delay in candidate["delays"].items():
                            old = baseline["delays"][name]
                            counts["wins" if delay < old else "losses" if delay > old else "ties"] += 1
                            ratios.append(old / delay)
                    comparisons.append({"mode": mode, "control": control, **counts,
                                        "geomean_delay_ratio": math.exp(sum(map(math.log, ratios))/len(ratios))})
            report["matched_comparisons"] = comparisons
    if args.stage == "donor":
        counts={"wins":0,"ties":0,"losses":0};ratios=[]
        for seed in (1,2,3):
            control=next(s for s in summaries if s["mode"]==args.kernel+"_adaptive" and s["seed"]==seed)
            candidate=next(s for s in summaries if s["mode"]==args.kernel+"_donor" and s["seed"]==seed)
            for case,delay in candidate["delays"].items():
                old=control["delays"][case];counts["wins" if delay<old else "losses" if delay>old else "ties"]+=1;ratios.append(old/delay)
        report["matched_comparisons"]=[{**counts,"geomean_delay_ratio":math.exp(sum(map(math.log,ratios))/len(ratios))}]
    save(destination, report)
    print("report:", destination)


if __name__ == "__main__":
    main()
