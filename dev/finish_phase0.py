"""Retain compact Phase 0 run evidence and verify artifacts; no benchmark runs."""
import json
from pathlib import Path
import shutil
import subprocess
from measure import ROOT, OFFICIAL, REVISION, digest, save
out = ROOT / "docs/evidence/phase0"
runs = []
for p in sorted((ROOT / "dev/artifacts").glob("*/manifest.json")):
    m = json.loads(p.read_text())
    compact = {k: v for k, v in m.items() if k not in ("official_hashes", "machine", "source")}
    compact["manifest_path"] = str(p.relative_to(ROOT))
    compact["manifest_sha256"] = digest(p)
    compact["machine"] = {k: v for k, v in m["machine"].items() if k != "meminfo"}
    compact["source"] = {k: v for k, v in m["source"].items() if k != "file_hashes"}
    compact["development_source_hashes"] = {k: v for k, v in m["source"]["file_hashes"].items()
                                             if k.startswith("dev/")}
    runs.append(compact)
    for name, h in m["outputs"].items():
        assert digest(p.parent / name) == h, (p, name)
    assert m["official_inputs_unchanged"]
    save(out / "official-input-hashes.json", m["official_hashes"])
save(out / "runs.json", runs)
smokes = [r for r in runs if r["config"]["mode"] == "smoke" and r["success"]]
assert len(smokes) == 2
assert smokes[0]["outputs"]["case_01.sol.json"] == smokes[1]["outputs"]["case_01.sol.json"]
assert all(r["result"]["legal"] and r["result"]["total_delay"] == 240 and
           r["result"]["ratio"] == 1 for r in smokes)
timeouts = [r for r in runs if r["steps"][0]["timeout"]]
assert len(timeouts) == 1 and not timeouts[0]["success"]
assert not timeouts[0]["outputs"]
assert not list((ROOT / timeouts[0]["manifest_path"]).parent.glob("case_01.sol.json"))
target = ROOT / "docs/research/M3D_ROUTING_RESEARCH.md"
target.parent.mkdir(parents=True, exist_ok=True)
if not target.exists():
    shutil.copyfile(ROOT / "docs/M3D_ROUTING_RESEARCH.md", target)
assert digest(target) == digest(ROOT / "docs/M3D_ROUTING_RESEARCH.md")
# Compare every archived official file to its exact pinned Git blob, not just pre/post run.
for name, h in json.loads((out / "official-input-hashes.json").read_text()).items():
    original = subprocess.check_output(["git", "show", REVISION + ":" + name], cwd=ROOT)
    import hashlib
    assert hashlib.sha256(original).hexdigest() == h, name
print(json.dumps({"runs": [{"run_id": r["run_id"], "success": r["success"],
                           "result": r.get("result")} for r in runs],
                  "route_sha256": smokes[0]["outputs"]["case_01.sol.json"],
                  "research_sha256": digest(target),
                  "official_files_verified": len(json.loads((out / "official-input-hashes.json").read_text()))},
                 indent=2))
