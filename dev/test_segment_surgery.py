"""Hand-check root labels, downstream accounting and preserved components."""
import unittest
from test_exact import make
from segment_surgery import SurgeryRouter,PricedBranchRouter
from branch_repair import Limit
from run_polish import Submission,NetRoute,check

class Segment(unittest.TestCase):
 def fixture(self):
  edges=[((0,1,0),(0,0,0)),((0,1,0),(1,1,0)),((1,1,0),(2,1,0)),((2,1,0),(3,1,0)),((3,1,0),(4,1,0)),((3,1,0),(3,2,0))]
  inst,sub=make(5,3,[1],1,(0,1,0),[(0,0,0),(4,1,0),(3,2,0)],own_edges=edges);return inst,sub
 def test_preserves_downstream_and_counts_both_sinks(self):
  inst,sub=self.fixture();r=SurgeryRouter(inst,sub,10000,5,1);retained,sinks,removed=r.retained(0,{(2,1,0)},False);plan=r.segment_plans[0];self.assertEqual(plan['downstream_sinks'],2);self.assertEqual(removed,2)
  for v in set(r.owner)-r.vertices(retained):r.owner.pop(v)
  tree=r.search(0,sinks,retained,{(2,1,0)});out=check(inst,Submission(inst.name,[tree]));self.assertTrue(out.legal);self.assertEqual(out.total_delay,13);self.assertEqual(check(inst,sub).total_delay,9)
  self.assertTrue(set(plan['down_edges'])<=set(tree.edges));self.assertEqual(r.tree(tree)[1][(3,1,0)],5)
 def test_junction_uses_existing_branch_fallback(self):
  inst,sub=self.fixture();r=SurgeryRouter(inst,sub,10000,5,1);r.retained(0,{(3,1,0)},False);self.assertNotIn(0,r.segment_plans);self.assertEqual(r.stats['segment_fallbacks'],1)
 def test_work_limit_preserves_original_route(self):
  inst,sub=self.fixture();r=SurgeryRouter(inst,sub,1,5,1);before=sub.to_dict();out=r.run('branch',100);self.assertTrue(check(inst,out).legal);self.assertEqual(out.to_dict(),before)
class PricedProposal(unittest.TestCase):
 def test_penalty_guides_geometry_without_changing_physical_score(self):
  path=[(0,1,0),(0,1,1),(1,1,1),(2,1,1),(2,1,0)]
  inst,sub=make(3,3,[1,1],1,path[0],[path[-1]],block=((1,0,0),(1,2,0)),own_edges=list(zip(path,path[1:])))
  sub.routes[1]=NetRoute(1,[((1,0,0),(1,1,0)),((1,1,0),(1,2,0))]);self.assertTrue(check(inst,sub).legal)
  r=PricedBranchRouter(inst,sub,10000,5,1,proposal_penalties=[4]);tree=r.search(0,[path[-1]],NetRoute(0,[]),set(),True);out=Submission(inst.name,[tree,sub.routes[1]])
  self.assertTrue(check(inst,out).legal);self.assertEqual(check(inst,out).total_delay,6);self.assertNotIn((1,1,0),r.vertices(tree));self.assertEqual(r.stats['proposal_price_4'],1)

if __name__=='__main__':unittest.main()
