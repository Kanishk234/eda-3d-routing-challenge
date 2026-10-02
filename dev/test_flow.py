"""Independent path-count oracles and rollback checks for tree-price hypotheses."""
import json,random,subprocess,tempfile,unittest
from pathlib import Path
from measure import ROOT
from test_exact import make
from run_polish import ENGINE,encode,decode,check

class FlowCounts(unittest.TestCase):
 def test_counts_match_hand_cases_and_individual_sink_paths(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);source=root/'flow.cpp';binary=root/'flow'
   source.write_text('#define main routing_engine_main\n#include '+json.dumps(str(ROOT/'dev/solver/exact_polish.cpp'))+'\n#undef main\nint main(){try {Net n;int nv,ns,ne;std::cin>>n.root>>nv>>ns>>ne;n.vertices.resize(nv);n.sinks.resize(ns);n.edges.resize(ne);for(int& v:n.vertices)std::cin>>v;for(int& v:n.sinks)std::cin>>v;for(auto& e:n.edges)std::cin>>e.first>>e.second;for(int c:downstream_counts(n))std::cout<<c<<" ";}catch(const std::exception&){return 2;}}\n')
   subprocess.run(['g++','-O2','-std=c++17',str(source),'-o',str(binary)],check=True,capture_output=True)
   def invoke(vertices,edges,driver,sinks):
    data=' '.join(map(str,[driver,len(vertices),len(sinks),len(edges),*vertices,*sinks,*[v for edge in edges for v in edge]]))
    return subprocess.run([str(binary)],input=data,text=True,capture_output=True,timeout=8)
   cases=[([0,1,2,3],[(0,1),(1,2),(2,3)],0,[2,3],[2,2,2,1]),([0,1,2,3,4,5],[(0,1),(1,2),(1,3),(3,4),(1,5)],0,[2,3,4],[3,3,1,2,1,0]),([0,1,2,3],[(0,1),(1,2),(2,3)],3,[0,1],[1,2,2,2])]
   for vertices,edges,driver,sinks,expected in cases:
    result=invoke(vertices,edges,driver,sinks);self.assertEqual(result.returncode,0);self.assertEqual(list(map(int,result.stdout.split())),expected)
   rng=random.Random(41)
   for _ in range(100):
    size=rng.randrange(2,30);vertices=list(range(size));edges=[(v,rng.randrange(v)) for v in range(1,size)];driver=rng.randrange(size);sinks=rng.sample([v for v in vertices if v!=driver],rng.randrange(1,size));adj=[[] for _ in vertices]
    for a,b in edges:adj[a].append(b);adj[b].append(a)
    expected=[0]*size
    # Separate breadth-first path search from each sink,then count its root path.
    for sink in sinks:
     paths=[(sink,[sink])];seen={sink};path=None
     for u,route in paths:
      if u==driver:path=route;break
      for v in adj[u]:
       if v not in seen:seen.add(v);paths.append((v,route+[v]))
     for v in path:expected[v]+=1
    result=invoke(vertices,edges,driver,sinks);self.assertEqual(result.returncode,0);self.assertEqual(list(map(int,result.stdout.split())),expected)
   self.assertEqual(invoke([],[],0,[1]).stdout,'')
   self.assertEqual(invoke([0,1,2],[(0,1)],0,[2]).returncode,2)
   self.assertEqual(invoke([0,1,2],[(0,1),(1,2),(2,0)],0,[2]).returncode,2)

 def test_price_modes_defaults_work_caps_and_official_legality(self):
  path=[(x,0,0) for x in range(5)]+[(4,y,0) for y in range(1,5)]
  inst,sub=make(5,5,[6,2],3,(0,0,0),[(4,0,0),(4,2,0),(4,4,0)],own_edges=list(zip(path,path[1:])))
  base=[str(ENGINE),'2','1','100','fanout_fine_escape','1000','repair_first=1','accept_equal=1']
  old=subprocess.run(base,input=encode(inst,sub),text=True,capture_output=True,check=True);explicit=subprocess.run(base+['tree_prices=0'],input=encode(inst,sub),text=True,capture_output=True,check=True);self.assertEqual(old.stdout,explicit.stdout)
  self.assertEqual(subprocess.run(base+['tree_prices=3'],input=encode(inst,sub),text=True,capture_output=True).returncode,2)
  for mode in (1,2):
   for limit in (1,20,100,1000):
    outputs=[]
    for wall in (2,5):
     run=subprocess.run([str(ENGINE),str(wall),'1','100','fanout_fine_escape',str(limit),'tree_prices='+str(mode),'repair_first=1','accept_equal=1'],input=encode(inst,sub),text=True,capture_output=True,check=True)
     out,stats=decode(inst,run.stdout);checked=check(inst,out);self.assertTrue(checked.legal);self.assertEqual(checked.total_delay,stats['total_delay']);self.assertLessEqual(checked.total_delay,check(inst,sub).total_delay);self.assertLessEqual(stats['expansions'],limit);outputs.append(run.stdout)
     if limit==1000:self.assertGreater(json.loads(run.stderr.splitlines()[-1])['flow_builds'],0)
    self.assertEqual(*outputs)

if __name__=='__main__':unittest.main(verbosity=2)
