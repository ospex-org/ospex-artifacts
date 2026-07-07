# MM live canary evidence: scenario matrix, MVE readiness scorecard, and verdict vocabulary

Every new market-maker live canary run is expected to publish two standardized companion files next to `evidence.json` (enforcement is adoption-triggered per run — see "Adoption and grandfathering" — so pre-scheme artifacts are unaffected):

- `scenario-matrix.json` (+ `scenario-matrix.md` render) — what happened in this run, scenario by scenario.
- `mve-scorecard.json` (+ `mve-scorecard.md` render) — what this run proves toward MVE (minimum viable ecosystem) readiness: for each standard capability, whether the run proved it live, proved it only through synthetic/controlled action, deferred it, or observed it fail.

Copyable starting points live in `templates/mm-live-canary/`. Both JSON files are schema-backed (`schemas/scenario-matrix.schema.json`, `schemas/mve-scorecard.schema.json`) and validated by `python3 scripts/validate-artifacts.py`.

## Adoption and grandfathering

These contracts are opt-in per run. The validator enforces them when a run directory contains `mve-scorecard.json`, or a `scenario-matrix.json` that declares adoption (a `$schema` pointer, or a `schemaVersion` of 2 or higher — it must be a plain integer; near-miss declarations such as `"2"` or `2.0` are rejected loudly rather than skipped). Scenario matrices published before this scheme keep their original free-form shapes and are not re-validated against it.

`runClass` is a closed registry, currently `mm-live-canary` only. A future run class is added to the registry in the validator together with its own pairing and capability rules; an unregistered or misspelled `runClass` is rejected rather than silently skipping checks.

The two adoptions are paired: a scorecard requires a v2 matrix in the same run directory; a v2 matrix declaring `runClass` `mm-live-canary` requires a scorecard; and when both files are present their `runClass` values must match. A scenario row and a capability row that share an id describe the same thing, so their outcome class must agree: `pass`/`pass_with_caveats` and `proven_live`/`proven_synthetic_only` are *proven*; `fail` and `failed` are *failed*; `deferred`/`not_run`/`not_applicable` (matrix) and `deferred`/`not_applicable` (scorecard) are *absent*. Any cross-class pairing — proven vs failed, proven vs absent, failed vs absent — is rejected, so the matrix cannot say "passed" while the scorecard says "deferred" (or vice versa). The schema pointers are also placement-checked: a file carrying one of these `$schema` ids must be named `scenario-matrix.json` / `mve-scorecard.json` inside a `runs/` artifact directory (templates under `templates/` are exempt), so a misnamed file cannot dodge validation while advertising the schema.

An adopting run covers exactly one target contest/speculation. A multi-contest canary publishes one adopting run directory per contest — the verdict vocabulary, postgame capability rows, and transaction-category cross-checks are all defined per single target. (The legacy three-game shakeout run predates this scheme and stays grandfathered.)

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

`exposure-drain-zero` must be `proven_live` in every published scorecard regardless of verdict: ending a canary with zero public exposure is the invariant that makes tiny live canaries safe to repeat. The live-window rows (`live-commitments-posted`, `live-fill`) likewise accept only `proven_live` under any verdict that claims them — a live canary's headline claim is live behavior, so `proven_synthetic_only` there forces an amber verdict or a `deferred` row. Under `FULL_GREEN` the three `postgame-*` rows must also be `proven_live`: a completed postgame lifecycle is real on-chain behavior, never synthetic.

`evidence` paths in scenario rows, capability rows, and the zero-exposure block must point at a sanitized raw evidence file — not a directory, and not the artifact's own companion files (`evidence.json`, the matrix/scorecard files, or `summary.md`), which would be circular.

## Verdict vocabulary

`verdict.label` is controlled. Exactly one label per run:

- **`FULL_GREEN`** — the live window and the postgame lifecycle both completed. Core capabilities (`live-commitments-posted`, `live-fill`, `exposure-drain-zero`, `cost-within-cap`, and the three `postgame-*` rows) are proven, no capability is `failed`, and the transactions include a successful settle plus successful score evidence. Artifact status: `complete_verified` or `complete_verified_with_caveats`.
- **`GREEN_LIVE_WINDOW_POSTGAME_DEFERRED`** — the live window completed green but the artifact was cut before the game was final, so scoring, settlement, and claims are deferred. All three `postgame-*` capabilities are `deferred`, no capability is `failed`, and no successful postgame transaction categories appear (a reverted postgame attempt — for example an early scoring attempt that reverted because the game was not final — may and should be disclosed). Artifact status: `partial`. When postgame later completes, the artifact is updated (or superseded by a fuller one) and the verdict becomes `FULL_GREEN`.
- **`AMBER_PRELIVE_GATE_HALT`** — setup and/or dry-run gates exercised the target safely, but the pre-live safety gate stopped the live write before any live public commitments were posted (for example an intended market stopped producing quote-ready/would-submit rows near first pitch). `live-commitments-posted` and `live-fill` are `failed` or `deferred`; `exposure-drain-zero` remains `proven_live`; postgame rows may still be `proven_live` if the already-created/manual-seeded target lifecycle completed. Artifact status: `partial` or `complete_verified_with_caveats`.
- **`AMBER_QUOTED_NO_FILL`** — the MM posted live commitments but no fill occurred in the window. `live-commitments-posted` is `proven_live`; `live-fill` is `deferred` (or `failed` with evidence); the fill-telemetry row `own-state-sse-canonical-fill` is `deferred`, `failed`, or `not_applicable` (a proven canonical fill would imply a fill occurred); and no successful fill transaction (`match-commitment` or `seed-match`) appears — both record a matched position. Artifact status: `partial` or `complete_verified_with_caveats`.
- **`AMBER_TOKEN_TOPUP_NEEDED`** — the run was limited or stopped early by a funding shortfall (gas token, USDC balance, or allowance) and needs a top-up before a rerun. At least one capability is `deferred` or `failed`. Artifact status: `partial` or `complete_verified_with_caveats`.

