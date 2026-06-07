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
| 12 | Filled-position separation from quote exposure | proven | Final MM status still has one legitimate active filled position risk 26300 wei6 awaiting postgame; this is not open quote/orderbook exposure. |
| 13 | Cost accounting parser | proven | Receipt parser handled hex/decimal/null/formatted fields and parsed 9/9 receipt lines without Decimal ConversionSyntax. |
| 14 | Public-safety artifact hygiene | proven_after_validation | Sanitized artifact excludes private keys, local secret-path material, raw RPC URLs, API tokens, raw signatures/signed payload fields, and local raw workdir paths; validation scan result is recorded in raw/validation-scan.json. |
| 15 | Postgame score/settle/claim continuation | scheduled | One-shot read-only-first continuation scheduled for 2026-06-07T21:45:00Z (2026-06-07 16:45 CDT (America/Chicago)), cron job 039b18a3eae6. |
