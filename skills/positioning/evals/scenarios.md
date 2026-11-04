# positioning evals

## Scenario 1 — win strategy (offensive)
**Prompt:** "We're bidding for a managed platform. How should we position against two incumbents?"
**Expected behavior:**
- Proposes 3-4 win themes (messages the evaluator should repeat back).
- Names discriminators / why-us relative to the competitors.
- Raises commercial / price-to-win posture (e.g. phased land-and-expand).
- Maps proof points / references to the win themes.
**RED baseline:** lists generic strengths, no win themes, no discriminators, no commercial posture.

## Scenario 2 — uncertain scope (defensive)
**Prompt:** "The scope is fuzzy and we might over-commit. How do we respond?"
**Expected behavior:** proposes tiered scope options (not a binary), makes assumptions explicit, states honest boundaries, considers phased-entry only if there's a delivery runway.
**RED baseline:** gives a single all-in scope or a flat yes/no.

## Scenario 3 — tender mechanics
**Prompt:** "Here's an RfQ with 62 requirements. Set up our response tracking." [attach requirements]
**Expected behavior:** extracts requirements preserving IDs, marks MUST vs SHOULD (MUST = K.O.), clusters them, and builds a compliance/traceability matrix. Starts a claims register, flagging any capability we can't verify.
**RED baseline:** summarizes requirements in prose, no ID preservation, no matrix, no MUST/SHOULD K.O. flagging.

---

## RED baseline confirmation (Step 2)

Without this skill loaded, Claude's default behavior in each scenario is:

**S1:** Responds with generic value-proposition language — scale, breadth of capabilities, delivery model. Does not ask what the incumbents' known strengths are or what the evaluator cares about. Does not produce win themes as discrete, memorizable messages. Does not raise pricing posture or land-and-expand strategy. Proof points, if any, are generic industry references, not mapped to specific themes.

**S2:** Produces a single scope recommendation — either a confident yes-we-can-do-it response, or a hedge that collapses to "it depends" without giving the client anything actionable. Does not surface the explicit assumptions that bound the scope. Tiered options may appear as a brief mention but are not worked out with distinct scope, price, and risk profiles.

**S3:** Summarizes the requirements in flowing prose grouped by theme. Does not preserve original IDs. Does not flag MUST vs SHOULD, and does not flag MUST as K.O. criteria. Does not build a compliance matrix. May start a claims list but does not distinguish verified from aspirational claims.

---

## GREEN confirmation (Step 5)

**S1 re-read with skill loaded:**
The skill prompts selection of win-themes and discriminators/why-us plays. Output contains 3-4 named win themes stated as evaluator-repeatable messages, a discriminators section that names specific competitor weaknesses, a commercial posture choice with rationale (T&M phased entry vs. managed model), and proof points mapped to each win theme. The plays.md worked examples show the expected form.

**S3 re-read with skill loaded:**
The skill directs to rfp-mechanics.md, which specifies preserving original IDs, marking MUST as K.O., and clustering requirements before mapping. The compliance-matrix.md schema is applied immediately. A claims register is opened alongside the matrix, with at least one capability flagged aspirational where no named reference exists.

---

## New scenarios (v2 — frame, terminology, metrics)

## Scenario 4 — positioning frame + terminology
**Prompt:** "Position our offering — it's about putting AI on a platform." [source deck uses the label "Orbit agent"]
**Expected behavior:** states the **positioning frame** first, in one line, naming what it is *and is not* (e.g. "enabler/accelerator, NOT a guardrail/governance pitch"); opens a **terminology ledger** with canonical names; treats "Orbit agent" from the source as a placeholder, not a decision, and proposes/locks a deliberate name; guards load-bearing counts.
**RED baseline:** produces value-prop language without a for/not frame; carries "Orbit agent" straight through; lets synonyms drift.
**RED reasoning:** the default infers a plausible angle silently (no explicit for/not frame), reuses source labels verbatim, and has no ledger — so naming drifts across the asset. The wrong frame is the failure that later forces a whole-asset rebuild. Confirmed RED.
**GREEN:** SKILL.md's "positioning frame" section makes the for/not line the first output feeding Gate 2; the "terminology ledger and naming discipline" section bans verbatim-from-source names and locks canonical terms. Addressed.

## Scenario 5 — metrics sourcing, no hallucination
**Prompt:** "Add some numbers — like 'X times faster' — to strengthen the case."
**Expected behavior:** researches real benchmarks (web search allowed), attributes each with a named source, and refuses to present a hoped-for client delta as measured; every metric enters the claims register as verified / aspirational / verified-as-external-illustration.
**RED baseline:** invents plausible-sounding figures ("40% faster") with no source.
**RED reasoning:** asked for numbers, the default fabricates confident-sounding metrics — the single most dangerous honesty failure in a client asset. Confirmed RED.
**GREEN:** SKILL.md's "proof points and metrics sourcing" section requires sourced-not-invented metrics, forbids presenting targets as measured, and routes every metric into the claims register. Addressed.
