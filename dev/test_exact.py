"""Independent correctness/integration checks for the C++ exact kernel."""
import json
import heapq
import random
import subprocess
import signal
import time
import unittest
from run_polish import ENGINE, encode, decode, Instance, Submission, NetRoute, check, NEIGHBORHOOD_MODES
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
        for mode in ["negotiated",*NEIGHBORHOOD_MODES]:
            for seed in (1,2,3):
                run,out,stats=core(inst,sub,mode,seed=seed)
                self.assertEqual(run.returncode,0)
                self.assertTrue(check(inst,out).legal)
                self.assertLessEqual(stats["total_delay"],before.total_delay)

    def test_seed_first_conflict_work_checkpoint_repetition(self):
        pins=[Pin(0,0,0,0,2,0),Pin(1,0,0,4,2,0),
              Pin(2,1,0,2,0,0),Pin(3,1,0,2,4,0)]
        inst=Instance("crossing",5,5,2,[2,1],2,[],pins,[Net(0,0,[1]),Net(1,2,[3])])
        horizontal=[(0,2,0),(0,2,1),(1,2,1),(2,2,1),(3,2,1),(4,2,1),(4,2,0)]
        vertical=[(2,y,0) for y in range(5)]
        sub=Submission(inst.name,[NetRoute(0,list(zip(horizontal,horizontal[1:]))),
                                  NetRoute(1,list(zip(vertical,vertical[1:])))])
        before=check(inst,sub).total_delay
        for limit in (1,20,100,1000):
            cmd=[str(ENGINE),"5","1","5","fanout_fine_conflict",str(limit),"repair_first=1"]
            runs=[subprocess.run(cmd,input=encode(inst,sub),text=True,capture_output=True,timeout=8) for _ in range(2)]
            self.assertEqual(runs[0].returncode,0)
            self.assertEqual(runs[0].stdout,runs[1].stdout)
            out,stats=decode(inst,runs[0].stdout)
            checked=check(inst,out)
            self.assertTrue(checked.legal)
            self.assertLessEqual(checked.total_delay,before)
            self.assertLessEqual(stats["expansions"],limit)

    def test_neutral_group_parser_and_work_checkpoints(self):
        pins=[Pin(0,0,0,0,2,0),Pin(1,0,0,4,2,0),Pin(2,1,0,2,0,0),Pin(3,1,0,2,4,0)]
        inst=Instance("crossing",5,5,2,[2,1],2,[],pins,[Net(0,0,[1]),Net(1,2,[3])])
        horizontal=[(0,2,0),(0,2,1),(1,2,1),(2,2,1),(3,2,1),(4,2,1),(4,2,0)]
        vertical=[(2,y,0) for y in range(5)]
        sub=Submission(inst.name,[NetRoute(0,list(zip(horizontal,horizontal[1:]))),NetRoute(1,list(zip(vertical,vertical[1:])))])
        data=encode(inst,sub);before=check(inst,sub).total_delay
        cmd=[str(ENGINE),"5","1","5","fanout_fine_window","1000"]
        default=subprocess.run(cmd,input=data,text=True,capture_output=True,timeout=8)
        explicit=subprocess.run(cmd+["accept_equal=0"],input=data,text=True,capture_output=True,timeout=8)
        self.assertEqual(default.stdout,explicit.stdout)
        bad=subprocess.run(cmd+["accept_equal=2"],input=data,text=True,capture_output=True,timeout=8)
        self.assertNotEqual(bad.returncode,0)
        neutral=0
        for limit in (1,20,100,1000):
            call=cmd[:-1]+[str(limit),"accept_equal=1","repair_first=1"]
            runs=[subprocess.run(call,input=data,text=True,capture_output=True,timeout=8) for _ in range(2)]
            self.assertEqual(runs[0].returncode,0);self.assertEqual(runs[0].stdout,runs[1].stdout)
            out,stats=decode(inst,runs[0].stdout);checked=check(inst,out)
            self.assertTrue(checked.legal);self.assertLessEqual(checked.total_delay,before);self.assertLessEqual(stats["expansions"],limit)
            counters=json.loads(runs[0].stderr.strip().splitlines()[-1])
            neutral+=counters["neutral_moves"]
            self.assertLessEqual(counters["neutral_moves"],stats["accepted_replacements"])
        self.assertGreater(neutral,0)

    def test_weighted_repair_sampling_defaults_caps_and_repetition(self):
        path=[(x,0,0) for x in range(5)]+[(4,y,0) for y in range(1,5)]
        inst,sub=make(5,5,[6,2],3,(0,0,0),[(4,4,0)],own_edges=list(zip(path,path[1:])))
        data=encode(inst,sub);cmd=[str(ENGINE),"5","1","5","fanout_fine_adaptive","1000"]
        default=subprocess.run(cmd,input=data,text=True,capture_output=True,timeout=8)
        explicit=subprocess.run(cmd+["repair_sampling=0"],input=data,text=True,capture_output=True,timeout=8)
        self.assertEqual(default.stdout,explicit.stdout)
        bad=subprocess.run(cmd+["repair_sampling=3"],input=data,text=True,capture_output=True,timeout=8)
        self.assertNotEqual(bad.returncode,0)
        for mode in (1,2):
            for limit in (1,20,1000):
                call=cmd[:-1]+[str(limit),"repair_sampling="+str(mode),"repair_first=1","accept_equal=1"]
                runs=[subprocess.run(call,input=data,text=True,capture_output=True,timeout=8) for _ in range(2)]
                self.assertEqual(runs[0].returncode,0);self.assertEqual(runs[0].stdout,runs[1].stdout)
                out,stats=decode(inst,runs[0].stdout);checked=check(inst,out)
                self.assertTrue(checked.legal);self.assertLessEqual(checked.total_delay,48);self.assertLessEqual(stats["expansions"],limit)

    def test_negotiated_zero_budget_keeps_checkpoint(self):
        inst,sub=make(3,1,[2],3,(0,0,0),[(2,0,0)],
                      own_edges=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0))])
        _,out,stats=core(inst,sub,"negotiated",budget=0)
        self.assertEqual(check(inst,out).total_delay,4)
        self.assertTrue(stats["budget_reached"])

    def test_plateau_keeps_hand_calculated_shortest_delays(self):
        inst,sub=make(5,1,[2],3,(0,0,0),[(2,0,0),(4,0,0)],
            own_edges=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0)),
                       ((2,0,0),(3,0,0)),((3,0,0),(4,0,0))])
        for seed in (1,2,3):
            _,out,stats=core(inst,sub,"explore",seed=seed)
            self.assertEqual(stats["total_delay"],12)
            self.assertTrue(check(inst,out).legal)

    def test_whole_restart_builds_cheaper_layer_tree(self):
        path=[(x,0,0) for x in range(5)]+[(4,y,0) for y in range(1,5)]
        inst,sub=make(5,5,[6,2],3,(0,0,0),[(4,4,0)],own_edges=list(zip(path,path[1:])))
        _,out,stats=core(inst,sub,"restart")
        self.assertEqual(stats["total_delay"],22)
        self.assertTrue(check(inst,out).legal)

    def test_whole_restart_zero_budget_preserves_route(self):
        inst,sub=make(3,1,[2],3,(0,0,0),[(2,0,0)],
                      own_edges=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0))])
        _,out,stats=core(inst,sub,"restart",budget=0)
        self.assertEqual(check(inst,out).total_delay,4)
        self.assertTrue(stats["budget_reached"])

    def test_candidate_selection_improves_single_net(self):
        path=[(x,0,0) for x in range(5)]+[(4,y,0) for y in range(1,5)]
        inst,sub=make(5,5,[6,2],3,(0,0,0),[(4,4,0)],own_edges=list(zip(path,path[1:])))
        _,out,stats=core(inst,sub,"select")
        self.assertEqual(stats["total_delay"],22)
        self.assertTrue(check(inst,out).legal)

    def test_candidate_selection_preserves_zero_budget(self):
        inst,sub=make(3,1,[2],3,(0,0,0),[(2,0,0)],
                      own_edges=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0))])
        _,out,stats=core(inst,sub,"select",budget=0)
        self.assertEqual(check(inst,out).total_delay,4)
        self.assertTrue(stats["budget_reached"])

    def test_wide_neighborhood_checkpoint(self):
        inst,sub=make(3,1,[2],3,(0,0,0),[(2,0,0)],
                      own_edges=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0))])
        for budget in (0,2):
            _,out,stats=core(inst,sub,"wide",budget=budget)
            self.assertEqual(check(inst,out).total_delay,4)
            self.assertTrue(check(inst,out).legal)

    def test_threshold_walk_keeps_best_legal_checkpoint(self):
        path=[(x,0,0) for x in range(5)]+[(4,y,0) for y in range(1,5)]
        inst,sub=make(5,5,[6,2],3,(0,0,0),[(4,4,0)],own_edges=list(zip(path,path[1:])))
        for seed in (1,2,3):
            _,out,stats=core(inst,sub,"walk",seed=seed)
            self.assertEqual(stats["total_delay"],22)
            self.assertTrue(check(inst,out).legal)

    def test_group_cost_variants_preserve_physical_delay(self):
        path=[(x,0,0) for x in range(5)]+[(4,y,0) for y in range(1,5)]
        inst,sub=make(5,5,[6,2],3,(0,0,0),[(4,0,0),(4,4,0)],own_edges=list(zip(path,path[1:])))
        for mode in ("compact","fanout"):
            _,out,stats=core(inst,sub,mode)
            self.assertEqual(stats["total_delay"],36)
            self.assertEqual(check(inst,out).total_delay,36)
            self.assertTrue(check(inst,out).legal)

    def test_resource_counts_do_not_duplicate_shared_trunk(self):
        from run_polish import route_resources
        inst,sub=make(5,1,[2],3,(0,0,0),[(2,0,0),(4,0,0)],
            own_edges=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0)),
                       ((2,0,0),(3,0,0)),((3,0,0),(4,0,0))])
        self.assertEqual(route_resources(sub),{"net_vertex_uses":5,"edges":4,"vias":0})
        self.assertEqual(check(inst,sub).total_delay,12)

    def test_fresh_price_variants_checkpoint_and_physical_cost(self):
        path=[(x,0,0) for x in range(5)]+[(4,y,0) for y in range(1,5)]
        inst,sub=make(5,5,[6,2],3,(0,0,0),[(4,4,0)],own_edges=list(zip(path,path[1:])))
        for mode in ("restart_fanout","restart_compact"):
            _,out,stats=core(inst,sub,mode)
            self.assertEqual(check(inst,out).total_delay,22)
            self.assertEqual(stats["total_delay"],22)
            _,out,_=core(inst,sub,mode,budget=0)
            self.assertEqual(check(inst,out).total_delay,48)

    def test_output_parser_rejects_truncation(self):
        inst,_=make(3,1,[1],1,(0,0,0),[(2,0,0)])
        with self.assertRaises(ValueError):
            decode(inst,"M3DOUT1 1 2 0 0 0 0 0 2 2 0 1")


