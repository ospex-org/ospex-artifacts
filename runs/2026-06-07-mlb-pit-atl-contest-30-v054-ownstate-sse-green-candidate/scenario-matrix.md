| # | Scenario | Classification | Evidence |
|---:|---|---|---|
| 1 | Release alignment and public-path install | proven | @ospex/cli 0.5.4 and @ospex/sdk 0.5.4 release tarballs were captured with SHA256s; MM dependency was pinned to the v0.5.4 SDK tarball. |
| 2 | Single approved target selection | proven | PIT-ATL MLB game was selected from MLB Stats/ESPN/Ospex game evidence; contest 30 and moneyline speculation 20 are the only live target in the run. |
| 3 | Contest creation and verification | proven | Contest creation tx confirmed; contest 30 indexed as verified with Pittsburgh Pirates @ Atlanta Braves start 2026-06-07T17:35:00Z. |
| 4 | Moneyline speculation seed | proven | Lazy first match created/seeded speculation 20 with a controlled low-value seed match. |
| 5 | Owner-state SSE connection/subscriber accounting | proven | During the main run API metrics showed ownState wallets=1/subscribers=1; final metrics returned ownState subscribers=0 and connections=0. |
| 6 | 62-minute live own-state SSE soak | proven | Main stage-maker-b live run telemetry spanned 2026-06-07T08:06:37Z to 2026-06-07T09:08:50Z with 61 ticks. |
| 7 | Controlled partial fill observed through own-state stream | proven | ospex-fresh-user partially filled stage-maker-b commitment 0xad05…; telemetry emitted fill source=own-state-stream with newFillWei6=26300. |
| 8 | Post-fill retained/remainder risk cleanup | proven | The partially filled commitment and subsequent replacement/open commitments were authoritatively invalidated by on-chain cancel txs; final public commitments for contest 30/speculation 20 were zero. |
| 9 | Restart/resume safety | proven | Restart telemetry emitted stream-cold-restart and stream-health-hold with exposure; no blank-slate repost remained live; later on-chain cancel cleaned remaining commitment. |
| 10 | Active stream-health/on-chain cancel behavior | proven_with_caveats | Authoritative cancels were exercised. A natural restart health hold occurred; no manufactured API outage/fault injection was performed. |
| 11 | Final public/orderbook exposure | proven | Final commitment list by contest and speculation returned zero rows; contest 30 orderbook had zero rows; MM visibleOpen=0 and authoritativelyInvalidated=2. |
| 12 | Filled-position separation from quote exposure | proven | The live run separated filled position risk from quote exposure; postgame settlement/claims later moved the winning lower/home positions to claimed while public commitment/orderbook exposure remained zero. |
| 13 | Cost accounting parser | proven | Receipt parser handled prior and postgame receipt summaries; operator-paid gas totals, LINK scoring spend, and USDC claim payouts are recorded in raw/cost-accounting.json. |
| 14 | Public-safety artifact hygiene | proven_after_validation | Sanitized artifact excludes private keys, local secret-path material, raw RPC URLs, API tokens, raw signatures/signed payload fields, local raw workdir paths, and long calldata blobs; validation scan result is recorded in raw/validation-scan.json. |
| 15 | Postgame score/settle/claim continuation | proven | One-shot read-only-first postgame continuation verified MLB Stats + ESPN Final PIT 2 / ATL 3, scored contest 30, settled speculation 20 lower/home, claimed stage-maker-b and ospex-fresh-user winnings, and all four controlled-wallet claim sweeps are zero-entry after claims. |
