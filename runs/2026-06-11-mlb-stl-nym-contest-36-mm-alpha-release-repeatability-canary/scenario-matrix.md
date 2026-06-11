# Scenario matrix

- **pass** — release-tag clone/install/build/smoke/typecheck/lint/test (`raw/release-runtime-matrix.sanitized.json`)
- **pass** — wallet auth/balance/allowance preflight (`raw/wallet-auth-balance-allowances.sanitized.json`)
- **pass** — 12:10 CDT target creation and moneyline seed/open (`raw/setup-seed.sanitized.json`)
- **pass** — dry-run quote and bounded dry-run loop (`raw/mm-dryrun-summary.sanitized.json`; one dry-run degraded telemetry event, errors `0`, live writes `0`)
- **pass** — tagged MM live quote and controlled tiny fill (`raw/live-fill.sanitized.json`)
- **pass** — own-state SSE canonical fill source (`raw/own-state-sse-summary.sanitized.json`)
- **pass** — shutdown/expiry/zero public exposure (`raw/zero-exposure.sanitized.json`)
- **pass_with_expected_timeout** — restart/cold-start read-only probe (`raw/restart-cold-start-probe.sanitized.json`)
- **pass_with_caveats** — postgame score/settle/claim (`raw/postgame-continuation.sanitized.json`)
