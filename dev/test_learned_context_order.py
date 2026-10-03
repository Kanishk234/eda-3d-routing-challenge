import unittest
from learned_context_order import curriculum,new_router,context,features,fit_linear,run_policy,follow
from test_exact import make
from run_polish import Submission,check
class ContextPolicy(unittest.TestCase):
 def test_curriculum_preserves_terminals(self):
  inst=curriculum(2001);self.assertEqual({p.id for p in inst.pins},{p for n in inst.nets for p in n.pins()})
 def test_features_respond_to_occupancy(self):
  inst,_=make(5,5,[1],1,(0,0,0),[(4,4,0)])
  r=new_router(inst);base=features(inst);a=context(r,[0],base)[0];r.owner[(2,2,0)]=99;b=context(r,[0],base)[0]
  self.assertEqual(len(a),16);self.assertGreater(b[9],a[9])
 def test_fit_known_pairwise_direction(self):
  w=fit_linear([({0:[1.0]*16,1:[0.0]*16},0)],10);self.assertGreater(sum(w),0)
 def test_policy_limit_and_hand_cost(self):
  inst,_=make(5,5,[6,2],3,(0,0,0),[(4,4,0)])
  model=dict(context_weights=[0]*16,static_weights=[0]*9)
  out,stats=run_policy(inst,'context_linear',model,1,1,5);self.assertIsNone(out);self.assertTrue(stats['limited'])
  out,stats=run_policy(inst,'context_linear',model,1,10000,5);self.assertTrue(check(inst,out).legal);self.assertEqual(stats['delay'],22)
 def test_teacher_has_complete_legal_routes(self):
  inst,_=make(3,3,[1],1,(0,0,0),[(2,2,0)])
  examples=[];stats={};r=follow(inst,[0],examples,stats);self.assertTrue(check(inst,Submission(inst.name,list(r.routes.values()))).legal);self.assertEqual(len(examples),1);self.assertGreater(stats['expansions'],0)
if __name__=='__main__':unittest.main()
