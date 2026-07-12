# Ospex MVE Phase 1 Block L — two-contest role-isolation artifact

Generated: 2026-07-12T05:25:30Z

Status: `complete_verified_with_caveats`
Verdict: `AMBER_LIVE_CAVEATS_FINAL_ZERO`
Publication label: `AMBER_QUOTED_NO_FILL`
Classification: `quoted_no_fill`

## Scope

- Two verified MLB contests: contests 44 and 45.
- Three speculations per contest: speculation IDs 120–125.
- Two independent maker wallets and two distinct taker wallets.
- Intended live objective: six controlled fills across all six contest/market pairs.
- Actual controlled live fills: zero.

## Proven in this run

- Six bounded setup seed fills completed with `selfMatch=false`.
- A clean 75-second two-maker dry rerun produced six of six shared healthy target pairs.
- Both live makers posted two-sided commitments across all six pairs: 24 visible commitments total.
- Runtime capacity was healthy at 12 anonymous odds streams, two owner streams, and 14 total connections.
- A pre-first-pitch closing snapshot captured all six exact designated lines.
- Official finals matched on-chain scoring: Kansas City Royals 1 at Baltimore Orioles 6; Houston Astros 9 at Texas Rangers 3.
- Two contests were scored, six speculations settled, and six winning positions claimed.
- Final positions, commitments, allowances, writer processes, and locks were zero.

## Live caveat

The intended six-fill live path was not exercised. A harness assertion read `stream.subscribers` instead of `odds.subscribers`, classified healthy capacity as failed, and halted before fill dispatch. The 24 posted commitments were then invalidated through 18 successful shutdown transactions: six bulk nonce-floor raises for maker A and twelve per-commitment cancellations for maker B. No Ospex protocol defect is established by this halt.

## Operator incidents

- A transient reference-line mismatch first reduced the exact shared target set from six to five and halted safely before live writes; a later rerun recovered to six of six.
- The stream-capacity metric field mismatch caused the zero-fill live halt.
- The pinned CLI treats a zero requested approval as `skip-not-requested`, not as `approve(spender, 0)`; explicit approve-zero transactions were used and all current/stale allowances ended at zero.
- The pinned schema-v1 authoritative-cleanup response does not require a top-level `ok`; terminal payload and readback checks now govern classification.

## Cost and terminal state

- Protocol creation fees: 5.000000 USDC.
- Total lifecycle gas: 2.613594756186865169 POL under the 5.000000 POL ceiling.
- Relied-on on-chain transactions: 62/62 successful.
- Controlled live match transactions: 0.
- Terminal result: final zero clean.

## Interpretation

This is not a successful six-fill role-isolated live regression. It is evidence of setup, dual-maker quoting, fail-closed shutdown, bounded cleanup, official scoring, settlement, claims, and final-zero recovery. A later funded run is still required to prove six controlled live fills and canonical own-state fill attribution.
