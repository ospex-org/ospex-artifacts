# R5 CRE lifecycle repeat — CWS @ BAL contest 2

Verdict: **R5 CRE lifecycle repeat GREEN with caveats** (`complete_verified_with_caveats`)

This artifact records an R5/CRE mainnet repeatability proof for Ospex contest `2`, Chicago White Sox @ Baltimore Orioles, moneyline speculation `2`.

## Scope

- Not a market-maker autonomous loop test.
- Manual/SDK/CLI controlled lifecycle.
- One contest, one moneyline speculation, one controlled fill.
- Tiny capital only.
- Proves the R5 create/verify/market-update/score/settle/claim path on Polygon mainnet for this controlled lifecycle.

## Target and team identity

| Field | Value |
|---|---|
| Game | Chicago White Sox @ Baltimore Orioles |
| gamePk | `824819` |
| Contest / speculation | `2` / `2` |
| Market | moneyline |
| Upper / lower | upper = away = Chicago White Sox; lower = home = Baltimore Orioles |
| Live fill odds | Chicago White Sox +121; Baltimore Orioles -139 reference moneyline |
| Favorite / underdog | Baltimore Orioles favorite; Chicago White Sox underdog |
| Final score | Chicago White Sox 9, Baltimore Orioles 3 |
| Winning side | away / upper / Chicago White Sox |

## Lifecycle result

| Gate | Result |
|---|---|
| Contest create | PASS — contest `2` created on Polygon mainnet. |
| CRE verification | PASS — contest `2` verified through R5 CRE. |
| Market update | PASS — exactly one market update requested; moneyline odds became visible. |
| Speculation creation | PASS — lazy moneyline speculation `2` was created on first match. |
| Commitment/fill | PASS — one controlled commitment was matched and filled on chain. |
| CRE score | PASS with caveat — first confirmed score request did not callback before retry; bounded second request scored the contest. |
| Settlement | PASS — speculation `2` closed to away/upper/Chicago White Sox. |
| Claim | PASS — `ospex-stage-maker-a` claimed the winning upper/away position. |
| Projection convergence | PASS with caveat — speculation read exposed `speculationStatus=1` while `settledAt`/`winSide` projection fields were null; final positions and orderbook converged clean. |

## Live controlled fill

| Field | Value |
|---|---|
| Creator / score operator | `ospex-stage-maker-b` / `0x4fa0a5aa3187517efc320aac7d33cd6115cc7482` |
| Maker | `ospex-stage-maker-a` / `0x5316fa54c170d1927f30d1a497ac9e85e3826a9b` |
| Taker | `ospex-flow-a` / `0x16dc5d67d080a5521ef2c79680dbfc2abf724d30` |
| Commitment | `0xd9715b7e7300ad559014e5ca92878fe7ff28dfbe83d41d9dcf12e3987372f088` |
| Create contest tx | `0x8d779b0c8c13ab65aa9ce65ee4f5756285fff91eca267e27173253d6365391b9` |
| Market update tx | `0xe5b43015b8c33feb16011a606b4103cf559100fe3366710d32f515ecc30c0f39` |
| Fill tx | `0xd8fc81fa228d4b2b6fbef56e9546813ff210eaa68d6e275afc851c33e0834eda` |
| Fill block | `89400929` |
| Maker side | upper / away / Chicago White Sox |
| Taker side | lower / home / Baltimore Orioles |
| Maker risk | 0.250000 USDC |
| Taker risk | 0.302500 USDC |
| Lazy creation fee | 0.500000 USDC total, split 0.250000 / 0.250000 |
| Receipt status | `0x1` |

## Postgame transactions

| Step | Tx |
|---|---|
| Score contest 2 request attempt 1 | `0xc3dd38ac986fa7ac4ec39add8cfc45e0e56ea984adb24ce1654bac5d43304945` |
| Score contest 2 request retry 2 | `0x979eb76ba0a39685e6cd6bede56ff9f0ffc6f5d90975a04003ca2b25797ea37e` |
| Settle speculation 2 | `0x6fd93bacfc0f50b40efedc88d8fc412b89de1fc9ff638177a9872c5f30ca262d` |
| Claim ospex-stage-maker-a upper/away winner | `0xe713b2732b0e35f72afba4ea51c59272a17faf6d0bcb983a8ed5359edbb3b43d` |

## Final state

- Contest `2`: `scored`, Chicago White Sox 9, Baltimore Orioles 3.
- Speculation `2`: closed (`speculationStatus=1`) in follow-up CLI read.
- Winning wallet `ospex-stage-maker-a`: follow-up `positions.status` shows `active=0`, `pendingSettle=0`, `claimable=0`.
- Taker wallet `ospex-flow-a`: follow-up `positions.status` shows `active=0`, `pendingSettle=0`, `claimable=0`.
- Final orderbook/commitment check: contest open commitments `0`, speculation open commitments `0`, controlled-maker open commitments `0`.

## Caveats

1. The first confirmed score-request transaction did not produce a callback before retry; this was handled by a bounded retry after official-final provider convergence.
2. The speculation API read exposed `speculationStatus=1` while `settledAt`/`winSide` projection fields were null; final positions/orderbook convergence verified the lifecycle result.

## Evidence files

Canonical facts are in `evidence.json`. Required raw evidence is under `raw/`, including:

- `raw/live_commit_fill_summary.json`
- `raw/postgame_lifecycle_summary.json`
- `raw/final_contest_2_show.json`
- `raw/final_speculation_2_show.json`
- `raw/score_contest_2_attempt_1.json`
- `raw/score_contest_2_retry_2.json`
- `raw/settle_speculation_2.json`
- `raw/claim_ospex-stage-maker-a_upper_speculation_2.json`
- `raw/current_positions_status_ospex-stage-maker-a.json`
- `raw/tx_receipts_summary.json`
