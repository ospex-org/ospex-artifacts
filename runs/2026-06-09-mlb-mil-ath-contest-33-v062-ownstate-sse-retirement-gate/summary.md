# MIL/ATH v0.6.2 own-state SSE retirement-gate pre-test — GREEN with deferred postgame lifecycle

**Status:** `complete_verified_with_caveats` / **GREEN pre-test / PASS with allowed postgame lifecycle deferral**.

## Verdict

The v0.6.2 re-run passed the retirement-gate pre-test rows that were load-bearing for the v0.6.0/v0.6.1 fixes. The full-soak operator watcher used the released CLI `0.6.2`, stayed continuously connected from cold start through shutdown, and proved the passive-expiry regression fix: heartbeat `liveCommitmentCount` fell from `2` to `0` without a fresh snapshot/reconnect, and final `summary.liveCommitmentCount` was `0`. A fresh post-drain watch also reported `0`, and public/orderbook state was empty.

The result authorizes treating the own-state SSE path as sufficient for the pre-test evidence, with the explicit caveat that postgame score/settle/claim for contest `33` is still a separate live-position cleanup obligation because the game had not started during this run.

## Target and team identity

- Game: Milwaukee Brewers @ Athletics
- Contest id: `33`; speculation id: `23`; market: moneyline
- Start: `2026-06-10T02:05:00+00:00` UTC; contest status during run: `verified`
- Team identity: Milwaukee Brewers = away / underdog by reference implied probability during run; Athletics = home / favorite by reference implied probability during run.

## Runtime alignment

- Released CLI used by operator watch: `0.6.2`.
- SDK tag `v0.6.2`: `7632955d0c689a04d3e40b2cca2653cf772119c3`.
- `ospex-market-maker` realignment PR #88 merged at `2026-06-09T20:44:20Z`.
- `yarn smoke` in `ospex-market-maker` and `yarn build && yarn typecheck && yarn test` in `ospex-sdk` were green during preflight.
- Evidence: `raw/release-version-matrix.sanitized.json`, `raw/mm-doctor-before-live.sanitized.json`.
- Public artifact hygiene: raw signatures and `signedPayload` structs are excluded; only redaction/presence booleans such as `signatureRedacted` and `signedPayloadPresent` are published.

## Observer evidence

- Full-soak watch counts: `{'heartbeat': 56, 'snapshot': 1, 'ready': 1, 'status': 1, 'commitment': 26, 'fill': 2, 'positionStatus': 2, 'summary': 1}`.
- Full-soak watch summary: `readyObserved=True`, `lastStatus=connected`, `liveCommitmentCount=0`, `exitReason=signal`, `linesAfterSummary=0`.
- Passive expiry proof: last positive heartbeat `2026-06-09T21:25:37.054Z` count `2` → first zero heartbeat `2026-06-09T21:25:57.051Z` count `0`.
- Fresh post-drain watch summary: `liveCommitmentCount=0`, `readyObserved=True`, `exitReason=until-ready`.

## Coverage highlights

- Normal visible fill: `0xcbdbe0afc35393a98cb4b59bc42f12cbaff449ad72968d075620328e04494791`; maker side away / Milwaukee Brewers; taker side home / Athletics.
- Partial fill: `0xa67bad453d28550a6ec255abacdde4e5c62d4546d94e31926adc1a6e06bca3d9`; taker risk `0.050000 USDC`; MM telemetry `newFillWei6=50000`.
- Soft-cancel/hidden recovery: commitment `0xe667b0f9cdd62bdc58282a4ff8c89cc2b580656170a8fe67f4d740522bf4b4eb` became `visibility:hidden` in owner watch with `signedPayloadPresent:true`; anonymous public list did not contain the hash.
- Expiry/replacement: MM telemetry recorded `3` replace event(s) and `3` expire event(s).
- Reconnect: separate v0.6.2 probe through a local drop proxy saw statuses `['connected', 'reconnecting', 'connected']` with `2` ready events.
- Restart/resume: restart run emitted `1` `stream-cold-restart` event and no fill telemetry in the restart run.
- No duplicate fill telemetry: watch fill keys unique = `True`; MM fill keys unique = `True`.
- Audit divergence events: `0`.

## Drain-to-zero

- Maker visible commitments: `0`.
- Public speculation commitments/orderbook: `0` / `0`.
- Full-soak watch summary live count: `0`.
- Fresh watch live count: `0`.
- Orphan process scan matches: `0`.

## Budget / cost

- New matched maker risk: `0.250000 USDC`.
- New matched taker risk: `0.266000 USDC`.
- Carry-over maker position risk observed from the v0.6.0 run: `0.346200 USDC`.
- Confirmed write receipts parsed: `7`.
- Total gas across two match txs and five on-chain cancel txs: `0.263331208166012854 POL`.
- Under the `≤5.00 USDC` controlled tiny-risk cap.

## Caveats / follow-up

1. Score → settle → claim is deferred per the scenario allowance because contest `33` had not started. Claim-all dry-runs for maker and taker returned zero entries; postgame cleanup remains required after official finality.
2. Two initial `PositionWithoutCommitment` MM audit-poll errors were observed because this run reused contest `33` with carry-over filled positions and a fresh local MM state. They did not persist as divergence and did not cause duplicate fill telemetry or non-zero final exposure.
3. Reconnect coverage used a separate operator watch/proxy so the full-soak watch could remain never-reconnected for the v0.6.2 passive-expiry regression proof.

## Files

- Evidence: `evidence.json`
- Scenario matrix: `scenario-matrix.md`, `scenario-matrix.json`
- Sanitized raw evidence: `raw/`
