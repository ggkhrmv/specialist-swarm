# Build validation — analytical first, the visual pass is the user's

For self-contained HTML assets (presentation sites, decks, capability maps), run this checklist
after every build and every rework increment. It is **analytical**: verify by structure and
geometry and report the counts. Analytical checks catch what no render can — tag balance, dangling
anchors, duplicate ids, exact coordinates.

**The visual pass belongs to the user, by default and always.** Report your numbers, then hand it
over. Do not render on your own initiative.

You may **offer** to render when there is a specific question a render would settle, and render
only if the user takes you up on it. The decision is theirs every time — a previous yes does not
carry to the next increment. When you offer, name the specific thing it would check, not "to have
a look".

Rendering does work in this environment (a headless browser may need libraries staged locally
first). That is not a licence to render unasked. But never tell the user a render is impossible,
and never use "screenshots come back blank here" as the reason to skip the offer — that claim
is false, and it hides a real choice from them.

## Structural checks

- **Tag balance.** Count and match open/close for the load-bearing tags: `<div>`, `<section>`,
  `<svg>`, `<ul>`, `<ol>`, `<script>`, `<style>`, and any comment markers. Report as counts
  ("div 155/155, section 15/15, svg 20/20").
- **No duplicate ids.** Every `id` is unique across the file.
- **Anchors resolve.** Every in-page `href="#x"` has a matching `id="x"` — zero dangling
  anchors. Every deep-dive link and back-link resolves both ways.
- **Self-contained.** No CDN or external URLs; fonts embedded (base64 or local), logos inline
  SVG. The file must open offline.
- **JS parses.** If there is script, `node --check` it (or equivalent). Every `getElementById`
  / `querySelector` target exists in the DOM. Controller selectors still resolve after any
  section move.

## Content scans (delegate the voice parts to the `voice` skill's tell-scan)

- **Price/placeholder discipline.** Zero `€`/price figures in views that must not carry them;
  no `[CLIENT]` placeholder leaked into a real name or vice versa.
- **Em dashes in visible exec copy.** Zero, using the entity-aware pattern
  `(?:—|&mdash;|&#8212;|&#x2014;)` over visible text (not CSS/JS/class names). Technical/low-level
  copy keeps its register.
- **Terminology consistency.** Canonical names and load-bearing counts match the `positioning`
  ledger across the file (and across files, for a multi-artifact system).
- **Sanctioned names only.** Product/vendor names appear only where the asset explicitly allows
  them as examples.
- **Assertion count.** Each load-bearing fact, caveat, and count has **one canonical location**;
  every later appearance must add something new. Grep each ledger count and each core claim and
  report occurrences per section — more than about three is a defect to justify or cut. In practice
  one count reached seven appearances where three were warranted. Two patterns to cut on sight:
  prose that restates a diagram's box labels, and a caveat repeated in the sub, the caption, *and*
  the deep-dive block (keep the caption).

## Dual-view integrity

For any asset with two reader views (exec/architect, summary/detail), a toggle that hides content
turns ordinary cross-references into dead ends. Two checks:

**Cross-view references.** Grep visible copy for positional and deictic phrases — `below`, `above`,
`see the table`, `as shown`, `the following`, `opposite`, `overleaf` — and for each hit assert the
target sits in the **same view** as the reference. A reference that legitimately crosses views must
name the other view explicitly ("set out in the architect view"), never rely on position. Re-run
this sweep after any single-view export: dropping a layer turns every pointer into it into a dead
reference.

**View assignment.** A new section, figure, or block has no default view — assign it. For each
section and figure id, confirm it is either inside the hidden-view wrapper or deliberately
default-facing, and list the assignment in your report. Unassigned means default-visible, which is
how mechanism leaks into a pitch view one increment at a time.

Corollary: content added to satisfy a specific reviewer's finding must land in the view **that
reviewer reads**. A funding gate written for the buyer is useless in the technical layer.

## After removing a block

Deletion breaks the things that pointed at what you deleted. After removing any block, check five
things:

- **Orphaned defs.** SVG `<marker>`, `<defs>`, gradients, and filters the block defined or was the
  last consumer of.
- **Lead-in and lead-out prose.** A sentence above or below that referenced it — positionally
  ("the table below") or by name. A table, diagram, or list that has lost its only lead-in.
- **Ledger-locked content.** A canonical name or load-bearing count that existed *only* in the cut
  text. If the author's own cut removed something ledger-locked, flag it for their ruling; do not
  silently restore it in your own words.
- **Sibling counts.** A grid or flex row tuned for N items must still read correctly at N−1.
- **Tag-count delta** as positive proof the cut was clean — report it (`svg 9→8`).

Also sweep for anchors and controller selectors that no longer resolve.

## Diagram geometry

Delegate each SVG diagram's internal geometry to the `diagram-spec` skill (boxes aligned,
arrows clear of boxes, labels on arrows, text fits, viewBox containment).

## Dead code

Note (don't necessarily remove) CSS classes or markup left orphaned by a restructure, so a later
sweep can clean them. Harmless-but-dead is fine to ship; unresolved-and-live is not.

## Report + hand off

Report the checklist result with numbers, then state explicitly: **geometry and structure verified
analytically; the visual pass is yours.** List what analysis could not settle so the user knows
where to look — and if one of those items is specific enough to be worth a render, offer it and let
them decide.
