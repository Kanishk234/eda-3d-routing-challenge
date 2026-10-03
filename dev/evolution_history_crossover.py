"""Refine history release and neutral-best annealing together, keeping parents."""
import json,sys
from pathlib import Path
import evolution_pilot as pilot
import evolution_history as history
import evolution_mixed_mutation as mixed
import evolution_basin_mutation as basin
from measure import digest,save

def mutation(source,kind):
 if kind=='control':return source
 if kind=='cold_decay':return history.mutation(source,kind)
 if kind=='fine_anneal_neutral':return mixed.mutation(source,kind)
 assert kind=='cold_anneal_neutral'
 return history.mutation(mixed.mutation(source,'fine_anneal_neutral'),'cold_decay')

def main():
 files=[Path(__file__),Path(history.__file__),Path(mixed.__file__),Path(basin.__file__)];expected={str(p.resolve()):digest(p) for p in files};pilot.mutation=mutation;pilot.main();out=Path(sys.argv[sys.argv.index('--out')+1]);report=json.loads((out/'progress.json').read_text());assert all(digest(Path(p))==h for p,h in expected.items())
 for p in files:(out/p.name).write_bytes(p.read_bytes())
 report['additional_source_sha256']=expected;report['scope']+=' Cold unused-resource history decay crossed with neutral-best annealing. Both pure parents retained,not automatically replaced.';save(out/'progress.json',report)
if __name__=='__main__':main()
