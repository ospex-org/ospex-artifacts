# Scenario matrix

Render of `scenario-matrix.json`; the JSON file is canonical. One row per scenario, same order.

| Scenario | Status | Evidence | Notes |
|---|---|---|---|
| target preflight | `not_run` | — | Target contest/speculation selection and verification state. Name both teams with home/away roles. |
| repo/runtime gates | `not_run` | — | Fresh clone or tagged release; install/build/smoke results; observed SDK/CLI/Node/Yarn versions. |
| wallet/auth/balances | `not_run` | — | Strict non-interactive auth result per wallet role; balance sufficiency for the planned window. |
| bounded approvals | `not_run` | — | Only bounded low-value allowances observed/created; no unlimited approvals. |
| MM doctor/quote/dry-run loop | `not_run` | — | Dry-run selected only the intended target and produced quote intents with no writes. |
| live commitments posted | `not_run` | — | Count, per-commitment risk, expiry, and intended-target-only scope of live commitments. |
| live fill | `not_run` | — | Fill transaction outcome with taker/maker risk amounts and sides named per the Team Identity Rule. |
| own-state SSE canonical fill | `not_run` | — | Fill event source observed in telemetry; canonical legacy fill sources observed (expected: none). |
| expiry/shutdown zero public exposure | `not_run` | — | Public/API live commitment exposure after shutdown and expiry grace; orphan process scan result. |
| restart/cold-start safety | `not_run` | — | State whether the probe was read-only/dry-run and whether it proves cursor resume or only no-phantom-exposure. |
| postgame lifecycle | `not_run` | — | External final score source and result, score/settle/claim transactions, final dry-run and process checks. Use `deferred` when the artifact is cut before the game is final. |
