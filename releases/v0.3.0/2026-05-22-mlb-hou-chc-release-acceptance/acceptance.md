# Ospex v0.3.0 release acceptance — Houston Astros @ Chicago Cubs

Status: **Stage 0 green** — public release install/read-only smoke passed, bounded live approvals succeeded, and the target contest was created and Chainlink-verified before first pitch.

## Scope

Validate that the public `v0.3.0` SDK/CLI release assets can be installed and used from a fresh environment, then use the early MLB game as a bounded live acceptance target.

## Release assets

- Release: `ospex-org/ospex-sdk` `v0.3.0`
- Published: 2026-05-22T15:25:19Z
- `ospex-sdk-0.3.0.tgz` sha256 `10a35b0e4b0806476a4709a4a81b60b5c58e16fc1cff45e08aa54fbfadb9d5c1`
- `ospex-cli-0.3.0.tgz` sha256 `62fdbf2328c65079b8784a802b81dfe6f70e89616103f1f6db01c9f4ee8a85a6`

## Target game

- Sport: MLB
- Matchup: Houston Astros @ Chicago Cubs
- Start: 2026-05-22T18:20:00Z
- Ospex gameId: `ccfee4a7-10b8-4c14-a565-49abda5c50db`
- Slug: `hou-chc-2026-05-22`
- Contest ID: `17`
- Contest status: `verified`
- Contest creator: `0x4ddfeeb90b53f7616135ce9d2b8f317af3c4066d`
- Created at: `2026-05-22T16:57:05+00:00`
- Verified at: `2026-05-22T16:57:17+00:00`

## Setup evidence

- Fresh Docker install from release tarballs succeeded.
- CLI version output: `0.3.0`.
- CLI help rendered successfully.
- `games list` JSON found the target game.
- npm high/critical audit gate passed.
- npm registry signatures/attestations gate passed.
- Low-value signer auth-check gate passed in the harness.

## Live gate evidence

- Bounded approvals succeeded for the low-value acceptance wallet:
  - LINK: `0.005` for OracleModule
  - Treasury USDC: `1.5`
  - Position risk USDC: `2`
- Approval txs:
  - PositionModule USDC approval: `0x6f91eb48ebb0a34dee26c9d086a71404af3a220fd4a02e46eeef6c3b8f902c1c`
  - TreasuryModule USDC approval: `0x08e067ec813dd5f43db6d5f92068db56be8824a09802015600d847d1ba59050a`
  - OracleModule LINK approval: `0x48c8f6e2f66132bb1024e37c134f5e854d042023c3366bcf5c186069927d9959`
- Doctor after approvals: green for match, submit, and create.
- Contest create tx: `0x7873e5136aadee555aee3411a4dbf1d67e1e65c874ef8cdbe71cb8ea283e5792`
- Chainlink request ID: `0xcae5ff511fdc2c4204e7cd7b6f722f48ac70c782a4c0ac5bcfaa9162802454cd`
- Contest verification result: `verified`.
- Final games-list readiness shows `contestCreated=true` and `contestId=17`.


## Stream-specific monitoring add-on

- Monitor command shape: `ospex odds watch 17 --json --include-refreshes`.
- Smoke duration: `90s`.
- Verdict: `pass` — snapshots and connected statuses were received for `moneyline`, `spread`, and `total`; refreshes were received for all three markets.
- Aggregate event counts: `snapshot=3`, `status=3`, `refresh=6`, `change=0` during the 90s smoke. No change event during a short sample is acceptable because refreshes prove the stream is live even when prices do not move.
- Public-safety checks: no provider/source-name leak terms, no secret/config leak terms, no non-JSON stdout lines, and no stderr lines in the smoke summary.
- Artifacts: `raw/odds-stream-smoke.summary.json`, `raw/odds-stream-smoke.summary.md`, `raw/odds-stream-smoke.received.ndjson`.
- Implementation scope: testing harness only; no product repo code change was required to run this monitor. If this monitor later reports missing events, stale `pollCapturedAt`, malformed JSON, degraded/reconnect loops, or provider/source leakage, that result would be evidence for a v0.3.1 investigation.

## Observations

- `npm audit` reports a moderate `ws` advisory via `ethers`; no high/critical findings and no available fix in the current dependency tree. Track as non-blocking unless project policy changes.
- The games list captured immediately after create still showed `contestCreated=false` / `contestId=null`, but the verified contest detail was already available and the later readiness games list showed `contestCreated=true` / `contestId=17`. Treat as transient API/indexer/list projection lag, not a contest-create failure.
- Final doctor after contest creation has match/submit readiness green, but create-contest readiness red because the exact `0.005` LINK OracleModule allowance was consumed by this contest creation. This is an allowance state for future contest creation, not a balance warning: `ospex-fresh-user` still had `0.295 LINK` afterward, which is healthy; only warn on LINK balance below roughly `0.02 LINK`.
- Optional tiny commitment submit/match was not run in this Stage 0 pass.

## Sanitized raw artifacts

- `acceptance.json`
- `raw/live-gates.json`
- `raw/tx-receipts.summary.json`
- `raw/contest-create-live.sanitized.json`
- `raw/contest-show-17.sanitized.json`
- `raw/doctor-after-approvals.sanitized.json`
- `raw/doctor-after-create.sanitized.json`
- `raw/games-target-final.sanitized.json`
- `raw/odds-stream-smoke.summary.json`
- `raw/odds-stream-smoke.summary.md`
- `raw/odds-stream-smoke.received.ndjson`
