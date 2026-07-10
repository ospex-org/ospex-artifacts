# Ospex late two-game harness stress test — 2026-07-08

Created for Vince at ~2026-07-08 20:05 ET.

This is **not** primarily an MVE green/volume test. This is a deliberately aggressive **operator harness stress test** using the two late MLB games as a real-time clock and real live quote surface. We want to break the harness tonight, while there is time to fix it, instead of discovering the same failure tomorrow minutes before first pitch.

## Current context

Recent failures were harness/operator failures, not protocol failures:

- Block F: live runner used fixed controlled-fill risk and preview correctly refused before tx.
- Block I: prelive dry gate treated `wouldSubmit < theoretical max` as fatal even though the missing rows were benign per-market `reference-line-mismatch` totals.

The exact Block I failure evidence to replay is here:

```text
<local-home>/.ospex/runs/20260708T181153Z-mve-phase1-block-i-evening-6game-expanded/sanitized/live-run-error.json
<local-home>/.ospex/runs/20260708T181153Z-mve-phase1-block-i-evening-6game-expanded/logs/mm-p1-prelive-dry-telemetry/run-2026-07-08T22-06-03-244Z-ncuwnw.ndjson
```

The Ospex/MM runbook has been patched with the rule we now need to prove:

```text
reference-line-mismatch is a benign per-market skip unless the test objective explicitly requires that moved market.
Do not convert two stale totals into a whole-block live halt.
```

## Target late games

Validate these again before writes. At file creation, MLB Stats showed both still `Pre-Game`, and Ospex local game-list evidence showed both `upcoming`/`hasOdds=true` earlier.

A — Colorado Rockies @ Los Angeles Dodgers

```text
scheduled: 2026-07-08 22:10 ET / 2026-07-09T02:10:00Z
Ospex gameId/jsonodds: b14eb3ed-8fe1-41bd-9edb-21c8b7c94fc0
MLB Stats gamePk: 823928
slug: col-lad-2026-07-09
```

B — Arizona Diamondbacks @ San Diego Padres

```text
scheduled: 2026-07-08 22:10 ET / 2026-07-09T02:10:00Z
Ospex gameId/jsonodds: 9c3489da-5456-45d4-af52-838f857f82f9
MLB Stats gamePk: 823279
slug: ari-sd-2026-07-09
```

Ignore LAA/TEX unless Vince explicitly reopens it; it was already `Warmup` at ~20:05 ET and is not part of this test.

## Run identity

Use a fresh run dir. Suggested:

```text
<local-home>/.ospex/runs/<timestamp>-mve-phase1-block-j-late-two-game-harness-stress
```

Suggested verdict labels:

```text
MVE_PHASE1_BLOCK_J_HARNESS_STRESS_GREEN
MVE_PHASE1_BLOCK_J_HARNESS_STRESS_GREEN_WITH_CAVEATS
MVE_PHASE1_BLOCK_J_HARNESS_STRESS_AMBER
MVE_PHASE1_BLOCK_J_HARNESS_STRESS_FAIL
```

This should not be published as a normal MVE green unless the artifact clearly explains this was a harness-stress drill. If live/postgame evidence is partial, publish facts-only amber/caveat evidence or keep local evidence until postgame.

## Hard safety limits

Read-only/replay phases first. Live writes only after self-tests pass.

Capital/risk:

```text
additional crypto required: expected NO
per quote live risk target: 0.005–0.050 USDC
controlled fills: max 1 per contest, optional if harness already sufficiently exercised
fees + controlled risk target: <= 15 USDC
hard stop and ask Vince if projected > 25 USDC
no unlimited approvals
bounded approvals only
no broad-slate writes
strict contest allowlist only
```

Stop immediately for:

```text
off-allowlist rows
broad-slate behavior
seedSpeculations unexpectedly enabled in the non-seeding live profile
wrong game identity
ambiguous side/line identity
unresolved own-state hold
unknown-own-fill
owner-mapping-failed
divergence
actual tx revert
unsafe residual open commitments
funding/allowance issue that cannot be bounded
raw JSON as the primary Slack alert from a no-agent job
```

