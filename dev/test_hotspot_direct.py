"""Direct neighborhoods must exercise groups and preserve legal rollback."""
import json,subprocess,tempfile,unittest
from pathlib import Path
from measure import ROOT
from evolution_hotspot_direct import mutation
import test_dual_hotspots as fixtures
from run_polish import encode,decode,check

class DirectHotspots(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory(dir=ROOT/'dev/artifacts');folder=Path(cls.tmp.name);source=(ROOT/'dev/solver/exact_polish.cpp').read_text();cpp=folder/'direct.cpp';cpp.write_text(mutation(source,'hotspot_direct4'));cls.binary=folder/'direct';subprocess.run(['g++','-O2','-std=c++17',str(cpp),'-o',str(cls.binary)],check=True)
 @classmethod
 def tearDownClass(cls):cls.tmp.cleanup()
 def test_direct_groups_obey_cap_and_work_interruption(self):
  i,s=fixtures.Hotspots.fixture(self);data=encode(i,s)+'M3DHOTSPOT1 1\n4 8\n'
  for budget in [1,100,10000]:
   p=subprocess.run([str(self.binary),'5','8','1000','fanout_fine_escape',str(budget),'group_limit=2','accept_equal=1'],input=data,capture_output=True,text=True,check=True);out,core=decode(i,p.stdout);r=check(i,out);self.assertTrue(r.legal);self.assertLessEqual(r.total_delay,11);self.assertLessEqual(core['expansions'],budget);c=json.loads(p.stderr);self.assertEqual(sum(c['group_size_histogram'][3:]),0)
   if budget==10000:self.assertGreater(c['hotspot_group_attempts'],0);self.assertGreater(c['hotspot_group_additions'],0)
 def test_direct_call_and_augmentation_do_not_duplicate(self):
  source=mutation((ROOT/'dev/solver/exact_polish.cpp').read_text(),'hotspot_direct2');self.assertIn('if(!hotspot_direct) augment_hotspot_group',source);self.assertIn('if(hotspot_direct)',source)
if __name__=='__main__':unittest.main()
