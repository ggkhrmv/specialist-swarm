# Interactive components

Everything here is live in `template.html`: the CSS in its "DEMO STAGE", "STEPPER", "QUIZ", "COPY BLOCK", "ACCORDION" and "BACK TO TOP" blocks, the behaviour in its single `<script>`. Copy the markup and keep the data attributes; the script finds them, so no page-specific JS is needed. All of it is vanilla and offline.

## When an interaction earns its place

A demo earns its place when the motion shows **cause and effect**: something accumulates, loads, moves through steps, or changes because of an action. Use it for the one or two ideas per page that are easier to see than to read. Everything else stays static. A page is presented live and also read afterwards as a leave-behind, so every demo must:

- **play once on reveal**, finish within 5 seconds (WCAG 2.2.2: longer autoplay needs a pause control), and read correctly in its final state,
- offer **Replay**, and for anything with steps a **Next step** button so a presenter can walk through it live,
- land on the **final state instantly** under `prefers-reduced-motion` or without IntersectionObserver.

## Sequenced demo — `[data-seq]`

One container plays a timeline of numbered steps.

```html
<div data-seq data-seq-gap="1000">                    <!-- ms between steps -->
  <button class="btn btn-ghost btn-sm" type="button" data-replay><span class="lbl">Replay</span></button>
  <button class="btn btn-tertiary btn-sm" type="button" data-seq-next><span class="lbl">Next step</span></button>
  <li class="seq-item" data-at="1">Lights up at step 1</li>
  <b data-values="0,20100,41800,65100">65,100</b>                    <!-- one value per step, tweened -->
</div>
```

| Attribute | Meaning |
|---|---|
| `data-seq` | The timeline. Plays once when 15% of it is visible. |
| `data-at="n"` | Gets `.is-on` from step `n` onwards. `data-at="0"` is visible from the start. |
| `data-values="a,b,c"` | Shows value *k* at step *k*, tweened. The last value is the static fallback text. Decimals follow the last value (`0.31` → 2 decimals). |
| `data-replay` | Restarts from step 0 and autoplays. |
| `data-seq-next` | Advances one step and stops autoplay. Gets `aria-disabled="true"` at the end (never `disabled`, which drops keyboard focus). |
| `data-seq-gap` | Milliseconds per step (default 800). Count-ups use ~70–90 with 10 steps. |
| `data-seq-steps` | Forces the step count, e.g. a count-up with no `data-at` items. |

**Count-up stat** is the same component: put `data-seq data-seq-gap="70" data-seq-steps="10"` on the stat grid and `data-values` on each number (see `#impact` in the template).

**States, not fades.** Items are always in the DOM and *light up*: `.seq-item` goes from neutral-200 text and border to black text with a brand-coloured left border (a colour and border-colour change). Movement, where needed, is `transform` only. Because the final state is a real state, a reader who scrolls past the animation, prints the page or uses reduced motion still sees everything.

**Charts inside a demo** follow `components.md` → Data visualisation and the `dataviz` skill: no draw-in animation, 1px outline on every bar, values as labels. A demo may reveal one chart row per step (the row lights up), which is a state change, not a chart animation.

**Recipes that worked** (build them from these primitives):
- *Today vs. the new way*: two lanes, steps lighting up with a day counter each (`#journey` in the template).
- *Context that accumulates*: a conversation where each turn lights up beside a per-turn row and a running total. Shows that each turn re-reads everything before it. For chat mock-ups: no bubbles, left-aligned messages, a small square avatar in `brand-400` with a white sparkle icon (never the brand logo), and no fake app chrome around it.
- *Layered loading*: items light up in order with a running "loaded" total, while the unused items stay dim.

Demos sit on a light `.band`. Do not mix light and dark modes in one layout. A dark surface is only right when the thing being depicted is itself dark (a terminal, say), and then it uses `neutral-500` with white text and `neutral-400` borders.

## Stepper and tabs — `[data-stepper]`

```html
<div data-stepper>                                     <!-- data-stepper="tabs" = plain tabs -->
  <div class="steptabs" role="tablist" aria-label="How it runs">
    <button class="steptab" role="tab" type="button" id="st-t1" aria-controls="st-1" aria-selected="true"><b>1</b><span>Discover</span><span class="sr-only"></span></button>
    <button class="steptab" role="tab" type="button" id="st-t2" aria-controls="st-2" aria-selected="false" tabindex="-1"><b>2</b><span>Define</span><span class="sr-only"></span></button>
  </div>
  <div class="steppanel" role="tabpanel" id="st-1" aria-labelledby="st-t1" tabindex="0">…</div>
  <div class="steppanel" role="tabpanel" id="st-2" aria-labelledby="st-t2" tabindex="0" hidden>…</div>
  <button class="btn btn-ghost btn-sm" type="button" data-step-prev><span class="lbl">Back</span></button>
  <button class="btn btn-tertiary btn-sm" type="button" data-step-next><span class="lbl">Next step</span></button>
</div>
```