Do **not** stop the entire test solely for:

```text
reference-line-mismatch for one market
no-reference-odds for one market
cap-hit / quote-count cap in an intentional cap-stress dry run
preview-stage match-size refusal where no tx was sent
one contest/market unavailable while other healthy allowlisted targets remain
```

## Timeline discipline

At start, report to Slack in human prose:

```text
setup start time ET/UTC
first pitch time
planned live runner time
latest safe retry time
hard stop time
whether extra crypto is needed
what fallback path will be used if primary live fails
```

Suggested timing if starting around 20:05–20:15 ET:

```text
20:05–20:25 ET  self-tests/replay harness only, no writes
20:25–20:55 ET  create/verify contests, update markets, create specs if needed
20:55–21:20 ET  dry-run/candidates/cap/mismatch harness stress
21:20–21:35 ET  render live manifest and live runner, run final replay
21:35–21:45 ET  primary prelive dry gate
21:45 ET        primary live harness run
21:55 ET        salvage/retry live run if needed
22:03 ET        latest safe retry start
22:05 ET        hard stop for new live starts
22:10 ET        first pitch
```

If current time is already after 21:30 ET when reading this, reduce scope. Do not cram everything in. Prefer replay + dry-run + one controlled live quote cycle over a rushed all-market mess.

## Required phases

### Phase 0 — environment / non-secret setup

1. Source operator env without logging secrets.
2. Record UTC and ET time.
3. Record repo heads:
   - `ospex-sdk`
   - `ospex-market-maker`
   - `ospex-core-api`
   - `ospex-indexer`
   - `ospex-contracts-v2`
   - `ospex-artifacts`
4. Record SDK/CLI version and MM internal `@ospex/sdk` version.
5. Check API `/healthz` and `/readyz`.
6. Check wallet balances/allowances for stage-maker-a, stage-maker-b, flow-a, fresh-user. Do not ask for more crypto unless the forecast proves it is needed.
7. Save all raw outputs under `raw/` and sanitized summaries under `sanitized/`.

### Phase 1 — pure harness self-tests, no chain writes

Before touching live games, write or patch a small local harness classifier in the run dir, e.g.:

```text
scripts/harness_gate_selftest.py
```

It must classify telemetry into:

```text
healthyTargets
benignSkips
fatalEvents
recommendedAction = GO | GO_WITH_CAVEATS | SALVAGE | STOP
```

At minimum it must pass these cases:

#### Self-test A — replay Block I p1

Input:

```text
<local-home>/.ospex/runs/20260708T181153Z-mve-phase1-block-i-evening-6game-expanded/logs/mm-p1-prelive-dry-telemetry/run-2026-07-08T22-06-03-244Z-ncuwnw.ndjson
```

Expected classification:

```text
recommendedAction: GO_WITH_CAVEATS
wouldSubmit: 14
benignSkips:
  - contest 29 total reference-line-mismatch
  - contest 31 total reference-line-mismatch
fatalEvents: []
```

This exact evidence killed Block I. The new harness must prove it would NOT kill it.

#### Self-test B — synthetic fatal off-allowlist

Create a tiny NDJSON fixture with one `would-submit` or `candidate` outside the configured contest allowlist.

Expected:

```text
recommendedAction: STOP
fatalEvents includes off-allowlist
```

#### Self-test C — synthetic preview-too-large branch

Create a small JSON fixture shaped like the Block F preview refusal:

```text
Match would revert: fillMakerRisk=111100 not in (0, remaining=100000]
```

Expected:

```text
recommendedAction: REDUCE_SIZE_AND_RETRY
no tx sent: true
fatalEvents: []
```

#### Self-test D — time-window safety

Mock a current time after latest safe retry but before first pitch.

Expected:

