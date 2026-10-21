"""Regression checks against the captured public scoring inputs (no network)."""
import copy
import csv
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("scoring_record", ROOT / "scripts/generate-scoring-record.py")
assert SPEC is not None and SPEC.loader is not None
scoring = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scoring)


class ScoringRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "scoring/snapshot.json").read_text())

    def test_complete_counter_and_agreement(self):
        rows = scoring.make_rows(self.data)
        self.assertEqual([r['contest_number'] for r in rows], list(range(1, 484)))
        scored = [r for r in rows if r['status'] == 'scored']
        self.assertEqual(len(scored), 475)
        self.assertTrue(all(r['comparison'] == 'match' for r in scored))
        self.assertTrue(all(r['score_transaction_hash'] and r['scored_at_utc'] for r in scored))

    def test_void_is_not_a_zero_zero_score(self):
        row = scoring.make_rows(self.data)[450]
        self.assertEqual(row['status'], 'void')
        self.assertEqual(row['actual_status'], 'Postponed')
        self.assertEqual(row['end_kind'], 'legacy_void')
        self.assertEqual(row['end_result'], 'void')
        self.assertEqual(row['ospex_away_score'], '')
        self.assertEqual(row['score_transaction_hash'], '')
        self.assertTrue(row['terminal_transaction_hash'])
        self.assertTrue(row['reason'])

    def test_all_residuals_and_other_unscored_rows_remain_visible(self):
        rows = scoring.make_rows(self.data)
        pending = {r['contest_number']: r for r in rows if r['status'] in ['unscored', 'unverified']}
        self.assertEqual(set(pending), {46, 47, 52, 85, 119, 123, 479})
        for row in pending.values():
            self.assertEqual(row['ospex_away_score'], '')
            self.assertEqual(row['terminal_transaction_hash'], '')
            self.assertEqual(row['comparison'], 'not_scored')
        self.assertEqual(pending[85]['actual_status'], 'Postponed')
        self.assertEqual(pending[119]['status'], 'unverified')
        self.assertEqual(pending[123]['status'], 'unverified')

    def test_missing_and_duplicate_contests_are_rejected(self):
        for change in ['missing', 'duplicate']:
            data = copy.deepcopy(self.data)
            if change == 'missing':
                data['contests']['R5'].pop()
            else:
                data['contests']['R5'].append(data['contests']['R5'][0])
            with self.subTest(change=change), self.assertRaisesRegex(ValueError, 'contest coverage'):
                scoring.make_rows(data)

    def test_identity_feed_mismatch_is_rejected(self):
        data = copy.deepcopy(self.data)
        data['identities'][0]['rundownId'] = 'different-game'
        with self.assertRaisesRegex(ValueError, 'identity mismatch'):
            scoring.make_rows(data)

    def test_planted_score_mismatch_is_published_and_build_continues(self):
        data = copy.deepcopy(self.data)
        actual = data['actualResults'][0]
        contest = next(c for c in data['contests']['R5'] if c['contestId'] == actual['contestId'])
        # Change only the independent final in memory, never chain/bundle evidence.
        actual['awayScore'] = contest['awayScore'] + 1
        outputs = scoring.build(ROOT, data)
        rows = list(csv.DictReader(io.StringIO(outputs['scoring/record.csv'])))
        self.assertEqual(len(rows), 483)
        row = next(r for r in rows if int(r['contest_number']) == actual['contestId'])
        self.assertEqual(row['status'], 'mismatch')
        self.assertEqual(row['comparison'], 'mismatch')
        self.assertEqual(row['end_result'], 'score')
        self.assertEqual(int(row['ospex_away_score']), contest['awayScore'])
        self.assertEqual(int(row['ospex_home_score']), contest['homeScore'])
        self.assertEqual(int(row['actual_away_score']), actual['awayScore'])
        self.assertEqual(int(row['actual_home_score']), actual['homeScore'])
        self.assertTrue(row['score_transaction_hash'] and row['scored_at_utc'])
        self.assertIn('differs from captured independent final', row['reason'])
        self.assertEqual(rows[-1]['contest_number'], '483')
        self.assertEqual(rows[-1]['status'], 'scored')
        summary = json.loads(outputs['scoring/summary.json'])
        self.assertEqual(summary['scored_total'], 475)
        self.assertEqual(summary['scored_matches'], 474)
        self.assertEqual(summary['scored_mismatches'], 1)
        self.assertEqual(summary['status_counts']['mismatch'], 1)
        page = outputs['scoring/README.md']
        self.assertIn('475 scored (474 match, 1 mismatch)', page)
        self.assertIn('| mismatch / score |', page)
        self.assertIn(f"| {actual['awayScore']}–{actual['homeScore']} | {contest['awayScore']}–{contest['homeScore']} | mismatch", page)
        self.assertNotIn('All scored rows agree', page)
        schema = json.loads((ROOT / 'schemas/scoring-row.schema.json').read_text())
        self.assertIn('mismatch', schema['properties']['status']['enum'])

    def test_actual_capture_errors_are_still_rejected(self):
        for field, value in [('awayTeam', 'Different team'), ('final', False),
                             ('awayScore', None), ('sourceTimeDeltaSeconds', 1)]:
            data = copy.deepcopy(self.data)
            data['actualResults'][0][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'actual result mismatch'):
                scoring.make_rows(data)

    def test_nfl_results_are_attributed_to_nflverse(self):
        rows = [r for r in scoring.make_rows(self.data) if r['league'] == 'nfl']
        self.assertEqual({r['contest_number'] for r in rows}, {478, 480, 481, 482, 483})
        expected = {
            478: ('2026_04_IND_WAS', 30, 13), 480: ('2026_05_TB_DAL', 24, 16),
            481: ('2026_05_BAL_ATL', 30, 23), 482: ('2026_06_SEA_DEN', 14, 17),
            483: ('2026_06_DAL_GB', 13, 23),
        }
        for row in rows:
            self.assertEqual(row['actual_source'], 'nflverse')
            self.assertTrue(row['actual_source_url'].startswith('https://raw.githubusercontent.com/nflverse/nfldata/'))
            self.assertEqual((row['actual_event_id'], row['actual_away_score'], row['actual_home_score']), expected[row['contest_number']])

    def test_game_time_displays_chain_start_and_preserves_source_times(self):
        outputs = scoring.build(ROOT, self.data)
        page = outputs['scoring/README.md']
        self.assertIn('| Chain start (UTC) |', page)
        moved = [r for r in scoring.make_rows(self.data) if r['source_time_delta_seconds']]
        self.assertEqual(len(moved), 25)
        self.assertEqual(max(abs(r['source_time_delta_seconds']) for r in moved), 13800)
        row = next(r for r in moved if r['contest_number'] == 436)
        self.assertEqual(scoring.utc(row['game_date_utc']), scoring.utc('2026-09-20T22:00:00Z'))
        self.assertEqual(scoring.utc(row['chain_start_utc']), scoring.utc(row['source_event_time_utc']))
        self.assertEqual(row['source_time_delta_seconds'], -13800)
        self.assertIn('| 436 | Detroit Tigers @ Chicago White Sox | 2026-09-20T18:10:00Z |', page)
        self.assertEqual(sum(scoring.utc(r['chain_start_utc']) == scoring.utc(r['source_event_time_utc'])
                             for r in moved if r['chain_start_utc']), 21)
        self.assertIn('| 119 | Texas Rangers @ Athletics | — |', page)

    def test_public_page_explains_pending_money_voids_and_sources(self):
        page = scoring.build(ROOT, self.data)['scoring/README.md']
        for explanation in ['R5 is the fifth deployment', 'No bets were ever placed on these seven contests',
                            'no money is held on them', 'seven days', 'settles a market',
                            'Unverified', 'Unscored', 'legacy_void', '22 contest numbers',
                            'nflverse', '478 MLB', 'rebuild never re-pulls', 'Python 3.11', 'Linux']:
            with self.subTest(explanation=explanation):
                self.assertIn(explanation, page)

    def test_missing_terminal_event_is_rejected(self):
        data = copy.deepcopy(self.data)
        data['terminalEvents'].pop(0)
        with self.assertRaisesRegex(ValueError, 'terminal event'):
            scoring.make_rows(data)

    def test_receipt_failure_wrong_emitter_and_score_are_rejected(self):
        for field, value in [('receiptStatus', 0), ('emitter', self.data['deployments']['R4']['contestModule']), ('awayScore', 999)]:
            data = copy.deepcopy(self.data)
            data['terminalEvents'][0][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'terminal event'):
                scoring.make_rows(data)

    def test_duplicate_event_is_rejected(self):
        data = copy.deepcopy(self.data)
        data['terminalEvents'].append(copy.deepcopy(data['terminalEvents'][0]))
        with self.assertRaisesRegex(ValueError, 'duplicate terminal event'):
            scoring.make_rows(data)

    def test_bundle_reconciliation_reads_original_files(self):
        stats = scoring.verify_bundles(ROOT, self.data)
        self.assertEqual(stats['runs'], 63)
        self.assertEqual(stats['identity_claims'], 219)
        self.assertEqual(stats['score_claims'], 497)
        self.assertEqual(stats['files'], 1118)
        data = copy.deepcopy(self.data)
        data['bundleClaims']['scores'][0]['score'][0] = 999
        with self.assertRaisesRegex(ValueError, 'bundle score mismatch'):
            scoring.verify_bundles(ROOT, data)

    def test_changed_bundle_bytes_are_rejected(self):
        data = copy.deepcopy(self.data)
        first = next(iter(data['bundleFileSha256']))
        data['bundleFileSha256'][first] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'bundle bytes changed'):
            scoring.verify_bundles(ROOT, data)

    def test_deployment_qualified_repeated_numbers(self):
        rows = scoring.make_run_rows(self.data)
        thirteen = [r for r in rows if r['contest_number'] == 13]
        self.assertEqual({r['deployment'] for r in thirteen}, {'R4', 'R5'})
        self.assertEqual(len({r['contest_key'] for r in thirteen}), 2)
        self.assertTrue(all(r['number_shared_across_deployments'] for r in thirteen))
        legacy_void = [r for r in rows if r['deployment'] == 'R4' and r['contest_number'] == 38]
        self.assertTrue(legacy_void)
        self.assertTrue(all(r['status'] == 'void' and r['terminal_transaction_hash'] for r in legacy_void))

    def test_future_end_kinds_without_any_v3_rows(self):
        self.assertTrue({'score', 'hour_24_void', 'day_7_result', 'day_30_release', 'all_reporters_retired_release'} <= scoring.END_KINDS)
        self.assertEqual({r['protocol_version'] for r in scoring.make_rows(self.data)}, {'v2'})
        schema = json.loads((ROOT / 'schemas/scoring-row.schema.json').read_text())
        self.assertEqual(set(schema['properties']['end_kind']['enum']), scoring.END_KINDS)
        self.assertEqual(set(schema['properties']['end_result']['enum']), {'', 'score', 'void', 'release'})

    def test_snapshot_schema_and_event_type_are_checked(self):
        for section, field, value, diagnostic in [
            (None, '$schema', 'wrong-schema', 'snapshot schema'),
            ('terminalEvents', 'eventTopic', '0x' + '0' * 64, 'terminal event type'),
            ('terminalEvents', 'eventSignature', 'OtherEvent()', 'terminal event type'),
            ('identities', 'chainStartTime', '', 'identity start'),
            ('identities', 'leagueId', 'nfl', 'identity league'),
        ]:
            data = copy.deepcopy(self.data)
            target = data if section is None else data[section][0]
            target[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, diagnostic):
                scoring.make_rows(data)

    def test_future_end_kinds_preserve_distinct_results(self):
        row = scoring.make_rows(self.data)[0]
        for kind, result in [('score', 'score'), ('hour_24_void', 'void'),
                             ('day_7_result', 'score'), ('day_7_result', 'void'),
                             ('day_30_release', 'release'), ('all_reporters_retired_release', 'release')]:
            future = dict(row, protocol_version='v3', end_kind=kind, end_result=result,
                          status={'score': 'scored', 'void': 'void', 'release': 'released'}[result])
            if result != 'score':
                future.update(ospex_away_score='', ospex_home_score='', comparison='not_scored',
                              score_transaction_hash='', scored_at_utc='')
            with self.subTest(kind=kind, result=result):
                scoring.validate_row(future)
                bad = dict(future, end_result='void' if result != 'void' else 'release')
                with self.assertRaisesRegex(ValueError, 'end result'):
                    scoring.validate_row(bad)
        with self.assertRaisesRegex(ValueError, 'end kind'):
            scoring.validate_row(dict(row, end_kind='day_30_release'))

    def test_repository_validator_checks_scoring_and_schema_location(self):
        from unittest.mock import patch
        spec = importlib.util.spec_from_file_location('artifact_validator', ROOT / 'scripts/validate-artifacts.py')
        assert spec is not None and spec.loader is not None
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        errors = []
        validator.validate_schema_pointers({ROOT / 'scoring/snapshot.json': self.data}, errors)
        self.assertEqual(errors, [])
        validator.validate_schema_pointers({ROOT / 'wrong.json': self.data}, errors)
        self.assertTrue(any('scoring/snapshot.json' in error for error in errors))
        errors = []
        validator.validate_generated_scoring(errors)
        self.assertEqual(errors, [])
        with patch.object(validator.subprocess, 'run') as run:
            run.return_value.returncode = 1
            run.return_value.stdout = 'generated scoring record differs: scoring/record.csv'
            validator.validate_generated_scoring(errors)
        self.assertTrue(any('generated scoring record differs' in error for error in errors))

    def test_csv_rebuild_is_byte_identical_and_complete(self):
        outputs = scoring.build(ROOT, self.data)
        for name, text in outputs.items():
            self.assertEqual((ROOT / name).read_bytes(), text.encode('utf-8'), name)
        rows = list(csv.DictReader(io.StringIO(outputs['scoring/record.csv'])))
        self.assertEqual(len(rows), 483)
        self.assertEqual(len({r['contest_key'] for r in rows}), 483)
        self.assertIn('## Every R5 contest', outputs['scoring/README.md'])


if __name__ == '__main__':
    unittest.main()
