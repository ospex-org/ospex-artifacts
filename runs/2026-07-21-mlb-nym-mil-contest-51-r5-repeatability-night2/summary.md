# Night 2 R5 repeatability — contest 51

## Verdict

**FULL_GREEN / complete_verified_with_caveats** — New York Mets @ Milwaukee Brewers contest 51 completed the bounded R5 lifecycle: three markets seeded, a controlled live-MM fill landed, the exact official final matched scored state, all target speculations settled, winning positions claimed, allowances revoked, and direct final-zero/accounting readback passed. The composite-doctor readback defect is retained as a run-adapter caveat.

## Target

- New York Mets (away) @ Milwaukee Brewers (home)
- Polygon mainnet, deployment round R5, contest 51
- Speculations: 135, 136, 137
- Official final: New York Mets 4–0 Milwaukee Brewers

## Completion

- All three target speculations settled and every winning position claimed.
- Direct reads proved zero target positions, claim plans, open commitments, allowances, and maker processes.
- No completion-pass revoke or other protocol write was required.
- USDC stakes, payouts, net P&L, protocol fees, and receipt-level POL gas reconciled exactly.

## Caveat

The run-local composite doctor correctly found zero allowances after revocation but the ladder converted its non-ready exit into `spentPOL=999` and mislabeled the stop as official-final. The raw failure is preserved privately; the published diagnosis is sanitized under `raw/`. The fix-forward is ospex-harness PR #12.
