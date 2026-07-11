# Ospex MVE Phase 1 Block K — six-game, two-maker artifact

Generated: 2026-07-11T07:13:38Z

Status: `complete_verified_with_caveats`  
Verdict: `AMBER_LIVE_CAVEATS_FINAL_ZERO_CLEAN`

## Scope

- Six verified MLB contests, contests 38–43.
- Three speculations per contest, speculation IDs 102–119.
- Two independent maker wallets/processes with 10 USDC global caps.
- Four distinct model IDs mapped to four signer wallets; same-provider route only.
- Closing-line, score, settle, claim, and final-zero verification included.

## Gates

- SDK: 54 test files / 883 tests passed at `v0.10.0`.
- Market maker: 28 test files / 1,084 tests passed at `14db79b`.
- Simultaneous two-maker dry manifests passed for all capacity-safe subruns.
- All live subruns safe: `False`.
- Two-maker competition achieved in every subrun: `False`.
- Postgame/final zero clean: `True`.
- Postgame receipts: `51/51` successful (6 score, 18 settle, 23 claim, 4 allowance-revoke transactions).

## Economic boundary

- Protocol creation fees: 15 USDC.
- Setup micro-collateral: 0.035670 USDC.
- Planned scope including setup: 39.035670 USDC under the 40 USDC ceiling.

## Findings

- Protocol/code: no blocker is claimed unless recorded in the live summaries.
- Docs/footgun: stale local module addresses were corrected; stale allowances ended at zero.
- Harness/operator: the measured SSE cap required target-scoped subruns rather than an unsafe all-nine-pair launch.
- Agent/frontend integration: four model IDs/signers are evidenced, but the configured route was one provider and no frontend registry adapter is claimed.

## Final rule

The artifact uses a GREEN-derived label only when all live, postgame, and final-zero gates support it. Null CLV for moved spread/total lines is retained as null rather than imputed.
