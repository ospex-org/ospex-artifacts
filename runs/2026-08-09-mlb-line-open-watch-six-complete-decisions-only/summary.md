# Sunday 8/9 MLB — decisions-only line-open watch, six scored outputs

## Result

- **Status:** `complete_verified_with_caveats`
- **Run label:** `SMOKE_V0_NOT_A_COHORT`
- **Target:** 15 Sunday games
- **Watcher completion:** `TARGET_LEDGER_COMPLETE` at `2026-08-09T13:39:30.675Z`

The watcher durably handled all 15 targets: **7 paid-fire claims, 6 complete decision artifacts, 1 interrupted fired claim preserved without replay, and 8 late detections that never fired**. The official source fetched at `2026-08-10T02:59:05Z` reports all 15 games final.

This was explicitly **decisions-only**. It created no contests, positions, commitments, fills, or transaction records. Protocol score requests, settlement, claims, allowance cleanup, and terminal-zero lifecycle checks were therefore **not applicable**; no Sunday protocol transaction needed to be sent.

## Slate reconciliation

| Game | Start UTC | Watch outcome | Final (away–home) |
|---|---|---|---:|
| Cincinnati Reds at Washington Nationals | 2026-08-09 16:15 | complete | 1–7 |
| Athletics at Boston Red Sox | 2026-08-09 17:35 | complete | 4–3 |
| Atlanta Braves at New York Yankees | 2026-08-09 17:35 | complete | 2–1 |
| New York Mets at Pittsburgh Pirates | 2026-08-09 17:35 | interrupted/no replay | 11–1 |
| Toronto Blue Jays at Philadelphia Phillies | 2026-08-09 17:35 | complete | 6–7 |
| Los Angeles Angels at Miami Marlins | 2026-08-09 17:40 | late/not fired | 3–12 |
| Chicago Cubs at Kansas City Royals | 2026-08-09 18:10 | late/not fired | 10–2 |
| Cleveland Guardians at Chicago White Sox | 2026-08-09 18:10 | late/not fired | 3–5 |
| Minnesota Twins at Milwaukee Brewers | 2026-08-09 18:10 | late/not fired | 3–4 |
| Colorado Rockies at St. Louis Cardinals | 2026-08-09 18:15 | late/not fired | 4–7 |
| Baltimore Orioles at Texas Rangers | 2026-08-09 18:35 | late/not fired | 10–5 |
| Detroit Tigers at San Francisco Giants | 2026-08-09 20:05 | late/not fired | 3–1 |
| Los Angeles Dodgers at Arizona Diamondbacks | 2026-08-09 20:10 | late/not fired | 2–4 |
| Tampa Bay Rays at Seattle Mariners | 2026-08-09 20:10 | complete | 4–1 |
| Houston Astros at San Diego Padres | 2026-08-10 00:20 | complete | 2–7 |

Canonical game UUID, exact teams, and exact scheduled start matched the official final source for all 15 games. See [`raw/slate-reconciliation.sanitized.json`](raw/slate-reconciliation.sanitized.json) and [`raw/official-final-source.sanitized.json`](raw/official-final-source.sanitized.json).

## Completed decision evidence

The six complete outputs contain **24/24 valid arm-game responses**, **72 model decision rows**, and **48 baseline rows**. Current-main scorer `scoring-v0.6.0` independently verified source hashes, decision echoes, and response linkage for each run.

`wouldAbstain=true` appears on `30/72` model rows: Anthropic `9/18`, Gemini `4/18`, OpenAI `7/18`, and xAI `10/18`. By market, the concentration is spread `22/24`, total `6/24`, and moneyline `2/24`; all six Anthropic, OpenAI, and xAI spread rows and four of six Gemini spread rows carry `wouldAbstain=true`. The fixed line-open schema marks moneyline/total rows `selectedForExecution=true` and spread rows false, but **nothing was executed**; that field is not evidence of a protocol trade.

See [`raw/model-decisions.sanitized.json`](raw/model-decisions.sanitized.json).

## Reference-closing CLV

