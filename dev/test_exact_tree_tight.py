"""Independent hand-cost and sound restricted optimality checks."""
import unittest
from test_exact import make
from branch_repair import Router
from exact_tree_repair import solve_trees as original
from exact_tree_repair_tight import solve_trees as refined
from run_polish import check,Submission,NetRoute
class TightTree(unittest.TestCase):
 def test_two_sink_cost_matches_hand_optimum(self):
  edges=[((x,0,0),(x+1,0,0)) for x in range(4)]+[((0,y,0),(0,y+1,0)) for y in range(4)]
  inst,sub=make(5,5,[1],1,(0,0,0),[(4,0,0),(0,4,0)],own_edges=edges)
  router=Router(inst,sub,10000,5,1);vertices={(x,y,0) for x in range(5) for y in range(5)}
  for solve in (original,refined):
   trees,stats=solve(router,[0],vertices,5,1);self.assertEqual(stats['status'],'OPTIMAL');self.assertEqual(stats['objective'],8);self.assertEqual(check(inst,Submission(inst.name,list(trees.values()))).total_delay,8)
 def test_no_gain_proof_retains_parent(self):
  path=[(0,0,0),(1,0,0),(2,0,0),(3,0,0),(3,1,0),(3,2,0),(3,3,0)]
  inst,sub=make(4,4,[1],1,path[0],[path[-1]],own_edges=list(zip(path,path[1:])))
  router=Router(inst,sub,10000,5,1);vertices={(x,y,0) for x in range(4) for y in range(4)};trees,stats=refined(router,[0],vertices,5,1,strict=True)
  self.assertFalse(trees);self.assertTrue(stats['proved_no_improvement']);self.assertEqual(stats['bound'],6);self.assertTrue(check(inst,sub).legal)
 def test_two_net_matches_independent_path_model(self):
  from exact_pair_repair import solve_paths
  inst,sub=make(3,2,[1],1,(0,0,0),[(2,0,0)],block=((0,1,0),(1,1,0)),own_edges=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0))])
  router=Router(inst,sub,10000,5,1);vertices={(x,y,0) for x in range(3) for y in range(2)}
  a,sa=solve_paths(router,[0,1],vertices,5,1,True);b,sb=refined(router,[0,1],vertices,5,1)
  self.assertEqual(sa['objective'],sb['objective']);self.assertEqual(sb['objective'],3)
 def test_improves_slow_layer_tree(self):
  path=[(x,0,0) for x in range(5)];inst,sub=make(5,1,[6,2],3,path[0],[path[-1]],own_edges=list(zip(path,path[1:])))
  router=Router(inst,sub,10000,5,1);out,stats=refined(router,[0],{(x,0,z) for x in range(5) for z in range(2)},5,1,strict=True)
  self.assertTrue(stats['restricted_optimal']);self.assertEqual(check(inst,Submission(inst.name,list(out.values()))).total_delay,14)

class CompetingTree(unittest.TestCase):
 def test_contested_two_layer_multi_sink_hand_optimum(self):
  a=[(0,1,0),(0,1,1),(1,1,1),(2,1,1),(2,1,0),(2,0,0)]
  inst,sub=make(3,3,[1,1],1,a[0],[(2,1,0),(2,0,0)],block=((1,0,0),(1,2,0)),own_edges=list(zip(a,a[1:])))
  sub.routes[1]=NetRoute(1,[((1,0,0),(1,1,0)),((1,1,0),(1,2,0))])
  self.assertTrue(check(inst,sub).legal);self.assertEqual(check(inst,sub).total_delay,11)
  router=Router(inst,sub,10000,5,1);vertices={(x,y,z) for x in range(3) for y in range(3) for z in range(2)}
  # Independent lower bound7 cannot be jointly routed (crossing at center).
  # Bipartite unit grid detours add even delay; explicit construction costs9.
  for solve in (original,refined):
   out,stats=solve(router,[0,1],vertices,5,1);self.assertTrue(stats['restricted_optimal']);self.assertEqual(stats['objective'],9);self.assertEqual(check(inst,Submission(inst.name,list(out.values()))).total_delay,9)

if __name__=='__main__':unittest.main()
