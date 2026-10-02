"""Focused independent checks for the partial branch prototype."""
import unittest
from branch_repair import Router
from test_exact import make
from run_polish import NetRoute,check

class BranchRepair(unittest.TestCase):
    def test_root_distance_frontier(self):
        path=[(0,0,0),(1,0,0),(2,0,0),(2,1,0),(2,2,0)]
        inst,sub=make(3,3,[1],1,path[0],[path[-1]],own_edges=list(zip(path,path[1:])))
        router=Router(inst,sub,1000,5,1)
        retained=NetRoute(0,[(path[0],path[1]),(path[1],path[2])])
        candidate=router.search(0,[path[-1]],retained,set())
        _,dist,_=router.tree(candidate)
        self.assertEqual(dist[path[-1]],4) # two retained + two new edges
        self.assertTrue(check(inst,type(sub)(inst.name,[candidate])).legal)

    def test_partial_cut_preserves_sibling_and_ancestor_sink(self):
        edges=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0)),((1,0,0),(1,1,0)),((1,1,0),(1,2,0))]
        inst,sub=make(3,3,[1],1,(0,0,0),[(1,0,0),(2,0,0),(1,2,0)],own_edges=edges)
        router=Router(inst,sub,1000,5,1);r,sinks,count=router.retained(0,{(1,1,0)},False)
        self.assertEqual(count,2);self.assertEqual(sinks,[(1,2,0)])
        self.assertEqual(set(r.edges),set(edges[:2]))
        rebuilt=router.search(0,sinks,r,set())
        self.assertTrue(check(inst,type(sub)(inst.name,[rebuilt])).legal)

    def test_fixed_work_rollback_and_determinism(self):
        path=[(0,0,0),(0,1,0),(1,1,0),(2,1,0),(2,0,0)]
        inst,sub=make(3,3,[1],1,path[0],[path[-1]],own_edges=list(zip(path,path[1:])))
        for mode in ['branch','whole']:
            for work in [1,5,20,100]:
                outputs=[]
                for _ in range(2):
                    router=Router(inst,sub,work,5,3);out=router.run(mode,5)
                    result=check(inst,out);self.assertTrue(result.legal)
                    self.assertLessEqual(result.total_delay,4);self.assertLessEqual(router.expansions,work)
                    outputs.append(out.to_dict())
                self.assertEqual(*outputs)

if __name__=='__main__':unittest.main(verbosity=2)
