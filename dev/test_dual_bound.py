"""Independent hand-optimum checks for conservative vertex-price bounds."""
import json,subprocess,tempfile,unittest
from pathlib import Path
from measure import ROOT
from dual_bound import source_text
from test_exact import make
from run_polish import encode,NetRoute

class DualBound(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory(dir=ROOT/'dev/artifacts');folder=Path(cls.tmp.name);cpp=folder/'bound.cpp';cpp.write_text(source_text((ROOT/'dev/solver/exact_polish.cpp').read_text()));cls.binary=folder/'bound';subprocess.run(['g++','-O2','-std=c++17',str(cpp),'-o',str(cls.binary)],check=True)
 @classmethod
 def tearDownClass(cls):cls.tmp.cleanup()
 def bound(self,inst,sub,model="uniform"):
  p=subprocess.run([str(self.binary),'16','4',model],input=encode(inst,sub),capture_output=True,text=True,check=True);return json.loads(p.stdout)
 def test_single_net_two_sinks_exact_empty_distance(self):
  edges=[((x,0,0),(x+1,0,0)) for x in range(4)]+[((0,y,0),(0,y+1,0)) for y in range(4)];i,s=make(5,5,[1],1,(0,0,0),[(4,0,0),(0,4,0)],own_edges=edges);r=self.bound(i,s);self.assertEqual(r['best_lower_bound'],8)
 def test_contested_multi_sink_bound_does_not_exceed_hand_optimum(self):
  a=[(0,1,0),(0,1,1),(1,1,1),(2,1,1),(2,1,0),(2,0,0)];i,s=make(3,3,[1,1],1,a[0],[(2,1,0),(2,0,0)],block=((1,0,0),(1,2,0)),own_edges=list(zip(a,a[1:])));s.routes[1]=NetRoute(1,[((1,0,0),(1,1,0)),((1,1,0),(1,2,0))]);
  for model in ['uniform','max_sink']:
   r=self.bound(i,s,model);self.assertEqual(r['iterations'][0]['lower_bound'],7);self.assertGreaterEqual(r['best_lower_bound'],7);self.assertLessEqual(r['best_lower_bound'],9)
 def test_expensive_layer_with_via_matches_hand14(self):
  path=[(x,0,0) for x in range(5)];i,s=make(5,1,[6,2],3,path[0],[path[-1]],own_edges=list(zip(path,path[1:])));self.assertEqual(self.bound(i,s)['best_lower_bound'],14)
if __name__=='__main__':unittest.main()
