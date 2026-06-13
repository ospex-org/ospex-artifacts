#!/usr/bin/env python3
"""Unit tests for the artifact validator."""

from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate-artifacts.py"
TEMPLATE_DIR = ROOT / "templates" / "mm-live-canary"

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
        "artifactType": "run",
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
            "sport": "mlb",
            "contestId": "35",
            "speculationId": "25",
            "homeTeam": "Los Angeles Angels",
            "awayTeam": "Houston Astros",
            "teamIdentity": {
                "home": {"team": "Los Angeles Angels", "positionType": "lower", "marketOddsAmerican": "-114", "identity": "favorite"},
                "away": {"team": "Houston Astros", "positionType": "upper", "marketOddsAmerican": "+114", "identity": "underdog"},
            },
        },
    }


def make_amber_no_fill_scorecard() -> dict:
    scorecard = make_postgame_deferred_scorecard()
    scorecard["verdict"] = {"label": "AMBER_QUOTED_NO_FILL", "reason": "Quotes posted; no fill arrived in the window."}
    for row in scorecard["capabilities"]:
        if row["id"] in {"live-fill", "own-state-sse-canonical-fill"}:
            row["proof"] = "deferred"
            row["evidence"] = None
            row["notes"] = "no fill in window"
    scorecard["transactions"] = [tx for tx in scorecard["transactions"] if tx["category"] != "match-commitment"]
    return scorecard


