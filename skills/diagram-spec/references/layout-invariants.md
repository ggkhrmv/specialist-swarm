# Layout invariants

The rules a diagram must satisfy to read as correct. Each is stated so it can be checked from
coordinates, not just by eye. These are the exact failure classes that caused repeated rework
rounds on real asset diagrams.

## Boxes

- **Aligned to their layer.** Every box that belongs to the same horizontal layer shares a y
  origin and height — one y-band per layer. A box that sits a few pixels off its layer reads as
  a mistake. Same for columns: boxes meant to line up vertically share an x.
- **Uniform sizing within a group.** Boxes representing peer items (the four artefacts in a
  gap diagram, the cards in a row) share width and height. Do not let one be 180 wide and its
  sibling 232 — equalize them and center the group symmetrically about its axis.
- **Symmetric spacing.** Equal gaps between peer boxes. If the group is centered on an axis
  (e.g. x=540), the boxes are symmetric about it, and any divider/caret on that axis (a gap
  marker, a domain divider) sits exactly on it.
- **No overlap.** No two box rectangles intersect. Leave a real gutter between them.

## One declared center line

- **Declare a single center constant (`CX`) and your column constants at the top of the layout, and
  derive every box `x` from them.** Never hand-place a box near the axis. A frame centered on 520
  with its contents centered on 535 is invisible in raw coordinates and glaring on screen — "the boxes
  inside are not centered; alignment should be easy to catch."
- Assert it: axis-column boxes share `CX` exactly, paired boxes are symmetric about it, and **each
  enclosing frame shares `CX` with its contents**. Report the computed centers, not "looks centered".

## Arrows / connectors

- **Orthogonal only.** Every connector is made of horizontal and vertical segments with 90° elbows.
  **No point-to-point diagonals** — they cannot be made to look deliberate and they read as
  hand-drawn ("wobbly, the lines are not straight"). Assert zero segments where `dx≠0 and dy≠0`, or
  justify each exception explicitly.
- **Route between boxes, never through them.** An arrow from A to B must not pass through the
  rectangle of any third box C. If a straight line would cross C, route around it (elbow/orthogonal
  path) or move the boxes.
- **Endpoints land on box edges** — on edge *centers* where possible. An arrow starts on the edge of
  its source box and ends on the edge of its target box — not floating in the gap, not buried inside.
- **Call and return draw as a double-track.** Where an actor calls a component and control returns,
  draw two parallel segments a fixed gap apart — one solid outbound, one dashed inbound — both landing
  on box edge-centers. Not one bidirectional line, and not two lines at different angles.
- **Consistent arrowheads and direction.** Direction matches the described flow (a read-back/return
  path is visually distinct — dashed or grey — and clearly reversed).
- **Every marker's fill matches the stroke of the line that references it.** Define one marker per
  connector colour; never reuse a default marker across differently-coloured lines ("make the arrow
  tip the same colour as the line — it's blue currently, and the line is red"). After a rebuild, also
  flag any marker still defined but no longer referenced.

## Labels

**Label placement is the dominant defect class in hand-built SVG.** Everything else in this file
causes fewer rounds of rework than this section.

- **A label's full extent collides with nothing.** Compute the whole text extent — not its origin
  point — and assert it intersects no box it does not belong to, no frame or region border, no
  connector line, and no other label. Real defects that passed a geometry check: band labels clipped
  by a boundary frame, a region title cut through by its own frame edge, two group labels stacked on
  the same coordinates, a grounding label struck through by a dashed border, and a route label sitting
  on its own vertical line.
- **Reserve label lanes in the grid *before* placing text.** Keep a ≥24–36 unit gutter between any
  frame edge and the nearest box, so titles have somewhere to live.
- **Frame and region titles sit outside the frame edge, not on it.** Mirror paired region labels — one
  above its frame, one below — so they read as a system.
- **On their arrow, not floating.** An edge label sits on or immediately beside the arrow it
  labels, and in front of it in z-order — never behind a box, never hovering above a different
  edge. (Arrow labels ending up *behind* boxes was a recurring defect.)
- **Layer/section labels are unambiguous.** Each layer or band has one label, positioned
  consistently (e.g. all left-gutter), not colliding with box content.

## Text

- **Fits its box.** Estimate rendered width (roughly `characters × fontSize × 0.55` for a
  typical sans font) and confirm it is less than the box inner width; otherwise wrap onto
  `<tspan>` lines or widen the box. Text overflowing or clipping its box is a first-pass fail.
- **Legibility floor — fit is a floor, not a target.** For a diagram rendered at roughly 900–1200px
  wide, box titles are **≥13** viewBox units and sub-labels **≥10.5**. **Shrinking the font to make
  text fit is forbidden**: widen the box, wrap onto `<tspan>` lines, or shorten the wording. Report
  the smallest font size in the diagram alongside the fit numbers, so the floor is visible. This
  exists because "the boxes and the text are really little and hard to read" had to be said twice —
  the fit check had passed throughout, because it only ever asked whether text fit, never whether it
  could be read.
- **Author copy is never shrunk or truncated to fit.** Reflow it across `<tspan>` lines or widen the
  box, and tell the author that only the line breaks are yours.
- **Vertically centered** within its box (account for baseline: `y ≈ boxCenterY + fontSize×0.35`).
- **Text is geometry.** Any change to a label's wording or font size **re-runs the fit and collision
  checks** before the diagram is shown. A verified layout does not stay verified when the words change
  — this bit twice, once after relabelling with longer names and once after enlarging fonts for
  legibility (which then required four box widenings).

## Frame

- **viewBox containment.** Every drawn element — box, arrowhead tip, label, caret — lies within
  the viewBox bounds. Nothing clipped at the edges.
- **Balanced markup.** Tags open and close correctly; a hand-edited SVG must stay well-formed
  (see the analytical-verification checks).

## Motion (if animated)

- An animated dot or pulse travels **along the arrow path** (`<animateMotion>` on the path or a
  path-following transform), not on a separate straight line above/below it. A dot that travels
  "above the arrow instead of on it" is the classic tell.

## Generate, don't hand-edit twice

The **second** time you edit a diagram's coordinates by hand, stop and write a small generator that
emits the SVG from parameters (box positions, labels, chips). Keep it beside the asset.

Hand-edited coordinates do not survive a third revision, and a generator makes the analytical checks
trivially re-runnable — in practice, once a diagram was script-generated, two subsequent geometry
changes each became a one-parameter edit instead of re-placing sixty coordinates by hand.

## Register

Keep diagrams framework/vendor-agnostic unless the asset sanctions specific names as examples.
A diagram is exec-facing surface: it carries the claim, not the mechanism catalog. The full register
rule — capability versus concrete, and the forbidden-name grep that enforces it — is in
[semantic-invariants.md](semantic-invariants.md).
