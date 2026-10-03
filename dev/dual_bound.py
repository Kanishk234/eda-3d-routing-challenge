"""Conservative vertex-price delay bounds on independent sink paths.
A valid lower bound, not a jointly routable solution or achievable score.
"""
import argparse,json,subprocess,time
from pathlib import Path
import run_polish as bridge
from measure import ROOT,OFFICIAL,digest,save

TAIL=r'''
#undef main
int main(int argc,char** argv) {
 try {
  int iterations=argc>1?std::stoi(argv[1]):16;
  int step=argc>2?std::stoi(argv[2]):4;
  bool strengthen=argc>3 && std::string(argv[3])=="max_sink";
  dual_resolution=argc>4?std::stoi(argv[4]):1;
  bool adaptive=argc>5 && std::string(argv[5])=="adaptive";
  if(dual_resolution!=1 && dual_resolution!=16)throw std::runtime_error("invalid price resolution");
  if(iterations<1 || iterations>64 || step<1 || step>64) throw std::runtime_error("invalid bound config");
  Engine engine;engine.deadline=std::chrono::steady_clock::now()+std::chrono::seconds(120);engine.read(false);
  std::fill(engine.owner.begin(),engine.owner.end(),-1);
  I upper=0;for(const Net& net:engine.nets)upper=add(upper,net.delay);
  engine.astar_search=true;engine.tight_heuristic=true;engine.fanout_prices=true;engine.tree_prices=0;engine.price_units=1024;
  std::vector<int> usage(engine.vcount,0);std::vector<I> prices(engine.vcount,0);
  std::vector<std::vector<I>> physical;
  engine.fanout_prices=false;
  for(const Net& net:engine.nets) {
   Net route;if(!engine.shortest(net,route,false,0,&usage,&prices,0)) throw std::runtime_error("physical bound expired");
   std::vector<I> costs;for(int sink:net.sinks)costs.push_back(engine.dist[sink]);physical.push_back(costs);
  }
  I best=0;
  std::cout<<"{\"iterations\":[";
  for(int iteration=0;iteration<iterations;++iteration) {
   __int128 scaled=0,price_sum=0;std::vector<double> demand(engine.vcount,0);
   for(std::size_t index=0;index<engine.nets.size();++index) {
    const Net& net=engine.nets[index];
    __int128 single=-1;std::vector<int> critical_path;
    if(strengthen) {
     engine.fanout_prices=false;Net full;
     if(!engine.shortest(net,full,false,0,&usage,&prices,0)) throw std::runtime_error("full-price bound expired");
     __int128 base=0;for(I cost:physical[index])base+=cost;
     int selected=-1;
     for(std::size_t k=0;k<net.sinks.size();++k) {
      __int128 value=base-physical[index][k]+engine.dist[net.sinks[k]];
      if(value>single){single=value;selected=net.sinks[k];}
     }
     for(int v=selected;v!=net.root;v=engine.parent[v]) {
      if(v<0) throw std::runtime_error("critical path missing");critical_path.push_back(v);
     }
    }
    engine.fanout_prices=true;
    Net route;if(!engine.shortest(net,route,false,0,&usage,&prices,0)) throw std::runtime_error("bound search expired");
    __int128 uniform=0;for(int sink:net.sinks)uniform+=engine.dist[sink];
    if(single>uniform) {scaled+=single;for(int v:critical_path)demand[v]+=1;}
    else {
     scaled+=uniform;auto counts=downstream_counts(route);
     for(std::size_t k=0;k<route.vertices.size();++k) if(route.vertices[k]!=route.root)
      demand[route.vertices[k]]+=static_cast<double>(counts[k])/net.sinks.size();
    }
   }
   for(I p:prices)price_sum+=p;
   __int128 numerator=scaled-engine.price_units*price_sum/dual_resolution;
   I bound=numerator>0?static_cast<I>((numerator+engine.price_units-1)/engine.price_units):0;best=std::max(best,bound);
   if(iteration)std::cout<<",";
   std::cout<<"{\"iteration\":"<<iteration<<",\"lower_bound\":"<<bound<<",\"best_lower_bound\":"<<best<<",\"priced_vertices\":"<<std::count_if(prices.begin(),prices.end(),[](I p){return p>0;})<<"}";
   double rate=static_cast<double>(step)/std::sqrt(iteration+1.0);
   if(adaptive) {
    double norm=0;
    for(int v=0;v<engine.vcount;++v)if(engine.pin_owner[v]<0 && (prices[v]>0 || demand[v]>1))norm+=(demand[v]-1)*(demand[v]-1);
    if(norm>0)rate=std::min(rate,0.25*std::max<I>(0,upper-bound)/norm);
   }
   for(int v=0;v<engine.vcount;++v)if(engine.pin_owner[v]<0)
    prices[v]=std::max<I>(0,static_cast<I>(std::llround(prices[v]+dual_resolution*rate*(demand[v]-1))));
  }
  std::cout<<"],\"best_lower_bound\":"<<best<<",\"expansions\":"<<engine.expansions<<"}\n";
 }catch(const std::exception& e){std::cerr<<e.what()<<"\n";return 1;}
}
'''

