"""Bounded LLM-proposed source-variant evaluation, inspired by GR-Evolve.
This session's existing coding model proposes mutations; no nested AI, external
API, training or GR-Evolve scripts are invoked. Production files stay frozen.
"""
import argparse,json,math,subprocess,time,os,platform,sys
from pathlib import Path
import run_polish as bridge
from measure import ROOT,OFFICIAL,digest,save,source_identity

def mutation(source,kind):
 if kind=='control':return source
 assert kind in ('conflict_first','conflict_last','delayed_conflict_first','flow_conflict_first','rotate_order')
 anchor='            if(shuffled_groups) std::shuffle(routing_order.begin(),routing_order.end(),group_rng);'
 assert source.count(anchor)==1
 direction='<' if kind=='conflict_last' else '>'
 if kind=='rotate_order':
  addition="""
            auto prior_order=routing_order;
            routing_order=group;
            std::rotate(routing_order.begin(),routing_order.begin()+(iteration%routing_order.size()),routing_order.end());
            ++evolution_order_calls;
            evolution_order_changes+=(prior_order!=routing_order);"""
 else:
  guard='iteration>=3 && iteration%3==0' if kind=='delayed_conflict_first' else 'true'
  debt="""for(int j:routing_order) for(int v:nets[j].vertices)
                    conflict_debt[j]+=(usage[v]>1);"""
  if kind=='flow_conflict_first':
   debt="""for(int j:routing_order) {
                    auto counts=downstream_counts(nets[j]);
                    for(std::size_t k=0;k<nets[j].vertices.size();++k)
                        if(usage[nets[j].vertices[k]]>1) conflict_debt[j]=add(conflict_debt[j],counts[k]);
                }"""
  addition="""
            // LLM-proposed local ordering; no change to physical acceptance.
            if(GUARD) {
                auto prior_order=routing_order;
                std::vector<I> conflict_debt(nets.size(),0);
                DEBT
                std::stable_sort(routing_order.begin(),routing_order.end(),[&](int a,int b) {
                    return conflict_debt[a] DIRECTION conflict_debt[b];
                });
                ++evolution_order_calls;
                evolution_order_changes+=(prior_order!=routing_order);
            }""".replace('GUARD',guard).replace('DEBT',debt).replace('DIRECTION',direction)
 candidate=source.replace(anchor,anchor+addition)
 # Short synthetic mutation tests don't contain Engine/output anchors.
 if 'struct Engine {' in candidate:
  candidate=candidate.replace('struct Engine {','struct Engine {\n    std::uint64_t evolution_order_calls=0,evolution_order_changes=0;',1)
  # Locate the unique output line using a raw literal.
  output=r'<<",\"negotiation_rounds\":"<<negotiation_rounds'
  extra=r'<<",\"evolution_order_calls\":"<<evolution_order_calls<<",\"evolution_order_changes\":"<<evolution_order_changes'
  assert candidate.count(output)==1
  candidate=candidate.replace(output,extra+output)
 return candidate