def make_amber_no_fill_evidence() -> dict:
    evidence = make_postgame_deferred_evidence()
    evidence["verdict"] = {"label": "AMBER_QUOTED_NO_FILL", "reason": "Quotes posted; no fill arrived in the window."}
    return evidence


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
        self.assertTrue(any("requires at least one successful settle transaction" in error for error in errors), errors)
        self.assertTrue(any("requires successful score-request or score-callback" in error for error in errors), errors)

    def test_postgame_deferred_rejects_postgame_tx_categories(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        scorecard["transactions"].append(
            {"category": "settle", "txHash": TX_E, "status": "success", "operatorControlled": True, "purpose": "early settle"}
        )
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertTrue(any("cannot include successful postgame transaction categories" in error for error in errors), errors)

    def test_postgame_deferred_allows_disclosed_reverted_postgame_attempt(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        scorecard["transactions"].append(
            {
                "category": "score-request",
                "txHash": TX_E,
                "status": "reverted",
                "operatorControlled": True,
                "purpose": "early scoring attempt reverted because the game was not final",
            }
        )
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertEqual(errors, [])

    def test_full_green_rejects_reverted_only_settle_and_score(self) -> None:
        scorecard = make_full_green_scorecard()
        for tx in scorecard["transactions"]:
            if tx["category"] in {"settle", "score-request", "score-callback"}:
                tx["status"] = "reverted"
        errors = run_scorecard_validation(scorecard, make_full_green_evidence())
        self.assertTrue(any("requires at least one successful settle transaction" in error for error in errors), errors)
        self.assertTrue(any("requires successful score-request or score-callback" in error for error in errors), errors)

    def test_full_green_allows_reverted_attempt_alongside_successful_retry(self) -> None:
        scorecard = make_full_green_scorecard()
        scorecard["transactions"].append(
            {
                "category": "settle",
                "txHash": TX_A,
                "status": "reverted",
                "operatorControlled": True,
                "purpose": "first settle attempt reverted before the successful retry",
            }
        )
        errors = run_scorecard_validation(scorecard, make_full_green_evidence())
        self.assertEqual(errors, [])

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
        docs = {ROOT / "runs" / "example-run" / "mve-scorecard.json": {"runClass": "mm-live-canary"}}
        validate_artifacts.validate_adoption_pairing(docs, errors)
        self.assertTrue(any("requires a schemaVersion >= 2 scenario-matrix.json" in error for error in errors), errors)

    def test_v2_canary_matrix_requires_scorecard(self) -> None:
        errors: list[str] = []
        docs = {
            ROOT / "runs" / "example-run" / "scenario-matrix.json": {
                "schemaVersion": 2,
                "runClass": "mm-live-canary",
                "scenarios": [],
            }
        }
        validate_artifacts.validate_adoption_pairing(docs, errors)
        self.assertTrue(any("requires an mve-scorecard.json" in error for error in errors), errors)

    def test_non_canary_v2_matrix_does_not_require_scorecard(self) -> None:
        errors: list[str] = []
        docs = {
            ROOT / "runs" / "example-run" / "scenario-matrix.json": {
                "schemaVersion": 2,
                "runClass": "future-run-class",
                "scenarios": [],
            }
        }
        validate_artifacts.validate_adoption_pairing(docs, errors)
        self.assertEqual(errors, [])

    def test_paired_adoption_passes(self) -> None:
        errors: list[str] = []
        docs = {
            ROOT / "runs" / "example-run" / "scenario-matrix.json": {
                "schemaVersion": 2,
                "runClass": "mm-live-canary",
                "scenarios": [],
            },
            ROOT / "runs" / "example-run" / "mve-scorecard.json": {"runClass": "mm-live-canary"},
        }
        validate_artifacts.validate_adoption_pairing(docs, errors)
        self.assertEqual(errors, [])

    def test_paired_run_class_mismatch_is_rejected(self) -> None:
        errors: list[str] = []
        docs = {
            ROOT / "runs" / "example-run" / "scenario-matrix.json": {
                "schemaVersion": 2,
                "runClass": "future-run-class",
                "scenarios": [],
            },
            ROOT / "runs" / "example-run" / "mve-scorecard.json": {"runClass": "mm-live-canary"},
        }
        validate_artifacts.validate_adoption_pairing(docs, errors)
        self.assertTrue(any("runClass 'future-run-class' must match" in error for error in errors), errors)

    def test_legacy_matrix_without_scorecard_passes(self) -> None:
        errors: list[str] = []
        docs = {ROOT / "runs" / "example-run" / "scenario-matrix.json": {"schemaVersion": 1, "scenarios": []}}
        validate_artifacts.validate_adoption_pairing(docs, errors)
        self.assertEqual(errors, [])


class AdoptionNearMissTests(unittest.TestCase):
    def matrix_errors(self, doc: object) -> list[str]:
        errors: list[str] = []
        validate_artifacts.validate_scenario_matrix(ROOT / "runs" / "example-run" / "scenario-matrix.json", doc, errors)
        return errors

    def test_schema_pointer_with_string_schema_version_is_rejected(self) -> None:
        errors = self.matrix_errors({"$schema": validate_artifacts.SCENARIO_MATRIX_SCHEMA_ID, "schemaVersion": "2", "scenarios": []})
        self.assertTrue(any("schemaVersion must be a plain integer >= 2" in error for error in errors), errors)

    def test_float_schema_version_is_rejected(self) -> None:
        errors = self.matrix_errors({"schemaVersion": 2.0, "scenarios": []})
        self.assertTrue(any("schemaVersion must be a plain integer >= 2" in error for error in errors), errors)

    def test_schema_pointer_without_schema_version_is_rejected(self) -> None:
        errors = self.matrix_errors({"$schema": validate_artifacts.SCENARIO_MATRIX_SCHEMA_ID, "scenarios": []})
        self.assertTrue(any("schemaVersion must be a plain integer >= 2" in error for error in errors), errors)

    def test_string_schema_version_without_schema_pointer_is_rejected(self) -> None:
        errors = self.matrix_errors({"schemaVersion": "2", "scenarios": []})
        self.assertTrue(any("schemaVersion must be a plain integer when present" in error for error in errors), errors)

    def test_legacy_v1_and_array_shapes_stay_grandfathered(self) -> None:
        self.assertEqual(self.matrix_errors({"schemaVersion": 1, "scenarios": []}), [])
        self.assertEqual(self.matrix_errors([{"scenario": "legacy", "classification": "proven"}]), [])

    def test_unknown_run_class_is_rejected_on_v2_matrix(self) -> None:
        errors = self.matrix_errors(
            {
                "$schema": validate_artifacts.SCENARIO_MATRIX_SCHEMA_ID,
                "schemaVersion": 2,
                "artifactId": "example-run",
                "generatedAt": "2026-06-11T06:00:00Z",
                "runClass": "mm-live-canery",
                "scenarios": [
                    {"id": "live-fill", "scenario": "live fill", "status": "deferred", "evidence": None, "notes": "ok"},
                ],
            }
        )
        self.assertTrue(any("runClass 'mm-live-canery' must be one of: mm-live-canary" in error for error in errors), errors)


class CrashResistanceTests(unittest.TestCase):
    """JSON-sourced values can be arrays/objects; the validator must append errors, never raise."""

    def test_scenario_row_list_status_is_reported_not_raised(self) -> None:
        errors: list[str] = []
        validate_artifacts.validate_scenario_matrix(
            ROOT / "runs" / "example-run" / "scenario-matrix.json",
            {
                "$schema": validate_artifacts.SCENARIO_MATRIX_SCHEMA_ID,
                "schemaVersion": 2,
                "artifactId": "example-run",
                "generatedAt": "2026-06-11T06:00:00Z",
                "runClass": "mm-live-canary",
                "scenarios": [{"id": "live-fill", "scenario": "live fill", "status": ["pass"], "notes": "ok"}],
            },
            errors,
        )
        self.assertTrue(any("must be one of" in error for error in errors), errors)

    def test_scorecard_unhashable_values_are_reported_not_raised(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        scorecard["verdict"]["label"] = ["FULL_GREEN"]
        for row in scorecard["capabilities"]:
            if row["id"] == "live-fill":
                row["proof"] = ["proven_live"]
                del row["evidence"]
        scorecard["transactions"][0]["category"] = ["approve"]
        scorecard["transactions"][1]["status"] = {"value": "success"}
        evidence = make_postgame_deferred_evidence()
        evidence["status"] = ["partial"]
        evidence["artifactFiles"]["raw"] = ["raw/a.json", "raw/b.json"]
        evidence["target"]["teamIdentity"]["home"]["identity"] = ["favorite"]
        errors = run_scorecard_validation(scorecard, evidence)
        self.assertTrue(any("verdict.label" in error for error in errors), errors)
        self.assertTrue(any("proof" in error and "must be one of" in error for error in errors), errors)
        self.assertTrue(any("category" in error and "must be one of" in error for error in errors), errors)
        self.assertTrue(any("status must be success or reverted" in error for error in errors), errors)
        self.assertTrue(any("artifactFiles.raw must be a string path" in error for error in errors), errors)
        self.assertTrue(any("identity must be favorite, underdog, or even" in error for error in errors), errors)


class ErrorMessageQualityTests(unittest.TestCase):
    def test_missing_proof_key_is_not_reported_as_missing_row(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        for row in scorecard["capabilities"]:
            if row["id"] == "live-fill":
                del row["proof"]
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertTrue(any("missing required key 'proof'" in error for error in errors), errors)
        self.assertFalse(any("missing capability rows" in error for error in errors), errors)

    def test_invalid_proof_value_is_not_reported_as_missing_row(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        for row in scorecard["capabilities"]:
            if row["id"] == "live-fill":
                row["proof"] = "proven"
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertTrue(any("proof 'proven' must be one of" in error for error in errors), errors)
        self.assertFalse(any("missing capability rows" in error for error in errors), errors)

    def test_unknown_scorecard_run_class_is_rejected(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        scorecard["runClass"] = "mm-live-canary "
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertTrue(any("runClass 'mm-live-canary '" in error and "must be one of" in error for error in errors), errors)

    def test_zero_exposure_null_evidence_is_rejected(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        scorecard["zeroExposure"]["evidence"] = None
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertTrue(any("zeroExposure.evidence must be a non-empty string" in error for error in errors), errors)

    def test_zero_exposure_empty_evidence_is_rejected(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        scorecard["zeroExposure"]["evidence"] = ""
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertTrue(any("zeroExposure.evidence" in error for error in errors), errors)


class SignatureSafetyPatternTests(unittest.TestCase):
    def pattern(self, label: str):
        for pattern_label, compiled in validate_artifacts.SAFETY_PATTERNS:
            if pattern_label == label:
                return compiled
        raise AssertionError(f"safety pattern {label!r} is missing")

    def test_matches_signature_keyed_hex_values(self) -> None:
        pattern = self.pattern("signature/signedPayload-keyed hex value")
        self.assertIsNotNone(pattern.search('"signature": "0xdeadbeef12345678"'))
        self.assertIsNotNone(pattern.search('"rawSignature": "0xABCDEF0123456789"'))
        self.assertIsNotNone(pattern.search('"signedPayload": "0x00112233445566778899"'))
        self.assertIsNotNone(pattern.search('"makerSignature": "0xdeadbeef12345678"'))
        self.assertIsNotNone(pattern.search('"signatureHex": "deadbeef12345678"'))

    def test_ignores_redaction_and_presence_booleans(self) -> None:
        pattern = self.pattern("signature/signedPayload-keyed hex value")
        self.assertIsNone(pattern.search('"signatureRedacted": true'))
        self.assertIsNone(pattern.search('"rawSignatureRedacted": true'))
        self.assertIsNone(pattern.search('"signedPayloadPresent": false'))
        self.assertIsNone(pattern.search('"signature": "0xREDACTED"'))

    def test_matches_signature_sized_bare_hex(self) -> None:
        pattern = self.pattern("signature-sized bare hex")
        self.assertIsNotNone(pattern.search('"value": "' + "ab" * 65 + '"'))
        self.assertIsNotNone(pattern.search('"value": "0x' + "ab" * 64 + '"'))
        self.assertIsNone(pattern.search('"txHash": "0x' + "ab" * 32 + '"'))
        self.assertIsNone(pattern.search('"blob": "' + "ab" * 200 + '"'))

    def test_matches_signature_rs_components(self) -> None:
        pattern = self.pattern("signature r/s components")
        sample = '"r": "0x' + "ab" * 32 + '",\n  "s": "0x' + "cd" * 32 + '"'
        self.assertIsNotNone(pattern.search(sample))
        self.assertIsNone(pattern.search('"r": "0x' + "ab" * 32 + '"'))

    def test_matches_calldata_sized_hex_blob(self) -> None:
        pattern = self.pattern(validate_artifacts.LONG_HEX_LABEL)
        self.assertIsNotNone(pattern.search('"data": "0x' + "ab" * 100 + '"'))
        self.assertIsNone(pattern.search('"txHash": "0x' + "ab" * 32 + '"'))


class SchemaPointerPlacementTests(unittest.TestCase):
    def test_misnamed_scorecard_carrier_is_rejected(self) -> None:
        errors: list[str] = []
        docs = {ROOT / "runs" / "example-run" / "scorecard.json": {"$schema": validate_artifacts.MVE_SCORECARD_SCHEMA_ID}}
        validate_artifacts.validate_schema_pointers(docs, errors)
        self.assertTrue(any("must be named mve-scorecard.json" in error for error in errors), errors)

    def test_template_carriers_are_exempt(self) -> None:
        errors: list[str] = []
        docs = {
            ROOT / "templates" / "mm-live-canary" / "mve-scorecard.template.json": {
                "$schema": validate_artifacts.MVE_SCORECARD_SCHEMA_ID
            }
        }
        validate_artifacts.validate_schema_pointers(docs, errors)
        self.assertEqual(errors, [])

    def test_correctly_placed_carrier_passes(self) -> None:
        errors: list[str] = []
        docs = {
            ROOT / "runs" / "example-run" / "mve-scorecard.json": {"$schema": validate_artifacts.MVE_SCORECARD_SCHEMA_ID}
        }
        validate_artifacts.validate_schema_pointers(docs, errors)
        self.assertEqual(errors, [])


class RowCoherenceTests(unittest.TestCase):
    def test_matrix_fail_contradicting_proven_capability_is_rejected(self) -> None:
        errors: list[str] = []
        directory = ROOT / "runs" / "example-run"
        docs = {
            directory / "scenario-matrix.json": {
                "schemaVersion": 2,
                "runClass": "mm-live-canary",
                "scenarios": [{"id": "live-fill", "scenario": "live fill", "status": "fail", "notes": "no fill"}],
            },
            directory / "mve-scorecard.json": {
                "runClass": "mm-live-canary",
                "capabilities": [{"id": "live-fill", "capability": "Live fill", "proof": "proven_live", "notes": "ok"}],
            },
        }
        validate_artifacts.validate_adoption_pairing(docs, errors)
        self.assertTrue(any("contradicts mve-scorecard.json proof 'proven_live'" in error for error in errors), errors)

    def test_consistent_rows_pass(self) -> None:
        errors: list[str] = []
        directory = ROOT / "runs" / "example-run"
        docs = {
            directory / "scenario-matrix.json": {
                "schemaVersion": 2,
                "runClass": "mm-live-canary",
                "scenarios": [{"id": "live-fill", "scenario": "live fill", "status": "pass", "notes": "ok"}],
            },
            directory / "mve-scorecard.json": {
                "runClass": "mm-live-canary",
                "capabilities": [{"id": "live-fill", "capability": "Live fill", "proof": "proven_live", "notes": "ok"}],
            },
        }
        validate_artifacts.validate_adoption_pairing(docs, errors)
        self.assertEqual(errors, [])

    def _shared_id_contradicts(self, scenario_status: str, scorecard_proof: str) -> bool:
        errors: list[str] = []
        directory = ROOT / "runs" / "example-run"
        docs = {
            directory / "scenario-matrix.json": {
                "schemaVersion": 2,
                "runClass": "mm-live-canary",
                "scenarios": [{"id": "live-fill", "scenario": "live fill", "status": scenario_status, "notes": "n"}],
            },
            directory / "mve-scorecard.json": {
                "runClass": "mm-live-canary",
                "capabilities": [{"id": "live-fill", "capability": "Live fill", "proof": scorecard_proof, "notes": "n"}],
            },
        }
        validate_artifacts.validate_adoption_pairing(docs, errors)
        return any("contradicts mve-scorecard.json proof" in error for error in errors)

    def test_full_outcome_class_matrix(self) -> None:
        # proven = {pass, pass_with_caveats} / {proven_live, proven_synthetic_only}
        # failed = {fail} / {failed}; absent = {deferred, not_run, not_applicable} / {deferred, not_applicable}
        proven_scn = ["pass", "pass_with_caveats"]
        failed_scn = ["fail"]
        absent_scn = ["deferred", "not_run", "not_applicable"]
        proven_proof = ["proven_live", "proven_synthetic_only"]
        failed_proof = ["failed"]
        absent_proof = ["deferred", "not_applicable"]

        same_class = (
            [(s, p) for s in proven_scn for p in proven_proof]
            + [(s, p) for s in failed_scn for p in failed_proof]
            + [(s, p) for s in absent_scn for p in absent_proof]
        )
        for scenario_status, proof in same_class:
            self.assertFalse(self._shared_id_contradicts(scenario_status, proof), f"{scenario_status} vs {proof} should be coherent")

        cross_class = (
            [(s, p) for s in proven_scn for p in failed_proof + absent_proof]
            + [(s, p) for s in failed_scn for p in proven_proof + absent_proof]
            + [(s, p) for s in absent_scn for p in proven_proof + failed_proof]
        )
        for scenario_status, proof in cross_class:
            self.assertTrue(self._shared_id_contradicts(scenario_status, proof), f"{scenario_status} vs {proof} should contradict")

    def test_hermes_probe_cases_now_rejected(self) -> None:
        for scenario_status, proof in [
            ("pass", "deferred"),
            ("pass_with_caveats", "not_applicable"),
            ("fail", "deferred"),
            ("fail", "not_applicable"),
            ("deferred", "proven_live"),
            ("not_applicable", "proven_live"),
        ]:
            self.assertTrue(self._shared_id_contradicts(scenario_status, proof), f"{scenario_status} vs {proof}")


class TeamIdentityOddsTests(unittest.TestCase):
    def test_swapped_odds_signs_are_rejected(self) -> None:
        evidence = make_postgame_deferred_evidence()
        evidence["target"]["teamIdentity"]["home"]["marketOddsAmerican"] = "+114"
        evidence["target"]["teamIdentity"]["away"]["marketOddsAmerican"] = "-114"
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("favorite must carry negative American odds" in error for error in errors), errors)
        self.assertTrue(any("underdog must carry positive American odds" in error for error in errors), errors)

    def test_non_odds_string_is_rejected(self) -> None:
        evidence = make_postgame_deferred_evidence()
        evidence["target"]["teamIdentity"]["home"]["marketOddsAmerican"] = "banana"
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("must be signed American odds" in error for error in errors), errors)


class AdoptingEvidenceTests(unittest.TestCase):
    def test_missing_artifact_type_is_rejected(self) -> None:
        evidence = make_postgame_deferred_evidence()
        del evidence["artifactType"]
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("artifactType must be 'run'" in error for error in errors), errors)

    def test_dangling_artifact_files_path_is_rejected(self) -> None:
        evidence = make_postgame_deferred_evidence()
        evidence["artifactFiles"]["cliPostgame"] = "raw/this-file-does-not-exist.json"
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("artifactFiles.cliPostgame" in error and "does not exist" in error for error in errors), errors)

    def test_superseded_requires_successor_pointer(self) -> None:
        evidence = make_postgame_deferred_evidence()
        evidence["status"] = "superseded"
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("requires a supersededBy pointer" in error for error in errors), errors)

    def test_superseded_with_valid_successor_passes(self) -> None:
        evidence = make_postgame_deferred_evidence()
        evidence["status"] = "superseded"
        evidence["supersededBy"] = (
            "runs/2026-06-11-mlb-stl-nym-contest-36-mm-alpha-release-repeatability-canary/evidence.json"
        )
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertEqual(errors, [])

    def test_companion_file_evidence_reference_is_rejected(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        for row in scorecard["capabilities"]:
            if row["id"] == "live-fill":
                row["evidence"] = "summary.md"
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertTrue(any("not the artifact's own companion files" in error for error in errors), errors)

    def test_adopting_run_requires_target(self) -> None:
        evidence = make_postgame_deferred_evidence()
        del evidence["target"]
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("target must be an object" in error for error in errors), errors)

    def test_target_requires_market_and_team_names(self) -> None:
        evidence = make_postgame_deferred_evidence()
        evidence["target"] = {"teamIdentity": evidence["target"]["teamIdentity"]}
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("target.market must be a non-empty string" in error for error in errors), errors)
        self.assertTrue(any("target.homeTeam must be a non-empty string" in error for error in errors), errors)
        self.assertTrue(any("target.awayTeam must be a non-empty string" in error for error in errors), errors)

    def test_team_identity_must_match_target_teams(self) -> None:
        evidence = make_postgame_deferred_evidence()
        evidence["target"]["teamIdentity"]["home"]["team"] = "Houston Astros"
        evidence["target"]["teamIdentity"]["away"]["team"] = "Los Angeles Angels"
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("must equal target.homeTeam" in error for error in errors), errors)
        self.assertTrue(any("must equal target.awayTeam" in error for error in errors), errors)

    def test_directory_evidence_path_is_rejected(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        for row in scorecard["capabilities"]:
            if row["id"] == "live-fill":
                row["evidence"] = "raw/"
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertTrue(any("must point at a sanitized evidence file, not a directory" in error for error in errors), errors)

    def test_superseded_by_must_target_run_evidence(self) -> None:
        evidence = make_postgame_deferred_evidence()
        evidence["status"] = "superseded"
        evidence["supersededBy"] = "README.md"
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("must point at another run's evidence JSON" in error for error in errors), errors)

    def test_full_green_rejects_synthetic_only_live_fill(self) -> None:
        scorecard = make_full_green_scorecard()
        for row in scorecard["capabilities"]:
            if row["id"] == "live-fill":
                row["proof"] = "proven_synthetic_only"
        errors = run_scorecard_validation(scorecard, make_full_green_evidence())
        self.assertTrue(any("requires proven_live capabilities" in error for error in errors), errors)

    def test_full_green_rejects_synthetic_only_postgame(self) -> None:
        scorecard = make_full_green_scorecard()
        for row in scorecard["capabilities"]:
            if row["id"] == "postgame-settle":
                row["proof"] = "proven_synthetic_only"
        errors = run_scorecard_validation(scorecard, make_full_green_evidence())
        self.assertTrue(any("requires proven_live capabilities" in error and "postgame-settle" in error for error in errors), errors)

    def test_amber_no_fill_baseline_passes(self) -> None:
        errors = run_scorecard_validation(make_amber_no_fill_scorecard(), make_amber_no_fill_evidence())
        self.assertEqual(errors, [])

    def test_amber_no_fill_rejects_successful_fill_transaction(self) -> None:
        scorecard = make_amber_no_fill_scorecard()
        scorecard["transactions"].append(
            {"category": "match-commitment", "txHash": TX_B, "status": "success", "operatorControlled": True, "purpose": "a fill"}
        )
        errors = run_scorecard_validation(scorecard, make_amber_no_fill_evidence())
        self.assertTrue(any("cannot include a successful match-commitment" in error for error in errors), errors)

    def test_amber_no_fill_allows_reverted_fill_attempt(self) -> None:
        scorecard = make_amber_no_fill_scorecard()
        scorecard["transactions"].append(
            {"category": "match-commitment", "txHash": TX_B, "status": "reverted", "operatorControlled": True, "purpose": "failed fill attempt"}
        )
        errors = run_scorecard_validation(scorecard, make_amber_no_fill_evidence())
        self.assertEqual(errors, [])


class MarketVocabularyTests(unittest.TestCase):
    def test_canonical_moneyline_passes(self) -> None:
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), make_postgame_deferred_evidence())
        self.assertEqual(errors, [])

    def test_market_case_variant_is_rejected_and_still_requires_team_identity(self) -> None:
        evidence = make_postgame_deferred_evidence()
        evidence["target"]["market"] = "Moneyline"
        del evidence["target"]["teamIdentity"]
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("must be exactly one of" in error for error in errors), errors)
        self.assertTrue(any("teamIdentity object" in error for error in errors), errors)

    def test_market_trailing_space_is_rejected_and_still_requires_team_identity(self) -> None:
        evidence = make_postgame_deferred_evidence()
        evidence["target"]["market"] = "moneyline "
        del evidence["target"]["teamIdentity"]
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("must be exactly one of" in error for error in errors), errors)
        self.assertTrue(any("teamIdentity object" in error for error in errors), errors)

    def test_unknown_market_is_rejected(self) -> None:
        evidence = make_postgame_deferred_evidence()
        evidence["target"]["market"] = "monyline"
        del evidence["target"]["teamIdentity"]
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("must be exactly one of" in error for error in errors), errors)

    def test_spread_market_passes_without_team_identity(self) -> None:
        evidence = make_postgame_deferred_evidence()
        evidence["target"]["market"] = "spread"
        del evidence["target"]["teamIdentity"]
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertEqual(errors, [])


