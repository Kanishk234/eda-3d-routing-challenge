"""Independent exhaustive oracle for restricted closure optimization."""
import json,random,tempfile,unittest
from pathlib import Path
from recombine_routes import minimum_closure,ancestor_costs
class Closure(unittest.TestCase):
    def test_forced_costly_dependencies(self):
        selected,cert=minimum_closure([-10,3,4],[(0,1),(1,2)])
        self.assertEqual(selected,{0,1,2});self.assertEqual(cert['minimum_delta'],-3)
        selected,cert=minimum_closure([-5,9],[(0,1)])
        self.assertEqual(selected,set());self.assertEqual(cert['minimum_delta'],0)
    def test_cycles_and_exhaustive_random(self):
        rng=random.Random(9021)
        for n in range(1,9):
            for _ in range(25):
                costs=[rng.randrange(-20,21) for _ in range(n)];arcs=[(i,j) for i in range(n) for j in range(n) if i!=j and rng.random()<.2]
                feasible=[]
                for bits in range(1<<n):
                    if all(not(bits>>i&1) or bits>>j&1 for i,j in arcs):feasible.append(sum(c for i,c in enumerate(costs) if bits>>i&1))
                selected,cert=minimum_closure(costs,arcs)
                self.assertEqual(cert['minimum_delta'],min(feasible));self.assertEqual(sum(costs[i] for i in selected),min(feasible))
    def test_nested_portfolio_costs_and_cycle_detection(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);child=root/'child';parent=root/'parent';portfolio=root/'mix'
            for p in (child,parent,portfolio):(p/'routes').mkdir(parents=True)
            (child/'manifest.json').write_text(json.dumps({'run_id':'child','wrapper_wall_s':3,'warm_start':{'directory':str(parent/'routes')}}))
            (parent/'manifest.json').write_text(json.dumps({'run_id':'parent','wrapper_wall_s':2,'warm_start':{'directory':str(portfolio/'routes')}}))
            (portfolio/'portfolio.json').write_text(json.dumps({'known_ancestry_runs':{'older':7},'missing_ancestor_artifacts':['lost']}))
            costs,missing=ancestor_costs(child);self.assertEqual(costs,{'child':3,'parent':2,'older':7});self.assertEqual(missing,{'lost'})
            (parent/'manifest.json').write_text(json.dumps({'run_id':'parent','wrapper_wall_s':2,'warm_start':{'directory':str(child/'routes')}}))
            with self.assertRaises(ValueError):ancestor_costs(child)

    def test_scaled_preference_preserves_primary_optimum(self):
        rng=random.Random(778)
        for n in range(1,8):
            for _ in range(20):
                costs=[rng.randrange(-4,5) for _ in range(n)];arcs=[(i,j) for i in range(n) for j in range(n) if i!=j and rng.random()<.25]
                feasible=[]
                for bits in range(1<<n):
                    if all(not(bits>>i&1) or bits>>j&1 for i,j in arcs):
                        feasible.append((sum(c for i,c in enumerate(costs) if bits>>i&1),-bits.bit_count()))
                selected,_=minimum_closure([c*(n+1)-1 for c in costs],arcs)
                self.assertEqual((sum(costs[i] for i in selected),-len(selected)),min(feasible))

if __name__=='__main__':unittest.main()
