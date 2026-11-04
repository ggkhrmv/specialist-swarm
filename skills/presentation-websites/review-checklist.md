# Review checklist (run before saying "done")

The gate a page passes before delivery. Work through all eight parts. The page is done when every **Error** item passes, every Warning is fixed or listed for the user, and the report at the end is written. If the user supplied brand guidelines, run their rules too. They win on any conflict.

## 0. Pre-emit self-critique (before the sweep)
Score the built page 1–5 on each axis. Anything **below 3 triggers a revision** before the rest of this checklist. Two passes is normal. A third pass usually means the brief is wrong, not the design, so re-read it.

| Axis | Question |
|---|---|
| **Point** | Is there one clear position the page takes, stated in the first screen? |
| **Hierarchy** | Can a reader tell in two seconds what is primary, secondary and tertiary? |
| **Execution** | Are rule weights, accent footprint, wrapping, focus rings and contrast all in spec? |
| **Specificity** | Does it look and read like *this* brief, or like a page that could be about anything? |
| **Restraint** | Has everything that isn't earning its place been removed? Is the boldness in one place? |
| **Variety** | Do section forms vary down the page? Would a generic page on this brief share this plan? |

## 1. Brand compliance

Errors:
- Every colour, spacing value, border, corner, shadow, z-index, duration and easing is a `:root` token. There are **no raw hex, `rgb()`, `hsl()` or `oklch()` values outside `:root`**. Check with `grep -nE '#[0-9a-fA-F]{3,8}\b|rgb\(|hsl\(|oklch\(' file.html` and confirm every hit sits inside `:root` or a logo SVG.
- Every `BRAND:` slot is filled from the kit, or the default is flagged in the report. No placeholder value ships as if it were the brand.
- Font weights are only the embedded ones. Font sizes come from the scale. Nothing below 14px except chart axes, tooltips and tags (12px).
- One corner value (`--corner`) everywhere except spinners and avatar crops.
- Borders are solid, 1px or 2px (4px only for accent bars and insight borders). No shadows on cards.
- At most one gradient surface. No glows, streaks or gradient text. No two dark or gradient sections touching. At most one inverse tile per group.
- One primary button per view. On gradient or black surfaces, the primary CTA is inverse secondary.
- The logo is the real SVG, unboxed and unaltered, top-left, with the compact mark in the footer. Nothing in the placeholder dashed boxes remains.
- One icon set from the sprite. No hand-drawn icons, emoji or text-glyph arrows.
- Accent colours appear only in data visualisation.
- SVG `<text>` uses the brand font token. `grep -o 'font-family="[^"]*"' file.html | sort -u` returns only brand tokens.
- Every artifact in a multi-file set carries the same brand kit.

Warnings:
- The brand colour is the one highlight per layout (60–70% neutral, 30–40% brand ramp).
- Eyebrows: none, or one per page in sentence case. No uppercase labels anywhere (`grep -n 'uppercase' file.html`).
- Charts follow `components.md` → Data visualisation.
- Header 72px with a 1px rule. Footer white, no top border. Content max width 1280.

**Fixer sweep.** For each raw value in a colour, spacing, font, border, shadow, z-index or timing property, replace it with the matching token, changing only that value. Anything without an exact token match is listed as **Unresolved**. Never force it onto the nearest step and never leave it as a silent comment. Search for raw values again at the end.

## 2. Slop gates (each answer must be "no")
1. Is the display font a default system or generic face because the brand font failed to embed?
2. Is there gradient text, a glow blob, or a radial "aura" behind the hero?
3. Is everything in the hero (meta, headline, lead, CTA) centred on one axis?
4. Is there a row of three identical icon-above-heading cards that isn't three genuinely parallel things?
5. Is any card nested in another card, or carrying a thick coloured side stripe?
6. Is there an uppercase eyebrow, a label beside its heading, or `01 / 02 / 03` on content that isn't a sequence?
7. Is one word in a headline highlighted in a different colour or weight for emphasis?
8. Is there any decorative element (badge, sticker, shape, ornament) with no meaning behind it?
9. Is there a number the user didn't supply and that has no source?
10. Is there re-drawn browser, phone, terminal or IDE chrome?
11. Is there fade-and-slide-up on every section, or hover-lift on every card?
12. Does any button, nav link or tab label wrap to two lines anywhere between 320 and 1920px?
13. Does a grid track that holds an image or long word use bare `1fr` instead of `minmax(0, 1fr)`?
14. Is there a second element sticky at `top: 0` that will slide under the header?
15. Does any CTA say "Get started", "Learn more" or "Submit" instead of what happens?

## 3. Accessibility (WCAG 2.2 AA)

