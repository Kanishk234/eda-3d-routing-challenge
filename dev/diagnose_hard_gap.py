"""Compare checked public geometry with local routes; never use it as a warm start."""
import json
import sys
from collections import defaultdict
from pathlib import Path
from measure import ROOT, OFFICIAL, digest, save
sys.path.insert(0, str(OFFICIAL))
from m3d.model import Instance, Submission
from m3d.checker import check


def main():
    audit = json.loads((ROOT/'docs/evidence/phase3/current-public-hard.json').read_text())
    public = max(audit['entries'], key=lambda e: e['result']['aggregate_score'])
    coverage = json.loads((ROOT/'docs/evidence/phase3/tier-followup-coverage.json').read_text())
    local = next(r for r in coverage['rows'] if r['tier']=='hard')
    directory = ROOT/'dev/artifacts'/local['run_id']/'routes'
    suite = json.loads((OFFICIAL/'benchmarks_hard/suite.json').read_text())
    records=[]; cases=[]; groups=defaultdict(lambda: {'nets':0,'local_delay':0,'public_delay':0,'signed_gap':0})
    for case in suite['cases']:
        inst=Instance.load(OFFICIAL/'benchmarks_hard'/case['instance_file'])
        ours=directory/(case['name']+'.sol.json')
        theirs=ROOT/public['local_routes']/ours.name
        assert digest(theirs)==public['output_hashes'][ours.name]
        results=[check(inst, Submission.load(path)) for path in (ours,theirs)]
        assert all(r.legal for r in results)
        costs=[{n.net:n.delay for n in r.nets} for r in results]
        pins={p.id:p for p in inst.pins}
        for net in inst.nets:
            terminals=[pins[p] for p in [net.driver,*net.sinks]]
            span=sum(max(getattr(p,a) for p in terminals)-min(getattr(p,a) for p in terminals) for a in ('x','y'))
            fanout=len(net.sinks)
            row={'case':case['name'],'net':net.id,'fanout':fanout,'xy_span':span,
                 'terminal_layers':sorted({p.z for p in terminals}),
                 'local_delay':costs[0][net.id],'public_delay':costs[1][net.id],
                 'signed_gap':costs[0][net.id]-costs[1][net.id]}
            records.append(row)
            for category in (f'fanout:{"1" if fanout==1 else "2-4" if fanout<=4 else "5+"}',
                             f'xy_span:{"<20" if span<20 else "20-49" if span<50 else "50+"}',
                             f'terminal_layers:{len(row["terminal_layers"])}'):
                g=groups[category];g['nets']+=1
                for key in ('local_delay','public_delay','signed_gap'):g[key]+=row[key]
        cases.append({'case':case['name'],'local_delay':results[0].total_delay,
                      'public_delay':results[1].total_delay,'local_sha256':digest(ours),'public_sha256':digest(theirs)})
    positive=sorted((r for r in records if r['signed_gap']>0),key=lambda r:r['signed_gap'],reverse=True)
    total_positive=sum(r['signed_gap'] for r in positive)
    report={'local_run':local['run_id'],'public_pr':public['pr'],'public_head':public['head'],
            'cases':cases,'groups':dict(groups),'nets':records,'top_20_positive_gaps':positive[:20],
            'positive_gap_sum':total_positive,'top_20_positive_gap_fraction':sum(r['signed_gap'] for r in positive[:20])/total_positive,
            'limitations':'Signed per-net geometry comparison, not independent improvement potential. Changing one net can displace others. Public routes are analysis inputs only; no public warm starts.'}
    save(ROOT/'docs/evidence/phase3/hard-gap-diagnosis.json',report)
    print(json.dumps({k:report[k] for k in ('positive_gap_sum','top_20_positive_gap_fraction','groups')},indent=2))


if __name__=='__main__': main()
