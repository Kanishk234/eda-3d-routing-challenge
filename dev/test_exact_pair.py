"""Independent tiny path enumeration for restricted exact repair."""
import itertools,unittest
from test_exact import make
from exact_pair_repair import solve_paths
from branch_repair import Router
from run_polish import Submission,check

class ExactPair(unittest.TestCase):
    def test_exhaustive_simple_path_oracle(self):
        inst,sub=make(3,2,[1],1,(0,0,0),[(2,0,0)],block=((0,1,0),(1,1,0)),own_edges=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0))])
        router=Router(inst,sub,10000,5,1);vertices={(x,y,0) for x in range(3) for y in range(2)};choices=[]
        for nid in [0,1]:
            n=router.nets[nid];root=router.pins[n.driver];sink=router.pins[n.sinks[0]];paths=[]
            def visit(u,path,cost):
                if u==sink:paths.append((set(path),cost));return
                for v,step in router.neighbors(u):
                    if v in vertices and v not in path and router.pin_owner.get(v,nid)==nid:visit(v,path+[v],cost+step)
            visit(root,[root],0);choices.append(paths)
        oracle=min(a[1]+b[1] for a,b in itertools.product(*choices) if not a[0]&b[0])
        for prune in [False,True]:
            result,stats=solve_paths(router,[0,1],vertices,2,1,prune);self.assertTrue(stats['restricted_optimal'])
            checked=check(inst,Submission(inst.name,list(result.values())));self.assertTrue(checked.legal);self.assertEqual(checked.total_delay,oracle)

    def test_new_geometry_improves_hand_detour(self):
        path=[(0,0,0),(0,1,0),(1,1,0),(2,1,0),(2,0,0)]
        inst,sub=make(3,3,[1],1,path[0],[path[-1]],block=((0,2,0),(1,2,0)),own_edges=list(zip(path,path[1:])))
        router=Router(inst,sub,10000,5,1);vertices={(x,y,0) for x in range(3) for y in range(3)}
        for prune in [False,True]:
            result,stats=solve_paths(router,[0,1],vertices,2,1,prune)
            checked=check(inst,Submission(inst.name,list(result.values())));self.assertTrue(checked.legal)
            self.assertEqual(stats['baseline'],5);self.assertEqual(checked.total_delay,3)

    def test_solver_limit_preserves_external_incumbent(self):
        inst,sub=make(3,2,[1],1,(0,0,0),[(2,0,0)],block=((0,1,0),(1,1,0)),own_edges=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0))])
        before=sub.to_dict();router=Router(inst,sub,1000,5,1)
        result,_=solve_paths(router,[0,1],{(x,y,0) for x in range(3) for y in range(2)},2,0)
        self.assertEqual(sub.to_dict(),before)
        if result:self.assertTrue(check(inst,Submission(inst.name,list(result.values()))).legal)

    def test_three_net_group(self):
        from m3d.model import Net,Pin
        from run_polish import NetRoute
        inst,sub=make(3,3,[1],1,(0,0,0),[(2,0,0)],block=((0,1,0),(1,1,0)),own_edges=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0))])
        inst.pins.extend([Pin(4,2,0,0,2,0),Pin(5,2,0,2,2,0)]);inst.nets.append(Net(2,4,[5]))
        sub.routes.append(NetRoute(2,[((0,2,0),(1,2,0)),((1,2,0),(2,2,0))]))
        router=Router(inst,sub,1000,5,1);result,stats=solve_paths(router,[0,1,2],{(x,y,0) for x in range(3) for y in range(3)},2,1)
        self.assertTrue(stats['restricted_optimal']);checked=check(inst,Submission(inst.name,list(result.values())))
        self.assertTrue(checked.legal);self.assertEqual(checked.total_delay,5)

if __name__=='__main__':unittest.main(verbosity=2)
