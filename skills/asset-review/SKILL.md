---
name: asset-review
description: Run a structured multi-persona review board (nine roles incl. author-credibility and practice lead, dispatched in parallel on a strong model at high effort) over a drafted consulting asset and merge the findings into a page-by-page redline, then run an altitude + marketing-drift check, a consistency/terminology check against the ledger, humanization (the bundled writing ruleset plus humanizer plus the voice skill's author-matching, localization, and machine tell-scan), and a claims check on both provenance (verified vs aspirational) and technical soundness (is the mechanism actually correct). Use when reviewing a full drafted proposal, deck, or document before it goes to an MD or client, running a color-team or red-team review, or doing a final de-AI and claims-honesty pass. For a quick single-slide critique use smd-review; for a pure text humanization pass on a snippet use humanizer; for author-voice/localization/marked-up de-slop use voice.
---

# asset-review

## When to use

Use this skill when a drafted asset needs a full structured review before it goes to an MD or client: multi-persona critique, a prioritized redline, humanization, and claims verification in one pass.

Do not use it for a single-slide critique (the `smd-review` skill handles that) or for humanizing a short standalone snippet where no review work is needed (the `humanizer` skill handles that).

## Workflow

Nine steps, run in sequence.

1. **Persona critique.** Select the relevant personas from `references/personas.md` and dispatch them as parallel read-only passes over the draft. Each persona reads the full asset and returns findings. See `references/parallel-dispatch.md` for the dispatch pattern, persona cap, and brief template. While the board runs, execute the deterministic steps (6b, 5) yourself so they merge alongside the persona findings — and do not act on a partial board.

2. **Fold in external human feedback.** Before merging, collect any reviewer notes already in hand: email comments, tracked changes, verbal notes from a walkthrough. Treat them as additional findings with a source label, not overrides.

3. **Adjudicate, then merge into a page-by-page redline.** Merging is not transcription. Before a finding enters the redline, label it **CONFIRMED** (you reproduced it), **FALSE POSITIVE** (the persona was wrong — say why), or **JUDGEMENT** (no fact to check; the author's call). Re-derive every numeric finding from the source data or the script that produced the figure rather than accepting the persona's word, and check every finding against the state file's decision log — a finding contradicting a logged decision is a conflict to surface, not an entry to apply. Then combine into `Loc | Current | Suggested | Why | Priority | Status`, de-duplicate, rank by convergence count, and sort by page. Report the board's **negative** result too: what it attacked and could not break. Full schema, the `D` (deferred) class, and worked examples in `references/redline-format.md`.

4. **Altitude & marketing-drift check.** Confirm each section is pitched at the right level for its audience. Executive sections carry claims and consequences, not mechanism. Technical sections carry precision. Flag mismatches as P1 or P2 redline entries. Also confirm the draft states and supports each win theme from the `positioning` win-themes list — flag any win theme that is asserted without supporting evidence as a P1 redline entry. Then run the **marketing-drift linter** over exec/high-level copy and flag as P1/P2: vendor-version or mechanism detail that belongs in the technical layer; self-referential citations or framing disclaimers that add nothing ("why the disclaimer here?"); internal-voice leakage — phrasing that reads like a note to the team rather than to the reader (e.g. "the honest trade-off an architect will ask about"); and rhetorical-question or slogan hooks where a stated proposition is stronger.

5. **Consistency & terminology check.** Check the draft against the `positioning` terminology ledger: every concept uses its canonical name (no invented synonyms — "the six dimensions" does not become "the six jobs"), no label was carried verbatim from a source input, and load-bearing counts and phrases match everywhere ("one API" vs "multiple APIs", "four layers" vs "five"). In a multi-artifact system, check consistency *across* the files, not just within one. Flag each drift as a P1 redline entry — inconsistency reads as carelessness to an evaluator.

6. **Humanization pass.** Run the bundled writing ruleset in `references/writing-ruleset.md` over the draft. If the `humanizer` skill is installed, run it at equal weight alongside the ruleset: both run, neither replaces the other. If the `voice` skill is installed, delegate to it as well — it adds what generic humanization does not: author-voice matching from a sample, DACH/German-structure localization, and the operational de-slop method for marked-up copy (entity-aware tell-scan, fragment-edit discipline, voice-reference anchor). This matters most for headlines, hero lines, and section titles, which regress worst and should get an explicit extra pass. Close the step with `voice`'s **machine tell-scan** and report the residual watchlist count per register (exec copy should reach zero).

6b. **Self-consistency + number integrity.** Two passes that compare the asset against *itself*, so they need no external source and no personas — run them yourself, and run them during Build too, not only here. **Self-consistency**: compare the persuasive layer (hero, titles, callouts, close, diagram labels) against the asset's own honest layer (maturity map, basis column, caveats). A claim the asset's own evidence contradicts is **P0** — a skeptic needs one click to use your own table against your own headline. Includes the exec-view reconciliation and promotion checks. Method in `references/self-consistency.md`. **Number integrity**: the five arithmetic-consistency checks, reader-reproducibility, stat integrity, and leave-one-out on every headline figure. Quantitative defects are repeatedly the largest single finding class, and they are presentation defects rather than modelling errors. Method in `references/number-check.md`.

7. **Claims check (provenance + technical soundness).** Verify each entry in the claims register (produced by the `positioning` skill). Every capability claim must be marked `verified` (named source) or `aspirational` (planned or intended). Then run the **technical-soundness** pass on every load-bearing technical claim — a separate axis from provenance: is the mechanism actually correct (ordering/timing), is it stated more strongly than the mechanism supports, and is it internally consistent across layers? Surface unsound mechanisms for the author as an architecture decision rather than silently rewriting the model. Full workflow, the soundness axis, and worked examples in `references/claims-check.md`.

8. **Compliance-matrix sign-off** (tender responses only). Confirm every MUST requirement in the compliance/traceability matrix from `positioning` is addressed and the evaluator can locate the response. Sign off the matrix. The `asset-forge` orchestrator checks for this sign-off before closing the Review gate.

## Optional dependencies

`smd-review`, `humanizer`, and `voice` are used when installed; the skill is complete without them.

If `smd-review` is not installed, step 1 runs the exec/MD persona using the bundled MD-persona prompt in `references/personas.md`. If `humanizer` is not installed, step 5 runs the bundled writing ruleset alone. If `voice` is not installed, step 5 runs without author-voice matching, localization, or the operational tell-scan — the ruleset and `humanizer` still run.

## Reference files

Read each reference file when its corresponding step runs.

- [references/personas.md](references/personas.md) — nine reviewer personas (incl. author-credibility, practice lead, redundancy/earn-its-keep) with questions, the bundled MD-persona prompt for when `smd-review` is absent
- [references/parallel-dispatch.md](references/parallel-dispatch.md) — how to dispatch personas as parallel subagents, persona cap, model/effort pinning, token cost, and output-merge method
- [references/redline-format.md](references/redline-format.md) — table schema, P0/P1/P2/D definitions, adjudication statuses, verbatim-current rule, worked examples
- [references/writing-ruleset.md](references/writing-ruleset.md) — the authoritative humanization standard: 14 core rules, required checks, safety rails, audit reference
- [references/self-consistency.md](references/self-consistency.md) — the persuasive layer against the asset's own honest layer; exec-view reconciliation; the promotion check
- [references/number-check.md](references/number-check.md) — five arithmetic-consistency checks, reader-reproducibility, stat integrity, leave-one-out, problem-side honesty
- [references/claims-check.md](references/claims-check.md) — claims verification workflow, verified/aspirational/disallowed categories, two worked examples

## Conventions

Always use `[CLIENT]` as the placeholder for the customer name — never write the real name.
