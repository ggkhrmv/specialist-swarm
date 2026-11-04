#!/usr/bin/env python3
"""
Build the BTS-Synthetic pitch deck: one self-contained HTML file.

    python3 build_deck.py SLIDES.html OUT.html --title "..." --context "..." [--count 5]

SLIDES.html holds only the <section class="slide"> elements. This script wraps them
in assets/shell.html (tokens, components, presenter script), embeds the fonts as
base64, and runs the quality gates. It exits non-zero and lists every problem if a
gate fails, so fix the slides and run it again until it prints "deck OK".

Standard library only. Run it with the skill directory anywhere: paths are
resolved relative to this file.
"""

from __future__ import annotations

import argparse
import base64
import html
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SHELL = SKILL / "assets" / "shell.html"
FONTS = SKILL / "assets" / "fonts"

FACES = [  # (family, file, weight, style)
    ("Instrument Serif", "instrument-serif-400.woff2", 400, "normal"),
    ("Instrument Serif", "instrument-serif-400-italic.woff2", 400, "italic"),
    ("Geist", "geist-400.woff2", 400, "normal"),
    ("Geist", "geist-500.woff2", 500, "normal"),
    ("Geist", "geist-600.woff2", 600, "normal"),
    ("Geist Mono", "geist-mono-400.woff2", 400, "normal"),
    ("Geist Mono", "geist-mono-500.woff2", 500, "normal"),
]

MAX_WORDS = 110  # per slide, excluding speaker notes and SVG text

EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF]")


def font_faces() -> str:
    rules = []
    for family, name, weight, style in FACES:
        data = base64.b64encode((FONTS / name).read_bytes()).decode()
        rules.append(f'@font-face {{ font-family: "{family}"; src: url(data:font/woff2;base64,{data}) '
                     f'format("woff2"); font-weight: {weight}; font-style: {style}; font-display: block; }}')
    return "\n".join(rules)


def strip_tags(fragment: str) -> str:
    fragment = re.sub(r"<aside class=\"notes\".*?</aside>", " ", fragment, flags=re.S)
    fragment = re.sub(r"<svg.*?</svg>", " ", fragment, flags=re.S)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    return html.unescape(fragment)


