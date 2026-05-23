# Ospex v0.3.0 release acceptance — Houston Astros @ Chicago Cubs

Status: **Stage 0 green + postgame scoring complete** — public release install/read-only smoke passed, bounded live approvals succeeded, the target contest was created and Chainlink-verified before first pitch, odds-stream monitoring passed through first pitch, and postgame scoring set the correct final score.

## Scope

Validate that the public `v0.3.0` SDK/CLI release assets can be installed and used from a fresh environment, then use the early MLB game as a bounded live acceptance target. Postgame scoring was also completed after the game ended. This artifact does **not** claim a full fill/settle/claim market lifecycle because the optional tiny commitment submit/match was not run and the contest had zero speculations.

## Release assets

- Release: `ospex-org/ospex-sdk` `v0.3.0`
- Published: 2026-05-22T15:25:19Z
- `ospex-sdk-0.3.0.tgz` sha256 `10a35b0e4b0806476a4709a4a81b60b5c58e16fc1cff45e08aa54fbfadb9d5c1`
- `ospex-cli-0.3.0.tgz` sha256 `62fdbf2328c65079b8784a802b81dfe6f70e89616103f1f6db01c9f4ee8a85a6`

## Target game

- Sport: MLB
- Matchup: Houston Astros @ Chicago Cubs
- Start: 2026-05-22T18:20:00Z
- External final score cross-check: Astros 4, Cubs 2
- Ospex gameId: `ccfee4a7-10b8-4c14-a565-49abda5c50db`
- Slug: `hou-chc-2026-05-22`
- Contest ID: `17`
- Contest status: `scored`
- Contest score: Houston Astros `4`, Chicago Cubs `2`
- Contest creator: `0x4ddfeeb90b53f7616135ce9d2b8f317af3c4066d`
- Created at: `2026-05-22T16:57:05+00:00`
- Verified at: `2026-05-22T16:57:17+00:00`
- Scored at: `2026-05-22T21:51:20+00:00`

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
- Post-create projection convergence passed: the immediate games list was stale, but contest detail resolved verified and a later games-list read converged to `contestCreated=true` / `contestId=17` before the gate was declared green.

## Stream-specific monitoring add-on

- Monitor command shape: `ospex odds watch 17 --json --include-refreshes`.
- Smoke verdict: `pass` over `90s` — snapshots, connected statuses, and refreshes arrived for `moneyline`, `spread`, and `total`.
- Through-first-pitch verdict: `pass` over `3000.03s`, from `2026-05-22T17:53:07.658599Z` to `2026-05-22T18:43:07.688607Z`.
- Through-first-pitch aggregate event counts: `snapshot=3`, `status=3`, `refresh=74`, `change=7`.
- Through-first-pitch per-market events:
  - `moneyline`: `snapshot=1`, `status=1`, `refresh=22`, `change=5`; max event gap `61.164s`; max poll age `23.203s`.
  - `spread`: `snapshot=1`, `status=1`, `refresh=26`, `change=1`; max event gap `61.164s`; max poll age `23.141s`.
  - `total`: `snapshot=1`, `status=1`, `refresh=26`, `change=1`; max event gap `61.139s`; max poll age `23.091s`.
- Public-safety checks: no provider/source-name leak terms, no secret/config/local-path leak terms, no non-JSON stdout lines, and no stderr lines in the through-first-pitch summary.
- Post-first-pitch observation: last market event was about `2026-05-22T18:19:47Z`, with `0` events after scheduled first pitch; treated as expected/neutral for this pre-game odds run, not a stream failure.
- Artifacts: `raw/odds-stream-smoke.summary.json`, `raw/odds-stream-smoke.summary.md`, `raw/odds-stream-smoke.received.ndjson`, `raw/odds-stream-through-first-pitch.summary.json`, `raw/odds-stream-through-first-pitch.summary.md`, `raw/odds-stream-through-first-pitch.received.ndjson`.
- Implementation scope: testing harness only; no product repo code change was required. Current stream evidence does not indicate a v0.3.1 blocker.

## Postgame scoring/lifecycle completion

- Independent final-score cross-check passed:
  - ESPN game summary: Astros 4, Cubs 2.
  - MLB Gameday / MLB Stories: Astros 4, Cubs 2.
- Postgame LINK approval for scoring: `0xbf18073f5f70731d125a1048c7041086b6ee16183aafd10d69b8fb1d13671878`.
- Score request tx: `0xc5dbac41d5beea2bd7b32b698e7cd485a57d1a184a1183623e9a0a63b1c42621`.
- Score request ID: `0xa7495fe7954443325cdb59b1bc21ba9dae10f1b250bf751c6439c74fc5cf5623`.
- Chainlink score callback / `CONTEST_SCORES_SET` tx: `0x72a35646cc3727c096f0309375432a4e17b04ff7267bf22154b15e4412d90783`.
- Contest final state: `scored`, away score `4`, home score `2`, scored at `2026-05-22T21:51:20+00:00`.
- Post-score projection convergence passed: the score request and callback txs succeeded, and the contest projection converged to `scored` with final score Astros `4`, Cubs `2` before postgame assertions.
- Speculations: `0`; positions: `0`; fills: `0`.
- Claim/settlement status: no settlement or claim txs were required because no commitment submit/match was run and no positions existed. `claim-all --dry-run --json` returned an empty entries array.
- Postgame wallet balances observed by doctor: POL `2.363093`, USDC `9`, LINK `0.29`.
- Postgame allowances: PositionModule USDC `2`, TreasuryModule USDC `0.5`, OracleModule LINK `0`.

## Observations

- `npm audit` reports a moderate `ws` advisory via `ethers`; no high/critical findings and no available fix in the current dependency tree. Track as non-blocking unless project policy changes.
- The games list captured immediately after create still showed `contestCreated=false` / `contestId=null`, but the verified contest detail was already available and the later readiness games list showed `contestCreated=true` / `contestId=17`. Treat as transient API/indexer/list projection lag, not a contest-create failure.
- Final doctor after contest creation and postgame scoring has match/submit readiness green, but create-contest readiness red because exact `0.005` LINK OracleModule allowances were consumed by oracle actions. This is an allowance state for future contest creation/scoring, not a balance warning: `ospex-fresh-user` still had `0.29 LINK` afterward, which is healthy; only warn on LINK balance below roughly `0.02 LINK`.
- Optional tiny commitment submit/match was not run in this Stage 0 pass. Therefore, no position settlement/claim path was exercised by this artifact.
- The `games` projection row for `hou-chc-2026-05-22` still had `status=upcoming` after the contest was scored. The contest row is canonical and correctly shows `scored`, but `games.status` appears stale for postgame display/filtering. Treat as follow-up, not an immediate release blocker.
- `claim-all --dry-run --json` with no entries returned top-level `ok=true` and `entries=[]`, but `payload.success=false`. That did not affect this run; it is a small agent-UX/no-op semantics follow-up.

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
- `raw/odds-stream-through-first-pitch.received.ndjson`
- `raw/odds-stream-through-first-pitch.summary.md`
- `raw/odds-stream-through-first-pitch.summary.json`
- `raw/postgame-final-score-source.json`
- `raw/postgame-score-live.sanitized.json`
- `raw/contest-show-17-postgame-final.sanitized.json`
- `raw/postgame-chain-events.sanitized.json`
- `raw/postgame-supabase-state.sanitized.json`
- `raw/postgame-claim-all-dry-run.sanitized.json`
- `raw/postgame-tx-receipts.summary.json`
