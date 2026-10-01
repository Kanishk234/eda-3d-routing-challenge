"""Run C++ exact tree polish from an explicitly validated baseline/incumbent."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import platform
import shutil
import signal
import subprocess
import sys
import time
from measure import ROOT, OFFICIAL, REVISION, digest, save, source_identity
sys.path.insert(0, str(OFFICIAL))
from m3d.model import Instance, Submission, NetRoute
from m3d.checker import check
from m3d.scorer import score_case, leaderboard

BUILD_FLAGS = ["-O3", "-std=c++17", "-Wall", "-Wextra", "-Wpedantic"]
ENGINE = ROOT / "dev/artifacts/build/exact_polish"

def encode(inst, sub):
    def vid(v):
        x,y,z=v
        return (z*inst.height+y)*inst.width+x
    routes={r.net:r for r in sub.routes}
    lines=[f"M3DIN1 {inst.width} {inst.height} {inst.layers} {inst.via_delay} {len(inst.nets)}",
           " ".join(map(str,inst.layer_delay))]
    pins=inst.pin_vertex()
    for n in inst.nets:
        edges=routes[n.id].edges
        lines.append(f"{n.id} {vid(pins[n.driver])} {len(n.sinks)} {len(edges)}")
        lines.append(" ".join(str(vid(pins[s])) for s in n.sinks))
        lines.extend(f"{vid(a)} {vid(b)}" for a,b in edges)
    return "\n".join(lines)+"\n"

def decode(inst, text):
    tokens=iter(text.split())
    def take():
        try: return next(tokens)
        except StopIteration: raise ValueError("truncated core output") from None
    if take()!="M3DOUT1": raise ValueError("invalid core output")
    count,total,timeout,accepted,searches,expansions=[int(take()) for _ in range(6)]
    if count!=len(inst.nets) or timeout not in (0,1): raise ValueError("invalid core header")
    vertices=inst.width*inst.height*inst.layers
    def coord(v):
        if not 0<=v<vertices: raise ValueError("invalid core vertex")
        z,r=divmod(v,inst.width*inst.height); y,x=divmod(r,inst.width)
        return x,y,z
    routes=[]
    delays={}
    for _ in range(count):
        nid,nedges,delay=[int(take()) for _ in range(3)]
        if nid in delays or not 0<=nedges<vertices: raise ValueError("invalid core route")
        delays[nid]=delay
        routes.append(NetRoute(nid,[(coord(int(take())),coord(int(take()))) for _ in range(nedges)]))
    if next(tokens,None) is not None: raise ValueError("trailing core output")
    return Submission(inst.name,routes), {"total_delay":total,"budget_reached":bool(timeout),
            "accepted_replacements":accepted,"searches":searches,"expansions":expansions,
            "net_delays":delays}

def run_core(case_dir, data, budget, seed, passes, mode="polish"):
    case_dir.mkdir(parents=True)
    source=case_dir/"input.txt"; output=case_dir/"output.txt"; resources=case_dir/"resources.txt"
    source.write_text(data)
    command=[str(ENGINE),str(budget),str(seed),str(passes),mode]
    measured=["/usr/bin/time","-f","%e %U %S %M","-o",str(resources),*command]
    start=time.perf_counter()
    interrupted=external_timeout=False
    with source.open() as stdin,output.open("w") as stdout,(case_dir/"stderr.log").open("w") as stderr:
        process=subprocess.Popen(measured,stdin=stdin,stdout=stdout,stderr=stderr,start_new_session=True)
        try:
            process.wait(timeout=budget+5)
        except (subprocess.TimeoutExpired,KeyboardInterrupt) as exc:
            interrupted=isinstance(exc,KeyboardInterrupt); external_timeout=not interrupted
            os.killpg(process.pid,signal.SIGTERM)
            try: process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid,signal.SIGKILL); process.wait()
    result={"command":command,"cwd":str(ROOT),"budget_s":budget,"external_cap_s":budget+5,
            "wall_s":time.perf_counter()-start,"exit_code":process.returncode,
            "interrupted":interrupted,"external_timeout":external_timeout,"peak_rss_kib":None,
            "user_cpu_s":None,"system_cpu_s":None}
    if resources.exists() and resources.read_text().strip():
        fields=resources.read_text().splitlines()[-1].split()
        if len(fields)==4:
            try: result.update(user_cpu_s=float(fields[1]),system_cpu_s=float(fields[2]),peak_rss_kib=int(fields[3]))
            except ValueError: pass
    try: result["repair_counters"]=json.loads((case_dir/"stderr.log").read_text().splitlines()[-1])
    except (ValueError,IndexError): result["repair_counters"]=None
    return result,output.read_text()

def main():
    wrapper_start=time.perf_counter()
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--suite",choices=["benchmarks","benchmarks_hard"],default="benchmarks_hard")
    p.add_argument("--case")
    p.add_argument("--mode",choices=["polish","repair","repairsoft","ablation"],default="polish")
    p.add_argument("--budget",type=float,default=10)
    p.add_argument("--seed",type=int,default=1)
    p.add_argument("--passes",type=int,default=5)
    p.add_argument("--resume-dir",type=Path)
    a=p.parse_args()
    if Path(sys.prefix).resolve()!=(ROOT/".venv").resolve(): p.error("use project .venv")
    if not 0<=a.budget<=600 or not 1<=a.passes<=100 or not 0<=a.seed<2**64: p.error("invalid config")
    if not ENGINE.is_file(): p.error("compile dev/solver/exact_polish.cpp first")
    tier="hard" if a.suite=="benchmarks_hard" else "intro"
    incumbent=(a.resume_dir or ROOT/"dev/artifacts/incumbents"/tier).resolve()
    man=json.loads((OFFICIAL/a.suite/"suite.json").read_text())
    cases=[c for c in man["cases"] if a.case is None or c["name"]==a.case]
    if not cases: p.error("unknown case")
    stamp=dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    out=ROOT/"dev/artifacts"/(stamp+"-exact-polish"); out.mkdir(parents=True)
    (out/"routes").mkdir()
    source=source_identity()
    m={"run_id":out.name,"started_utc":stamp,"upstream_revision":REVISION,"source":source,
       "config":{**vars(a),"resume_dir":str(a.resume_dir) if a.resume_dir else None},
       "machine":{"hostname":platform.node(),"os":platform.platform(),"python":sys.version,
                  "affinity_cpus":len(os.sched_getaffinity(0)),"meminfo":Path("/proc/meminfo").read_text()},
       "workers":1,"threads":1,"compiler_flags":BUILD_FLAGS,"binary_sha256":digest(ENGINE),
       "solver_sha256":digest(ROOT/"dev/solver/exact_polish.cpp"),
       "compiler_version":subprocess.check_output(["g++","--version"],text=True).splitlines()[0],
       "warm_start":{"directory":str(incumbent),"origin":"validated baseline or explicit resumed incumbent"},
       "portfolio_runs":1,"cases":[],"outputs":{}}
    snapshot=out/"development-source"; snapshot.mkdir()
    for f in [ROOT/"dev/run_polish.py",ROOT/"dev/measure.py",ROOT/"dev/solver/exact_polish.cpp"]:
        shutil.copyfile(f,snapshot/f.name)
    official_hashes={str(f.relative_to(OFFICIAL)):digest(f) for f in OFFICIAL.rglob("*")
                     if f.is_file() and "__pycache__" not in f.parts and f.suffix!=".pyc"}
    m["official_hashes"]=official_hashes
    save(out/"manifest.json",m)
    scores=[]
    ok=True
    for c in cases:
        inst=Instance.load(OFFICIAL/a.suite/c["instance_file"])
        warm=incumbent/(c["name"]+".sol.json")
        old=Submission.load(warm); previous=check(inst,old)
        if not previous.legal: raise RuntimeError("unverified/illegal warm start")
        # Accepted checkpoint exists before search, so child failure cannot erase it.
        destination=out/"routes"/warm.name
        temporary=destination.with_suffix(".json.tmp")
        old.save(str(temporary)); os.replace(temporary,destination)
        result,raw=run_core(out/c["name"],encode(inst,old),a.budget,a.seed,a.passes,a.mode)
        record={"case":c["name"],"case_sha256":digest(OFFICIAL/a.suite/c["instance_file"]),
                "case_seed":inst.seed,"warm_start_sha256":digest(warm),"before_delay":previous.total_delay,
                "process":result,"candidate_accepted":False,"error":None}
        try:
            if result["exit_code"]!=0: raise ValueError("core did not complete; checkpoint retained")
            candidate,stats=decode(inst,raw)
            checked=check(inst,candidate)
            if not checked.legal or checked.total_delay!=stats["total_delay"] or checked.total_delay>previous.total_delay:
                raise ValueError("candidate illegal, mis-scored or worse")
            if {n.net:n.delay for n in checked.nets}!=stats["net_delays"]:
                raise ValueError("per-net delay disagreement")
            candidate.save(str(temporary))
            reloaded=Submission.load(temporary)
            rechecked=check(inst,reloaded)
            if not rechecked.legal or rechecked.total_delay!=checked.total_delay:
                raise ValueError("serialization changed legality or delay")
            os.replace(temporary,destination)
            record.update(candidate_accepted=True,core=stats)
        except (ValueError,OSError) as exc:
            record["error"]=str(exc); ok=False
        score=score_case(inst,Submission.load(destination),c["baseline_total"])
        scores.append(score)
        record.update(legal=score.legal,total_delay=score.total_delay,ratio=score.ratio,output_sha256=digest(destination))
        m["cases"].append(record); m["outputs"][str(destination.relative_to(out))]=digest(destination)
        save(out/"manifest.json",m)
        print(f"{c['name']}: legal={score.legal} delay={score.total_delay} before={previous.total_delay} "
              f"ratio={score.ratio:.6f} wall={result['wall_s']:.3f}s",flush=True)
        if result["interrupted"]: break
    lb=leaderboard(scores).to_dict()
    if len(scores)!=len(man["cases"]):
        lb.update(complete=False,aggregate_score=0.0)
    m["result"]=lb
    m["official_inputs_unchanged"]=all(digest(OFFICIAL/f)==h for f,h in official_hashes.items())
    m["success"]=ok and m["official_inputs_unchanged"] and len(scores)==len(cases)
    m["wrapper_wall_s"]=time.perf_counter()-wrapper_start
    m["total_core_wall_s"]=sum(c["process"]["wall_s"] for c in m["cases"])
    save(out/"score.json",lb); save(out/"manifest.json",m)
    print("manifest:",out/"manifest.json")
    print("complete:",lb["complete"],"aggregate:",lb["aggregate_score"])
    return 0 if m["success"] else 1

if __name__=="__main__":
    raise SystemExit(main())
