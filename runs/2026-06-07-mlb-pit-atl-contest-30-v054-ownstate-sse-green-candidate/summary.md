# Ospex owner-state SSE v0.5.4 live soak — PIT-ATL contest 30

## Verdict

**GREEN-candidate live artifact, postgame pending** — the prior live run already completed a ~62-minute own-state SSE soak for contest 30/speculation 20 with a controlled partial fill, restart/resume, authoritative on-chain cancels, final public/orderbook exposure zero, and final own-state subscribers zero. This artifact revision is intentionally marked top-level `status: partial` until the scheduled postgame score/settle/claim continuation completes.

## Target

- Game: Pittsburgh Pirates @ Atlanta Braves
- Contest ID: `30`
- Speculation ID: `20` (moneyline; `upper = away/Pittsburgh`, `lower = home/Atlanta`)
- Start: `2026-06-07T17:35:00Z`
- MLB Stats gamePk: `824916`
- ESPN event id: `401815661`

## Wallet roles

- Contest creator / postgame scoring operator: stage-maker-a `0x5316fa54c170d1927f30d1a497ac9e85e3826a9b`
- Live market-maker: stage-maker-b `0x4fa0a5aa3187517efc320aac7d33cd6115cc7482`
- Controlled taker used for partial fill: ospex-fresh-user `0x4ddfeeb90b53f7616135ce9d2b8f317af3c4066d`
- Additional claim-sweep wallet: ospex-flow-a `0x16dc5d67d080a5521ef2c79680dbfc2abf724d30`

No private keys, passphrases, raw RPC URLs, API tokens, raw signed payload material, local signer paths, or long calldata blobs are included in this artifact.

## What was proven

- SDK/CLI and MM release path aligned to `v0.5.4`; captured release tarball SHA256s are in `raw/release-matrix.sanitized.json`.
- Contest 30 was created and verified on Polygon mainnet; speculation 20 was created/seeded by a controlled lazy first match.
- The MM ran with owner-state SSE enabled for the single PIT-ATL contest/speculation. API metrics showed own-state subscribers rose to 1 during the run and returned to 0 after shutdown.
- Main live telemetry ran from `2026-06-07T08:06:37Z` to `2026-06-07T09:08:50Z` (~62 minutes, 61 ticks).
- Controlled partial fill tx `0xc69c43c87668c47a6832d6bafd728c4fbecab54f54570ba8f3ba2bfd33d88922` filled maker commitment `0xad05fb35f01a00d753e7207c2bd65c0bc2298fe81a6de7d0e0b7931005f52c21`; telemetry observed it through `source=own-state-stream`.
- Restart/resume emitted a stream-cold-restart and stream-health hold with exposure rather than blank-slate reposting.
- Authoritative on-chain cancel txs cleared post-fill/restart open commitment exposure. Final commitment lists for contest 30 and speculation 20 returned zero rows; final contest orderbook rows were zero; final metrics own-state subscribers were zero.

## Cost accounting

Receipt/cost accounting used a robust parser for cast receipt JSON fields (hex strings, decimal strings, integers, nulls, and formatted values). It parsed 9/9 captured receipt lines without the previous `decimal.InvalidOperation` / `ConversionSyntax` failure.

- Total POL gas across captured txs: `0.815285406394901999` POL.
- LINK evidence: preflight stage-maker-a oracle allowance was `0.19 LINK`; contest creation receipt shows `0.005 LINK` transferred from stage-maker-a to ContestModule and forwarded to the oracle/link recipient. No separate LINK approval tx was present in captured receipts.
- USDC movements from receipts:
  - Contest creation: stage-maker-a `1.000000 USDC` to protocol fee recipient.
  - Seed speculation creation fee: stage-maker-a `0.250000 USDC`, ospex-fresh-user `0.250000 USDC` to protocol fee recipient.
  - Seed match risk escrow: stage-maker-a `0.100000 USDC`, ospex-fresh-user `0.129000 USDC` to PositionModule.
  - Controlled partial fill risk escrow: stage-maker-b `0.026300 USDC`, ospex-fresh-user `0.019988 USDC` to PositionModule.
  - On-chain cancels: no USDC transfer/approval events in the three cancel receipts.

Detailed receipt summaries are in `raw/tx-receipts.summary.json` and `raw/cost-accounting.json`.

## Postgame continuation

A one-shot read-only-first postgame job is scheduled for **2026-06-07T21:45:00Z** (**2026-06-07 16:45 CDT (America/Chicago)**), cron job `039b18a3eae6`. It must independently verify the final score with MLB Stats API and ESPN, use only v0.5.4 release CLI/SDK, score contest 30 with the contest creator/operator wallet, settle speculation 20, claim winnings for winning controlled wallets, dry-run claim sweeps for all relevant wallets, and update this same artifact branch/PR.

## Caveats

- Postgame score/settle/claim is pending until the game is final; this artifact is therefore `status: partial` despite the live soak being GREEN-candidate.
- The final MM state contains one legitimate filled active position (`26300` wei6 maker risk) awaiting postgame. That is not public/orderbook quote exposure.
- One restart on-chain-cancel attempt emitted an `OspexChainError` without tx hash before later successful authoritative cancels; final public exposure was zero.
- No manufactured API outage/fault injection was performed; natural restart/health-hold behavior was observed.

## Raw/sanitized evidence

See `evidence.json`, `scenario-matrix.md`, `scenario-matrix.json`, and the `raw/` directory. Raw runtime files remain preserved in the original workdir and were not moved/deleted/overwritten.