def source_text(original):
 anchor='static_cast<I>(std::ceil(std::sqrt(static_cast<double>(n.sinks.size()))))'
 assert original.count(anchor)==2
 modified=original.replace(anchor,'static_cast<I>(n.sinks.size())')
 price='multiply(price,price_units)/divisor'
 assert modified.count(price)==1
 modified=modified.replace(price,'multiply(price,price_units)/dual_resolution/divisor')
 return 'static long long dual_resolution=1;\n#define main original_main\n'+modified+TAIL

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--coverage',type=Path,required=True);p.add_argument('--cases',nargs='+',required=True,help='tier/case');p.add_argument('--iterations',type=int,default=16);p.add_argument('--step',type=int,default=4);p.add_argument('--model',choices=['uniform','max_sink'],default='uniform');p.add_argument('--resolution',type=int,choices=[1,16],default=1);p.add_argument('--adaptive',action='store_true');p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out=a.out.resolve();assert not a.out.exists();a.out.mkdir(parents=True);parent=ROOT/'dev/solver/exact_polish.cpp';cpp=a.out/'bound.cpp';cpp.write_text(source_text(parent.read_text()));binary=a.out/'bound';cmd=['g++','-O3','-std=c++17','-Wall','-Wextra',str(cpp),'-o',str(binary)];subprocess.run(cmd,check=True);coverage=json.loads(a.coverage.read_text());result=dict(complete=False,coverage_sha256=digest(a.coverage),parent_source_sha256=digest(parent),source_sha256=digest(cpp),binary_sha256=digest(binary),build_command=cmd,iterations=a.iterations,step=a.step,model=a.model,resolution=a.resolution,adaptive=a.adaptive,rows=[],scope='Valid conservative independent-path Lagrangian lower bounds under nonnegative integer vertex prices. Uniform fanout division with fixed-point floor relaxes price costs. No achievable ceiling,global optimality or legal route claim.');save(a.out/'report.json',result)
 for key in a.cases:
  tier,name=key.split('/');stage=next(x for x in coverage['rows'] if x['tier']==tier);suite=stage['config']['suite'];inv=json.loads((OFFICIAL/suite/'suite.json').read_text());case=next(x for x in inv['cases'] if x['name']==name);path=OFFICIAL/suite/case['instance_file'];route=ROOT/'dev/artifacts'/stage['run_id']/'routes'/(name+'.sol.json');inst=bridge.Instance.load(path);sub=bridge.Submission.load(route);checked=bridge.check(inst,sub);assert checked.legal;start=time.monotonic();process=subprocess.run([str(binary),str(a.iterations),str(a.step),a.model,str(a.resolution),'adaptive' if a.adaptive else 'fixed'],input=bridge.encode(inst,sub),capture_output=True,text=True,timeout=125,check=True);raw=json.loads(process.stdout);assert 0<raw['best_lower_bound']<=checked.total_delay;result['rows'].append(dict(tier=tier,case=name,case_sha256=digest(path),parent_sha256=digest(route),incumbent_delay=checked.total_delay,baseline_delay=case['baseline_total'],score_ceiling=case['baseline_total']/raw['best_lower_bound'],wall_s=time.monotonic()-start,command=[str(binary),str(a.iterations),str(a.step),a.model,str(a.resolution),'adaptive' if a.adaptive else 'fixed'],**raw));save(a.out/'report.json',result);print(key,raw['best_lower_bound'],checked.total_delay,flush=True)
 result['complete']=True;save(a.out/'report.json',result)
if __name__=='__main__':main()
