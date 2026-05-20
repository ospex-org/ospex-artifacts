# Ospex Evidence Artifact: Braves @ Marlins MM Shakeout

**Artifact ID:** `2026-05-19-mlb-atl-mia-contest-13`  
**Network:** Polygon mainnet  
**Contest:** `13`  
**Speculation:** `6`  
**Market:** MLB moneyline  
**Status:** complete / verified

## Result

Atlanta Braves defeated Miami Marlins, **8–4**.

Protocol semantics for this market:

- `upper` / `away` = Atlanta Braves
- `lower` / `home` = Miami Marlins
- winning side = `away`

External score sources:

- MLB Stats API: gamePk `823865`, status `Final`
- ESPN: https://www.espn.com/mlb/game/_/gameId/401815404/braves-marlins

## What this artifact proves

This run demonstrates a complete low-value Ospex market-maker lifecycle:

1. contest and moneyline speculation existed on Polygon mainnet
2. market-maker posted a live EIP-712 commitment
3. controlled taker matched exactly one tiny quote
4. quote exposure was pulled before first pitch
5. contest was scored with the real final score
6. speculation settled
7. winning positions claimed
8. post-claim sweeps showed no remaining claimable entries

## Controlled MM fill

- Commitment hash: `0x1ea627807fd38e6fdea74974ab1fb0ed6cf14bc1ae52fd385ce53fa43b1107a3`
- Fill tx: `0x4af9a8c39e1c125775db50ea08665ad9a5d8781299b820eee32e5a964f2f1ff9`
- Maker: `mm-shakeout-maker-a` / `0x46aebc238a200be9bf38e4ffdab1e94c4bfd74d2`
- Taker: `mm-shakeout-flow-a` / `0x1de13292256fddca9eea1ae53a79a83243cfd494`
- Maker side: `upper` / away / Braves
- Taker side: `lower` / home / Marlins
- Maker risk: `0.25 USDC`
- Taker risk: `0.195 USDC`
- Odds tick: `178`

Polygonscan:

- https://polygonscan.com/tx/0x4af9a8c39e1c125775db50ea08665ad9a5d8781299b820eee32e5a964f2f1ff9

## Quote cutoff before first pitch

First pitch was `2026-05-19T20:10:00Z`.

Observed MM behavior:

- Last submit: `2026-05-19T20:02:03Z`
- Last replace: `2026-05-19T20:06:42Z`
- Soft-cancel: `2026-05-19T20:08:14Z`
- Final local expire: `2026-05-19T20:08:44Z`
- After first pitch: candidate skips only; no new submits/replaces
- Visible/live commitments after first pitch: `0`

## Scoring, settlement, and claims

Score request:

- Tx: `0x3c57443af490685fa6cf30c08dbf75bd548afbf89dd65b46ed00dadbf9dfbe37`
- Block: `87139585`
- Gas: `0.143330755517 POL`

MM automated settlement:

- Tx: `0x3a120a1ccdbe16dc2d7421d997d54b166f445a03bed093c0752575c7ea3b25b5`
- Block: `87139593`
- Gas: `0.026692616984 POL`

MM automated claim:

- Tx: `0x61d83f967ca0fd9052a3290c7d7aa7350259ebe9ec013579be233abfd42e13b8`
- Payout: `0.445 USDC`
- Gas: `0.023004942054 POL`

Stage seed winner claim:

- Tx: `0x516a806690665d6745a2c962d1964ebb870ecfe45a6ef56ed4e75c9237ae26b8`
- Payout: `0.087 USDC`
- Gas: `0.022030177879 POL`

## Position outcomes

- Stage seed wallet: Braves/upper, risk `0.05 USDC`, profit `0.037 USDC`, claimed `0.087 USDC`
- MM maker wallet: Braves/upper, risk `0.25 USDC`, profit `0.195 USDC`, claimed `0.445 USDC`
- Flow wallet: Marlins/lower, total risk `0.232 USDC`, lost, no claim expected

## Caveats / product debt observed

- Expired commitment rows can remain `status=open` in Supabase; live-active orderbook semantics must include expiry/non-cancelled/fillable checks.
- Source `games.status` was observed stale after protocol scoring; canonical protocol/indexer contest state was correct.
- Pre-start `UnexpectedFillStatus` telemetry matched known expiry/open classification noise; there were no phantom fills.
- MM local realized PnL accounting did not reflect the claim even though indexed protocol state and wallet balances did.

## Files

- `evidence.json` — sanitized machine-readable artifact
- `raw/indexer-snapshot.sanitized.json` — selected Supabase/indexer rows with signatures omitted
- `raw/tx-receipts.summary.json` — compact Polygon receipt summaries
- `raw/final-score-source.json` — MLB Stats API final-score observation

Private operator files, RPC URLs, wallet password files, signatures, and raw telemetry logs are intentionally excluded.
