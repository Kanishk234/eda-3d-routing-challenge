"""Own CPU policies for congestion-dependent fresh sequential construction.
Teacher labels come from own sampled orders on disjoint synthetic training
layouts; no incumbent/competitor geometry or pretrained routing labels.
"""
import argparse,json,math,random,time,resource
from pathlib import Path
from learned_fresh_order import synthetic,features,candidate_orders,construct
from branch_repair import Router,Limit
from run_polish import Submission,NetRoute,check
from measure import ROOT,digest,save

def curriculum(seed):
 inst=synthetic(seed);cap=[4,6,10][seed%3];inst.nets=inst.nets[:cap];keep={p for n in inst.nets for p in n.pins()};inst.pins=[p for p in inst.pins if p.id in keep];inst.name='curriculum_'+str(seed);return inst

def new_router(inst,work=1000000,seconds=30):
 empty=Submission(inst.name,[NetRoute(n.id,[]) for n in inst.nets]);r=Router(inst,empty,work,seconds,1);r.owner={};return r

def context(r,remaining,base):
 occupied=list(r.owner);result={};pins=r.pins
 for nid in remaining:
  n=r.nets[nid];points=[pins[p] for p in n.pins()];xs=[v[0] for v in points];ys=[v[1] for v in points]
  lo,hi=min(xs),max(xs);bottom,top=min(ys),max(ys);area=(hi-lo+1)*(top-bottom+1)*r.inst.layers
  density=sum(lo<=x<=hi and bottom<=y<=top for x,y,z in occupied)/area
  free=[];near=[]
  for point in points:
   neighbors=[v for v,w in r.neighbors(point)];free.append(sum(v not in r.owner and r.pin_owner.get(v,nid)==nid for v in neighbors)/max(1,len(neighbors)))
   near.append(sum(abs(x-point[0])+abs(y-point[1])+abs(z-point[2])<=2 for x,y,z in occupied)/25)
  other_pins=sum(lo<=pins[p][0]<=hi and bottom<=pins[p][1]<=top for j in remaining if j!=nid for p in r.nets[j].pins())/area
  result[nid]=base[nid]+[density,min(free),sum(free)/len(free),max(near),other_pins,len(occupied)/(r.inst.width*r.inst.height*r.inst.layers),len(remaining)/len(r.nets)]
 return result

def follow(inst,order,examples=None,stats=None):
 r=new_router(inst);remaining=list(order);base=features(inst)
 for nid in order:
  if examples is not None:examples.append((context(r,remaining,base),nid))
  n=r.nets[nid];tree=r.search(nid,{r.pins[s] for s in n.sinks},NetRoute(nid,[]),set())
  if stats is not None:stats['expansions']=r.expansions
  if tree is None:return None
  r.routes[nid]=tree;r.owner.update({v:nid for v in r.vertices(tree)});remaining.remove(nid)
 return r

def fit_linear(examples,epochs=100):
 weights=[0.0]*16
 for epoch in range(epochs):
  gradient=[0.0]*16;count=0
  for choices,target in examples:
   for nid,x in choices.items():
    if nid==target:continue
    delta=[a-b for a,b in zip(choices[target],x)];score=sum(a*b for a,b in zip(weights,delta));factor=1/(1+math.exp(max(-40,min(40,score))))
    for k,v in enumerate(delta):gradient[k]+=factor*v
    count+=1
  if count:
   for k in range(16):weights[k]+=.5*(gradient[k]/count-.005*weights[k])
 return weights

def run_policy(inst,name,model,seed,work=1000000,seconds=30):
 r=new_router(inst,work,seconds);base=features(inst);remaining=list(base);routes=[];rng=random.Random(seed);rng.shuffle(remaining);start=time.monotonic()
 try:
  while remaining:
   if name=='random':nid=remaining[0]
   elif name=='short_first':nid=min(remaining,key=lambda i:(base[i][5],i))
   else:
    c=context(r,remaining,base)
    if name=='pressure':nid=min(remaining,key=lambda i:(c[i][10],-c[i][9],i))
    elif name=='static_linear':nid=max(remaining,key=lambda i:(sum(a*b for a,b in zip(model['static_weights'],base[i])), -i))
    elif name=='context_linear':nid=max(remaining,key=lambda i:(sum(a*b for a,b in zip(model['context_weights'],c[i])),-i))
    elif name=='context_mlp':
     import torch
     ids=sorted(remaining)
     with torch.inference_mode():scores=model['mlp'](torch.tensor([c[i] for i in ids],dtype=torch.float32)).flatten().tolist()
     nid=max(zip(ids,scores),key=lambda pair:(pair[1],-pair[0]))[0]
    else:raise ValueError(name)
   n=r.nets[nid];tree=r.search(nid,{r.pins[s] for s in n.sinks},NetRoute(nid,[]),set())
   if tree is None:return None,dict(expansions=r.expansions,limited=False,completed_nets=len(routes),wall_s=time.monotonic()-start)
   routes.append(tree);r.owner.update({v:nid for v in r.vertices(tree)});remaining.remove(nid)
 except Limit:return None,dict(expansions=r.expansions,limited=True,completed_nets=len(routes),wall_s=time.monotonic()-start)
 out=Submission(inst.name,routes);checked=check(inst,out);assert checked.legal
 return out,dict(expansions=r.expansions,limited=False,completed_nets=len(routes),delay=checked.total_delay,wall_s=time.monotonic()-start)

