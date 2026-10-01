"""Freeze Phase 1 evidence and baseline-only incumbents, after official verification."""
import json
from pathlib import Path
import shutil
import sys
from measure import ROOT, OFFICIAL, REVISION, digest, save
sys.path.insert(0, str(OFFICIAL))
from m3d.model import Instance, Submission
from m3d.checker import check

evidence = ROOT / "docs/evidence/phase1"
evidence.mkdir(parents=True, exist_ok=True)
intro = ROOT / "dev/artifacts/20261001T171253.322797Z-suite"
interrupted = ROOT / "dev/artifacts/20261001T171347.624859Z-suite"
hard = ROOT / "dev/artifacts/20261001T171522.463214Z-suite"
audit = ROOT / "dev/artifacts/20261001T171845.570340Z-audit"
for folder in [intro, interrupted]:
    path = folder / "manifest.json"
    m = json.loads(path.read_text())
    m["methodology_notes"] = ["Intro/hard runs overlapped for approximately 1.3 seconds; "
                              "intro score is valid but its timing is not a fully isolated sample. "
                              "First hard run was intentionally interrupted and excluded from timing/quality claims."]
    save(path, m)
comparison = {"upstream_revision": REVISION, "scope": "intro/hard baseline reproduction and pinned public hard comparison",
              "tiers": {}, "public_provenance": json.loads((audit / "public-provenance.json").read_text())}
for tier, folder, run in [("intro", "benchmarks", intro), ("hard", "benchmarks_hard", hard)]:
    score = json.loads((run / "score.json").read_text())
    assert score["complete"] and score["aggregate_score"] == 1
    assert all(c["legal"] and c["total_delay"] == c["baseline_delay"] for c in score["cases"])
    target = ROOT / "dev/artifacts/incumbents" / tier
    target.mkdir(parents=True, exist_ok=True)
    routes = []
    man = json.loads((OFFICIAL / folder / "suite.json").read_text())
    for entry in man["cases"]:
        original = run / "routes" / (entry["name"] + ".sol.json")
        result = check(Instance.load(OFFICIAL / folder / entry["instance_file"]), Submission.load(original))
        assert result.legal and result.total_delay == entry["baseline_total"]
        incumbent = target / original.name
        temporary = target / (original.name + ".tmp")
        shutil.copyfile(original, temporary)
        temporary.replace(incumbent)
        routes.append({"case": entry["name"], "legal": True, "delay": result.total_delay,
                       "sha256": digest(incumbent), "source_run": run.name,
                       "path": str(incumbent.relative_to(ROOT)), "origin": "fresh official baseline reproduction",
                       "case_sha256": digest(OFFICIAL / folder / entry["instance_file"])})
    save(target / "index.json", routes)
    comparison["tiers"][tier] = {"baseline_reproduction": score, "source_run": run.name,
                                 "incumbents": routes}
public = json.loads((audit / "public-score.json").read_text())
reference = json.loads((audit / "reference-score.json").read_text())
assert public["complete"] and public["n_legal"] == 9 and reference["aggregate_score"] == 1
comparison["tiers"]["hard"]["public_comparison"] = public
comparison["tiers"]["hard"]["reference_rescore"] = reference
comparison["tiers"]["hard"]["best_observed_in_this_audit"] = {
    "method": "PR3 pathfinder_lns", "aggregate": public["aggregate_score"],
    "note": "public output quality; not our solver or a claim of latest/global best"}
save(evidence / "comparison.json", comparison)
runs = []
profiles = []
for path in sorted((ROOT / "dev/artifacts").glob("*/manifest.json")):
    m = json.loads(path.read_text())
    if m["started_utc"] < "20261001T171200":
        continue
    compact = {k: v for k, v in m.items() if k not in ("official_hashes", "source", "machine")}
    compact["source"] = {k: v for k, v in m["source"].items() if k != "file_hashes"}
    compact["manifest_path"] = str(path.relative_to(ROOT))
    compact["manifest_sha256"] = digest(path)
    compact["machine"] = {k: v for k, v in m["machine"].items() if k != "meminfo"}
    runs.append(compact)
    assert m["official_inputs_unchanged"], path
    for name,h in m.get("outputs",{}).items():
        assert digest(path.parent/name) == h, name
    if m["config"].get("mode") == "profile":
        assert m["success"] and m["result"]["legal"]
        profiles.append({"run_id":m["run_id"],"resources":m["steps"][0],"profile":m["result"]})
assert {p["profile"]["suite"] for p in profiles} == {"benchmarks_hard","benchmarks_scale"}
save(evidence / "runs.json", runs)
save(evidence / "profiles.json", profiles)
print(json.dumps({"intro_aggregate":comparison["tiers"]["intro"]["baseline_reproduction"]["aggregate_score"],
                  "hard_aggregate":reference["aggregate_score"],"public_hard":public["aggregate_score"],
                  "profiles":[{"case":p["profile"]["suite"]+"/"+p["profile"]["case"],
                                "stages":p["profile"]["stages"],"search":p["profile"]["search"],
                                "rss_kib":p["resources"]["peak_rss_kib"],
                                "wall_s":p["resources"]["wall_s"]} for p in profiles]},indent=2))
