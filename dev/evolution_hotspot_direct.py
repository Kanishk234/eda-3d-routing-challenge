"""Refine hotspots into direct coordinated neighborhoods that bypass seed gains."""
import json,sys
from pathlib import Path
import evolution_hotspot as hotspot
from measure import digest,save
base_mutation=hotspot.mutation

def mutation(source,kind):
 if kind=='control':return source
 limit={'hotspot_direct2':2,'hotspot_direct4':4}[kind];source=base_mutation(source,'hotspot'+str(limit));anchor='                if(conflict_windows) {';assert source.count(anchor)==1
 addition='''                if(hotspot_direct) {
                    augment_hotspot_group(group,index,max_blockers+1);
                    if(group.size()<2){++no_gain;continue;}
                    ++attempts;
                } else if(conflict_windows) {'''
 source=source.replace(anchor,addition,1).replace('    std::vector<I> hotspot_halo;','    bool hotspot_direct=true;\n    std::vector<I> hotspot_halo;',1)
 call='\n                augment_hotspot_group(group,index,max_blockers+1);';assert source.count(call)==1;return source.replace(call,'\n                if(!hotspot_direct) augment_hotspot_group(group,index,max_blockers+1);',1)

def main():
 source=Path(__file__);expected=digest(source);hotspot.mutation=mutation;hotspot.main();out=Path(sys.argv[sys.argv.index('--out')+1]);report=json.loads((out/'progress.json').read_text());assert digest(source)==expected;report['additional_source_sha256'][str(source.resolve())]=expected;(out/source.name).write_bytes(source.read_bytes());report['scope']+=' Direct hotspot groups bypass the individual-net gain gate;all external nets stay fixed and normal negotiated legality/rollback/physical acceptance apply.';save(out/'progress.json',report)
if __name__=='__main__':main()
