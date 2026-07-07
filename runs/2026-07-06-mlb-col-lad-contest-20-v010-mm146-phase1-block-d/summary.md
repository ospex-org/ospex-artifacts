# Colorado Rockies @ Los Angeles Dodgers — MVE Phase 1 Block D

- Artifact ID: `2026-07-06-mlb-col-lad-contest-20-v010-mm146-phase1-block-d`
- Contest: `20`
- Speculations: moneyline `48`, spread `49`, total `50`
- Intended live target: `total` speculation `50`
- Live MM: not started; pre-live dry-run gate failed before live writes
- Pre-live dry-run gate: `failed` (`wouldSubmitCount=16`; COL/LAD total absent from would-submit rows)
- Manual seed/fill: all three markets filled with tiny controlled risk; contest open commitments returned to `0`
- Final score: Colorado Rockies 7, Los Angeles Dodgers 8
- Score tx(s): 0x268e1d27b42031d743b2c630c79be22071794ada26b45f757410fa983cb07371
- Claim tx(s): 0xe7d8d5ae2978976a2cdddea42a34dd589d8cd04c829f6033735c9d8c4acde830, 0x10fbc85c8f809396b88dbc59132e16f327b7323e750cd6dd3b4b460446e98264, 0x9b60abba61788fe3ebf988175862120be94d3bb82b3347e29f98ec1e1091dd70
- Final open commitments: `0`
- Final target positions: active `0`, pendingSettle `0`, claimable `0` for controlled wallets after manual remediation
- Verdict: `MVE_PHASE1_BLOCK_D_AMBER` (`AMBER_PRELIVE_GATE_HALT`)

Caveats: live MM never posted because the scheduled pre-live safety gate stopped before writes; no stale quote was forced. The postgame watcher initially left residual claimables, then manual remediation claims completed final zero-state.
