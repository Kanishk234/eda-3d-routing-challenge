"""Isolated fixed-point precision variants with unchanged physical objective."""
import json,sys
from pathlib import Path
import evolution_pilot as pilot
from measure import digest,save

def mutation(source,kind):
 if kind=='control':return source
 units={'precision64':64,'precision256':256,'precision1024':1024}[kind]
 anchor='engine.price_units=kernel=="fanout_fine"?16:1;'
 assert source.count(anchor)==1
 return source.replace(anchor,f'engine.price_units=kernel=="fanout_fine"?{units}:1;')

def main():
 source=Path(__file__);expected=digest(source);pilot.mutation=mutation;pilot.main();out=Path(sys.argv[sys.argv.index('--out')+1]);report=json.loads((out/'progress.json').read_text());assert digest(source)==expected;(out/source.name).write_bytes(source.read_bytes());report['additional_source_sha256']={str(source.resolve()):expected};report['scope']+=' Finer fixed-point congestion units;all physical distances and reported scores unchanged. No training or external model API.';save(out/'progress.json',report)
if __name__=='__main__':main()
