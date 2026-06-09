# Scenario matrix

| ID | Scenario | Status | Evidence | Notes |
|---|---|---:|---|---|
| `phase0-baseline` | Phase 0 target selection and approval handoff | `pass` | `raw/phase0-preflight.sanitized.json` | SEA/BAL selected; no contest/speculation existed; bounded create/seed approval required. |
| `runtime-matrix` | Release/runtime matrix | `pass` | `evidence.json` | CLI/SDK/MM v0.5.4 aligned; MM installed SDK release tarball pin present; runtime PR pressure zero. |
| `setup-create-seed` | Contest/speculation setup | `pass` | `raw/phase1-handoff.sanitized.md` | Contest 32 created/verified; moneyline speculation 22 opened; bounded allowance remediation recorded. |
| `live-mm-fill` | Live MM canary and controlled partial fill | `pass` | `raw/controlled-match-report.sanitized.json`, `raw/mm-telemetry-summary.sanitized.json` | Main quote filled by controlled taker; fill economics and exactly-one telemetry ingestion recorded. |
| `restart-resume-ownstate` | Restart/resume own-state SSE | `pass` | `raw/mm-telemetry-summary.sanitized.json`, `raw/telemetry-ownstate-extract.sanitized.ndjson` | Same state dir reused privately; stream-cold-restart observed; stream-health-hold entered and cleared; no duplicate fill accounting. |
| `cleanup-safety` | Cleanup and final safety | `pass` | `raw/cleanup-report.sanitized.json`, `raw/phase2-safety-recheck.sanitized.json`, `raw/mm-final-state.sanitized.json` | Partial remainder and opposite-side quote cancelled; visible commitments 0; orderbook empty; live process count 0. |
| `budget-cost` | Budget and receipt accounting | `pass` | `raw/receipt-cost-rollup.sanitized.json` | 8/8 receipts parsed; total gas 0.77985881746265763 POL; estimated USDC movement/lock 1.778760 under cap. |
| `postgame-lifecycle` | Postgame score/settle/claim lifecycle | `pass` | `raw/final-score-source.json`, `raw/cli-postgame.sanitized.json`, `raw/final-positions-claims.sanitized.json`, `raw/final-safety-state.sanitized.json`, `raw/tx-receipts.summary.json` | Official sources agreed SEA 6, BAL 3 Final; contest scored; speculation settled; both winning controlled wallets claimed; final claim sweeps empty; orderbook and visible commitments zero. |
