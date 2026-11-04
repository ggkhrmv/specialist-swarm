"""
Score a Deal Desk proposal against the traps planted in the Acme Corp RFP.

The Acme RFP (synthetic-data/rfp-acme-corp.md) asks for 13 things that collide with
our own playbooks: commercial terms Pricing must refuse, clauses Legal must counter,
an SLA that Technical Fit can only meet at extra cost, a competitor that owns the
customer's BI tool. demo/README.md has the full answer key. This script checks
whether the deliverable deals with each trap, so a demo can end on a number
("13 traps planted, 12 handled") and the team can compare runs.

It is a keyword check, not a judge: a trap counts as handled when the right terms
appear close together (e.g. "MFN" near "decline"). Treat a miss as "look here" and
confirm it in the document with --show before saying it on stage.

By default it reads the proposal and, if present, the coordinator's internal deal
notes: some answers belong in the notes, not in front of the customer (e.g. how we
position against a named competitor). Hits found only in the notes are marked.

$0, no network, stdlib only. Works on docx and on text/markdown files.

Usage:
    uv run python demo/scorecard.py              # outputs/proposal-response.docx + internal-deal-notes.md
    uv run python demo/scorecard.py <file> [<file> ...] --show
"""

import html
import re
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
DEFAULTS = [HERE / "outputs" / "proposal-response.docx",
            HERE / "outputs" / "internal-deal-notes.md"]
RADIUS = 3  # paragraphs: the terms of one check must sit within ±RADIUS paragraphs

# Recurring vocabularies
PUSHBACK = (r"declin|reject|refus|cannot|can't|won't|will not|do not accept|not accept|"
            r"unacceptable|strike|delete|counter|push back|no MFN|non-starter|blocker|"
            r"walk away|not agree|excluded|not offer|in its place|instead of|"
            r"price certainty|price protection")
PCT_WE_CAN_GIVE = r"\b(1[0-9]|2[0-9]|30)(\.\d)?\s?%"

# id, title, lanes, seam?, regexes that must all match within ±RADIUS paragraphs of
# a match of the first one. Seams are traps that only show when two lanes' reports
# are read against each other.
CHECKS = [
    ("C1", "35% discount demand answered with a playbook-sized discount",
     "Pricing", False,
     [r"35\s?%", PCT_WE_CAN_GIVE + r"|(do not|cannot|can't|won't) meet|\bTCO\b|cost of ownership"]),
    ("C2", "5-year fixed price / no escalators vs the 3-year escalator rule",
     "Pricing", False, [r"escalat|CPI|renewal years?|indexation|price step",
      r"CPI|capped|\d\s?%|forgo|waive|step|schedule"]),
    ("C3", "Net 90 payment countered (Net 30 / Net 60)",
     "Pricing", False, [r"Net[ -]?90|payment", r"Net[ -]?(30|60)\b"]),
    ("C4", "MFN clause refused",
     "Pricing + Legal", False, [r"\bMFN\b|most[- ]favou?red", PUSHBACK]),
    ("C5", "30-day termination at will vs the multi-year discount",
     "Legal x Pricing", True,
     [r"terminat", r"convenience|at will|without cause|30[- ]day|30 days",
      r"\b(60|90)[- ]?days?|pro[- ]?rat|commit|multi[- ]year|discount"]),
    ("C6", "Uncapped breach liability capped (12 / 24 months of fees)",
     "Legal + Pricing", False,
     [r"liabilit|indemn", r"uncapped|unlimited|\bcap", r"\b(12|24|twelve|twenty-four)[- ]months?"]),
    ("C7", "No-notice audits countered (notice, frequency, cost)",
     "Legal", False, [r"audit", r"notice", r"once|one per|annual|per year|30[- ]day|30 days"]),
    ("C8", "99.99% SLA priced as an add-on (active-active, extra fee)",
     "Technical Fit x Pricing", True,
     [r"99\.99", r"add-?on|active[- ]active|premium|\$\s?(80|100|120)\s?K|uplift|surcharge"]),
    ("C9", "SLA remedy: service credits, not termination on any miss",
     "Legal x Technical Fit", True,
     [r"SLA|uptime|service level", r"service credits?|sole remedy|credit"]),
    ("C10", "IP vesting countered with a licence (Stark precedent)",
     "Legal x Pricing data", True,
     [r"\bIP\b|intellectual property|work product|ownership", r"licen[cs]|licence-back|license-back"]),
    ("C11", "Subprocessor veto countered (notice + objection right)",
     "Legal", False, [r"sub-?processor", r"notif|notice|object|30[- ]day|30 days|list"]),
    ("C12", "Microsoft Fabric / 'free with E5' reframed to TCO",
     "Competitive x Technical Fit", True,
     [r"Fabric|Microsoft", r"\bE5\b|TCO|total cost|cost of ownership"]),
    ("C13", "Teradata migration timeline sized (16-24 weeks)",
     "Technical Fit", False,
     [r"Teradata|migrat|implement|timeline|go-live", r"\b(16|20|24|sixteen|twenty-four)[- ]weeks?|weeks?\s+(\d+\s?[–-]\s?)?(16|20|24)\b"]),
]


