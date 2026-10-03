"""Compare frozen pretrained NDS groups against spatial and native controls."""
import json
import sys
from pathlib import Path
import evolution_pilot as pilot
from measure import ROOT, digest, save


def mutation(source, kind):
    if kind == 'control': return source
    assert kind in ['neural_groups', 'spatial_groups']
    choice = 'neural' if kind == 'neural_groups' else 'spatial'
    fields = '''
    std::vector<std::vector<int>> pretrained_groups;
    void read_pretrained_groups() {
        std::string magic;int count;
        if(!(std::cin>>magic>>count) || magic!="M3DNEURAL1" || count!=static_cast<int>(nets.size()))
            throw std::runtime_error("invalid neural group header");
        pretrained_groups.resize(count);
        for(int focal=0;focal<count;++focal) {
            std::vector<int> neural,spatial;
            for(auto* group:{&neural,&spatial}) {
                int size;if(!(std::cin>>size) || size<2 || size>13)throw std::runtime_error("invalid neural group size");
                std::set<int> seen;
                for(int j=0;j<size;++j){int v;if(!(std::cin>>v) || v<0 || v>=count || !seen.insert(v).second)throw std::runtime_error("invalid neural group index");group->push_back(v);}
                if(group->front()!=focal)throw std::runtime_error("invalid neural focal net");
            }
            pretrained_groups[focal]=CHOICE;
        }
    }
'''.replace('CHOICE', choice)
    replacements = [
        ('struct Engine {', 'struct Engine {\n'+fields),
        ('        engine.read(search_only);', '        engine.read(search_only);engine.read_pretrained_groups();'),
        ('                if(conflict_windows) {', '''                if(!pretrained_groups.empty()) {
                    group=pretrained_groups[index];
                    if(group.size()>static_cast<std::size_t>(max_blockers+1))group.resize(max_blockers+1);
                    if(group.size()<2){++no_gain;continue;}
                    ++attempts;
                } else if(conflict_windows) {'''),
        ('if(adaptive_groups && !(used_escape && escape_direct)) {',
         'if(pretrained_groups.empty() && adaptive_groups && !(used_escape && escape_direct)) {')]
    for anchor, replacement in replacements:
        assert source.count(anchor)==1, anchor
        source=source.replace(anchor,replacement,1)
    return source


def main():
    args=sys.argv;plan=json.loads(Path(args[1]).read_text());groups_path=ROOT/plan['neural_groups']
    groups=json.loads(groups_path.read_text());assert groups['complete']
    index={(r['tier'],r['case']):r for r in groups['rows']}
    coverage=json.loads((ROOT/plan['coverage']).read_text())
    frozen={str(p.resolve()):digest(p) for p in [Path(__file__),groups_path]}
    for item in plan['cases']:
        row=index[(item['tier'],item['case'])];stage=next(r for r in coverage['rows'] if r['tier']==item['tier'])
        parent=ROOT/'dev/artifacts'/stage['run_id']/'routes'/(item['case']+'.sol.json')
        assert digest(parent)==row['parent_sha256']
    old_run=pilot.bridge.run_core
    def with_groups(directory,data,*args,**kwargs):
        rows=[r for (tier,case),r in index.items() if directory.name.startswith(tier+'-'+case+'-')]
        assert len(rows)==1;row=rows[0];data+='M3DNEURAL1 '+str(len(row['neural_groups']))+'\n'
        for neural,spatial in zip(row['neural_groups'],row['spatial_groups']):
            for group in [neural,spatial]:data+=str(len(group))+' '+' '.join(map(str,group))+'\n'
        return old_run(directory,data,*args,**kwargs)
    pilot.bridge.run_core=with_groups;pilot.mutation=mutation;pilot.main()
    out=Path(args[args.index('--out')+1]);report=json.loads((out/'progress.json').read_text())
    assert all(digest(Path(p))==sha for p,sha in frozen.items())
    report['additional_source_sha256']=frozen
    report['pretrained_inference_wall_s']=sum(r['inference_wall_s'] for r in groups['rows'])
    report['scope']='Pretrained NDS VRP-proxy static neighborhoods vs same-size nearest-center groups and native control. No training. Exact physical delay/official legality govern acceptance. Matched routing work caps;extra inference cost disclosed. Proxy features and frozen groups are experimental transfer,not objective equivalence or full-tier claim.'
    (out/Path(__file__).name).write_bytes(Path(__file__).read_bytes());save(out/'progress.json',report)


if __name__=='__main__':main()
