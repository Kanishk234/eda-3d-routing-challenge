// Exact single-net shortest-path rerouting. Original implementation; C++17.
// Official JSON/checking remains in Python. Input is a versioned integer bridge.
#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <csignal>
#include <cstdint>
#include <iostream>
#include <limits>
#include <numeric>
#include <queue>
#include <random>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <tuple>
#include <functional>
#include <vector>

using I = std::int64_t;
constexpr I INF = std::numeric_limits<I>::max()/4;
volatile std::sig_atomic_t stopped = 0;
void on_signal(int) { stopped = 1; }
I add(I a, I b) {
    if (b < 0 || a < 0 || a > INF-b) throw std::runtime_error("delay overflow");
    return a+b;
}
I multiply(I value,I scale) {
    if(value<0 || scale<0 || (scale && value>INF/scale)) throw std::runtime_error("priority overflow");
    return value*scale;
}
struct Net {
    int id, root;
    std::vector<int> sinks, vertices;
    std::vector<std::pair<int,int>> edges;
    I delay=0;
};
// Number of sinks whose unique root path uses each vertex of a coherent tree.
std::vector<int> downstream_counts(const Net& n) {
    if(n.vertices.empty()) return {}; // Fresh construction has no old component.
    auto local=[&](int v) {
        auto it=std::lower_bound(n.vertices.begin(),n.vertices.end(),v);
        if(it==n.vertices.end() || *it!=v) throw std::runtime_error("missing flow vertex");
        return static_cast<int>(it-n.vertices.begin());
    };
    std::vector<std::vector<int>> links(n.vertices.size());
    for(auto [a,b]:n.edges) {int u=local(a),v=local(b);links[u].push_back(v);links[v].push_back(u);}
    int root=local(n.root);
    std::vector<int> parent(n.vertices.size(),-1),order{root},counts(n.vertices.size(),0);
    parent[root]=root;
    for(std::size_t k=0;k<order.size();++k) for(int v:links[order[k]]) if(parent[v]<0) {
        parent[v]=order[k];order.push_back(v);
    }
    if(order.size()!=n.vertices.size() || n.edges.size()+1!=order.size()) throw std::runtime_error("invalid flow tree");
    for(int sink:n.sinks) ++counts[local(sink)];
    for(std::size_t k=order.size();k>1;--k) {
        int u=order[k-1],p=parent[u];
        if(counts[p]>static_cast<int>(n.sinks.size())-counts[u]) throw std::runtime_error("sink count overflow");
        counts[p]+=counts[u];
    }
    if(counts[root]!=static_cast<int>(n.sinks.size())) throw std::runtime_error("invalid sink flow");
    return counts;
}
std::vector<int> canonical_geometry(const std::vector<Net>& nets) {
    std::vector<int> state;
    for(const Net& n:nets) {
        state.push_back(n.id);state.push_back(n.root);state.push_back(static_cast<int>(n.edges.size()));
        auto edges=n.edges;
        for(auto& e:edges) if(e.first>e.second) std::swap(e.first,e.second);
        std::sort(edges.begin(),edges.end());
        for(auto [a,b]:edges) {state.push_back(a);state.push_back(b);}
    }
    return state;
}
struct NegotiationConfig { I present_initial=2,present_step=2,history_step=2; };
struct Engine {
    NegotiationConfig negotiation;
    int group_limit=13;
    bool repair_first=false;
    bool accept_equal=false;
    int repair_sampling=0;
    std::uint64_t neutral_moves=0;
    int polish_order=0;
    std::uint64_t polish_attempts=0,polish_completed=0,polish_improvements=0;
    int w,h,l,vcount,wh;
    I via;
    I price_units=1;
    std::vector<I> layer;
    std::vector<Net> nets, donor_nets;
    std::vector<int> owner,pin_owner,parent;
    std::vector<I> dist,heuristic_table;
    std::chrono::steady_clock::time_point deadline;
    std::uint64_t searches=0, expansions=0, accepted=0;
    double read_s=0,validation_s=0,optimization_s=0,search_reset_s=0,search_rebuild_s=0,snapshot_s=0,negotiation_setup_s=0,negotiation_scan_s=0;
    bool timed_out=false,work_exhausted=false;
    std::uint64_t work_limit=0;
    bool ablation_mode=false;
    bool compact_groups=false,fanout_prices=false,astar_search=false,tight_heuristic=false,gap_order=false,discounted_groups=false;
    bool random_ties=false; std::uint64_t tie_seed=0;
    bool conflict_windows=false;
    bool seed_first_groups=false;
    bool shuffled_groups=false,diverse_proposals=false,adaptive_groups=false,spatial_groups=false;
    bool eligibility_proposals=false;
    std::uint64_t eligibility_searches=0,eligibility_recovered=0;
    std::uint64_t eligibility_attempts=0,eligibility_strict=0,eligibility_neutral=0,eligibility_failed=0,eligibility_nonimproving=0;
    I eligibility_gain=0;
    I escape_penalty=4;
    int escape_options=2;
    bool escape_direct=false;
    int tree_prices=0;
    int neutral_tabu=0;
    std::vector<std::vector<int>> neutral_history;
    std::uint64_t neutral_tabu_rejections=0,neutral_history_peak_bytes=0;
    double neutral_tabu_s=0;
    std::vector<int> sink_flow,flow_touched;
    std::uint64_t flow_builds=0,flow_shared_vertices=0;
    double flow_setup_s=0;
    std::mt19937_64 group_rng{0};
    std::array<double,3> neighborhood_weights{{1,1,1}};
    std::array<std::uint64_t,3> neighborhood_attempts{{0,0,0}},neighborhood_gains{{0,0,0}};
    std::uint64_t large_group_attempts=0,large_group_strict=0;
    I large_group_gain=0;
    std::uint64_t donor_eligible=0,donor_selected=0,donor_gains=0;
    std::array<std::uint64_t,65> group_sizes{};
    std::uint64_t tie_rank(int v) const {
        std::uint64_t x=static_cast<std::uint64_t>(v)+tie_seed+0x9e3779b97f4a7c15ULL;
        x=(x^(x>>30))*0xbf58476d1ce4e5b9ULL;
        x=(x^(x>>27))*0x94d049bb133111ebULL;
        return x^(x>>31);
    }
    std::uint64_t negotiation_rounds=0,conflicted_rounds=0;
    std::uint64_t uphill_moves=0,fresh_attempts=0,fresh_legal=0;
    std::uint64_t selection_nodes=0,selection_complete=0,selection_partial=0;
    std::uint64_t proposals=0,no_gain=0,too_many=0,attempts=0,failed=0,nonimproving=0;

