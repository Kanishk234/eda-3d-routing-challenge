"""Independent physical-cost and rollback checks for neural corridor proposals."""
import unittest
from test_exact import make,reference
from branch_repair import Router,Limit
from rest_proposals import template,tree_with_template
from run_polish import Submission,check

class Proposals(unittest.TestCase):
    def test_l_corridor(self):
        self.assertEqual(template([(0,0),(2,2)],[0,1]),{(0,0),(0,1),(0,2),(1,2),(2,2)})

    def test_primary_delay_matches_independent_dijkstra(self):
        inst,sub=make(5,5,[6,2],3,(0,0,0),[(4,4,0),(2,3,0)])
        r=Router(inst,sub,10000,5,1)
        tree=tree_with_template(r,0,{(0,0),(4,4)},0)
        result=check(inst,Submission(inst.name,[tree]))
        self.assertTrue(result.legal)
        expected,_=reference(inst,(0,0,0),[(4,4,0),(2,3,0)],set())
        self.assertEqual(result.total_delay,expected)

    def test_limit_preserves_ownership(self):
        inst,sub=make(5,5,[1],1,(0,0,0),[(4,4,0)])
        r=Router(inst,sub,1,5,1);before=dict(r.owner)
        with self.assertRaises(Limit):tree_with_template(r,0,set(),0)
        self.assertEqual(r.owner,before)

if __name__=='__main__':unittest.main()