def read_text(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8")
        xml = re.sub(r"</w:p>|<w:br\s*/>|<w:tab\s*/>|</w:tc>", "\n", xml)
        return html.unescape(re.sub(r"<[^>]+>", "", xml))
    return path.read_text(encoding="utf-8", errors="replace")


def find(text: str, groups: list) -> str | None:
    """The paragraph that anchors a match (every group within ±RADIUS of it), else None."""
    paras = [" ".join(line.split()) for line in text.splitlines() if line.strip()]
    first, rest = groups[0], groups[1:]
    for i, para in enumerate(paras):
        if not re.search(first, para, re.I):
            continue
        window = " / ".join(paras[max(0, i - RADIUS): i + RADIUS + 1])
        if all(re.search(g, window, re.I) for g in rest):
            return para
    return None


def default_paths() -> list[Path]:
    """The proposal, plus the notes only if the same run downloaded them (outputs/ keeps
    files from earlier runs: a run that writes no notes leaves the old ones behind)."""
    docx, notes = DEFAULTS
    if not docx.is_file():
        return []
    if notes.is_file() and abs(notes.stat().st_mtime - docx.stat().st_mtime) < 120:
        return [docx, notes]
    if notes.is_file():
        print(f"  (skipping {notes.name}: it is from an earlier run)\n")
    return [docx]


def main() -> None:
    args = [Path(a) for a in sys.argv[1:] if not a.startswith("-")]
    show = "--show" in sys.argv
    paths = args or default_paths()
    missing = [p for p in args if not p.is_file()]
    if missing or not paths:
        raise SystemExit(f"No such file: {missing[0] if missing else DEFAULTS[0]}. "
                         "Run the swarm first, or pass a path.")
    texts = [(p, read_text(p)) for p in paths]

    hits, seam_hits, seams, in_main = 0, 0, 0, 0
    names = " + ".join(p.name for p in paths)
    print(f"Scorecard: {names}  (Acme Corp RFP answer key, demo/README.md)\n")
    for cid, title, lanes, seam, groups in CHECKS:
        found = next(((p, snip) for p, text in texts if (snip := find(text, groups))), None)
        ok = found is not None
        hits += ok
        in_main += ok and found[0] == paths[0]
        seams += seam
        seam_hits += ok and seam
        mark = "✓" if ok else "✗"
        tag = "  [seam]" if seam else ""
        where = f"  [in {found[0].name}]" if ok and found[0] != paths[0] else ""
        print(f"  {mark} {cid:4s} {title}  ({lanes}){tag}{where}")
        if show and ok:
            print(f"         … {found[1][:380]} …")
    print(f"\n  Traps handled: {hits}/{len(CHECKS)}   cross-lane seams: {seam_hits}/{seams}")
    if len(paths) > 1:
        print(f"  ({in_main} in {paths[0].name}, the rest in the other files)")
    if hits < len(CHECKS):
        print("  A ✗ means the keywords weren't found close together. Check the document "
              "before calling it a miss.")


if __name__ == "__main__":
    main()
