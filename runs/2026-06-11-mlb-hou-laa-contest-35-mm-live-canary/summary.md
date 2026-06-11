# HOU-LAA contest 35 MM live canary — GREEN live-window / POSTGAME-DEFERRED

**Status:** `complete_verified_with_caveats` / **GREEN-live-window / POSTGAME-DEFERRED**.

## Verdict

The tiny post-retirement live canary passed its live-window criteria. Contest `35` / speculation `25` was prepared for Houston Astros @ Los Angeles Angels after Contest `34` had already passed first pitch. The live MM posted only two tiny short-expiry commitments on the intended HOU-LAA moneyline target, one controlled partial fill succeeded, MM telemetry recorded the canonical fill source as `own-state-stream`, no canonical legacy polling/diff source was observed, and public/API live exposure drained to zero after shutdown and expiry grace.

Postgame remains deferred until the real-world final score is independently verified. A continuation cron (`a17f517fd6c3`) is scheduled for `2026-06-11T06:00:00Z`.

## Target and wallets

- Game: Houston Astros @ Los Angeles Angels
- Contest/speculation: `35` / `25`; market: moneyline
- Start: `2026-06-11T01:38:00+00:00` UTC
- Target setup/seed wallet: stage-maker-a `0x5316fa54c170d1927f30d1a497ac9e85e3826a9b`
- Live MM maker wallet: stage-maker-b `0x4fa0a5aa3187517efc320aac7d33cd6115cc7482`
- Controlled taker wallet: flow-a `0x16dc5d67d080a5521ef2c79680dbfc2abf724d30`

## Runtime alignment

- MM repo/head: `ospex-org/ospex-market-maker` `eb06ce2dbd18ff5817e976bc5be53f6c332ee103`
- SDK dependency observed: `@ospex/sdk v0.6.2`
- CLI/SDK: `0.6.2`
- Node/Yarn: `v22.22.0` / `1.22.22`
- Install/build/smoke passed from fresh clone.

## Live-window evidence

- Live commitments posted: `2` tiny commitments, each `0.100000 USDC` risk, both expiring `2026-06-11T01:12:24+00:00`.
- Filled commitment: `0xa614b53b44cf09e6b22634f684fa6e435f349070204e509bf83f7ab12786ca38`.
- Fill tx: `0x61b910e5d363fbe1733e505a572876d7ead4b8b6677077ed5f41defc251f39d2`, status `confirmed`.
- Controlled fill size: taker risk `0.049984 USDC`; maker filled risk `0.056800 USDC`.
- Own-state SSE evidence: one `fill` event, source `own-state-stream`; `legacyCanonical` list empty; stream health hold entered and cleared automatically in live mode.
- Public/API exposure after shutdown+expiry: contest count `0`, speculation count `0`, maker visible commitment count `0`.
- Orphan process scan: `0`.

## Budget / cost

- Total operator gas observed: `0.73947760950971103 POL`.
- New controlled live risk: `0.049984 USDC` taker / `0.056800 USDC` maker filled.
- Within the `≤5.00 USDC` controlled tiny-risk cap.

## Caveats

1. Contest `34` was skipped for live writes because first pitch had already passed. HOU-LAA was created/seeded under the user's explicit green light to keep the canary window.
2. Quote-both-sides posted two tiny commitments; only one was partially filled. The unfilled commitment was soft-cancelled/expired and public exposure reached zero.
3. Restart/cold-start probe was read-only/dry-run with fresh local state. It proves no phantom public exposure and safe cold-start behavior; it is not a process-level persisted cursor resume proof.
4. Postgame score → settle → claim is deferred and scheduled; this artifact is not FULL GREEN yet.

## Files

- Evidence: `evidence.json`
- Scenario matrix: `scenario-matrix.md`, `scenario-matrix.json`
- Sanitized raw evidence: `raw/`
- Postgame continuation: `raw/postgame-continuation.sanitized.json`
