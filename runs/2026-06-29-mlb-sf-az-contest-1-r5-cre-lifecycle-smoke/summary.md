# R5 CRE full-lifecycle smoke — SF @ AZ contest 1

Verdict: **R5 CRE full lifecycle smoke GREEN** (`complete_verified_with_caveats`)

This artifact records the first R5/CRE mainnet full-lifecycle proof for Ospex contest `1`, San Francisco Giants @ Arizona Diamondbacks, moneyline speculation `1`.

## Scope

- Not a market-maker autonomous loop test.
- Manual/SDK/CLI controlled lifecycle.
- One contest, one moneyline speculation, one controlled fill.
- Tiny capital only.
- Proves the R5 create/verify/market-update/score/settle/claim path on Polygon mainnet for this controlled lifecycle.

## Target and team identity

| Field | Value |
|---|---|
| Game | San Francisco Giants @ Arizona Diamondbacks |
| gamePk | `825065` |
| Contest / speculation | `1` / `1` |
| Market | moneyline |
| Upper / lower | upper = away = San Francisco Giants; lower = home = Arizona Diamondbacks |
| Live fill odds | San Francisco Giants +116; Arizona Diamondbacks -116 implied taker side |
| Favorite / underdog | Arizona Diamondbacks favorite; San Francisco Giants underdog |
| Final score | San Francisco Giants 4, Arizona Diamondbacks 5 |
| Winning side | home / lower / Arizona Diamondbacks |

## Lifecycle result

| Gate | Result |
|---|---|
| Contest ready | PASS — contest `1` was already verified and market-updated before the controlled fill. |
| Speculation creation | PASS — lazy moneyline speculation `1` was created on first match. |
| Commitment/fill | PASS — one controlled commitment was matched and filled on chain. |
| CRE score | PASS — `contests score 1` sent R5 CRE score request and contest projected `scored`. |
| Settlement | PASS — speculation `1` settled to home/lower/Arizona Diamondbacks. |
| Claim | PASS — `ospex-flow-a` claimed the winning lower/home position. |
| Projection convergence | PASS with caveat — immediate post-claim dry-run briefly showed projection lag, then follow-up status converged to zero active/pending/claimable. |

## Live controlled fill

| Field | Value |
|---|---|
| Maker | `ospex-stage-maker-a` / `0x5316fa54c170d1927f30d1a497ac9e85e3826a9b` |
| Taker | `ospex-flow-a` / `0x16dc5d67d080a5521ef2c79680dbfc2abf724d30` |
| Commitment | `0x6bd7976471b1d23de686a11cdef1dfd950108591516395256dcb952e9a525d33` |
| Fill tx | `0xa7c75bcc5f1c991580e6eb0eb4abccab09df221741ead75ee8ac96fdca50e4af` |
| Fill block | `89372813` |
| Maker side | upper / away / San Francisco Giants |
| Taker side | lower / home / Arizona Diamondbacks |
| Maker risk | 0.250000 USDC |
| Taker risk | 0.290000 USDC |
| Lazy creation fee | 0.500000 USDC total, split 0.250000 / 0.250000 |
| Receipt status | `0x1` |

## Postgame transactions

| Step | Tx |
|---|---|
| Score contest 1 request | `0xeb3c5b51fdc15f879bfc351acab401b4796fa93f43f3b0e8e6d1a31dc0b1da6a` |
| Settle speculation 1 | `0xb759520a6198e4fa3627573ec6ade5c17bf9292a1ed291d14fdb07fd3ea2a7f2` |
| Claim ospex-flow-a lower/home winner | `0x98aa5123daae557c168bfb766572b4241b602b563593c224678205329fd90fa4` |

## Final state

- Contest `1`: `scored`, San Francisco Giants 4, Arizona Diamondbacks 5.
- Speculation `1`: closed (`speculationStatus=1`) in follow-up CLI read.
- Winning wallet `ospex-flow-a`: follow-up `positions.status` shows `active=0`, `pendingSettle=0`, `claimable=0`.
- Follow-up `claim-all --dry-run` for `ospex-flow-a`: zero entries.

## Caveat

Immediate post-claim dry-run briefly showed the winning position as pendingSettle due to projection lag; follow-up CLI positions.status showed active=0, pendingSettle=0, claimable=0.

## Evidence files

Canonical facts are in `evidence.json`. Required raw evidence is under `raw/`, including:

- `raw/postgame_lifecycle_summary.json`
- `raw/live_commit_fill_summary.json`
- `raw/final_contest_1_show.json`
- `raw/final_speculation_1_show.json`
- `raw/score_contest_1.json`
- `raw/settle_speculation_1.json`
- `raw/claim_ospex-flow-a_lower_speculation_1.json`
- `raw/current_positions_status_ospex-flow-a.json`
