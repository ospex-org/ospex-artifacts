# MM live canary evidence: scenario matrix, MVE readiness scorecard, and verdict vocabulary

Market-maker live canary runs publish two standardized companion files next to `evidence.json`:

- `scenario-matrix.json` (+ `scenario-matrix.md` render) — what happened in this run, scenario by scenario.
- `mve-scorecard.json` (+ `mve-scorecard.md` render) — what this run proves toward MVE (minimum viable ecosystem) readiness: for each standard capability, whether the run proved it live, proved it only through synthetic/controlled action, deferred it, or observed it fail.

Copyable starting points live in `templates/mm-live-canary/`. Both JSON files are schema-backed (`schemas/scenario-matrix.schema.json`, `schemas/mve-scorecard.schema.json`) and validated by `python3 scripts/validate-artifacts.py`.

## Adoption and grandfathering

These contracts are opt-in per run. The validator enforces them when a run directory contains `mve-scorecard.json`, or a `scenario-matrix.json` declaring `schemaVersion` ≥ 2. The two adoptions are paired: a scorecard requires a v2 matrix in the same run directory and vice versa. Scenario matrices published before this scheme keep their original free-form shapes and are not re-validated against it.

## Scenario matrix (`schemaVersion` ≥ 2)

One row per scenario exercised (or intentionally skipped) in the run:

| Field | Meaning |
|---|---|
| `id` | Stable kebab-case identifier, unique within the matrix. |
| `scenario` | Human-readable label. |
| `status` | `pass`, `pass_with_caveats`, `fail`, `deferred`, `not_run`, or `not_applicable`. |
| `evidence` | Path to the sanitized evidence file, relative to the artifact directory. Required for `pass`, `pass_with_caveats`, and `fail`. |
| `notes` | Factual, test-scoped notes. Team references follow the Team Identity Rule: actual team name plus home/away role. |

Scenario `status` values are row-local, like other gate-level statuses; artifact-level `status` keeps its own controlled vocabulary (`docs/artifact-types.md`). Scenario rows are free-form per run; the standardized cross-run axis is the scorecard's capability list below.

## MVE readiness scorecard

The scorecard makes runs comparable over time. Every `mm-live-canary` scorecard carries all fourteen standard capability rows:

| Capability id | What `proven_live` means here |
|---|---|
| `target-preflight` | An intended target contest/speculation was selected and its verification state confirmed. |
| `repo-runtime-gates` | Fresh clone/release install, build, and smoke gates passed; versions recorded. |
| `wallet-auth-balances` | Strict non-interactive auth succeeded for each wallet role with sufficient balances. |
| `bounded-approvals` | Only bounded low-value allowances were observed or created. |
| `dry-run-quote-loop` | Doctor/quote/dry-run loop selected only the intended target and produced quote intents without writes. |
| `live-commitments-posted` | The MM posted live public commitments on the intended target during the window. |
| `live-fill` | A live-posted commitment was filled on-chain during the window (organic or controlled taker). |
| `own-state-sse-canonical-fill` | Telemetry recorded the fill source as the own-state stream with no canonical legacy fill sources. |
| `exposure-drain-zero` | Public/API live commitment exposure reached zero at end of run with no orphan process. |
| `restart-cold-start-safety` | A restart or cold-start probe ran without creating phantom public exposure; notes state whether it proves cursor resume. |
| `postgame-score` | The contest was scored against a verified external final score. |
| `postgame-settle` | The speculation settled to the winning side. |
| `postgame-claim` | Winning controlled positions were claimed, or a no-op was proven via empty claim-all dry-runs for every controlled wallet. |
| `cost-within-cap` | Total controlled spend and gas stayed within the run cap. |

Proof levels:

- `proven_live` — demonstrated by real on-chain/API behavior during this run.
- `proven_synthetic_only` — demonstrated only through seeded, staged, or dry-run action; not yet by organic live behavior.
- `deferred` — intentionally left unproven in this run (for example postgame steps when the artifact is cut before the game is final, or a fill that never arrived).
- `failed` — attempted and observed to fail. Requires evidence.
- `not_applicable` — the capability does not apply to this run variant.

`exposure-drain-zero` must be `proven_live` in every published scorecard regardless of verdict: ending a canary with zero public exposure is the invariant that makes tiny live canaries safe to repeat.

## Verdict vocabulary

`verdict.label` is controlled. Exactly one label per run:

