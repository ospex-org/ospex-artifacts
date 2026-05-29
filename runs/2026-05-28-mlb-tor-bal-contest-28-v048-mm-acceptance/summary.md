# Blue Jays @ Orioles v0.4.8 CLI/MM acceptance lifecycle smoke

- Artifact ID: `2026-05-28-mlb-tor-bal-contest-28-v048-mm-acceptance`
- Status: `complete_verified_with_caveats`
- Network: Polygon mainnet (`chainId=137`)
- Target: Toronto Blue Jays @ Baltimore Orioles (`tor-bal-2026-05-28`, gameId `386da824-5f00-49e2-835d-6b47854b55a5`, start `2026-05-28T22:35:00+00:00`)
- Contest/speculation: contest `28`, moneyline speculation `18`
- Captured: `2026-05-29T02:31:08Z`

## Verdict

GREEN complete with non-blocking caveats.

- v0.4.8 CLI contest-create error handling: PASS. The first create attempt was a typed no-transaction `ALLOWANCE_INSUFFICIENT` precondition, not generic `CHAIN_ERROR`; exact bounded approval then allowed bundled/local CLI create to succeed.
- v0.4.8 match JSON approval-remediation UX: PASS. The seed match exercised allowance remediation and ended `fillable` with no stale current allowance blocker; the controlled MM fill also ended `fillable`.
- MM pregame/live smoke: PASS. Bounded live MM posted low-value quotes, one controlled fill succeeded, and final public/orderbook exposure was zero.
- Postgame lifecycle: PASS. Final score, score callback, settlement, winning claim, final dry-runs, and zero orderbook exposure converged.

## Final score and protocol outcome

Official final source: MLB Stats API.

- Toronto Blue Jays: 2
- Baltimore Orioles: 1
- Ospex outcome: away/upper wins.
- Contest `28`: `scored`, score `2-1`, scored at `2026-05-29T02:17:08+00:00`.
- Speculation `18`: `closed`, win side `away/upper`, settled at `2026-05-29T02:18:06+00:00`.

## Key transactions

- Contest create: `0xd111bf649be221391186abfe42450c98d5003d23d605ab5fdea94d2ab5ec448c`
- Seed match: `0x52b95f8f6ad386969923ae72df41a2a07dfd4b7268d6c10b9dcdcf59936fc04f`
- Controlled MM fill: `0x0cff3b6f7372e7018b49d70a00be834137b8bc8c6799f450c787e064addc93c9`
- Score request: `0x71b1320e2298ba8f5797ae252609db0392a46296c4e1ef24e4d3a3fdbcb81347`
- Score callback / scores set: `0x765da2f3eabb296e8dfa6be25e9d600539f75c49f11ced83b917c66438e70087`
- Settle speculation: `0xbc4e86dd9be0ca5227cdbe3bd9ce1cad8ad70e0b977c1b798daf79c52e21dc1f`
- Claim winning controlled position (`ospex-flow-a`): `0x7383ba430542321d620b77eac2c202bc3ac672bc8669e9a74bf7d6cd16ba48dc`

## Claim and exposure closure

- Claimed position: `ospex-flow-a`, upper/away, risk `179000` wei6, profit `200000` wei6, claimed payout `379000` wei6 = `0.379000 USDC`.
- Final `claim-all --dry-run --json` entry counts: `0` for `ospex-stage-maker-a`, `ospex-stage-maker-b`, `ospex-flow-a`, and `ospex-fresh-user`.
- Final contest show orderbook count: `0`.
- Final visible-live commitments: `0`.
- Final unmatched-live-like commitments: `0`.
- No MM runner process remained.

## Caveats

- Operator precondition: creator fee allowance needed an exact bounded approval before contest create.
- MM product/state: one replacement cycle occurred before stop while waiting for MM fill telemetry; replacement rows are expired/non-visible and do not represent live orderbook exposure.
- Operator scheduling: the one-shot postgame cron was set for `2026-05-29T03:15:00Z` (`2026-05-28 22:15 CDT`), so manual completion began before the scheduled cleanup fired.

## Raw evidence

- `raw/repo-freshness.sanitized.json`
- `raw/cli-phase.sanitized.json`
- `raw/mm-phase.sanitized.json`
- `raw/mm-telemetry-summary.sanitized.json`
- `raw/final-score-source.json`
- `raw/final-supabase-state.sanitized.json`
- `raw/cli-postgame.sanitized.json`
- `raw/tx-receipts.summary.json`
- `raw/oracle-score-callbacks.sanitized.json`
- `raw/process-check.sanitized.json`
- `raw/process-check.sanitized.txt`
