#!/usr/bin/env python3
"""Unit tests for the artifact validator."""

from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate-artifacts.py"

spec = importlib.util.spec_from_file_location("validate_artifacts", VALIDATOR_PATH)
assert spec is not None and spec.loader is not None
validate_artifacts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_artifacts)

# Read-only on-disk anchor so evidence-path existence checks resolve against
# real published files. Run artifacts are immutable evidence, so this is stable.
SAMPLE_RUN_DIR = ROOT / "runs" / "2026-06-11-mlb-hou-laa-contest-35-mm-live-canary"
TX_A = "0x" + "ab" * 32
TX_B = "0x" + "cd" * 32
TX_C = "0x" + "ef" * 32
TX_D = "0x" + "12" * 32
TX_E = "0x" + "34" * 32
TX_F = "0x" + "56" * 32


def make_postgame_deferred_scorecard() -> dict:
    return {
        "$schema": validate_artifacts.MVE_SCORECARD_SCHEMA_ID,
        "schemaVersion": 1,
        "artifactId": SAMPLE_RUN_DIR.name,
        "generatedAt": "2026-06-11T06:00:00Z",
        "runClass": "mm-live-canary",
        "verdict": {
            "label": "GREEN_LIVE_WINDOW_POSTGAME_DEFERRED",
            "reason": "Live window complete; game not final at capture.",
        },
        "capabilities": [
            {"id": "target-preflight", "capability": "Target selection", "proof": "proven_live", "evidence": "raw/target-decision.sanitized.json", "notes": "ok"},
            {"id": "repo-runtime-gates", "capability": "Runtime gates", "proof": "proven_live", "evidence": "raw/release-runtime-matrix.sanitized.json", "notes": "ok"},
            {"id": "wallet-auth-balances", "capability": "Wallet auth", "proof": "proven_live", "evidence": "raw/wallet-auth-balance-allowances.sanitized.json", "notes": "ok"},
            {"id": "bounded-approvals", "capability": "Bounded approvals", "proof": "proven_live", "evidence": "raw/wallet-auth-balance-allowances.sanitized.json", "notes": "ok"},
            {"id": "dry-run-quote-loop", "capability": "Dry-run loop", "proof": "proven_synthetic_only", "evidence": "raw/mm-dryrun-summary.sanitized.json", "notes": "ok"},
            {"id": "live-commitments-posted", "capability": "Live commitments", "proof": "proven_live", "evidence": "raw/live-public-commitments-posted.sanitized.json", "notes": "ok"},
            {"id": "live-fill", "capability": "Live fill", "proof": "proven_live", "evidence": "raw/live-fill.sanitized.json", "notes": "ok"},
            {"id": "own-state-sse-canonical-fill", "capability": "Own-state SSE fill", "proof": "proven_live", "evidence": "raw/own-state-sse-summary.sanitized.json", "notes": "ok"},
            {"id": "exposure-drain-zero", "capability": "Zero exposure", "proof": "proven_live", "evidence": "raw/zero-exposure.sanitized.json", "notes": "ok"},
            {"id": "restart-cold-start-safety", "capability": "Cold-start safety", "proof": "proven_synthetic_only", "evidence": "raw/restart-cold-start-probe.sanitized.json", "notes": "ok"},
            {"id": "postgame-score", "capability": "Score", "proof": "deferred", "evidence": None, "notes": "game not final"},
            {"id": "postgame-settle", "capability": "Settle", "proof": "deferred", "evidence": None, "notes": "game not final"},
            {"id": "postgame-claim", "capability": "Claim", "proof": "deferred", "evidence": None, "notes": "game not final"},
            {"id": "cost-within-cap", "capability": "Cost cap", "proof": "proven_live", "evidence": "raw/tx-receipts.summary.json", "notes": "ok"},
        ],
        "zeroExposure": {
            "checkedAtUtc": "2026-06-11T06:00:00Z",
            "publicMakerVisibleCommitments": 0,
            "publicContestSpecVisibleCommitments": 0,
            "contestOrderbookCount": 0,
            "orphanProcessCount": 0,
            "evidence": "raw/zero-exposure.sanitized.json",
        },
        "transactions": [
            {"category": "approve", "txHash": TX_A, "status": "success", "operatorControlled": True, "purpose": "bounded USDC approval"},
            {"category": "match-commitment", "txHash": TX_B, "status": "success", "operatorControlled": True, "purpose": "controlled partial fill"},
        ],
    }


