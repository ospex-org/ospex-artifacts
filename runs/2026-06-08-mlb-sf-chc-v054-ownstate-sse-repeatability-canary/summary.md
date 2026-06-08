# Ospex v0.5.4 own-state SSE repeatability canary — SF-CHC contest 31

## Verdict

**GREEN repeatability canary / complete verified with caveats** — live quote, one controlled partial fill, restart/resume, authoritative cancel, zero public/orderbook exposure, subscriber cleanup, independent final-score agreement, scoring, settlement, claims, and empty post-claim sweeps are complete.

Strategic result: **Phase 3 own-state SSE is live-proven twice / repeatability improved; still not MVE-scale-proven.**

## Baseline

- Baseline PR #15: merged into `main` at `2026-06-07T22:45:05Z`, merge commit `c280253b1b8dd74397b2bad89cbe1bda1f4eda90`.
- This artifact branch is based on that merged main commit.

## Target

- Game: San Francisco Giants @ Chicago Cubs
- MLB Stats gamePk: `824670`
- Start: `2026-06-08T00:30:00Z` / `2026-06-07 19:30 CDT`
- Contest ID: `31`
- Speculation ID: `21` (moneyline; `upper = away/San Francisco Giants`, `lower = home/Chicago Cubs`)
- Final score: San Francisco Giants `2`, Chicago Cubs `1`.

## Wallet roles

- Contest creator / scorer / seed upper winner: ospex-flow-a `0x16dc5d67d080a5521ef2c79680dbfc2abf724d30`
- Market-maker: stage-maker-b `0x4fa0a5aa3187517efc320aac7d33cd6115cc7482`
- Controlled taker/fill wallet: ospex-fresh-user `0x4ddfeeb90b53f7616135ce9d2b8f317af3c4066d`
- Claim-sweep/readiness wallet: stage-maker-a `0x5316fa54c170d1927f30d1a497ac9e85e3826a9b`

## Runtime/release matrix

- `ospex --version`: `0.5.4`
- `@ospex/cli`: `0.5.4`
- `@ospex/sdk` runtime: `0.5.4`
- MM installed `@ospex/sdk`: `0.5.4` from the v0.5.4 GitHub release tarball
- SDK v0.5.4 tag commit: `7622600bf3a940b892db2560e6cceb997e976a01`
- Runtime repo SHAs: market-maker `350e6f62cc8e3b4f3e337674c4e198cb20c2c3f1`, SDK worktree `989f3161fc16cf14e1f90d6054dd4328f7e1492c`, core API `11ff7f1ed90048161c4a3afc34a91cfa3fc29e23`, indexer `24403d5e6a157a1229de119e80bc48232282cc15`.
- Open PRs in the four runtime repos at preflight: none.

## Live evidence

- Contest 31 was created and verified; speculation 21 was created/seeded.
- Live MM used one wallet/state/target, owner-state subscription enabled, live mode, tiny caps, and on-chain shutdown cancel.
- Quote emitted: yes. Main selected quote hash `0x3d7e892053d045069cd0b426263aa08a98823cf9f0b9dad6f2c3e93ccd713335` with maker risk `100000` wei6.
- Controlled partial fill tx: `0x30ca335e185af1a2303dd58b9d92f37f7af94508fce05119293a0ff6f2931cec`.
- Partial-fill retained remainder: maker filled `32000` wei6 from `100000` wei6, retaining `68000` wei6 before authoritative cancel.
- Own-state SSE evidence: stream health hold entered/cleared; fill telemetry source was `own-state-stream`; divergence/unknown-own-fill/owner-mapping-failed counts were zero.
- Restart/resume: restart from same state showed stream-cold-restart + health-hold clear, zero duplicate fill events for the filled hash, and no unsafe final public exposure.
- Authoritative cancel txs are listed in `raw/tx-receipts.summary.json`; final public commitments/orderbook rows are zero.
- Subscriber cleanup: post-shutdown API metrics show own-state subscribers `0`, stream subscribers `0`, connections `0`.

## Postgame evidence

- Read-only preflight captured UTC and America/Chicago time, no MM/live-soak process, and v0.5.4 CLI/SDK runtime proof.
- MLB Stats API and ESPN both showed Final and agreed: San Francisco Giants `2`, Chicago Cubs `1`.
- Score: initial request tx `0x7c08ccaec288854d18d946ea26c4529e0b9e06df38557e62d60e260613bbec0b` emitted a sanitized oracle upstream API failure callback `0x4d92d656d59a903afb499e70c0e4f92b356b1fb8037a0b9bd3d28fadb48c8628`; retry request tx `0x8a47c3ef1d0418cede5887ee92954e3062a1b6abfdc6a7d7f0712f3bda62a195` fulfilled via callback `0xec0fb8c1e3d9a5129771d731a4d831fece19c65b5ffc6307b17faae55d2e21d2` and projected contest 31 as scored `2-1`.
- Settle: speculation 21 settled away/upper with tx `0xd14c2f9eb5a67f04c21d2202e081b1035909d16bc981c0104cf7f01e5e1a8fa7`.
- Claims: stage-maker-b claimed `72000` wei6 (`0.072000 USDC`) with tx `0x3aa349fa934ca9c4139409630c99002eb0a7e69935e99c45dfd04644e34ff2fd`; ospex-flow-a seed/setup upper position claimed `200000` wei6 (`0.200000 USDC`) with tx `0x990f9b0b88334a93d21c5c65e951d98cdf1c78dd97ad0a27594a4978ae801baa`.
- Not claimed: ospex-fresh-user lower/home position lost; stage-maker-a had no claimable entry.
- Post-claim dry-run sweeps for stage-maker-a, stage-maker-b, ospex-fresh-user, and ospex-flow-a all returned zero entries.

## Cost accounting

- Captured pre-postgame run tx count: `12`.
- Pre-postgame captured operator POL gas: `0.853754960952895306` POL.
- LINK: operator net spend before postgame was `0.005 LINK`; the postgame score retry added one additional scoring request after the first callback failed.
- USDC movements before claims: contest creation `1.000000`; speculation seed/create fees `0.250000` per seed participant; seed risk `0.100000` per side; partial fill risk `0.032000` maker + `0.040000` taker; cancels transferred no USDC.
- Postgame claims paid `0.072000 USDC` to stage-maker-b and `0.200000 USDC` to ospex-flow-a.
- Budget assessment: below the approved `<= $5` equivalent cap.

## Final exposure

- Public visible commitments/orderbook rows for contest 31/speculation 21: `0`.
- Active/pending/claimable positions across the four checked wallets: `0`.
- Winning controlled positions are claimed; losing lower/home position has no claimable payout.
- No Ospex MM/live-soak process observed after shutdown/postgame.
- No additional cron jobs were scheduled by this run.

## Caveats

- This is a repeatability + one-new-coverage-axis canary, not broad MVE scale proof.
- A short serial warmup window for the same wallet/state/target emitted and cancelled quotes before the controlled partial-fill window; no second target and no simultaneous second MM were run.
- Explicit raw stream-auth token and heartbeat frames were intentionally not printed or archived; readiness/fill ingestion is evidenced indirectly through stream health, fill source, and cleanup metrics.
- The first score request produced a sanitized oracle upstream API failure callback; a bounded retry fulfilled and scored the contest.

## Raw/sanitized evidence

See `evidence.json`, `scenario-matrix.md`, `scenario-matrix.json`, and the `raw/` directory, especially the `raw/postgame-*` files. No signing material, raw signatures, signed payloads, local-only paths, endpoint URLs, auth headers, or specific upstream odds-provider labels are included.
