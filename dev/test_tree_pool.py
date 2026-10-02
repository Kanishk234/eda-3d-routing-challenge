"""Compare finite-pool selection with exhaustive independent enumeration."""
import itertools,random,unittest
from select_tree_pool import solve_pool

class TreePool(unittest.TestCase):
    def test_independent_exhaustive_oracles(self):
        rng=random.Random(17)
        for _ in range(30):
            resources=[];costs=[]
            for nid in range(3):
                resources.append([{20+nid},*[{20+nid,*rng.sample(range(5),rng.randrange(1,4))} for _ in range(2)]])
                costs.append([rng.randrange(8,20),rng.randrange(1,20),rng.randrange(1,20)])
            valid=[]
            for choices in itertools.product(range(3),repeat=3):
                chosen=[resources[nid][k] for nid,k in enumerate(choices)]
                if all(not chosen[i]&chosen[j] for i in range(3) for j in range(i)):
                    valid.append(sum(costs[nid][k] for nid,k in enumerate(choices)))
            choices,result=solve_pool(costs,resources,[0,0,0],2,1)
            self.assertTrue(result['restricted_optimal']);self.assertEqual(result['chosen_delay'],min(valid))
            self.assertEqual(result['chosen_delay'],sum(costs[nid][k] for nid,k in enumerate(choices)))

if __name__=='__main__':unittest.main(verbosity=2)
