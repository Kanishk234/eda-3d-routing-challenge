"""Sample diverse high-price direct neighborhoods using the seeded group RNG."""
import json,sys
from pathlib import Path
import evolution_hotspot_direct as direct
from measure import digest,save
base_mutation=direct.mutation

def mutation(source,kind):
 if kind=='control':return source
 if kind=='hotspot_direct4':return base_mutation(source,kind)
 assert kind=='hotspot_diverse4';source=base_mutation(source,'hotspot_direct4')
 old='''        int added=0;
        for(auto candidate:ranked){if(added>=4 || group.size()>=static_cast<std::size_t>(cap))break;group.push_back(candidate.second);++added;++hotspot_group_additions;}'''
 new='''        if(ranked.size()>12)ranked.resize(12);
        int added=0;
        while(added<4 && group.size()<static_cast<std::size_t>(cap) && !ranked.empty()) {
            std::vector<double> weights;for(auto candidate:ranked)weights.push_back(std::sqrt(static_cast<double>(candidate.first)));
            std::discrete_distribution<std::size_t> pick(weights.begin(),weights.end());auto selected=pick(group_rng);
            group.push_back(ranked[selected].second);ranked.erase(ranked.begin()+selected);++added;++hotspot_group_additions;
        }'''
 assert source.count(old)==1;return source.replace(old,new)

def main():
 source=Path(__file__);expected=digest(source);direct.mutation=mutation;direct.main();out=Path(sys.argv[sys.argv.index('--out')+1]);report=json.loads((out/'progress.json').read_text());assert digest(source)==expected;report['additional_source_sha256'][str(source.resolve())]=expected;(out/source.name).write_bytes(source.read_bytes());report['scope']+=' Diversified direct groups draw up to4nets without replacement from top12affinities,sqrt-weighted,using existing seeded group RNG.';save(out/'progress.json',report)
if __name__=='__main__':main()
