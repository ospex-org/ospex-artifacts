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

    def test_actual_score_or_teams_mismatch_is_rejected(self):
        for field in ['awayScore', 'awayTeam']:
            data = copy.deepcopy(self.data)
            data['actualResults'][0][field] = 999 if field == 'awayScore' else 'Different team'
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'actual result mismatch'):
                scoring.make_rows(data)

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
        self.assertTrue({'score', 'hour_24_void', 'day_7_result', 'day_30_release', 'all_scorers_retired_release'} <= scoring.END_KINDS)
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
                             ('day_30_release', 'release'), ('all_scorers_retired_release', 'release')]:
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
            self.assertEqual((ROOT / name).read_text(), text, name)
        rows = list(csv.DictReader(io.StringIO(outputs['scoring/record.csv'])))
        self.assertEqual(len(rows), 483)
        self.assertEqual(len({r['contest_key'] for r in rows}), 483)
        self.assertIn('## Every R5 contest', outputs['scoring/README.md'])


if __name__ == '__main__':
    unittest.main()
