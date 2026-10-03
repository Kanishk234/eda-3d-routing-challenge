import unittest
import importlib.util
from types import SimpleNamespace
from hrm_local_proposals import window, encode, guided_tree


class WindowChecks(unittest.TestCase):
    def router(self):
        pins = {'a': (0, 0, 0), 'b': (3, 2, 1), 'c': (2, 1, 0)}
        net = SimpleNamespace(pins=lambda: ['a', 'b'])
        return SimpleNamespace(pins=pins, nets={1: net}, owner={(1, 0, 0): 2},
                               pin_owner={(2, 1, 0): 2},
                               inst=SimpleNamespace(in_bounds=lambda v: 0 <= v[0] < 4 and 0 <= v[1] < 3 and 0 <= v[2] < 2))

    @unittest.skipUnless(importlib.util.find_spec('torch'), 'optional PyTorch dependency')
    def test_boundaries_external_resources_and_axis_order(self):
        r = self.router(); self.assertEqual(window(r, [1]), (0, 0, 0))
        grid = encode(r, [1], (0, 0, 0))
        self.assertEqual(tuple(grid.shape), (16, 4, 16))
        self.assertEqual(int(grid[0, 0, 0]), 3)
        self.assertEqual(int(grid[2, 1, 3]), 3)
        self.assertEqual(int(grid[0, 0, 1]), 2)
        self.assertEqual(int(grid[1, 0, 2]), 2)
        self.assertEqual(int(grid[0, 3, 0]), 2)
        self.assertEqual(int(grid[15, 0, 15]), 2)

    def test_large_windows_rejected_without_rescaling(self):
        r = self.router(); r.pins['b'] = (16, 0, 0)
        self.assertIsNone(window(r, [1]))
        r.pins['b'] = (0, 0, 4)
        self.assertIsNone(window(r, [1]))

    def test_neural_preferences_cannot_replace_physical_cost(self):
        root, sink = (0, 0, 0), (2, 0, 0)
        n = SimpleNamespace(driver='a', sinks=['b'])
        r = SimpleNamespace(pins={'a': root, 'b': sink}, nets={1: n},
                            owner={}, pin_owner={}, expansions=0, work=100,
                            deadline=float('inf'))
        def neighbors(v):
            x, y, z = v
            return [(u, 1) for u in [(x+1,y,z),(x-1,y,z),(x,y+1,z),(x,y-1,z)]
                    if 0 <= u[0] <= 2 and 0 <= u[1] <= 1]
        r.neighbors = neighbors
        preferred = {(0,1,0), (1,1,0), (2,1,0)}
        tree = guided_tree(r, 1, preferred, [1], 0)
        self.assertEqual(len(tree.edges), 2)
        self.assertEqual({v for e in tree.edges for v in e}, {root, (1,0,0), sink})


if __name__ == '__main__': unittest.main()
