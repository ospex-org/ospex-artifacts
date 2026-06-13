# Scenario matrix

Render of `scenario-matrix.json`; the JSON file is canonical. One row per scenario, same order. This template defaults to a live-window-green / postgame-deferred run; shared-id rows stay consistent with the scorecard's proof levels.

| Scenario | Status | Evidence | Notes |
|---|---|---|---|
| target preflight | `pass` | `raw/target-decision.sanitized.json` | Target contest/speculation selection and verification state. Name both teams with home/away roles. |
| repo/runtime gates | `pass` | `raw/release-runtime-matrix.sanitized.json` | Fresh clone or tagged release; install/build/smoke results; observed SDK/CLI/Node/Yarn versions. |
| wallet/auth/balances | `pass` | `raw/wallet-auth-balance-allowances.sanitized.json` | Strict non-interactive auth result per wallet role; balance sufficiency for the planned window. |
| bounded approvals | `pass` | `raw/wallet-auth-balance-allowances.sanitized.json` | Only bounded low-value allowances observed/created; no unlimited approvals. |
| MM doctor/quote/dry-run loop | `pass` | `raw/mm-dryrun-summary.sanitized.json` | Dry-run selected only the intended target and produced quote intents with no writes. |
| live commitments posted | `pass` | `raw/live-public-commitments-posted.sanitized.json` | Count, per-commitment risk, expiry, and intended-target-only scope of live commitments. |
| live fill | `pass` | `raw/live-fill.sanitized.json` | Fill transaction outcome with taker/maker risk amounts and sides named per the Team Identity Rule. If no fill, set `deferred`/`fail` and use `AMBER_QUOTED_NO_FILL`. |
| own-state SSE canonical fill | `pass` | `raw/own-state-sse-summary.sanitized.json` | Fill event source observed in telemetry; canonical legacy fill sources observed (expected: none). |
| expiry/shutdown zero public exposure | `pass` | `raw/zero-exposure.sanitized.json` | Public/API live commitment exposure after shutdown and expiry grace; orphan process scan result. |
| restart/cold-start safety | `pass_with_caveats` | `raw/restart-cold-start-probe.sanitized.json` | State whether the probe was read-only/dry-run and whether it proves cursor resume or only no-phantom-exposure. |
| postgame lifecycle | `deferred` | — | External final score source and result, score/settle/claim transactions, final dry-run and process checks. Defaults to `deferred` (artifact cut before the game is final); set `pass` with evidence once the lifecycle completes. |
