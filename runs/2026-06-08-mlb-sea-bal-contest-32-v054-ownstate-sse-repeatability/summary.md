# SEA/BAL v0.5.4 own-state SSE repeatability canary — complete verified with caveats

**Status:** `complete_verified_with_caveats` / GREEN repeatability canary with documented Phase 1 operational caveats.

## Verdict

The SEA/BAL v0.5.4 own-state SSE repeatability canary is complete through postgame lifecycle. Phase 1 proved the bounded live MM + own-state SSE restart/resume path; Phase 3 verified official finality, scored contest `32`, settled moneyline speculation `22`, claimed the two winning controlled wallets only, and rechecked empty final claim sweeps plus zero public/orderbook exposure.

## Official final score gate

- MLB Stats API: `Final`, Seattle Mariners `6`, Baltimore Orioles `3`.
- ESPN API: `Final`, Seattle Mariners `6`, Baltimore Orioles `3`.
- Agreement: `true`; moneyline win side `upper` / away / Seattle Mariners.
- Evidence: `raw/final-score-source.json`.

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

## Cleanup and Phase 2 safety

- Retained partial cancel tx: `0xb051cfcd450f9b4e0007d265627f80c8a1771faa4981af3737e5dde1fcf27ddd`
- Opposite-side quote cancel tx: `0x9d0c376e24d594ba6d713d514e61c9d0c8ca8dcdd9ece4df383ebf014db38a4e`
- Final visible maker commitments after Phase 1/2: `0`
- Final orderbook after Phase 1/2: `[]`
- Final live MM process count after Phase 1/2: `0`

## Phase 3 postgame lifecycle

- Score contest tx: `0x4dda5dadd3cdab71b6220028cb11122de8e66cdac5d6fa1feb6f5aa246c4329d` (signer guard matched `stage-maker-a` / `0x5316fa54c170d1927f30d1a497ac9e85e3826a9b`)
- Settle speculation tx: `0x78e3bc0c954a6b8cdda8354e6a77ebe5866c06eafe57521f2209a4b32f7b54a2` (signer guard matched `stage-maker-a` / `0x5316fa54c170d1927f30d1a497ac9e85e3826a9b`)
- Claim `stage-maker-a` winning upper position: `0x23379e64b9416358ff1d7e29a7e0680a9afe7e79e18cdfb91738f3a308df4719`; claimed `95500 wei6` / `0.095500 USDC`.
- Claim `ospex-flow-a` winning upper position: `0xe196e6934de5389d4cd044b9e85bb6b3a17c5f429dcc89144f984c308bbd9601`; claimed `183260 wei6` / `0.183260 USDC`.
- Final `claim-all --dry-run` sweeps: both controlled wallets returned zero entries / zero payout.
- Final protocol state: contest `scored`, speculation `closed`, win side `away`, orderbook `[]`, visible live maker commitments `0`, live MM process count `0`.
- Evidence: `raw/cli-postgame.sanitized.json`, `raw/final-contest-show.sanitized.json`, `raw/final-positions-claims.sanitized.json`, `raw/final-safety-state.sanitized.json`, `raw/tx-receipts.summary.json`.

## Budget / cost

- Phase 1 confirmed write receipts: `8 / 8` parsed
- Phase 1 total gas: `0.77985881746265763 POL`
- Phase 3 postgame receipts: `4 / 4` parsed; postgame gas `0.301535670981113934 POL`
- Total gas including postgame: `1.081394488443771564 POL`
- Estimated Phase 1 USDC movement/lock: `1.778760 USDC`, under the `≤ 5.00 USDC` cap
- LINK/operator subscription spend: not measured in local receipt gas; score transaction and callback projection succeeded.

## Caveats

1. Initial `maxOpenCommitments: 2` self-limited before the controlled taker saw a candidate; successful run used bounded `4`.
2. One near-expiry candidate attempt returned rc `1` with timeout/no receipt and did not land.
3. One transient `OwnerPositionStatusForUnknownPosition` occurred before fill materialization; fill accounting then occurred exactly once.

## Files

- Evidence: `evidence.json`
- Scenario matrix: `scenario-matrix.md`, `scenario-matrix.json`
- Sanitized raw evidence: `raw/`
