---
name: diagram-spec
description: Author and verify hand-built inline SVG diagrams for consulting assets and presentation sites — layer/flow diagrams, architecture diagrams, swimlanes, gap diagrams, loop diagrams — so they are correct on the first pass instead of taking many correction rounds. Covers both semantic correctness (which boundary owns each box, whether each arrow is literally true, the abstraction register) and layout invariants (alignment to a declared center line, uniform sizing, orthogonal routing, labels that collide with nothing, text that fits and stays legible, viewBox containment), verified analytically by computing geometry from the SVG source. The visual pass stays with the user. Use when building or fixing an SVG diagram in an HTML asset, when a diagram "doesn't look right" (misaligned boxes, wobbly or diagonal lines, arrows through boxes, text overflow, colliding or floating labels, unreadable type), when a diagram asserts the wrong ownership or mechanism, or when asset-forge's Build phase produces a diagram. Not for chart/data visualization (see dataviz) or for overall page design (see presentation-websites / hallmark).
---

# diagram-spec

## When to use

Use this when a consulting asset or presentation site needs a **hand-authored inline SVG diagram** — a layered platform-flow diagram, an architecture diagram, a swimlane, a gap/before-after diagram, a loop diagram — and you want it geometrically right without a long tail of "the arrow goes through the box / the text is cut off / the label floats" corrections.

Not for data charts (bar/line/scatter — use `dataviz`). Not for overall page layout or brand styling (use `presentation-websites` or `hallmark`).

## The core problem this solves

Two things make hand-built SVG diagrams painful, and this skill addresses both:

1. **They violate layout invariants** that are obvious to the eye but easy to miss in raw coordinates — boxes not aligned to the layer they belong to, arrows routed straight through other boxes, labels floating above an arrow instead of on it, text overflowing its box. In practice these cause round after round of rework.
2. **They can be geometrically perfect and still wrong.** The analytical pass clears the layout while the diagram *asserts* something false — the wrong box inside the wrong boundary, an arrow describing a mechanism that does not work that way, a name that commits to a tool nobody has chosen. No amount of coordinate checking finds this. It needs a separate semantic pass, run first.

## Workflow

1. **Declare the semantics before the coordinates.** Fix three things in writing: the **abstraction register** (capability-level or concrete), the **containment map** (which boundary owns every box), and the **arrow sentences** (each connector read back as `source · verb · target`). See [references/semantic-invariants.md](references/semantic-invariants.md). Containment and arrow errors are content errors, not layout nits, and each one cost a full rebuild in practice.
2. **Sketch in ASCII.** Lay out boxes, layers, and arrows and get the structure agreed. Cheap to change; catches the wrong structure before coordinates exist. If you are enhancing an existing diagram or a sketch the user supplied, treat that sketch as a **floor, not a spec** — see [references/enhance-by-dispatch.md](references/enhance-by-dispatch.md).
3. **Author against the invariants.** Build the SVG following [references/layout-invariants.md](references/layout-invariants.md). **Declare a single center constant and your column constants at the top and derive every box from them** — never hand-place a box near the axis. Shared x-columns for aligned boxes, shared y-rows for layers, uniform box dimensions within a group, symmetric spacing. **The second time you edit coordinates by hand, stop and write a generator** that emits the SVG from parameters; hand-edited coordinates do not survive a third revision.
4. **Verify analytically.** Run the checks in [references/analytical-verification.md](references/analytical-verification.md): viewBox containment; layers share a y-band; columns share an x; **frames share their center with their contents**; no box overlap; **zero diagonal connector segments**; arrow endpoints land on box edges and paths clear third boxes; **every label's full extent collides with nothing** — no foreign box, frame border, connector, or other label; text fits its box **and** clears the legibility floor; arrowhead fills match their line strokes; stated counts still match the element count. **Text is geometry** — any change to wording or font size re-runs the fit and collision checks.
5. **Report the geometry; the visual pass is the user's.** State what you verified, with numbers, and hand the visual confirmation over — every time, not once. You may *offer* a render when a specific question needs it: two free-floating labels sharing vertical space, or a text width within ~10% of its container, are the cases where the `characters × fontSize × 0.55` estimate is not good enough. Name the question, and let the user decide. A previous yes does not carry to the next diagram, and never tell the user a render is impossible.

## Interaction

If the asset uses clickable/interactive diagram nodes (a liked pattern), keep hit-targets on the box shapes, keep the diagram legible without the interaction, and ensure it still reads in print/no-JS.

## Conventions

Always use `[CLIENT]` as the placeholder for the customer name.

**Fix the abstraction register before drawing, and enforce it mechanically.** A diagram of a target state that is not yet decided uses the **capability register** — no product, vendor, repository, or tool names; the diagram describes capabilities and information flows ("reads platform status", not a named tool). A diagram depicting something that exists and is available today may use the **concrete register**. A single asset can hold both: a mockup of a real interaction stays concrete while the architecture views stay agnostic. Enforce with a forbidden-name grep over the diagram source and report the count. "Grounded in the research" means *accurate*, not *named*.

Where the asset has an **evidence-continuity map** in its state file, draw every label from it, and never label a box at a maturity the map does not support.
