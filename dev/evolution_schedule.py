"""Test spending scarce expansion budgets on coordinated repair before polish."""
import json,sys
from pathlib import Path
import evolution_pilot as pilot
from measure import digest,save

def mutation(source,kind):
 if kind=='control':return source
 assert kind=='repair_first'
 anchor='engine.price_units=kernel=="fanout_fine"?16:1;'
 assert source.count(anchor)==1
 return source.replace(anchor,anchor+'engine.repair_first=true;')

def main():
 source=Path(__file__);expected=digest(source);pilot.mutation=mutation;pilot.main();out=Path(sys.argv[sys.argv.index('--out')+1]);report=json.loads((out/'progress.json').read_text());assert digest(source)==expected;(out/source.name).write_bytes(source.read_bytes());report['additional_source_sha256']={str(source.resolve()):expected};report['scope']+=' Budget scheduling refinement prompted by stress profiles:50M consumed by initial polish before any repair proposals. Compare repair-first with existing polish-first.';save(out/'progress.json',report)
if __name__=='__main__':main()
