# Ospex MVE Phase 1 Block J — late two-game harness stress

Generated: 2026-07-10T19:34:44Z

Verdict: `MVE_PHASE1_BLOCK_J_HARNESS_STRESS_GREEN_WITH_CAVEATS`.

This is a facts-only **operator harness-stress artifact**, not a normal MVE-green or organic-market-activity claim.

## Why this artifact exists

Block J used two late MLB games to prove the repaired harness before the next expanded live block. It replayed the exact Block I classifier failure, exercised safe/fatal/cap/time/alert branches, ran a bounded live quote/fill cycle, found and fixed a real preview-classifier bug, and completed postgame with a clean zero-state.

## Targets

- Contest `36`: Colorado Rockies @ Los Angeles Dodgers — specs `96` moneyline, `97` spread, `98` total.
- Contest `37`: Arizona Diamondbacks @ San Diego Padres — specs `99` moneyline, `100` spread, `101` total.

## Harness evidence

- Block I p1 replay: `GO_WITH_CAVEATS`; 14 would-submit rows; two benign moved-total skips; zero fatal events.
- Normal strict dry run: `GO`; 12 would-submit rows.
- Intentional cap pressure: `GO_WITH_CAVEATS`; 4 would-submit rows; cap refusals remained per-market caveats.
- Synthetic off-allowlist: `STOP`.
- Oversize preview: `REDUCE_SIZE_AND_RETRY`; no tx sent.
- Time-window safety and human-readable alert branches passed.

## Live branch

- 12 live commitment quotes posted.
- 2 controlled live matches completed, one per contest, total taker risk `0.010000 USDC`.
- Oversized previews failed before tx, then safe `0.005000 USDC` retries matched.
- Zero open commitments after shutdown/cancel and no orphan MM process.
- No fatal own-state events.

## Classifier remediation

The first live pass exposed a harness bug: the local classifier treated any `0x...` value—including a commitment hash—as tx evidence. It therefore misclassified a safe preview refusal and skipped the controlled-fill branch. The fix now requires explicit `txHash`/`transactionHash`/`txSent:true` evidence. Self-tests passed after the patch and the live rerun completed both controlled fills.

## Final drift and postgame

- Final read-only drift check: `GO`; 12 would-submit rows; all six target market pairs healthy; no skips/fatals; no tx sent.
- Both contests reached official final and scored state.
- All six target specs completed settlement checks.
- Controlled wallets ended with zero active, pending-settle, and claimable target positions.
- Open commitments ended `36=0`, `37=0`.

## Limitations

All wallets were controlled and risk was deliberately microscopic. This proves harness behavior and remediation, not organic demand, uncontrolled counterparties, or production-scale liquidity.
