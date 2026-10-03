"""Extract best-bound vertex tolls for measured repair-neighborhood proposals."""
import argparse,json,os,platform,subprocess,time,sys
from pathlib import Path
import dual_bound
import run_polish as bridge
from measure import ROOT,OFFICIAL,REVISION,digest,save

def source_text(original):
 prefix=dual_bound.source_text(original)[:-len(dual_bound.TAIL)]
 source=dual_bound.TAIL
 old='  I best=0;';assert source.count(old)==1;source=source.replace(old,'  I best=0;std::vector<I> best_prices(engine.vcount,0);')
 old='best=std::max(best,bound);';assert source.count(old)==1;source=source.replace(old,'if(bound>best){best=bound;best_prices=prices;}')
 old='  std::cout<<"],\\\"best_lower_bound\\\":"<<best<<",\\\"expansions\\\":"<<engine.expansions<<"}\\n";'
 new=r'''  std::cout<<"],\"best_lower_bound\":"<<best<<",\"expansions\":"<<engine.expansions<<",\"hotspots\":[";
  std::vector<std::pair<I,int>> ranked;
  for(int v=0;v<engine.vcount;++v)if(best_prices[v]>0)ranked.emplace_back(best_prices[v],v);
  std::sort(ranked.begin(),ranked.end(),[](auto a,auto b){return a.first!=b.first?a.first>b.first:a.second<b.second;});
  for(std::size_t k=0;k<std::min<std::size_t>(256,ranked.size());++k){if(k)std::cout<<",";std::cout<<"["<<ranked[k].second<<","<<ranked[k].first<<"]";}
  std::cout<<"]}\n";'''
 assert source.count(old)==1;return prefix+source.replace(old,new)

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--coverage',type=Path,required=True);p.add_argument('--cases',nargs='+',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out=a.out.resolve();assert not a.out.exists();a.out.mkdir(parents=True);inputs=[a.coverage,ROOT/'dev/solver/exact_polish.cpp',Path(__file__),Path(dual_bound.__file__)];frozen={str(p.resolve()):digest(p) for p in inputs};cpp=a.out/'hotspots.cpp';cpp.write_text(source_text((ROOT/'dev/solver/exact_polish.cpp').read_text()));binary=a.out/'hotspots';cmd=['g++','-O3','-std=c++17','-Wall','-Wextra',str(cpp),'-o',str(binary)];subprocess.run(cmd,check=True);coverage=json.loads(a.coverage.read_text());report=dict(complete=False,upstream_revision=REVISION,frozen_sha256=frozen,source_sha256=digest(cpp),binary_sha256=digest(binary),build_command=cmd,machine=dict(hostname=platform.node(),os=platform.platform(),cpus=len(os.sched_getaffinity(0)),python=sys.version),rows=[],scope='Own legal parent inputs,64adaptive fractional-price iterations;top256positive vertex prices from best bound. Heuristic hotspots,not certified graph cuts or legal relaxed routes. Analysis cost is additional to routing work.');save(a.out/'report.json',report)
 for key in a.cases:
  tier,name=key.split('/');stage=next(x for x in coverage['rows'] if x['tier']==tier);suite=stage['config']['suite'];inv=json.loads((OFFICIAL/suite/'suite.json').read_text());case=next(x for x in inv['cases'] if x['name']==name);path=OFFICIAL/suite/case['instance_file'];parent=ROOT/'dev/artifacts'/stage['run_id']/'routes'/(name+'.sol.json');inst=bridge.Instance.load(path);sub=bridge.Submission.load(parent);checked=bridge.check(inst,sub);assert checked.legal;command=[str(binary),'64','1','max_sink','16','adaptive'];start=time.monotonic();run=subprocess.run(command,input=bridge.encode(inst,sub),capture_output=True,text=True,timeout=125,check=True);raw=json.loads(run.stdout);assert raw['best_lower_bound']<=checked.total_delay;assert all(0<=v<inst.width*inst.height*inst.layers and price>0 for v,price in raw['hotspots']);report['rows'].append(dict(tier=tier,case=name,case_sha256=digest(path),parent_sha256=digest(parent),parent_delay=checked.total_delay,command=command,wall_s=time.monotonic()-start,price_resolution=16,**raw));save(a.out/'report.json',report);print(key,len(raw['hotspots']),flush=True)
 assert all(digest(Path(p))==sha for p,sha in frozen.items());report['complete']=True;save(a.out/'report.json',report)
if __name__=='__main__':main()
