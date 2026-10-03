import unittest
from test_exact import make
from component_reuse import ReuseRouter
from run_polish import Submission,check
from branch_repair import Limit
class Reuse(unittest.TestCase):
 def test_reused_vertices_remove_price_not_delay(self):
  inst,sub=make(3,1,[2],1,(0,0,0),[(2,0,0)])
  r=ReuseRouter(inst,sub,1000,5,1);prices={(1,0,0):10}
  a=r.connect_pair(0,(0,0,0),(2,0,0),1,prices,set());b=r.connect_pair(0,(0,0,0),(2,0,0),1,prices,{(1,0,0)})
  self.assertEqual(a[0],28);self.assertEqual(b[0],8)
 def test_merge_projection_is_legal_and_physical(self):
  inst,sub=make(3,3,[1],1,(0,0,0),[(2,0,0),(2,2,0)])
  for flag in [False,True]:
   r=ReuseRouter(inst,sub,100000,5,1);tree=r.build_reuse(0,{},flag);result=check(inst,Submission(inst.name,[tree]));self.assertTrue(result.legal);self.assertGreaterEqual(result.total_delay,6)
 def test_budget_interrupt_preserves_input(self):
  inst,sub=make(5,5,[1],1,(0,0,0),[(4,4,0)])
  r=ReuseRouter(inst,sub,1,5,1);before=dict(r.owner)
  with self.assertRaises(Limit):r.build_reuse(0,{},True)
  self.assertEqual(r.owner,before)
if __name__=='__main__':unittest.main()
