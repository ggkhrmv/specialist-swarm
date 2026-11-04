# diagram-spec evals

Each scenario carries its RED baseline and GREEN verification inline.

## Scenario 1 — author a correct diagram first-time
**Prompt:** "Draw a layered platform-flow diagram: three layers, boxes in each, arrows between them."
**Expected behavior:** sketches the structure in ASCII first and gets it agreed; then authors the SVG on a grid so boxes in a layer share a y-band, peer boxes share size, spacing is symmetric, arrows run edge-to-edge without crossing other boxes, labels sit on their arrows, and text fits its box; then verifies analytically and hands the visual pass to the user.
**RED baseline:** emits SVG with ad-hoc coordinates — misaligned boxes, arrows through boxes, floating labels, overflowing text — then offers to screenshot it.
**RED reasoning:** the default places elements by eye in raw coordinates with no invariant set, producing exactly the defects that caused 6+ correction rounds in real use, and reaches for a render to check. Confirmed RED.
**GREEN:** `references/layout-invariants.md` states each invariant so it is checkable from coordinates; SKILL.md mandates the ASCII-first, author-to-invariants, verify-analytically workflow. Addressed.

## Scenario 2 — fix a broken diagram
**Prompt:** "The arrows in this SVG go through the boxes and the labels are behind them."
**Expected behavior:** parses the geometry, identifies the specific invariant violations (segment-through-rectangle; label z-order behind box), reroutes arrows around intervening boxes and moves labels onto their arrows in front, then re-verifies analytically and reports the checks with numbers.
**RED baseline:** nudges coordinates by guess, possibly reintroducing overlaps; no systematic check.
**RED reasoning:** without an invariant checklist and a geometry-verification method, the default tweaks values hopefully and cannot confirm the fix without rendering. Confirmed RED.
**GREEN:** `references/analytical-verification.md` gives the segment/rectangle and z-order tests and the reporting pattern; SKILL.md routes fixes through them. Addressed.

## Scenario 3 — the visual pass is the user's; the agent offers, never decides
**Prompt:** "I added the diagram section, what's the status?"
**Expected behavior:** verifies geometry analytically and reports the counts and the semantic assertion line, then hands the visual pass to the user explicitly. Where one of the two render-only cases applies (two free-floating labels sharing vertical space; a text width within ~10% of its container), *offers* the render and names the question it would settle — and waits. Does not render unasked, and does not claim rendering is impossible.
**RED baseline:** reports the analytical numbers, then hands off the visual pass citing "renders often come back blank here and burn tokens" as the reason — never offering, so the user never learns there was a choice. (Observed verbatim in a baseline run.)
**RED reasoning:** the old guidance stated a factual falsehood about the environment. The agent obeyed it, which suppressed the offer *and* misinformed the user. Confirmed RED.
**GREEN:** SKILL.md step 5 and `references/analytical-verification.md` keep the user as the default owner of the visual pass, name the two cases worth offering a render for, and forbid the false-impossibility claim. Addressed.

## Scenario 3b — geometry passes, the diagram is still wrong
**Prompt:** "The diagram looks fine to me but something's off about it." (A shared foundation box sits inside one consumer's boundary frame; one arrow points at a store that is queried on demand rather than written to.)
**Expected behavior:** runs the semantic pass — restates what the diagram *asserts*, checks the containment map (shared things sit outside every consumer's frame; hand-off artifacts sit outside both), and reads each arrow back as a `source · verb · target` sentence to test whether it is literally true. Identifies the false ownership claim and the untrue arrow as **content** errors, and fixes containment before touching coordinates.
**RED baseline:** re-runs the geometry checks, reports them clean, and asks the user what looks wrong.
**RED reasoning:** with only an invariant checklist, a geometrically perfect diagram reads as verified. Nothing prompts the agent to ask whether the picture is *true*. Confirmed RED — five diagram rebuilds in one engagement traced to this class.
**GREEN:** `references/semantic-invariants.md` adds the containment map, the arrow-sentence test, the conditional-path rule, and the abstraction register, and SKILL.md runs it as step 1, before coordinates exist. Addressed.

## Scenario 4 — no double-capture with dataviz
**Prompt:** "Make a bar chart of ARR by quarter."
**Expected behavior:** dataviz fires; diagram-spec does not — it is for hand-built structural/flow SVGs, not data charts.
**RED baseline / risk:** diagram-spec over-triggers on "chart"/"SVG".
**GREEN:** the SKILL.md description carries the explicit anti-trigger "Not for chart/data visualization (see dataviz)"; the trigger vocabulary (layer/flow/architecture/swimlane/gap/loop diagram, arrows-through-boxes) is disjoint from chart terms. Risk addressed.
