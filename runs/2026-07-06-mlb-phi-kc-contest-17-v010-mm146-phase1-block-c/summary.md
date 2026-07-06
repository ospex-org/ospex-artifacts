# Philadelphia Phillies @ Kansas City Royals — MVE Phase 1 Block C

- Artifact ID: `2026-07-06-mlb-phi-kc-contest-17-v010-mm146-phase1-block-c`
- Contest: `17`
- Speculations: moneyline `39`, spread `40`, total `41`
- Live target/fill: `spread` speculation `40`; tx `0xa914cb66bdbf3d152c123947eaf6ea3d9b81bcfb31e0bcf0fba1ac1cedecc5f5`; side `Kansas City Royals +1.5`
- Live MM run ID: `2026-07-06T14-35-54-630Z-idgviw`
- Live quote hashes: 0x95305e672aa6282232fb0adbcc70c200349f7ad966a0baacbe1beddc274a893d, 0x4a55ede8756ac7890743965b1cfd11f0280ac30a4a1739bd1a074092de4df9ab, 0xfba5207311cb3aa7d68d4c0a22d18bca474365ce9a7c1329a3a26b0785798903, 0x8092bbfa63cd49f3c9139d4650e635a24f39893036b298496bbe5f7a75de19a9
- Final score: Philadelphia Phillies 1, Kansas City Royals 15
- Final open commitments: `0`
- Final target positions: active `0`, pendingSettle `0`, claimable `0` for controlled wallets
- Verdict: `MVE_PHASE1_BLOCK_C_GREEN_WITH_CAVEATS`

Caveats: startup own-state stream-health hold entered and cleared before controlled fill; one own-state-stream projection-ordering error occurred immediately before canonical fill, but canonical fill was observed (`eventCounts.fill=1`) and bad own-state counts remained zero; live total skipped with `reference-line-mismatch` after setup/dry-run quote-readiness; explicit settle commands were already-settled no-ops after the score transaction.
