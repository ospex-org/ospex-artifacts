# Ospex Evidence Artifact: Astros @ Cubs MM Smoke and Post-game Lifecycle

**Artifact ID:** `2026-05-23-mlb-hou-chc-contest-19-mm-smoke`
**Network:** Polygon mainnet
**Contest:** `19`
**Speculation:** `11`
**Market:** MLB moneyline
**Status:** complete / verified with caveats

## Result

Houston Astros defeated Chicago Cubs, **3–0**.

Protocol semantics for this market:

- `upper` / `away` = Houston Astros
- `lower` / `home` = Chicago Cubs
- winning side = `away` / `upper`

External score source:

- MLB Stats API: gamePk `824674`, status `Final`

## What this artifact proves

This run demonstrates a low-value Ospex MM smoke plus complete post-game lifecycle:

1. MM local gates passed: build, typecheck, lint, and `423` tests across `14` files
2. contest created and verified for Houston Astros @ Chicago Cubs
3. moneyline speculation #11 created by a tiny setup match
4. live MM quoted the target contest
5. one controlled low-value taker fill executed against the MM
6. final MM/API/orderbook exposure was clean after shutdown/expiry
7. contest was scored with the real final score
8. speculation was settled with `winSide=away`
9. both winning Astros-side positions were claimed
10. final claim dry-runs were empty for all relevant test wallets
11. post-write projection convergence gates passed for fill, score, settle, and claim after one recorded stale-read retry

## Controlled fills

Seed/setup fill:

- Commitment hash: `0xac4f31286afb19e1a870efa921e61f0fe8a2ba15966034683b09158f2b65f43b`
- Fill tx: `0x7a56548bf11a3b211f0c3d69715e66e9308984d8a2bbb2372735f6a180922e44`
- Maker: `ospex-stage-maker-a` / `0x5316fa54c170D1927F30d1a497aC9E85E3826A9B`
- Taker: `mm-shakeout-flow-a` / `0x1De13292256fddCA9EeA1Ae53a79a83243CFD494`
- Maker side: `upper` / away / Astros
- Taker side: `lower` / home / Cubs
- Maker risk: `0.25 USDC`
- Taker risk: `0.25 USDC`
- Odds tick: `200` (`+100` / decimal `2.00`)

Controlled MM fill:

- Commitment hash: `0xbe49b5a6cfe9df96609268c02305cfabdd4f2321f1f20484e316c42d2acf49d4`
- Fill tx: `0x678b85a6c76f8b7c9ba4932df4f69eb1e7192b1b6c34e381c7bdf5ecc82ec3cb`
- Maker: `mm-shakeout-maker-a` / `0x46aebC238a200be9bf38E4ffdab1E94C4bfD74D2`
- Taker: `mm-shakeout-flow-a` / `0x1De13292256fddCA9EeA1Ae53a79a83243CFD494`
- Maker side: `upper` / away / Astros
- Taker side: `lower` / home / Cubs
- Maker risk filled: `0.179800 USDC`
- Taker risk: `0.249922 USDC`
- Odds tick: `239` (maker decimal `2.39`; taker decimal `1.72`)

Polygonscan:

- Contest create: https://polygonscan.com/tx/0x1d05a9759a3798ef2dbf57788ed51546ed6137b481930c4f303b35b1ccaa4a32
- Contest verify callback: https://polygonscan.com/tx/0xc712ba4e916ade5eb984915cd6636e20b98988938e8ca50bbb5b6f802feb3912
- Seed match/speculation create: https://polygonscan.com/tx/0x7a56548bf11a3b211f0c3d69715e66e9308984d8a2bbb2372735f6a180922e44
- Controlled MM fill: https://polygonscan.com/tx/0x678b85a6c76f8b7c9ba4932df4f69eb1e7192b1b6c34e381c7bdf5ecc82ec3cb
- Score request: https://polygonscan.com/tx/0xc04c62d499c87dfb0df612ea38cf37ba2dbe6fff99da74f43d9043efcaaa76da
- Score callback / scores set: https://polygonscan.com/tx/0x48fe749a1f2b745b101278632855b5f85d87e79bde09e2eed60e02be290a9f22
- Settle: https://polygonscan.com/tx/0xfd324a2fc82ab531f2dba7fae513204da92c8d16fb4ba9fde20ae038d8f32cab
- Seed winner claim: https://polygonscan.com/tx/0xa84a002e57cec4b3dff478d1e5317ff16e22c3bd57ea2bb02ba216b9736995db
- MM winner claim: https://polygonscan.com/tx/0xb046ba21f307aba9fe6487fae167213f19c56b68694e682259e09e6365fff245

