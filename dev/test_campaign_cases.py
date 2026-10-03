"""Reject malformed case plans before any routing subprocess starts."""
import json,subprocess,sys,tempfile,unittest
from pathlib import Path
from measure import ROOT

class Campaign(unittest.TestCase):
 def test_invalid_design_name_fails_before_work(self):
  plan=json.loads((ROOT/'dev/configs/parallel-case-campaign.json').read_text());plan['cases']=[x for x in plan['cases'] if x['tier']=='designs'][:1];plan['cases'][0]['case']='case_01'
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'plan.json';p.write_text(json.dumps(plan));out=Path(d)/'out';r=subprocess.run([sys.executable,str(ROOT/'dev/campaign_cases.py'),str(p),'--out',str(out)],capture_output=True,text=True)
   self.assertNotEqual(r.returncode,0);self.assertIn('Unknown designs case: case_01',r.stderr);self.assertFalse((out/'progress.json').exists());self.assertEqual(list(out.iterdir()),[])
 def test_all_declared_names_exist(self):
  from measure import OFFICIAL
  plan=json.loads((ROOT/'dev/configs/parallel-case-campaign.json').read_text());coverage=json.loads((ROOT/plan['coverage']).read_text())
  for item in plan['cases']:
   stage=next(x for x in coverage['rows'] if x['tier']==item['tier']);names={x['name'] for x in json.loads((OFFICIAL/stage['config']['suite']/'suite.json').read_text())['cases']};self.assertIn(item['case'],names)
if __name__=='__main__':unittest.main()