- **`FULL_GREEN`** — the live window and the postgame lifecycle both completed. Core capabilities (`live-commitments-posted`, `live-fill`, `exposure-drain-zero`, `cost-within-cap`, and the three `postgame-*` rows) are proven, no capability is `failed`, and the transactions include settle plus score evidence. Artifact status: `complete_verified` or `complete_verified_with_caveats`.
- **`GREEN_LIVE_WINDOW_POSTGAME_DEFERRED`** — the live window completed green but the artifact was cut before the game was final, so scoring, settlement, and claims are deferred. All three `postgame-*` capabilities are `deferred`, no capability is `failed`, and no postgame transaction categories appear. Artifact status: `partial`. When postgame later completes, the artifact is updated (or superseded by a fuller one) and the verdict becomes `FULL_GREEN`.
- **`AMBER_QUOTED_NO_FILL`** — the MM posted live commitments but no fill occurred in the window. `live-commitments-posted` is proven; `live-fill` is `deferred` (or `failed` with evidence). Artifact status: `partial` or `complete_verified_with_caveats`.
- **`AMBER_TOKEN_TOPUP_NEEDED`** — the run was limited or stopped early by a funding shortfall (gas token, USDC balance, or allowance) and needs a top-up before a rerun. At least one capability is `deferred` or `failed`. Artifact status: `partial` or `complete_verified_with_caveats`.
- **`RED_SAFETY_HALT`** — a safety mechanism halted the run (for example unintended target selection, exposure beyond bounds, or an orphan process). This label exists so internal and operational tooling shares one vocabulary, but it is **not publishable in this repository**: the `run` artifact status vocabulary has no failure status, and the validator rejects any published scorecard carrying it. Halted/failed canary evidence stays internal; the underlying issue is tracked and fixed in the relevant code repository.

A `superseded` artifact keeps its original scorecard verdict; the status-mapping checks accept `superseded` for any verdict.

`GREEN_LIVE_WINDOW_POSTGAME_DEFERRED` and `FULL_GREEN` are deliberately distinct claims. A live-window artifact must not state or imply a completed lifecycle: deferral is recorded as `deferred` postgame rows, a `partial` artifact status, and the absence of postgame transaction categories, all of which the validator cross-checks.

## Transaction categories

Every on-chain transaction the run relies on appears in the scorecard's `transactions` array with a controlled `category`:

`approve`, `create-contest`, `seed-match`, `match-commitment`, `cancel-commitment`, `nonce-floor-raise`, `score-request`, `score-callback`, `settle`, `claim`, `other`.

Rules the validator enforces:

- `txHash` is a 0x-prefixed 32-byte hash; `status` is `success` or `reverted`; `operatorControlled` is boolean.
- `score-callback` entries must have `operatorControlled: false` — the oracle network sends the callback, and its gas is lifecycle evidence rather than controlled-operator spend.
- The same hash may appear under two categories only when one transaction genuinely performs both actions; exact duplicates are rejected.
- Category presence must match the verdict (no postgame categories under `GREEN_LIVE_WINDOW_POSTGAME_DEFERRED`; settle plus score evidence under `FULL_GREEN`).

Free-form context (which wallet role, which position) belongs in `purpose`.

## Moneyline team identity

When an adopting run's `evidence.json` records `target.market` as `moneyline`, `target.teamIdentity` is required with `home` and `away` entries:

```json
"teamIdentity": {
  "home": { "team": "…", "positionType": "lower", "marketOddsAmerican": "-120", "identity": "favorite" },
  "away": { "team": "…", "positionType": "upper", "marketOddsAmerican": "+120", "identity": "underdog" }
}
```

The validator enforces the protocol mapping (`home` = `lower`, `away` = `upper`), distinct team names, market odds on both sides, and a coherent identity pairing (`favorite`/`underdog`, or `even`/`even` for a pick'em). This keeps the Team Identity Rule machine-checkable: abstract side labels never appear without the actual team names.

## Zero-exposure block

The scorecard's `zeroExposure` object records the end-of-run public exposure check: `publicMakerVisibleCommitments`, `publicContestSpecVisibleCommitments`, `contestOrderbookCount`, and `orphanProcessCount` must all be the integer `0`, with `checkedAtUtc` and an `evidence` path to the sanitized snapshot. A filled position held for postgame settlement is position exposure, not live commitment exposure, and does not belong in these counts.

## Cross-file consistency

For adopting runs the validator also checks `evidence.json`:

- `artifactFiles` references both `scenario-matrix.json` and `mve-scorecard.json`.
- The artifact-level `status` matches the verdict mapping above.
- If `evidence.json` carries a `verdict.label`, it equals the scorecard's label exactly.