Errors:
- Contrast as rendered: body text 4.5:1, large text 3:1, UI parts and focus rings 3:1. Brand colour as text only where it passes. Never neutral-300 for text.
- A visible focus ring on every control: 2px brand colour with a 2px offset, white on gradient and black.
- Keyboard: every control is a real `<button>` or link, no `tabindex` above 0, and hidden panels use `hidden`. Tabs have roles plus arrow keys, Home and End. The accordion has `aria-expanded` and `aria-controls`.
- The reduced-motion override is present, and demos land on their final state under it.
- Autoplay finishes within 5s or has a pause control. Nothing flashes more than three times a second.
- Exactly one `h1`, no skipped heading levels, landmarks (`header`/`nav`/`main`/`footer`), and a skip link first.
- Images have alt text. Decorative SVG is `aria-hidden="true" focusable="false"`. Charts are a `<figure>` with `role="img"` and an `aria-label` that carries the values.
- Disabled controls use `aria-disabled="true"` so focus is not lost.
- No `user-scalable=no`. Text reflows at 200% zoom. No `px` font size on `html`.
- Primary touch targets are at least 44px.

## 4. Copy
- Sentence case for every heading, button, label and tab. Headlines have no trailing period and make a claim.
- Plain, active and specific. Lead with what the reader gains, and back each claim with proof. Define a term the first time it appears. One crisp line beats a paragraph.
- Name things the way the reader would, not the way the system is built. An action keeps one name through the whole page.
- Consistent conventions (from the brand's house style, or US by default): dates, currency, "%" with numerals, an en dash for ranges (6–8 weeks), no ampersand or "+" for "and", no exclamation marks.
- Lists are introduced with a colon, parallel, with each item capitalised.
- Audience questions (quizzes, polls) never give the answer away in the prompt.
- When the author's name is on the page, run `humanizer`, `voice` and `writing` if they are installed, and apply the house bans: no em dashes, no "X, not Y" constructions, no reflexive groups of three, no punchline closers, no signposting ("Let's dive in").
- **Machine tell-scan:** grep the visible text for em dashes, "X, not Y", the AI-vocabulary watchlist (delve, unlock, seamless, leverage, robust, game-changer, elevate, empower, journey) and signposting openers. Report the counts.

## 5. Honest numbers
- Every figure is sourced (fact-checked against the primary source; a research sub-agent is fine for this), or visibly labelled as illustrative or a placeholder. Never ship an invented metric.
- Illustrative calculations state their assumptions on the page in one line.
- Prices, limits and policy facts carry their date ("list prices, October 2026").

## 6. Self-contained
- `python3 embed-fonts.py file.html` printed `self-contained OK` and embedded the brand faces and every `asset:` image. If it printed `NO FONTS EMBEDDED`, the brand deliberately has no custom font and the report says so.
- No external `src`, `url()`, `<link>` or `@import`. Outbound `href` links are fine, and they open in a new tab with `rel="noopener"`.
- Large screenshots were shrunk before embedding, and each image is embedded once.

## 7. Render and click through
Use `agent-browser`, Playwright, or headless Chrome/Edge on the built file:
- Screenshot each section at **1440×900**, **1280×800** (hero fit) and **375×800**. With `html{scroll-behavior:smooth}`, set it to `auto` before scripted scrolling, or the screenshots land mid-scroll. Some headless browsers enforce a minimum window width, so measure the viewport, don't trust the screenshot size.
- `document.documentElement.scrollWidth` equals the viewport width at 375 (no sideways scroll).
- Check that the brand font actually rendered (`document.fonts.check('16px "Brand Sans"')`, or compare a heading against the fallback), and that no icon shows as tofu.
- Click through every interactive part: Replay, Next step to the end, every tab plus keyboard Home/End, every quiz answer and restart, every accordion item, Copy. Confirm the console logged no errors.
- Look for: two dark or gradient bands touching, cramped or orphaned headings, text over 75ch, a chart without labels, and an `asset:` reference that didn't resolve.

## Report (end of every build)
A short summary in the chat: what was built, the key decisions and why, every brand override and every flagged default. Then:

```
Critique: P_ H_ E_ S_ R_ V_          Brand: X errors · X warnings · X passed
Slop gates: X/15 pass                Accessibility: Passes AA / Fails AA
Copy: tell-scan em dashes 0 · X-not-Y 0 · watchlist 0
Self-contained: OK (N KB, F font faces, I images)
Rendered: 1440 + 1280 + 375, interactions clicked, 0 console errors
Flagged defaults: … (brand inputs you derived or assumed)
Unresolved: … (anything you could not fix, and why)
```

Then hand the visual pass to the user with a specific list of what to look at: that the brand font rendered rather than falling back, that the logo sits correctly, the one bold element, and the section rhythm. The visual judgement is theirs, and "please eyeball it" is not a handoff.
