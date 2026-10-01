// Exact single-net shortest-path rerouting. Original implementation; C++17.
// Official JSON/checking remains in Python. Input is a versioned integer bridge.
#include <algorithm>
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
#include <vector>

using I = std::int64_t;
constexpr I INF = std::numeric_limits<I>::max()/4;
volatile std::sig_atomic_t stopped = 0;
void on_signal(int) { stopped = 1; }
I add(I a, I b) {
    if (b < 0 || a < 0 || a > INF-b) throw std::runtime_error("delay overflow");
    return a+b;
}
struct Net {
    int id, root;
    std::vector<int> sinks, vertices;
    std::vector<std::pair<int,int>> edges;
    I delay=0;
};
struct Engine {
    int w,h,l,vcount,wh;
    I via;
    std::vector<I> layer;
    std::vector<Net> nets;
    std::vector<int> owner,pin_owner,parent;
    std::vector<I> dist;
    std::chrono::steady_clock::time_point deadline;
    std::uint64_t searches=0, expansions=0, accepted=0;
    bool timed_out=false;
    std::uint64_t proposals=0,no_gain=0,too_many=0,attempts=0,failed=0,nonimproving=0;

    bool expired() {
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
        std::vector<std::vector<std::pair<int,I>>> adj(vcount);
        for(auto [a,b]:net.edges) {
            I cost=weight(a,b);
            adj[a].push_back({b,cost}); adj[b].push_back({a,cost});
        }
        std::vector<I> costs(vcount,INF);
        std::queue<int> q;
        q.push(net.root); costs[net.root]=0;
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
        for(int s:net.sinks) total=add(total,costs[s]);
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
            n.delay=validate_tree(n);
            for(int v:n.vertices) {
                if(owner[v]!=-1) throw std::runtime_error("shared routing vertex");
                owner[v]=n.id;
            }
        }
    }
    bool shortest(const Net& n,Net& proposed,bool ignore_owners=false,I occupancy_penalty=0) {
        ++searches;
        if(expired()) return false;
        std::fill(dist.begin(),dist.end(),INF);
        std::fill(parent.begin(),parent.end(),-1);
        std::vector<char> is_sink(vcount,0);
        for(int s:n.sinks) is_sink[s]=1;
        int left=static_cast<int>(n.sinks.size());
        using Node=std::pair<I,int>;
        std::priority_queue<Node,std::vector<Node>,std::greater<Node>> q;
        dist[n.root]=0; q.push({0,n.root});
        while(!q.empty() && left) {
            auto [cost,u]=q.top(); q.pop();
            if(cost!=dist[u]) continue;
            ++expansions;
            if((expansions&1023)==0 && expired()) return false;
            if(is_sink[u]) { is_sink[u]=0; --left; }
            neighbors(u,[&](int v,I delay){
                if((!ignore_owners && owner[v]>=0 && owner[v]!=n.id) ||
                   (pin_owner[v]>=0 && pin_owner[v]!=n.id)) return;
                I extra=(ignore_owners && owner[v]>=0 && owner[v]!=n.id)?occupancy_penalty:0;
                I next=add(add(cost,delay),extra);
                if(next<dist[v]) { dist[v]=next; parent[v]=u; q.push({next,v}); }
            });
        }
        if(left || expired()) return false;
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
        return true;
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
    void repair(unsigned long long seed,int passes,I penalty=0) {
        std::mt19937_64 rng(seed);
        std::vector<int> order(nets.size()); std::iota(order.begin(),order.end(),0);
        for(int pass=0;pass<passes && !expired();++pass) {
            for(std::size_t i=order.size();i>1;--i) std::swap(order[i-1],order[rng()%i]);
            bool changed=false;
            for(int index:order) {
                if(expired()) break;
                ++proposals; Net ideal;
                if(!shortest(nets[index],ideal,true,penalty)) break;
                if(ideal.delay>=nets[index].delay) { ++no_gain; continue; }
                std::set<int> blockers;
                for(int v:ideal.vertices) if(owner[v]>=0 && owner[v]!=nets[index].id)
                    blockers.insert(owner[v]);
                if(blockers.size()>4) { ++too_many; continue; }
                ++attempts;
                std::vector<int> group{index};
                for(std::size_t j=0;j<nets.size();++j)
                    if(blockers.count(nets[j].id)) group.push_back(static_cast<int>(j));
                // Full transaction snapshot makes all failed/expired repairs reversible.
                auto old_owner=owner;
                std::vector<Net> old;
                I before=0;
                for(int j:group) {
                    old.push_back(nets[j]); before=add(before,nets[j].delay);
                    for(int v:nets[j].vertices) owner[v]=-1;
                }
                bool legal=true; I after=0;
                for(int j:group) {
                    Net candidate;
                    if(!shortest(nets[j],candidate)) { legal=false; break; }
                    for(int v:candidate.vertices) owner[v]=candidate.id;
                    after=add(after,candidate.delay); nets[j]=std::move(candidate);
                }
                if(legal && after<before) { ++accepted; changed=true; }
                else {
                    if(!legal) ++failed; else ++nonimproving;
                    owner=std::move(old_owner);
                    for(std::size_t k=0;k<group.size();++k) nets[group[k]]=std::move(old[k]);
                }
            }
            if(!changed) break;
        }
    }
    void output() {
        std::cerr<<"{\"proposals\":"<<proposals<<",\"no_gain\":"<<no_gain
                 <<",\"too_many\":"<<too_many<<",\"attempts\":"<<attempts
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
        if(argc!=5) throw std::runtime_error("usage: engine SECONDS SEED PASSES polish|search|repair");
        double seconds=std::stod(argv[1]);
        if(!std::isfinite(seconds) || seconds<0 || seconds>600) throw std::runtime_error("invalid budget");
        auto seed=std::stoull(argv[2]); int passes=std::stoi(argv[3]);
        if(passes<1 || passes>100) throw std::runtime_error("invalid passes");
        bool search_only=std::string(argv[4])=="search";
        if(!search_only && std::string(argv[4])!="polish" && std::string(argv[4])!="repair" && std::string(argv[4])!="repairsoft") throw std::runtime_error("invalid mode");
        std::signal(SIGINT,on_signal); std::signal(SIGTERM,on_signal);
        Engine engine;
        engine.deadline=std::chrono::steady_clock::now()+std::chrono::duration_cast<std::chrono::steady_clock::duration>(std::chrono::duration<double>(seconds));
        engine.read(search_only);
        if(std::string(argv[4])=="repair" || std::string(argv[4])=="repairsoft")
            engine.repair(seed,passes,std::string(argv[4])=="repairsoft"?4:0);
        else engine.polish(seed,passes,search_only);
        engine.output();
        return 0;
    } catch(const std::exception& e) { std::cerr<<e.what()<<"\n"; return 2; }
}
