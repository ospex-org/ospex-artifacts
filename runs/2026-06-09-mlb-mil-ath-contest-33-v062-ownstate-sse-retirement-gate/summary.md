# MIL/ATH v0.6.2 own-state SSE retirement-gate — GREEN complete

**Status:** `complete_verified_with_caveats` / **GREEN / PASS complete with postgame lifecycle claimed**.

## Verdict

The v0.6.2 re-run passed the own-state SSE retirement-gate. The full-soak operator watcher used the released CLI `0.6.2`, stayed continuously connected from cold start through shutdown, and proved the passive-expiry regression fix: heartbeat `liveCommitmentCount` fell from `2` to `0` without a fresh snapshot/reconnect, and final `summary.liveCommitmentCount` was `0`. A fresh post-drain watch also reported `0`, and public/orderbook state was empty.

The postgame lifecycle is now complete. The independent final-score source reported Athletics `7`, Milwaukee Brewers `5`; contest `33` was scored, speculation `23` closed with `home/lower` as the winner, both controlled winning lower positions were claimed, and final `claim-all --dry-run` sweeps for both controlled wallets returned zero entries.

## Target and team identity

- Game: Milwaukee Brewers @ Athletics
- Contest id: `33`; speculation id: `23`; market: moneyline
- Start: `2026-06-10T02:05:00+00:00` UTC
- Final: Milwaukee Brewers `5`, Athletics `7`
- Team identity: Milwaukee Brewers = away / upper / underdog by reference implied probability during run; Athletics = home / lower / favorite by reference implied probability during run and final winner.

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
- Post-claim own-state read-only probes for maker and taker both reached `ready` with `liveCommitmentCount=0`.

## Coverage highlights

- Normal visible fill: `0xcbdbe0afc35393a98cb4b59bc42f12cbaff449ad72968d075620328e04494791`; maker side away / Milwaukee Brewers; taker side home / Athletics.
- Partial fill: `0xa67bad453d28550a6ec255abacdde4e5c62d4546d94e31926adc1a6e06bca3d9`; taker risk `0.050000 USDC`; MM telemetry `newFillWei6=50000`.
- Soft-cancel/hidden recovery: commitment `0xe667b0f9cdd62bdc58282a4ff8c89cc2b580656170a8fe67f4d740522bf4b4eb` became `visibility:hidden` in owner watch with `signedPayloadPresent:true`; anonymous public list did not contain the hash.
- Expiry/replacement: MM telemetry recorded `3` replace event(s) and `3` expire event(s).
- Reconnect: separate v0.6.2 probe through a local drop proxy saw statuses `['connected', 'reconnecting', 'connected']` with `2` ready events.
- Restart/resume: restart run emitted `1` `stream-cold-restart` event and no fill telemetry in the restart run.
- No duplicate fill telemetry: watch fill keys unique = `True`; MM fill keys unique = `True`.
- Audit divergence events: `0`.
- Score → settle → claim: score request `0x965d72f833aa9338c75af7245bb638239f2946e89ca1a899c80342aa1a8fa901`, score callback `0x1c0cf69e522e78fd6bd180a8d256b816f2dc0c9c73c96ceccce4b4a6ea46bf72`, settle `0xe30337862ba55ee963968fb959caa4b4b36ff1869067de9b13fcc0585fa0c606`, maker claim `0x0b477a0b92ac83a0c43ad3107f5d5728703ca84bbfbdb821f9a7ba5701757545`, taker claim `0x1de3508cdc9b42d98f8cdc682a6bd5b669814f6d4fd179225cfaaba10086a38a`.

## Drain-to-zero / postgame cleanup

- Maker visible commitments: `0`.
- Public speculation commitments/orderbook: `0` / `0`.
- Full-soak watch summary live count: `0`.
- Fresh watch live count: `0`.
- Orphan process scan matches: `0`.
- Final postgame maker claim dry-run entries: `0`.
- Final postgame taker claim dry-run entries: `0`.
- Winning lower/home positions claimed: maker payout `0.702000 USDC`; taker payout `0.512096 USDC`.

## Budget / cost

- New matched maker risk: `0.250000 USDC`.
- New matched taker risk: `0.266000 USDC`.
- Carry-over maker position risk observed from the v0.6.0 run: `0.346200 USDC`.
- Postgame controlled gas: `0.298666188081483846 POL`.
- Score request LINK spent: `0.005000 LINK`.
- Total operator-controlled gas across run + postgame: `0.561997396247496700 POL`.
- Under the `≤5.00 USDC` controlled tiny-risk cap.

## Caveats

1. Two initial `PositionWithoutCommitment` MM audit-poll errors were observed because this run reused contest `33` with carry-over filled positions and a fresh local MM state. They did not persist as divergence and did not cause duplicate fill telemetry or non-zero final exposure.
2. Reconnect coverage used a separate operator watch/proxy so the full-soak watch could remain never-reconnected for the v0.6.2 passive-expiry regression proof.

## Files

- Evidence: `evidence.json`
- Scenario matrix: `scenario-matrix.md`, `scenario-matrix.json`
- Postgame lifecycle: `raw/postgame-lifecycle.sanitized.json`, `raw/final-score-source.sanitized.json`, `raw/cli-postgame.sanitized.json`
- Sanitized raw evidence: `raw/`
