// Experimental fresh negotiation; reuses our existing parser/search/checks.
// Separate binary leaves the production solver and active native jobs unchanged.
#define main production_entry
#include "exact_polish.cpp"
#undef main

int main(int argc,char** argv) {
 try {
  if(argc!=8) throw std::runtime_error("usage: fresh SECONDS SEED ROUNDS WORK aggressive|gradual CONFLICT_ONLY POLISH_PASSES");
  double seconds=std::stod(argv[1]);auto seed=std::stoull(argv[2]);int rounds=std::stoi(argv[3]);auto work=std::stoull(argv[4]);std::string schedule=argv[5];int selective=std::stoi(argv[6]),passes=std::stoi(argv[7]);
  if(!std::isfinite(seconds)||seconds<0||seconds>600||rounds<1||rounds>10000||work==0||(schedule!="aggressive"&&schedule!="gradual")||(selective!=0&&selective!=1)||passes<0||passes>1000) throw std::runtime_error("invalid fresh config");
  std::signal(SIGINT,on_signal);std::signal(SIGTERM,on_signal);Engine e;e.work_limit=work;e.deadline=std::chrono::steady_clock::now()+std::chrono::duration_cast<std::chrono::steady_clock::duration>(std::chrono::duration<double>(seconds));e.read(false);
  auto start=std::chrono::steady_clock::now();auto original=e.nets;auto old_owner=e.owner;auto physical=e.layer;I physical_via=e.via;constexpr I SCALE=64;
  for(I& delay:e.layer) { delay=multiply(delay,SCALE); }
  e.via=multiply(e.via,SCALE);
  std::fill(e.owner.begin(),e.owner.end(),-1);for(Net& n:e.nets){n.vertices.clear();n.edges.clear();n.delay=0;}
  e.astar_search=true;e.tight_heuristic=true;e.random_ties=true;e.tie_seed=seed;e.fanout_prices=true;
  std::vector<int> usage(e.vcount,0);std::vector<I> history(e.vcount,0);std::vector<char> over(e.vcount,0);std::vector<int> order(e.nets.size());std::iota(order.begin(),order.end(),0);std::mt19937_64 rng(seed);
  double present=schedule=="gradual"?.05:2, factor=schedule=="gradual"?1.03:1.12,cap=schedule=="gradual"?3:32;I history_step=schedule=="gradual"?3:128;bool legal=false;int completed_rounds=0;std::uint64_t routed_nets=0;bool failed=false;
  for(int iteration=0;iteration<rounds && !e.expired();++iteration){
   std::shuffle(order.begin(),order.end(),rng);I price=static_cast<I>(std::llround(present*SCALE));
   for(int j:order){
    if(selective && iteration && iteration%10){bool touches=false;for(int v:e.nets[j].vertices)if(over[v]){touches=true;break;}if(!touches)continue;}
    for(int v:e.nets[j].vertices) { --usage[v]; }
    Net candidate;
    if(!e.shortest(e.nets[j],candidate,false,0,&usage,&history,price)){failed=true;break;}
    e.nets[j]=std::move(candidate);for(int v:e.nets[j].vertices)++usage[v];++routed_nets;
   }
   if(failed)break;
   ++completed_rounds;bool conflict=false;
   for(int v=0;v<e.vcount;++v){over[v]=usage[v]>1;if(over[v]){conflict=true;history[v]=add(history[v],multiply(history_step,usage[v]-1));}}
   if(!conflict){legal=true;break;}
   present=std::min(cap,present*factor);
  }
  e.layer=physical;e.via=physical_via;e.heuristic_table.clear();
  if(legal){
   for(Net& n:e.nets){if(n.delay%SCALE)throw std::runtime_error("nonintegral physical delay");n.delay/=SCALE;for(int v:n.vertices){if(e.owner[v]>=0)throw std::runtime_error("fresh ownership collision");e.owner[v]=n.id;}if(e.validate_tree(n)!=n.delay)throw std::runtime_error("fresh physical mismatch");}
   e.fresh_legal=1;e.fresh_attempts=1;e.price_units=16;e.polish(seed,passes,false);
  } else {e.nets=std::move(original);e.owner=std::move(old_owner);e.fresh_attempts=1;}
  e.optimization_s=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  std::cerr<<"FRESH "<<legal<<" "<<completed_rounds<<" "<<routed_nets<<" "<<e.expansions<<"\n";e.output();return 0;
 }catch(const std::exception& x){std::cerr<<x.what()<<"\n";return 2;}
}
