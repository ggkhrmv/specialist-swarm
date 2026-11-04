# Analytical verification

Verify a diagram by computing its geometry from the SVG source. Analysis is precise where the eye is
not: it gives you exact coordinates, exact counts, and a result you can report. Compute, report the
numbers, and **hand the visual pass to the user** — that is the default every time.

## What analysis cannot settle

Two classes need a rendered look, and both come down to the same thing: `characters × fontSize × 0.55`
is an *estimate* of text advance width, good enough inside a box and not good enough at the margins.

- **Two free-floating labels sharing vertical space.** One analytical pass correctly reported zero
  out-of-viewBox coordinates and every arrow landing properly; the render showed a 14px horizontal
  overlap between two labels.
- **Any text whose computed width is within ~10% of its container.**

When you hit one of these, **offer the render and name the question it would settle**. The decision is
the user's, every time — a previous yes does not carry forward. Never claim a render is impossible; if
one is unavailable, hand over the visual pass with *exactly this list* of what to look at, not "please
eyeball it".

Extract the coordinates (parse the SVG, or read the `<rect>` / `<line>` / `<path>` / `<text>`
attributes directly) and run these checks. A small script — walk the elements, build a list of
box rects and arrow segments, and assert the conditions below — is the reliable way; eyeballing
raw coordinates is exactly what fails.

## Checks

1. **Well-formedness.** Tags balanced; the SVG parses. For an HTML file, confirm counts:
   `<svg>`/`</svg>`, `<g>`/`</g>`, `<rect>`, `<text>` all balanced, and no stray unclosed tags.
2. **viewBox containment.** For every element, `0 ≤ minX,minY` and `maxX ≤ vbWidth`,
   `maxY ≤ vbHeight` (include arrowhead tips and text extents, not just box origins).
3. **Layer alignment.** Group boxes by intended layer; assert each group shares a y (and
   height). Group boxes by column; assert each shares an x (and width).
4. **Uniform sizing.** Peer boxes share width and height. Report any outlier (the 180-vs-232 case).
5. **Center line and symmetry.** Compute each box's center. Assert axis-column boxes share the
   declared `CX` **exactly**, paired boxes are symmetric about it, **every enclosing frame shares `CX`
   with its contents**, and any divider or caret sits on the axis. Report the computed centers — a
   frame on 520 around contents on 535 passes a "looks centered" check and fails on screen.
6. **No box overlap.** For every pair of box rects, assert they do not intersect (standard
   rectangle-overlap test); a positive gutter is expected.
7. **Orthogonality.** Count connector segments where `dx≠0 and dy≠0`. The answer must be **0**, or
   every exception explicitly justified. Report it ("0 of 11 segments are diagonal").
8. **Arrow endpoints on edges.** For each connector, assert its start point lies on the source
   box perimeter and its end on the target box perimeter (within a small tolerance).
9. **No arrow-through-box.** For each connector segment, assert it does not intersect any box
   other than its source and target (segment/rectangle intersection test).
10. **Label collision — the big one.** For every `<text>`, compute its **full extent** (not its origin
    point) and assert it intersects **nothing**: no box it does not belong to, no frame or region
    border, no connector line, and no other label. Additionally, an edge label sits within a small
    distance of its arrow's midpoint, and its document order puts it after any box it overlays. This
    single check catches more real defects than any other in this file.
11. **Text fit and legibility.** For each `<text>`, estimate width (`len × fontSize × ~0.55`) and
    assert it is ≤ the inner width of its containing box; else wrap onto `<tspan>` lines or widen the
    box. **Also assert the legibility floor** — box titles ≥13 units, sub-labels ≥10.5 at a ~900–1200px
    render width — and **report the smallest font size in the diagram** so shrinking-to-fit is visible.
12. **Marker colour match.** For each `marker-end` reference, compare the marker's fill against the
    referencing element's stroke; they must match. Separately flag any marker defined but no longer
    referenced after a rebuild.
13. **Count coherence.** If the element count changed, grep every count word referring to it — digit
    and word form — across the standfirst, caption, `aria-label`, deep-dive block, summary rows, and
    `<meta>` description. Report each as still-accurate or updated.
14. **Animation path.** If a dot/pulse animates, assert it references the arrow's path
    (`<animateMotion>` / path reference), not an independent line.

## Reporting

State the result with numbers, per the pattern used on real assets:

> "svg 21/21 well-formed; all 4 artefact boxes 232×64 and symmetric about CX=540, and the enclosing
> frame is also centered on 540; gap marker, domain divider, and caret all on x=540; no box overlap;
> 0 of 6 connector segments diagonal; all 6 arrows land on edge-centers and clear other boxes; all 11
> text extents collide with nothing; longest label 'Infrastructure resources' ≈ 196px < 216px box
> width; smallest font 11 units (floor 10.5); 6 markers, each matching its line's stroke; 'four
> outcomes' still matches 4 boxes. **Geometry verified analytically — the visual pass is yours.**"

Also report the **assertion line** from `semantic-invariants.md` — what the diagram claims, in one
sentence — so the author can check the meaning, not just the geometry.

Then hand over the visual confirmation. Where one of the two render-only cases applies, say so and
offer it, naming what it would settle.

## Related file-level validation

When the diagram lives in a larger HTML asset, the Build-phase analytical-validation checklist
(in `asset-forge`) covers the file as a whole — duplicate ids, dangling in-page anchors,
self-containment. This file is specifically about the diagram's internal geometry.