def compare(rows,variant):
 pairs=[]
 for row in rows:
  if row['variant']!=variant:continue
  baseline=next(r for r in rows if r['variant']=='control' and (r['tier'],r['case'],r['seed'])==(row['tier'],row['case'],row['seed']))
  pairs.append((baseline['delay'],row['delay']))
 assert pairs
 return dict(variant=variant,wins=sum(b>a for b,a in pairs),ties=sum(b==a for b,a in pairs),losses=sum(b<a for b,a in pairs),geomean_score_ratio=math.exp(sum(math.log(b/a) for b,a in pairs)/len(pairs)),pairs=len(pairs))

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out=a.out.resolve();assert not a.out.exists();a.out.mkdir(parents=True);plan=json.loads(a.plan.read_text());assert 0<plan['work_budget']<=100000000;assert 0<plan['budget']<=60;coverage=json.loads((ROOT/plan['coverage']).read_text());source=ROOT/'dev/solver/exact_polish.cpp';original=source.read_text();mutator=mutation;operator_source=None
 if plan.get('mutation_family')=='basin':
  import evolution_basin_mutation as operators
  mutator=operators.mutation;operator_source=Path(operators.__file__)
 elif plan.get('mutation_family')=='mixed':
  import evolution_mixed_mutation as operators
  mutator=operators.mutation;operator_source=Path(operators.__file__)
 elif plan.get('mutation_family','ordering')!='ordering':raise ValueError('Unknown mutation family')
 frozen={str(q.resolve()):digest(q) for q in [source,ROOT/'dev/artifacts/build/exact_polish',ROOT/'dev/run_polish.py',ROOT/plan['coverage'],a.plan,Path(__file__)]};
 if operator_source is not None:
  frozen[str(operator_source.resolve())]=digest(operator_source);(a.out/operator_source.name).write_bytes(operator_source.read_bytes())
  if plan.get('mutation_family')=='mixed':
   extra=ROOT/'dev/evolution_basin_mutation.py';frozen[str(extra.resolve())]=digest(extra);(a.out/extra.name).write_bytes(extra.read_bytes())
 (a.out/'orchestration.py').write_bytes(Path(__file__).read_bytes());(a.out/'plan.json').write_bytes(a.plan.read_bytes());start=time.monotonic();flags=['-O3','-std=c++17','-Wall','-Wextra','-Wpedantic'];report=dict(status='running',plan=plan,source_identity=source_identity(),frozen_sha256=frozen,variants=[],rows=[],workers=1,machine=dict(hostname=platform.node(),os=platform.platform(),python=sys.version,compiler=subprocess.run(['g++','--version'],capture_output=True,text=True,check=True).stdout.splitlines()[0]),affinity_cpus=len(os.sched_getaffinity(0)),scope='LLM-proposed variants from current existing coding-agent session; independently implemented GR-Evolve-inspired measured loop,not execution/reproduction of its stack. Same parent/work caps,seeds,configs; concurrent native runs prevent isolated timing claims. No training,paid API or competitor routes. Development pilot only;reserved validation required before adoption.');save(a.out/'progress.json',report)
 try:
  binaries={}
  for kind in plan['variants']:
   folder=a.out/kind;folder.mkdir();cpp=folder/'solver.cpp';cpp.write_text(mutator(original,kind));binary=folder/'solver';cmd=['g++',*flags,str(cpp),'-o',str(binary)]
   with (folder/'build.log').open('w') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
   binaries[kind]=binary;report['variants'].append(dict(name=kind,source_sha256=digest(cpp),binary_sha256=digest(binary),build_command=cmd,proposal=plan.get('proposals',{}).get(kind,kind+'; isolated source mutation,physical scoring/rollback unchanged.' if kind!='control' else 'Immutable parent recompiled with same flags.')));save(a.out/'progress.json',report)
  # Interleave variants per case/seed; independent immutable parent for each.
  for item in plan['cases']:
   stage=next(r for r in coverage['rows'] if r['tier']==item['tier']);suite=stage['config']['suite'];inv=json.loads((OFFICIAL/suite/'suite.json').read_text());case=next(c for c in inv['cases'] if c['name']==item['case']);path=OFFICIAL/suite/case['instance_file'];parent=ROOT/'dev/artifacts'/stage['run_id']/'routes'/(case['name']+'.sol.json');inst=bridge.Instance.load(path);sub=bridge.Submission.load(parent);before=bridge.check(inst,sub);assert before.legal;data=bridge.encode(inst,sub)
   for seed in plan['seeds']:
    for kind in plan['variants']:
     assert all(digest(Path(q))==h for q,h in frozen.items());bridge.ENGINE=binaries[kind];directory=a.out/kind/f'{item["tier"]}-{case["name"]}-{seed}';process,raw=bridge.run_core(directory,data,plan['budget'],seed,plan.get('passes',1000),item['mode'],plan['work_budget'],item['settings']);assert process['exit_code']==0;out,core=bridge.decode(inst,raw);checked=bridge.check(inst,out);assert checked.legal and checked.total_delay==core['total_delay'] and checked.total_delay<=before.total_delay;assert core['expansions']==plan['work_budget'] or (plan.get('allow_natural_completion',False) and not core['budget_reached']),'Budget ended before matched work; cannot call this an equal-work comparison';assert {x.net:x.delay for x in checked.nets}==core['net_delays'];target=directory/'candidate.sol.json';out.save(str(target));assert bridge.check(inst,bridge.Submission.load(target)).legal
     report['rows'].append(dict(variant=kind,tier=item['tier'],case=case['name'],seed=seed,case_sha256=digest(path),parent_sha256=digest(parent),output_sha256=digest(target),before_delay=before.total_delay,delay=checked.total_delay,case_score=bridge.score_case(inst,out,case['baseline_total']).ratio,legal=True,core=core,process=process));save(a.out/'progress.json',report);print(kind,case['name'],seed,'gain',before.total_delay-checked.total_delay,flush=True)
  assert all(digest(Path(q))==h for q,h in frozen.items());report.update(status='complete',comparisons=[dict(tier=tier,**compare([r for r in report['rows'] if r['tier']==tier],v)) for tier in sorted({r['tier'] for r in report['rows']}) for v in plan['variants'] if v!='control'],wall_s=time.monotonic()-start);save(a.out/'progress.json',report);print(report['comparisons'],flush=True)
 except BaseException as error:report.update(status='failed',error=repr(error),wall_s=time.monotonic()-start);save(a.out/'progress.json',report);raise
if __name__=='__main__':main()
