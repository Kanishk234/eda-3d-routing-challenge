import unittest
from branch_repair import Router, Limit
from hrm_branch_proposals import box, branches, branch_router
from hrm_local_proposals import guided_tree
from test_exact import make
from run_polish import NetRoute, Submission, check


class BranchWindows(unittest.TestCase):
    def setup_branch(self):
        edges = [((x,0,0),(x+1,0,0)) for x in range(4)] + [((3,0,0),(3,1,0))]
        inst, sub = make(5,2,[1],2,(0,0,0),[(4,0,0),(3,1,0)],own_edges=edges)
        original = Router(inst,sub,1000,10,1)
        b = dict(nid=0,attachment=(2,0,0),removed={(3,0,0),(4,0,0),(3,1,0)},
                 sinks=[(4,0,0),(3,1,0)],retained=NetRoute(0,edges[:2]))
        return inst, sub, original, b

    def test_connected_outside_preserved_and_delays_counted(self):
        inst, sub, original, b = self.setup_branch()
        r = branch_router(original,[b],(0,0,0))
        self.assertNotIn(r.owner[(1,0,0)], [0])
        tree = guided_tree(r,0,set(),[0],0)
        merged = NetRoute(0,[*b['retained'].edges,*tree.edges])
        result = check(inst,Submission(inst.name,[merged]))
        self.assertTrue(result.legal)
        # Driver to each sink takes four unit steps; shared trunk counts twice.
        self.assertEqual(result.total_delay,8)
        self.assertEqual(original.owner[(1,0,0)],0)
        self.assertEqual(check(inst,sub).total_delay,8)

    def test_interruption_does_not_mutate_original(self):
        inst, sub, original, b = self.setup_branch(); old = dict(original.owner)
        r = branch_router(original,[b],(0,0,0),work=1)
        with self.assertRaises(Limit): guided_tree(r,0,set(),[0],0)
        self.assertEqual(original.owner,old)
        self.assertTrue(check(inst,sub).legal)

    def test_extraction_covers_all_downstream_sinks(self):
        _, _, original, _ = self.setup_branch()
        selected = branches(original)
        self.assertEqual(len(selected),1)
        self.assertEqual(set(selected[0]['sinks']),{(4,0,0),(3,1,0)})
        self.assertEqual(selected[0]['gap'],0)
        self.assertIsNone(box({(0,0,0),(16,0,0)}))


if __name__=='__main__': unittest.main()
