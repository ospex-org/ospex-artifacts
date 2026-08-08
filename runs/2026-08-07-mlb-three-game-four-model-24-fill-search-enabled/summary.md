# Friday 8/7 MLB — three games, four models, 24 fills, search enabled

## Result

**Status:** `complete_verified_with_caveats`

**Run label:** `SMOKE_V0_NOT_A_COHORT`

**Network:** Polygon mainnet (`chainId=137`)

**Scope:** contests `88–90`, six moneyline/total speculations, four model arms, `24/24` controlled fills

**Terminal:** `TERMINAL_ZERO` at `2026-08-08T04:59:32.586032+00:00`

This is the first search-enabled controlled MVE artifact in this repository. All 24 frozen fills completed, all three contests were scored against exact-team/time official finals, six speculations settled, 22 winning positions were claimed, and the terminal readback found zero open commitments, pending settlements, claimables, nonterminal positions, or relevant writer processes.

This remains controlled smoke/MVE evidence, **not** a canonical cohort and not a model leaderboard.

## Games

| Contest | Game (away at home) | Start UTC | Markets / fills | Final |
|---:|---|---|---:|---:|
| 88 | Los Angeles Dodgers at Arizona Diamondbacks | 2026-08-08 01:40 | moneyline + total / 8 | ARI 4–3 LAD |
| 89 | Houston Astros at San Diego Padres | 2026-08-08 01:40 | moneyline + total / 8 | HOU 6–3 SD |
| 90 | Tampa Bay Rays at Seattle Mariners | 2026-08-08 01:45 | moneyline + total / 8 | TB 2–1 SEA |

The artifact date is the Friday `2026-08-07` slate date; the games began after midnight UTC.

## On-chain and lifecycle evidence

- Setup: 3 contest creations + 6 speculation creations.
- Controlled execution: `24/24` fills, 24 unique fill transaction hashes, zero failed fills; every fill is bound to its structured frozen decision (selection, confidence, probabilities, abstention flag, policy, and timing).
- Execution policy: `fixed-moneyline-total`. Under the pinned schema, `selectedForExecution: true` is required for supplied moneyline/total forecasts, so it is not an independent execution signal. `wouldAbstain` remains independent and was true on `4/24` executed rows (OpenAI three; Anthropic one).
- Execution adapter: serialized; every fill confirmation preceded the next submission.
- Maker capacity: six tracked markets and six realtime channels, exactly the three-game × two-market requirement. This is capacity-bound evidence, not spare-capacity evidence.
- Postgame: 3 score requests, 3 independently recovered `ContestScoresSet` callback transactions, 6 settlements, and 22 claim transactions.
- Receipt reconciliation: **72/72 unique published transaction hashes succeeded** on Polygon; total gas was `4.947824872942650954 POL`, reported separately from USDC PnL.
- Official final reconciliation: exact away team, home team, and scheduled UTC start matched for all three games; all final scores matched the scores landed on chain.
- Terminal readback: all three contests had zero open commitments, pending settlements, claimables, nonterminal positions, and relevant writer processes.

See [`raw/fills-and-receipts.sanitized.json`](raw/fills-and-receipts.sanitized.json), [`raw/postgame-lifecycle.sanitized.json`](raw/postgame-lifecycle.sanitized.json), and [`raw/terminal-zero.sanitized.json`](raw/terminal-zero.sanitized.json).

## Search and spend boundary

Search was enabled on all 12 model/game calls.

| Arm | Calls | Input tokens | Search count | Search evidence | Conservative spend |
|---|---:|---:|---:|---|---:|
| `openai-gpt-5.6-sol` | 3 | 70,721 | 5 | retained | $1.301934 |
| `anthropic-claude-fable-5` | 3 | 90,255 | 6 | retained | $1.554750 |
| `google-gemini-3.1-pro-preview` | 3 | 10,544 | **unknown** | **unknown / unproven** | $0.309314* |
| `xai-grok-4.5` | 3 | 470,958 | 48 | retained | $2.245944 |

Known billable searches total `59`; three Gemini calls have unknown search accounting. Gemini declared its search tool, but the archive retained no normalized search audit, grounding metadata, or tool-use token evidence. The only supported classification is **unknown/unproven**—not “did not search” and not zero.

