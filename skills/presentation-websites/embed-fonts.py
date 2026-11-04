#!/usr/bin/env python3
"""
Make a presentation-website HTML file self-contained: embed the brand font(s) as base64
@font-face rules and inline every `asset:` image, then check for external references.

Usage:
    python3 embed-fonts.py path/to/site.html                 # edits in place
    python3 embed-fonts.py path/to/site.html out.html        # writes a copy
    python3 embed-fonts.py site.html --assets DIR            # images live somewhere else
    python3 embed-fonts.py site.html --fonts DIR             # font files live somewhere else

Fonts: set FONT_FAMILY and FONTS below to the brand kit (FONT_FAMILY must equal the first family
in --font-brand in the template's :root). Drop the woff2/ttf files into assets/fonts/ next to this
script. The script replaces the marker  /*__FONT_FACES__*/  in the file's <style>. Re-running is
safe: previously embedded faces for these families are removed and re-inserted.

If FONTS is empty the script skips fonts, says so, and still inlines images. Only do that when
the brand deliberately uses a system fallback; otherwise a missing font is a bug.

Images: reference them as  <img src="asset:photo.jpg">  and keep the files in an `assets/` folder
next to the HTML (or pass --assets DIR). Each one is inlined as a base64 data: URL. Embed each image
ONCE; reuse it elsewhere with <img data-img-from="#id-of-the-first-img"> (see interactions.md).
Shrink big screenshots first (e.g. macOS: `sips -s format jpeg -s formatOptions 82 --resampleWidth 1200`).
"""
import base64, os, re, sys

# ---------------------------------------------------------------------------- BRAND: fonts
FONT_FAMILY = "Brand Sans"     # must equal the first family in --font-brand
FONTS = [
    # (filename in assets/fonts/, font-weight, font-style). Embed only the weights the page uses.
    # ("BrandSans-Light.woff2",    300, "normal"),
    # ("BrandSans-Regular.woff2",  400, "normal"),
    # ("BrandSans-Italic.woff2",   400, "italic"),
    # ("BrandSans-Semibold.woff2", 600, "normal"),
]
# Optional second family (a display/serif face for pull-quotes, or a brand icon font).
FONT_FAMILY_DISPLAY = None     # e.g. "Brand Serif"; must equal --font-display
FONTS_DISPLAY = [
    # ("BrandSerif-Regular.woff2", 400, "normal"),
]
# ----------------------------------------------------------------------------

MARKER = "/*__FONT_FACES__*/"
FONT_MIME = {".woff2": ("font/woff2", "woff2"), ".woff": ("font/woff", "woff"),
             ".ttf": ("font/ttf", "truetype"), ".otf": ("font/otf", "opentype")}
IMG_MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".webp": "image/webp", ".gif": "image/gif", ".svg": "image/svg+xml"}
HERE = os.path.dirname(os.path.abspath(__file__))


def face(family, path, weight, style):
    ext = os.path.splitext(path)[1].lower()
    if ext not in FONT_MIME:
        sys.exit(f"unsupported font type: {path}")
    mime, fmt = FONT_MIME[ext]
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return (f'@font-face{{font-family:"{family}";font-weight:{weight};font-style:{style};'
            f'font-display:swap;src:url(data:{mime};base64,{b64}) format("{fmt}");}}')


def inline_images(html, asset_dir):
    """Replace src="asset:<file>" (and url("asset:<file>")) with base64 data: URLs."""
    missing, count = [], 0

    def load(name):
        path = os.path.join(asset_dir, name)
        ext = os.path.splitext(path)[1].lower()
        if not os.path.exists(path) or ext not in IMG_MIME:
            missing.append(name)
            return None
        with open(path, "rb") as f:
            return f"data:{IMG_MIME[ext]};base64," + base64.b64encode(f.read()).decode("ascii")

    def sub_src(m):
        nonlocal count
        data = load(m.group(1))
        if data is None:
            return m.group(0)
        count += 1
        return f'src="{data}"'

    def sub_url(m):
        nonlocal count
        data = load(m.group(1))
        if data is None:
            return m.group(0)
        count += 1
        return f'url("{data}")'

    html = re.sub(r'src="asset:([^"]+)"', sub_src, html)
    html = re.sub(r'url\(["\']?asset:([^"\')]+)["\']?\)', sub_url, html)
    return html, count, missing


def main():
    args = sys.argv[1:]
    asset_dir = font_dir = None
    for flag in ("--assets", "--fonts"):
        if flag in args:
            i = args.index(flag)
            if flag == "--assets":
                asset_dir = args[i + 1]
            else:
                font_dir = args[i + 1]
            del args[i:i + 2]
    if not args:
        sys.exit("usage: embed-fonts.py site.html [out.html] [--assets DIR] [--fonts DIR]")
    src = args[0]
    dst = args[1] if len(args) > 1 else src
    asset_dir = asset_dir or os.path.join(os.path.dirname(os.path.abspath(src)), "assets")
    font_dir = font_dir or os.path.join(HERE, "assets", "fonts")

    html = open(src, encoding="utf-8").read()
    html, n_img, missing = inline_images(html, asset_dir)

    rules, families = [], []
    for family, fonts in ((FONT_FAMILY, FONTS), (FONT_FAMILY_DISPLAY, FONTS_DISPLAY)):
        if not family or not fonts:
            continue
        families.append(family)
        for name, w, s in fonts:
            p = os.path.join(font_dir, name)
            if not os.path.exists(p):
                sys.exit(f"missing font: {p}")
            rules.append(face(family, p, w, s))

    if rules:
        block = "\n".join(rules)
        # idempotency: drop faces previously embedded for these families
        for fam in families:
            html = re.sub(r'@font-face\{font-family:"' + re.escape(fam) + r'";[^}]*\}\n?', "", html)
        if MARKER in html:
            html = html.replace(MARKER, block, 1)
        else:
            html = re.sub(r"(<style[^>]*>)", lambda m: m.group(1) + "\n" + block, html, count=1)

    open(dst, "w", encoding="utf-8").write(html)

    # verify self-contained
    refs = re.findall(r'(?:src|href)\s*=\s*["\']([^"\']+)', html)
    src_leaks = [m for m in re.findall(r'src\s*=\s*["\']([^"\']+)', html)
                 if not m.startswith(("data:", "#"))]
    link_tags = re.findall(r"<link\b[^>]*>", html, flags=re.I)
    imports = re.findall(r"@import[^;]+;", html)
    css_urls = [u for u in re.findall(r'url\(["\']?([^"\')]+)', html) if not u.startswith(("data:", "#"))]
    kb = len(html.encode("utf-8")) / 1024

    if rules:
        print(f"embedded {len(rules)} font face(s) ({', '.join(families)}), {n_img} image(s) -> {dst}  ({kb:.0f} KB)")
    else:
        print(f"NO FONTS EMBEDDED (FONTS is empty), {n_img} image(s) -> {dst}  ({kb:.0f} KB)")
        print("  The page will render the fallback font. Fill FONT_FAMILY/FONTS unless the brand has no custom font.")
    if missing:
        print("WARNING: images not found in", asset_dir, ":", missing)
    if src_leaks or link_tags or imports or css_urls:
        print("WARNING: possible external references:", (src_leaks + css_urls)[:5], link_tags[:2], imports[:2])
    else:
        ext_links = [r for r in refs if r.startswith("http")]
        note = f" ({len(ext_links)} outbound link(s) in href are fine)" if ext_links else ""
        print("self-contained OK: no external src, url(), <link> or @import" + note)


if __name__ == "__main__":
    main()
