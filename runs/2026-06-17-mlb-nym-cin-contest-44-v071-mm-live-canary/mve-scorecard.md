# MVE scorecard

**Verdict:** FULL_GREEN

The v0.7.1 NYM @ CIN MM canary completed the full lifecycle: official final score New York Mets 9, Cincinnati Reds 1 was verified; contest 44 was scored; speculation 33 settled to away/upper/New York Mets; the winning controlled live-fill and setup seed/open positions were claimed; final claim sweeps, public commitments/orderbook, and live-MM process checks are zero. Caveats are limited to a not-run restart/cold-start probe and CLI readback omission of winSide/settledAt despite converged indexer/protocol state.

| id | capability | proof | evidence | notes |
|---|---|---|---|---|
| target-preflight | Target preflight and allowlist | proven_live | raw/target-preflight.sanitized.json | Primary target verified and quote_ready before live writes. |
| repo-runtime-gates | Repo/runtime gates | proven_live | raw/release-runtime-matrix.sanitized.json | v0.7.1 CLI/SDK/MM runtime alignment verified. |
| wallet-auth-balances | Wallet auth, balances, allowances | proven_live | raw/wallet-auth-balance-allowances.sanitized.json | Reserved live maker was clean before start and wallet balances/allowances were sufficient. |
| bounded-approvals | Bounded approvals / no unlimited approvals | proven_live | raw/bounded-approvals.sanitized.json | No unlimited approvals; no new live approvals were required. |
| dry-run-quote-loop | Dry-run quote loop | proven_synthetic_only | raw/mm-dryrun-summary.sanitized.json | Quote dry-run was synthetic/read-only by nature and selected target 44 only. |
| live-commitments-posted | Live commitments posted | proven_live | raw/live-public-commitments-posted.sanitized.json | Live public commitments posted on target 44/33 only. |
| live-fill | Controlled live fill | proven_live | raw/live-fill.sanitized.json | Exactly one controlled live fill succeeded. |
| own-state-sse-canonical-fill | Own-state SSE canonical fill source | proven_live | raw/own-state-sse-summary.sanitized.json | Telemetry fill event source is own-state-stream. |
| exposure-drain-zero | Exposure drained to zero | proven_live | raw/zero-exposure.sanitized.json | End-of-run public/API/MM visible-open exposure is zero. |
| restart-cold-start-safety | Restart/cold-start safety | not_applicable |  | Not part of this live-window canary artifact; final zero-exposure/process checks cover shutdown safety. |
| postgame-score | Postgame score | proven_live | raw/postgame-lifecycle.sanitized.json | Official final score New York Mets 9, Cincinnati Reds 1 verified and contest 44 scored. |
| postgame-settle | Postgame settle | proven_live | raw/postgame-lifecycle.sanitized.json | Speculation 33 settled to away/upper/New York Mets. |
| postgame-claim | Postgame claim/no-op | proven_live | raw/postgame-lifecycle.sanitized.json | Winning upper/New York Mets positions for mm-shakeout-flow-a and ospex-stage-maker-b claimed; losing lower/Cincinnati positions no-op. |
| cost-within-cap | Cost within cap | proven_live | raw/tx-receipts.summary.json | Live + postgame controlled costs stayed within the low-value canary envelope. |

## Transactions

- create-contest: `0x1fa840f942a6b6c34981a91b98dc940e1a815160539e3bea9564a52839c32e73` — Setup handoff created verified contest 44 for NYM @ CIN before the live MM window.
- seed-match: `0x173f061fa56934fe51c906d9635d3a53b7c1d75a703e811d7b931d1b4143026e` — Setup handoff seed/open moneyline fill for speculation 33.
- match-commitment: `0x7d8ad8dc09db574e7b4ab1e713d8b1ff16b2df9dc0e0bc73335bb090849273cc` — Exactly one controlled live MM fill by mm-shakeout-flow-a against commitment 0x7818744c708eb986aefcfe7ec70913821652bd061268f61287f0a78b22a6662b.
- score-request: `0xec13a28e3fb6b1ca8ee2d8a66bb413a329be39cebc09857e348cfd486cde82de` — Score contest 44 after official MLB final source showed New York Mets 9, Cincinnati Reds 1.
- settle: `0xc5a9d1b68781b519484f903debdd179c6ffcf308fc1001cbc695519a143b957e` — Settle speculation 33 to away/upper/New York Mets.
- claim: `0x2e5d50bec4b618768c6193fcbe9cdddffd9e3813f2090cb9b50f6f3c9c5141c1` — Claim mm-shakeout-flow-a winning live-fill upper/New York Mets position.
- claim: `0x390cf95777650673d2971377ca1914dc27274039610921bf9d860ffc942818e9` — Claim ospex-stage-maker-b winning setup seed/open upper/New York Mets position.
