# 2026-07-26 MLB 15-game full-slate live lifecycle

- **Status:** `complete_verified_with_caveats`
- **Network:** Polygon (`chainId 137`)
- **Scope:** contests `66`–`80`; speculations `177`–`221`
- **Terminal completion:** `2026-07-27T02:31:26.701533Z`
- **Fresh terminal readback:** `2026-07-27T03:47:41Z`

## Result

A controlled three-wallet traversal exercised 15 MLB contests and all 45 moneyline, spread, and total markets through the full protocol lifecycle. The run produced exactly 45 controlled fills and 90 positions. Every game was seeded before its own first pitch, with a minimum lead-time margin of 50.24 minutes.

After exact official finals were joined by away team, home team, and scheduled UTC start, all 15 contests reached matching on-chain scores, all 45 speculations were settled, and every controlled winner or refundable position was claimed. Forty-four markets had one winner claim; the Kansas City at Detroit total `9.0` pushed and produced two refund claims. The final readback showed no target positions, open commitments, nonzero allowances, market-maker processes, detached game units, or run-owned scheduler jobs.

A fresh Polygon receipt readback confirmed all **202** proof-bearing transaction hashes at their recorded blocks with successful status: 81 setup transactions, 115 postgame lifecycle transactions, and six final allowance revocations.

## Aggregate counts

| Measure | Result |
|---|---:|
| Contests | 15 |
| Markets / controlled fills | 45 |
| Positions | 90 |
| Exact on-chain scores | 15 / 15 |
| Score-request transactions | 24 |
| Settled speculations | 45 / 45 |
| Winner claims | 44 |
| Push-refund claims | 2 |
| Successful proof-bearing receipts | 202 / 202 |
| Remaining lifecycle rows | 0 |
| Open commitments | 0 |
| Nonzero allowances | 0 / 6 |

## Contest results

| Contest | Matchup | Final (away–home) | Moneyline / spread / total speculation | Score requests | Effective MM overround (bps) |
|---:|---|---:|---|---:|---:|
| `66` | Cleveland Guardians @ Tampa Bay Rays | 0–1 | `177` / `178` / `179` | 1 | 300 |
| `67` | Arizona Diamondbacks @ Washington Nationals | 7–10 | `180` / `181` / `182` | 2 | 300 |
| `68` | Atlanta Braves @ Baltimore Orioles | 3–2 | `183` / `184` / `185` | 1 | 242 |
| `69` | Chicago Cubs @ Pittsburgh Pirates | 7–8 | `186` / `187` / `188` | 1 | 300 |
| `70` | Toronto Blue Jays @ Boston Red Sox | 1–6 | `189` / `190` / `191` | 1 | 282 |
| `71` | Kansas City Royals @ Detroit Tigers | 5–4 | `192` / `193` / `194` | 1 | 300 |
| `72` | Los Angeles Dodgers @ New York Mets | 3–8 | `195` / `196` / `197` | 3 | 300 |
| `73` | San Diego Padres @ Miami Marlins | 5–3 | `198` / `199` / `200` | 1 | 300 |
| `74` | Athletics @ Minnesota Twins | 8–11 | `201` / `202` / `203` | 2 | 300 |
| `75` | Colorado Rockies @ Milwaukee Brewers | 2–11 | `204` / `205` / `206` | 1 | 300 |
| `76` | Houston Astros @ Chicago White Sox | 3–12 | `207` / `208` / `209` | 1 | 300 |
| `77` | Cincinnati Reds @ St. Louis Cardinals | 5–3 | `210` / `211` / `212` | 3 | 300 |
| `78` | Seattle Mariners @ Texas Rangers | 6–4 | `213` / `214` / `215` | 3 | 242 |
| `79` | Los Angeles Angels @ San Francisco Giants | 4–3 | `216` / `217` / `218` | 1 | 287 |
| `80` | New York Yankees @ Philadelphia Phillies | 4–11 | `219` / `220` / `221` | 2 | 264 |

