# July 27 MLB five-game bounded run — incomplete safe stop

- **Canonical artifact status:** `partial`
- **Final operational status:** `incomplete_safe_stop`
- **Network:** Polygon mainnet (`chainId=137`)
- **Created / seeded / quarantined:** **5 / 4 / 1**
- **Money-bearing lifecycle:** **12 speculations, 12 fills, 24 positions, 4 exact scores, 12 settlements, 12 claims**

This is deliberately **not** a five-game green result. Contests 81–84 completed the full controlled money-bearing lifecycle and reached terminal state. Contest 85 was created and verified but quarantined before market, fill, or position writes because its immutable `23:00Z` start did not equal the frozen canonical `23:10Z` start.

## Contest outcomes

| Contest | Matchup | Lifecycle | Final (away-home) | Confirmed score requests |
|---:|---|---|---:|---:|
| 81 | Baltimore Orioles at Detroit Tigers | seeded-scored-settled-claimed-terminal | 8-5 | 1 |
| 82 | Arizona Diamondbacks at Pittsburgh Pirates | seeded-scored-settled-claimed-terminal | 2-3 | 2 |
| 83 | Philadelphia Phillies at Miami Marlins | seeded-scored-settled-claimed-terminal | 7-8 | 3 |
| 84 | Toronto Blue Jays at Washington Nationals | seeded-scored-settled-claimed-terminal | 3-2 | 1 |
| 85 | Cleveland Guardians at Cincinnati Reds | created-verified-quarantined-before-markets-or-fills | — | — |

Game 02 required **two** confirmed idempotent score requests before projection convergence. Game 03 required **three**. All four money-bearing contests ultimately matched their exact official final score and closed all three moneyline/spread/total speculations.

## Accounting

- Matched principal escrowed and recovered: **212.309297 USDC**
- Protocol fees reconciled: **11.000000 USDC**
- Unexplained USDC: **0.000000 USDC**
- Recorded operator-controlled proof transactions: **66 / 66 successful receipts**
- Recorded operator-controlled proof-transaction gas: **4.183561557749687312 POL**, within the 100 POL run cap

`raw/accounting.sanitized.json` separates escrow contribution by role from claim-payout recipient by role and reconciles each controlled wallet from its frozen initial balance to terminal balance.

## Terminal state

- Open commitments: **0** across contests 81–85
- Actionable positions: **0**
- Nonzero run-scoped allowances: **0 / 6**
- Market-maker processes: **0**
- Finalizer processes, service units, and per-game finalizer jobs: **0**
- Contest 85 financial state: **0 speculations, 0 fills, 0 positions, 0 open commitments**

Two terminal support cron jobs were intentionally retained only through durable PR readback and are directed to be removed immediately afterward; they are not active per-game finalizers.

## Safe-stop caveat

The exact-minute mismatch is real at the published interfaces: canonical identity is `23:10Z`, while contest 85 is immutable at `23:00Z`. Subsequent verifier-source review showed that UTC-hour normalization can explain why the two values passed oracle agreement. That does not turn this into a five-seeded-game green run: the bounded setup gate required exact canonical minute equality and correctly failed closed before Cleveland–Cincinnati acquired financial state.

## Evidence boundary

This artifact proves the recorded controlled lifecycle, receipt set, exact final-score joins, settlement and claim outcomes, accounting conservation, safe quarantine, and terminal-zero state. It does **not** prove organic demand, independent outside-agent participation, sports-model predictive performance, or production-scale concurrency.

Machine-readable source of truth: [`evidence.json`](evidence.json).
