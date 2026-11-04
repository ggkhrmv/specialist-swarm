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

$0, no network, stdlib only. Works on the docx or on any text/markdown file (e.g.
outputs/coordinator-transcript.md).

Usage:
    uv run python demo/scorecard.py                         # outputs/proposal-response.docx
    uv run python demo/scorecard.py path/to/proposal.docx --show
"""

import html
import re
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
DEFAULT = HERE / "outputs" / "proposal-response.docx"
RADIUS = 3  # paragraphs: the terms of one check must sit within ±RADIUS paragraphs

# Recurring vocabularies
PUSHBACK = (r"declin|reject|refus|cannot|can't|won't|will not|do not accept|not accept|"
            r"unacceptable|strike|delete|counter|push back|no MFN|non-starter|blocker|"
            r"walk away|not agree|excluded")
PCT_WE_CAN_GIVE = r"\b(1[0-9]|2[0-9]|30)(\.\d)?\s?%"

# id, title, lanes, seam?, regexes that must all match within ±RADIUS paragraphs of
# a match of the first one. Seams are traps that only show when two lanes' reports
# are read against each other.
CHECKS = [
    ("C1", "35% discount demand answered with a playbook-sized discount",
     "Pricing", False, [r"35\s?%", PCT_WE_CAN_GIVE]),
    ("C2", "5-year fixed price / no escalators vs the 3-year escalator rule",
     "Pricing", False, [r"escalat|CPI", r"CPI|capped|\d\s?%|forgo|waive"]),
    ("C3", "Net 90 payment countered (Net 30 / Net 60)",
     "Pricing", False, [r"Net[ -]?90", r"Net[ -]?(30|60)|quarterly"]),
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
     [r"Teradata|migrat|implement|timeline|go-live", r"\b(16|20|24|sixteen|twenty-four)[- ]weeks?"]),
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


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    show = "--show" in sys.argv
    path = Path(args[0]) if args else DEFAULT
    if not path.is_file():
        raise SystemExit(f"No such file: {path}. Run the swarm first, or pass a path.")
    text = read_text(path)

    hits, seam_hits, seams = 0, 0, 0
    print(f"Scorecard: {path.name}  (Acme Corp RFP answer key, demo/README.md)\n")
    for cid, title, lanes, seam, groups in CHECKS:
        snippet = find(text, groups)
        ok = snippet is not None
        hits += ok
        seams += seam
        seam_hits += ok and seam
        mark = "✓" if ok else "✗"
        tag = "  [seam]" if seam else ""
        print(f"  {mark} {cid:4s} {title}  ({lanes}){tag}")
        if show and ok:
            print(f"         … {snippet[:380]} …")
    print(f"\n  Traps handled: {hits}/{len(CHECKS)}   cross-lane seams: {seam_hits}/{seams}")
    if hits < len(CHECKS):
        print("  A ✗ means the keywords weren't found close together. Check the document "
              "before calling it a miss.")


if __name__ == "__main__":
    main()