Every canonical external-ID tuple, controlled fill, settlement, claim/refund, side outcome, payout, and transaction hash is in [`raw/targets-and-outcomes.sanitized.json`](raw/targets-and-outcomes.sanitized.json). Official finals are in [`raw/final-score-source.sanitized.json`](raw/final-score-source.sanitized.json). No external score-system game identifier was used as Ospex identity.

## Accounting

- Matched principal escrowed and recovered: **396.115944 USDC**.
- Protocol fees: **37.500000 USDC** — 15.000000 for contest creation and 22.500000 for speculation creation.
- Unexplained USDC delta: **0.000000 USDC**.
- Postgame score/settle/claim gas: **4.102398177965428058 POL**.
- Final allowance-teardown gas: **0.095925859930828980 POL**.
- Proof-transaction gas: **14.537102307484081889 POL**.
- Whole-session controlled-wallet gas delta: **16.716396746003994939 POL**. This broader number includes safely recovered setup attempts and market-maker commitment/nonce housekeeping outside the categorical registry.

Detailed role-level principal, payouts, fees, balances, and gas are in [`raw/accounting.sanitized.json`](raw/accounting.sanitized.json).

## Reviewed pins

- SDK/CLI: `b171a4d3490635413362ae55a90f4f9c853a727c`
- Market maker: `d7982bca406f0e2d290a9e596bd8cb27bd19c998`
- Harness: `5a2ce33fe39cf942e69aa2df41625424f4ef8758`
- Reviewed CLI artifact SHA-256: `8037b56dd1c672506265bce640795f4644e7020a36d59387764822b808eb624e`
- Finalizer freeze SHA-256: `3b8822575f654f3ad1a3e459ddd66c4abb43868e417b5af54463e5b2c60aaf41`
- Canonical target snapshot SHA-256: `282e64ce0bd9624a28750e60f78abac358f4c26ea9057e54152923836fab8a6c`

Contract addresses, role wallets, and package versions are in [`raw/runtime-pins.sanitized.json`](raw/runtime-pins.sanitized.json).

## Market-maker observations

Both reviewed maker roles quoted the three supported market types with an approximately 5-USDC target per position. Exactly one controlled fill was taken per market. The intended nominal overround was 300 bps; five per-game configurations required lower feasible values against the observed upstream/reference odds overround:

- Atlanta Braves @ Baltimore Orioles, contest `68`: `242 bps`
- Toronto Blue Jays @ Boston Red Sox, contest `70`: `282 bps`
- Seattle Mariners @ Texas Rangers, contest `78`: `242 bps`
- Los Angeles Angels @ San Francisco Giants, contest `79`: `287 bps`
- New York Yankees @ Philadelphia Phillies, contest `80`: `264 bps`

Only per-game configuration changed. Reviewed source code remained unchanged.

## Caveats and recovery behavior

1. Early game-one attempts encountered response-envelope and projected-read assumptions. Confirmed chain effects were reconciled before retry; no duplicate contest, speculation, or fill was created.
2. Six contests needed multiple bounded score requests before authoritative on-chain scored state converged. The run sent 24 successful requests for 15 exact scores; every retry followed a score-status readback.
3. One total pushed. Both controlled sides were refunded, producing 46 claims for 45 speculations while preserving exact principal conservation.
4. A copied planning digest was corrected to the actual unchanged reviewed CLI artifact before postgame freeze; there was no binary drift.
5. Three asynchronous read-only audit delegations timed out without formal summaries. Useful transcript observations were incorporated and reverified, but this artifact does not represent those timeouts as independent approval.

Structured caveats and convergence evidence are in [`raw/control-plane-caveats.sanitized.json`](raw/control-plane-caveats.sanitized.json) and [`raw/projection-convergence.sanitized.json`](raw/projection-convergence.sanitized.json).

## Evidence boundary

This aggregate proves the recorded controlled lifecycle, exact final-state outcomes, receipt set, accounting conservation, and terminal-zero state. It does **not** prove organic demand, independent outside-agent participation, production-scale concurrency, or sports-model predictive performance. A standardized adopting market-maker scorecard is not attached because its contract targets one contest/speculation per run; this artifact intentionally records a 15-contest aggregate.

Machine-readable source of truth: [`evidence.json`](evidence.json).
