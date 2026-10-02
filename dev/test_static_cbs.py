"""Physical objective, geometry improvements, and interruption checks."""
import unittest
from test_exact import make
from branch_repair import Router
from static_cbs import solve_cbs
from run_polish import Submission,check
class StaticCBS(unittest.TestCase):
    def test_new_geometry(self):
        path=[(0,0,0),(0,1,0),(1,1,0),(2,1,0),(2,0,0)]
        inst,sub=make(3,3,[1],1,path[0],[path[-1]],block=((0,2,0),(1,2,0)),own_edges=list(zip(path,path[1:])))
        r=Router(inst,sub,10000,5,1);out,s=solve_cbs(r,[0,1],{(x,y,0) for x in range(3) for y in range(3)})
        checked=check(inst,Submission(inst.name,list(out.values())))
        self.assertTrue(checked.legal);self.assertEqual(checked.total_delay,3);self.assertTrue(s['restricted_optimal'])
    def test_shared_trunk(self):
        edges=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0)),((2,0,0),(2,1,0)),((2,1,0),(2,2,0))]
        inst,sub=make(3,3,[1],1,(0,0,0),[(2,0,0),(2,2,0)],own_edges=edges)
        out,s=solve_cbs(Router(inst,sub,10000,5,1),[0],{(x,y,0) for x in range(3) for y in range(3)})
        self.assertEqual(check(inst,Submission(inst.name,list(out.values()))).total_delay,6);self.assertEqual(s['bound'],6)
    def test_work_limit_preserves_state(self):
        path=[(0,0,0),(0,1,0),(1,1,0),(2,1,0),(2,0,0)]
        inst,sub=make(3,2,[1],1,path[0],[path[-1]],own_edges=list(zip(path,path[1:])))
        before=sub.to_dict()
        out,s=solve_cbs(Router(inst,sub,10000,5,1),[0],{(x,y,0) for x in range(3) for y in range(2)},work_limit=1)
        self.assertEqual(sub.to_dict(),before);self.assertTrue(check(inst,Submission(inst.name,list(out.values()))).legal)
        self.assertFalse(s['restricted_optimal']);self.assertLessEqual(s['bound'],s['objective'])
if __name__=='__main__':unittest.main(verbosity=2)

class ConflictBranch(unittest.TestCase):
    def test_crossing_requires_static_vertex_branch(self):
        from run_polish import NetRoute
        horizontal=[(0,1,0),(0,1,1),(1,1,1),(2,1,1),(2,1,0)]
        vertical=[(1,0,0),(1,1,0),(1,2,0)]
        inst,sub=make(3,3,[1,1],1,horizontal[0],[horizontal[-1]],block=(vertical[0],vertical[-1]),own_edges=list(zip(horizontal,horizontal[1:])))
        sub.routes[1]=NetRoute(1,list(zip(vertical,vertical[1:])))
        self.assertTrue(check(inst,sub).legal)
        out,s=solve_cbs(Router(inst,sub,10000,5,1),[0,1],{(x,y,z) for x in range(3) for y in range(3) for z in range(2)})
        # Each direct path costs2; crossing requires at least two extra steps/vias.
        self.assertTrue(s['restricted_optimal']);self.assertGreater(s['branch_nodes'],0)
        self.assertEqual(s['objective'],6);self.assertEqual(check(inst,Submission(inst.name,list(out.values()))).total_delay,6)

class AvoidanceTie(unittest.TestCase):
    def test_physical_bounds_match_independent_shortest_paths(self):
        from test_exact import reference
        for size in range(3,8):
            path=[(x,0,0) for x in range(size)]
            inst,sub=make(size,2,[3,1],2,path[0],[path[-1]],own_edges=list(zip(path,path[1:])))
            expected,_=reference(inst,path[0],[path[-1]],set())
            vertices={(x,y,z) for x in range(size) for y in range(2) for z in range(2)}
            for avoid in [False,True]:
                out,s=solve_cbs(Router(inst,sub,10000,5,1),[0],vertices,avoid_ties=avoid)
                result=check(inst,Submission(inst.name,list(out.values())))
                self.assertTrue(result.legal);self.assertTrue(s['restricted_optimal']);self.assertEqual(result.total_delay,expected)

class BypassOracle(unittest.TestCase):
    def test_exhaustive_disjoint_path_pairs(self):
        import random,itertools
        from run_polish import NetRoute
        rng=random.Random(91);vertices={(x,y,0) for x in range(3) for y in range(3)}
        for trial in range(20):
            a,b,c,d=rng.sample(sorted(vertices),4)
            inst,sub=make(3,3,[1],1,a,[b],block=(c,d));choices=[]
            for root,sink,foreign in [(a,b,{c,d}),(c,d,{a,b})]:
                paths=[]
                def visit(path):
                    if path[-1]==sink:paths.append(path);return
                    x,y,z=path[-1]
                    for v in [(x+1,y,z),(x-1,y,z),(x,y+1,z),(x,y-1,z)]:
                        if v in vertices and v not in foreign and v not in path:visit(path+[v])
                visit([root]);choices.append(paths)
            legal=[(p,q) for p,q in itertools.product(*choices) if not set(p)&set(q)]
            if not legal:continue
            oracle=min(len(p)+len(q)-2 for p,q in legal)
            p,q=max(legal,key=lambda pair:sum(map(len,pair)))
            sub.routes=[NetRoute(i,list(zip(path,path[1:]))) for i,path in enumerate([p,q])]
            for avoid in [False,True]:
                out,s=solve_cbs(Router(inst,sub,100000,5,1),[0,1],vertices,bypass=True,avoid_ties=avoid)
                checked=check(inst,Submission(inst.name,list(out.values())))
                self.assertTrue(checked.legal);self.assertTrue(s['restricted_optimal']);self.assertEqual(checked.total_delay,oracle)
