import unittest
from test_exact import make
from branch_repair import Router
from adaptive_price_pool import priced,generate
from run_polish import check,Submission
from select_tree_pool import solve_pool
class PricePool(unittest.TestCase):
    def test_hand_toll_changes_path_without_illegal_tree(self):
        path=[(0,0,0),(1,0,0),(2,0,0)]
        inst,sub=make(3,2,[1],1,path[0],[path[-1]],own_edges=list(zip(path,path[1:])))
        r=Router(inst,sub,1000,5,1);tree=priced(r,0,{(1,0,0):100})
        result=check(inst,Submission(inst.name,[tree]));self.assertTrue(result.legal);self.assertEqual(result.total_delay,4)
        self.assertNotIn((1,0,0),r.vertices(tree))
    def test_work_limit_keeps_verified_base_in_pool(self):
        path=[(0,0,0),(1,0,0),(2,0,0)]
        inst,sub=make(3,2,[1],1,path[0],[path[-1]],own_edges=list(zip(path,path[1:])))
        before=sub.to_dict();r=Router(inst,sub,1,5,1);ids,pool,history,limited=generate(r,4,16)
        self.assertTrue(limited);self.assertEqual(sub.to_dict(),before);self.assertEqual(pool[0][0][1],2)
        choices,stats=solve_pool([[t[1] for t in pool[i]] for i in ids],[[t[2] for t in pool[i]] for i in ids],[0],1,1)
        self.assertEqual(stats['chosen_delay'],2)
if __name__=='__main__':unittest.main()

class FractionalMaster(unittest.TestCase):
    def test_hand_capacity_tradeoff_and_dual_sign(self):
        from adaptive_price_pool import fractional_prices
        pool={0:[(None,5,{(0,0,0)}),(None,2,{(1,0,0)})],1:[(None,5,{(2,0,0)}),(None,2,{(1,0,0)})]}
        prices,bound=fractional_prices([0,1],pool)
        self.assertAlmostEqual(bound,7);self.assertAlmostEqual(prices[(1,0,0)],48)
    def test_fractional_bound_is_restricted_not_global(self):
        from adaptive_price_pool import fractional_prices
        pool={0:[(None,10,{(0,0,0)})]};_,bound=fractional_prices([0],pool)
        self.assertEqual(bound,10)
        pool[0].append((None,2,{(1,0,0)}));_,bound=fractional_prices([0],pool);self.assertEqual(bound,2)
