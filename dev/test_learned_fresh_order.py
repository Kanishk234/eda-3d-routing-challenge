import unittest
from learned_fresh_order import synthetic,features,construct,train,order_model
from run_polish import check
class FreshLearned(unittest.TestCase):
    def test_generated_pins_distinct_and_deterministic(self):
        a=synthetic(1001);b=synthetic(1001);self.assertEqual(a.to_dict(),b.to_dict());pv=a.pin_vertex();self.assertEqual(len(set(pv.values())),len(pv))
    def test_pairwise_training_learns_known_direction(self):
        weights=train([({0:[1.0]*9,1:[0.0]*9},[0,1])]);self.assertGreater(sum(weights),0)
    def test_fresh_output_official_legality(self):
        for seed in range(1001,1005):
            inst=synthetic(seed);out=construct(inst,order_model(inst,[0]*9))
            if out:self.assertTrue(check(inst,out[0]).legal)
if __name__=='__main__':unittest.main()
