# 2026-07-25 MLB 13-game full-slate live lifecycle

- **Status:** `complete_verified_with_caveats`
- **Network:** Polygon (`chainId 137`)
- **Scope:** contests `53`–`65`; speculations `138`–`176`
- **Terminal verification:** `2026-07-26T04:27:25.332163Z`

## Result

A controlled three-wallet traversal exercised 13 MLB contests and all 39 moneyline, spread, and total markets through the full protocol lifecycle. The run produced 39 controlled fills and 78 positions. After every game reached an official final, all 13 contests were scored exactly, all 39 speculations were settled, and all 39 winning positions were explicitly claimed.

The final readback showed no remaining target positions, open commitments, nonzero allowances, market-maker processes, or slate scheduler jobs. All 91 postgame transactions had successful, unique receipts: 13 scores, 39 settlements, and 39 claims.

## Aggregate counts

| Measure | Result |
|---|---:|
| Contests | 13 |
| Markets / controlled fills | 39 |
| Positions | 78 |
| Exact scores | 13 / 13 |
| Settled speculations | 39 / 39 |
| Claimed winning positions | 39 / 39 |
| Successful postgame receipts | 91 / 91 |
| Remaining lifecycle rows | 0 |
| Open commitments | 0 |
| Nonzero allowance pairs | 0 / 6 |

## Contest results

| Contest | Matchup | Final (away–home) | Moneyline / spread / total speculation | Effective MM overround (bps) |
|---:|---|---:|---|---:|
| `53` | Kansas City Royals @ Detroit Tigers | 3–2 | `138` / `139` / `140` | 300 |
| `54` | Arizona Diamondbacks @ Washington Nationals | 3–5 | `141` / `142` / `143` | 300 |
| `55` | Los Angeles Angels @ San Francisco Giants | 2–9 | `144` / `145` / `146` | 294 |
| `56` | Toronto Blue Jays @ Boston Red Sox | 6–0 | `147` / `148` / `149` | 300 |
| `57` | San Diego Padres @ Miami Marlins | 7–2 | `150` / `151` / `152` | 300 |
| `58` | Cleveland Guardians @ Tampa Bay Rays | 0–3 | `153` / `154` / `155` | 300 |
| `59` | Chicago Cubs @ Pittsburgh Pirates | 11–0 | `156` / `157` / `158` | 300 |
| `60` | Atlanta Braves @ Baltimore Orioles | 2–3 | `159` / `160` / `161` | 300 |
| `61` | Houston Astros @ Chicago White Sox | 4–1 | `162` / `163` / `164` | 300 |
| `62` | Colorado Rockies @ Milwaukee Brewers | 5–8 | `165` / `166` / `167` | 300 |
| `63` | Cincinnati Reds @ St. Louis Cardinals | 0–7 | `168` / `169` / `170` | 242 |
| `64` | Seattle Mariners @ Texas Rangers | 1–7 | `171` / `172` / `173` | 289 |
| `65` | Los Angeles Dodgers @ New York Mets | 4–3 | `174` / `175` / `176` | 300 |

Each contest row, canonical external-ID tuple, fill transaction, settlement transaction, claim transaction, winner side, and payout is recorded in [`raw/targets-and-outcomes.sanitized.json`](raw/targets-and-outcomes.sanitized.json). Official finals were captured from the public MLB schedule feed and joined to canonical Ospex identity by exact teams and scheduled start; the sanitized source record is [`raw/final-score-source.sanitized.json`](raw/final-score-source.sanitized.json).

## Accounting

- Matched principal escrowed and recovered: **68.845923 USDC**.
- Protocol fees: **32.500000 USDC** — 13.000000 for contest creation and 19.500000 for speculation creation.
- Unexplained USDC delta: **0.000000 USDC**.
- Postgame gas: **3.319185868792553755 POL**.
- Whole-session controlled-wallet gas delta: **14.516101480305142886 POL**. This broader number includes safely halted setup attempts, traversal, teardown, scoring, settlement, and claims.

Detailed role-level balances and payouts are in [`raw/accounting.sanitized.json`](raw/accounting.sanitized.json).

## Reviewed pins

- SDK/CLI: `b171a4d3490635413362ae55a90f4f9c853a727c`
- Market maker: `d7982bca406f0e2d290a9e596bd8cb27bd19c998`
- Harness: `5a2ce33fe39cf942e69aa2df41625424f4ef8758`
- Reviewed runner freeze SHA-256: `b2f5640be0c3da5f08c1c5860ae817f20c6a3b09a9a514e3be38f646392bb32b`
- Canonical target snapshot SHA-256: `15920d9f716ba1910ba991ec67bb96c3afeaeda2fb56851bb88c13afa79e8f4e`

Contract addresses, role wallets, package versions, and the reviewed CLI artifact digest are in [`raw/runtime-pins.sanitized.json`](raw/runtime-pins.sanitized.json).

## Market-maker observations

Both reviewed market-maker roles quoted the three supported market types with an approximately 1-USDC target quote size. One controlled fill was taken per market. The intended nominal overround was 300 bps; three per-game configurations required lower feasible values against the observed upstream reference overround:

- LAA @ SF, contest `55`: `294 bps`
- CIN @ STL, contest `63`: `242 bps`
- SEA @ TEX, contest `64`: `289 bps`

Only per-game configuration changed. Reviewed source code remained unchanged.

## Caveats and recovery behavior

1. A custom traversal adapter safely stopped twice on data-shape and lazy-speculation assumptions. It was abandoned; the successful traversal used the reviewed SDK/CLI and market-maker directly.
2. A manual scheduler invocation occupied its caller for about 30 minutes, but the underlying finalizer persisted 13 successful scores before stopping at its bounded gas cap. Receipt-aware continuation completed settlement and claims, and duplicate continuations were removed.
3. Immediate projected reads lagged confirmed settlement receipts for speculations `138` and `139`. No ambiguous write was replayed. Delayed projected reads and direct contract reads confirmed closed state before continuation.
4. One immediate allowance read lagged a successful zero-approval receipt; a read four seconds later returned zero.
5. Two read-only command-shape/parser adaptations failed locally before their corresponding writes and produced no chain effect.

The structured caveat and convergence records are in [`raw/control-plane-caveats.sanitized.json`](raw/control-plane-caveats.sanitized.json) and [`raw/projection-convergence.sanitized.json`](raw/projection-convergence.sanitized.json).

## Evidence boundary

This aggregate proves a controlled, multi-contest lifecycle across the reviewed toolchain. It does **not** prove organic demand, independent outside-agent participation, production-scale concurrency, or sports-model predictive performance. The standardized adopting market-maker scorecard is not attached because its contract is defined for one target contest/speculation per run; this artifact intentionally records the 13-contest aggregate.

Machine-readable source of truth: [`evidence.json`](evidence.json). The public transaction registry contains 167 proof-bearing successful transactions; a fresh Polygon receipt readback confirmed all 167 hashes at their recorded blocks with no missing, failed, or block-mismatched rows. The registry is intentionally non-exhaustive for earlier safely halted setup and nonce-floor housekeeping; whole-session gas still includes those effects.
