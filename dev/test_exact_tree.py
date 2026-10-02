"""Independent sink-delay and tree legality checks for the distance model."""
import unittest
from test_exact import make
from branch_repair import Router
from exact_tree_repair import solve_trees
from exact_pair_repair import solve_paths
from run_polish import Submission,check

class ExactTree(unittest.TestCase):
    def test_shared_trunk_counted_per_sink(self):
        edges=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0)),((2,0,0),(2,1,0)),((2,1,0),(2,2,0))]
        inst,sub=make(3,3,[1],1,(0,0,0),[(2,0,0),(2,2,0)],own_edges=edges)
        router=Router(inst,sub,10000,5,1);out,stats=solve_trees(router,[0],{(x,y,0) for x in range(3) for y in range(3)},2,1)
        self.assertTrue(stats['restricted_optimal']);result=check(inst,Submission(inst.name,list(out.values())))
        self.assertTrue(result.legal);self.assertEqual(result.total_delay,6);self.assertEqual(stats['objective'],6)

    def test_two_net_distance_model_matches_path_model(self):
        inst,sub=make(3,2,[1],1,(0,0,0),[(2,0,0)],block=((0,1,0),(1,1,0)),own_edges=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0))])
        router=Router(inst,sub,10000,5,1);vertices={(x,y,0) for x in range(3) for y in range(2)}
        a,sa=solve_paths(router,[0,1],vertices,2,1,True);b,sb=solve_trees(router,[0,1],vertices,2,1)
        self.assertTrue(sa['restricted_optimal']);self.assertTrue(sb['restricted_optimal'])
        self.assertEqual(check(inst,Submission(inst.name,list(a.values()))).total_delay,check(inst,Submission(inst.name,list(b.values()))).total_delay)

    def test_unoccupied_layer_delay_hand_calculation(self):
        path=[(x,0,0) for x in range(5)]
        inst,sub=make(5,1,[6,2],3,path[0],[path[-1]],own_edges=list(zip(path,path[1:])))
        router=Router(inst,sub,10000,5,1);out,stats=solve_trees(router,[0],{(x,0,z) for x in range(5) for z in range(2)},2,1)
        result=check(inst,Submission(inst.name,list(out.values())));self.assertTrue(result.legal)
        self.assertEqual(result.total_delay,14) # four cost2 steps + two cost3 vias

    def test_limit_does_not_mutate_incumbent(self):
        edges=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0))]
        inst,sub=make(3,1,[1],1,(0,0,0),[(2,0,0)],own_edges=edges);before=sub.to_dict()
        router=Router(inst,sub,10000,5,1);solve_trees(router,[0],{(x,0,0) for x in range(3)},2,0)
        self.assertEqual(sub.to_dict(),before)

    def test_strict_cut_proves_no_improvement_on_optimal_hand_tree(self):
        edges=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0))]
        inst,sub=make(3,1,[1],1,(0,0,0),[(2,0,0)],own_edges=edges)
        router=Router(inst,sub,10000,5,1);out,stats=solve_trees(router,[0],{(x,0,0) for x in range(3)},2,1,strict=True)
        self.assertFalse(out);self.assertTrue(stats['proved_no_improvement']);self.assertEqual(stats['bound'],2)

    def test_strict_cut_finds_new_tree(self):
        path=[(0,0,0),(0,1,0),(1,1,0),(2,1,0),(2,0,0)]
        inst,sub=make(3,2,[1],1,path[0],[path[-1]],own_edges=list(zip(path,path[1:])))
        router=Router(inst,sub,10000,5,1);out,stats=solve_trees(router,[0],{(x,y,0) for x in range(3) for y in range(2)},2,1,strict=True)
        self.assertTrue(stats['restricted_optimal']);result=check(inst,Submission(inst.name,list(out.values())))
        self.assertTrue(result.legal);self.assertEqual(result.total_delay,2)

if __name__=='__main__':unittest.main(verbosity=2)