```text
recommendedAction: POSTGAME_ONLY_OR_ABORT_LIVE
no new live writes
human message says why
```

#### Self-test E — human alert format

Simulate every non-green branch and assert the first Slack/no-agent line is human-readable and not raw escaped JSON.

Expected first line examples:

```text
⚠️ Block J harness continuing with caveats: 1 moved total skipped, 5 healthy markets remain.
❌ Block J harness stopped before tx: off-allowlist row detected. No tx sent. Open commitments check pending.
```

Not acceptable:

```text
{"ok":false,"phase":"live",...}
```

Do not proceed to live setup until these self-tests pass.

### Phase 2 — setup the two late games

Re-check live status from both sources:

- Ospex CLI/API games list
- MLB Stats API official schedule

Abort setup if a target game is no longer upcoming/safe.

For each target:

1. Create contest if absent.
2. Wait for R5/CRE verification.
3. Request market update.
4. Confirm odds for moneyline/spread/total where available.
5. Create/open specs for moneyline/spread/total if needed using manual seed/fill pattern, with microscopic risk.
6. Prove manual seed open commitments = 0.
7. Save `speculations-by-contest-market.json`.

Do not require all three markets if odds/specs are unavailable. This is a harness test. The key is that the harness reacts correctly.

### Phase 3 — dry-run stress matrix

Run several dry-run configurations, all strict allowlist.

#### Dry-run profile 1 — normal strict all-market

```text
markets: moneyline, spread, total
allowlist: exactly the two target contest IDs
seedSpeculations: false
maxTrackedMarkets: 6
maxOpenCommitments: enough for all healthy rows, e.g. 12+
```

Expected:

```text
GO or GO_WITH_CAVEATS
healthyTargets derived from actual would-submit rows
benign skips recorded per market
no all-or-nothing theoretical-count failure
```

#### Dry-run profile 2 — intentional cap pressure

Same allowlist, but intentionally set:

```text
maxOpenCommitments: 4 or 6
```

Expected:

```text
GO_WITH_CAVEATS or SALVAGE
cap-limited markets recorded
no full harness crash
no off-allowlist rows
```

This is to ensure the runner knows the difference between a **safe cap caveat** and a **fatal safety issue**.

#### Dry-run profile 3 — synthetic missing/moved market manifest

If the real live odds do not move enough to produce `reference-line-mismatch`, feed the classifier a synthetic or replay manifest where one target total is skipped for `reference-line-mismatch`.

Expected:

```text
GO_WITH_CAVEATS
only that market omitted from healthyTargets
```

#### Dry-run profile 4 — seed profile, read-only unless explicitly safe

Render a config with `seedSpeculations: true` and bounded `risk.maxDailyFeeUSDC`, but use dry-run only unless you explicitly state the creation-fee budget and Vince has approved.

Purpose:

```text
prove the harness can distinguish expected seeding behavior from unexpected seedSpeculations in the normal live profile
```

Expected:

```text
normal profile: seedSpeculations true would be fatal/unexpected
seed stress profile: seedSpeculations true is expected and fee-gated
```

### Phase 4 — live runner requirements

The live runner must be target-manifest driven.

Bad pattern:

```python
if len(would) < len(contests) * len(markets) * 2:
    fail()
```

Required pattern:

```text
prelive dry telemetry -> target manifest
live visible wait -> wait only for healthyTargets
fill selection -> prefer planned markets, but fall back to visible healthy alternatives
```

The manifest should look like:

```json
{
  "contestIds": ["...", "..."],
  "healthyTargets": [
    {"contestId":"...", "market":"moneyline", "sides":2},
    {"contestId":"...", "market":"spread", "sides":2}
  ],
  "benignSkips": [
    {"contestId":"...", "market":"total", "reason":"reference-line-mismatch"}
  ],
  "fatalEvents": [],
  "minimumCoverage": {
    "minContestsWithAnyVisibleQuote": 1,
    "minHealthyMarketsTotal": 2,
    "requireNoOffAllowlist": true
  }
}
```

