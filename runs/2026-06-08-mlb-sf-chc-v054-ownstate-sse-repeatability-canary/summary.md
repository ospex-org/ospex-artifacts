# Ospex v0.5.4 own-state SSE repeatability canary — SF-CHC contest 31

## Verdict

**GREEN-candidate / partial artifact** — live quote, one controlled partial fill, restart/resume, authoritative cancel, zero public/orderbook exposure, and subscriber cleanup evidence completed. Postgame score/settle/claim is not complete yet; one continuation job is scheduled.

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
- Contest status during canary: `verified`; game status at artifact publication: pre-game.

## Wallet roles

- Contest creator / postgame scorer: ospex-flow-a `0x16dc5d67d080a5521ef2c79680dbfc2abf724d30`
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

## Cost accounting

- Captured run tx count: `12`.
- Total captured operator POL gas: `0.853754960952895306` POL.
- Gas by action: contest create `0.387391704461504809` POL; seed match `0.192436951951284898` POL; controlled partial fill `0.10055528859595362` POL; on-chain cancels `0.173371015944151979` POL.
- LINK: operator net spend `0.005 LINK` for contest creation verification request.
- USDC movements: contest creation `1.000000`; speculation seed/create fees `0.250000` per seed participant; seed risk `0.100000` per side; partial fill risk `0.032000` maker + `0.040000` taker; cancels transferred no USDC. Claims are pending postgame.
- Budget assessment: below the approved `<= $5` equivalent cap before postgame.

## Postgame

- Status: scheduled, not complete.
- Cron job: `3d597ff4ea6c`
- Scheduled time: `2026-06-08T04:45:00Z` / `2026-06-07 23:45 CDT`.
- Continuation will verify MLB Stats + ESPN Final/agreed score before scoring contest 31, settling speculation 21, claiming winners only, running empty sweeps, updating this artifact, validating, safety scanning, committing, pushing, and updating/opening the PR.

## Caveats

- This is a repeatability + one-new-coverage-axis canary, not broad MVE scale proof.
- A short serial warmup window for the same wallet/state/target emitted and cancelled quotes before the controlled partial-fill window; no second target and no simultaneous second MM were run.
- Explicit raw stream-auth token and heartbeat frames were intentionally not printed or archived; readiness/fill ingestion is evidenced indirectly through stream health, fill source, and cleanup metrics.
- One active position (`32000` wei6 maker risk) remains pending game outcome. It is not live/matchable/orderbook exposure.

## Raw/sanitized evidence

See `evidence.json`, `scenario-matrix.md`, `scenario-matrix.json`, and the `raw/` directory. No private signing material, raw signatures, signed payloads, local-only paths, RPC URLs, authorization headers, or specific upstream odds-provider labels are included.