def make_postgame_deferred_evidence() -> dict:
    return {
        "status": "partial",
        "artifactFiles": {
            "summary": "summary.md",
            "scenarioMatrixJson": "scenario-matrix.json",
            "mveScorecardJson": "mve-scorecard.json",
        },
        "verdict": {
            "label": "GREEN_LIVE_WINDOW_POSTGAME_DEFERRED",
            "reason": "Live window complete; game not final at capture.",
        },
        "target": {
            "market": "moneyline",
            "teamIdentity": {
                "home": {"team": "Los Angeles Angels", "positionType": "lower", "marketOddsAmerican": "-114", "identity": "favorite"},
                "away": {"team": "Houston Astros", "positionType": "upper", "marketOddsAmerican": "+114", "identity": "underdog"},
            },
        },
    }


def make_full_green_scorecard() -> dict:
    scorecard = make_postgame_deferred_scorecard()
    scorecard["verdict"] = {"label": "FULL_GREEN", "reason": "Live window and postgame lifecycle complete."}
    for row in scorecard["capabilities"]:
        if row["id"] in {"postgame-score", "postgame-settle", "postgame-claim"}:
            row["proof"] = "proven_live"
            row["evidence"] = "raw/cli-postgame.sanitized.json"
            row["notes"] = "postgame complete"
    scorecard["transactions"].extend(
        [
            {"category": "score-request", "txHash": TX_C, "status": "success", "operatorControlled": True, "purpose": "score contest"},
            {"category": "score-callback", "txHash": TX_D, "status": "success", "operatorControlled": False, "purpose": "oracle callback"},
            {"category": "settle", "txHash": TX_E, "status": "success", "operatorControlled": True, "purpose": "settle speculation"},
            {"category": "claim", "txHash": TX_F, "status": "success", "operatorControlled": True, "purpose": "claim winning position"},
        ]
    )
    return scorecard


def make_full_green_evidence() -> dict:
    evidence = make_postgame_deferred_evidence()
    evidence["status"] = "complete_verified_with_caveats"
    evidence["verdict"] = {"label": "FULL_GREEN", "reason": "Live window and postgame lifecycle complete."}
    return evidence


def run_scorecard_validation(scorecard: dict, evidence: dict) -> list[str]:
    errors: list[str] = []
    docs = {SAMPLE_RUN_DIR / "evidence.json": evidence}
    validate_artifacts.validate_mve_scorecard(SAMPLE_RUN_DIR / "mve-scorecard.json", scorecard, docs, errors)
    return errors


class ProjectionConvergenceValidationTests(unittest.TestCase):
    def test_valid_projection_convergence_contract_passes(self) -> None:
        errors: list[str] = []
        validate_artifacts.validate_projection_convergence(
            Path("runs/example/evidence.json"),
            {
                "projectionConvergence": {
                    "expectation": "tx confirmed; waiting for API projection before final assertions",
                    "gates": [
                        {
                            "name": "postClaim",
                            "afterWrite": "claim",
                            "txConfirmed": True,
                            "waitTarget": "claimableCount=0 and position.claimed=true",
                            "expectedFinalState": ["claimableCount=0", "position.claimed=true"],
                            "observedFinalState": ["claim-all dry-run entries=0", "positions status claimableCount=0"],
                            "converged": True,
                            "staleReadObserved": True,
                        }
                    ],
                }
            },
            errors,
        )

        self.assertEqual(errors, [])

    def test_projection_convergence_gate_requires_observed_final_state(self) -> None:
        errors: list[str] = []
        validate_artifacts.validate_projection_convergence(
            Path("runs/example/evidence.json"),
            {
                "projectionConvergence": {
                    "expectation": "tx confirmed; waiting for API projection before final assertions",
                    "gates": [
                        {
                            "name": "postClaim",
                            "afterWrite": "claim",
                            "txConfirmed": True,
                            "waitTarget": "claimableCount=0 and position.claimed=true",
                            "expectedFinalState": ["claimableCount=0", "position.claimed=true"],
                            "converged": True,
                        }
                    ],
                }
            },
            errors,
        )

        self.assertIn(
            "runs/example/evidence.json: projectionConvergence.gates[0] missing required key 'observedFinalState'",
            errors,
        )


