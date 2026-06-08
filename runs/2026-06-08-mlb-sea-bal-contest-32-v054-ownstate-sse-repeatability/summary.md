# SEA/BAL v0.5.4 own-state SSE repeatability canary — partial artifact

**Status:** `partial` / GREEN-candidate pending postgame lifecycle. This is not a full GREEN artifact yet.

## Verdict

Phase 1 produced a bounded v0.5.4 own-state SSE repeatability canary for **Seattle Mariners @ Baltimore Orioles** (`sea-bal-2026-06-08`) with contest `32` and moneyline speculation `22`. The run exercised contest/speculation setup, bounded allowance remediation, live MM quote publication, a controlled partial fill, restart/resume own-state behavior, on-chain cleanup, and Phase 2 safety rechecks.

Full GREEN is intentionally withheld until the postgame score/settle/claim lifecycle is completed and this same artifact/PR is updated.

## Target

- Game: Seattle Mariners @ Baltimore Orioles
- Slug: `sea-bal-2026-06-08`
- Start: `2026-06-08T22:35:00Z` / `2026-06-08 17:35 CDT`
- Contest id: `32`
- Speculation id: `22`
- Market: moneyline (`upper=away`, `lower=home`)

## Phase 0 baseline and approval

- Previous artifact baseline: ospex-artifacts PR #16 merged to `main` at `2026-06-08T15:10:43Z` (`9fbbac9c158f7f7dfd08d52b170dbccf10049537`).
- Runtime PR pressure at Phase 0: zero open PRs across market-maker, SDK, core API, and indexer.
- Runtime matrix: CLI `0.5.4`, SDK runtime `0.5.4`, market-maker installed SDK `0.5.4` with the release tarball pin in package/lock files.
- Phase 0 selected SEA/BAL as the earliest viable same-evening MLB target. No existing contest/speculation existed, so Phase 1 required explicit bounded create/seed approval.
- Spend cap: `≤ 5.00 USDC`; maker/creator `stage-maker-a`; controlled taker `ospex-flow-a`.

## Setup

- Contest create tx: `0x28fab025e65d00ce3f23055efcc2cae266fa9f0790702abcf993f141db3d2640`
- Contest id: `32`; final Phase 1 contest status: `verified`
- Seed commitment hash: `0x60515a8bf862119d9cdb2f01b17ac0d5d250d6d551b3a2c50f712fc2dfcebcb0`
- Seed/open-speculation tx: `0x0f1b38bf8a176f75830c7a929a24019767679eea27ccf1896e89b2803e30badf`
- Speculation id: `22`
- Bounded allowance remediation used exact/non-max approvals: `0.35 USDC`, `1.0 USDC`, and `0.25 USDC`.

## Live canary

- MM config summary: `raw/mm-config-summary.sanitized.json`
- `ownState.subscribe`: enabled
- State/telemetry directories: retained privately; local paths are not published.
- Main filled MM quote hash: `0x2e62e694ba0856203cbc0716c9343e084003065ac1db9c69e9891cc34fef4f9d`
- Controlled fill tx: `0x1590ec5398b6ef103fba850ae492bd5c5b8e21a4e4b21d88f670eb553ce8bded`
- Controlled fill economics: taker risk `0.099960 USDC`; maker filled risk `0.083300 USDC`
- Own-state SSE fill ingestion: exactly once (`eventCounts.fill = 1`).

## Restart/resume

- Restart/resume used the same local state directory.
- `stream-cold-restart` observed.
- `stream-health-hold` entered with setup exposure and then cleared.
- No duplicate fill accounting observed.

## Cleanup and safety

- Retained partial cancel tx: `0xb051cfcd450f9b4e0007d265627f80c8a1771faa4981af3737e5dde1fcf27ddd`
- Opposite-side quote cancel tx: `0x9d0c376e24d594ba6d713d514e61c9d0c8ca8dcdd9ece4df383ebf014db38a4e`
- Final visible maker commitments: `0`
- Final orderbook: `[]`
- Final live MM process count: `0`
- Phase 2 recheck confirmed: visible commitments `0`, orderbook count `0`, process count `0`.
- Active filled positions remain for postgame lifecycle handling: `2` positions / `133300 wei6` own risk.

## Budget / cost

- Confirmed write receipts: `8 / 8` parsed
- Total gas: `0.77985881746265763 POL`
- Estimated USDC movement/lock: `1.778760 USDC`, under the `≤ 5.00 USDC` cap
- LINK: not measured in Phase 1

## Caveats

1. Initial `maxOpenCommitments: 2` self-limited before the controlled taker saw a candidate; successful run used bounded `4`.
2. One near-expiry candidate attempt returned rc `1` with timeout/no receipt and did not land.
3. One transient `OwnerPositionStatusForUnknownPosition` occurred before fill materialization; fill accounting then occurred exactly once.
4. Filled positions remain active until postgame score/settle/claim.

## Files

- Evidence: `evidence.json`
- Scenario matrix: `scenario-matrix.md`, `scenario-matrix.json`
- Sanitized raw evidence: `raw/`
