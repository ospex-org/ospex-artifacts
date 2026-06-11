# HOU-LAA contest 35 MM live canary — FULL GREEN / COMPLETE

**Status:** `complete_verified_with_caveats` / **FULL GREEN / COMPLETE**.
Captured: `2026-06-11T06:23:31Z`

## Verdict

The tiny post-retirement live canary completed its full postgame lifecycle. Contest `35` / speculation `25` was prepared for Houston Astros @ Los Angeles Angels after Contest `34` had already passed first pitch. The live MM posted only two tiny short-expiry commitments on the intended HOU-LAA moneyline target, one controlled partial fill succeeded, MM telemetry recorded the canonical fill source as `own-state-stream`, no canonical legacy polling/diff source was observed, and public/API live exposure drained to zero after shutdown and expiry grace.

Postgame is now complete: MLB Stats API verified a final score of Houston Astros `2`, Los Angeles Angels `3` (10 innings), so home/lower won. Contest `35` was scored by the contest creator/operator wallet, speculation `25` settled `home`, the two winning controlled positions were claimed, the setup wallet had no claimable winning position, final claim-all dry-runs are empty for all controlled wallets, public/API live commitments remain zero, and no MM process remains.

## Target and wallets

- Game: Houston Astros @ Los Angeles Angels
- Contest/speculation: `35` / `25`; market: moneyline
- Start: `2026-06-11T01:38:00+00:00` UTC
- Final score source: MLB Stats API schedule (`gamePk` `824022`), fetched `2026-06-11T06:18:55Z`; status `Final`
- Protocol outcome: home/lower (Los Angeles Angels) wins
- Target setup/seed wallet: stage-maker-a `0x5316fa54c170d1927f30d1a497ac9e85e3826a9b`
- Live MM maker wallet: stage-maker-b `0x4fa0a5aa3187517efc320aac7d33cd6115cc7482`
- Controlled taker wallet: flow-a `0x16dc5d67d080a5521ef2c79680dbfc2abf724d30`

## Runtime alignment

- MM repo/head: `ospex-org/ospex-market-maker` `eb06ce2dbd18ff5817e976bc5be53f6c332ee103`
- SDK dependency observed: `@ospex/sdk v0.6.2`
- CLI/SDK: `0.6.2`
- Node/Yarn: `v22.22.0` / `1.22.22`
- Install/build/smoke passed from fresh clone; postgame write commands used the built `@ospex/cli` `0.6.2`.

## Live-window evidence

- Live commitments posted: `2` tiny commitments, each `0.100000 USDC` risk, both expiring `2026-06-11T01:12:24+00:00`.
- Filled commitment: `0xa614b53b44cf09e6b22634f684fa6e435f349070204e509bf83f7ab12786ca38`.
- Fill tx: `0x61b910e5d363fbe1733e505a572876d7ead4b8b6677077ed5f41defc251f39d2`, status `success`.
- Controlled fill size: taker risk `0.049984 USDC`; maker filled risk `0.056800 USDC`.
- Own-state SSE evidence: one `fill` event, source `own-state-stream`; `legacyCanonical` list empty; stream health hold entered and cleared automatically in live mode.
- Public/API exposure after shutdown+expiry and again after postgame: contest orderbook count `0`, indexer visible-live commitments `0`, maker visible commitment count `0`.
- Orphan process scan: `0`.

## Postgame lifecycle

- Score request tx: `0xd2db66dcc8d8740ce933ef9704b3f7b7bded72caecfb538ca6a68177d71074be` (`0.185458527013152777 POL` gas).
- Score callback / `CONTEST_SCORES_SET` tx: `0x9091ac23b31bd36f2457702b01d9329dc78f6d46fb41879e90922f820f5ff00c` (`0.110139035169543598 POL` observed callback gas; callback sender is not a controlled wallet).
- Settle speculation tx: `0x9a9491db3315de1b3e2050c485503c4ae4731b6a4285b5a46d7b6c52b517fa89` (`0.043875431255954286 POL` gas), win side `home`.
- Claim tx — stage-maker-b: `0x22ddc13d4cdcd7a0edd288fdf32ab9218d0cbbac998535934090221592dbbea4` (`0.035391119683640125 POL` gas), payout `106784` wei6 / `0.106784 USDC`.
- Claim tx — flow-a: `0xcbd92cd4c1fe5b2412613be2333368090e2410a9fe794dacb303111e0fd38865` (`0.035345616680631375 POL` gas), payout `20800` wei6 / `0.020800 USDC`.
- stage-maker-a final claim-all dry-run: zero entries / no-op (upper/away seed maker position lost).
- Final claim-all dry-runs: zero entries for stage-maker-b, flow-a, and stage-maker-a.

## Budget / cost

- Total operator gas observed through full lifecycle: `1.039548304143089593 POL` (≈ `0.259887 USDC` at the run config reporting price `0.25 USDC/POL`).
- Postgame operator gas: `0.300070694633378563 POL` (≈ `0.075018 USDC` at the same reporting price).
- Callback observed gas: `0.110139035169543598 POL` (included as lifecycle evidence, excluded from controlled-operator spend total because sender was not a controlled wallet).
- New controlled live risk remained `0.049984 USDC` taker / `0.056800 USDC` maker filled; claims returned the winning positions.
- Within the `≤5.00 USDC` controlled tiny-risk/spend cap.

## Caveats

1. Contest `34` was skipped for live writes because first pitch had already passed. HOU-LAA was created/seeded under the user's explicit green light to keep the canary window.
2. Quote-both-sides posted two tiny commitments; only one was partially filled. The unfilled commitment was soft-cancelled/expired and public exposure reached zero.
3. Restart/cold-start probe was read-only/dry-run with fresh local state. It proves no phantom public exposure and safe cold-start behavior; it is not a process-level persisted cursor resume proof.
4. Coverage caveat only: this proves the one-target low-value canary path, not broad multi-contest MM scale.

## Files

- Evidence: `evidence.json`
- Scenario matrix: `scenario-matrix.md`, `scenario-matrix.json`
- Final score source: `raw/final-score-source.json`
- Postgame CLI/claim evidence: `raw/cli-postgame.sanitized.json`
- Final API/indexer/process state: `raw/final-cli-api-state.sanitized.json`
- Tx receipts/cost summary: `raw/tx-receipts.summary.json`
- Sanitized raw evidence: `raw/`