class ScenarioMatrixValidationTests(unittest.TestCase):
    def test_legacy_array_matrix_is_skipped(self) -> None:
        errors: list[str] = []
        validate_artifacts.validate_scenario_matrix(
            ROOT / "runs" / "example-run" / "scenario-matrix.json",
            [{"scenario": "legacy", "classification": "proven"}],
            errors,
        )
        self.assertEqual(errors, [])

    def test_legacy_v1_matrix_is_skipped(self) -> None:
        errors: list[str] = []
        validate_artifacts.validate_scenario_matrix(
            ROOT / "runs" / "example-run" / "scenario-matrix.json",
            {"schemaVersion": 1, "scenarios": [{"scenario": "legacy", "status": "pass_with_expected_timeout"}]},
            errors,
        )
        self.assertEqual(errors, [])

    def test_valid_v2_matrix_passes(self) -> None:
        errors: list[str] = []
        validate_artifacts.validate_scenario_matrix(
            SAMPLE_RUN_DIR / "scenario-matrix.json",
            {
                "$schema": validate_artifacts.SCENARIO_MATRIX_SCHEMA_ID,
                "schemaVersion": 2,
                "artifactId": SAMPLE_RUN_DIR.name,
                "generatedAt": "2026-06-11T06:00:00Z",
                "runClass": "mm-live-canary",
                "scenarios": [
                    {"id": "live-fill", "scenario": "live fill", "status": "pass", "evidence": "raw/live-fill.sanitized.json", "notes": "ok"},
                    {"id": "postgame-lifecycle", "scenario": "postgame lifecycle", "status": "deferred", "evidence": None, "notes": "game not final"},
                ],
            },
            errors,
        )
        self.assertEqual(errors, [])

    def test_v2_matrix_rejects_unknown_status(self) -> None:
        errors: list[str] = []
        validate_artifacts.validate_scenario_matrix(
            SAMPLE_RUN_DIR / "scenario-matrix.json",
            {
                "$schema": validate_artifacts.SCENARIO_MATRIX_SCHEMA_ID,
                "schemaVersion": 2,
                "artifactId": SAMPLE_RUN_DIR.name,
                "generatedAt": "2026-06-11T06:00:00Z",
                "runClass": "mm-live-canary",
                "scenarios": [
                    {"id": "live-fill", "scenario": "live fill", "status": "pass_with_expected_timeout", "evidence": "raw/live-fill.sanitized.json", "notes": "ok"},
                ],
            },
            errors,
        )
        self.assertTrue(any("status 'pass_with_expected_timeout'" in error for error in errors), errors)

    def test_v2_pass_row_requires_evidence(self) -> None:
        errors: list[str] = []
        validate_artifacts.validate_scenario_matrix(
            SAMPLE_RUN_DIR / "scenario-matrix.json",
            {
                "$schema": validate_artifacts.SCENARIO_MATRIX_SCHEMA_ID,
                "schemaVersion": 2,
                "artifactId": SAMPLE_RUN_DIR.name,
                "generatedAt": "2026-06-11T06:00:00Z",
                "runClass": "mm-live-canary",
                "scenarios": [
                    {"id": "live-fill", "scenario": "live fill", "status": "pass", "evidence": None, "notes": "ok"},
                ],
            },
            errors,
        )
        self.assertTrue(any("evidence is required when status is 'pass'" in error for error in errors), errors)

    def test_v2_matrix_requires_artifact_id_to_match_directory(self) -> None:
        errors: list[str] = []
        validate_artifacts.validate_scenario_matrix(
            SAMPLE_RUN_DIR / "scenario-matrix.json",
            {
                "$schema": validate_artifacts.SCENARIO_MATRIX_SCHEMA_ID,
                "schemaVersion": 2,
                "artifactId": "some-other-run",
                "generatedAt": "2026-06-11T06:00:00Z",
                "runClass": "mm-live-canary",
                "scenarios": [
                    {"id": "live-fill", "scenario": "live fill", "status": "deferred", "evidence": None, "notes": "ok"},
                ],
            },
            errors,
        )
        self.assertTrue(any("artifactId must equal the artifact directory name" in error for error in errors), errors)


