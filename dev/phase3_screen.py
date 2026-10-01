"""Bounded development-only repair screening; never selects per-case best results."""
import json
import subprocess
import sys
from pathlib import Path
from measure import ROOT, digest, save


def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--label",default="repair-diagnostics")
    parser.add_argument("--mode",choices=["repair","repairsoft","ablation","negotiated","explore","restart","select","wide","walk","descent","compact","fanout","restart_fanout","restart_compact","restart_polish"],default="repair")
    parser.add_argument("--budget",type=float,default=2)
    parser.add_argument("--passes",type=int,default=5)
    parser.add_argument("--resume-dir",type=Path,default=ROOT/'dev/artifacts/20261001T212816.474321Z-exact-polish/routes')
    parser.add_argument("--cases",default="1,2,3,4,5,6,7")
    parser.add_argument("--seeds",default="1,2,3")
    args=parser.parse_args()
    numbers=[int(x) for x in args.cases.split(',')]
    seeds=[int(x) for x in args.seeds.split(',')]
    if not numbers or any(x not in range(1,8) for x in numbers): parser.error("development cases01–07 only")
    start=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))
    warm=args.resume_dir.resolve()
    for seed in ((1,) if args.mode=="ablation" else seeds):
        for number in numbers:
            subprocess.run([sys.executable,str(ROOT/'dev/run_polish.py'),
                '--mode',args.mode,'--case',f'case_{number:02}',
                '--budget',str(args.budget),'--passes',str(args.passes),'--seed',str(seed),'--resume-dir',str(warm)],check=True)
    rows=[]
    for p in sorted(set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))-start):
        m=json.loads(p.read_text()); assert m['success'] and m['official_inputs_unchanged']
        c=m['cases'][0]
        rows.append({'run_id':m['run_id'],'seed':m['config']['seed'],**c,
                     'wrapper_wall_s':m['wrapper_wall_s'],'manifest_sha256':digest(p),
                     'solver_sha256':m['solver_sha256'],'binary_sha256':m['binary_sha256'],
                     'source_identity':m['source']['files_sha256']})
    out=ROOT/'docs/evidence/phase3'; out.mkdir(exist_ok=True)
    save(out/(args.label+'.json'),{'mode':args.mode,'scope':{'development_cases':numbers,'seeds':seeds,'budget_s':args.budget,'passes':args.passes},
          'warm_start':str(warm.relative_to(ROOT)), 'workers':1,'rows':rows,
          'total_core_wall_s':sum(r['process']['wall_s'] for r in rows),
          'total_wrapper_wall_s':sum(r['wrapper_wall_s'] for r in rows),
          'portfolio_selection':False})
    print('screen complete',len(rows),'improved',sum(r['total_delay']<r['before_delay'] for r in rows))

if __name__=='__main__': main()
