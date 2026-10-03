"""Dual-price neighborhood proposals from own dynamically computed hotspots."""
import json,sys
from pathlib import Path
import evolution_pilot as pilot
from measure import ROOT,digest,save

def mutation(source,kind):
 if kind=='control':return source
 limit={'hotspot2':2,'hotspot4':4}[kind]
 fields='''    std::vector<I> hotspot_halo;
    std::uint64_t hotspot_group_attempts=0,hotspot_group_additions=0;
    void read_hotspots() {
        std::string magic;int count;
        if(!(std::cin>>magic>>count) || magic!="M3DHOTSPOT1" || count<0 || count>256) throw std::runtime_error("invalid hotspot header");
        hotspot_halo.assign(vcount,0);std::set<int> seen;
        for(int k=0;k<count;++k) {
            int v;I price;if(!(std::cin>>v>>price) || price<=0 || price>1000000000) throw std::runtime_error("invalid hotspot price");
            valid_vertex(v);if(!seen.insert(v).second)throw std::runtime_error("duplicate hotspot");
            int x=v%w,y=(v%wh)/w,z=v/wh;
            for(int dz=-1;dz<=1;++dz)for(int dy=-3;dy<=3;++dy)for(int dx=-3;dx<=3;++dx) {
                int distance=std::abs(dx)+std::abs(dy)+2*std::abs(dz);
                if(distance>3 || x+dx<0 || x+dx>=w || y+dy<0 || y+dy>=h || z+dz<0 || z+dz>=l)continue;
                int u=((z+dz)*h+y+dy)*w+x+dx;hotspot_halo[u]=add(hotspot_halo[u],multiply(price,4-distance));
            }
        }
    }
    void augment_hotspot_group(std::vector<int>& group,int seed,int cap) {
        ++hotspot_group_attempts;int anchor=nets[seed].root;I peak=0;
        for(int v:nets[seed].vertices)if(hotspot_halo[v]>peak){peak=hotspot_halo[v];anchor=v;}
        if(!peak || group.size()>=static_cast<std::size_t>(cap))return;
        int ax=anchor%w,ay=(anchor%wh)/w,az=anchor/wh;
        std::vector<std::pair<I,int>> ranked;
        for(std::size_t j=0;j<nets.size();++j) {
            if(std::find(group.begin(),group.end(),j)!=group.end())continue;
            I affinity=0;
            for(int v:nets[j].vertices)if(std::abs(v%w-ax)+std::abs((v%wh)/w-ay)<=4 && std::abs(v/wh-az)<=1)affinity=std::max(affinity,hotspot_halo[v]);
            if(affinity>0)ranked.emplace_back(multiply(affinity,std::max<I>(1,nets[j].delay-relaxed_delay(nets[j]))),static_cast<int>(j));
        }
        std::sort(ranked.begin(),ranked.end(),[](auto a,auto b){return a.first!=b.first?a.first>b.first:a.second<b.second;});
        int added=0;
        for(auto candidate:ranked){if(added>=LIMIT || group.size()>=static_cast<std::size_t>(cap))break;group.push_back(candidate.second);++added;++hotspot_group_additions;}
    }
'''.replace('LIMIT',str(limit))
 for anchor in ['struct Engine {','        engine.read(search_only);','                if(group.size()>13) ++large_group_attempts;']:assert source.count(anchor)==1
 source=source.replace('struct Engine {','struct Engine {\n'+fields,1).replace('        engine.read(search_only);','        engine.read(search_only);engine.read_hotspots();',1).replace('                if(group.size()>13) ++large_group_attempts;','                augment_hotspot_group(group,index,max_blockers+1);\n                if(group.size()>13) ++large_group_attempts;',1)
 output=r'<<",\"negotiation_rounds\":"<<negotiation_rounds';extra=r'<<",\"hotspot_group_attempts\":"<<hotspot_group_attempts<<",\"hotspot_group_additions\":"<<hotspot_group_additions';assert source.count(output)==1;return source.replace(output,extra+output)

def main():
 args=sys.argv;plan_path=Path(args[1]);plan=json.loads(plan_path.read_text());hotspot_path=ROOT/plan['hotspots'];hotspots=json.loads(hotspot_path.read_text());assert hotspots['complete'];index={(r['tier'],r['case']):r for r in hotspots['rows']};coverage=json.loads((ROOT/plan['coverage']).read_text());source=Path(__file__);frozen={str(p.resolve()):digest(p) for p in [source,hotspot_path]};old_run=pilot.bridge.run_core
 for item in plan['cases']:
  row=index[(item['tier'],item['case'])];stage=next(r for r in coverage['rows'] if r['tier']==item['tier']);parent=ROOT/'dev/artifacts'/stage['run_id']/'routes'/(item['case']+'.sol.json');assert digest(parent)==row['parent_sha256']
 def with_hotspots(directory,data,*args,**kwargs):
  matches=[r for (tier,case),r in index.items() if directory.name.startswith(tier+'-'+case+'-')];assert len(matches)==1;row=matches[0];data+='M3DHOTSPOT1 '+str(len(row['hotspots']))+'\n'+''.join(f'{v} {price}\n' for v,price in row['hotspots']);return old_run(directory,data,*args,**kwargs)
 pilot.bridge.run_core=with_hotspots;pilot.mutation=mutation;pilot.main();out=Path(args[args.index('--out')+1]);r=json.loads((out/'progress.json').read_text());assert all(digest(Path(p))==sha for p,sha in frozen.items());r['additional_source_sha256']=frozen;r['hotspot_analysis_wall_s']=sum(x['wall_s'] for x in hotspots['rows']);r['scope']+=' Dynamic own dual-price hotspots;analysis adds search cost. Geometric vicinity is a heuristic neighborhood,not a certified cut. Mandatory blockers retained and group cap respected.';(out/source.name).write_bytes(source.read_bytes());save(out/'progress.json',r)
if __name__=='__main__':main()
