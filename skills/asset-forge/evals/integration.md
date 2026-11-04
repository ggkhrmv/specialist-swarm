# Triggering / Collision Analysis — asset-forge skill system

**Scope:** The original matrix (§1–3) covers seven skills — asset-forge, positioning,
storyline, asset-review, presentation-websites, smd-review, humanizer — against
eight prompts. §4 (v2) adds the three new sub-skills — voice, diagram-spec, capability-map —
and their neighbours (writing, dataviz). Description-level triggering only; no end-to-end run.

---

## 1. Triggering Matrix

| Prompt | Should fire | Should NOT fire | Verdict |
|---|---|---|---|
| "Build me a proposal from scratch" | asset-forge | positioning, storyline, presentation-websites | CLEAN |
| "Draft the SCQA storyline" | storyline | asset-forge | CLEAN |
| "How do we position against incumbents?" | positioning | asset-forge | CLEAN |
| "Run the review board on this draft" | asset-review | smd-review | CLEAN |
| "Review this one slide" | smd-review | asset-review | CLEAN |
| "Humanize this paragraph" | humanizer | asset-review | CLEAN |
| "Make a branded pitch page for us" | presentation-websites | asset-forge | CLEAN |
| "Build me the branded deck for this RfQ" | asset-forge (full workflow) OR presentation-websites (Build-phase artifact) | — | AMBIGUOUS |

---

## 2. Row-by-row assessment

### Row 1 — "Build me a proposal from scratch" → asset-forge  CLEAN

asset-forge's description contains the phrase "Use when starting a consulting asset from
scratch or running the full proposal or bid process end to end" — an exact lexical match.
The phrase "from scratch" is unique to asset-forge across all seven descriptions; no other
skill claims it.

