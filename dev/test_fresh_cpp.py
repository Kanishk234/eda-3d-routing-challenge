import subprocess,unittest
from pathlib import Path
from test_exact import make
from run_polish import encode,decode,check
BINARY=Path(__file__).resolve().parent/'artifacts/build/fresh_probe'
def execute(inst,sub,work=100000,seconds=5,selective=1):
 p=subprocess.run([str(BINARY),str(seconds),'1','500',str(work),'aggressive',str(selective),'3'],input=encode(inst,sub),text=True,capture_output=True,timeout=10)
 if p.returncode:raise RuntimeError(p.stderr)
 out,stats=decode(inst,p.stdout);fresh=next(x for x in p.stderr.splitlines() if x.startswith('FRESH ')).split();return out,stats,int(fresh[1])
class CompiledFresh(unittest.TestCase):
 def test_fresh_physical_delay(self):
  # Supply a legal long-layer baseline, then construct from scratch.
  path=[(x,0,0) for x in range(5)]+[(4,y,0) for y in range(1,5)]
  inst,sub=make(5,5,[6,2],3,path[0],[path[-1]],own_edges=list(zip(path,path[1:])))
  out,stats,fresh=execute(inst,sub);self.assertEqual(fresh,1);self.assertTrue(check(inst,out).legal);self.assertEqual(check(inst,out).total_delay,22)
 def test_limit_restores_legal_input(self):
  path=[(0,0,0),(1,0,0),(2,0,0)];inst,sub=make(3,3,[1],1,path[0],[path[-1]],own_edges=list(zip(path,path[1:])))
  out,stats,fresh=execute(inst,sub,1);self.assertEqual(fresh,0);self.assertTrue(check(inst,out).legal);self.assertEqual(out.to_dict(),sub.to_dict())
 def test_old_geometry_not_fresh_seed(self):
  a=[(0,0,0),(1,0,0),(2,0,0)];b=[(0,0,0),(0,1,0),(1,1,0),(2,1,0),(2,0,0)]
  inst,s1=make(3,3,[1],1,a[0],[a[-1]],own_edges=list(zip(a,a[1:])))
  _,s2=make(3,3,[1],1,b[0],[b[-1]],own_edges=list(zip(b,b[1:])))
  x,_,fresh=execute(inst,s1);y,_,fresh2=execute(inst,s2);self.assertEqual(fresh,fresh2);self.assertEqual(x.to_dict(),y.to_dict())
if __name__=='__main__':unittest.main()
