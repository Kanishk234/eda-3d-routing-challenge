"""Serial budget scaling on representative development cases only."""
import json
import subprocess
import sys
from measure import ROOT, save, digest

def main():
    start=set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))
    warm=ROOT/'dev/artifacts/20261001T215550.921679Z-exact-polish/routes'
    for budget in (2,10):
        for case in ('case_01','case_04','case_07'):
            subprocess.run([sys.executable,str(ROOT/'dev/run_polish.py'),'--mode','wide',
              '--case',case,'--seed','1','--passes','100','--budget',str(budget),
              '--resume-dir',str(warm)],check=True)
    rows=[]
    for p in sorted(set((ROOT/'dev/artifacts').glob('*-exact-polish/manifest.json'))-start):
        m=json.loads(p.read_text());assert m['success'] and m['official_inputs_unchanged']
        rows.append({'run_id':m['run_id'],'config':m['config'],'case':m['cases'][0],
          'wrapper_wall_s':m['wrapper_wall_s'],'source_identity':m['source']['files_sha256'],
          'solver_sha256':m['solver_sha256'],'binary_sha256':m['binary_sha256'],'manifest_sha256':digest(p)})
    save(ROOT/'docs/evidence/phase3/budget-scaling.json',{'scope':'cases01/04/07,seed1,100 cycles,2vs10s; same plateau warm starts; no validation-case tuning','rows':rows,
         'total_wrapper_wall_s':sum(r['wrapper_wall_s'] for r in rows),'portfolio_selection':False})

if __name__=='__main__':main()