The scorer produced `102/120` primary-scoreable rows: model `60/72`, baseline `42/48`. The remaining 18 rows were explicitly unscored: `line_moved` affected 12 totals rows across two games (8 model, 4 baseline), while `push_capable_line` affected 6 totals rows in one game (4 model, 2 baseline). Both refusal reasons fire per game on every totals participant, so no participant is selectively advantaged. No row was schedule-changed.

| Arm | Market | Scoreable games | Mean economic CLV | Mean margin-adjusted CLV | Primary economic CLV > 0 |
|---|---|---:|---:|---:|---:|
| `anthropic-claude-fable-5` | moneyline | 6/6 | -2.2855% | 1.4109% | 3/6 |
| `anthropic-claude-fable-5` | spread | 6/6 | -1.7910% | 1.9705% | 2/6 |
| `anthropic-claude-fable-5` | total | 3/6 | -8.5341% | -4.3082% | 0/3 |
| `google-gemini-3.1-pro-preview` | moneyline | 6/6 | -4.9192% | -1.3140% | 1/6 |
| `google-gemini-3.1-pro-preview` | spread | 6/6 | -1.7850% | 1.9646% | 2/6 |
| `google-gemini-3.1-pro-preview` | total | 3/6 | -4.2821% | 0.1477% | 1/3 |
| `openai-gpt-5.6-sol` | moneyline | 6/6 | -7.8014% | -4.3275% | 0/6 |
| `openai-gpt-5.6-sol` | spread | 6/6 | -4.9387% | -1.3076% | 2/6 |
| `openai-gpt-5.6-sol` | total | 3/6 | 1.1146% | 5.7969% | 2/3 |
| `xai-grok-4.5` | moneyline | 6/6 | -2.4868% | 1.1886% | 3/6 |
| `xai-grok-4.5` | spread | 6/6 | -2.5139% | 1.2087% | 1/6 |
| `xai-grok-4.5` | total | 3/6 | -0.1499% | 4.4767% | 2/3 |

The final column counts `primaryEconomicClvPct > 0`, not the margin-adjusted variant. The published primary de-vig method is `proportional-v1`; the scorer also declares `shin-v1` as a sensitivity method, but sensitivity values are not pooled into these primary columns. Each machine-readable aggregate now includes its `abstainedRows` count.

These are per-market, game-level descriptive aggregates. This smoke run is **not a cohort or leaderboard**, and pooled cross-market comparisons are intentionally omitted. Full sanitized scorer rows, de-vig provenance, abstention counts, and denominators are in [`raw/clv-scoring.sanitized.json`](raw/clv-scoring.sanitized.json).

## Search and spend boundary

| Arm | Complete calls | Search evidence | Conservative spend |
|---|---:|---|---:|
| `anthropic-claude-fable-5` | 6 | 20 known / 0 unknown | $5.587110 |
| `google-gemini-3.1-pro-preview` | 6 | 3 known / 5 unknown | $0.575786 |
| `openai-gpt-5.6-sol` | 6 | 9 known / 0 unknown | $2.661084 |
| `xai-grok-4.5` | 6 | 95 known / 0 unknown | $4.616456 |

Completed-artifact spend was **$13.440436**. The interrupted at-most-once claim retains a conservative **$5.000000** reservation and the preflight reserve was **$1.000000**, making cap-accounted total **$19.440436 / $60.000000**. The interrupted dispatch's provider billing is unknown because no run artifact landed.

Complete outputs retain `127` known billable searches and `5` unknown/unproven search calls. Unknown never means zero. Per-arm spend is **not cost-per-pick comparable**. Complete provider envelopes were not retained, so the missing search evidence cannot be reconstructed offline; this remains tracked in [ospex-benchmark issue #92](https://github.com/ospex-org/ospex-benchmark/issues/92).

See [`raw/provider-accounting.sanitized.json`](raw/provider-accounting.sanitized.json).

## Evidence boundary

Published: target ledger outcomes, exact public game identities, official finals, structured forecast fields, sanitized CLV rows/aggregates, conservative token/search/spend aggregates, source commits, and source-file hashes.

Not published: credentials, local paths, wallet/key material, private provider payloads or identifiers, model rationales/answer text, captured search queries/results, named upstream odds sources, private database rows, or controller logs.

Validate locally with:

```bash
python scripts/generate-indexes.py --check
python scripts/validate-artifacts.py
```
