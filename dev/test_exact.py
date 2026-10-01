"""Independent correctness/integration checks for the C++ exact kernel."""
import heapq
import random
import subprocess
import signal
import time
import unittest
from run_polish import ENGINE, encode, decode, Instance, Submission, NetRoute, check
from m3d.model import Pin, Net

def make(w,h,delays,via,root,sinks,block=None,own_edges=None):
    vertices=[root,*sinks]
    pins=[Pin(i,0,int(v[2]>0),*v) for i,v in enumerate(vertices)]
    nets=[Net(0,0,list(range(1,len(vertices))))]
    routes=[NetRoute(0,own_edges or [])]
    if block:
        a,b=block
        base=len(pins)
        pins += [Pin(base,1,int(a[2]>0),*a),Pin(base+1,1,int(b[2]>0),*b)]
        nets.append(Net(1,base,[base+1])); routes.append(NetRoute(1,[(a,b)]))
    inst=Instance("toy",w,h,len(delays),delays,via,[],pins,nets)
    return inst,Submission(inst.name,routes)

def reference(inst,root,sinks,blocked):
    distances={root:0}; previous={}
    queue=[(0,root)]
    while queue:
        cost,u=heapq.heappop(queue)
        if cost!=distances[u]: continue
        x,y,z=u
        for dx,dy,dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
            v=(x+dx,y+dy,z+dz)
            if not (0<=v[0]<inst.width and 0<=v[1]<inst.height and 0<=v[2]<inst.layers) or v in blocked:
                continue
            step=inst.via_delay if dz else inst.layer_delay[z]
            candidate=cost+step
            if candidate<distances.get(v,10**30):
                distances[v]=candidate; previous[v]=u; heapq.heappush(queue,(candidate,v))
    return sum(distances[s] for s in sinks),previous

def core(inst,sub,mode="search",budget=2,seed=1):
    run=subprocess.run([str(ENGINE),str(budget),str(seed),"5",mode],input=encode(inst,sub),
                       text=True,capture_output=True,timeout=budget+3)
    if run.returncode:
        return run,None,None
    result,stats=decode(inst,run.stdout)
    return run,result,stats

