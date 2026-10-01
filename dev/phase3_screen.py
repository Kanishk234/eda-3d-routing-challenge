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
    parser.add_argument("--mode",choices=["repair","repairsoft","ablation"],default="repair")
    args=parser.parse_args()
    start=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))
    warm=ROOT/'dev/artifacts/20261001T212816.474321Z-exact-polish/routes'
    for seed in ((1,) if args.mode=="ablation" else (1,2,3)):
        for number in range(1,8):
            subprocess.run([sys.executable,str(ROOT/'dev/run_polish.py'),
                '--mode',args.mode,'--case',f'case_{number:02}',
                '--budget','2','--passes','5','--seed',str(seed),'--resume-dir',str(warm)],check=True)
    rows=[]
    for p in sorted(set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))-start):
        m=json.loads(p.read_text()); assert m['success'] and m['official_inputs_unchanged']
        c=m['cases'][0]
        rows.append({'run_id':m['run_id'],'seed':m['config']['seed'],**c,
                     'wrapper_wall_s':m['wrapper_wall_s'],'manifest_sha256':digest(p),
                     'solver_sha256':m['solver_sha256'],'binary_sha256':m['binary_sha256'],
                     'source_identity':m['source']['files_sha256']})
    out=ROOT/'docs/evidence/phase3'; out.mkdir(exist_ok=True)
    save(out/(args.label+'.json'),{'mode':args.mode,'scope':'hard01–07 only, seeds1–3,2s/case,5passes,max4 blocking nets',
          'warm_start':str(warm.relative_to(ROOT)), 'workers':1,'rows':rows,
          'total_core_wall_s':sum(r['process']['wall_s'] for r in rows),
          'total_wrapper_wall_s':sum(r['wrapper_wall_s'] for r in rows),
          'portfolio_selection':False})
    print('screen complete',len(rows),'improved',sum(r['total_delay']<r['before_delay'] for r in rows))

if __name__=='__main__': main()
