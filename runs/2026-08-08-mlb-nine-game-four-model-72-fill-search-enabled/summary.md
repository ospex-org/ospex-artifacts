# Saturday 8/8 MLB — nine games, four models, 72 fills, search enabled

## Result

**Status:** `complete_verified_with_caveats`
**Run label:** `SMOKE_V0_NOT_A_COHORT`
**Network:** Polygon mainnet (`chainId=137`)
**Scope:** contests `91–99`, 18 moneyline/total speculations, four model arms, `72/72` controlled fills
**Terminal:** `TERMINAL_ZERO` at `2026-08-09T05:04:42.156776Z`

All 72 frozen fills completed. All nine exact-team/time official finals matched the on-chain scores, all 18 speculations settled, every claimable position was claimed, and terminal readback found zero open commitments, pending settlements, claimables, nonterminal positions, or relevant writer processes.

This is controlled MVE/lifecycle evidence, **not** a canonical cohort or model leaderboard. No CLV scoring is included in this publication.

## Games

| Contest | Game (away at home) | Start UTC | Final (away–home) |
|---:|---|---|---:|
| 91 | Minnesota Twins at Milwaukee Brewers | 2026-08-08 23:10 | 3–4 |
| 92 | Chicago Cubs at Kansas City Royals | 2026-08-08 23:10 | 3–6 |
| 93 | Baltimore Orioles at Texas Rangers | 2026-08-08 23:15 | 1–5 |
| 94 | Cleveland Guardians at Chicago White Sox | 2026-08-08 23:15 | 3–6 |
| 95 | Colorado Rockies at St. Louis Cardinals | 2026-08-08 23:15 | 8–6 |
| 96 | Detroit Tigers at San Francisco Giants | 2026-08-08 23:15 | 8–0 |
| 97 | Houston Astros at San Diego Padres | 2026-08-08 23:15 | 2–3 |
| 98 | Los Angeles Dodgers at Arizona Diamondbacks | 2026-08-09 00:10 | 2–1 |
| 99 | Tampa Bay Rays at Seattle Mariners | 2026-08-09 01:50 | 3–2 |

## Execution and lifecycle

- Setup: 9 contests + 18 speculations (`27/27` successful transactions). Speculation 260 mined before an interrupted local checkpoint; its transaction was recovered by a bounded nonce/block scan and the durable rerun reconciled it without resending.
- Controlled execution: `72/72` fills, 72 unique fill IDs, 72 unique fill transaction hashes, and zero failed final fill rows.
- Exact recovery: 46 fills completed in parent runs; 26 exact missing-fill recoveries completed (window 1: 4, window 2: 12, window 3: 10). No designated decision was regenerated and no completed fill was resent.
- One window-3 quote/cancel redaction race failed before send; its single recovery transaction succeeded.
- Postgame: 9 score requests, 9 independently recovered `ContestScoresSet` callbacks, 18 settlements, and 71 claim transactions. There were 53 explicit no-position/already-claimed observations with no transaction.
- Receipt reconciliation: **211/211 unique published transaction hashes succeeded**; total gas was `15.885028894302939418 POL`.
- Transaction-set boundary: the 211 published transactions are scope-exact to permissions, setup, fills, scoring, settlement, claims, and cleanup. They are not all run-window wallet activity: 65 routine maker order-management transactions (`raiseMinNonce`: 48; `cancelCommitment`: 17) are excluded, and no lifecycle transaction is excluded.
- Permissions: Flow received exact 1 USDC PositionModule and 18 USDC TreasuryModule allowances; Maker received exact 250 USDC PositionModule allowance. Flow PositionModule and Maker PositionModule were revoked to zero. Flow TreasuryModule reached zero through the exact 18 USDC creation-fee spend; both roles had immediate zero readbacks for both modules. Model TreasuryModule allowances were zero; the documented model PositionModule ceiling remained a standing shared-MVE exception.

