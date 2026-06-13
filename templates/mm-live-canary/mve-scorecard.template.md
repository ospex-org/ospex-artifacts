# MVE readiness scorecard

Render of `mve-scorecard.json`; the JSON file is canonical. Verdict labels, proof levels, and transaction categories are controlled vocabularies defined in `docs/mm-live-canary-evidence.md`. This template defaults to a live-window-green / postgame-deferred run; if the run differs, change the verdict and the proof levels together.

## Verdict

**`GREEN_LIVE_WINDOW_POSTGAME_DEFERRED`** — one-paragraph factual verdict reason derived from the evidence.

## Capabilities

| Capability | Proof | Evidence | Notes |
|---|---|---|---|
| Target selection and contest verification | `proven_live` | `raw/target-decision.sanitized.json` | … |
| Fresh clone/release install, build, and smoke gates | `proven_live` | `raw/release-runtime-matrix.sanitized.json` | … |
| Non-interactive wallet auth and balance sufficiency | `proven_live` | `raw/wallet-auth-balance-allowances.sanitized.json` | … |
| Bounded low-value allowances only | `proven_live` | `raw/wallet-auth-balance-allowances.sanitized.json` | … |
| Doctor/quote/dry-run loop on the intended target only | `proven_synthetic_only` | `raw/mm-dryrun-summary.sanitized.json` | Dry-run, no writes → synthetic-only. |
| Live commitments posted on the intended target | `proven_live` | `raw/live-public-commitments-posted.sanitized.json` | … |
| Live fill against a posted commitment | `proven_live` | `raw/live-fill.sanitized.json` | If no fill, switch verdict to `AMBER_QUOTED_NO_FILL` and set this `deferred`/`failed`. |
| Fill detection sourced canonically from own-state SSE | `proven_live` | `raw/own-state-sse-summary.sanitized.json` | … |
| Public/API live exposure drained to zero at end of run | `proven_live` | `raw/zero-exposure.sanitized.json` | Must be `proven_live` in every published canary. |
| Restart/cold-start safety without phantom exposure | `proven_synthetic_only` | `raw/restart-cold-start-probe.sanitized.json` | Read-only/dry-run probe → synthetic-only. |
| Contest scored against a verified external final score | `deferred` | — | `proven_live` (with evidence) + verdict `FULL_GREEN` once postgame completes. |
| Speculation settled to the winning side | `deferred` | — | … |
| Winning positions claimed or no-op proven via empty dry-runs | `deferred` | — | … |
| Total controlled spend and gas within the run cap | `proven_live` | `raw/tx-receipts.summary.json` | … |

## Zero exposure

Checked at `YYYY-MM-DDTHH:MM:SSZ` (`raw/zero-exposure.sanitized.json`): public maker-visible commitments `0`, public contest/spec-visible commitments `0`, contest orderbook count `0`, orphan processes `0`.

## Transactions

| Category | Tx hash | Status | Operator-controlled | Purpose |
|---|---|---|---|---|
| `approve` | `0x…` | `success` | yes | … |
| `match-commitment` | `0x…` | `success` | yes | … |