class AmberFillTelemetryTests(unittest.TestCase):
    def test_amber_no_fill_rejects_proven_canonical_fill(self) -> None:
        scorecard = make_amber_no_fill_scorecard()
        for row in scorecard["capabilities"]:
            if row["id"] == "own-state-sse-canonical-fill":
                row["proof"] = "proven_live"
                row["evidence"] = "raw/own-state-sse-summary.sanitized.json"
        errors = run_scorecard_validation(scorecard, make_amber_no_fill_evidence())
        self.assertTrue(any("own-state-sse-canonical-fill" in error and "implies a fill occurred" in error for error in errors), errors)

    def test_amber_no_fill_allows_not_applicable_canonical_fill(self) -> None:
        scorecard = make_amber_no_fill_scorecard()
        for row in scorecard["capabilities"]:
            if row["id"] == "own-state-sse-canonical-fill":
                row["proof"] = "not_applicable"
                row["evidence"] = None
        errors = run_scorecard_validation(scorecard, make_amber_no_fill_evidence())
        self.assertEqual(errors, [])


class EvenPickemTests(unittest.TestCase):
    def _evidence_with_even(self, home_odds: str, away_odds: str) -> dict:
        evidence = make_postgame_deferred_evidence()
        ti = evidence["target"]["teamIdentity"]
        ti["home"]["identity"] = "even"
        ti["home"]["marketOddsAmerican"] = home_odds
        ti["away"]["identity"] = "even"
        ti["away"]["marketOddsAmerican"] = away_odds
        return evidence

    def test_standard_vigged_pickem_passes(self) -> None:
        for home, away in [("-110", "-110"), ("-105", "-115"), ("-100", "+100"), ("+100", "+100")]:
            errors = run_scorecard_validation(make_postgame_deferred_scorecard(), self._evidence_with_even(home, away))
            self.assertEqual(errors, [], f"{home}/{away}: {errors}")

    def test_lopsided_line_mislabeled_even_is_rejected(self) -> None:
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), self._evidence_with_even("-150", "+130"))
        self.assertTrue(any("even/even pick'em requires symmetric odds" in error for error in errors), errors)