See [`raw/fills-and-receipts.sanitized.json`](raw/fills-and-receipts.sanitized.json), [`raw/postgame-lifecycle.sanitized.json`](raw/postgame-lifecycle.sanitized.json), [`raw/terminal-zero.sanitized.json`](raw/terminal-zero.sanitized.json), and [`raw/deviations.sanitized.json`](raw/deviations.sanitized.json).

## Search and spend boundary

One retained whole-window attempt stopped before protocol writes after a transient Anthropic HTTP 529. Its measured spend is included. The complete replacement and windows 2–3 were designated before execution.

| Arm | Designated calls | Designated search evidence | Designated spend | Failed-attempt spend |
|---|---:|---|---:|---:|
| `anthropic-claude-fable-5` | 9 | 27 known / 0 unknown | $7.123020 | $1.086930 |
| `google-gemini-3.1-pro-preview` | 9 | 1 known / 8 unknown | $1.035584 | $0.352310 |
| `openai-gpt-5.6-sol` | 9 | 13 known / 3 unknown | $3.284424 | $1.016503 |
| `xai-grok-4.5` | 9 | 142 known / 0 unknown | $6.665700 | $2.125292 |

Designated spend was `$18.108728`; the retained failed attempt added `$4.581035`, for `$22.689763` total under the `$50.000000` stop threshold. Designated calls have `183` known billable searches and `11` unknown/unproven search records. The failed attempt has `56` known searches and `3` unknown records. Unknown never means zero or “did not search.”

Per-arm spend is **not cost-per-pick comparable**: equal call counts do not make provider workloads comparable, and search auditability/token mix differ across arms.

Complete provider envelopes were not retained, so missing search evidence cannot be recovered offline; this remains tracked in [ospex-benchmark issue #92](https://github.com/ospex-org/ospex-benchmark/issues/92). Captured queries, result references, answer text, and provider response bodies are not published.

## Trading economics

Gas and off-chain provider spend are excluded from USDC trading PnL and reported separately.

| Participant | Principal | Terminal payout | Net trading PnL | Claim txs |
|---|---:|---:|---:|---:|
| `flow` | $0.360000 | $0.360000 | **$0.000000** | 18 |
| `anthropic-claude-fable-5` | $17.998971 | $18.904830 | **$0.905859** | 10 |
| `google-gemini-3.1-pro-preview` | $17.998993 | $21.514884 | **$3.515891** | 11 |
| `openai-gpt-5.6-sol` | $17.998940 | $14.457305 | **$-3.541635** | 8 |
| `xai-grok-4.5` | $17.998950 | $16.011430 | **$-1.987520** | 8 |
| `maker` | $66.776500 | $67.883905 | **$1.107405** | 16 |

The `fixed-moneyline-total` execution policy filled every supplied moneyline/total forecast, including `10/72` rows with `wouldAbstain=true` (`openai-gpt-5.6-sol`: 5; `xai-grok-4.5`: 5; other arms: 0). All 10 fall in the two negative-PnL rows above, so this is policy-conditioned realized PnL, not a model ranking.

All 72 fills executed at taker-facing decimal odds better than the frozen reference (mean improvement `0.028285`), adding `$2.036369` of maker risk versus applying the frozen references to the same taker principal. That is execution price improvement, not model performance.

Model plus maker trading PnL reconciles to zero. Flow setup-position trading net is zero; Flow separately paid 9 USDC in contest-creation fees and 9 USDC in speculation-creation fees, for `-$18.000000` before gas.

Nine realized games do not support model ranking, and this artifact contains no CLV appendix.

## Evidence boundary

Published: exact game identities, frozen reference odds, executed structured decision fields, fill amounts, source-copied transaction hashes, successful receipt blocks/timestamps/gas, official finals, score callbacks, settlement/claim evidence, terminal-zero readback, trading economics, sanitized search/spend aggregates, source commits/hashes, and recovery deviations.

Not published: credentials, local paths, wallet addresses/key material, private provider payloads or envelopes, model rationales/answer text, captured search queries/results, named upstream odds providers, private database rows, or controller logs.

Validate locally with:

```bash
python scripts/generate-indexes.py --check
python scripts/validate-artifacts.py
```
