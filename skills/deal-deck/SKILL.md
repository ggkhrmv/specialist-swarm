---
name: deal-deck
description: Build the BTS-Synthetic executive pitch deck for a deal as one self-contained HTML file of 16:9 slides (keyboard navigation, speaker notes, print to PDF), in the BTS-Synthetic brand, with editorial SVG diagrams such as a price-bridge waterfall, a positioning quadrant or a timeline. Use after the written proposal is synthesised, when the deal needs a short deck version of it, for example a 5-slide pitch deck saved to /mnt/session/outputs/pitch-deck.html. The brand, fonts, layout components and presenter script are fixed in the skill; you write only the slide content, and the build script embeds everything and runs the quality gates.
---

# Deal deck

You turn a finished proposal synthesis into a **five-slide executive pitch deck**: one
`.html` file that opens offline in any browser, presents full screen and prints to PDF
one slide per page. The deck is the short version of the docx, so it carries **the same
numbers, the same positions and the same governing thought**. If the two disagree, the
deck is wrong.

`SKILL_DIR` below is the directory this SKILL.md is in.

| File | What it is |
|---|---|
| `scripts/build_deck.py` | Wraps your slides in the shell, embeds the fonts, runs the gates. Standard library only. |
| `assets/shell.html` | Brand tokens, components, diagram styles, presenter script. Read it only to look up a class; never edit it. |
| `examples/example-slides.html` | A complete worked deck for a **fictional** customer. Read it before you write. Never reuse its figures. |

## Workflow

1. **Start from the synthesis you already have**: the governing thought, the win themes,
   the headline price and terms, the legal positions, the top risks. Do not brief the
   specialists again for the deck.
2. **Read `examples/example-slides.html`** to see every component and both diagram
   recipes in use.
3. **Write your slides** to a scratch file outside the outputs directory, e.g.
   `/tmp/deck/slides.html`. It contains only the five `<section class="slide">` elements,
   nothing else: no `<html>`, `<style>` or `<script>`.
4. **Build:**
   ```bash
   python3 SKILL_DIR/scripts/build_deck.py /tmp/deck/slides.html /mnt/session/outputs/pitch-deck.html \
     --title "Acme Corp · Enterprise data platform proposal" \
     --context "Acme Corp · RFP response · Confidential"
   ```
   `--context` is the footer line on every slide. If it prints `FAIL`, fix each listed
   problem and build again until it prints `deck OK`. Treat `warn:` lines as edits to
   make unless you have a reason not to.
5. **Read your slides back in order, titles only.** The five titles alone must make the
   argument. Then check every figure against the docx.

## The five slides

| # | Job | Form |
|---|---|---|
| 1 | **Cover.** The governing thought with the client as the subject, plus three facts. | `.slide--cover`: `h1.cover__title` (one phrase in `<em>` at most), `p.cover__sub`, `dl.cover__facts` with three `dt`/`dd` pairs (e.g. headline fee, discount or term, timeline). |
| 2 | **The answer on one slide.** Three claims, each with its proof. | `.body.g-7-5`: a `ul.points` of three items (icon + `strong` + `span`) beside `div.kpis.kpis--stack` with one `kpi--inverse` tile and one or two neutral tiles. |
| 3 | **Why we fit and win** (Technical Fit + Competitive Intel). | `.body.g-5-7`: lead and two discriminators beside **one diagram**: a positioning quadrant (recipe B) or a requirement or criteria coverage chart. |
| 4 | **Commercial proposal** (Pricing). | `.body.g-7-5`: a price-bridge waterfall (recipe A) from list to the offered fee, beside a terms `table` and one `callout`. |
| 5 | **Contract approach, risks and the path to award** (Legal + your risk view). | `.body`: a clause `table` (clause, they ask, our position, a `tag`) and an `ol.steps` to signature, with the current step `is-now`. |

Every slide except the cover opens with `<h2 class="title">` and ends with
`<aside class="notes">`, the speaker notes: what to say, the fallback position, the
number to remember. Detail that does not fit goes in the notes or stays in the docx.

## Copy rules

- **Titles are action titles**: one full sentence that states the claim, 8 to 14 words,
  sentence case, no trailing period. "Commercial proposal" is a label, not a title;
  "Five years for $X, fixed at signature, with no escalators" is a title.
- **The client is the subject** wherever the sentence allows: what they get, what they
  avoid, what they decide.
- **At most about 110 words per slide**, notes excluded. The build warns above that.
- **Every number comes from the specialists' reports or the docx.** Never invent a
  metric to fill a tile. A figure that is an estimate says so ("est.") on the slide.
- Plain, specific, active copy. No emoji, no `→` glyphs, no uppercase labels, no
  marketing filler ("seamless", "cutting-edge", "best-in-class").
- Name competitors as the RFP names them; keep claims about them to what Competitive
  Intel reported.

## Design rules

The brand is fixed. You choose content and composition, not colours or type.

- **Palette:** deep petrol brand (`--brand-100` to `--brand-500`), warm paper neutrals,
  and one copper accent (`--accent`). Copper marks the **one or two focal things per
  slide** (our dot on the quadrant, the offered fee bar, the current step). Using it on
  more erases the signal.
- **Use the shell's classes; never write a colour.** The build fails on any hex, `rgb()`,
  `<style>`, inline `font-family`, `box-shadow`, `<img>`, external URL or emoji. Inline
  `style` is fine for layout custom properties such as `style="--i:2"`.
- **One inverse tile per slide** at most (`.kpi--inverse` or `.inverse`). The cover is
  the deck's only gradient.
