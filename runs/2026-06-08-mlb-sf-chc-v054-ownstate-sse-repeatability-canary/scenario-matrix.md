# Scenario matrix

| # | Scenario | Status | Evidence |
|---:|---|---|---|
| 1 | Fresh install SDK/CLI release v0.5.4 | `proven` | Release assets and v0.5.4 CLI package/bin verified. |
| 2 | MM installed SDK v0.5.4 from release tarball | `proven` | MM node_modules has @ospex/sdk 0.5.4 and package/lock reference the v0.5.4 release tarball. |
| 3 | Same-evening target discovery | `proven` | SF @ CHC same-evening MLB target selected with reference odds available and contest creation allowed. |
| 4 | Contest creation, if needed | `proven` | Contest 31 created and verified on Polygon mainnet. |
| 5 | Moneyline speculation seed/create | `proven` | Speculation 21 moneyline created/seeded; upper=away, lower=home. |
| 6 | Single controlled live quote/fill | `proven` | One controlled partial fill tx executed against a live MM quote. |
| 7 | Partial-fill retained remainder | `proven` | Maker quote risk 100000 wei6; fill consumed 32000 wei6, leaving retained remainder before authoritative cancel. |
| 8 | Authoritative on-chain cancel after partial fill | `proven` | Filled/remainder and shutdown quotes were authoritatively cancelled on-chain. |
| 9 | Restart/resume after fill | `proven_with_caveats` | Restart used same wallet/state, recovered health, and showed zero duplicate fill events for the filled hash; short restart emitted then canceled new quotes. |
| 10 | Own-state SSE ready/heartbeat/fill ingestion | `proven_with_caveats` | Own-state health hold cleared and fill was ingested from own-state-stream; explicit heartbeat frame not separately archived in public artifact. |
| 11 | Audit/poll comparator retained, no divergence | `proven` | Telemetry summary has zero divergence, unknown-own-fill, and owner-mapping-failed events. |
| 12 | Final zero public/orderbook exposure | `proven` | Commitments list returned zero visible rows; contest/speculation orderbook rows zero after shutdown. |
| 13 | Subscriber cleanup after shutdown | `proven_with_caveats` | API metrics after shutdown show own-state and stream subscribers at 0; during subscriber count not separately archived. |
| 14 | Postgame score/settle/claim lifecycle | `proven_with_caveats` | MLB Stats API and ESPN both showed Final with SF 2, CHC 1; initial score request emitted a sanitized upstream API failure, retry fulfilled, contest 31 scored, speculation 21 settled away/upper, and winning controlled positions claimed. |
| 15 | Final empty claim sweeps | `proven` | Post-claim dry-run sweeps for stage-maker-a, stage-maker-b, ospex-fresh-user, and ospex-flow-a all returned zero entries. |
| 16 | Multi-contest read-only discovery | `read_only_proven` | Read-only games discovery ran; canary intentionally selected one target. |
| 17 | Two simultaneous live targets | `deferred` | Intentionally not run for bounded canary. |
| 18 | Two independent live MMs | `deferred` | Intentionally not run; no simultaneous second MM observed. |
| 19 | Fillability/solvency signaling | `proven_with_caveats` | Fillability/advisory and funding guard data were observed; not treated as a broad solvency proof. |
| 20 | Long soak / 24–48h stability | `deferred` | Out of scope for repeatability canary. |