class GreenDeferredPostgameTxTests(unittest.TestCase):
    def test_green_deferred_rejects_successful_settle(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        scorecard["transactions"].append(
            {"category": "settle", "txHash": TX_E, "status": "success", "operatorControlled": True, "purpose": "p"}
        )
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertTrue(any("cannot include successful postgame transaction categories" in e for e in errors), errors)


class AmberPostgameTxTests(unittest.TestCase):
    def test_amber_no_fill_allows_speculation_level_settle(self) -> None:
        # settle is speculation-level; AMBER_QUOTED_NO_FILL claims only "no fill", not "no postgame".
        scorecard = make_amber_no_fill_scorecard()
        scorecard["transactions"].append(
            {"category": "settle", "txHash": TX_E, "status": "success", "operatorControlled": True, "purpose": "settle the contest"}
        )
        errors = run_scorecard_validation(scorecard, make_amber_no_fill_evidence())
        self.assertEqual(errors, [])

    def test_amber_no_fill_rejects_successful_seed_match(self) -> None:
        scorecard = make_amber_no_fill_scorecard()
        scorecard["transactions"].append(
            {"category": "seed-match", "txHash": TX_E, "status": "success", "operatorControlled": True, "purpose": "seed"}
        )
        errors = run_scorecard_validation(scorecard, make_amber_no_fill_evidence())
        self.assertTrue(any("cannot include a successful" in e and "seed-match" in e for e in errors), errors)

    def test_amber_no_fill_allows_reverted_seed_match(self) -> None:
        scorecard = make_amber_no_fill_scorecard()
        scorecard["transactions"].append(
            {"category": "seed-match", "txHash": TX_E, "status": "reverted", "operatorControlled": True, "purpose": "seed"}
        )
        errors = run_scorecard_validation(scorecard, make_amber_no_fill_evidence())
        self.assertEqual(errors, [])


class LiveFillTxTests(unittest.TestCase):
    def test_green_deferred_live_fill_requires_fill_tx(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        scorecard["transactions"] = [tx for tx in scorecard["transactions"] if tx["category"] not in validate_artifacts.FILL_TX_CATEGORIES]
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertTrue(any("live-fill proven_live requires a successful fill transaction" in e for e in errors), errors)

    def test_full_green_live_fill_requires_fill_tx(self) -> None:
        scorecard = make_full_green_scorecard()
        scorecard["transactions"] = [tx for tx in scorecard["transactions"] if tx["category"] not in validate_artifacts.FILL_TX_CATEGORIES]
        errors = run_scorecard_validation(scorecard, make_full_green_evidence())
        self.assertTrue(any("live-fill proven_live requires a successful fill transaction" in e for e in errors), errors)

    def test_reverted_fill_tx_does_not_satisfy_proven_live(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        for tx in scorecard["transactions"]:
            if tx["category"] == "match-commitment":
                tx["status"] = "reverted"
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertTrue(any("live-fill proven_live requires a successful fill transaction" in e for e in errors), errors)

    def test_seed_match_satisfies_live_fill(self) -> None:
        scorecard = make_postgame_deferred_scorecard()
        for tx in scorecard["transactions"]:
            if tx["category"] == "match-commitment":
                tx["category"] = "seed-match"
        errors = run_scorecard_validation(scorecard, make_postgame_deferred_evidence())
        self.assertEqual(errors, [])


class TargetIdentityTests(unittest.TestCase):
    def test_missing_contest_id_is_rejected(self) -> None:
        evidence = make_postgame_deferred_evidence()
        del evidence["target"]["contestId"]
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("target.contestId must be a non-empty string" in e for e in errors), errors)

    def test_contest_id_mismatching_directory_is_rejected(self) -> None:
        evidence = make_postgame_deferred_evidence()
        evidence["target"]["contestId"] = "99"
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("must match the contest id in the run directory name" in e for e in errors), errors)

    def test_missing_speculation_id_is_rejected(self) -> None:
        evidence = make_postgame_deferred_evidence()
        del evidence["target"]["speculationId"]
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("target.speculationId must be a non-empty string" in e for e in errors), errors)

    def test_sport_mismatching_directory_is_rejected(self) -> None:
        evidence = make_postgame_deferred_evidence()
        evidence["target"]["sport"] = "nfl"
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), evidence)
        self.assertTrue(any("must match the sport in the run directory name" in e for e in errors), errors)

    def test_consistent_identity_passes(self) -> None:
        errors = run_scorecard_validation(make_postgame_deferred_scorecard(), make_postgame_deferred_evidence())
        self.assertEqual(errors, [])