### Phase 5 — live harness stress

Only start live if:

```text
current time < latest safe retry time
MLB/Ospex status still upcoming/safe
self-tests passed
prelive dry gate returns GO or GO_WITH_CAVEATS
no fatal events
```

Start one live MM instance for the two-contest allowlist.

Stress actions:

1. Wait for visible quotes for `healthyTargets` only.
2. Intentionally run one oversize `commitments match` preview against a selected quote with `ok={0,1}` handling.
   - Do **not** execute the oversize preview.
   - Verify no tx was sent.
   - Verify the runner records this as `REDUCE_SIZE_AND_RETRY`, not fatal.
3. Retry with a computed safe tiny risk.
4. Execute at most one tiny controlled fill per contest if preview is clean.
   - Use stage-maker-b or flow-a as taker; do not rely on same-wallet self-match semantics.
   - Risk target: 0.005–0.050 USDC.
5. If one contest or preferred market cannot be safely filled, skip it and continue the other.
6. Stop MM cleanly.
7. Soft-cancel/expire remaining visible quotes.
8. Prove open commitments = 0 for both contests.
9. Confirm no orphan MM process.

Optional chaos test if there is still time and safety is green:

```text
Start a second dry-run/scratch observation from copied config/state only.
Never point scratch dry-run at live state.dir.
Prove synthetic dry state does not confuse live open-commitment checks.
```

Do **not** deliberately run two live MM processes on the same maker wallet. That tests a dangerous condition we already know to avoid.

### Phase 6 — postgame watcher

Install a postgame watcher if any real manual seed/fill or controlled live fills occurred.

Use MLB Stats API official final, bound by `gamePk`:

```text
COL @ LAD: 823928
ARI @ SD: 823279
```

On official final:

1. Save official score source.
2. `score-status` each contest.
3. `score --wait` if unscored.
4. Settle every target speculation.
5. Claim target wallets.
6. Verify:
   - active = 0
   - pendingSettle = 0
   - claimable = 0
   - open commitments = 0
7. Pause/remove the watcher after success.

### Phase 7 — required final report

Report in Slack in human prose. Include:

```text
run dir
current verdict
self-test summary
which harness bugs were exercised
whether any tx was sent
contests/specs used
live quotes posted count
controlled fills count and risk
benign skips
fatal events
open commitment proof
orphan process proof
postgame watcher job id if installed
whether extra crypto was needed
whether raw JSON was avoided in Slack
```

Explicitly classify failures by class:

```text
harness-classifier failure
harness-live-runner failure
expected safe MM refusal
protocol/API/SDK failure
wallet/funding issue
operator timing issue
```

If the harness fails, that is a useful result. Preserve evidence and do not try to hide it behind a green label.

## Minimum success criteria

This harness stress test is useful if it proves at least all of the following:

```text
1. Block I p1 replay no longer fails all-or-nothing.
2. reference-line-mismatch becomes a per-market caveat.
3. preview-too-large becomes reduce-size-and-retry, not live-block fatal.
4. live runner waits on healthyTargets, not theoretical full market count.
5. controlled fill target selection can fall back by market/contest.
6. no-agent/Slack output is human-readable before raw details.
7. shutdown proves zero-open and no orphan process.
```

A green harness outcome with no actual fills is acceptable if the harness branches were really exercised and all live quotes were cleaned up. A tiny actual fill is better only if it does not distract from the harness objective.

## If time gets tight

Prioritize in this exact order:

```text
1. Block I replay classifier self-test.
2. Synthetic fatal/benign branch tests.
3. Two-game contest/spec setup only if safe.
4. Dry-run strict allowlist normal/cap-stress.
5. Live quote post + visible target manifest.
6. Optional tiny controlled fill.
7. Postgame watcher if any real fill occurred.
```

Do not skip the replay/classifier step to chase live action. The replay is the point of tonight.