class ExactKernel(unittest.TestCase):
    def test_cheaper_layer_and_vias(self):
        inst,sub=make(5,5,[6,2],3,(0,0,0),[(4,4,0)])
        _,out,stats=core(inst,sub)
        # Eight XY steps at cost2 and two cost3 vias =22, vs48 on bottom.
        self.assertEqual(stats["total_delay"],22)
        self.assertTrue(check(inst,out).legal)

    def test_shared_trunk_counts_for_each_sink(self):
        inst,sub=make(5,1,[1],3,(0,0,0),[(2,0,0),(4,0,0)])
        _,out,stats=core(inst,sub)
        self.assertEqual(stats["total_delay"],6)
        self.assertEqual(len(out.routes[0].edges),4)
        self.assertEqual(check(inst,out).total_delay,6)

    def test_foreign_pin_and_via_endpoints(self):
        inst,sub=make(3,2,[1,1],1,(0,0,0),[(2,0,0)],((1,0,0),(1,0,1)))
        _,out,stats=core(inst,sub)
        self.assertEqual(stats["net_delays"][0],4)
        self.assertTrue(check(inst,out).legal)
        occupied={v for e in out.routes[0].edges for v in e}
        self.assertNotIn((1,0,0),occupied); self.assertNotIn((1,0,1),occupied)

    def test_unroutable_foreign_column(self):
        inst,sub=make(3,1,[1,1],1,(0,0,0),[(2,0,0)],((1,0,0),(1,0,1)))
        run,out,_=core(inst,sub)
        self.assertEqual(run.returncode,2); self.assertIsNone(out)

    def test_random_graph_costs_against_independent_dijkstra(self):
        rng=random.Random(147)
        for i in range(30):
            delays=[rng.randrange(1,10),rng.randrange(1,10)]
            root=(0,0,0); sinks=[(4,3,1),(4,0,0)]
            a=(rng.randrange(1,4),rng.randrange(0,3),rng.randrange(2))
            b=(a[0],a[1]+1,a[2])
            inst,sub=make(5,4,delays,rng.randrange(1,8),root,sinks,(a,b))
            expected,_=reference(inst,root,sinks,{a,b})
            _,out,stats=core(inst,sub,seed=i)
            self.assertEqual(stats["net_delays"][0],expected)
            self.assertTrue(check(inst,out).legal)
            self.assertEqual(check(inst,out).total_delay,stats["total_delay"])

    def test_no_improvement_preserves_ownership_and_route(self):
        block=((1,0,0),(1,0,1))
        own=[((0,0,0),(0,1,0)),((0,1,0),(1,1,0)),
             ((1,1,0),(2,1,0)),((2,1,0),(2,0,0))]
        inst,sub=make(3,2,[1,1],1,(0,0,0),[(2,0,0)],block,own)
        before=check(inst,sub)
        self.assertTrue(before.legal)
        _,out,stats=core(inst,sub,"polish")
        self.assertEqual(stats["accepted_replacements"],0)
        self.assertTrue(check(inst,out).legal)
        self.assertEqual(check(inst,out).total_delay,before.total_delay)
        self.assertEqual({frozenset(e) for e in out.routes[0].edges},{frozenset(e) for e in own})

    def test_zero_budget_keeps_valid_incumbent(self):
        own=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0))]
        inst,sub=make(3,1,[2],3,(0,0,0),[(2,0,0)],own_edges=own)
        _,out,stats=core(inst,sub,"polish",budget=0)
        self.assertTrue(stats["budget_reached"])
        self.assertEqual(stats["total_delay"],4)
        self.assertTrue(check(inst,out).legal)

    def test_rejects_cycles_and_conflicts(self):
        own=[((0,0,0),(1,0,0)),((1,0,0),(1,1,0)),
             ((1,1,0),(0,1,0)),((0,1,0),(0,0,0))]
        inst,sub=make(2,2,[1],1,(0,0,0),[(1,1,0)],own_edges=own)
        run,_,_=core(inst,sub,"polish")
        self.assertEqual(run.returncode,2)

    def test_disconnected_tree_rejected(self):
        inst,sub=make(4,1,[1],1,(0,0,0),[(3,0,0)],
                      own_edges=[((0,0,0),(1,0,0)),((2,0,0),(3,0,0))])
        run,_,_=core(inst,sub,"polish")
        self.assertEqual(run.returncode,2)

    def test_shared_routing_vertex_rejected(self):
        inst,sub=make(3,2,[1],1,(0,0,0),[(2,0,0)],
                      block=((1,0,0),(1,1,0)),
                      own_edges=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0))])
        run,_,_=core(inst,sub,"polish")
        self.assertEqual(run.returncode,2)

    def test_wide_integer_delays(self):
        own=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0)),((2,0,0),(3,0,0)),
             ((3,0,0),(4,0,0))]
        inst,sub=make(5,1,[1000000000],1,(0,0,0),[(4,0,0)],own_edges=own)
        _,out,stats=core(inst,sub,"polish")
        self.assertEqual(stats["total_delay"],4000000000)
        self.assertEqual(check(inst,out).total_delay,4000000000)

    def test_signal_keeps_complete_incumbent(self):
        vertices=[(x,0,0) for x in range(500)]
        vertices += [(499,y,0) for y in range(1,500)]
        vertices += [(499,499,z) for z in range(1,6)]
        edges=list(zip(vertices,vertices[1:]))
        inst,sub=make(500,500,[6,4,2,2,4,6],3,vertices[0],[vertices[-1]],own_edges=edges)
        proc=subprocess.Popen([str(ENGINE),"60","1","100","polish"],text=True,
                              stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        proc.stdin.write(encode(inst,sub)); proc.stdin.close(); proc.stdin=None
        time.sleep(0.01)
        proc.send_signal(signal.SIGTERM)
        output,stderr=proc.communicate(timeout=5)
        self.assertEqual(proc.returncode,0,stderr)
        out,stats=decode(inst,output)
        self.assertTrue(stats["budget_reached"])
        self.assertTrue(check(inst,out).legal)
        self.assertLessEqual(stats["total_delay"],check(inst,sub).total_delay)

    def test_group_repair_is_legal_and_nonworsening(self):
        own=[((0,0,0),(0,1,0)),((0,1,0),(1,1,0)),
             ((1,1,0),(2,1,0)),((2,1,0),(2,0,0))]
        inst,sub=make(3,2,[1,1],1,(0,0,0),[(2,0,0)],
                      ((1,0,0),(1,0,1)),own)
        before=check(inst,sub).total_delay
        for seed in (1,2,3):
            run,out,stats=core(inst,sub,"repair",seed=seed)
            self.assertEqual(run.returncode,0)
            self.assertTrue(check(inst,out).legal)
            self.assertLessEqual(stats["total_delay"],before)

    def test_group_repair_zero_budget_retains_incumbent(self):
        own=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0))]
        inst,sub=make(3,1,[2],3,(0,0,0),[(2,0,0)],own_edges=own)
        _,out,stats=core(inst,sub,"repair",budget=0)
        self.assertEqual(check(inst,out).total_delay,4)
        self.assertTrue(stats["budget_reached"])

    def test_soft_repair_reports_physical_shared_trunk_delay(self):
        own=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0)),
             ((2,0,0),(3,0,0)),((3,0,0),(4,0,0))]
        inst,sub=make(5,1,[2],3,(0,0,0),[(2,0,0),(4,0,0)],own_edges=own)
        _,out,stats=core(inst,sub,"repairsoft")
        self.assertEqual(stats["total_delay"],12)
        self.assertEqual(check(inst,out).total_delay,12)

    def test_attachment_ablation_matches_independent_shortest_cost(self):
        import json
        inst,sub=make(5,1,[2],3,(0,0,0),[(2,0,0),(4,0,0)],
            own_edges=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0)),
                       ((2,0,0),(3,0,0)),((3,0,0),(4,0,0))])
        run,out,_=core(inst,sub,"ablation")
        report=json.loads(run.stderr.splitlines()[-1])
        self.assertEqual(report["completed_nets"],1)
        self.assertEqual(report["exact_delay"],12)
        self.assertEqual(report["root_attachment_delay"],12)
        self.assertEqual(check(inst,out).total_delay,12)

    def test_negotiated_group_crossing_stays_legal(self):
        pins=[Pin(0,0,0,0,2,0),Pin(1,0,0,4,2,0),
              Pin(2,1,0,2,0,0),Pin(3,1,0,2,4,0)]
        inst=Instance("crossing",5,5,2,[2,1],2,[],pins,[Net(0,0,[1]),Net(1,2,[3])])
        horizontal=[(0,2,0),(0,2,1),(1,2,1),(2,2,1),(3,2,1),(4,2,1),(4,2,0)]
        vertical=[(2,y,0) for y in range(5)]
        sub=Submission(inst.name,[NetRoute(0,list(zip(horizontal,horizontal[1:]))),
                                  NetRoute(1,list(zip(vertical,vertical[1:])))])
        before=check(inst,sub)
        self.assertTrue(before.legal)
        for seed in (1,2,3):
            run,out,stats=core(inst,sub,"negotiated")
            self.assertEqual(run.returncode,0)
            self.assertTrue(check(inst,out).legal)
            self.assertLessEqual(stats["total_delay"],before.total_delay)

    def test_negotiated_zero_budget_keeps_checkpoint(self):
        inst,sub=make(3,1,[2],3,(0,0,0),[(2,0,0)],
                      own_edges=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0))])
        _,out,stats=core(inst,sub,"negotiated",budget=0)
        self.assertEqual(check(inst,out).total_delay,4)
        self.assertTrue(stats["budget_reached"])

    def test_output_parser_rejects_truncation(self):
        inst,_=make(3,1,[1],1,(0,0,0),[(2,0,0)])
        with self.assertRaises(ValueError):
            decode(inst,"M3DOUT1 1 2 0 0 0 0 0 2 2 0 1")

if __name__=="__main__":
    unittest.main(verbosity=2)
