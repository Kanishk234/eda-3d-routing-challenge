"""Retain the exact repair family; compare strengthened per-sink bounds."""
import sys,json
from pathlib import Path
import exact_tree_repair,exact_tree_repair_tight,exact_pair_repair
from measure import digest,save

def main():
 files=[Path(__file__),Path(exact_tree_repair_tight.__file__)];frozen={str(p.resolve()):digest(p) for p in files}
 exact_tree_repair.solve_trees=exact_tree_repair_tight.solve_trees
 exact_pair_repair.main()
 out=Path(sys.argv[sys.argv.index('--out')+1]);report=json.loads((out/'progress.json').read_text());assert all(digest(Path(p))==h for p,h in frozen.items());report['additional_frozen_sha256']=frozen
 for p in files:(out/p.name).write_bytes(p.read_bytes())
 save(out/'progress.json',report)
if __name__=='__main__':main()
