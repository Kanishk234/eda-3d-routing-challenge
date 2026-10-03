import unittest
from test_exact import make
from fresh_negotiation import construct
from run_polish import check
S=dict(initial=.05,multiplier=1.03,cap=3,history=.05,fanout_power=.5)
class Fresh(unittest.TestCase):
 def test_physical_cost(self):
  inst,_=make(5,5,[6,2],3,(0,0,0),[(4,4,0)])
  out,stats=construct(inst,1,10000,5,S,2);self.assertTrue(check(inst,out).legal);self.assertEqual(check(inst,out).total_delay,22)
 def test_work_limit_no_conflicting_output(self):
  inst,_=make(5,5,[1],1,(0,0,0),[(4,4,0)])
  out,stats=construct(inst,1,1,5,S,2);self.assertIsNone(out);self.assertTrue(stats['limited']);self.assertEqual(stats['expansions'],1)
 def test_conflict_only_stops_on_legal_state(self):
  inst,_=make(5,5,[1],1,(0,0,0),[(4,4,0)])
  out,stats=construct(inst,1,10000,5,dict(S,conflict_only=True,full_every=10),20)
  self.assertTrue(check(inst,out).legal);self.assertEqual(len(stats['rounds']),1)
 def test_fixed_work_determinism(self):
  inst,_=make(5,5,[1,2],3,(0,0,0),[(4,4,0)])
  a,_=construct(inst,2,10000,5,S,3);b,_=construct(inst,2,10000,5,S,3);self.assertEqual(a.to_dict(),b.to_dict())
if __name__=='__main__':unittest.main()