The private `rawResponse` field retained extracted answer text, not the complete provider envelope. Missing Gemini evidence therefore cannot be re-parsed after provider/API drift. This is tracked in [ospex-benchmark issue #92](https://github.com/ospex-org/ospex-benchmark/issues/92).

xAI used `470,958 / 10,544 = 44.665971×` Gemini's input tokens and had 48 evidenced billable searches versus Gemini's unknown count. Its spend was `$2.245944` versus `$0.309314`. **Cost per pick is not comparable across arms.** The starred Gemini spend excludes any unknown search fees.

The xAI calls recorded 20, 17, and 11 billable searches with request-side `max_turns: 5`. That parameter caps agentic turns, not searches, and one turn may invoke tools in parallel, so no enforceable search-count bound was exceeded. Counts were observed and priced; derived actual spend was accepted before fill authorization. The private activation note that called 16 a search bound was incorrect; this artifact follows the pinned benchmark source.

No captured search query, result URL, extracted answer text, or provider response body is published here.

## Trading economics

Derived from matched principal and terminal claim payouts; `4.947824872942650954 POL` in Polygon gas is reported separately, and both gas and off-chain provider spend are excluded from USDC trading PnL.

| Participant | Principal | Terminal payout | Net trading PnL | Claim txs |
|---|---:|---:|---:|---:|
| `anthropic-claude-fable-5` | $5.999701 | $3.929292 | **-$2.070409** | 2 |
| `google-gemini-3.1-pro-preview` | $5.999690 | $5.798717 | **-$0.200973** | 3 |
| `openai-gpt-5.6-sol` | $5.999601 | $5.838192 | **-$0.161409** | 3 |
| `xai-grok-4.5` | $5.999677 | $8.337077 | **+$2.337400** | 4 |
| maker | $22.368600 | $22.463991 | **+$0.095391** | 4 |
| Flow setup positions | $0.120000 | $0.120000 | $0.000000 | 6 |

Model plus maker trading PnL reconciles to zero. Flow also paid `$3.000000` in contest-creation fees and `$3.000000` in speculation-creation fees, so its net after creation fees is `-$6.000000` before gas.

These three realized games are not enough to rank models.

## CLV scoring appendix: contests 87–90

A current-main scoring run joined the prior contest `87` with Friday contests `88–90`:

- `80` picks in scope; `62` scored.
- `18` refused, all `push_capable_line`; schedule-held-out: `0`.
- Close capture: `12/12` fresh and usable pre-lock.
- Schedule drift: `0/12` rows.
- Moneyline eligible sample: `n=4` per participant.
- No model beat `baseline-away-ml` on moneyline economic or margin-adjusted mean CLV.

At `n=4`, that last result is noise—not a ranking, promotion, or model-selection result. The complete participant/market table and close timing rows are in [`raw/scoring-contests-87-90.sanitized.json`](raw/scoring-contests-87-90.sanitized.json).

## Permission boundary

The three permission grants are labeled in the raw evidence: Flow PositionModule `1.000000 USDC`, Flow TreasuryModule `6.000000 USDC`, and Maker PositionModule `100.000000 USDC`. After the final fill, source-copied transactions `0x06565a28b2905955b4534be946782ded1c13abbd41a5e1734ccd349c54a83d46` (Flow) and `0x38b57a6eb68f197ffae5105adb4f0f0fe7ffd450ddd7ee079d8b0a9a95b8e836` (Maker) set their PositionModule allowances to zero; immediate readbacks found both PositionModule and TreasuryModule at zero for each role. The terminal source separately records the model PositionModule ceiling as a standing exception; model TreasuryModule allowances were zero. Exact later model PositionModule balances are omitted because subsequent shared MVE activity makes them non-Friday state.

## Evidence boundary

Published:

- exact game identities, frozen reference odds, executed structured decisions, fill amounts, transaction hashes, successful receipt blocks/timestamps/gas, final scores, settlement/claim evidence, terminal readback, derived trading economics, sanitized search/spend aggregates, source commits/hashes, and cross-run scoring aggregates;
- the explicit search-envelope and comparability caveats above.

Not published:

- credentials, local paths, wallet key material, private provider payloads or envelopes, extracted model answer text, captured search queries/result references, named upstream odds providers, private database rows, or controller logs.

Validate locally with:

```bash
python scripts/generate-indexes.py --check
python scripts/validate-artifacts.py
```