class TemplateCoherenceTests(unittest.TestCase):
    """The shipped templates must validate cleanly once only the placeholder tokens are filled."""

    def _load(self, name: str) -> dict:
        return json.loads((TEMPLATE_DIR / name).read_text(encoding="utf-8"))

    def _fill_tokens(self, scorecard: dict) -> dict:
        scorecard["artifactId"] = SAMPLE_RUN_DIR.name
        scorecard["generatedAt"] = "2026-06-11T06:00:00Z"
        scorecard["zeroExposure"]["checkedAtUtc"] = "2026-06-11T06:00:00Z"
        scorecard["zeroExposure"]["evidence"] = "raw/tx-receipts.summary.json"
        for row in scorecard["capabilities"]:
            if row.get("evidence") is not None:
                row["evidence"] = "raw/tx-receipts.summary.json"
        for idx, tx in enumerate(scorecard["transactions"]):
            tx["txHash"] = "0x" + f"{idx:02d}" * 32
        return scorecard

    def test_scorecard_template_is_internally_coherent(self) -> None:
        scorecard = self._fill_tokens(self._load("mve-scorecard.template.json"))
        evidence = make_postgame_deferred_evidence()
        errors = run_scorecard_validation(scorecard, evidence)
        self.assertEqual(errors, [], errors)

    def test_scenario_matrix_template_is_valid(self) -> None:
        matrix = self._load("scenario-matrix.template.json")
        matrix["artifactId"] = SAMPLE_RUN_DIR.name
        matrix["generatedAt"] = "2026-06-11T06:00:00Z"
        for row in matrix["scenarios"]:
            if row.get("evidence") is not None:
                row["evidence"] = "raw/tx-receipts.summary.json"
        errors: list[str] = []
        validate_artifacts.validate_scenario_matrix(SAMPLE_RUN_DIR / "scenario-matrix.json", matrix, errors)
        self.assertEqual(errors, [], errors)

    def test_template_pair_has_no_shared_id_contradiction(self) -> None:
        matrix = self._load("scenario-matrix.template.json")
        scorecard = self._load("mve-scorecard.template.json")
        errors: list[str] = []
        docs = {
            SAMPLE_RUN_DIR / "scenario-matrix.json": matrix,
            SAMPLE_RUN_DIR / "mve-scorecard.json": scorecard,
        }
        validate_artifacts.validate_adoption_pairing(docs, errors)
        self.assertFalse(any("contradicts mve-scorecard.json proof" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