class WorkAndAstarProperties(unittest.TestCase):
    def test_astar_matches_independent_dijkstra_and_checker(self):
        rng=random.Random(281)
        for i in range(30):
            a=(rng.randrange(1,4),rng.randrange(3),rng.randrange(2))
            b=(a[0],a[1]+1,a[2])
            inst,sub=make(5,4,[rng.randrange(1,10) for _ in range(2)],
                          rng.randrange(1,8),(0,0,0),[(4,3,1),(4,0,0)],(a,b))
            expected,_=reference(inst,(0,0,0),[(4,3,1),(4,0,0)],{a,b})
            _,warm,_=core(inst,sub,seed=i)
            for mode in ("polish","astar","astar_tight"):
                run,out,stats=core(inst,warm,mode,seed=i)
                self.assertEqual(run.returncode,0)
                checked=check(inst,out)
                self.assertTrue(checked.legal)
                self.assertEqual(stats["net_delays"][0],expected)
                self.assertEqual(checked.total_delay,stats["total_delay"])

    def test_donor_input_validation_work_cap_and_repeatability(self):
        path=[(x,0,0) for x in range(5)]+[(4,y,0) for y in range(1,5)]
        inst,sub=make(5,5,[6,2],3,(0,0,0),[(4,4,0)],own_edges=list(zip(path,path[1:])))
        _,donor,_=core(inst,sub)
        data=encode(inst,sub)+encode(inst,donor)
        for seed in (1,2,3):
            for limit in (1,25,100):
                outputs=[]
                for budget in (2,5):
                    run=subprocess.run([str(ENGINE),str(budget),str(seed),"1000","fanout_fine_donor",str(limit)],input=data,text=True,capture_output=True,timeout=8)
                    self.assertEqual(run.returncode,0)
                    result,stats=decode(inst,run.stdout)
                    counters=json.loads(run.stderr.splitlines()[-1])
                    self.assertLessEqual(counters["donor_gains"],counters["donor_selected"])
                    self.assertLessEqual(counters["donor_selected"],counters["donor_eligible"])
                    self.assertTrue(check(inst,result).legal)
                    self.assertLessEqual(stats["expansions"],limit)
                    self.assertLessEqual(stats["total_delay"],check(inst,sub).total_delay)
                    outputs.append(run.stdout)
                self.assertEqual(*outputs)
        for invalid in (encode(inst,sub),encode(inst,sub)+encode(inst,donor).replace("M3DIN1 5 5", "M3DIN1 6 5",1)):
            run=subprocess.run([str(ENGINE),"2","1","100","fanout_fine_donor","100"],input=invalid,text=True,capture_output=True,timeout=5)
            self.assertEqual(run.returncode,2)

    def test_polish_order_preserves_work_caps_and_exact_single_net_delay(self):
        path=[(x,0,0) for x in range(5)]+[(4,y,0) for y in range(1,5)]
        inst,sub=make(5,5,[6,2],3,(0,0,0),[(4,4,0)],own_edges=list(zip(path,path[1:])))
        for order in (1,2):
            for cap in (1,100,1000):
                outputs=[]
                for budget in (2,5):
                    run=subprocess.run([str(ENGINE),str(budget),"1","1000","fanout_fine_adaptive",str(cap),f"polish_order={order}"],input=encode(inst,sub),text=True,capture_output=True,timeout=8)
                    self.assertEqual(run.returncode,0);result,stats=decode(inst,run.stdout)
                    checked=check(inst,result);self.assertTrue(checked.legal);self.assertLessEqual(checked.total_delay,48);self.assertLessEqual(stats["expansions"],cap)
                    if cap==1000:self.assertEqual(checked.total_delay,22)
                    counters=json.loads(run.stderr.splitlines()[-1]);self.assertEqual(counters["polish_order"],order)
                    self.assertLessEqual(counters["polish_improvements"],counters["polish_completed"])
                    outputs.append(run.stdout)
                self.assertEqual(*outputs)

    def test_repair_first_repetition_and_interrupted_checkpoint(self):
        path=[(x,0,0) for x in range(5)]+[(4,y,0) for y in range(1,5)]
        inst,sub=make(5,5,[6,2],3,(0,0,0),[(4,4,0)],own_edges=list(zip(path,path[1:])))
        for cap in (2,3,13):
            for work in (1,25,100):
                outputs=[]
                for budget in (2,5):
                    run=subprocess.run([str(ENGINE),str(budget),"1","1000","fanout_fine_adaptive",str(work),"repair_first=1",f"group_limit={cap}"],input=encode(inst,sub),text=True,capture_output=True,timeout=8)
                    self.assertEqual(run.returncode,0)
                    result,stats=decode(inst,run.stdout);checked=check(inst,result)
                    self.assertTrue(checked.legal);self.assertLessEqual(checked.total_delay,check(inst,sub).total_delay)
                    self.assertLessEqual(stats["expansions"],work)
                    counters=json.loads(run.stderr.splitlines()[-1]);self.assertEqual(counters["repair_first"],1)
                    self.assertFalse(any(counters["group_size_histogram"][cap+1:]))
                    outputs.append(run.stdout)
                self.assertEqual(*outputs)

    def test_group_limit_caps_actual_transaction_sizes(self):
        path=[(x,0,0) for x in range(5)]+[(4,y,0) for y in range(1,5)]
        inst,sub=make(5,5,[6,2],3,(0,0,0),[(4,4,0)],own_edges=list(zip(path,path[1:])))
        for limit in (2,3,7,13):
            run=subprocess.run([str(ENGINE),"2","1","1000","fanout_fine_adaptive","1000",f"group_limit={limit}"],input=encode(inst,sub),text=True,capture_output=True,timeout=5)
            self.assertEqual(run.returncode,0)
            result,stats=decode(inst,run.stdout);self.assertTrue(check(inst,result).legal)
            counters=json.loads(run.stderr.splitlines()[-1])
            self.assertEqual(counters["group_limit"],limit)
            self.assertFalse(any(counters["group_size_histogram"][limit+1:]))

    def test_schedule_parser_defaults_and_rejections(self):
        inst,sub=make(3,1,[1],1,(0,0,0),[(2,0,0)],own_edges=[((0,0,0),(1,0,0)),((1,0,0),(2,0,0))])
        base=[str(ENGINE),"2","1","100","fanout_fine","100"]
        def invoke(args):
            return subprocess.run(base+args,input=encode(inst,sub),text=True,capture_output=True,timeout=5)
        old=invoke([]); explicit=invoke(["present_initial=2","present_step=2","history_step=2","group_limit=13","repair_first=0","polish_order=0"])
        self.assertEqual(old.returncode,0);self.assertEqual(explicit.returncode,0)
        self.assertEqual(old.stdout,explicit.stdout)
        for args in (["unknown=1"],["history_step=-1"],["present_step=65"],["present_initial="],
                     ["history_step=2","history_step=3"],["present_step=999999999999999999999999"],["history_step"],["group_limit=1"],["group_limit=14"],["repair_first=2"],["polish_order=3"]):
            self.assertEqual(invoke(args).returncode,2)

    def test_work_cap_is_exact_repeatable_and_preserves_legal_routes(self):
        inst,sub=make(5,5,[6,2],3,(0,0,0),[(4,4,0)],own_edges=[
            *(( (x,0,0),(x+1,0,0)) for x in range(4)),
            *(( (4,y,0),(4,y+1,0)) for y in range(4))])
        for mode in ["astar","fanout_astar","fanout_tight","fanout_fine","treecost","restart_astar","fanout_walk",*NEIGHBORHOOD_MODES]:
            for limit in (1,10,25,100):
                outputs=[]
                for wall in (2,5):
                    run=subprocess.run([str(ENGINE),str(wall),"7","100",mode,str(limit)],
                        input=encode(inst,sub),text=True,capture_output=True,timeout=8)
                    self.assertEqual(run.returncode,0,run.stderr)
                    out,stats=decode(inst,run.stdout)
                    self.assertLessEqual(stats["expansions"],limit)
                    self.assertTrue(check(inst,out).legal)
                    self.assertEqual(check(inst,out).total_delay,stats["total_delay"])
                    outputs.append(run.stdout)
                self.assertEqual(*outputs)

if __name__=="__main__":
    unittest.main(verbosity=2)
