# Brand kit: what to collect, and where each input goes

The template ships with **neutral placeholder values**. It is a scaffold, not a brand. Collect these inputs before composing, and map each one to its slot. Wherever you fill a gap yourself, say so in the report.

## Checklist

| # | Input | Ask for | If missing | Slot |
|---|---|---|---|---|
| 1 | **Primary colour ramp** | The signature colour plus official tints and shades | Derive 100 (light tint), 200, 300 (the given colour), 400, 500 (deepest) from one hex and **flag it** | `--color-brand-100…500` in `:root` |
| 2 | **Neutrals** | The brand's grey scale, white to black | Keep the template's warm-neutral ramp, or cool it to match the brand; flag it | `--color-white`, `--color-neutral-100…500`, `--color-black` |
| 3 | **Accent colours** | 1–3 secondary colours | Leave the placeholders, use them only in charts, and validate with `dataviz` | `--color-accent-1…3`, `--dv-cat-*` |
| 4 | **Font family + files** | The font name, the `woff2` (preferred) or `ttf` files, and the weights in use | Ask. If the brand truly has no custom font, choose **one** named fallback family and say so | `--font-brand`; files in `assets/fonts/`; `FONT_FAMILY` + `FONTS` in `embed-fonts.py` |
| 5 | **Weights** | Which weights the brand uses for headings, body, UI | 300 / 400 / 600 | `--font-weight-light/regular/strong` (only weights you embed) |
| 6 | **Display face** *(optional)* | A serif or display face for pull-quotes | Reuse the brand font | `--font-display`; `FONT_FAMILY_DISPLAY` in `embed-fonts.py` |
| 7 | **Logo** | The full logo as SVG, plus a compact mark if one exists, and the light/dark variants | Ask for the SVG, or an image you can trace. **Never** redraw it as styled text | LOGO SLOT in the header (`.logo`) and footer (`.logo-mark`) |
| 8 | **Logo rules** | Minimum size, clear space, approved colourways, co-branding rules | Keep it unboxed and unaltered at a sensible size; flag it | `.logo` / `.logo-mark` height; `.cobrand` gap |
| 9 | **Corner policy** | Square or a specific radius | Square (`0`) | `--corner` |
| 10 | **Icon set** | The brand's icon library, if it has one | Material Symbols Outlined (in the sprite, Apache-2.0) | Replace the `<symbol>` paths and keep the ids |
| 11 | **Text link colour** | If the brand specifies one | `--color-brand-400` | `--color-link` |
| 12 | **Gradient** | An official gradient image or recipe | Radial from the brand ramp (in the template) | `.hero` / `.cta` background, or `asset:gradient.png` |
| 13 | **Footer / legal line** | Copyright, disclaimer, required legal links | "© <year> <Brand>." plus "Figures shown are illustrative." while placeholders remain | The footer `BRAND:` comment |
| 14 | **Voice rules** | House style: spelling (US/UK), number and date formats, banned words | Plain, active and specific; US conventions; flag it | Copy; see `review-checklist.md` → Copy |
| 15 | **Guideline source** | A brand guideline PDF, `design.md` or token file | — | Read it first. **It wins on any conflict.** Flag mismatches; never patch them silently |

## Deriving a ramp from one colour
Keep the hue, and step lightness and chroma: 100 is a near-white tint for fills and tag backgrounds, 200 is a light tint (never body text), 300 is the given colour, 400 is about 15–20% darker (used for hover and pressed), and 500 is the deepest (the base of gradients). Check white text on 300, 400 and 500, and 300 as text on white (see `design-tokens.md` → Contrast). If 300 fails as text on white, use 400 for text and links, and say so.

## Logos
- Paste the exact SVG. Keep its `viewBox`. Add `class="logo"`, `role="img"` and `aria-label="<Brand>"`.
- Use `fill="currentColor"` for the parts that should flip on dark surfaces. Keep fixed brand colours on the parts that must never change.
- The full logo goes top-left on first contact and the compact mark in the footer. Never box, recolour, tint, stretch or fade it.
- A logo glyph (a chevron, a dot, a symbol) is never reused as an arrow, bullet or decoration.
- **Co-branding** (partner or client logo next to the brand's) needs written approval from the partner. Use the commented `.cobrand` lockup and follow both brands' clear-space rules, with neither logo dominating.

## Fonts
1. Drop the files into `assets/fonts/` (next to `embed-fonts.py`) or pass `--fonts DIR`.
2. In `embed-fonts.py`, set `FONT_FAMILY` to the exact family name used first in `--font-brand`, and list each file with its weight and style. Embed only the weights the page uses, because each face adds 30–60 KB.
3. Check the licence: embedding a font in a distributed HTML file is web-font use. Make sure the brand's licence covers it. **Never commit licensed font files to a public repository.**

## Recording overrides
When the brand forces a change to a framework default (rounded corners, a dark-first brand, a different weight set, a link colour), set the token once and add one line to the report: `Override: --corner 8px (brand is rounded)`.
