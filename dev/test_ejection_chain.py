import unittest
from test_exact import make
from branch_repair import Router
from ejection_chain import attempt
from run_polish import check,Submission
class Chain(unittest.TestCase):
    def fixture(self,work):
        path=[(0,0,0),(0,1,0),(1,1,0),(2,1,0),(2,0,0)]
        inst,sub=make(3,3,[1],1,path[0],[path[-1]],block=((0,2,0),(1,2,0)),own_edges=list(zip(path,path[1:])))
        return inst,sub,Router(inst,sub,work,5,1)
    def test_strict_gain_official_objective(self):
        for entry in [False,True]:
            inst,sub,r=self.fixture(10000);result=attempt(r,0,3,16,entry)
            self.assertTrue(result['accepted']);self.assertEqual(result['gain'],2)
            self.assertEqual(check(inst,Submission(inst.name,list(r.routes.values()))).total_delay,3)
    def test_interrupt_restores_routes_and_owner(self):
        inst,sub,r=self.fixture(1);owner=r.owner.copy();routes=r.routes.copy();result=attempt(r,0,3,16,True)
        self.assertTrue(result['limited']);self.assertEqual(owner,r.owner);self.assertEqual(routes,r.routes)
    def test_cap_failure_never_damages_legal_state(self):
        inst,sub,r=self.fixture(10000);result=attempt(r,0,1,0,True)
        self.assertTrue(check(inst,Submission(inst.name,list(r.routes.values()))).legal)
if __name__=='__main__':unittest.main()