`GREEN_LIVE_WINDOW_POSTGAME_DEFERRED` explicitly asserts deferral, so it may not carry a *successful* postgame transaction category (`score-request`, `score-callback`, `settle`, `claim`) — only `FULL_GREEN` does. The AMBER labels assert only "no fill" / "needs top-up" and make no claim about postgame (settling a speculation is contest-level, independent of whether the MM filled), so they are not constrained on postgame transactions; a disclosed *reverted* attempt is always allowed.
- **`RED_SAFETY_HALT`** — a safety mechanism halted the run (for example unintended target selection, exposure beyond bounds, or an orphan process). This label exists so internal and operational tooling shares one vocabulary, but it is **not publishable in this repository**: the `run` artifact status vocabulary has no failure status, and the validator rejects any published scorecard carrying it. Halted/failed canary evidence stays internal; the underlying issue is tracked and fixed in the relevant code repository.

A `superseded` artifact keeps its original scorecard verdict; the status-mapping checks accept `superseded` for any verdict, but the evidence must then carry a `supersededBy` pointer — `runs/<artifact-id>/evidence.json` of another run, which must exist — so supersession is anchored rather than asserted. (`RED_SAFETY_HALT` is deliberately absent from the published schema's enum for the same reason it is rejected here.)

`GREEN_LIVE_WINDOW_POSTGAME_DEFERRED` and `FULL_GREEN` are deliberately distinct claims. A live-window artifact must not state or imply a completed lifecycle: deferral is recorded as `deferred` postgame rows, a `partial` artifact status, and the absence of successful postgame transaction categories, all of which the validator cross-checks.

## Transaction categories

Every on-chain transaction the run relies on appears in the scorecard's `transactions` array with a controlled `category`:

`approve`, `create-contest`, `seed-match`, `match-commitment`, `cancel-commitment`, `nonce-floor-raise`, `score-request`, `score-callback`, `settle`, `claim`, `other`.

Rules the validator enforces:

- `txHash` is a 0x-prefixed 32-byte hash; `status` is `success` or `reverted`; `operatorControlled` is boolean.
- `score-callback` entries must have `operatorControlled: false` — the oracle network sends the callback, and its gas is lifecycle evidence rather than controlled-operator spend.
- Exact duplicate entries — the same `txHash` under the same `category` (hash compared case-insensitively) — are rejected.
- `seed-match` records a matched position (a controlled `MatchingModule.matchCommitment`); R4 has no on-chain no-counterparty seed, so a successful `seed-match` or `match-commitment` is a fill.
- Successful-category presence must match the verdict and the capability rows: no successful postgame categories (`score-request`, `score-callback`, `settle`, `claim`) under `GREEN_LIVE_WINDOW_POSTGAME_DEFERRED`; no successful fill (`match-commitment`/`seed-match`) under `AMBER_QUOTED_NO_FILL`; a successful settle plus successful score evidence under `FULL_GREEN`; and a successful fill (`match-commitment`/`seed-match`) whenever the `live-fill` capability is `proven_live` (a proven on-chain fill must be backed by its transaction). Reverted entries never count toward (or against) these checks, so disclosed failed attempts do not block an honest verdict.

Free-form context (which wallet role, which position) belongs in `purpose`. The validator permits the same hash to appear under two different categories but does not verify the reuse; authors must only dual-categorize a hash when one transaction genuinely performs both actions.

## Moneyline team identity

`target.market` is a closed vocabulary — exactly `moneyline`, `spread`, or `total` (the protocol's scorer modules). The moneyline team-identity requirement keys off the normalized value, so a non-canonical spelling (`Moneyline`, `moneyline `) is both rejected as a market value and still required to carry `teamIdentity` — it cannot be used to slip past the rule.

When an adopting run's `evidence.json` records `target.market` as `moneyline`, `target.teamIdentity` is required with `home` and `away` entries. It is keyed by **role** (`home`/`away`), each entry carrying its own `identity` field — deliberately not the older `homeFavorite`/`awayUnderdog` shape some pre-scheme artifacts use, which breaks for pick'ems and for games where the away team is the favorite. (The validator gives a clear migration error if the legacy shape appears.)

```json
"teamIdentity": {
  "home": { "team": "…", "positionType": "lower", "marketOddsAmerican": "-120", "identity": "favorite" },
  "away": { "team": "…", "positionType": "upper", "marketOddsAmerican": "+120", "identity": "underdog" }
}
```

The validator enforces the protocol mapping (`home` = `lower`, `away` = `upper`), distinct team names, and a coherent identity pairing (`favorite`/`underdog`, or `even`/`even` for a pick'em). `marketOddsAmerican` must be signed American odds with magnitude ≥ 100, and the sign must agree with the identity: favorites carry negative odds, underdogs positive. An `even`/`even` pick'em is judged by symmetry rather than an exact price — the two sides' implied probabilities must be close — so a normally-vigged pick'em (`-110`/`-110`, `-105`/`-115`) is accepted while a lopsided line mislabeled `even` is rejected. This keeps the Team Identity Rule machine-checkable: abstract side labels never appear without the actual team names, and a sign swap — the classic side-confusion failure — is rejected.

## Zero-exposure block

The scorecard's `zeroExposure` object records the end-of-run public exposure check: `publicMakerVisibleCommitments`, `publicContestSpecVisibleCommitments`, `contestOrderbookCount`, and `orphanProcessCount` must all be the integer `0`, with `checkedAtUtc` and an `evidence` path to the sanitized snapshot. A filled position held for postgame settlement is position exposure, not live commitment exposure, and does not belong in these counts.

## Cross-file consistency

For adopting runs the validator also checks `evidence.json`:

- `artifactType` is `run`.
- `artifactFiles` references both `scenario-matrix.json` and `mve-scorecard.json`, and every other referenced path exists.
- The artifact-level `status` matches the verdict mapping above; `superseded` additionally requires the `supersededBy` pointer.
- If `evidence.json` carries a `verdict.label`, it equals the scorecard's label exactly.
- `target` is required and names the single contest/speculation concretely: non-empty `market` (one of `moneyline`/`spread`/`total`), `sport`, decimal `contestId`, decimal `speculationId`, `homeTeam`, and `awayTeam` (distinct). For moneyline targets, `teamIdentity.home.team` and `teamIdentity.away.team` must equal `target.homeTeam` / `target.awayTeam`, so the identity block cannot quietly swap sides.

## Canonical target binding

The core invariant for an adopting `mm-live-canary` run: **the public `evidence.json.target` must be the same target proven by the artifact's canonical raw evidence.** A run must not pass validation while claiming a contest, speculation, sport, team, or market that its own cited evidence does not show. Three checks enforce this, all **fail-closed** (a missing or unparseable input is an error, never a silent skip):

1. **Run-directory binding.** The run directory name must parse as `runs/YYYY-MM-DD-<sport>-…-contest-<contestId>-…/`. If the `-contest-<id>` segment or the `YYYY-MM-DD-<sport>-` prefix is absent, the run is rejected — a directory like `2026-06-08-mlb-sf-chc-…-canary` (no `-contest-<id>`) cannot be an adopting canary. `target.contestId` must equal the parsed contest id and `target.sport` the parsed sport.

2. **Target-preflight binding.** The `target-preflight` capability must cite an evidence file (normally `raw/target-decision.sanitized.json`). The validator loads it and requires `selectedTarget.{contestId, sport, homeTeam, awayTeam}` to be **present** and to equal the public target, plus a `selectedTarget.speculations[]` entry whose `speculationId`, `contestId`, and `type` match `target.speculationId`, `target.contestId`, and `target.market`. Missing file, non-file, missing `selectedTarget`, a missing required `selectedTarget` field, or no matching speculation → error.

3. **Live-fill binding.** When `live-fill` is `proven_live` (or any successful `match-commitment`/`seed-match` transaction is present), the `live-fill` capability must cite fill evidence (normally `raw/live-fill.sanitized.json`) whose `result.contest.{contestId, sport, homeTeam, awayTeam}` and `result.speculation.speculationId` are **present** and equal the public target; `result.commitment.contestId`/`marketType`, when present, must also match. Missing/non-file/mismatched, or a missing required `result.contest`/`result.speculation` field → error.

Matching is **exact**. A missing required raw field is fail-closed (it is an error, never skipped). Public `target.contestId`/`target.speculationId` must match `^\d+$` directly — no surrounding whitespace — and `target.homeTeam`/`target.awayTeam` must equal the raw team strings with no trim normalization. Raw numeric ids may be JSON numbers or strings (compared via `str()`); only `sport` and `market` are compared case-insensitively. This is cross-file identity consistency for the documented machine-checkable fields, not a general truth oracle — the one residual gap is free text the raw evidence does not contain at all (e.g. a team name nowhere in the cited capture); every field the raw evidence carries is bound exactly.