- **Icons** come from the sprite only: `<svg class="icon" aria-hidden="true"><use href="#i-check"/></svg>`.
  Available: `i-check`, `i-shield`, `i-alert`, `i-clock`, `i-target`, `i-layers`,
  `i-price`, `i-contract`, `i-people`, `i-chart`.
- **Numbered steps only for real sequences** (`ol.steps`). Tags only for status
  (`tag--accept`, `tag--counter`, `tag--decline`, or `tag--low`, `tag--med`, `tag--high` for risk).

Component cheat sheet: `.title`, `.lead`, `.label`, `.source` (footnote), `.body` with
`.g-7-5`, `.g-5-7`, `.g-1-1` or `.g-3` (add `.top` to align to the top instead of the
middle), `.stack`, `.points` (`.points--plain` without icons), `.kpis` / `.kpi` /
`.kpi__figure` (`<small>` for a unit) / `.kpi__label`, `.callout` (`.callout--focal`),
`.inverse`, `.table` (`.num` for right-aligned figures), `.steps`, `.tag`,
`figure.figure` with `figcaption`.

## Diagrams

Diagram rules adapted from Cathryn Lavery's diagram-design (MIT).

**Draw a diagram only when it says more than a table would.** Slides 3 and 4 each carry
one; the other slides do not need one.

**Size the viewBox to the column, 1:1 with slide pixels,** so the text classes render
at their true size. Column widths: full width 1408, `g-7-5` 792 and 568, `g-5-7` 568
and 792, `g-1-1` 680 and 680. Keep the height at 440 or less.

**Accessible SVG contract**, enforced by the build:
`<svg class="dg" viewBox="0 0 W H" role="img" aria-labelledby="x-title x-desc">`, with
`<title id="x-title">` as the first child (60 characters or fewer) and a one-sentence
`<desc id="x-desc">` about the content, not the geometry. Use a unique prefix per diagram.

**Classes** (no colours in markup): text `dg-name` (20px, labels), `dg-sub` (15px mono,
sublabels), `dg-label` / `dg-axis` (14px mono), `dg-value` (34px serif figures),
`dg-callout` (italic aside, at most one); focal variants `dg-name--focal`,
`dg-value--focal`. Shapes `dg-box` (`--brand`, `--focal`, `--quiet`), `dg-area` (a brand
tint region), `dg-grid`, `dg-baseline`, `dg-zone`, `dg-line` (`--focal`, `--brand`,
`--dash`), `dg-bar` (`--light`, `--quiet`, `--focal`), `dg-dot` (`--quiet`, `--focal`).
Arrowheads: `marker-end="url(#dg-arrow)"` or `url(#dg-arrow-focal)`. Add `grow` to
bars, plus `style="--i:N"` for the stagger, and they build up when the slide opens.

**Layout discipline:**
- Density 4 out of 10: at most 9 nodes or bars and 2 focal elements. Every element must
  earn its place: if removing it loses nothing, remove it.
- Coordinates, widths and gaps on a 4px grid. Text never touches a line, a box edge or
  another label: leave 8px or more. Check text widths before placing a label: about
  11.5px per character for `dg-name`, 9px for `dg-sub`, 8.5px for `dg-label`.
- Connectors are straight or right-angled, never diagonal. Draw lines before boxes so
  boxes sit on top. An arrow label sits on a `dg-mask` rect beside its line, not on it.
- Labels stay inside the viewBox. Text anchored `end` near the left edge, or `start`
  near the right edge, is the usual overflow.
- No legend floating inside the plot; label the marks directly.

**Recipe A: price-bridge waterfall** (viewBox 792 by 440). Baseline at y=380, values
above the bars, category labels at y=408, sublabels such as "−20%" at y=428.
`scale = 300 / list_total` pixels per unit of currency. With N bars, slot = 720 / N,
bar width = slot − 60, bar i at `x = 40 + i*slot + 30`. The first bar (`dg-bar--light`)
runs from `y = 380 − list*scale` to 380. Each discount bar (`dg-bar--quiet`) hangs from
the running total: `y = 380 − running*scale`, `height = discount*scale`. The final bar
(`dg-bar--focal`) is the offered fee from `y = 380 − fee*scale` to 380. Join each bar's
top to the next with a dashed `dg-line dg-line--dash`. Put each value 16px above its
bar's top edge. Check that list minus the discounts equals the fee exactly.

**Recipe B: positioning quadrant** (viewBox 792 by 440). Plot rect at x 40 to 760,
y 40 to 392, dashed midlines at x=400 and y=216, the target quadrant filled with
`dg-area`, the y-axis title at (40, 24), the x-axis title right-aligned at (760, 420).
Each bidder is a `dg-dot--quiet` (r=8) with a `dg-name` label 16px to the right and an
optional `dg-sub` 22px below it. Us: `dg-dot--focal` (r=12) with a `dg-name--focal`
label. Keep every label inside its own quadrant. Axes must be criteria the RFP actually
weights, and the source line must say the positions are our assessment.

**Other forms** that fit the shell: a horizontal bar chart of requirement coverage or
evaluation criteria (`grow-x` bars, labels left, values right), or a timeline of
milestones (a `dg-baseline` with `dg-dot`s, labels alternating above and below).

## Before you finish

- `build_deck.py` printed `deck OK` and the file is at `/mnt/session/outputs/pitch-deck.html`.
- Five slides, the titles alone tell the story, and every slide after the cover has notes.
- Every figure matches the docx: price, discount, term, payment terms, positions.
- At most two copper marks per slide, and nothing in a diagram overlaps or leaves its viewBox.
