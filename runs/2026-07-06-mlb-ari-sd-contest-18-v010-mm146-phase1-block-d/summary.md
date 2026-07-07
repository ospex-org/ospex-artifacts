# Arizona Diamondbacks @ San Diego Padres — MVE Phase 1 Block D

- Artifact ID: `2026-07-06-mlb-ari-sd-contest-18-v010-mm146-phase1-block-d`
- Contest: `18`
- Speculations: moneyline `42`, spread `43`, total `44`
- Intended live target: `moneyline` speculation `42`
- Live MM: not started; pre-live dry-run gate failed before live writes
- Pre-live dry-run gate: `failed` (`wouldSubmitCount=16`; COL/LAD total absent from would-submit rows)
- Manual seed/fill: all three markets filled with tiny controlled risk; contest open commitments returned to `0`
- Final score: Arizona Diamondbacks 8, San Diego Padres 0
- Score tx(s): 0xf3a7ea54d4681d860e3c908b25fd96f05b241c84ec8b6ba8abdd5ef6e56b9c80
- Claim tx(s): 0xaa898c7413fc1bde7b21f95a71d684260fd4833c9a3ac6d6053bb2b1fd31a0fa, 0x7178ef894281ce3175f379b83e83f34e27f10dcaf84e3ced9455d6e0a32ed4b2, 0xd883f8984bcbb3d6d091de7985148f32f1454cc4728a4a43aa7be28e95a66212
- Final open commitments: `0`
- Final target positions: active `0`, pendingSettle `0`, claimable `0` for controlled wallets after manual remediation
- Verdict: `MVE_PHASE1_BLOCK_D_AMBER` (`AMBER_PRELIVE_GATE_HALT`)

Caveats: live MM never posted because the scheduled pre-live safety gate stopped before writes; no stale quote was forced. The postgame watcher initially left residual claimables, then manual remediation claims completed final zero-state.
