# Test Harness Expectations

These expectations apply to live Ospex artifact runs and release-acceptance gates that perform chain writes. They keep harness assertions aligned with Ospex's split between canonical on-chain state and derived API/Supabase projections.

## Post-write assertion contract

For every write gate that is part of the artifact scope, the harness should record two separate facts:

1. **Transaction confirmation** — the write transaction receipt succeeded on-chain (`status=0x1`, tx hash, block, and purpose recorded).
2. **Projection convergence** — the relevant API/indexer read model reached the expected post-write state before the harness makes final assertions.

A confirmed transaction followed by one stale immediate API read is not, by itself, a protocol failure. It is projection lag if the projection converges inside the documented wait window. The artifact should record both the stale observation and the later converged state.

## Required waits by lifecycle step

Live lifecycle harnesses should wait for these convergence targets before declaring the step green:

- **After contest create:** contest detail resolves by `contestId`, `verifiedAt`/verification status is visible when verification is in scope, and list/search projections eventually show the contest-created state.
- **After commitment submit/fill:** commitment/fill projection reflects the filled or no-longer-live commitment, positions are created for both sides, and visible live commitments exclude expired/cancelled/filled rows.
- **After score:** contest status/final score projection reflects the canonical scored state; source score evidence remains recorded separately.
- **After settle:** speculation status reaches settled/closed, and winning positions move out of `pendingSettle` into the claimable bucket.
- **After claim:** claim transaction receipt is successful, `claim-all --dry-run` or equivalent chain-aware command reports no remaining actionable claims, and the positions projection converges to `claimableCount=0` and/or `claimed=true` for the winning positions.

## Harness UX wording

When a tx is confirmed but the API/indexer read model has not caught up yet, harness/CLI output should use language like:

```text
tx confirmed; waiting for API projection...
```

It should not surface the first stale read as a final failure unless convergence times out.

## Artifact JSON contract

Artifacts may encode the convergence evidence in a top-level `projectionConvergence` object:

```json
{
  "projectionConvergence": {
    "expectation": "tx confirmed; waiting for API projection before final assertions",
    "gates": [
      {
        "name": "postClaim",
        "afterWrite": "claim",
        "txConfirmed": true,
        "waitTarget": "claimableCount=0 and position.claimed=true",
        "expectedFinalState": ["claimableCount=0", "position.claimed=true"],
        "observedFinalState": ["claim-all dry-run entries=0", "positions status claimableCount=0"],
        "converged": true,
        "staleReadObserved": true
      }
    ]
  }
}
```

`python3 scripts/validate-artifacts.py` validates this shape whenever the object is present. Future live-write artifacts should include it directly or explain why a projection wait was out of scope.
