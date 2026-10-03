"""Frozen NDS proposes net neighborhoods through an explicit VRP proxy.

Net centers -> customers, relative vertex footprint -> demand, spatial bins
-> tours, and nearest centers -> tour neighbors. This is not an equivalence
between vehicle routing and chip trees. No training or quality claim here.
"""
import argparse
import collections
import importlib.util
import json
import time
import typing
from pathlib import Path
from types import SimpleNamespace
from branch_repair import Router
from measure import ROOT, OFFICIAL, digest, save
from run_polish import Instance, Submission, check


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--coverage',type=Path,required=True)
    p.add_argument('--cases',nargs='+',default=['case_01','case_04','case_07'])
    p.add_argument('--model-dir',type=Path,default=Path('dev/artifacts/nds-pretrained'))
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();assert not a.out.exists()
    import torch,numpy as np
    from omegaconf import DictConfig,ListConfig,OmegaConf
    from omegaconf.base import Metadata,ContainerMetadata
    from omegaconf.nodes import AnyNode
    manifest=json.loads((a.model_dir/'manifest.json').read_text())
    assert all(digest(a.model_dir/f['path'])==f['sha256'] for f in manifest['files'])
    allowed=[dict,list,int,collections.defaultdict,typing.Any,DictConfig,ListConfig,Metadata,ContainerMetadata,AnyNode,
             (np._core.multiarray.scalar,'numpy.core.multiarray.scalar'),np.dtype,type(np.dtype('float64'))]
    with torch.serialization.safe_globals(allowed):
        checkpoint=torch.load(a.model_dir/'models/cvrp_100/checkpoint-2000.pt',map_location='cpu',weights_only=True)
    params=OmegaConf.to_container(checkpoint['model_params'],resolve=False)
    params.update(problem='cvrp',eval_type='argmax')
    spec=importlib.util.spec_from_file_location('licensed_nds_model',a.model_dir/'src/model.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    torch.set_num_threads(1);torch.manual_seed(64)
    model=module.Model(**params);model.load_state_dict(checkpoint['model_state_dict'],strict=True);model.eval()
    stage=next(r for r in json.loads(a.coverage.read_text())['rows'] if r['tier']=='hard');suite=stage['config']['suite']
    inventory=json.loads((OFFICIAL/suite/'suite.json').read_text())
    assert set(a.cases)<={c['name'] for c in inventory['cases']}
    report=dict(complete=False,model_manifest=manifest,coverage_sha256=digest(a.coverage),source_sha256=digest(Path(__file__)),
                rows=[],scope=__doc__,torch_version=torch.__version__,threads=1,seed=64)
    for case in inventory['cases']:
        if case['name'] not in a.cases:continue
        path=OFFICIAL/suite/case['instance_file'];inst=Instance.load(path)
        parent=ROOT/'dev/artifacts'/stage['run_id']/'routes'/(case['name']+'.sol.json');sub=Submission.load(parent);assert check(inst,sub).legal
        router=Router(inst,sub,1,1,1);ids=[n.id for n in inst.nets];count=len(ids);assert count>=4
        centers=[];demands=[]
        for n in inst.nets:
            pins=[router.pins[p] for p in n.pins()]
            centers.append([sum(v[0] for v in pins)/len(pins)/max(1,inst.width-1),
                            sum(v[1] for v in pins)/len(pins)/max(1,inst.height-1)])
            demands.append(min(1.0,len(router.vertices(router.routes[n.id]))/(0.1*inst.width*inst.height*inst.layers)))
        xy=torch.tensor([centers]);demand=torch.tensor([demands])
        nearest=[[j for j in sorted(range(count),key=lambda j:(sum((centers[i][k]-centers[j][k])**2 for k in range(2)),j)) if j!=i] for i in range(count)]
        neighbors=torch.tensor([[[row[0]+1,row[1]+1] for row in nearest]])
        tours=torch.tensor([[min(3,int(x*4))+4*min(3,int(y*4)) for x,y in centers]])
        reset=SimpleNamespace(problem_feat=SimpleNamespace(depot_xy=xy.mean(1,keepdim=True),node_xy=xy,node_demand=demand),neighbours=neighbors,tour_index=tours)
        z=torch.randn(1,count,params['z_dim'])
        mask=torch.full((1,count,count+1),float('-inf'))
        for i,row in enumerate(nearest):mask[0,i,[j+1 for j in row[:12]]]=0
        state=SimpleNamespace(BATCH_IDX=torch.zeros(1,count,dtype=torch.long),current_node=torch.arange(1,count+1).reshape(1,count),ninf_mask=mask)
        start=time.monotonic();groups=[[i] for i in range(count)]
        with torch.inference_mode():
            model.pre_forward(reset,z)
            for _ in range(3):
                selected,_,prob=model(state);assert torch.isfinite(prob).all()
                for i,value in enumerate(selected[0].tolist()):
                    assert value>0 and value-1 not in groups[i];groups[i].append(value-1)
                    state.ninf_mask[0,i,value]=float('-inf')
                state.current_node=selected
        spatial=[[i,*nearest[i][:3]] for i in range(count)]
        report['rows'].append(dict(tier='hard',case=case['name'],case_sha256=digest(path),parent_sha256=digest(parent),net_ids=ids,
                                  neural_groups=groups,spatial_groups=spatial,inference_wall_s=time.monotonic()-start,
                                  proxy_centers=centers,proxy_demands=demands,finite_probabilities=True))
    report['complete']=True;save(a.out,report)
    print([(r['case'],len(r['neural_groups']),r['inference_wall_s']) for r in report['rows']])


if __name__=='__main__':main()
