import subprocess
import tempfile
import unittest
from pathlib import Path
from evolution_neural_groups import mutation
from measure import ROOT
from run_polish import Instance,Submission,NetRoute,encode,decode,check
from m3d.model import Pin,Net


class NeuralGroups(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory(dir=ROOT/'dev/artifacts')
        directory=Path(cls.temp.name);cpp=directory/'solver.cpp'
        cpp.write_text(mutation((ROOT/'dev/solver/exact_polish.cpp').read_text(),'neural_groups'))
        cls.binary=directory/'solver'
        subprocess.run(['g++','-O2','-std=c++17',str(cpp),'-o',str(cls.binary)],check=True)

    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()

    def fixture(self):
        pins=[];nets=[];routes=[]
        for i in range(4):
            pins.extend([Pin(2*i,i,0,0,i,0),Pin(2*i+1,i,0,2,i,0)])
            nets.append(Net(i,2*i,[2*i+1]))
            routes.append(NetRoute(i,[((0,i,0),(1,i,0)),((1,i,0),(2,i,0))]))
        inst=Instance('toy',3,4,1,[1],2,[],pins,nets)
        return inst,Submission(inst.name,routes)

    def trailer(self):
        rows=['M3DNEURAL1 4']
        for i in range(4):
            group=[i,*[j for j in range(4) if j!=i]]
            rows.extend(['4 '+' '.join(map(str,group))]*2)
        return '\n'.join(rows)+'\n'

    def test_control_identity_and_unique_anchors(self):
        original=(ROOT/'dev/solver/exact_polish.cpp').read_text()
        self.assertEqual(mutation(original,'control'),original)
        with self.assertRaises(AssertionError):mutation(original+'\nstruct Engine {','neural_groups')

    def test_deterministic_work_limit_preserves_legal_trees(self):
        inst,sub=self.fixture();outputs=[]
        for _ in range(2):
            p=subprocess.run([str(self.binary),'5','7','1000','fanout_fine_escape','3000','group_limit=2'],input=encode(inst,sub)+self.trailer(),text=True,capture_output=True,check=True)
            candidate,core=decode(inst,p.stdout);r=check(inst,candidate)
            self.assertTrue(r.legal);self.assertEqual(r.total_delay,8)
            self.assertLessEqual(core['expansions'],3000);outputs.append(p.stdout)
        self.assertEqual(*outputs)

    def test_invalid_group_indices_and_focal_rejected(self):
        inst,sub=self.fixture();valid=self.trailer()
        for bad in [valid.replace('4 0 1 2 3','4 0 0 2 3',1),valid.replace('4 0 1 2 3','4 0 1 2 4',1),valid.replace('4 0 1 2 3','4 1 0 2 3',1)]:
            p=subprocess.run([str(self.binary),'1','1','1','fanout_fine_escape','100'],input=encode(inst,sub)+bad,text=True,capture_output=True)
            self.assertNotEqual(p.returncode,0)


if __name__=='__main__':unittest.main()
