"""Hand-cost, parser and interruption checks for hotspot proposals."""
import json,subprocess,tempfile,unittest
from pathlib import Path
from measure import ROOT
from dual_hotspots import source_text
from evolution_hotspot import mutation
from test_exact import make
from run_polish import encode,decode,check,NetRoute

class Hotspots(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory(dir=ROOT/'dev/artifacts');folder=Path(cls.tmp.name);original=(ROOT/'dev/solver/exact_polish.cpp').read_text();cls.binary={}
  for name,source in [('analysis',source_text(original)),('router',mutation(original,'hotspot2'))]:
   cpp=folder/(name+'.cpp');cpp.write_text(source);binary=folder/name;subprocess.run(['g++','-O2','-std=c++17',str(cpp),'-o',str(binary)],check=True);cls.binary[name]=binary
 @classmethod
 def tearDownClass(cls):cls.tmp.cleanup()
 def fixture(self):
  a=[(0,1,0),(0,1,1),(1,1,1),(2,1,1),(2,1,0),(2,0,0)];i,s=make(3,3,[1,1],1,a[0],[(2,1,0),(2,0,0)],block=((1,0,0),(1,2,0)),own_edges=list(zip(a,a[1:])));s.routes[1]=NetRoute(1,[((1,0,0),(1,1,0)),((1,1,0),(1,2,0))]);return i,s
 def test_extract_preserves_hand_bound_and_valid_positive_prices(self):
  i,s=self.fixture();p=subprocess.run([str(self.binary['analysis']),'32','1','max_sink','16','adaptive'],input=encode(i,s),capture_output=True,text=True,check=True);r=json.loads(p.stdout);self.assertGreaterEqual(r['best_lower_bound'],7);self.assertLessEqual(r['best_lower_bound'],9);self.assertTrue(all(0<=v<18 and price>0 for v,price in r['hotspots']));self.assertLessEqual(len(r['hotspots']),256)
 def test_work_interruption_remains_legal_and_deterministic(self):
  i,s=self.fixture();data=encode(i,s)+'M3DHOTSPOT1 1\n4 8\n';cmd=[str(self.binary['router']),'5','7','1000','fanout_fine_escape','3000','accept_equal=1','group_limit=2'];outputs=[]
  for _ in range(2):
   p=subprocess.run(cmd,input=data,capture_output=True,text=True,check=True);out,core=decode(i,p.stdout);checked=check(i,out);self.assertTrue(checked.legal);self.assertLessEqual(checked.total_delay,11);self.assertLessEqual(core['expansions'],3000);self.assertEqual(checked.total_delay,core['total_delay']);outputs.append(p.stdout)
  self.assertEqual(*outputs)
 def test_rejects_invalid_hotspot_trailer(self):
  i,s=self.fixture()
  for tail in ['M3DHOTSPOT1 1\n18 8\n','M3DHOTSPOT1 1\n4 -1\n','WRONG 0\n']:
   p=subprocess.run([str(self.binary['router']),'1','1','1','fanout_fine_escape','100'],input=encode(i,s)+tail,capture_output=True,text=True);self.assertNotEqual(p.returncode,0)
 def test_control_is_original_source(self):
  original=(ROOT/'dev/solver/exact_polish.cpp').read_text();self.assertEqual(mutation(original,'control'),original)
if __name__=='__main__':unittest.main()
