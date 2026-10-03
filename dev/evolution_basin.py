"""Launch basin variants through the existing measured source-evolution runner."""
import json,sys
from pathlib import Path
import evolution_pilot as pilot
import evolution_basin_mutation as operators
from measure import digest,save

def main():
 expected={str(p.resolve()):digest(p) for p in [Path(__file__),Path(operators.__file__)]}
 pilot.mutation=operators.mutation
 pilot.main()
 out=Path(sys.argv[sys.argv.index('--out')+1]);report=json.loads((out/'progress.json').read_text())
 assert all(digest(Path(p))==h for p,h in expected.items())
 report['additional_source_sha256']=expected
 for file in [Path(__file__),Path(operators.__file__)]:
  (out/file.name).write_bytes(file.read_bytes())
 report['scope']+=' Isolated fine-price uphill/annealing mutations; best legal state restored by existing repair transaction. No score regression allowed in retained output.'
 save(out/'progress.json',report)
if __name__=='__main__':main()