def check(slides_html: str, expected: int) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    sections = re.findall(r"<section\b[^>]*class=\"[^\"]*\bslide\b[^\"]*\"[^>]*>.*?</section>",
                          slides_html, flags=re.S)

    if len(sections) != expected:
        errors.append(f"found {len(sections)} <section class=\"slide\"> elements, expected {expected}")

    for i, sec in enumerate(sections, 1):
        is_cover = "slide--cover" in sec.split(">", 1)[0]
        if not is_cover and not re.search(r"<h2\b[^>]*class=\"[^\"]*\btitle\b", sec):
            errors.append(f"slide {i}: no <h2 class=\"title\"> action title")
        if is_cover and "cover__title" not in sec:
            errors.append(f"slide {i}: cover has no <h1 class=\"cover__title\">")
        words = len(strip_tags(sec).split())
        if words > MAX_WORDS:
            warnings.append(f"slide {i}: {words} words on the slide (aim for under {MAX_WORDS}); "
                            "move detail into the speaker notes or the docx")
        if "<aside class=\"notes\"" not in sec:
            warnings.append(f"slide {i}: no speaker notes (<aside class=\"notes\">)")
        for svg in re.findall(r"<svg\b[^>]*>.*?</svg>", sec, flags=re.S):
            opening = svg.split(">", 1)[0]
            if "<use " in svg and svg.count("<") <= 3:
                continue  # an icon reference from the sprite
            if 'aria-hidden="true"' in opening:
                continue
            if 'role="img"' not in opening or "<title" not in svg:
                errors.append(f"slide {i}: a diagram <svg> needs role=\"img\", aria-labelledby and a <title>")
            if 'class="dg' not in opening:
                errors.append(f"slide {i}: a diagram <svg> needs class=\"dg\" so it picks up the diagram styles")
            if "viewBox" not in opening:
                errors.append(f"slide {i}: a diagram <svg> needs a viewBox")

    rules = [
        (r"\b(?:animation|transition)\s*:|<animate", "animation (charts are static: draw marks at their final size)"),
        (r"(?:src|href)\s*=\s*\"(?:https?:)?//", "external src/href (the deck must be self-contained)"),
        (r"url\(\s*['\"]?(?:https?:)?//", "external url() reference"),
        (r"@import", "@import"),
        (r"<link\b", "<link> tag"),
        (r"<script\b", "<script> in the slides (the shell owns the only script)"),
        (r"<style\b", "<style> in the slides (use the shell's classes)"),
        (r"<img\b", "<img> (draw an SVG instead; no external or raster images)"),
        (r"\brgba?\(|\bhsla?\(|\boklch\(", "raw colour function (use a class or var(--token))"),
        (r"text-transform\s*:\s*uppercase", "uppercase text-transform"),
        (r"box-shadow", "box-shadow (borders, not shadows)"),
        (r"background-clip\s*:\s*text", "gradient text"),
        (r"font-family\s*:", "inline font-family (the shell sets the type)"),
        (r"\bLorem\b|\bTODO\b|\bTBD\b|\[placeholder\]", "placeholder text"),
    ]
    for pattern, what in rules:
        if re.search(pattern, slides_html, flags=re.I if "Lorem" in pattern else 0):
            errors.append(f"slides contain {what}")
    for tag in re.findall(r"<[^>]+>", slides_html):
        tag = re.sub(r"\b(?:href|id|aria-[a-z]+)\s*=\s*\"[^\"]*\"", "", tag)
        if re.search(r"#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3}(?:[0-9a-fA-F]{2})?)?\b", tag):
            errors.append(f"raw hex colour in {tag[:60]!r}: use a class or var(--token)")
            break
    if EMOJI.search(slides_html):
        errors.append("slides contain emoji (use the sprite icons: #i-check, #i-shield, #i-alert, ...)")
    if "→" in strip_tags(slides_html):
        warnings.append("slides use the → glyph in copy; draw an arrow in SVG or rephrase")
    return errors, warnings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slides", type=Path, help="HTML file with only the <section class=\"slide\"> elements")
    ap.add_argument("out", type=Path, help="where to write the deck, e.g. /mnt/session/outputs/pitch-deck.html")
    ap.add_argument("--title", required=True, help="document title, e.g. 'Acme Corp · Data platform proposal'")
    ap.add_argument("--context", required=True,
                    help="footer line on every slide, e.g. 'Acme Corp · RFP response · Confidential'")
    ap.add_argument("--count", type=int, default=5, help="expected number of slides (default 5)")
    args = ap.parse_args()

    slides_html = args.slides.read_text(encoding="utf-8")
    errors, warnings = check(slides_html, args.count)
    for w in warnings:
        print(f"warn: {w}")
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        print(f"\n{len(errors)} problem(s). Fix the slides and run build_deck.py again.")
        return 1

    shell = SHELL.read_text(encoding="utf-8")
    out = (shell.replace("{{FONT_FACES}}", font_faces())
                .replace("{{TITLE}}", html.escape(args.title))
                .replace("{{CONTEXT}}", html.escape(args.context))
                .replace("{{SLIDES}}", slides_html.strip()))
    leftover = re.findall(r"\{\{\w+\}\}", out)
    if leftover:
        print(f"FAIL: unfilled shell slots {leftover}")
        return 1
    external = re.findall(r"(?:src|href)\s*=\s*\"(?:https?:)?//[^\"]+|url\(\s*['\"]?https?://[^)]+", out)
    if external:
        print(f"FAIL: external references in the built deck: {external[:3]}")
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(out, encoding="utf-8")
    n = len(re.findall(r"<section\b[^>]*class=\"[^\"]*\bslide\b", slides_html))
    print(f"deck OK: {n} slides, {len(FACES)} font faces embedded, self-contained, "
          f"{len(out.encode()) // 1024} KB -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