Potential collisions checked:
- **positioning**: "Use when deciding how to position a proposal" could fire, but the
  anti-trigger in asset-forge ("For a single phase … invoke that sub-skill directly
  instead") makes it clear positioning is a sub-skill, not an entry point for a full build.
- **presentation-websites**: Its trigger text requires a web artifact "for a specific brand
  whose design tokens, fonts, and logos you supply" — but the prompt mentions neither a brand
  nor HTML, so this description criterion does not match.
- **storyline**: "Use when drafting or sharpening the storyline or narrative of a proposal"
  could fire, but "from scratch" and the full-workflow framing make asset-forge more specific.

No anti-trigger clause needed; the existing wording resolves this cleanly.

---

### Row 2 — "Draft the SCQA storyline" → storyline  CLEAN

The word "SCQA" appears only in storyline's description. asset-forge's description mentions
"Storyline" as a phase name, but its trigger condition is "starting … from scratch or running
the full proposal … end to end" — not drafting a single structure. Additionally, asset-forge
carries an explicit anti-trigger ("For a single phase … just the storyline … invoke that
sub-skill directly instead"), removing any residual ambiguity.

---

### Row 3 — "How do we position against incumbents?" → positioning  CLEAN

"Position against incumbents" maps directly to positioning's "discriminators/why-us: where
you are genuinely different from the specific alternatives." asset-forge carries the same
anti-trigger as in Row 2 — single-phase tasks delegate to sub-skills. No other skill
references competitive positioning or incumbents.

---

### Row 4 — "Run the review board on this draft" → asset-review  CLEAN

"Review board" implies a multi-persona formal review, which maps to asset-review's core
workflow ("multi-persona critique … merge the findings into a page-by-page redline"). The
phrase "color-team or red-team review" in asset-review's description is the consulting term
for this kind of structured board.

smd-review's trigger list is exhaustive and phrase-matched: "review this slide / give me MD
feedback / review like a senior MD / is this exec-ready / review this deck / too dense? /
fix the action title." None of those patterns match "run the review board." smd-review is
also described as covering "slides and short flows," not a full draft.

---

### Row 5 — "Review this one slide" → smd-review  CLEAN

"review this slide" is the first phrase in smd-review's trigger list — an exact match.
asset-review contains an explicit anti-trigger: "For a quick single-slide critique use
smd-review." The word "one" reinforces the single-item scope, ruling out asset-review's
multi-persona, full-asset workflow.

---

### Row 6 — "Humanize this paragraph" → humanizer  CLEAN

humanizer's description ("Remove signs of AI-generated writing from text. Use when editing
or reviewing text to make it sound more natural and human-written") matches directly.
asset-review contains an explicit anti-trigger: "for a pure text humanization pass on a
snippet use humanizer." "Paragraph" signals a snippet scope, not a full drafted asset.

---

### Row 7 — "Make a branded pitch page for us" → presentation-websites  CLEAN

presentation-websites has two matching trigger clauses: "a one-pager, landing page, or
web-based presentation … for a specific brand" and the example trigger "make a branded
presentation site." Both fire here; "for us" signals the user's own brand kit is the one to
apply. The word "page" signals a single-file web artifact, which is presentation-websites'
sole output type.

asset-forge lists "pitch deck" as an asset type, but its trigger condition requires starting
"from scratch" with a full phased workflow. "Make … a page" does not invoke a multi-phase
process.

---

### Row 8 — "Build me the branded deck for this RfQ"  AMBIGUOUS

This is the known gap case flagged in the Task 4 review.

**Why asset-forge fires:** The phrase "for this RfQ" places the request inside a formal
tender context. asset-forge's description lists "RfP or RfQ response" as a covered asset
type. "Build me" could mean "start the full workflow."

**Why presentation-websites fires:** "branded deck" maps to its trigger clause "web-based
presentation … for a specific brand" and the example "make a branded presentation site." A
"deck" in web form is exactly what this skill produces. "Build me" could mean "produce the
artifact now."

**Root cause:** presentation-websites' description scopes itself by artifact and brand only —
"a web-based presentation for a specific brand" — and says nothing that excludes the case
where the user needs a full proposal or bid workflow, not just an HTML artifact. At the same
time, asset-forge's description does not clarify what happens when the user arrives at the
Build phase with a branding requirement and upstream phases already complete.

Neither skill has an anti-trigger clause for this overlap.

---

## 3. Findings — recommended wording fixes

Only Row 8 requires intervention.

### Finding 1 — presentation-websites description (frontmatter)

**Problem:** The scope "web-based presentation/leave-behind for a specific brand" is
unqualified, causing it to compete with asset-forge on any branded proposal or
RfQ-response request that names a deck or page.

**Skill:** presentation-websites  
**Current phrase:** 'Triggers include "make a branded presentation site", "build a
microsite in our brand", or "use the presentation-website framework".'

**Recommended replacement:**
> Triggers include "make a branded presentation site", "build a microsite in our brand", a
> standalone branded capability pitch or readout page, or "use the presentation-website
> framework". Not for full RfQ or bid-response workflows — for those, use asset-forge; this
> skill handles the Build-phase HTML artifact when upstream workflow phases are already complete.

Key changes:
- Name the standalone pitch/readout page as the in-scope case, so a page that is the end of a
  bid workflow is not read as the same thing.
- Add an explicit anti-trigger sentence pointing to asset-forge for full RfQ/bid workflows.
- Clarify the correct use case: Build-phase artifact only, when upstream phases are done.

---

### Finding 2 — asset-forge description (frontmatter)

**Problem:** asset-forge's description does not explain the handoff to
presentation-websites at the Build phase, leaving users uncertain whether to enter
via asset-forge or go directly to presentation-websites when they say "build me
the branded deck for this RfQ."

**Skill:** asset-forge  
**Current closing sentence:** "For a single phase (just the positioning, just the storyline,
or just a review), invoke that sub-skill directly instead."

**Recommended replacement:**
> For a single phase (just the positioning, just the storyline, or just a review), invoke
> that sub-skill directly instead. Exception: if the request names an RfQ or proposal
> context alongside a branded HTML deliverable, enter via asset-forge — it will run
> the workflow and delegate the Build phase to presentation-websites. Use
> presentation-websites directly only when all upstream phases are already complete
> and only the HTML artifact remains to be produced.

Key changes:
- Adds a named exception for the RfQ + branded-deliverable combination, making asset-forge the
  unambiguous winner when an upstream workflow context is present.
- Gives users a clear decision rule: "upstream phases complete → go direct;
  upstream phases not yet done → go through asset-forge."

---

## Summary

| Row | Verdict | Fix required |
|---|---|---|
| "Build me a proposal from scratch" | CLEAN | None |
| "Draft the SCQA storyline" | CLEAN | None |
| "How do we position against incumbents?" | CLEAN | None |
| "Run the review board on this draft" | CLEAN | None |
| "Review this one slide" | CLEAN | None |
| "Humanize this paragraph" | CLEAN | None |
| "Make a branded pitch page for us" | CLEAN | None |
| "Build me the branded deck for this RfQ" | AMBIGUOUS | Two description edits (see Findings 1 and 2) |

---

## 4. Expanded family (v2) — voice, diagram-spec, capability-map

Three new sub-skills join the family. The writing-adjacent skills (humanizer, writing, voice) are **designed to co-run** inside asset-review's humanization step, so among them the goal is not mutual exclusion but correct additive triggering; the risk is the visual/asset skills (diagram-spec vs dataviz, capability-map vs asset-forge/presentation-websites).

| Prompt | Should fire | Should NOT solely capture | Verdict |
|---|---|---|---|
| "Make this hero line sound like me, not like AI" | voice | humanizer, writing (generic — miss the author-voice + de-slop specifics) | CLEAN |
| "De-slop the copy in this HTML page" | voice | humanizer alone (misses entity-aware/fragment method) | CLEAN |
| "Restructure this for a German exec audience" | voice (localization) | storyline alone | CLEAN |
| "The arrows in this SVG diagram cut through the boxes" | diagram-spec | dataviz | CLEAN |
| "Chart our ARR by quarter" | dataviz | diagram-spec | CLEAN |
| "Build a reusable capability/maturity assessment architects fill in" | capability-map | asset-forge full workflow, presentation-websites | CLEAN |

### Row assessments

- **voice vs humanizer vs writing.** voice's description states the boundary explicitly ("Not a replacement for humanizer … or writing — it runs alongside them and adds author-voice, localization, and the marked-up-file operating method"). The trigger phrases unique to voice — "sound like me", "reads too AI-like after humanizer/writing already ran", "German/DACH audience", "de-slopping copy inside HTML/SVG/Markdown" — do not appear in humanizer's or writing's descriptions. For a generic "humanize this paragraph", humanizer still wins (voice adds nothing without a voice sample or marked-up context). Additive-by-design; CLEAN.
- **diagram-spec vs dataviz.** diagram-spec carries an explicit anti-trigger ("Not for chart/data visualization (see dataviz)"); dataviz triggers on chart/graph/plot/dashboard terms. "Arrows through boxes", "layer/flow/architecture/swimlane diagram", "misaligned boxes" are unique to diagram-spec. CLEAN.
- **capability-map vs asset-forge/presentation-websites.** capability-map is the artifact skill for a fillable assessment; its description anti-triggers away from linear decks and data charts. When the request is a *full engagement* around such an asset, asset-forge is the entry point and delegates the artifact to capability-map (mirrors the presentation-websites handoff). "Reusable … fill in per client … maturity assessment" is unique to capability-map. CLEAN.

No description fixes required for the three new skills; the boundary clauses were written into their frontmatter at creation.