## Scoring, settlement, and claims

Score:

- Score request tx: `0xc04c62d499c87dfb0df612ea38cf37ba2dbe6fff99da74f43d9043efcaaa76da`
- Scores-set callback tx: `0x48fe749a1f2b745b101278632855b5f85d87e79bde09e2eed60e02be290a9f22`
- Protocol score: Astros `3`, Cubs `0`

Settlement:

- Tx: `0xfd324a2fc82ab531f2dba7fae513204da92c8d16fb4ba9fde20ae038d8f32cab`
- winSide: `away`

Winner claims:

- `ospex-stage-maker-a`: Astros/upper, claimed `0.5 USDC`, tx `0xa84a002e57cec4b3dff478d1e5317ff16e22c3bd57ea2bb02ba216b9736995db`
- `mm-shakeout-maker-a`: Astros/upper, claimed `0.429722 USDC`, tx `0xb046ba21f307aba9fe6487fae167213f19c56b68694e682259e09e6365fff245`

Position outcomes:

- `ospex-stage-maker-a`: Astros/upper, risk `0.25 USDC`, gross realized profit `0.25 USDC`
- `mm-shakeout-maker-a`: Astros/upper, risk `0.179800 USDC`, gross realized profit `0.249922 USDC`
- `mm-shakeout-flow-a`: Cubs/lower, total risk `0.499922 USDC`, lost, no claim expected

## MM exposure and telemetry

- Live run ID: `2026-05-23T16-37-47-636Z-c2kf9o`
- Live window: `2026-05-23T16:37:47.639Z` → `2026-05-23T16:41:57.995Z`
- Ticks: `8`
- Candidate contests tracked: `1`
- Quote intents: `4`, all quotable
- Submit events: `5`
- Fill events: `1`
- Final commitments list for the MM maker: `0` rows
- Final contest orderbook rows: `0`
- Final Supabase visible-live commitments for contest #19: `0`
- Live MM runner processes after wrap-up: `0`

## Caveats / product or ops debt observed

- Initial setup match using `ospex-stage-maker-b` failed with `CHAIN_ERROR` before any transaction hash/effect. Retry with `mm-shakeout-flow-a` succeeded.
- After a controlled partial fill, the MM attempted an off-chain cancel of the partially-filled commitment and the API rejected it because off-chain cancel is not allowed once a match exists. Remaining maker capacity expired naturally; final orderbook/API exposure was clean. Subsequent MM code changes may address this edge case; this artifact records what happened in this run.
- MM local status still classified two shutdown-cancelled quotes as `softCancelled` after natural expiry, while public/API visibility was clean.
- The first MM winner `claim-all` attempt used a stale `pendingSettle` projection after another wallet had already settled speculation #11. A refresh exposed the MM position as claimable, and retry claim-only succeeded.
- Private operator files, local run paths, RPC URLs, credential material, password files, keystore paths, raw signatures, and raw telemetry transcripts are intentionally excluded.

## Files

- `evidence.json` — sanitized machine-readable artifact
- `raw/indexer-snapshot.sanitized.json` — selected Supabase/API projection rows with signatures omitted
- `raw/tx-receipts.summary.json` — compact Polygon receipt summaries
- `raw/final-score-source.json` — MLB Stats API final-score observation
- `raw/mm-telemetry-summary.sanitized.json` — MM telemetry rollup without local paths/raw telemetry
- `raw/mm-final-status.sanitized.json` — MM final status rollup without local paths
- `raw/mm-controlled-fill.sanitized.json` — selected CLI fill evidence with raw signature omitted
- `raw/mm-filled-commitment.sanitized.json` — final commitment read with raw signature omitted
- `raw/mm-maker-commitments-final.sanitized.json` — final MM commitments-list read
- `raw/claim-lifecycle.sanitized.json` — post-score claim/settle/final dry-run evidence