def train_mlp(examples,epochs):
 import torch
 torch.set_num_threads(1);torch.manual_seed(19)
 model=torch.nn.Sequential(torch.nn.Linear(16,32),torch.nn.Tanh(),torch.nn.Linear(32,1));positive=[];negative=[]
 for choices,target in examples:
  for nid,x in choices.items():
   if nid!=target:positive.append(choices[target]);negative.append(x)
 if not positive:return model
 a=torch.tensor(positive,dtype=torch.float32);b=torch.tensor(negative,dtype=torch.float32);opt=torch.optim.Adam(model.parameters(),lr=.01)
 for _ in range(epochs):opt.zero_grad();loss=torch.nn.functional.softplus(-(model(a)-model(b))).mean();loss.backward();opt.step()
 return model.eval()

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();a.out.mkdir(parents=True)
 plan=json.loads(a.plan.read_text());frozen={str(q.resolve()):digest(q) for q in [a.plan,Path(__file__),ROOT/'dev/learned_fresh_order.py',ROOT/'dev/branch_repair.py']};start=time.monotonic();examples=[];static_examples=[];training=[];teacher_work=0;report=dict(status='training',plan=plan,source_sha256=frozen,training=training,validation=[],workers=1,scope='Own fresh synthetic sampled teachers; disjoint heldout layouts,all failures retained;CPU pairwise linear/MLP imitation,not RL. No official-tier claim.');save(a.out/'progress.json',report)
 for seed in plan['train_seeds']:
  inst=curriculum(seed);candidates=[]
  for order in candidate_orders(inst,random.Random(seed),plan['teacher_random_orders']):
   stats={};teacher=follow(inst,order,stats=stats);teacher_work+=stats.get('expansions',0)
   if teacher:
    checked=check(inst,Submission(inst.name,list(teacher.routes.values())));assert checked.legal;candidates.append((checked.total_delay,order))
  row=dict(seed=seed,feasible_sampled_orders=len(candidates),best_delay=None)
  if candidates:
   delay,order=min(candidates,key=lambda x:(x[0],x[1]));row['best_delay']=delay;static_examples.append((features(inst),order));assert follow(inst,order,examples) is not None
  training.append(row);save(a.out/'progress.json',report)
 from learned_fresh_order import train
 model=dict(static_weights=train(static_examples),context_weights=fit_linear(examples),mlp=train_mlp(examples,plan['mlp_epochs']))
 import torch
 torch.save(model['mlp'].state_dict(),a.out/'mlp.pt');save(a.out/'model.json',dict(static_weights=model['static_weights'],context_weights=model['context_weights'],feature_count=16,mlp_architecture='16,32,tanh,1',source_sha256=frozen,mlp_sha256=digest(a.out/'mlp.pt')))
 report.update(status='validation',training_decisions=len(examples),teacher_sampled_expansions=teacher_work,teacher_attempts=len(plan['train_seeds'])*(plan['teacher_random_orders']+4),teacher_scope='All sampled attempts counted; selected teacher replay and learner fitting add effort',torch_version=torch.__version__);save(a.out/'progress.json',report)
 for family,seeds in [('curriculum',plan['validation_seeds']),('original',plan.get('original_validation_seeds',[]))]:
  for seed in seeds:
   inst=curriculum(seed) if family=='curriculum' else synthetic(seed);row=dict(family=family,seed=seed,methods={})
   for name in plan['methods']:
    out,stats=run_policy(inst,name,model,seed,plan['work_budget'],plan['budget']);stats['legal']=out is not None
    if out:target=a.out/f'{family}-{seed}-{name}.sol.json';out.save(str(target));assert check(inst,Submission.load(str(target))).legal;stats['output_sha256']=digest(target)
    row['methods'][name]=stats
   report['validation'].append(row);save(a.out/'progress.json',report)
 assert all(digest(Path(p))==h for p,h in frozen.items());report.update(status='complete',wall_s=time.monotonic()-start,peak_rss_kb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,model_sha256=digest(a.out/'model.json'));save(a.out/'progress.json',report)
 print('complete',len(static_examples),'teachers',len(examples),'decisions',flush=True)
if __name__=='__main__':main()
