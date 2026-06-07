# Ospex owner-state SSE v0.5.4 live soak — PIT-ATL contest 30

## Verdict

**GREEN-candidate lifecycle artifact, postgame complete** — the bounded contest 30/speculation 20 run completed the prior ~62-minute own-state SSE live soak and this one-shot read-only-first continuation completed score, settle, claim, final exposure, cost-accounting, and artifact-publication evidence. Top-level status is `complete_verified_with_caveats` because this proves a single-contest v0.5.4 acceptance/lifecycle run, not broad MVE scale or manufactured outage coverage.

## Target

- Game: Pittsburgh Pirates @ Atlanta Braves
- Final score: Pittsburgh Pirates `2`, Atlanta Braves `3` (`Final` by MLB Stats API schedule/feed and ESPN summary)
- Contest ID: `30`
- Speculation ID: `20` (moneyline; `upper = away/Pittsburgh`, `lower = home/Atlanta`)
- Start: `2026-06-07T17:35:00Z`
- MLB Stats gamePk: `824916`
- ESPN event id: `401815661`

## Wallet roles

- Contest creator / postgame scoring operator: stage-maker-a `0x5316fa54c170d1927f30d1a497ac9e85e3826a9b`
- Live market-maker and postgame winner: stage-maker-b `0x4fa0a5aa3187517efc320aac7d33cd6115cc7482`
- Controlled taker and postgame winner: ospex-fresh-user `0x4ddfeeb90b53f7616135ce9d2b8f317af3c4066d`
- Additional claim-sweep wallet: ospex-flow-a `0x16dc5d67d080a5521ef2c79680dbfc2abf724d30`

No private keys, passphrases, raw RPC URLs, API tokens, raw signed payload material, local signer paths, or long calldata blobs are included in this artifact.

## What was proven

- SDK/CLI and MM release path aligned to `v0.5.4`; captured release tarball SHA256s are in `raw/release-matrix.sanitized.json`. The postgame continuation used `@ospex/cli 0.5.4`, `@ospex/sdk 0.5.4`, and `ospex --version 0.5.4` from release tarballs.
- Contest 30 was created and verified on Polygon mainnet; speculation 20 was created/seeded by a controlled lazy first match.
- The MM ran with owner-state SSE enabled for the single PIT-ATL contest/speculation. API metrics showed own-state subscribers rose to 1 during the run and returned to 0 after shutdown.
- Main live telemetry ran from `2026-06-07T08:06:37Z` to `2026-06-07T09:08:50Z` (~62 minutes, 61 ticks).
- Controlled partial fill tx `0xc69c43c87668c47a6832d6bafd728c4fbecab54f54570ba8f3ba2bfd33d88922` filled maker commitment `0xad05fb35f01a00d753e7207c2bd65c0bc2298fe81a6de7d0e0b7931005f52c21`; telemetry observed it through `source=own-state-stream`.
- Restart/resume emitted a stream-cold-restart and stream-health hold with exposure rather than blank-slate reposting.
- Authoritative on-chain cancel txs cleared post-fill/restart open commitment exposure. Public commitments/orderbook were zero before postgame and remained zero after postgame.
- Postgame verified MLB Stats + ESPN Final PIT `2` / ATL `3`; lower/home/Atlanta won.
- Contest 30 was scored, speculation 20 was settled/closed, and both winning controlled wallets claimed successfully.
- Post-claim dry-run sweeps for stage-maker-a, stage-maker-b, ospex-fresh-user, and ospex-flow-a all returned zero entries.

## Postgame txs

- Score request tx (stage-maker-a): `0xbf0e141cdfeee5bdc6c3fbe4a4b998487a7b16ee38ef3f8b7d35d55b4bb35009`
- Score callback / `CONTEST_SCORES_SET` tx: `0xefb50d47f17593fcc1ccd08b126068b3cd81a7bf56732fd303a69cfc92c8360f`
- Settle speculation 20 tx: `0xc76dae2047636ee97c1e637771d84c549b5ba7bc1ca967754b1ec87552a7a3ca`
- Claim stage-maker-b tx: `0x1859b8ce4a7818d0f97d5063597a5fb4b0f3b9b81ce13c4dac25b50841cd324d` (`46288` wei6 / `0.046288 USDC`)
- Claim ospex-fresh-user tx: `0x6a2387e62e411d4cfd40e75414fc83c9549cc2a7b60dbe715adef37490813b58` (`229000` wei6 / `0.229 USDC`)

## Cost accounting

Receipt/cost accounting uses sanitized cast receipt summaries and token-transfer summaries.

- Total operator-paid POL gas across captured live + postgame txs: `1.116642961820084357` POL.
- Postgame operator-paid POL gas: `0.301357555425182358` POL.
- Postgame score callback/fulfillment gas: `0.14114029822685597` POL-equivalent on-chain gas, recorded as chain evidence only because it was not signed by the operator wallet and is excluded from operator-paid totals.
- LINK evidence: contest creation and postgame scoring each transferred `0.005 LINK` from stage-maker-a to an Ospex oracle module and then to the oracle/link recipient; observed cumulative stage-maker-a LINK net spend is `0.010 LINK`.
- Postgame USDC claim payouts: stage-maker-b `0.046288 USDC`; ospex-fresh-user `0.229 USDC`.

Detailed receipt summaries are in `raw/tx-receipts.summary.json`, `raw/postgame-tx-receipts.summary.json`, and `raw/cost-accounting.json`.

## Caveats

- This is a GREEN-candidate single-contest v0.5.4 acceptance/lifecycle artifact, not proof of broad MVE scale.
- No manufactured API outage/fault injection was performed; natural restart/health-hold behavior was observed.
- One restart on-chain-cancel attempt emitted an `OspexChainError` without tx hash before later successful authoritative cancels; final public exposure and postgame claim state are clean.
- The score callback/fulfillment tx is recorded for chain evidence but was not signed by an operator wallet.

## Raw/sanitized evidence

See `evidence.json`, `scenario-matrix.md`, `scenario-matrix.json`, and the `raw/` directory. Raw runtime files remain preserved in the original private workdir and were not moved/deleted/overwritten.
