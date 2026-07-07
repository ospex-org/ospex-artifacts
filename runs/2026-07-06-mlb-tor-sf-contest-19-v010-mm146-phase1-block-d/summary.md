# Toronto Blue Jays @ San Francisco Giants — MVE Phase 1 Block D

- Artifact ID: `2026-07-06-mlb-tor-sf-contest-19-v010-mm146-phase1-block-d`
- Contest: `19`
- Speculations: moneyline `45`, spread `46`, total `47`
- Intended live target: `spread` speculation `46`
- Live MM: not started; pre-live dry-run gate failed before live writes
- Pre-live dry-run gate: `failed` (`wouldSubmitCount=16`; COL/LAD total absent from would-submit rows)
- Manual seed/fill: all three markets filled with tiny controlled risk; contest open commitments returned to `0`
- Final score: Toronto Blue Jays 1, San Francisco Giants 10
- Score tx(s): 0x5e1ed8fb7ceb620c26a127d45ae00802f5e43f8ac170694d60b04031f1b7f454
- Claim tx(s): 0x04478a22e546ac5a29d2f528287e0fc25fbfb61a930e453d865152e01ffe9688, 0x4d68a21c75df5372380d6ad6449bf8b35aaba19239a952d57bb6b3529bc57c51, 0x1361c1ebd25c0f5db1b4b250f2e3df9442e9e6bbddb09ee4886abc8d78f651bb
- Final open commitments: `0`
- Final target positions: active `0`, pendingSettle `0`, claimable `0` for controlled wallets after manual remediation
- Verdict: `MVE_PHASE1_BLOCK_D_AMBER` (`AMBER_PRELIVE_GATE_HALT`)

Caveats: live MM never posted because the scheduled pre-live safety gate stopped before writes; no stale quote was forced. The postgame watcher initially left residual claimables, then manual remediation claims completed final zero-state.