- Arrow keys, Home and End move between tabs; the panel slides in 8px (transform only).
- In stepper mode, earlier tabs get `.is-done` and their empty `.sr-only` span reads "(done)". In `data-stepper="tabs"` mode, nothing is marked done. Use tabs mode for a gallery or explorer (one card per item, click a figure to open its card), stepper mode for a sequence.
- Tabs can sit in more than one `role="tablist"` inside the same container (e.g. two labelled groups of an explorer).
- On narrow screens the step labels collapse to visually hidden text; the accessible name stays.
- A stepper is the right home for a build-up method: each step shows *what you send* (a copy block) beside *what comes back*, with a one-line "why this step" underneath.

## Quiz — `[data-quiz]`

One question at a time. Pick, see why, go next; a final "pattern" card and a restart.

```html
<div class="quiz" data-quiz>
  <p class="quiz__progress" data-quiz-progress></p>
  <div class="quiz__q" data-quiz-q>
    <p class="quiz__prompt">"Statement to judge."</p>
    <div class="quiz__opts">
      <button type="button" class="btn btn-tertiary quiz__opt" data-correct="myth"><span class="lbl">Myth</span></button>
      <button type="button" class="btn btn-tertiary quiz__opt" data-correct="fact"><span class="lbl">Fact</span></button>
    </div>
    <div class="quiz__exp" data-answer="myth"><strong>Myth.</strong> One or two sentences on why.</div>
  </div>
  <div class="quiz__done" data-quiz-done hidden>…<button type="button" data-quiz-restart>Start over</button></div>
</div>
```

The prompt never hints at the answer. Mix the answers (not all "Myth"). Each explanation starts with the verdict in words ("Myth.") so the result never rests on the green or red alone, then states the mechanism.

## Copy block — `[data-copy]`

For anything the reader should reuse: a prompt, an agenda, a snippet.

```html
<div class="copyblock">
  <div class="copyblock__bar"><span>Step 2 prompt</span><button class="btn btn-tertiary btn-sm" type="button" data-copy="#p-2"><span class="lbl">Copy</span></button></div>
  <pre id="p-2">Text to copy. [placeholders in brackets]</pre>
</div>
```

Success is silent: the label reads "Copied" for 1.6s and a hidden `role="status"` line announces it. The bar label is sentence case, not an uppercase kicker.

## Shared images — `[data-img-from]`

Embed an image once, reuse it anywhere:

```html
<img src="asset:analyst.png" alt="Analyst agent" id="img-analyst">   <!-- inlined by embed-fonts.py -->
<img data-img-from="#img-analyst" alt="">                            <!-- reuses it at runtime -->
```

A figure gallery that shows each picture twice (thumbnail plus card) halves its file size this way.

## Accessibility contract (every interactive piece)

- Real `<button type="button">` for every control, at least 44px tall where it is a primary touch target; visible `:focus-visible` ring (2px brand colour, 2px offset; white on gradient or black), never animated in.
- Disable with `aria-disabled="true"` plus an ignored click, so focus is never lost mid-presentation.
- Decorative SVG: `aria-hidden="true" focusable="false"`. Arrows in button text sit in `<span aria-hidden="true">`.
- A row of meter dots or a chart without text: `role="img"` with an `aria-label` that says the value.
- Do not put `aria-live` on a demo whose items already sit in the DOM; it announces nothing useful.
- Data tables: `<caption>` (can be `.sr-only`), `scope="col"` and `scope="row"`.
- Motion: `background`, `border-color`, `color` and `transform` only, token durations (150/300/700ms) and `--easing-standard`. No opacity fades. The required reduced-motion rule in the template collapses everything.
- One `h1`, no skipped heading levels, landmarks `header` / `nav` / `main` / `footer`, and a skip link first.
- `html{scroll-padding-top}` matches the sticky header, so anchor jumps don't hide headings.
- External links in a page that is presented live open in a new tab: `target="_blank" rel="noopener"`.

## Accordion — `[data-accordion]`

```html
<div class="accordion" data-accordion>
  <div class="acc__item">
    <h3><button class="acc__btn" type="button" aria-expanded="false" aria-controls="acc-1" id="acc-b1">Question<svg class="icon" aria-hidden="true" focusable="false"><use href="#i-expand-more"/></svg></button></h3>
    <div class="acc__panel" id="acc-1" role="region" aria-labelledby="acc-b1" hidden>Answer.</div>
  </div>
</div>
```

One item open at a time. Enter and Space work because the trigger is a real button. Use an accordion for genuinely secondary content (FAQs, detail a presenter may skip), never to hide the main argument.

## Back to top — `[data-to-top]`

One `<button class="to-top" data-to-top aria-label="Back to top">` per page, only on pages taller than about four screens. It slides in after 300px (a sentinel watched by IntersectionObserver, no scroll listener) and moves focus to `<main tabindex="-1">` after scrolling.
