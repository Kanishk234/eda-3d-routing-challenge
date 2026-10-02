"""Inspect published route artifacts only; never execute or warm-start from them."""
import json
from measure import ROOT, OFFICIAL, REVISION, digest, save
from run_polish import route_resources
from m3d.model import Instance, Submission
from m3d.checker import check
from m3d.scorer import score_case, leaderboard


def main():
    revisions = ['ca3cb1de2c046546f2ed8fca14576f6056b8488d',
                 'd9cddc4cc365290f4c6f4d1752f460c46e03ddbe']
    source = ROOT / 'dev/artifacts/research-reubalink'
    our_report = ROOT / 'docs/evidence/phase3/tier-schedule-coverage.json'
    ours = next(r for r in json.loads(our_report.read_text())['rows'] if r['tier'] == 'hard')
    our_cases = {c['case']: c for c in ours['cases']}
    suite = OFFICIAL / 'benchmarks_hard/suite.json'
    manifest = json.loads(suite.read_text())
    report = {'repository': 'THOMACHAYAN/eda-3d-routing-challenge',
              'branch': 'reubalink-hard', 'upstream_revision': REVISION,
              'suite_sha256': digest(suite), 'our_coverage_sha256': digest(our_report),
              'our_recorded_score': ours['score']['aggregate_score'],
              'custom_solver_source_found_in_inspected_branches': False,
              'external_code_executed': False, 'public_routes_used_as_warm_starts': False,
              'revisions': [], 'cases': [], 'largest_positive_net_gaps': [],
              'limitations': 'Methods/timing from metadata and commit messages are author reports. '
              'Only output legality/delay are recomputed. Method and additional search effort are confounded. '
              'Our comparison uses recorded per-net results, not a fresh reproduction of our GitHub-best run. '
              'No inference of an exact implementation or global optimum from output trees.'}
    scores = {revision: [] for revision in revisions}
    categories = {name: {'nets': 0, 'our_delay': 0, 'public_delay': 0, 'positive_gap': 0}
                  for name in ('one_sink', 'multiple_sinks')}
    gaps = []
    for case in manifest['cases']:
        name = case['name']
        instance_path = OFFICIAL / 'benchmarks_hard' / case['instance_file']
        instance = Instance.load(instance_path)
        if digest(instance_path) != our_cases[name]['case_sha256']:
            raise RuntimeError('case identity differs from our recorded run')
        row = {'case': name, 'case_sha256': digest(instance_path),
               'our_recorded_delay': our_cases[name]['total_delay'], 'public': []}
        final_nets = None
        for revision in revisions:
            path = source / revision / 'routes' / (name + '.sol.json')
            submission = Submission.load(path)
            checked = check(instance, submission)
            if not checked.legal:
                raise RuntimeError(f'illegal published output: {name}/{revision}')
            score = score_case(instance, submission, case['baseline_total'])
            if score.total_delay != checked.total_delay:
                raise RuntimeError('official checking/scoring disagreement')
            scores[revision].append(score)
            row['public'].append({'revision': revision, 'legal': checked.legal,
                                  'delay': checked.total_delay, 'ratio': score.ratio,
                                  'output_sha256': digest(path), 'resources': route_resources(submission)})
            final_nets = {n.net: n.delay for n in checked.nets}
        recorded_nets = our_cases[name]['core']['net_delays']
        if sum(recorded_nets.values()) != row['our_recorded_delay']:
            raise RuntimeError('recorded net sum disagrees')
        for net in instance.nets:
            our_delay = recorded_nets[str(net.id)]
            their_delay = final_nets[net.id]
            group = categories['one_sink' if len(net.sinks) == 1 else 'multiple_sinks']
            group['nets'] += 1
            group['our_delay'] += our_delay
            group['public_delay'] += their_delay
            group['positive_gap'] += max(0, our_delay - their_delay)
            gaps.append({'case': name, 'net': net.id, 'sinks': len(net.sinks),
                         'our_delay': our_delay, 'public_delay': their_delay,
                         'gap': our_delay - their_delay})
        report['cases'].append(row)
    for revision in revisions:
        metadata = source / revision / 'meta.json'
        report['revisions'].append({'revision': revision, 'method_self_report': json.loads(metadata.read_text())['method'],
                                    'metadata_sha256': digest(metadata), 'score': leaderboard(scores[revision]).to_dict(),
                                    'total_delay': sum(s.total_delay for s in scores[revision])})
    report['gap_by_sink_count'] = categories
    report['largest_positive_net_gaps'] = sorted((g for g in gaps if g['gap'] > 0),
                                               key=lambda g: g['gap'], reverse=True)[:20]
    destination = ROOT / 'docs/evidence/phase3/reubalink-inspection.json'
    if destination.exists():
        raise RuntimeError('report already exists; use a new filename for a subsequent inspection')
    save(destination, report)
    for r in report['revisions']:
        print(r['revision'], r['score']['aggregate_score'], r['total_delay'])
    print(json.dumps(categories, indent=2))


if __name__ == '__main__':
    main()
