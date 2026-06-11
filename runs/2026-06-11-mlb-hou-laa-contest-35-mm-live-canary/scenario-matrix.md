# Scenario matrix

| Scenario | Status | Evidence | Notes |
|---|---|---|---|
| target preflight | `pass` | `raw/target-decision.sanitized.json` | Contest 34 verified but already post-start; HOU-LAA target was created/seeded under user green light. |
| repo/runtime gates | `pass` | `raw/release-runtime-matrix.sanitized.json` | Fresh clone main, install/build/smoke passed. |
| wallet/auth/balances | `pass` | `raw/wallet-auth-balance-allowances.sanitized.json` | Strict non-interactive auth succeeded for setup, maker, and flow wallets after signer source resolution. |
| bounded approvals | `pass` | `raw/wallet-auth-balance-allowances.sanitized.json` | Only bounded low-value allowances observed/created; no unlimited approvals. |
| MM doctor/quote/dry-run loop | `pass` | `raw/mm-dryrun-summary.sanitized.json` | Dry-run selected only contest 35 and produced intended quote intents with no writes. |
| live commitments posted | `pass` | `raw/live-public-commitments-posted.sanitized.json` | MM posted two tiny 0.100000 USDC live commitments on contest 35/speculation 25 only; both had short expiry. |
| controlled partial fill | `pass` | `raw/live-fill.sanitized.json` | One flow-a partial fill succeeded: taker risk 0.049984 USDC, maker filled risk 0.056800 USDC. |
| own-state SSE canonical fill | `pass` | `raw/own-state-sse-summary.sanitized.json` | Telemetry recorded fill source own-state-stream and zero canonical legacy source events. |
| expiry/shutdown zero public exposure | `pass` | `raw/zero-exposure.sanitized.json` | After shutdown and expiry grace, public/API commitments were zero; no orphan process remained. |
| restart/cold-start safety | `pass_with_caveat` | `raw/restart-cold-start-probe.sanitized.json` | Read-only dry-run cold-start booted without persisted state/cursor and left public exposure zero; not a process-level cursor-resume proof. |
| postgame lifecycle | `deferred` | `raw/postgame-continuation.sanitized.json` | Score/settle/claim deferred until final score. Continuation cron scheduled for 2026-06-11T06:00:00Z. |
