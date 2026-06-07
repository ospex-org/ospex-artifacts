| # | Scenario | Classification | Evidence |
|---:|---|---|---|
| 1 | Fresh current checkout/build/test | proven | market-maker/sdk/core-api/indexer local gates were recorded PASS before live work. |
| 2 | core-api M1 local own-state load harness | proven | bench:check and bench:ownstate were recorded PASS. |
| 3 | stream-auth token mint | proven | MM live ownState.subscribe:true connected to owner-auth SSE; subscriber count rose to 1. |
| 4 | owner snapshot | read_only_proven | Earlier owner snapshot smoke passed; restart baseline loaded without blank-state undercount. |
| 5 | owner SSE ready/heartbeat/frame path | proven | ownState subscriber count 1 during run; fill arrived via own-state-stream; restart stream health hold cleared. |
| 6 | MM canonical SSE writer enabled | proven | MM config ownState.subscribe:true; fill event source=own-state-stream; audit/poll produced no divergence events. |
| 7 | controlled live quote | proven | Stage-maker-b live MM posted three commitments total under contest allowlist 29. |
| 8 | controlled fill observed via own-state SSE | proven | ospex-flow-a full-filled one live MM quote; telemetry recorded exactly one fill event source=own-state-stream. |
| 9 | fill dedup/restart safety | proven_with_caveats | Restart loaded same state, emitted stream-cold-restart/resume health hold, refused blank-slate repost due no headroom; no duplicate fill events. Caveat: state retained an expired soft-cancelled row until next run cleanup. |
| 10 | audit-vs-canonical divergence | proven | No divergence events in telemetry summary. |
| 11 | own-state health/indexer lag gate | proven | Natural restart stream-health-hold entered with exposure and then cleared before quoting; health gate halted posting. |
| 12 | beforePost fail-closed posting gate | proven_with_caveats | During restart, the hold/no-headroom prevented posting while stream baseline was cold; no post occurred before hold cleared. Caveat: no manufactured degraded API outage. |
| 13 | signedPayload persisted but not leaked | proven | MM state persisted signedPayload internally; artifact safety scan excludes signedPayload/signature material. |
| 14 | hidden-row/public redaction safety | proven | Final public visible/open commitment query returned 0 while local soft-cancelled/expired lifecycle rows remained internal only. |
| 15 | routine on-chain cancel / authoritative invalidation | deferred | Run used off-chain cancel mode because explicit on-chain cancel approval was not requested/obtained for the MM; no authoritative cancel tx. |
| 16 | active stream-health cancel-sweep | deferred | Run used orders.cancelMode: offchain; no on-chain active cancel-sweep occurred. Natural stream-health hold was observed on restart, but sweep behavior was not exercised. |
| 17 | final zero public exposure | proven | No MM process; ownState/odds subscribers 0; public visible open/partial commitments 0; soft-cancelled local row expired on-chain. |
| 18 | postgame score/settle/claim | proven_with_caveats | Postgame continuation: MLB Stats API and ESPN agreed MIL 7, COL 1 final; contest 29 scored, speculation 19 settled/closed with win_side=away, both upper/away winner claims confirmed, final claim sweeps empty. Overall artifact remains AMBER because original soak was short/full-fill/offchain-cancel-only. |