    bool expired() {
        if(work_limit && expansions>=work_limit) { work_exhausted=true; timed_out=true; return true; }
        if (stopped || std::chrono::steady_clock::now() >= deadline) {
            timed_out=true;
            return true;
        }
        return false;
    }
    template<class F> void neighbors(int u,F visit) const {
        int z=u/wh, rem=u%wh, y=rem/w, x=rem%w;
        if (x+1<w) visit(u+1,layer[z]);
        if (x>0) visit(u-1,layer[z]);
        if (y+1<h) visit(u+w,layer[z]);
        if (y>0) visit(u-w,layer[z]);
        if (z+1<l) visit(u+wh,via);
        if (z>0) visit(u-wh,via);
    }
    void valid_vertex(int v) const {
        if (v<0 || v>=vcount) throw std::runtime_error("vertex outside grid");
    }
    I weight(int a,int b) const {
        valid_vertex(a); valid_vertex(b);
        I result=-1;
        neighbors(a,[&](int v,I cost){ if(v==b) result=cost; });
        if(result<0) throw std::runtime_error("illegal edge");
        return result;
    }
    I validate_tree(Net& net) const {
        std::set<int> vertices{net.root};
        for(int s:net.sinks) vertices.insert(s);
        std::set<std::pair<int,int>> unique;
        for(auto [a,b]:net.edges) {
            weight(a,b);
            if(a>b) std::swap(a,b);
            if(!unique.insert({a,b}).second) throw std::runtime_error("duplicate edge");
            vertices.insert(a); vertices.insert(b);
        }
        net.vertices.assign(vertices.begin(),vertices.end());
        for(int v:net.vertices)
            if(pin_owner[v]>=0 && pin_owner[v]!=net.id)
                throw std::runtime_error("foreign terminal");
        // Validate only this tree's vertices, not the entire routing grid.
        auto local=[&](int v) {
            auto it=std::lower_bound(net.vertices.begin(),net.vertices.end(),v);
            if(it==net.vertices.end() || *it!=v) throw std::runtime_error("missing tree vertex");
            return static_cast<int>(it-net.vertices.begin());
        };
        std::vector<std::vector<std::pair<int,I>>> adj(net.vertices.size());
        for(auto [a,b]:net.edges) {
            I cost=weight(a,b);
            int u=local(a),v=local(b);
            adj[u].push_back({v,cost}); adj[v].push_back({u,cost});
        }
        std::vector<I> costs(net.vertices.size(),INF);
        std::queue<int> q;
        int root=local(net.root);
        q.push(root); costs[root]=0;
        std::size_t seen=0;
        while(!q.empty()) {
            int u=q.front(); q.pop(); ++seen;
            for(auto [v,cost]:adj[u]) if(costs[v]==INF) {
                costs[v]=add(costs[u],cost); q.push(v);
            }
        }
        if(seen!=net.vertices.size() || net.edges.size()+1!=seen)
            throw std::runtime_error("disconnected or cyclic tree");
        I total=0;
        for(int s:net.sinks) total=add(total,costs[local(s)]);
        return total;
    }
    void read(bool search_only) {
        std::string magic;
        int count;
        if(!(std::cin>>magic>>w>>h>>l>>via>>count) || magic!="M3DIN1")
            throw std::runtime_error("invalid bridge header");
        if(w<=0 || h<=0 || l<=0 || w>2000000 || h>2000000 || l>2000000)
            throw std::runtime_error("invalid dimensions");
        I size=static_cast<I>(w)*h*l;
        if(w<=0 || h<=0 || l<=0 || size>2000000 || via<=0 || via>1000000000 ||
           count<=0 || count>100000) throw std::runtime_error("unsupported grid/cost size");
        vcount=static_cast<int>(size); wh=w*h;
        layer.resize(l);
        for(I& x:layer) if(!(std::cin>>x) || x<=0 || x>1000000000)
            throw std::runtime_error("invalid layer delay");
        owner.assign(vcount,-1); pin_owner.assign(vcount,-1);
        parent.resize(vcount); dist.resize(vcount);
        std::set<int> ids;
        nets.resize(count);
        for(Net& n:nets) {
            int sinks,edges;
            if(!(std::cin>>n.id>>n.root>>sinks>>edges) || n.id<0 || sinks<=0 ||
               sinks>vcount || edges<0 || edges>=vcount || !ids.insert(n.id).second)
                throw std::runtime_error("invalid net header");
            valid_vertex(n.root);
            n.sinks.resize(sinks);
            for(int& s:n.sinks) { if(!(std::cin>>s)) throw std::runtime_error("missing sink"); valid_vertex(s); }
            std::set<int> terminals(n.sinks.begin(),n.sinks.end());
            if(terminals.size()!=n.sinks.size() || terminals.count(n.root))
                throw std::runtime_error("duplicate terminal");
            terminals.insert(n.root);
            for(int v:terminals) {
                if(pin_owner[v]!=-1) throw std::runtime_error("shared pin");
                pin_owner[v]=n.id;
            }
            n.edges.resize(edges);
            for(auto& e:n.edges) if(!(std::cin>>e.first>>e.second))
                throw std::runtime_error("missing edge");
        }
        for(std::size_t i=0;i<nets.size();++i) {
            Net& n=nets[i];
            if(search_only && i==0) continue;
            auto validation_start=std::chrono::steady_clock::now();
            n.delay=validate_tree(n);
            validation_s+=std::chrono::duration<double>(std::chrono::steady_clock::now()-validation_start).count();
            for(int v:n.vertices) {
                if(owner[v]!=-1) throw std::runtime_error("shared routing vertex");
                owner[v]=n.id;
            }
        }
    }
    bool shortest(const Net& n,Net& proposed,bool ignore_owners=false,I occupancy_penalty=0,
                  const std::vector<int>* usage=nullptr,const std::vector<I>* history=nullptr,I present=0,
                  const std::vector<I>* corridor_prices=nullptr) {
        ++searches;
        if(random_ties) tie_seed+=0x9e3779b97f4a7c15ULL;
        if(expired()) return false;
        if(usage && tree_prices) {
            auto flow_start=std::chrono::steady_clock::now();
            if(sink_flow.empty()) sink_flow.assign(vcount,0);
            for(int v:flow_touched) sink_flow[v]=0;
            flow_touched.clear();
            auto counts=downstream_counts(n);
            for(std::size_t k=0;k<counts.size();++k) {
                sink_flow[n.vertices[k]]=counts[k];flow_touched.push_back(n.vertices[k]);
                if(counts[k]>1) ++flow_shared_vertices;
            }
            ++flow_builds;
            flow_setup_s+=std::chrono::duration<double>(std::chrono::steady_clock::now()-flow_start).count();
        }
        auto reset_start=std::chrono::steady_clock::now();
        std::fill(dist.begin(),dist.end(),INF);
        std::fill(parent.begin(),parent.end(),-1);
        std::vector<char> is_sink(vcount,0);
        for(int s:n.sinks) is_sink[s]=1;
        search_reset_s+=std::chrono::duration<double>(std::chrono::steady_clock::now()-reset_start).count();
        int left=static_cast<int>(n.sinks.size());
        // Distance to the union of sink-layer rectangles in a relaxed graph.
        // Every horizontal edge there costs the cheapest physical layer cost.
        // This is consistent, is zero at every sink, and excludes congestion.
        struct Box {int z,x0,x1,y0,y1;};
        std::vector<Box> boxes;
        if(astar_search) for(int z=0;z<l;++z) {
            Box b{z,w,-1,h,-1};
            for(int sink:n.sinks) if(sink/wh==z) {
                int x=sink%w,y=(sink%wh)/w;
                b.x0=std::min(b.x0,x);b.x1=std::max(b.x1,x);
                b.y0=std::min(b.y0,y);b.y1=std::max(b.y1,y);
            }
            if(b.x1>=0) boxes.push_back(b);
        }
        I cheapest=*std::min_element(layer.begin(),layer.end());
        auto& table=heuristic_table;
        int extent=w+h-1;
        if(tight_heuristic && table.empty()) {
            table.resize(static_cast<std::size_t>(l)*l*extent);
            for(int a=0;a<l;++a) for(int b=0;b<l;++b) for(int d=0;d<extent;++d) {
                I best=INF;
                for(int k=0;k<l;++k) best=std::min(best,add(static_cast<I>(d)*layer[k],static_cast<I>(std::abs(a-k)+std::abs(b-k))*via));
                table[(a*l+b)*extent+d]=best;
            }
        }
        auto heuristic=[&](int vertex) -> I {
            if(!astar_search) return 0;
            int z=vertex/wh,x=vertex%w,y=(vertex%wh)/w;
            I result=INF;
            for(const Box& b:boxes) {
                I xy=std::max({b.x0-x,0,x-b.x1})+std::max({b.y0-y,0,y-b.y1});
                result=std::min(result,tight_heuristic?table[(z*l+b.z)*extent+xy]:add(xy*cheapest,static_cast<I>(std::abs(z-b.z))*via));
            }
            return result;
        };
        using Node=std::tuple<I,std::uint64_t,int,I>;
        std::priority_queue<Node,std::vector<Node>,std::greater<Node>> q;
        dist[n.root]=0; q.push({multiply(heuristic(n.root),price_units),random_ties?tie_rank(n.root):static_cast<std::uint64_t>(n.root),n.root,0});
        while(!q.empty() && left) {
            auto [priority,rank,u,cost]=q.top(); q.pop();
            if(cost!=dist[u]) continue;
            if(work_limit && expansions>=work_limit) { expired(); return false; }
            ++expansions;
            if((expansions&1023)==0 && expired()) return false;
            if(is_sink[u]) { is_sink[u]=0; --left; }
            neighbors(u,[&](int v,I delay){
                if((!ignore_owners && owner[v]>=0 && owner[v]!=n.id) ||
                   (pin_owner[v]>=0 && pin_owner[v]!=n.id)) return;
                I extra=(ignore_owners && owner[v]>=0 && owner[v]!=n.id)?multiply(occupancy_penalty,price_units):0;
                if(corridor_prices) extra=add(extra,multiply((*corridor_prices)[v],price_units));
                if(usage) {
                    I price=add((*history)[v],static_cast<I>((*usage)[v])*present);
                    I divisor=fanout_prices?static_cast<I>(std::ceil(std::sqrt(static_cast<double>(n.sinks.size())))):1;
                    if(tree_prices && sink_flow[v]>0) divisor=sink_flow[v];
                    else if(tree_prices==1) divisor=1;
                    extra=add(extra,multiply(price,price_units)/divisor);
                }
                I next=add(add(cost,multiply(delay,price_units)),extra);
                if(next<dist[v]) { dist[v]=next; parent[v]=u; q.push({add(next,multiply(heuristic(v),price_units)),random_ties?tie_rank(v):static_cast<std::uint64_t>(v),v,next}); }
            });
        }
        if(left || expired()) return false;
        auto rebuild_start=std::chrono::steady_clock::now();
        proposed=n; proposed.edges.clear(); proposed.delay=0;
        std::vector<char> in_tree(vcount,0);
        in_tree[n.root]=1;
        for(int sink:n.sinks) {
            int qv=sink; I physical=0;
            while(qv!=n.root) {
                int pv=parent[qv];
                if(pv<0) throw std::runtime_error("missing physical predecessor");
                physical=add(physical,weight(qv,pv)); qv=pv;
            }
            proposed.delay=add(proposed.delay,physical);
            int u=sink;
            while(!in_tree[u]) {
                int p=parent[u];
                if(p<0) throw std::runtime_error("missing predecessor");
                in_tree[u]=1;
                proposed.edges.push_back(std::minmax(u,p));
                u=p;
            }
        }
        proposed.vertices.clear();
        for(int v=0;v<vcount;++v) if(in_tree[v]) proposed.vertices.push_back(v);
        std::sort(proposed.edges.begin(),proposed.edges.end());
        search_rebuild_s+=std::chrono::duration<double>(std::chrono::steady_clock::now()-rebuild_start).count();
        return true;
    }
    bool attach(const Net& n,Net& proposed,bool root_aware,int root_scale=4,
                const std::vector<int>* usage=nullptr,const std::vector<I>* history=nullptr,I present=0) {
        proposed=n; proposed.edges.clear(); proposed.delay=0;
        std::vector<char> tree(vcount,0),remaining(vcount,0);
        std::vector<I> rootdist(vcount,INF);
        tree[n.root]=1; rootdist[n.root]=0;
        for(int v:n.sinks) remaining[v]=1;
        int left=static_cast<int>(n.sinks.size());
        using Node=std::pair<I,int>;
        while(left) {
            if(expired()) return false;
            ++searches;
            std::fill(dist.begin(),dist.end(),INF);
            std::fill(parent.begin(),parent.end(),-1);
            std::priority_queue<Node,std::vector<Node>,std::greater<Node>> q;
            for(int v=0;v<vcount;++v) if(tree[v]) {
                I seed=0;
                if(root_aware) for(int k=0;k<root_scale;++k) seed=add(seed,rootdist[v]);
                dist[v]=seed; q.push({dist[v],v});
            }
            int found=-1;
            while(!q.empty()) {
                auto [cost,u]=q.top();q.pop(); if(cost!=dist[u]) continue;
                if(work_limit && expansions>=work_limit) { expired(); return false; }
                ++expansions; if((expansions&1023)==0 && expired()) return false;
                if(remaining[u]) {found=u;break;}
                neighbors(u,[&](int v,I delay) {
                    if(tree[v] || (owner[v]>=0 && owner[v]!=n.id) ||
                       (pin_owner[v]>=0 && pin_owner[v]!=n.id)) return;
                    I step=0;for(int k=0;k<4;++k) step=add(step,delay);
                    if(usage) {
                        I price=add((*history)[v],static_cast<I>((*usage)[v])*present);
                        I divisor=fanout_prices?static_cast<I>(std::ceil(std::sqrt(static_cast<double>(n.sinks.size())))):1;
                        for(int k=0;k<4;++k) step=add(step,price/divisor);
                    }
                    I next=add(cost,step);
                    if(next<dist[v]) {dist[v]=next;parent[v]=u;q.push({next,v});}
                });
            }
            if(found<0) return false;
            std::vector<int> path; int v=found;
            while(!tree[v]) {path.push_back(v);v=parent[v];if(v<0) return false;}
            for(auto it=path.rbegin();it!=path.rend();++it) {
                int next=*it;rootdist[next]=add(rootdist[v],weight(v,next));
                proposed.edges.push_back(std::minmax(v,next));tree[next]=1;v=next;
            }
            remaining[found]=0;--left;
        }
        proposed.vertices.clear();
        for(int v=0;v<vcount;++v) if(tree[v]) proposed.vertices.push_back(v);
        for(int v:n.sinks) proposed.delay=add(proposed.delay,rootdist[v]);
        return true;
    }
    void ablation() {
        I exact_sum=0,attach_sum=0,root_sum=0; int completed=0;
        std::cout.flush();
        for(const Net& n:nets) {
            Net exact,zero,aware;
            if(!shortest(n,exact) || !attach(n,zero,false) || !attach(n,aware,true)) break;
            if(aware.delay!=exact.delay) throw std::runtime_error("root-aware/exact discrepancy");
            exact_sum=add(exact_sum,exact.delay);attach_sum=add(attach_sum,zero.delay);
            root_sum=add(root_sum,aware.delay);++completed;
        }
        std::cerr<<"{\"completed_nets\":"<<completed<<",\"exact_delay\":"<<exact_sum
                 <<",\"zero_attachment_delay\":"<<attach_sum<<",\"root_attachment_delay\":"<<root_sum<<"}\n";
    }
    void polish(unsigned long long seed,int passes,bool search_only) {
        if(search_only) {
            Net replacement;
            if(!shortest(nets[0],replacement)) throw std::runtime_error("no completed shortest tree");
            nets[0]=std::move(replacement);
            return;
        }
        std::vector<int> order(nets.size()); std::iota(order.begin(),order.end(),0);
        std::mt19937_64 random(seed);
        for(int pass=0;pass<passes && !expired();++pass) {
            // Deterministic Fisher-Yates for a fixed standard generator/seed.
            for(std::size_t i=order.size();i>1;--i) std::swap(order[i-1],order[random()%i]);
            bool improved=false;
            for(int index:order) {
                if(expired()) break;
                Net candidate;
                Net& old=nets[index];
                if(!shortest(old,candidate)) {
                    if(timed_out) break;
                    throw std::runtime_error("old route feasible but search failed");
                }
                if(candidate.delay>=old.delay) continue;
                // The original route is untouched until complete successful replacement.
                for(int v:old.vertices) owner[v]=-1;
                for(int v:candidate.vertices) {
                    if(owner[v]>=0) throw std::runtime_error("ownership commit collision");
                    owner[v]=old.id;
                }
                old=std::move(candidate); ++accepted; improved=true;
            }
            if(!improved) break;
        }
    }
    bool negotiate(const std::vector<int>& group,I& after,int max_rounds=12) {
        auto setup_start=std::chrono::steady_clock::now();
        std::vector<int> usage(vcount,0);
        std::vector<I> history(vcount,0);
        for(int j:group) for(int v:nets[j].vertices) ++usage[v];
        negotiation_setup_s+=std::chrono::duration<double>(std::chrono::steady_clock::now()-setup_start).count();
        auto routing_order=group;
        for(int iteration=0;iteration<max_rounds && !expired();++iteration) {
            ++negotiation_rounds;
            if(shuffled_groups) std::shuffle(routing_order.begin(),routing_order.end(),group_rng);
            for(int j:routing_order) {
                for(int v:nets[j].vertices) --usage[v];
                Net candidate;
                bool routed=(compact_groups || discounted_groups)?attach(nets[j],candidate,true,compact_groups?3:4,&usage,&history,add(negotiation.present_initial,multiply(negotiation.present_step,iteration))):
                    shortest(nets[j],candidate,false,0,&usage,&history,add(negotiation.present_initial,multiply(negotiation.present_step,iteration)));
                if(!routed) return false;
                nets[j]=std::move(candidate);
                for(int v:nets[j].vertices) ++usage[v];
            }
            auto scan_start=std::chrono::steady_clock::now();
            bool conflict=false;
            for(int v=0;v<vcount;++v) if(usage[v]>1) {
                conflict=true;history[v]=add(history[v],multiply(negotiation.history_step,usage[v]-1));
            }
            negotiation_scan_s+=std::chrono::duration<double>(std::chrono::steady_clock::now()-scan_start).count();
            if(conflict) { ++conflicted_rounds; continue; }
            after=0;
            for(int j:group) {
                after=add(after,nets[j].delay);
                for(int v:nets[j].vertices) owner[v]=nets[j].id;
            }
            return true;
        }
        return false;
    }
    bool seed_first_repair(const std::vector<int>& group,I& after,int rounds) {
        // Outer transaction owns rollback, including expired/incomplete repairs.
        int seed=group.front(); Net candidate;
        if(!shortest(nets[seed],candidate)) return false;
        nets[seed]=std::move(candidate);
        for(int v:nets[seed].vertices) owner[v]=nets[seed].id;
        std::vector<int> displaced(group.begin()+1,group.end());
        I remainder=0;
        if(!negotiate(displaced,remainder,rounds)) return false;
        // Exact fixed-owner polish; a failed search rolls the transaction back.
        after=0;
        for(int j:group) {
            Net improved;
            if(!shortest(nets[j],improved)) return false;
            if(improved.delay<=nets[j].delay) {
                for(int v:nets[j].vertices) owner[v]=-1;
                for(int v:improved.vertices) owner[v]=improved.id;
                nets[j]=std::move(improved);
            }
            after=add(after,nets[j].delay);
        }
        return true;
    }
    bool select_candidates(const std::vector<int>& group,I& after) {
        std::vector<std::vector<Net>> choices(group.size());
        std::vector<int> usage(vcount,0);
        std::vector<I> history(vcount,0);
        I best=0;
        for(int j:group) { best=add(best,nets[j].delay); for(int v:nets[j].vertices) ++usage[v]; }
        for(std::size_t k=0;k<group.size();++k) {
            const Net& original=nets[group[k]]; choices[k].push_back(original);
            for(int v:original.vertices) --usage[v];
            for(int option=0;option<6 && !expired();++option) {
                Net candidate;
                if(!shortest(original,candidate,false,0,&usage,&history,option%3*2)) break;
                bool duplicate=false;
                for(const Net& other:choices[k]) if(other.edges==candidate.edges) duplicate=true;
                if(!duplicate) choices[k].push_back(std::move(candidate));
            }
            for(int v:original.vertices) ++usage[v];
            std::sort(choices[k].begin(),choices[k].end(),[](const Net& a,const Net& b){return a.delay<b.delay;});
        }
        std::vector<I> lower(group.size()+1,0);
        for(std::size_t k=group.size();k>0;--k) lower[k-1]=add(lower[k],choices[k-1][0].delay);
        std::vector<int> used(vcount,0),pick(group.size()),best_pick;
        bool complete=true;
        std::function<void(std::size_t,I)> visit=[&](std::size_t k,I cost) {
            ++selection_nodes;
            if(expired()) { complete=false; return; }
            if(add(cost,lower[k])>=best) return;
            if(k==group.size()) { best=cost;best_pick=pick;return; }
            for(std::size_t c=0;c<choices[k].size();++c) {
                const Net& candidate=choices[k][c]; bool conflict=false;
                for(int v:candidate.vertices) if(used[v]) {conflict=true;break;}
                if(conflict) continue;
                for(int v:candidate.vertices) ++used[v];
                pick[k]=static_cast<int>(c);
                visit(k+1,add(cost,candidate.delay));
                for(int v:candidate.vertices) --used[v];
                if(!complete) break;
            }
        };
        if(!expired()) visit(0,0); else complete=false;
        if(complete) ++selection_complete;else ++selection_partial;
        if(best_pick.empty()) return false;
        after=best;
        for(std::size_t k=0;k<group.size();++k) {
            nets[group[k]]=std::move(choices[k][best_pick[k]]);
            for(int v:nets[group[k]].vertices) owner[v]=nets[group[k]].id;
        }
        return true;
    }
    I relaxed_delay(const Net& n) const {
        I total=0;
        for(int sink:n.sinks) {
            I xy=std::abs(n.root%w-sink%w)+std::abs((n.root%wh)/w-(sink%wh)/w);
            I best=INF;
            for(int z=0;z<l;++z)
                best=std::min(best,add(xy*layer[z],static_cast<I>(std::abs(n.root/wh-z)+std::abs(sink/wh-z))*via));
            total=add(total,best);
        }
        return total;
    }
    void repair(unsigned long long seed,int passes,I penalty=0,bool negotiated=false,bool selection=false,int max_blockers=4,bool uphill=false) {
        const int repair_rounds=max_blockers>4?24:12;
        max_blockers=std::min(max_blockers,group_limit-1);
        std::mt19937_64 rng(seed);
        I current=0;for(const Net& n:nets) current=add(current,n.delay);
        I best=current;
        std::vector<Net> best_nets;std::vector<int> best_owner;
        if(uphill) {best_nets=nets;best_owner=owner;}
        std::vector<int> order(nets.size()); std::iota(order.begin(),order.end(),0);
        std::vector<I> bounds(nets.size());
        if(gap_order || spatial_groups || repair_sampling) for(std::size_t j=0;j<nets.size();++j) bounds[j]=relaxed_delay(nets[j]);
        if(neutral_history.empty()) remember_neutral_state();
        for(int pass=0;pass<passes && !expired();++pass) {
            for(std::size_t i=order.size();i>1;--i) std::swap(order[i-1],order[rng()%i]);
            if(gap_order || spatial_groups) std::stable_sort(order.begin(),order.end(),[&](int a,int b){return nets[a].delay-bounds[a]>nets[b].delay-bounds[b];});
            auto seeds=order;
            if(repair_sampling) {
                std::vector<double> weights(nets.size());
                for(std::size_t j=0;j<nets.size();++j) {
                    double gap=static_cast<double>(std::max<I>(0,nets[j].delay-bounds[j]));
                    double divisor=repair_sampling==2?static_cast<double>(std::max<std::size_t>(1,nets[j].vertices.size())):1.0;
                    weights[j]=0.01+gap/divisor;
                }
                std::discrete_distribution<int> pick(weights.begin(),weights.end());
                for(int& j:seeds) j=pick(group_rng);
            }
            bool changed=false;
            for(int index:seeds) {
                if(expired()) break;
                ++proposals;
                std::vector<int> group{index};
                bool used_donor=false,used_escape=false;
                if(conflict_windows) {
                    Net ideal;
                    if(!shortest(nets[index],ideal,true,penalty)) break;
                    if(ideal.delay>=nets[index].delay) {++no_gain;continue;}
                    std::set<int> blockers; std::vector<int> conflicts;
                    for(int v:ideal.vertices) if(owner[v]>=0 && owner[v]!=nets[index].id) {
                        blockers.insert(owner[v]);conflicts.push_back(v);
                    }
                    if(blockers.size()>static_cast<std::size_t>(max_blockers)) {++too_many;continue;}
                    for(int j:order) if(blockers.count(nets[j].id)) group.push_back(j);
                    if(!conflicts.empty()) {
                        int anchor=conflicts[group_rng()%conflicts.size()];
                        int size=group_rng()%2?4:8;
                        int x0=std::max(0,anchor%w-size/2),y0=std::max(0,(anchor%wh)/w-size/2);
                        std::vector<int> local;
                        for(int j:order) {
                            if(std::find(group.begin(),group.end(),j)!=group.end()) continue;
                            for(int v:nets[j].vertices) {
                                int x=v%w,y=(v%wh)/w;
                                if(x>=x0 && x<x0+size && y>=y0 && y<y0+size) {local.push_back(j);break;}
                            }
                        }
                        // Include a few nearby alternatives; preserve every ideal-path blocker.
                        std::size_t target=std::min(group.size()+3,static_cast<std::size_t>(max_blockers+1));
                        for(int j:local) {if(group.size()>=target) break;group.push_back(j);}
                    }
                    ++attempts;
                } else if(spatial_groups) {
                    // Rank windows from our own incumbent, across all layers.
                    const auto& vertices=nets[index].vertices;
                    int anchor=vertices[group_rng()%vertices.size()];
                    int ax=anchor%w,ay=(anchor%wh)/w;
                    I best_merit=-1;
                    for(int size:{4,8,12}) {
                        int x0=std::max(0,ax-size/2),y0=std::max(0,ay-size/2);
                        std::vector<int> touching;
                        for(int j:order) {
                            if(j==index) continue;
                            bool hit=false;
                            for(int v:nets[j].vertices) {
                                int x=v%w,y=(v%wh)/w;
                                if(x>=x0 && x<x0+size && y>=y0 && y<y0+size) {hit=true;break;}
                            }
                            if(hit) touching.push_back(j);
                        }
                        std::stable_sort(touching.begin(),touching.end(),[&](int a,int b){
                            return nets[a].delay-bounds[a]>nets[b].delay-bounds[b];
                        });
                        if(touching.size()>static_cast<std::size_t>(max_blockers)) touching.resize(max_blockers);
                        I merit=0;
                        for(int j:touching) merit=add(merit,std::max<I>(0,nets[j].delay-bounds[j]));
                        if(merit>best_merit) {
                            best_merit=merit;group.assign(1,index);
                            group.insert(group.end(),touching.begin(),touching.end());
                        }
                    }
                    if(group.size()<2) {++no_gain;continue;}
                } else {
                Net ideal;
                if(!shortest(nets[index],ideal,true,penalty)) break;
                if(diverse_proposals) {
                    std::vector<I> prices(vcount,0);
                    Net previous=ideal;
                    auto merit=[&](const Net& candidate) {
                        std::set<int> displaced;
                        for(int v:candidate.vertices) if(owner[v]>=0 && owner[v]!=candidate.id) displaced.insert(owner[v]);
                        return std::make_pair(displaced.size(),candidate.delay);
                    };
                    for(int option=0;option<2 && !expired();++option) {
                        for(int v:previous.vertices) prices[v]=add(prices[v],4);
                        Net alternate;
                        if(!shortest(nets[index],alternate,true,penalty,nullptr,nullptr,0,&prices)) break;
                        if(alternate.delay<nets[index].delay &&
                           (ideal.delay>=nets[index].delay || merit(alternate)<merit(ideal))) ideal=alternate;
                        previous=std::move(alternate);
                    }
                }
                if(eligibility_proposals && ideal.delay<nets[index].delay) {
                    auto displaced=[&](const Net& candidate) {
                        std::set<int> ids;
                        for(int v:candidate.vertices) if(owner[v]>=0 && owner[v]!=candidate.id) ids.insert(owner[v]);
                        return ids;
                    };
                    auto blockers=displaced(ideal);
                    if(blockers.size()>static_cast<std::size_t>(max_blockers)) {
                        std::vector<I> prices(vcount,0);
                        Net previous=ideal;
                        for(int option=0;option<escape_options && !expired();++option) {
                            auto avoid=displaced(previous);
                            for(const Net& n:nets) if(avoid.count(n.id))
                                for(int v:n.vertices) prices[v]=add(prices[v],escape_penalty);
                            Net alternate; ++eligibility_searches;
                            if(!shortest(nets[index],alternate,true,penalty,nullptr,nullptr,0,&prices)) break;
                            auto next=displaced(alternate);
                            if(alternate.delay<nets[index].delay &&
                               std::make_pair(next.size(),alternate.delay)<std::make_pair(blockers.size(),ideal.delay)) {
                                ideal=alternate;blockers=next;
                            }
                            previous=std::move(alternate);
                            if(blockers.size()<=static_cast<std::size_t>(max_blockers)) {++eligibility_recovered;used_escape=true;break;}
                        }
                    }
                }
                if(!donor_nets.empty()) {
                    const Net& donor=donor_nets[index];
                    auto merit=[&](const Net& candidate) {
                        std::set<int> displaced;
                        for(int v:candidate.vertices) if(owner[v]>=0 && owner[v]!=candidate.id) displaced.insert(owner[v]);
                        return std::make_pair(displaced.size(),candidate.delay);
                    };
                    if(donor.delay<nets[index].delay) ++donor_eligible;
                    if(donor.delay<nets[index].delay &&
                       (ideal.delay>=nets[index].delay || merit(donor)<merit(ideal))) {ideal=donor;used_donor=true;++donor_selected;}
                }
                if(ideal.delay>=nets[index].delay) { ++no_gain; continue; }
                std::set<int> blockers;
                for(int v:ideal.vertices) if(owner[v]>=0 && owner[v]!=nets[index].id)
                    blockers.insert(owner[v]);
                if(blockers.size()>static_cast<std::size_t>(max_blockers)) { ++too_many; continue; }
                ++attempts;
                for(std::size_t j=0;j<nets.size();++j)
                    if(blockers.count(nets[j].id)) group.push_back(static_cast<int>(j));
                }
                if(spatial_groups) ++attempts;
                int strategy=0;
                if(adaptive_groups && !(used_escape && escape_direct)) {
                    std::discrete_distribution<int> choose(neighborhood_weights.begin(),neighborhood_weights.end());
                    strategy=choose(group_rng);
                    if(strategy==1) {
                        // Include dependencies of displaced nets, not just the target's blockers.
                        for(std::size_t k=1;k<group.size() && group.size()<static_cast<std::size_t>(max_blockers+1) && !expired();++k) {
                            Net dependency;
                            if(!shortest(nets[group[k]],dependency,true,penalty)) break;
                            for(int v:dependency.vertices) if(owner[v]>=0) {
                                auto found=std::find_if(nets.begin(),nets.end(),[&](const Net& n){return n.id==owner[v];});
                                int candidate=static_cast<int>(found-nets.begin());
                                if(std::find(group.begin(),group.end(),candidate)==group.end()) group.push_back(candidate);
                                if(group.size()>=static_cast<std::size_t>(max_blockers+1)) break;
                            }
                        }
                    } else if(strategy==2) {
                        auto additions=order;std::shuffle(additions.begin(),additions.end(),group_rng);
                        std::size_t target=std::min(group.size()+3,static_cast<std::size_t>(max_blockers+1));
                        for(int candidate:additions) {
                            if(group.size()>=target) break;
                            if(std::find(group.begin(),group.end(),candidate)==group.end()) group.push_back(candidate);
                        }
                    }
                    ++neighborhood_attempts[strategy];
                }
                if(group.size()>13) ++large_group_attempts;
                if(used_escape) ++eligibility_attempts;
                ++group_sizes[std::min(group.size(),group_sizes.size()-1)];
                // Full transaction snapshot makes all failed/expired repairs reversible.
                auto snapshot_start=std::chrono::steady_clock::now();
                auto old_owner=owner;
                snapshot_s+=std::chrono::duration<double>(std::chrono::steady_clock::now()-snapshot_start).count();
                std::vector<Net> old;
                I before=0;
                for(int j:group) {
                    old.push_back(nets[j]); before=add(before,nets[j].delay);
                    for(int v:nets[j].vertices) owner[v]=-1;
                }
                bool legal=true; I after=0;
                if(seed_first_groups) legal=seed_first_repair(group,after,repair_rounds);
                else if(selection) legal=select_candidates(group,after);
                else if(negotiated) legal=negotiate(group,after,repair_rounds);
                else for(int j:group) {
                    Net candidate;
                    if(!shortest(nets[j],candidate)) { legal=false; break; }
                    for(int v:candidate.vertices) owner[v]=candidate.id;
                    after=add(after,candidate.delay); nets[j]=std::move(candidate);
                }
                bool accept_uphill=uphill && legal && after>=before && after-before<=before/100 && rng()%4==0;
                bool geometry_changed=false;
                if(accept_equal && legal && after==before) {
                    for(std::size_t k=0;k<group.size();++k) {
                        auto a=nets[group[k]].edges,b=old[k].edges;
                        std::sort(a.begin(),a.end());std::sort(b.begin(),b.end());
                        if(a!=b) {geometry_changed=true;break;}
                    }
                }
                if(neutral_tabu && geometry_changed) {
                    auto start=std::chrono::steady_clock::now();auto state=canonical_geometry(nets);
                    if(std::find(neutral_history.begin(),neutral_history.end(),state)!=neutral_history.end()) {geometry_changed=false;++neutral_tabu_rejections;}
                    neutral_tabu_s+=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
                }
                bool accept_neutral=accept_equal && legal && after==before && geometry_changed;
                if(adaptive_groups) {
                    double reward=legal && after<before?100.0*static_cast<double>(before-after)/static_cast<double>(before):0;
                    neighborhood_weights[strategy]=0.9*neighborhood_weights[strategy]+0.1*(0.1+reward);
                    if(reward>0) ++neighborhood_gains[strategy];
                }
                if(legal && (after<before || accept_uphill || accept_neutral)) {
                    if(group.size()>13 && after<before) {++large_group_strict;large_group_gain=add(large_group_gain,before-after);}
                    if(used_donor && after<before) ++donor_gains;
                    if(used_escape && after<before) {++eligibility_strict;eligibility_gain=add(eligibility_gain,before-after);}
                    if(used_escape && accept_neutral) ++eligibility_neutral;
                    ++accepted; changed=true;
                    if(accept_uphill) ++uphill_moves;
                    if(accept_neutral) ++neutral_moves;
                    if(neutral_tabu && after<before) neutral_history.clear();
                    remember_neutral_state();
                    current=add(current-before,after);
                    if(uphill && current<best) { best=current;best_nets=nets;best_owner=owner; }
                }
                else {
                    if(!legal) ++failed; else ++nonimproving;
                    if(used_escape) {if(!legal) ++eligibility_failed;else ++eligibility_nonimproving;}
                    owner=std::move(old_owner);
                    for(std::size_t k=0;k<group.size();++k) nets[group[k]]=std::move(old[k]);
                }
            }
            if(!changed) break;
        }
        if(uphill) {nets=std::move(best_nets);owner=std::move(best_owner);}
    }
    void remember_neutral_state() {
        if(!neutral_tabu || !accept_equal) return;
        auto start=std::chrono::steady_clock::now();
        auto state=canonical_geometry(nets);
        if(std::find(neutral_history.begin(),neutral_history.end(),state)==neutral_history.end()) {
            if(neutral_history.size()>=static_cast<std::size_t>(neutral_tabu)) neutral_history.erase(neutral_history.begin());
            neutral_history.push_back(std::move(state));
        }
        std::uint64_t bytes=0;for(const auto& saved:neutral_history) bytes+=saved.size()*sizeof(int);
        neutral_history_peak_bytes=std::max(neutral_history_peak_bytes,bytes);
        neutral_tabu_s+=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    }
    void restart(unsigned long long seed,int passes,bool polish_fresh=false) {
        random_ties=true;tie_seed=seed;
        std::mt19937_64 rng(seed);
        std::vector<int> group(nets.size());std::iota(group.begin(),group.end(),0);
        for(int pass=0;pass<passes && !expired();++pass) {
            ++fresh_attempts;
            for(std::size_t i=group.size();i>1;--i) std::swap(group[i-1],group[rng()%i]);
            auto old_nets=nets;auto old_owner=owner;
            I before=0;for(const Net& n:nets) before=add(before,n.delay);
            std::fill(owner.begin(),owner.end(),-1);
            for(Net& n:nets) {n.vertices.clear();n.edges.clear();n.delay=0;}
            I after=0;
            bool legal=negotiate(group,after,100);
            if(legal) {
                ++fresh_legal;
                if(polish_fresh) {
                    polish(seed+static_cast<unsigned long long>(pass),3,false);
                    after=0;for(const Net& n:nets) after=add(after,n.delay);
                }
            }
            if(legal && after<before) ++accepted;
            else {nets=std::move(old_nets);owner=std::move(old_owner);}
        }
    }
    void explore(unsigned long long seed,int passes,bool wide=false) {
        random_ties=true; tie_seed=seed;
        std::mt19937_64 rng(seed);
        std::vector<int> order(nets.size());std::iota(order.begin(),order.end(),0);
        std::vector<I> lower(nets.size()),area(nets.size());
        if(polish_order) for(std::size_t j=0;j<nets.size();++j) {
            lower[j]=relaxed_delay(nets[j]);
            int x0=nets[j].root%w,x1=x0,y0=(nets[j].root%wh)/w,y1=y0;
            for(int v:nets[j].sinks) {int x=v%w,y=(v%wh)/w;x0=std::min(x0,x);x1=std::max(x1,x);y0=std::min(y0,y);y1=std::max(y1,y);}
            area[j]=static_cast<I>(x1-x0+1)*(y1-y0+1);
        }
        for(int pass=0;pass<passes && !expired();++pass) {
            for(std::size_t i=order.size();i>1;--i) std::swap(order[i-1],order[rng()%i]);
            if(polish_order) {
                std::vector<long double> potential(nets.size());
                for(std::size_t j=0;j<nets.size();++j) {
                    I denominator=polish_order==1?area[j]:std::max<I>(1,lower[j]);
                    potential[j]=static_cast<long double>(std::max<I>(0,nets[j].delay-lower[j]))/denominator;
                }
                std::stable_sort(order.begin(),order.end(),[&](int a,int b){return potential[a]>potential[b];});
            }
            if(repair_first) repair(seed+static_cast<unsigned long long>(pass),1,4,true,false,wide?std::max(12,group_limit-1):4);
            for(int j:order) {
                ++polish_attempts;
                Net candidate;
                if(!shortest(nets[j],candidate)) break;
                ++polish_completed;
                if(candidate.delay<nets[j].delay) ++polish_improvements;
                if(candidate.delay>nets[j].delay) continue;
                for(int v:nets[j].vertices) owner[v]=-1;
                for(int v:candidate.vertices) owner[v]=nets[j].id;
                nets[j]=std::move(candidate);
            }
            if(!repair_first) repair(seed+static_cast<unsigned long long>(pass),1,4,true,false,wide?std::max(12,group_limit-1):4);
        }
    }
    std::string group_histogram() const {
        std::string result="[";
        for(std::size_t i=0;i<group_sizes.size();++i) {if(i) result+=",";result+=std::to_string(group_sizes[i]);}
        return result+"]";
    }
    void output() {
        if(!ablation_mode) std::cerr<<"{\"proposals\":"<<proposals<<",\"no_gain\":"<<no_gain
                 <<",\"too_many\":"<<too_many<<",\"attempts\":"<<attempts
                 <<",\"negotiation_rounds\":"<<negotiation_rounds<<",\"conflicted_rounds\":"<<conflicted_rounds
                 <<",\"fresh_attempts\":"<<fresh_attempts<<",\"fresh_legal\":"<<fresh_legal
                 <<",\"read_s\":"<<read_s<<",\"validation_s\":"<<validation_s<<",\"optimization_s\":"<<optimization_s
                 <<",\"search_reset_s\":"<<search_reset_s<<",\"search_rebuild_s\":"<<search_rebuild_s
                 <<",\"present_initial\":"<<negotiation.present_initial<<",\"present_step\":"<<negotiation.present_step<<",\"history_step\":"<<negotiation.history_step
                 <<",\"polish_order\":"<<polish_order<<",\"polish_attempts\":"<<polish_attempts<<",\"polish_completed\":"<<polish_completed<<",\"polish_improvements\":"<<polish_improvements
                 <<",\"repair_first\":"<<repair_first
                 <<",\"group_limit\":"<<group_limit<<",\"group_size_histogram\":"<<group_histogram()
                 <<",\"price_units\":"<<price_units
                 <<",\"snapshot_s\":"<<snapshot_s<<",\"negotiation_setup_s\":"<<negotiation_setup_s<<",\"negotiation_scan_s\":"<<negotiation_scan_s
                 <<",\"work_limit\":"<<work_limit<<",\"work_exhausted\":"<<work_exhausted
                 <<",\"expansions_per_second\":"<<(optimization_s>0?expansions/optimization_s:0)
                 <<",\"eligibility_searches\":"<<eligibility_searches<<",\"eligibility_recovered\":"<<eligibility_recovered
                 <<",\"eligibility_attempts\":"<<eligibility_attempts<<",\"eligibility_strict\":"<<eligibility_strict<<",\"eligibility_neutral\":"<<eligibility_neutral
                 <<",\"eligibility_failed\":"<<eligibility_failed<<",\"eligibility_nonimproving\":"<<eligibility_nonimproving<<",\"eligibility_gain\":"<<eligibility_gain
                 <<",\"escape_penalty\":"<<escape_penalty<<",\"escape_options\":"<<escape_options<<",\"escape_direct\":"<<escape_direct
                 <<",\"neutral_tabu\":"<<neutral_tabu<<",\"neutral_tabu_rejections\":"<<neutral_tabu_rejections<<",\"neutral_history_peak_bytes\":"<<neutral_history_peak_bytes<<",\"neutral_tabu_s\":"<<neutral_tabu_s
                 <<",\"tree_prices\":"<<tree_prices<<",\"flow_builds\":"<<flow_builds<<",\"flow_shared_vertices\":"<<flow_shared_vertices<<",\"flow_setup_s\":"<<flow_setup_s
                 <<",\"large_group_attempts\":"<<large_group_attempts<<",\"large_group_strict\":"<<large_group_strict<<",\"large_group_gain\":"<<large_group_gain
                 <<",\"repair_sampling\":"<<repair_sampling
                 <<",\"accept_equal\":"<<accept_equal<<",\"neutral_moves\":"<<neutral_moves
                 <<",\"uphill_moves\":"<<uphill_moves
                 <<",\"selection_nodes\":"<<selection_nodes<<",\"selection_complete\":"<<selection_complete
                 <<",\"selection_partial\":"<<selection_partial
                 <<",\"neighborhood_attempts\":["<<neighborhood_attempts[0]<<","<<neighborhood_attempts[1]<<","<<neighborhood_attempts[2]<<"]"
                 <<",\"neighborhood_gains\":["<<neighborhood_gains[0]<<","<<neighborhood_gains[1]<<","<<neighborhood_gains[2]<<"]"
                 <<",\"donor_eligible\":"<<donor_eligible<<",\"donor_selected\":"<<donor_selected<<",\"donor_gains\":"<<donor_gains
                 <<",\"group_size_2\":"<<group_sizes[2]<<",\"group_size_3\":"<<group_sizes[3]<<",\"group_size_13\":"<<group_sizes[13]
                 <<",\"failed\":"<<failed<<",\"nonimproving\":"<<nonimproving<<"}\n";
        I total=0; for(const Net& n:nets) total=add(total,n.delay);
        std::cout<<"M3DOUT1 "<<nets.size()<<" "<<total<<" "<<timed_out<<" "
                 <<accepted<<" "<<searches<<" "<<expansions<<"\n";
        for(const Net& n:nets) {
            std::cout<<n.id<<" "<<n.edges.size()<<" "<<n.delay<<"\n";
            for(auto [a,b]:n.edges) std::cout<<a<<" "<<b<<"\n";
        }
    }
};
int main(int argc,char**argv) {
    try {
        if(argc<5) throw std::runtime_error("usage: engine SECONDS SEED PASSES polish|search|repair");
        double seconds=std::stod(argv[1]);
        if(!std::isfinite(seconds) || seconds<0 || seconds>600) throw std::runtime_error("invalid budget");
        auto seed=std::stoull(argv[2]); int passes=std::stoi(argv[3]);
        if(passes<1 || passes>1000) throw std::runtime_error("invalid passes");
        const std::string mode=argv[4];
        const auto split=mode.rfind('_');
        const std::string kernel=split==std::string::npos?mode:mode.substr(0,split);
        const std::string operation=split==std::string::npos?"":mode.substr(split+1);
        const bool neighborhood_mode=(kernel=="fanout_astar" || kernel=="fanout_tight" || kernel=="fanout_fine") &&
                                     (operation=="escape" || operation=="shuffle" || operation=="diverse" || operation=="adaptive" || operation=="spatial" || operation=="hybrid" || operation=="donor" || operation=="window" || operation=="conflict");
        bool search_only=std::string(argv[4])=="search";
        if(!search_only && !neighborhood_mode && std::string(argv[4])!="polish" && std::string(argv[4])!="repair" && std::string(argv[4])!="repairsoft" && std::string(argv[4])!="ablation" && std::string(argv[4])!="negotiated" && std::string(argv[4])!="explore" && std::string(argv[4])!="restart" && std::string(argv[4])!="select" && std::string(argv[4])!="wide" && std::string(argv[4])!="walk" && std::string(argv[4])!="descent" && std::string(argv[4])!="compact" && std::string(argv[4])!="fanout" && std::string(argv[4])!="restart_fanout" && std::string(argv[4])!="restart_compact" && std::string(argv[4])!="restart_polish" && std::string(argv[4])!="fanout_walk" && std::string(argv[4])!="fanout_descent" && std::string(argv[4])!="astar" && std::string(argv[4])!="fanout_astar" && std::string(argv[4])!="fanout_gap" && std::string(argv[4])!="fanout_astar_gap" && std::string(argv[4])!="restart_fine" && std::string(argv[4])!="restart_astar" && std::string(argv[4])!="treecost" && std::string(argv[4])!="fanout_tight" && std::string(argv[4])!="astar_tight" && std::string(argv[4])!="fanout_fine") throw std::runtime_error("invalid mode");
        std::signal(SIGINT,on_signal); std::signal(SIGTERM,on_signal);
        Engine engine;
        if(argc>=6) {
            std::string limit=argv[5];
            if(limit.empty() || limit.find_first_not_of("0123456789")!=std::string::npos) throw std::runtime_error("invalid work limit");
            engine.work_limit=std::stoull(limit);
        }
        std::set<std::string> config_keys;
        for(int i=6;i<argc;++i) {
            std::string arg=argv[i]; auto split=arg.find('=');
            if(split==std::string::npos) throw std::runtime_error("expected key=value config");
            std::string key=arg.substr(0,split),value=arg.substr(split+1);
            if(!config_keys.insert(key).second || value.empty() || value.find_first_not_of("0123456789")!=std::string::npos)
                throw std::runtime_error("invalid or duplicate config");
            I number=std::stoll(value);
            if(number>64) throw std::runtime_error("config outside 0..64");
            if(key=="present_initial") engine.negotiation.present_initial=number;
            else if(key=="present_step") engine.negotiation.present_step=number;
            else if(key=="history_step") engine.negotiation.history_step=number;
            else if(key=="polish_order") {
                if(number>2) throw std::runtime_error("polish_order must be0..2");
                engine.polish_order=static_cast<int>(number);
            }
            else if(key=="repair_first") {
                if(number>1) throw std::runtime_error("repair_first must be0or1");
                engine.repair_first=number!=0;
            }
            else if(key=="repair_sampling") {
                if(number>2) throw std::runtime_error("repair_sampling must be0..2");
                engine.repair_sampling=static_cast<int>(number);
            }
            else if(key=="neutral_tabu") engine.neutral_tabu=static_cast<int>(number);
            else if(key=="tree_prices") {
                if(number>2) throw std::runtime_error("tree_prices must be0..2");
                engine.tree_prices=static_cast<int>(number);
            }
            else if(key=="escape_direct") {
                if(number>1) throw std::runtime_error("escape_direct must be0or1");
                engine.escape_direct=number!=0;
            }
            else if(key=="escape_penalty") engine.escape_penalty=number;
            else if(key=="escape_options") {
                if(number<1 || number>4) throw std::runtime_error("escape_options must be1..4");
                engine.escape_options=static_cast<int>(number);
            }
            else if(key=="accept_equal") {
                if(number>1) throw std::runtime_error("accept_equal must be0or1");
                engine.accept_equal=number!=0;
            }
            else if(key=="group_limit") {
                if(number<2 || number>64) throw std::runtime_error("group limit outside 2..64");
                engine.group_limit=static_cast<int>(number);
            }
            else throw std::runtime_error("unknown config key");
        }
        engine.deadline=std::chrono::steady_clock::now()+std::chrono::duration_cast<std::chrono::steady_clock::duration>(std::chrono::duration<double>(seconds));
        auto read_start=std::chrono::steady_clock::now();
        engine.read(search_only);
        engine.read_s=std::chrono::duration<double>(std::chrono::steady_clock::now()-read_start).count();
        if(operation=="donor") {
            Engine alternate; alternate.deadline=engine.deadline; alternate.read(false);
            if(alternate.w!=engine.w || alternate.h!=engine.h || alternate.l!=engine.l ||
               alternate.layer!=engine.layer || alternate.via!=engine.via || alternate.nets.size()!=engine.nets.size())
                throw std::runtime_error("donor instance mismatch");
            for(std::size_t j=0;j<engine.nets.size();++j)
                if(alternate.nets[j].id!=engine.nets[j].id || alternate.nets[j].root!=engine.nets[j].root || alternate.nets[j].sinks!=engine.nets[j].sinks)
                    throw std::runtime_error("donor terminals mismatch");
            engine.donor_nets=std::move(alternate.nets);
            engine.read_s=std::chrono::duration<double>(std::chrono::steady_clock::now()-read_start).count();
        }
        auto optimization_start=std::chrono::steady_clock::now();
        engine.ablation_mode=std::string(argv[4])=="ablation";
        if(neighborhood_mode) {
            engine.astar_search=true;engine.fanout_prices=true;
            engine.tight_heuristic=kernel=="fanout_tight" || kernel=="fanout_fine";
            engine.price_units=kernel=="fanout_fine"?16:1;
            engine.shuffled_groups=true;engine.group_rng.seed(seed^0x6a09e667f3bcc909ULL);
            engine.diverse_proposals=operation=="diverse" || operation=="hybrid";
            engine.eligibility_proposals=operation=="escape";
            engine.adaptive_groups=operation=="escape" || operation=="adaptive" || operation=="hybrid" || operation=="donor";
            engine.spatial_groups=operation=="spatial" || operation=="window";
            engine.seed_first_groups=operation=="window" || operation=="conflict";
            engine.conflict_windows=operation=="conflict";
            if(engine.conflict_windows) engine.gap_order=true;
            engine.explore(seed,passes,true);
        }
        else if(std::string(argv[4])=="fanout_fine") {engine.price_units=16;engine.tight_heuristic=true;engine.astar_search=true;engine.fanout_prices=true;engine.explore(seed,passes,true);}
        else if(std::string(argv[4])=="astar_tight") {engine.tight_heuristic=true;engine.astar_search=true;engine.polish(seed,passes,false);}
        else if(std::string(argv[4])=="fanout_tight") {engine.tight_heuristic=true;engine.astar_search=true;engine.fanout_prices=true;engine.explore(seed,passes,true);}
        else if(std::string(argv[4])=="treecost") {engine.discounted_groups=true;engine.astar_search=true;engine.fanout_prices=true;engine.explore(seed,passes,true);}
        else if(std::string(argv[4])=="fanout_astar_gap") {engine.gap_order=true;engine.astar_search=true;engine.fanout_prices=true;engine.explore(seed,passes,true);}
        else if(std::string(argv[4])=="restart_fine") {engine.price_units=16;engine.tight_heuristic=true;engine.astar_search=true;engine.fanout_prices=true;engine.restart(seed,passes,true);}
        else if(std::string(argv[4])=="restart_astar") {engine.astar_search=true;engine.fanout_prices=true;engine.restart(seed,passes,true);}
        else if(std::string(argv[4])=="fanout_gap") {engine.gap_order=true;engine.fanout_prices=true;engine.explore(seed,passes,true);}
        else if(std::string(argv[4])=="astar") {engine.astar_search=true;engine.polish(seed,passes,false);}
        else if(std::string(argv[4])=="fanout_astar") {engine.astar_search=true;engine.fanout_prices=true;engine.explore(seed,passes,true);}
        else if(engine.ablation_mode) engine.ablation();
        else if(std::string(argv[4])=="restart_polish") {
            engine.fanout_prices=true;engine.restart(seed,passes,true);
        }
        else if(std::string(argv[4])=="restart_fanout" || std::string(argv[4])=="restart_compact") {
            engine.fanout_prices=std::string(argv[4])=="restart_fanout";
            engine.compact_groups=std::string(argv[4])=="restart_compact";
            engine.restart(seed,passes);
        }
        else if(std::string(argv[4])=="compact" || std::string(argv[4])=="fanout") {
            engine.compact_groups=std::string(argv[4])=="compact";
            engine.fanout_prices=std::string(argv[4])=="fanout";
            engine.explore(seed,passes,true);
        }
        else if(std::string(argv[4])=="fanout_walk" || std::string(argv[4])=="fanout_descent") {
            engine.fanout_prices=true;engine.random_ties=true;engine.tie_seed=seed;
            engine.repair(seed,passes,4,true,false,12,std::string(argv[4])=="fanout_walk");
        }
        else if(std::string(argv[4])=="descent") {
            engine.random_ties=true;engine.tie_seed=seed;engine.repair(seed,passes,4,true,false,12,false);
        }
        else if(std::string(argv[4])=="walk") {
            engine.random_ties=true;engine.tie_seed=seed;engine.repair(seed,passes,4,true,false,12,true);
        }
        else if(std::string(argv[4])=="wide") engine.explore(seed,passes,true);
        else if(std::string(argv[4])=="select") {
            engine.random_ties=true;engine.tie_seed=seed;engine.repair(seed,passes,4,false,true);
        }
        else if(std::string(argv[4])=="restart") engine.restart(seed,passes);
        else if(std::string(argv[4])=="explore") engine.explore(seed,passes);
        else if(std::string(argv[4])=="negotiated") engine.repair(seed,passes,4,true);
        else if(std::string(argv[4])=="repair" || std::string(argv[4])=="repairsoft")
            engine.repair(seed,passes,std::string(argv[4])=="repairsoft"?4:0);
        else engine.polish(seed,passes,search_only);
        engine.optimization_s=std::chrono::duration<double>(std::chrono::steady_clock::now()-optimization_start).count();
        engine.output();
        return 0;
    } catch(const std::exception& e) { std::cerr<<e.what()<<"\n"; return 2; }
}
