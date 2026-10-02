"""Independent legality, physical distance and interruption checks."""
import unittest
from test_exact import make,reference
from branch_repair import Router,Limit
from generate_tree_candidates import priced_tree,attachment_tree
from run_polish import Submission,check

class CandidateTrees(unittest.TestCase):
    def test_physical_distance_and_foreign_terminals(self):
        inst,sub=make(5,5,[6,2],3,(0,0,0),[(4,4,0)],block=((2,2,0),(2,3,0)))
        router=Router(inst,sub,10000,5,1);tree=priced_tree(router,0,0)
        result=next(n for n in check(inst,Submission(inst.name,[tree])).nets if n.net==0)
        self.assertTrue(result.legal);expected,_=reference(inst,(0,0,0),[(4,4,0)],{(2,2,0),(2,3,0)})
        self.assertEqual(result.delay,expected)

    def test_work_limit(self):
        inst,sub=make(5,5,[1],1,(0,0,0),[(4,4,0)])
        router=Router(inst,sub,1,5,1)
        with self.assertRaises(Limit):priced_tree(router,0,0)
        self.assertEqual(router.expansions,1)

    def test_attachment_physical_cost_and_work_limit(self):
        inst,sub=make(3,3,[1],1,(0,0,0),[(2,0,0),(2,2,0)])
        for scale in [8,12,16]:
            router=Router(inst,sub,1000,5,1);tree=attachment_tree(router,0,0,scale)
            result=check(inst,Submission(inst.name,[tree]));self.assertTrue(result.legal)
            self.assertEqual(result.total_delay,6)
        router=Router(inst,sub,1,5,1)
        with self.assertRaises(Limit):attachment_tree(router,0,0,16)

if __name__=='__main__':unittest.main(verbosity=2)
