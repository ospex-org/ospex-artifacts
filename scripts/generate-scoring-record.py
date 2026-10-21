#!/usr/bin/env python3
"""Rebuild the public scoring record from frozen public inputs, without network access."""
import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_SCHEMA = 'https://github.com/ospex-org/ospex-artifacts/schemas/scoring-snapshot.schema.json'
END_KINDS = {'', 'score', 'legacy_void', 'hour_24_void', 'day_7_result', 'day_30_release', 'all_scorers_retired_release'}
END_RESULTS = {'': {''}, 'score': {'score'}, 'legacy_void': {'void'}, 'hour_24_void': {'void'}, 'day_7_result': {'score', 'void'}, 'day_30_release': {'release'}, 'all_scorers_retired_release': {'release'}}
EVENT_TYPES = {
    'score': ('ContestScoresSet(uint256,uint32,uint32)', '0xc903c4e9c23026031ddc91220dc647e66e2fa4c0b78cf06a66049b36967579d0'),
    'legacy_void': ('ContestVoided(uint256)', '0x186f23694976df7d5f78e12ed49edc71b37a77bc7bde5cc4393a4b7f1e24c79d'),
}
STATUS = {0: 'unverified', 1: 'unscored', 2: 'scored', 3: 'void'}
FIELDS = ['contest_key', 'chain_id', 'deployment', 'protocol_version', 'deployment_address', 'contest_module_address', 'contest_number', 'league', 'away_team', 'home_team', 'game_date_utc', 'chain_start_utc', 'actual_status', 'actual_away_score', 'actual_home_score', 'actual_source', 'actual_source_url', 'actual_event_id', 'source_event_time_utc', 'identity_match_method', 'source_time_delta_seconds', 'ospex_away_score', 'ospex_home_score', 'comparison', 'status', 'end_kind', 'end_result', 'reason', 'score_transaction_hash', 'scored_at_utc', 'terminal_transaction_hash', 'terminal_at_utc', 'terminal_block_number', 'terminal_explorer_url', 'snapshot_block_number', 'snapshot_at_utc', 'run_bundles']
RUN_FIELDS = ['run', 'reference_kind', 'contest_key', 'deployment', 'protocol_version', 'deployment_address', 'contest_number', 'number_shared_across_deployments', 'status', 'ospex_away_score', 'ospex_home_score', 'end_kind', 'terminal_transaction_hash', 'terminal_at_utc', 'evidence_path']
ADDRESS = re.compile(r'0x[0-9a-fA-F]{40}\Z')
HASH = re.compile(r'0x[0-9a-fA-F]{64}\Z')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def utc(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def iso(seconds):
    return datetime.fromtimestamp(seconds, timezone.utc).isoformat().replace('+00:00', 'Z')


def validate_row(row):
    """Shared row contract; v3 examples are tests only, never captured live rows."""
    require(set(row) == set(FIELDS), 'row fields')
    version, kind, result, status = (row[k] for k in ['protocol_version', 'end_kind', 'end_result', 'status'])
    allowed = {'', 'score', 'legacy_void'} if version == 'v2' else END_KINDS - {'legacy_void'}
    require(version in {'v2', 'v3'} and kind in allowed, 'row end kind')
    require(result in END_RESULTS[kind], 'row end result')
    require(status in ({'unverified', 'unscored'} if result == '' else {dict(score='scored', void='void', release='released')[result]}), 'row end result/status')
    for name in ['deployment_address', 'contest_module_address']:
        require(ADDRESS.fullmatch(row[name]), 'row deployment address')
    require(row['contest_key'] == f"{row['chain_id']}:{row['deployment_address']}:{row['contest_number']}", 'row contest key')
    for name in ['chain_id', 'contest_number', 'snapshot_block_number']:
        require(type(row[name]) is int and row[name] > 0, 'row positive integer: ' + name)
    terminal = bool(result)
    require(all(bool(row[k]) == terminal for k in ['terminal_transaction_hash', 'terminal_at_utc', 'terminal_block_number', 'terminal_explorer_url']), 'row terminal coverage')
    if terminal:
        require(HASH.fullmatch(row['terminal_transaction_hash']), 'row terminal hash')
        require(row['terminal_explorer_url'] == 'https://polygonscan.com/tx/' + row['terminal_transaction_hash'], 'row terminal explorer')
    scored = result == 'score'
    if scored:
        require(all(type(row[k]) is int and row[k] >= 0 for k in ['ospex_away_score', 'ospex_home_score']), 'row score values')
        require(row['score_transaction_hash'] == row['terminal_transaction_hash'] and row['scored_at_utc'] == row['terminal_at_utc'], 'row score receipt')
        require(row['comparison'] in {'match', 'mismatch'}, 'row score comparison')
    else:
        require(all(row[k] == '' for k in ['ospex_away_score', 'ospex_home_score', 'score_transaction_hash', 'scored_at_utc']), 'non-score row has score')
        require(row['comparison'] == 'not_scored', 'row non-score comparison')
    require(bool(row['reason']), 'row reason')


def keyed(values, key, label):
    result = {}
    for value in values:
        k = key(value)
        require(k not in result, 'duplicate ' + label + ': ' + str(k))
        result[k] = value
    return result


def validate(data):
    require(data.get('$schema') == SNAPSHOT_SCHEMA, 'snapshot schema')
    require(data['schemaVersion'] == 1 and data['chainId'] == 137, 'unsupported snapshot')
    require(set(data['deployments']) == {'R4', 'R5'}, 'this capture contains only R4/R5, not v3')
    chains = {}
    for dep, cfg in data['deployments'].items():
        require(cfg['version'] == 'v2' and ADDRESS.fullmatch(cfg['core']) and ADDRESS.fullmatch(cfg['contestModule']), 'deployment identity')
        values = data['contests'][dep]
        ids = [v['contestId'] for v in values]
        require(len(ids) == cfg['contestCount'] and sorted(ids) == list(range(1, cfg['contestCount'] + 1)), dep + ' contest coverage')
        chains[dep] = {v['contestId']: v for v in values}
        require(all(v['contestStatus'] in STATUS for v in values), 'unknown contest status')
    events = keyed(data['terminalEvents'], lambda e: (e['deployment'], e['contestId']), 'terminal event')
    for (dep, number), event in events.items():
        cfg = data['deployments'][dep]
        require(number in chains[dep], 'terminal event without contest')
        require((event['eventSignature'], event['eventTopic']) == EVENT_TYPES.get(event['kind']), 'terminal event type')
        require(event['receiptStatus'] == 1 and event['emitter'].lower() == cfg['contestModule'].lower(), 'terminal event receipt/emitter')
        require(HASH.fullmatch(event['transactionHash']) and HASH.fullmatch(event['blockHash']), 'terminal event hashes')
        require(cfg['deployBlock'] <= event['blockNumber'] <= data['snapshotBlock']['number'], 'terminal event block outside snapshot')
        require(utc(event['timestampUtc']) <= utc(data['snapshotBlock']['timestampUtc']), 'terminal event timestamp outside snapshot')
    for dep, contests in chains.items():
        for number, contest in contests.items():
            event = events.get((dep, number))
            status = contest['contestStatus']
            require(bool(event) == (status in [2, 3]), 'terminal event coverage: ' + dep + ':' + str(number))
            if event:
                require(event['kind'] == ('score' if status == 2 else 'legacy_void'), 'terminal event kind')
                if status == 2:
                    require([event['awayScore'], event['homeScore']] == [contest['awayScore'], contest['homeScore']], 'terminal event score mismatch')
                else:
                    require(event['awayScore'] is None and event['homeScore'] is None, 'terminal event void is not a score')
    api = keyed(data['identities'], lambda a: int(a['contestId']), 'identity')
    results = keyed(data['actualResults'], lambda a: a['contestId'], 'actual result')
    require(set(api) == set(results) == set(chains['R5']), 'identity/result contest coverage')
    for number, contest in chains['R5'].items():
        identity, actual = api[number], results[number]
        require(all(str(identity[k]) == str(contest[k]) for k in ['jsonoddsId', 'rundownId', 'sportspageId']), 'identity mismatch: ' + str(number))
        start = identity['chainStartTime']
        require((start == '' if contest['startTime'] == 0 else bool(start) and int(utc(start).timestamp()) == contest['startTime']), 'identity start mismatch: ' + str(number))
        require(identity['leagueId'] == identity['sport'] and (contest['leagueId'] == 0 if contest['contestStatus'] == 0 else contest['leagueId'] == {'mlb': 3, 'nfl': 2}.get(identity['leagueId'])), 'identity league mismatch: ' + str(number))
        require(identity['awayTeam'] == actual['awayTeam'] and identity['homeTeam'] == actual['homeTeam'], 'actual result mismatch: teams ' + str(number))
        delta = int((utc(actual['sourceEventTimeUtc']) - utc(identity['gameMatchTime'])).total_seconds())
        require(delta == actual['sourceTimeDeltaSeconds'] and abs(delta) < 43200, 'actual result mismatch: event time ' + str(number))
        require(actual['sourceUrl'].startswith(('https://statsapi.mlb.com/', 'https://site.api.espn.com/')), 'unsupported actual-result source')
        if contest['contestStatus'] == 2:
            require(actual['final'] and [actual['awayScore'], actual['homeScore']] == [contest['awayScore'], contest['homeScore']], 'actual result mismatch: score ' + str(number))
    return chains, events, api, results


def contest_key(data, dep, number):
    return str(data['chainId']) + ':' + data['deployments'][dep]['core'] + ':' + str(number)


def make_rows(data):
    chains, events, api, results = validate(data)
    runs = {}
    for binding in data['runBindings']:
        if binding['deployment'] == 'R5':
            for number in binding['contestIds']:
                runs.setdefault(number, []).append('runs/' + binding['run'])
    rows = []
    for number, contest in sorted(chains['R5'].items()):
        identity, actual = api[number], results[number]
        event = events.get(('R5', number), {})
        status = STATUS[contest['contestStatus']]
        scored = status == 'scored'
        reason = 'Protocol score recorded; agrees with captured independent final.' if scored else 'Verified contest; no terminal event at the snapshot.'
        if status == 'unverified':
            reason = 'Contest never verified; no terminal event at the snapshot.'
        elif status == 'void':
            reason = 'v2 cooldown void; on-chain reason not encoded; independent game status: ' + actual['status'] + '.'
        elif number in [46, 47, 52]:
            reason = 'Historical result unavailable to the scoring feeds; remains verified and unscored. Independent final shown separately.'
        elif actual['status'] == 'Postponed':
            reason = 'Independent game status is postponed; verified but neither scored nor voided at the snapshot.'
        cfg = data['deployments']['R5']
        rows.append(dict(zip(FIELDS, [
            contest_key(data, 'R5', number), data['chainId'], 'R5', cfg['version'], cfg['core'], cfg['contestModule'], number,
            identity['leagueId'], identity['awayTeam'], identity['homeTeam'], identity['gameMatchTime'], iso(contest['startTime']) if contest['startTime'] else '',
            actual['status'], actual['awayScore'] if actual['final'] else '', actual['homeScore'] if actual['final'] else '',
            actual['provider'], actual['sourceUrl'], actual['eventId'], actual['sourceEventTimeUtc'], actual['matchMethod'], actual['sourceTimeDeltaSeconds'],
            contest['awayScore'] if scored else '', contest['homeScore'] if scored else '', 'match' if scored else 'not_scored', status,
            event.get('kind', ''), 'score' if scored else 'void' if status == 'void' else '', reason,
            event.get('transactionHash', '') if scored else '', event.get('timestampUtc', '') if scored else '',
            event.get('transactionHash', ''), event.get('timestampUtc', ''), event.get('blockNumber', ''),
            'https://polygonscan.com/tx/' + event['transactionHash'] if event else '', data['snapshotBlock']['number'], data['snapshotBlock']['timestampUtc'], ';'.join(sorted(runs.get(number, [])))
        ])))
        validate_row(rows[-1])
    return rows


def make_run_rows(data):
    chains, events, _, _ = validate(data)
    numbers = {dep: {n for b in data['runBindings'] if b['deployment'] == dep for n in b['contestIds']} for dep in ['R4', 'R5']}
    shared = numbers['R4'] & numbers['R5']
    rows = []
    for binding in sorted(data['runBindings'], key=lambda b: b['run']):
        dep = binding['deployment']
        for number in binding['contestIds']:
            contest = chains[dep][number]
            event = events.get((dep, number), {})
            cfg = data['deployments'][dep]
            scored = contest['contestStatus'] == 2
            rows.append(dict(zip(RUN_FIELDS, [
                binding['run'], 'canonical_evidence' if number in binding['evidenceContestIds'] else 'supporting_file', contest_key(data, dep, number), dep, cfg['version'], cfg['core'], number, number in shared,
                STATUS[contest['contestStatus']], contest['awayScore'] if scored else '', contest['homeScore'] if scored else '', event.get('kind', ''), event.get('transactionHash', ''), event.get('timestampUtc', ''), 'runs/' + binding['run'] + '/evidence.json'
            ])))
    return rows


def pointer(value, path):
    for token in path.strip('/').split('/') if path else []:
        token = token.replace('~1', '/').replace('~0', '~')
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def verify_bundles(root, data):
    chains, _, _, _ = validate(data)
    root = Path(root)
    files = data['bundleFileSha256']
    current = {f.relative_to(root).as_posix() for f in (root / 'runs').rglob('*') if f.is_file()}
    require(current == set(files), 'bundle file inventory changed: refresh the capture explicitly')
    for name, digest in files.items():
        require(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest, 'bundle bytes changed: ' + name)
    bindings = keyed(data['runBindings'], lambda b: b['run'], 'run binding')
    require(set(bindings) == {f.parent.name for f in (root / 'runs').glob('*/evidence.json')}, 'run binding coverage')
    for binding in bindings.values():
        dep = binding['deployment']
        if dep is None:
            require(not binding['contestIds'], 'unbound contest')
            continue
        cfg = data['deployments'][dep]
        require(binding['deploymentProof'], 'missing deployment proof')
        for proof in binding['deploymentProof']:
            if 'transactionHash' in proof:
                require(proof['receiptStatus'] == 1 and bool({cfg['core'].lower(), cfg['contestModule'].lower()} & {a.lower() for a in proof['emitters']}), 'deployment proof mismatch')
                require(proof['transactionHash'] in (root / proof['file']).read_text(), 'deployment proof absent from bundle')
            else:
                contest = chains[dep][proof['contestId']]
                require(all(contest[k] == v for k, v in proof['fields'].items()), 'deployment identity proof mismatch')
    documents = {}
    def original(claim):
        path = claim['file']
        if path not in documents:
            documents[path] = json.loads((root / path).read_text())
        return pointer(documents[path], claim['path'])
    for claim in data['bundleClaims']['identities']:
        source = original(claim)
        field = claim['field']
        alias = {'rundownId': 'rundown_id', 'sportspageId': 'sportspage_id', 'jsonoddsId': 'jsonodds_id'}[field]
        observed = str(source.get(field, source.get(alias)))
        require(observed == claim['bundle'] == chains[claim['deployment']][claim['contestId']][field], 'bundle identity mismatch: ' + claim['file'])
    for claim in data['bundleClaims']['scores']:
        source = original(claim)
        score = [int(source[field]) for field in claim['fields']]
        contest = chains[claim['deployment']][claim['contestId']]
        require(contest['contestStatus'] == 2 and score == claim['score'] == [contest['awayScore'], contest['homeScore']], 'bundle score mismatch: ' + claim['file'])
    return {'runs': len(bindings), 'files': len(files), 'identity_claims': len(data['bundleClaims']['identities']), 'score_claims': len(data['bundleClaims']['scores'])}


def csv_text(rows, fields):
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def render(rows, summary):
    cfg = rows[0]
    text = [
        '# Public scoring record', '',
        '[Download the complete CSV](record.csv) · [Deployment-qualified legacy/run index](run-contests.csv) · [Rebuild and source documentation](../docs/scoring-record.md)', '',
        'Every R5 contest from deployment through Polygon block **' + str(cfg['snapshot_block_number']) + '** (' + cfg['snapshot_at_utc'] + '). This is a frozen snapshot, not a live service.', '',
        '**' + str(summary['rows']) + ' contests: ' + str(summary['status_counts']['scored']) + ' scored, ' + str(summary['status_counts']['void']) + ' void, ' + str(summary['status_counts']['unscored']) + ' verified/unscored, ' + str(summary['status_counts']['unverified']) + ' unverified.** All scored rows agree with their captured independent final; pending and void rows are not counted as accurate scores.', '',
        'All scores below are **away–home**. The timestamp is the successful terminal transaction’s block time, never API ingestion time. A dash means absent, not zero. The CSV carries full addresses, source IDs, original game times, matching notes and transaction hashes.', '',
        '**R5 deployment:** [`' + cfg['deployment_address'] + '`](https://polygonscan.com/address/' + cfg['deployment_address'] + '). Join on `(chain_id, deployment_address, contest_number)`, never the number alone.', '',
        '**The five sweep residuals:** #46, #47 and #52 are historical verified games whose scoring feeds no longer supplied a final; #119 and #123 are unverified registry entries for the same real game. All five belong here. The complete counter also retains #85 (postponed, still unscored) and #479 (unverified); none is silently omitted.', '',
        '**Voids:** R5 #451 is a cooldown void for a game reported postponed. The event does not encode a reason; the independent status is shown rather than invented as an on-chain reason. The older R4 #38 void is in the deployment-qualified run index, not misattributed to R5 #38.', '',
        '**Repeated numbers:** all original run bundles remain byte-for-byte unchanged. The run index labels every reference with R4 or R5 and its core address, including ' + str(len(summary['shared_number_ids'])) + ' numbers shared across full bundle contents (' + str(len(summary['canonical_shared_number_ids'])) + ' in canonical `evidence.json` files). It covers the previously reported doubled numbers without dropping references to force a historical count.', '',
        '## Every R5 contest', '',
        '| R5 contest | Game (away @ home) | Game date UTC | Actual | Ospex | Status / end | Written UTC | Transaction | Actual source |',
        '| --- | --- | --- | --- | --- | --- | --- | --- | --- |'
    ]
    for row in rows:
        actual = str(row['actual_away_score']) + '–' + str(row['actual_home_score']) if row['actual_away_score'] != '' else row['actual_status']
        score = str(row['ospex_away_score']) + '–' + str(row['ospex_home_score']) if row['ospex_away_score'] != '' else '—'
        tx = '[receipt](' + row['terminal_explorer_url'] + ')' if row['terminal_explorer_url'] else '—'
        text.append('| ' + ' | '.join([str(row['contest_number']), row['away_team'] + ' @ ' + row['home_team'], row['game_date_utc'], actual, score, row['status'] + (' / ' + row['end_kind'] if row['end_kind'] else ''), row['terminal_at_utc'] or '—', tx, '[' + row['actual_source'] + '](' + row['actual_source_url'] + ')']) + ' |')
    return '\n'.join(text) + '\n'


def build(root, data=None):
    root = Path(root)
    if data is None:
        data = json.loads((root / 'scoring/snapshot.json').read_text())
    bundle_stats = verify_bundles(root, data)
    rows, run_rows = make_rows(data), make_run_rows(data)
    sets = {dep: {r['contest_number'] for r in run_rows if r['deployment'] == dep} for dep in ['R4', 'R5']}
    canonical = {dep: {r['contest_number'] for r in run_rows if r['deployment'] == dep and r['reference_kind'] == 'canonical_evidence'} for dep in ['R4', 'R5']}
    summary = {'snapshot_block': data['snapshotBlock'], 'rows': len(rows), 'status_counts': dict(Counter(r['status'] for r in rows)), 'scored_matches': sum(r['comparison'] == 'match' for r in rows), 'run_index_rows': len(run_rows), 'bundle_reconciliation': bundle_stats, 'shared_number_ids': sorted(sets['R4'] & sets['R5']), 'canonical_shared_number_ids': sorted(canonical['R4'] & canonical['R5']), 'v3_rows': 0}
    return {'scoring/record.csv': csv_text(rows, FIELDS), 'scoring/run-contests.csv': csv_text(run_rows, RUN_FIELDS), 'scoring/summary.json': json.dumps(summary, indent=2, sort_keys=True) + '\n', 'scoring/README.md': render(rows, summary)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if any generated file differs; never write.')
    args = parser.parse_args()
    outputs = build(ROOT)
    for name, text in outputs.items():
        path = ROOT / name
        if args.check:
            require(path.exists() and path.read_text() == text, 'generated scoring record differs: ' + name)
        else:
            path.write_text(text)
    print(('Checked' if args.check else 'Generated') + ' scoring record: ' + ', '.join(outputs))


if __name__ == '__main__':
    main()
