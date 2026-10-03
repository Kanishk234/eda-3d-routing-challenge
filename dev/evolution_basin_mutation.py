"""Refine the existing fine-price repair engine with bounded uphill search.
Physical scoring and best-legal restoration remain the incumbent authority.
"""
def mutation(source,kind):
 if kind=='control':return source
 assert kind in ('fine_uphill','fine_anneal','fine_anneal_warm')
 anchor='repair(seed+static_cast<unsigned long long>(pass),1,4,true,false,wide?std::max(12,group_limit-1):4);'
 assert source.count(anchor)==2
 candidate=source.replace(anchor,anchor[:-2]+',true);')
 acceptance='                bool accept_uphill=uphill && legal && after>=before && after-before<=before/100 && rng()%4==0;'
 assert candidate.count(acceptance)==1
 if kind=='fine_uphill':
  replacement='                bool accept_uphill=uphill && legal && after>before && after-before<=before/100 && rng()%4==0;'
 else:
  scale='0.005' if kind=='fine_anneal_warm' else '0.002'
  replacement='''                double work_phase=work_limit?std::min(1.0,static_cast<double>(expansions)/work_limit):0.5;
                double temperature=std::max(1.0,SCALE*before*(1.0-work_phase)*(1.0-work_phase));
                bool accept_uphill=uphill && legal && after>before && after-before<=before/50 &&
                    static_cast<double>(rng()%1000000)/1000000.0<std::exp(-static_cast<double>(after-before)/temperature);'''.replace('SCALE',scale)
 candidate=candidate.replace(acceptance,replacement)
 return candidate
