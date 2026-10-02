"""CPU learned initial net ordering on fresh synthetic routing instances.

Pairwise imitation of the best own sampled order. No incumbent route geometry,
external training routes, neural dependency, or global optimality claim.
"""
import argparse,json,math,random,time
from pathlib import Path
from run_polish import Instance,Submission,NetRoute,check
from m3d.model import Pin,Net
from branch_repair import Router,Limit
from measure import digest,save

def synthetic(seed):
    rng=random.Random(seed);w=h=rng.choice([7,9,11]);layers=2
    vertices=[(x,y,z) for z in range(layers) for y in range(h) for x in range(w)];rng.shuffle(vertices)
    pins=[];nets=[]
    for nid in range(rng.randrange(5,11)):
        count=rng.randrange(2,5);ids=[]
        for _ in range(count):
            v=vertices.pop();pid=len(pins);pins.append(Pin(pid,nid,int(v[2]>0),*v));ids.append(pid)
        nets.append(Net(nid,ids[0],ids[1:]))
    return Instance('synthetic_'+str(seed),w,h,layers,[rng.randrange(1,5),rng.randrange(1,5)],rng.randrange(1,5),[],pins,nets)

def features(inst):
    pv=inst.pin_vertex();out={}
    for n in inst.nets:
        vertices=[pv[p] for p in n.pins()];xs=[v[0] for v in vertices];ys=[v[1] for v in vertices]
        dx=(max(xs)-min(xs))/inst.width;dy=(max(ys)-min(ys))/inst.height
        cross=sum(v[2]!=vertices[0][2] for v in vertices[1:])/max(1,len(n.sinks))
        span=sum(abs(v[0]-vertices[0][0])+abs(v[1]-vertices[0][1]) for v in vertices[1:])/(inst.width+inst.height)
        overlap=0
        for other in inst.nets:
            if other.id==n.id:continue
            points=[pv[p] for p in other.pins()]
            overlap+=int(min(x for x,y,z in points)<=max(xs) and max(x for x,y,z in points)>=min(xs) and min(y for x,y,z in points)<=max(ys) and max(y for x,y,z in points)>=min(ys))
        out[n.id]=[len(n.sinks)/4,dx,dy,dx*dy,cross,span,overlap/max(1,len(inst.nets)-1),vertices[0][2],inst.via_delay/max(inst.layer_delay)]
    return out

def construct(inst,order):
    empty=Submission(inst.name,[NetRoute(n.id,[]) for n in inst.nets]);router=Router(inst,empty,1000000,30,1);router.owner={};routes=[]
    for nid in order:
        n=router.nets[nid]
        try:tree=router.search(nid,{router.pins[s] for s in n.sinks},NetRoute(nid,[]),set())
        except Limit:return None
        if tree is None:return None
        routes.append(tree);router.owner.update({v:nid for v in router.vertices(tree)})
    out=Submission(inst.name,routes);checked=check(inst,out);assert checked.legal
    return out,checked.total_delay,router.expansions

def candidate_orders(inst,rng,trials):
    f=features(inst);ids=list(f);orders=[sorted(ids,key=lambda i:f[i][5]),sorted(ids,key=lambda i:-f[i][5]),sorted(ids,key=lambda i:-f[i][0]),sorted(ids,key=lambda i:-f[i][6])]
    for _ in range(trials):order=ids.copy();rng.shuffle(order);orders.append(order)
    return orders

def train(examples,epochs=80):
    weights=[0.0]*9
    for epoch in range(epochs):
        gradient=[0.0]*9;count=0
        for features_,order in examples:
            for rank,a in enumerate(order):
                for b in order[rank+1:]:
                    delta=[x-y for x,y in zip(features_[a],features_[b])];score=sum(w*x for w,x in zip(weights,delta));factor=1/(1+math.exp(max(-40,min(40,score))))
                    for k,x in enumerate(delta):gradient[k]+=factor*x
                    count+=1
        if not count:break
        for k in range(9):weights[k]+=0.5*(gradient[k]/count-0.01*weights[k])
    return weights

def order_model(inst,weights):
    f=features(inst);return sorted(f,key=lambda i:(-sum(w*x for w,x in zip(weights,f[i])),i))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();a.out.mkdir(parents=True)
    sources=[Path(__file__),Path(__file__).with_name('branch_repair.py')];frozen={str(p.resolve()):digest(p) for p in sources};start=time.monotonic();examples=[];training=[];rng=random.Random(17)
    for seed in range(1001,1025):
        inst=synthetic(seed);candidates=[]
        for order in candidate_orders(inst,rng,12):
            result=construct(inst,order)
            if result:candidates.append((result[1],order,result[2]))
        if candidates:
            best=min(candidates,key=lambda x:(x[0],x[1]));examples.append((features(inst),best[1]));training.append(dict(seed=seed,legal_orders=len(candidates),best_delay=best[0]))
        else:training.append(dict(seed=seed,legal_orders=0,best_delay=None))
    weights=train(examples);model=dict(weights=weights,features=['fanout','bbox_x','bbox_y','bbox_area','cross_layer','total_xy_span','bbox_overlap','driver_layer','via_layer_ratio'],training=training,source_sha256=frozen,scope='Pairwise imitation of best own finite sampled fresh orders on synthetic layouts; not reinforcement learning,not a pretrained external model.');save(a.out/'model.json',model)
    validation=[]
    for seed in range(9001,9025):
        inst=synthetic(seed);f=features(inst);ids=list(f);random_order=ids.copy();random.Random(seed).shuffle(random_order)
        methods=dict(learned=order_model(inst,weights),short_first=sorted(ids,key=lambda i:f[i][5]),long_first=sorted(ids,key=lambda i:-f[i][5]),fanout_first=sorted(ids,key=lambda i:-f[i][0]),random=random_order)
        row=dict(seed=seed,methods={})
        for name,order in methods.items():
            result=construct(inst,order);row['methods'][name]=dict(legal=bool(result),delay=result[1] if result else None,expansions=result[2] if result else None)
            if result:result[0].save(str(a.out/f'{seed}-{name}.sol.json'))
        validation.append(row)
    assert all(digest(Path(p))==sha for p,sha in frozen.items());save(a.out/'report.json',dict(status='complete',training=training,validation=validation,weights=weights,wall_s=time.monotonic()-start,source_sha256=frozen,model_sha256=digest(a.out/'model.json'),scope='Fresh synthetic train/validation seeds disjoint. One constructive attempt per method; no official-tier or generalization gain claim. Incomplete construction retained as failure,not silently omitted.'))
    print('train cases',len(examples),'validation',len(validation),flush=True)
if __name__=='__main__':main()
