"""Explore releasable congestion prices without changing physical acceptance."""
import json,sys
from pathlib import Path
import evolution_pilot as pilot
from measure import digest,save

def mutation(source,kind):
 if kind=='control':return source
 anchor='''            for(int v=0;v<vcount;++v) if(usage[v]>1) {
                conflict=true;history[v]=add(history[v],multiply(negotiation.history_step,usage[v]-1));
            }'''
 assert source.count(anchor)==1
 if kind=='dual_release':tail='else if(usage[v]==0) history[v]=std::max<I>(0,history[v]-negotiation.history_step);'
 elif kind=='cold_decay':tail='else if(usage[v]==0 && iteration%3==2) history[v]=history[v]*3/4;'
 elif kind=='cycle_history':tail='else if(iteration%6==5) history[v]=history[v]/2;'
 else:raise ValueError(kind)
 return source.replace(anchor,anchor+' '+tail)

def main():
 source=Path(__file__);expected=digest(source);pilot.mutation=mutation;pilot.main();out=Path(sys.argv[sys.argv.index('--out')+1]);report=json.loads((out/'progress.json').read_text());assert digest(source)==expected;(out/source.name).write_bytes(source.read_bytes());report['additional_source_sha256']={str(source.resolve()):expected};report['scope']+=' Releasable nonnegative local history tolls:projected dual-like update or unused-resource decay. Not an exact dual optimizer or dual bound.';save(out/'progress.json',report)
if __name__=='__main__':main()
