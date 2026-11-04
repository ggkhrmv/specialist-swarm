# asset-review evals

## Scenario 1 — multi-persona review board

**Prompt:** "Review this drafted proposal before it goes to the MD." [attach a multi-page draft]

**Expected behavior:**
- Runs multiple reviewer personas (economic buyer, technical buyer, procurement, legal, red-team, exec/MD).
- Merges findings into a page-by-page redline (Loc | Current | Suggested | Why | Priority).
- Checks the asset lands the win themes; flags altitude mismatches (asset-type-conditional).

**RED baseline:** one flat pass of generic comments, no personas, no prioritized redline.

**RED reasoning:** Without the persona roster and the parallel-dispatch pattern, a default pass produces unstructured prose commentary. No role differentiation means the economic buyer's cost-risk concerns and the red-team's credibility challenges collapse into a single undifferentiated list. Without the redline schema and priority levels, the author cannot tell what to fix before sending and what can wait.

---

## Scenario 2 — humanization (equal-weight passes)

**Prompt:** "Do a final de-AI pass on this section."

**Expected behavior:** applies the full writing ruleset AND (if installed) humanizer; both run, neither is skipped; catches "X, not Y" overuse, filler, curly quotes, TED-talk cadence without inventing typos or forcing slang.

**RED baseline:** a single light edit; misses the ruleset-level issues.

**RED reasoning:** Without the writing ruleset, a default humanization pass focuses on surface word swaps. Rule-level issues (reflexive three-part cadence, paragraph-closing type definitions, identical paragraph arcs, concession-plus-positive rhythm) go undetected. The safety rails (no invented typos, no forced slang) are not enforced.

---

## Scenario 3 — claims honesty

