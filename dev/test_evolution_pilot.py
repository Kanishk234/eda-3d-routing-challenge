"""Check source isolation and score-ratio comparison independently."""
import math,unittest
from evolution_pilot import mutation,compare

class Evolution(unittest.TestCase):
 def test_control_is_identical_and_mutations_are_local(self):
  parent='before\n            if(shuffled_groups) std::shuffle(routing_order.begin(),routing_order.end(),group_rng);\nafter\n'
  self.assertEqual(mutation(parent,'control'),parent)
  for variant,op in [('conflict_first','>'),('conflict_last','<')]:
   candidate=mutation(parent,variant);self.assertTrue(candidate.startswith('before\n'));self.assertTrue(candidate.endswith('\nafter\n'));self.assertIn('conflict_debt[a] '+op+' conflict_debt[b]',candidate)
  self.assertNotIn('conflict_debt',parent)
 def test_score_ratio_does_not_use_sum_delay(self):
  rows=[dict(variant=v,tier='hard',case=c,seed=1,delay=d) for v,c,d in [('control','small',100),('trial','small',80),('control','large',1000),('trial','large',1050)]]
  r=compare(rows,'trial');self.assertEqual((r['wins'],r['losses']),(1,1));self.assertGreater(r['geomean_score_ratio'],1);self.assertAlmostEqual(r['geomean_score_ratio'],math.sqrt((100/80)*(1000/1050)))
  # Total delay got worse, but the geometric mean case score improved.
  self.assertGreater(80+1050,100+1000)
 def test_mutation_requires_unique_anchor(self):
  with self.assertRaises(AssertionError):mutation('no anchor','conflict_first')

if __name__=='__main__':unittest.main()