class MveScorecardValidationTests(unittest.TestCase):
    def test_valid_postgame_deferred_scorecard_passes(self) -> None:
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), make_postgame_deferred_evidence())
        self.assertEqual(errors, [])

    def test_valid_full_green_scorecard_passes(self) -> None:
        errors = run_scorecard_validation(make_full_green_scorecard(), make_full_green_evidence())
        self.assertEqual(errors, [])

    def test_red_safety_halt_is_not_publishable(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        scorecard["verdict"]["label"] = "RED_SAFETY_HALT"
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertTrue(any("not publishable" in error for error in errors), errors)

    def test_unknown_verdict_label_is_rejected(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        scorecard["verdict"]["label"] = "GREEN_WITH_COVERAGE_AMBER"
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertTrue(any("verdict.label" in error and "must be one of" in error for error in errors), errors)

    def test_full_green_rejects_deferred_postgame(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        scorecard["verdict"] = {"label": "FULL_GREEN", "reason": "claims completion"}
        evidence = make_full_green_evidence()
        errors = run_scorecard_validation(scorecard, evidence)
        self.assertTrue(any("requires proven core capabilities" in error for error in errors), errors)
        self.assertTrue(any("requires at least one settle transaction" in error for error in errors), errors)
        self.assertTrue(any("requires score-request or score-callback" in error for error in errors), errors)

    def test_postgame_deferred_rejects_postgame_tx_categories(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        scorecard["transactions"].append(
            {"category": "settle", "txHash": TX_E, "status": "success", "operatorControlled": True, "purpose": "early settle"}
        )
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertTrue(any("cannot include postgame transaction categories" in error for error in errors), errors)

    def test_score_callback_must_not_be_operator_controlled(self) -> None:
        scorecard = make_full_green_scorecard()
        for tx in scorecard["transactions"]:
            if tx["category"] == "score-callback":
                tx["operatorControlled"] = True
        errors = run_scorecard_validation(scorecard, make_full_green_evidence())
        self.assertTrue(any("operatorControlled must be false" in error for error in errors), errors)

    def test_exact_duplicate_transaction_is_rejected(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        scorecard["transactions"].append(copy.deepcopy(scorecard["transactions"][0]))
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertTrue(any("duplicate transaction entry" in error for error in errors), errors)

    def test_zero_exposure_counts_must_be_zero(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        scorecard["zeroExposure"]["publicMakerVisibleCommitments"] = 1
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertTrue(any("publicMakerVisibleCommitments must be the integer 0" in error for error in errors), errors)

    def test_exposure_drain_zero_must_be_proven_live(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        for row in scorecard["capabilities"]:
            if row["id"] == "exposure-drain-zero":
                row["proof"] = "proven_synthetic_only"
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertTrue(any("exposure-drain-zero must be proven_live" in error for error in errors), errors)

    def test_missing_capability_row_is_reported(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        scorecard["capabilities"] = [row for row in scorecard["capabilities"] if row["id"] != "cost-within-cap"]
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertTrue(any("missing capability rows: cost-within-cap" in error for error in errors), errors)

    def test_duplicate_capability_id_is_reported(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        scorecard["capabilities"].append(copy.deepcopy(scorecard["capabilities"][0]))
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertTrue(any("duplicate capability id" in error for error in errors), errors)

    def test_verdict_status_mapping_is_enforced(self) -> None:
        evidence = make_postgame_deferred_evidence()
        evidence["status"] = "complete_verified"
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("does not match scorecard verdict" in error for error in errors), errors)

    def test_evidence_verdict_label_must_match_scorecard(self) -> None:
        evidence = make_postgame_deferred_evidence()
        evidence["verdict"]["label"] = "FULL GREEN / COMPLETE"
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("verdict.label must equal the scorecard verdict label" in error for error in errors), errors)

    def test_moneyline_requires_team_identity(self) -> None:
        evidence = make_postgame_deferred_evidence()
        del evidence["target"]["teamIdentity"]
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("moneyline target requires a teamIdentity object" in error for error in errors), errors)

    def test_team_identity_enforces_position_type_mapping(self) -> None:
        evidence = make_postgame_deferred_evidence()
        evidence["target"]["teamIdentity"]["home"]["positionType"] = "upper"
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("teamIdentity.home.positionType must be 'lower'" in error for error in errors), errors)

    def test_team_identity_rejects_two_favorites(self) -> None:
        evidence = make_postgame_deferred_evidence()
        evidence["target"]["teamIdentity"]["away"]["identity"] = "favorite"
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("identities must pair favorite/underdog or even/even" in error for error in errors), errors)

    def test_artifact_files_must_reference_companion_files(self) -> None:
        evidence = make_postgame_deferred_evidence()
        del evidence["artifactFiles"]["mveScorecardJson"]
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("artifactFiles must reference mve-scorecard.json" in error for error in errors), errors)


class AdoptionPairingTests(unittest.TestCase):
    def test_scorecard_requires_v2_matrix(self) -> None:
        errors: list[str] = []
        docs = {ROOT / "runs" / "example-run" / "mve-scorecard.json": {}}
        validate_artifacts.validate_adoption_pairing(docs, errors)
        self.assertTrue(any("requires a schemaVersion >= 2 scenario-matrix.json" in error for error in errors), errors)

    def test_v2_matrix_requires_scorecard(self) -> None:
        errors: list[str] = []
        docs = {ROOT / "runs" / "example-run" / "scenario-matrix.json": {"schemaVersion": 2, "scenarios": []}}
        validate_artifacts.validate_adoption_pairing(docs, errors)
        self.assertTrue(any("requires an mve-scorecard.json" in error for error in errors), errors)

    def test_paired_adoption_passes(self) -> None:
        errors: list[str] = []
        docs = {
            ROOT / "runs" / "example-run" / "scenario-matrix.json": {"schemaVersion": 2, "scenarios": []},
            ROOT / "runs" / "example-run" / "mve-scorecard.json": {},
        }
        validate_artifacts.validate_adoption_pairing(docs, errors)
        self.assertEqual(errors, [])

    def test_legacy_matrix_without_scorecard_passes(self) -> None:
        errors: list[str] = []
        docs = {ROOT / "runs" / "example-run" / "scenario-matrix.json": {"schemaVersion": 1, "scenarios": []}}
        validate_artifacts.validate_adoption_pairing(docs, errors)
        self.assertEqual(errors, [])


class SignatureSafetyPatternTests(unittest.TestCase):
    def pattern(self):
        for label, compiled in validate_artifacts.SAFETY_PATTERNS:
            if label == "signature/signedPayload-keyed hex value":
                return compiled
        raise AssertionError("signature/signedPayload safety pattern is missing")

    def test_matches_signature_keyed_hex_values(self) -> None:
        pattern = self.pattern()
        self.assertIsNotNone(pattern.search('"signature": "0xdeadbeef12345678"'))
        self.assertIsNotNone(pattern.search('"rawSignature": "0xABCDEF0123456789"'))
        self.assertIsNotNone(pattern.search('"signedPayload": "0x00112233445566778899"'))

    def test_ignores_redaction_and_presence_booleans(self) -> None:
        pattern = self.pattern()
        self.assertIsNone(pattern.search('"signatureRedacted": true'))
        self.assertIsNone(pattern.search('"rawSignatureRedacted": true'))
        self.assertIsNone(pattern.search('"signedPayloadPresent": false'))
        self.assertIsNone(pattern.search('"signature": "0xREDACTED"'))


if __name__ == "__main__":
    unittest.main()
