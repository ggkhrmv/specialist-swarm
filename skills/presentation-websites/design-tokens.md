# Token reference

Every value in `template.html` lives in `:root` under these names. Components use the names only. Lines marked `BRAND:` in the template are filled from the brand kit (`brand-kit.md`), and everything else derives from them. The shipped values are neutral placeholders.

## Colour

| Token | Role |
|---|---|
| `--color-brand-100` | Brand tag background, light fills |
| `--color-brand-200` | Light tint for chart series and fills. Never body text on white |
| `--color-brand-300` | The signature colour: primary action, focus ring, accent bars, **the one highlight** |
| `--color-brand-400` | Hover, pressed, selection, text links |
| `--color-brand-500` | Deepest shade, the base layer of gradients |
| `--color-neutral-100` | Card and band background |
| `--color-neutral-200` | Hairlines, dividers |
| `--color-neutral-300` | Non-text UI only. It usually fails contrast as text |
| `--color-neutral-400` | Minimum colour for readable secondary text |
| `--color-neutral-500` | Secondary body text |
| `--color-white` / `--color-black` | Primary surfaces and text. Black is also the inverse tile |
| `--color-accent-1…3` | Data visualisation only, under 5% of a layout |
| `--color-{success,warning,critical,info}-{100,300,400}` | Status ramps: 100 background, 300 fill, 400 text/border |

**Semantic layer.** Components reference `--global-text-body-color-{primary,secondary,tertiary,inverse}`, `--global-text-headline-color-{primary,inverse}`, `--global-background-{primary,secondary}`, `--global-surface-color-100`, `--global-border-color-{200,focus}`, `--global-actioncolor-primary-{rested,hover}` and `--color-link`. Re-point these to change a role without touching components.

**Proportion.** 60–70% neutrals, 30–40% brand ramp, under 5% accents. The brand colour marks the brand's presence or a key moment once per layout, plus interactive elements. It is never chrome, decoration or a large fill.

**Contrast (WCAG 2.2 AA).** Body text 4.5:1. Large text (24px+, or 18.66px+ bold) 3:1. Icons, UI borders and focus rings 3:1. Check every text and background pair *as rendered*: text inside a card inherits its colour while the card changes the background. If `brand-300` fails as text on white, use `brand-400` for text. On dark or brand surfaces, text is white.

## Typography

- `--font-brand`: the brand family first, then **one** named fallback (`"Brand Sans", Arial, sans-serif`). `--font-display` is an optional second face for pull-quotes.
- Weights: `--font-weight-light`, `--font-weight-regular`, `--font-weight-strong`. Use only weights you embedded. Headings and `<strong>` use strong. Body, buttons, nav, tab labels and legends use regular, and selection shows as a border or check, never as weight.
- Tracking: `--tracking-heading` (tighten for geometric sans faces, e.g. -0.03em to -0.05em) and `--tracking-body`.
- Headings: line-height 1.1, sentence case, **no trailing period**, left-aligned, `text-wrap: balance`, `overflow-wrap: anywhere`.
- Fixed scale, switched at 720px. No `clamp()`:

| Token | Desktop | Mobile | Class |
|---|---|---|---|
| `--fs-display` | 80 | 40 | `.display` |
| `--fs-h1` | 64 | 36 | `.h1`, headline numbers |
| `--fs-h2` | 48 | 28 | `.h2` (section heads) |
| `--fs-h3` | 28 | 20 | `.h3` |
| `--fs-h4` | 24 | 20 | `.h4` |

- Body: `.lead` 22/32 (18/24 mobile), `.body` 18/24, base 16/24, `.small` 14/20. The minimum is 16px for body copy and 14px for labels, buttons and nav. Use 12px only for chart axes, tooltips and tags.
- Line length 40–75ch (`.measure` = 62ch). Apply `.measure` to text, **never to `.wrap`**, because that re-centres the block and breaks left alignment. `text-wrap: pretty` on paragraphs.
- If the brand's type scale differs, change the `--fs-*` values; the classes follow.

## Space, borders, layers, motion

- Spacing: 4px base, `--space-1` (4) … `--space-24` (96).
- Borders: `--border-xs` 1px (hairlines, buttons), `--border-sm` 2px (focus ring, nav and tab underline), `--border-md` 4px (card accent bar, insight border). Solid only.
- Corners: `--corner`, one value everywhere (0 by default). Round only spinners and avatar crops.
- Shadows: none by default. `--shadow-md` is for floating UI (tooltip, back-to-top). Never on cards.
- z-index: `--z-base` 0 · `--z-raised` 10 · `--z-nav` 100 · `--z-dropdown` 200 · `--z-sticky` 300 · `--z-scrim` 400 · `--z-modal` 500 · `--z-toast` 600 · `--z-tooltip` 700. Only the header is sticky at `top: 0`. Any other sticky element is offset by `--header-h`.
- Motion: `--duration-fast` 150ms · `--duration-moderate` 300ms · `--duration-slow` 700ms; `--easing-standard`, `--easing-slow`. Animate only `background`, `border-color`, `color` and `transform`. No opacity fades except on scrims. Never `transition: all`. The reduced-motion override is required.
- Focus ring: 2px solid `--global-border-color-focus`, offset 2px. White on gradient, brand and black surfaces. Never `outline: none`.

## Layout

| Tier | Width | Margin (`--pad`) |
|---|---|---|
| Small | 320–719 | 16 |
| Medium | 720–1279 | 24 |
| Large | 1280+ | 40 |

Content max width `--maxw` 1280. Header `--header-h` 72 (56 mobile), sticky, white, with a 1px bottom rule. `html{scroll-padding-top}` matches the header. Touch targets are at least 44px. Grid tracks that can hold images or long words use `minmax(0, 1fr)`, never bare `1fr`.

## Gradients

Radial only, built from brand tokens, white text on top. No glows or streaks layered on top. At most **one** gradient surface per page: the hero *or* the CTA band. If the brand ships an official gradient image, inline it via `asset:` and never mix it with a CSS gradient on one element. Solid `brand-500` is the fallback.

## Data visualisation

`--dv-cat-1…7` is the categorical order: brand, neutral, accent, tint, black, accent, light neutral. Never reorder or skip it. `--dv-bar-primary` is for single-series bars, and every bar gets a 1px `--dv-bar-outline`. A brand-derived palette rarely passes a colour-blind check, so validate it with the `dataviz` skill and never let identity rest on colour alone: use direct labels.
