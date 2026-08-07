# August 6 SD@ARI contest 87 — four models, two markets, 8/8 fills, terminal zero

- **Status:** `complete_verified_with_caveats`
- **Network:** Polygon mainnet (`chainId=137`)
- **Contest:** `87`; moneyline `235`; total 9 `236`
- **Frozen plan:** `91654424daa58ba05e879db6aa6bb38cc1ba53770fa339daf6a03b572732c488`

Four role-isolated model wallets each supplied one moneyline and one total decision. All **8/8 frozen arms** have durable successful fill completions: four from the original pass and four from two separately timestamped, authorized late-retry passes. Aggregate model risk was **7.999343 USDC** against 8 USDC requested.

## Controlled fills

| Model | Market | Selection | Model risk USDC | Timing | Transaction |
|---|---|---|---:|---|---|
| Anthropic | moneyline | Arizona Diamondbacks | `0.999972` | original-pass-completion | [`0x27cbde649366071491f7812561dfc68f06e378d7186cc7f03750b293b04ff974`](https://polygonscan.com/tx/0x27cbde649366071491f7812561dfc68f06e378d7186cc7f03750b293b04ff974) |
| Gemini | moneyline | San Diego Padres | `0.999915` | authorized-late-retry | [`0xd6a1022179f21de07ae7d85aa010ecf055d4e858b945b62b6218c9f7110daee1`](https://polygonscan.com/tx/0xd6a1022179f21de07ae7d85aa010ecf055d4e858b945b62b6218c9f7110daee1) |
| OpenAI | moneyline | Arizona Diamondbacks | `0.999898` | original-pass-completion | [`0x9fda4f46523abc6a35bbd58ce2b08965ecc52738cbda178165633c3fe1befdb0`](https://polygonscan.com/tx/0x9fda4f46523abc6a35bbd58ce2b08965ecc52738cbda178165633c3fe1befdb0) |
| xAI | moneyline | Arizona Diamondbacks | `0.999898` | authorized-late-retry | [`0x94cdff539bf2f2e7376e503228ec88d49cfd8a728ba8decafa826f4d30be8e32`](https://polygonscan.com/tx/0x94cdff539bf2f2e7376e503228ec88d49cfd8a728ba8decafa826f4d30be8e32) |
| Anthropic | total | under | `0.999915` | authorized-late-retry | [`0x29ec0f98c4c9e34f9316006b847cf941f6c43e82aa8f8520281b2f23b84b4f5f`](https://polygonscan.com/tx/0x29ec0f98c4c9e34f9316006b847cf941f6c43e82aa8f8520281b2f23b84b4f5f) |
| Gemini | total | over | `0.999915` | authorized-late-retry | [`0x3cfd307b03cca69f5b0380c4ea4e3b37f4d126fefcc75bde06285c3fa83f57e8`](https://polygonscan.com/tx/0x3cfd307b03cca69f5b0380c4ea4e3b37f4d126fefcc75bde06285c3fa83f57e8) |
| OpenAI | total | under | `0.999915` | original-pass-completion | [`0x68fdeba966b20322e059930a51f9074d0af57b076b8fe82617343fe83886d059`](https://polygonscan.com/tx/0x68fdeba966b20322e059930a51f9074d0af57b076b8fe82617343fe83886d059) |
| xAI | total | under | `0.999915` | original-pass-completion | [`0xf602c24ae2008cfad66ab883ac3f974ee9637b407a7813262c104c1ac1bca608`](https://polygonscan.com/tx/0xf602c24ae2008cfad66ab883ac3f974ee9637b407a7813262c104c1ac1bca608) |

## Postgame lifecycle

San Diego won **5–1**. The CRE callback set the exact on-chain score; moneyline speculation `235` settled **away / San Diego**, and total-9 speculation `236` settled **under**.

- score request: [`0xb92215ea056326b75ea25c55e72540d633d13142442dc8c8d164205d718d775d`](https://polygonscan.com/tx/0xb92215ea056326b75ea25c55e72540d633d13142442dc8c8d164205d718d775d)
- CRE score callback: [`0xc0082b2f1f96bb62414719379d60d83ceee4325d4c02ad7a8637df6b4dc92425`](https://polygonscan.com/tx/0xc0082b2f1f96bb62414719379d60d83ceee4325d4c02ad7a8637df6b4dc92425)
- settle moneyline 235: [`0xcd6989e5a88857bbbbd41362a96ab427efc3d4d17c844f81e1922a9630665622`](https://polygonscan.com/tx/0xcd6989e5a88857bbbbd41362a96ab427efc3d4d17c844f81e1922a9630665622)
- settle total 236: [`0x93a7e0b7f52e4b08a8e68cba4790e9e5bbaae49cbcd790799c9201b18670082e`](https://polygonscan.com/tx/0x93a7e0b7f52e4b08a8e68cba4790e9e5bbaae49cbcd790799c9201b18670082e)
- winning claims: **8**, all confirmed

Fresh publication readback found all **22/22** proof transactions successful: eight fills, score request, CRE callback, two settlements, eight claims, and two dated-permission revocations.

## Terminal zero

At `2026-08-07T12:05:36.170738Z`:

- active / pending-settlement / claimable positions across six wallets: **0 / 0 / 0**
- Maker A live contest commitments: **0**
- relevant controller processes: **0**
- Flow dated Position/Treasury allowance: **0 / 0**
- Maker A dated Position/Treasury allowance: **0 / 0**
- durable controlled-fill completions: **8**

The four model Position allowances remain under the accepted reusable-standing-allowance exception; all model Treasury allowances are zero.

## Disclosed caveats

The requested pre-start Maker report was missed. Four fills required two authorized retry passes, and the original failures remain preserved rather than rewritten. A readiness field mismatch delayed the single score request by over seven hours; claim-side routing and late-index readback also required manual repair. No duplicate score request or failed on-chain recovery transaction was sent. No closing-odds/CLV artifact exists. B1 lifecycle proof is complete with defects disclosed; B2 remains held.

Machine-readable source of truth: [`evidence.json`](evidence.json).
