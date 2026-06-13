# MVE readiness scorecard

Render of `mve-scorecard.json`; the JSON file is canonical. Verdict labels, proof levels, and transaction categories are controlled vocabularies defined in `docs/mm-live-canary-evidence.md`.

## Verdict

**`GREEN_LIVE_WINDOW_POSTGAME_DEFERRED`** — one-paragraph factual verdict reason derived from the evidence.

## Capabilities

| Capability | Proof | Evidence | Notes |
|---|---|---|---|
| Target selection and contest verification | `deferred` | — | … |
| Fresh clone/release install, build, and smoke gates | `deferred` | — | … |
| Non-interactive wallet auth and balance sufficiency | `deferred` | — | … |
| Bounded low-value allowances only | `deferred` | — | … |
| Doctor/quote/dry-run loop on the intended target only | `deferred` | — | … |
| Live commitments posted on the intended target | `deferred` | — | … |
| Live fill against a posted commitment | `deferred` | — | … |
| Fill detection sourced canonically from own-state SSE | `deferred` | — | … |
| Public/API live exposure drained to zero at end of run | `deferred` | — | Must be `proven_live` in every published canary. |
| Restart/cold-start safety without phantom exposure | `deferred` | — | … |
| Contest scored against a verified external final score | `deferred` | — | … |
| Speculation settled to the winning side | `deferred` | — | … |
| Winning positions claimed or no-op proven via empty dry-runs | `deferred` | — | … |
| Total controlled spend and gas within the run cap | `deferred` | — | … |

## Zero exposure

Checked at `YYYY-MM-DDTHH:MM:SSZ` (`raw/zero-exposure.sanitized.json`): public maker-visible commitments `0`, public contest/spec-visible commitments `0`, contest orderbook count `0`, orphan processes `0`.

## Transactions

| Category | Tx hash | Status | Operator-controlled | Purpose |
|---|---|---|---|---|
| `approve` | `0x…` | `success` | yes | … |
| `match-commitment` | `0x…` | `success` | yes | … |
