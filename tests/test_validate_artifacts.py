#!/usr/bin/env python3
"""Unit tests for the artifact validator."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate-artifacts.py"

spec = importlib.util.spec_from_file_location("validate_artifacts", VALIDATOR_PATH)
assert spec is not None and spec.loader is not None
validate_artifacts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_artifacts)


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


if __name__ == "__main__":
    unittest.main()