**Prompt:** "Check our capability claims." [draft mentions a capability the team hasn't actually delivered]

**Expected behavior:** flags the unverified/aspirational claim (the kubeVirt-style correction), asks for a source, and flags any fabricated-looking credential.

**RED baseline:** accepts all claims as stated.

**RED reasoning:** Without the claims-check reference, a default pass has no mechanism to distinguish verified from aspirational claims and no worked example to recognize the pattern (confident language wrapping an undelivered capability). Fabricated-looking credentials (certifications that do not exist, reference projects named but not described) pass unquestioned.

---

## GREEN verification (post-implementation)

**S1 — PASS.** `references/personas.md` gives six roles with distinct questions; economic buyer and red-team ask fundamentally different things, so merging their output into one redline produces differentiated findings. `references/parallel-dispatch.md` defines the parallel dispatch pattern and a persona cap so the author selects a relevant subset. `references/redline-format.md` gives the table schema, P0/P1/P2 definitions, and the verbatim-current rule, so findings are prioritized and locatable.

**S2 — PASS.** `references/writing-ruleset.md` carries 14 core rules, 10 required checks, safety rails, and the optional audit reference. Rule 10 (watch regularity) catches the "X, not Y" overuse explicitly. Rule 7 (do not perform) catches TED-talk cadence. Safety rails prohibit invented typos and forced slang. The equal-weight note at the end of the ruleset specifies that humanizer (when installed) runs alongside, not instead of, the ruleset.

**S3 — PASS.** `references/claims-check.md` defines the verified/aspirational/disallowed categories, requires a named source per capability claim, and carries two worked examples: the kubeVirt-style correction (capability never delivered, presented as a credential) and a CV listing a certification that does not exist. The schema from `positioning`'s claims register feeds directly into this check.

---

## New scenarios (v2 — expanded board, soundness, consistency, voice)

## Scenario 4 — expanded board + technical soundness
**Prompt:** "Review this deck before it goes out — my name is on it." [draft claims "prompt injection is contained by design" and a policy engine gates at a point where it doesn't run]
**Expected behavior:** dispatches the board on a strong model at high effort, including the **author-credibility** persona ("would I defend this live?") and, where relevant, the **practice lead**; the claims check runs both provenance *and* **technical soundness** — flagging the mechanically wrong policy-engine timing and the too-bold "contained by design" even though both are honestly the team's own design; surfaces them as an architecture decision rather than silently rewriting.
**RED baseline:** a generic pass that accepts honestly-held but mechanically wrong claims because they are "ours", and has no author-reputation lens.
**RED reasoning:** the default conflates honesty (is it ours?) with soundness (is the mechanism correct?) and has no persona representing the presenter's reputation. A confidently stated but wrong mechanism sails through. Confirmed RED.
**GREEN:** `references/personas.md` adds author-credibility and practice-lead with distinct questions; `references/claims-check.md` adds the technical-soundness axis with the exact policy-engine-timing and "contained by design" examples; `references/parallel-dispatch.md` specifies a strong model at high effort. Addressed.

## Scenario 5 — consistency, terminology, marketing-drift
**Prompt:** "Review this — something feels off and inconsistent." [draft calls the same concept "the six dimensions" then "the six jobs"; exec section says "one API", a later section says "multiple APIs"; an exec para reads like an internal note]
**Expected behavior:** the consistency/terminology check flags the "six dimensions" vs "six jobs" drift against the ledger, the "one API"/"multiple APIs" load-bearing contradiction, and any label lifted verbatim from a source; the marketing-drift linter flags the internal-voice leakage and any mechanism detail or framing disclaimer in exec copy.
**RED baseline:** treats synonyms as stylistic variety and misses the count contradiction and the internal-voice leak.
**RED reasoning:** the default has no terminology ledger to check against and reads synonym drift as good writing, not a defect; it has no marketing-drift lens for internal-voice or gratuitous disclaimers. Confirmed RED.
**GREEN:** SKILL.md steps 4–5 add the marketing-drift linter and the consistency/terminology check against the `positioning` ledger, with the exact examples. Addressed.

## Scenario 6 — voice delegation + tell-scan exit
**Prompt:** "Final de-AI pass — the headlines still read like a bot." [marked-up HTML with mixed `—` / `&mdash;`]
**Expected behavior:** step 6 runs the ruleset + humanizer **and** delegates to `voice` (author-matching, entity-aware fragment de-slop, voice-reference anchor), gives headlines/hero/titles an explicit extra pass, and closes with the **machine tell-scan**, reporting residual watchlist hits per register (exec → 0).
**RED baseline:** one light pass; treats headlines like body copy; whole-paragraph literal edits that silently fail on mixed em-dash entities; no verifiable exit.
**RED reasoning:** the default has no author-voice mechanism, no entity-aware/fragment method, and no machine exit check — so headlines regress and "de-slopped" is a feeling, not a count. Confirmed RED.
**GREEN:** SKILL.md step 6 delegates to `voice` and requires the machine tell-scan exit; the `voice` skill's `tell-scan.md` carries the entity-aware pattern and fragment rule, and `voice-matching.md` the anchor method. Addressed.

## Scenario 7 — the asset contradicts its own evidence layer
**Prompt:** "Review this before it goes to the exec." [hero: "Safe by construction. Every hard mechanism is de-risked; the risk is retired." · §4 present tense: "every crossing is gated and logged" · §7 the asset's own maturity table: policy engine cur=1 "to build", audit cur=0 "to build", isolation cur=1 "designed, not yet built" · §8: "most of the safety boundaries are still on paper" · close: "The delivery mechanisms already work."]
**Expected behavior:** runs step 6b and reports the contradictions **as P0**, in a table pairing each persuasive claim with the asset's own contradicting evidence and its location. Fixes by splitting each claim on the axis the evidence splits ("the delivery mechanisms are proven; the safety boundaries are designed, not built — that is what the first phase funds") or by moving to design-intent voice, never by softening into mush. Then runs the two sub-checks: confirms every reconciliation sentence renders in the *same view* as both claims it reconciles, and asks which line is the asset's most disarming — promoting it if it sits only in the technical view.
**RED baseline:** finds the contradictions (a fresh reader with the whole asset in view generally does) and ranks them P0 — but produces neither sub-check: no in-view reconciliation test, no promotion check. Also drifts into unrequested scope (rubric legends, table provenance metadata).
**RED reasoning:** detection is not the gap; **timing and completeness** are. Without a named step this only ever runs at the post-build board, when the fix is a re-cut rather than an edit — and the two checks that need a specific prompt never happen. Partial RED, confirmed on the sub-checks.
**GREEN:** `references/self-consistency.md` makes it a named step (6b) that also runs during Build, sets the P0 override explicitly, and carries both sub-checks. Addressed.

## Scenario 8 — merging a board without adjudicating it
**Prompt:** "The six personas are back, merge them into a redline." [Six findings, of which: one claims a table sums wrong (true, but the asset's own footnote already explains why); one attacks an independence claim the asset never makes; one demands raising a target that the state file records as a deliberate, dated owner decision; one reports garbled text that is styled inline pills rendering correctly; one cites a section that does not exist; one miscounts a figure's occurrences.]
**Expected behavior:** adjudicates **before** merging — every finding labelled CONFIRMED / FALSE POSITIVE / JUDGEMENT, numeric findings re-derived from the backing script rather than accepted, and every finding checked against the state file's decision log so the locked target is rejected *citing the log entry*. Output splits into applied / content gaps / deferred, ranks by convergence count, adds a `D` row for anything that would change commercial or political posture, and reports the board's negative result. Surfaces the stale decision-log entry as a correction, not as prose buried mid-report.
**RED baseline:** does verify against the source and does catch the false positives — but produces no adjudication labels, no `D` class, no convergence counts, and buries the stale-log finding in a paragraph under "also surfaced". Reports the two unlocatable findings as "hold, do not action" rather than as FALSE POSITIVE with a reason.
**RED reasoning:** the verification instinct is present; the **structure that makes it legible to the author** is not. Without labels and a deferred class, an audited board reads like an unaudited one, and posture-changing findings get applied or dropped silently. Confirmed RED.
**GREEN:** SKILL.md step 3 requires the three labels, the decision-log check, and the negative result; `references/redline-format.md` adds the `Status` column, the `D` class with cost-of-doing-nothing, and the applied/gaps/deferred split. Addressed.
