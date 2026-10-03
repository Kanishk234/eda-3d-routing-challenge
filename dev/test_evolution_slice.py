"""Exercise work-slice interruption and legality on a hand-checked layout."""
import json,subprocess,tempfile,unittest
from pathlib import Path
from evolution_slice import mutation
from test_exact import make
from run_polish import encode,decode,check,NetRoute
from measure import ROOT

class WorkSlice(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory(dir=ROOT/'dev/artifacts');folder=Path(cls.tmp.name);original=(ROOT/'dev/solver/exact_polish.cpp').read_text();cls.binaries={}
  for kind in ['slice10','slice25']:
   cpp=folder/(kind+'.cpp');cpp.write_text(mutation(original,kind));binary=folder/kind;subprocess.run(['g++','-O2','-std=c++17',str(cpp),'-o',str(binary)],check=True);cls.binaries[kind]=binary
 @classmethod
 def tearDownClass(cls):cls.tmp.cleanup()
 def fixture(self):
  a=[(0,1,0),(0,1,1),(1,1,1),(2,1,1),(2,1,0),(2,0,0)];i,s=make(3,3,[1,1],1,a[0],[(2,1,0),(2,0,0)],block=((1,0,0),(1,2,0)),own_edges=list(zip(a,a[1:])));s.routes[1]=NetRoute(1,[((1,0,0),(1,1,0)),((1,1,0),(1,2,0))]);return i,s
 def test_work_interruption_preserves_legal_nonworsening_output(self):
  i,s=self.fixture();self.assertEqual(check(i,s).total_delay,11)
  for kind,binary in self.binaries.items():
   for budget in [1,100,10000]:
    with self.subTest(kind=kind,budget=budget):
     p=subprocess.run([str(binary),'5','1','1000','fanout_fine_escape',str(budget),'accept_equal=1','group_limit=2'],input=encode(i,s),capture_output=True,text=True,check=True);out,core=decode(i,p.stdout);r=check(i,out);self.assertTrue(r.legal);self.assertLessEqual(r.total_delay,11);self.assertEqual(r.total_delay,core['total_delay']);self.assertLessEqual(core['expansions'],budget)
 def test_control_is_byte_identical(self):
  source=(ROOT/'dev/solver/exact_polish.cpp').read_text();self.assertEqual(mutation(source,'control'),source)
if __name__=='__main__':unittest.main()
