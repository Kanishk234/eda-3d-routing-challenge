"""Crossover hypotheses; retain pure parent controls for attribution."""
from evolution_pilot import mutation as ordering
from evolution_basin_mutation import mutation as basin

def mutation(source,kind):
 if kind=='control':return source
 if kind in ('flow_conflict_first','conflict_last','delayed_conflict_first'):return ordering(source,kind)
 if kind in ('fine_anneal','fine_uphill'):return basin(source,kind)
 if kind in ('fine_anneal_neutral','fine_uphill_neutral','delayed_anneal_neutral'):
  if kind=='delayed_anneal_neutral':source=ordering(source,'delayed_conflict_first')
  operator='fine_uphill' if kind=='fine_uphill_neutral' else 'fine_anneal'
  result=basin(source,operator);anchor='if(uphill && current<best) { best=current;best_nets=nets;best_owner=owner; }';assert result.count(anchor)==1
  return result.replace(anchor,anchor.replace('current<best','current<=best'))
 combinations={'flow_anneal':('flow_conflict_first','fine_anneal'),'last_anneal':('conflict_last','fine_anneal'),'flow_uphill':('flow_conflict_first','fine_uphill')}
 assert kind in combinations
 a,b=combinations[kind]
 return basin(ordering(source,a),b)
