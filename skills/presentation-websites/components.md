# Component and pattern library

Every component below is live in `template.html`. Copy it from there, change the copy and structure freely, and keep the tokens. Interactive behaviour (sequenced demos, stepper, quiz, accordion, copy, shared images) is documented in `interactions.md`. The demo content in the template is fictional. Replace all of it.

## Page rhythm

Structure it like a website: no fixed order, no slides, no next-slide navigation. Compose sections around the story, and **vary the section form** so the page never repeats head → three cards → callout. Alternate white and `.band` (neutral-100) sections, and change the head between `.head-split` and a plain stacked head.

- Light is the default mode. Do not mix light and dark modes in one layout.
- Sanctioned accents: **one** gradient surface per page (the hero *or* the CTA band), and **one** inverse tile (black, white text) per group.
- The brand colour appears once per layout as the highlight, plus on interactive elements.
- Structure is information. A divider means the content changed. A number means a sequence. A border means a group. Decoration with no meaning behind it gets cut.

## Header
Sticky, white, `--header-h` (72px, 56px mobile), 1px neutral-200 bottom rule, `z-index: var(--z-nav)`. The full logo goes top-left in the LOGO SLOT. Up to six anchor links, right-aligned, 14px regular, black, on one line (`white-space: nowrap`), with a 2px brand underline that grows on hover and marks the active section (scroll-spy). Below 1024px the links hide; add a menu only if the page needs one. Nav labels are short nouns ("Approach"), never two lines.

**Co-brand lockup** (commented out in the header): brand logo, a 1px neutral-200 vertical separator, then the partner logo. It needs the partner's written approval. Follow both brands' clear-space rules.

## Section heads
The headline carries the point. Sentence case, no trailing period. Write action titles (a claim), not topic labels ("Most of the three weeks is waiting", not "Current state").
- `.head-split`: headline left, lead right. The default for content sections.
- Plain stacked head (`h2` then `.lead`) to vary the rhythm.
- `.meta-line` above the page title gives context (document type, date, stage).
- `.eyebrow` exists but is **opt-in, at most once per page**, for genuinely chaptered content. 14px strong, neutral-400, sentence case, stacked directly above its heading, never beside it.

## Intro band (default opener)
Calm and light: meta line, `.h1`, `.lead`, and an optional `.intro-meta` row (14px neutral-400 key, 20px strong value, top rule). Open with the most characteristic thing about the subject. Use a hero only if a cover genuinely earns its place.

## Hero / cover (optional)
A radial brand gradient with white headline and lead. Buttons on it are inverse: the primary CTA is `.btn-inv-secondary` (white fill, black text) and supporting actions use `.btn-inv-tertiary`. If the page has a hero, the CTA band at the end goes light (a `.band` with a `.btn-primary`) so there is only one gradient surface. Check at **1280×800** that the headline, lead and primary CTA all fit above the fold. Don't centre everything. Don't add ornaments that mean nothing.

## Buttons
| Class | Variant | Where |
|---|---|---|
| `.btn-primary` | Brand fill | Light surfaces, **one per view** |
| `.btn-secondary` | Black fill | Light surfaces |
| `.btn-tertiary` | 1px black border, brand label | Supporting actions, quiz options, stepper nav |
| `.btn-ghost` | Label only | Low-emphasis actions (Replay, Back) |
| `.btn-inv-secondary` | White fill | Primary CTA on gradient or black |
| `.btn-inv-tertiary` | Neutral-400 border, white label | Supporting action on gradient or black |

Sizes: `.btn-lg` 64, default 48, `.btn-sm` 32. Labels are regular weight inside `<span class="lbl">`, whose underline grows on hover. Group order left to right: ghost, tertiary, primary, with an 8px gap. A trailing icon is optional (`#i-arrow-forward`, 20px) and doesn't slide. To disable, use `aria-disabled="true"` (keeps focus). Labels name what happens ("Book the session", not "Submit" or "Learn more") and never wrap to two lines.

## Two-column + feature list
`.cols`: a headline beside a wider body column. `.feature-list` items: a check icon in brand colour plus text, with hairline rules between items. Bold the first phrase of each item so the list scans.

## Headline numbers
`.stat-grid` of neutral-100 tiles: the figure on the heading scale (`--fs-h1`, strong, black, tabular numerals), an 18px strong label and a 14px caption that says what was measured and where it came from. One tile may be `.stat--inverse` (black). Numbers count up once on reveal via `[data-seq]`. **Every number is sourced or visibly labelled illustrative.** A stat slot with no real number gets cut, not filled. Solid figures only, never gradient text.

## Insight callout
`.insight`: a 4px brand left border, a sparkle icon, and one or two sentences that state the so-what of the numbers or chart above it. Use at most one per section.

## Demo stage (light)
A `.band` section holding a sequenced demo: `.lanes` of white panels, `.seq-item` rows that light up (a colour and left-border state change) as the timeline plays, counters on the heading scale, and Replay / Next step controls. At most one brand-coloured counter. Recipes are in `interactions.md`.

