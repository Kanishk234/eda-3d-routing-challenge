"""Small independent physical-delay checks for fresh component construction."""
import unittest
from test_exact import make
from component_router import ComponentRouter
from run_polish import check

class Components(unittest.TestCase):
    def test_hand_delay_and_legal_projection(self):
        inst,sub=make(3,3,[1],2,(0,0,0),[(2,0,0),(2,2,0)])
        for method in ['merge','star']:
            router=ComponentRouter(inst,sub,10000,5,1);out=router.construct(method,2)
            self.assertIsNotNone(out);result=check(inst,out);self.assertTrue(result.legal)
            self.assertEqual(result.total_delay,6)

    def test_empty_construction_budget_returns_no_route(self):
        inst,sub=make(5,5,[6,2],3,(0,0,0),[(4,4,0)])
        router=ComponentRouter(inst,sub,1,5,1)
        self.assertIsNone(router.construct('merge',2));self.assertEqual(router.expansions,1)

    def test_fresh_construction_ignores_warm_start_geometry(self):
        path=[(0,0,0),(0,1,0),(1,1,0),(2,1,0),(2,0,0)]
        inst,a=make(3,3,[1],1,path[0],[path[-1]])
        _,b=make(3,3,[1],1,path[0],[path[-1]],own_edges=list(zip(path,path[1:])))
        results=[ComponentRouter(inst,s,1000,5,2).construct('merge',2).to_dict() for s in [a,b]]
        self.assertEqual(*results)

if __name__=='__main__':unittest.main(verbosity=2)