## Before / after panels
`.panel` (neutral-100) beside `.panel.is-after`, which is the section's inverse tile (black, white text). The label is 14px strong, sentence case.

## Stepper / tabs
`.steptabs` with numbered `.steptab` buttons: the label is 16px regular in neutral-400, black when selected, with a 2px brand underline. No fills. Done steps show a brand-coloured numeral. Use `data-stepper="tabs"` for plain tabs or a gallery/explorer. Only number tabs that are really a sequence.

## Cards
`.card`: neutral-100 background, 32px padding, `--corner`, no shadow. A 4px brand accent bar grows from the **bottom** on hover and on keyboard focus. An optional 40px icon in brand colour, an `.h4` title and `.body` copy. No dividers inside cards. Card actions are ghost or secondary, never primary. Never nest a card in a card. A row of three identical icon cards is the most generic layout there is, so use one only when the content really is three parallel things.

## Tags
`.tag` (neutral-100) and `.tag--brand` (brand-100): 24px high, 12px regular, sentence case, non-interactive.

## Accordion
`[data-accordion]`: `<h3><button class="acc__btn" aria-expanded aria-controls>` headers and 1px neutral-300 rules that turn brand-coloured on hover. The chevron rotates. One item is open at a time.

## Quiz
`[data-quiz]`: one statement at a time on a white card, tertiary option buttons, and the explanation in an insight-style box. See `interactions.md`.

## Copy block
`.copyblock`: a neutral-100 bar with a sentence-case label and a Copy button, with the text in a `<pre>`. See `interactions.md`.

## CTA band
The page's one gradient surface (unless the hero has it). White `.h2` and `.lead`, then inverse tertiary followed by inverse secondary. The headline names the next step and the lead says what happens in it.

## Footer
White, at least 88px tall, 40px padding, no top border. The compact mark in its LOGO SLOT and a short legal line. Add 2–4 sentence-case legal links only when they are real. Not the generic four-column link footer: a presentation page has nothing to fill it with.

## Back to top
`[data-to-top]`: fixed bottom-right, white, 1px border, `--shadow-md`, brand-coloured icon and label. It slides in after 300px of scroll. Use it only on pages taller than about four screens.

## Icons
One set, inline sprite: `<svg class="icon" aria-hidden="true" focusable="false"><use href="#i-check"/></svg>`. Sizes `.icon-20`, default 24, `.icon-32`, `.icon-40`. The default set is Material Symbols Outlined (Apache-2.0): target, growth, gear, bulb, globe, check, people, chart, doc, shield, clock, network, search, rocket, arrow-forward, arrow-back, arrow-up, replay, copy, close, expand-more, expand-less, open-in-new, sparkle, info. For another icon, copy its path from the Material Symbols Outlined SVG (24px, weight 400, unfilled) into a new `<symbol>`. If the brand has its own icon set, swap the paths and keep the ids. Never draw an icon, use emoji, or mix two libraries. Pair every icon with text.

## Data visualisation
Load the `dataviz` skill before writing chart code. Within this framework:
- Use the `--dv-cat-*` categorical order, never reordered or skipped. Single-series bars use `--dv-bar-primary`.
- Lines: max 3 series. Bars: max 4 categories per group, zero baseline, horizontal gridlines only, no 3D.
- **Every bar gets a 1px `--dv-bar-outline`**, and the chart always has a legend or direct labels. On a presentation page, show the values as direct labels so identity never rests on colour.
- Legend: dot + label list, 14px regular, in the same order as the data. Axis labels 12px minimum in neutral-400.
- No draw-in animation on charts. A sequenced demo may step through states (rows lighting up), which is not a chart animation.
- Wrap each chart in `<figure>` + `<figcaption>`, give it `role="img"` and an `aria-label` with the key values, and cite the source in the caption.

## Diagrams
Hand-built inline SVG diagrams (layers, flows, architectures) follow `diagram-spec`: computed geometry, orthogonal routing, labels that collide with nothing, and every `font-family` set to the brand token.

## Tables
The header row is neutral-100, 14px strong, sentence case. Body rows are separated by 1px neutral-200 rules, left-aligned, with no vertical borders and tabular numerals in number columns. Include a `<caption>` (it can be `.sr-only`) and `scope` on header cells.

## Quotes
Pull-quotes in `--font-display` at a heading size, black, with the attribution in 14px neutral-400. No decorative quote glyphs or brand symbols as quote marks. Quote real people only, with permission.

## Images
Real photography or screenshots in rectangular crops (`--corner`), with no brand-colour tint or overlay. Use illustration only from the brand's own library. Inline every image (`src="asset:…"`, embedded by `embed-fonts.py`) and embed each one once (`[data-img-from]` for reuse). Shrink screenshots before embedding. Show product UI as a real screenshot, never as re-drawn browser, phone or IDE chrome.
