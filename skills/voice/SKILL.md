---
name: voice
description: Make marked-up copy read as a specific human author wrote it, not a chatbot — three jobs that generic humanization does not do. (1) Voice-matching from a real sample of the author's writing, so the text sounds like them and not like "human-sounding AI." (2) Market/language localization, principally DACH/German exec-readout structure and tone even when the copy is in English. (3) An operational de-slop pass for HTML and other marked-up artifacts: an entity-aware tell watchlist run as grep, a fragment-level edit discipline (never whole-paragraph literal replaces), a voice-reference anchor, and a machine tell-scan as a verifiable exit check. Use when the author's name is on the asset and it still "reads too AI-like" after humanizer/writing already ran, when copy must land for a German/DACH audience, or when de-slopping copy that lives inside HTML/SVG/Markdown with entities. Delegated to by asset-review's humanization step. Not a replacement for humanizer (mechanical pattern detection) or writing (prose philosophy) — it runs alongside them and adds author-voice, localization, and the marked-up-file operating method.
---

# voice

## What this skill is for

Generic humanization asks "does this read as human?" This skill asks three sharper questions that generic humanization does not answer:

1. **Does it read as *this author*?** Not human-in-general — the specific person whose name is on the asset. This needs a real sample of their writing, not an abstract ideal.
2. **Does it land for *this market*?** A line that reads well to an Anglo-American ear can read as glib marketing to a German exec. DACH/German-structure localization is a distinct job from sounding human.
3. **Did the de-slop pass actually hold, and can I prove it?** On marked-up copy (HTML, SVG, Markdown), the tells hide inside entities and the naive edit method silently fails. This skill makes the pass operational and verifiable.

It exists because "reads too AI-like" kept recurring **after** `humanizer` and `writing` had already run — worst on headlines, hero lines, and section titles — and because the fixes that finally worked were author-voice matching, DACH restructuring, and a fragment-level de-slop method that no prose skill encodes.

## Relationship to the other writing skills

Run all three; none replaces another.

- `humanizer` — mechanical pattern detection (Wikipedia "signs of AI writing").
- `writing` (and asset-review's bundled `writing-ruleset.md`) — a prose-quality philosophy.
- **`voice`** (this skill) — author-specific voice, market localization, and the operating method for de-slopping marked-up files with a proof step.

When `asset-review` reaches its humanization step, it delegates here **in addition to** running the ruleset and `humanizer`.

## The three jobs

### 1. Voice-matching
Match the text to a real sample of the author's own writing. **A standing profile for the default author is in [references/voice-bar.md](references/voice-bar.md)** — read it whenever the asset carries their name; it holds their compression ratio, hard bans, the rules mined from their own rewrites, and the grammar slips to fix silently. For any other author, build a profile with the method in [references/voice-matching.md](references/voice-matching.md): the **voice-sample bank**, the **rewrite-diff sample** (the author's own rewrite of your copy is the richest source there is — ask for whole passages), and the **voice-reference-anchor** method (nominate one clean section already in the author's voice and de-slop everything else to match *it*, not an abstract ideal).

### 2. Localization
Restructure and re-tone for the target market. Read [references/localization.md](references/localization.md) — principally DACH/German exec-readout structure (front-loaded, explicit logic, WHY→WHAT→HOW, every number sourced, no manufactured punchlines), applied even when the copy stays in English.

### 3. Operational de-slop
Run the tell-scan as a repeatable, verifiable pass over marked-up copy. Read [references/tell-scan.md](references/tell-scan.md) — the entity-aware grep watchlist, the fragment-edit discipline, register-awareness (exec copy → zero tells; technical copy keeps its register), and the machine tell-scan exit check.

## Workflow

1. **Establish the voice reference.** Read the standing profile if the asset is the default author's; otherwise get or build the voice-sample bank and nominate the in-asset anchor section. If neither exists, say so and proceed on the ruleset alone — do not fabricate a voice.
2. **Set the register map and the scope.** Which parts are exec/high-level (target: zero tells), which are technical/low-level (keep the technical register — `day-2`, `reconciles`, `bidirectional` are not tells there), and which are **scannable fragments** that the pass does not touch at all (table cells, headers, chips, eyebrows, stat captions, diagram labels). State whether section titles are in scope; if they are, retitle **all or none**.
3. **Back up the file.** The backup is the diff baseline that lets you attribute every residual hit as yours or pre-existing.
4. **Localize if the audience calls for it** (DACH/German structure and tone).
5. **Run the operational de-slop pass** fragment by fragment, matching the anchor. Change every encoding of a claim together — prose, table cell, SVG `<text>`, `aria-label`, caption.
6. **Run the machine tell-scan** and report the residual count per register, **before → after**, separating your own edits from pre-existing hits. Exec copy should reach zero watchlist hits; a non-zero count in technical copy is fine only if each hit is register-appropriate.
7. **Re-check the claims on every line you rewrote.** A voice pass changes tense, modality, and hedging, so it is **claims-affecting, not cosmetic**. In practice a full author-voice rewrite reintroduced present-tense overclaims across titles, benefit cards, and close rows — on lines the author had personally written — and it took a six-persona board to find them. Confirm no rewritten line now asserts as present fact something the asset's own baseline grades as absent, designed, or unbuilt. Author-supplied copy gets the same check as generated copy. Method: `asset-review/references/claims-check.md`.

## Exit check (verifiable)

The pass is not done on a feeling. It is done when the machine tell-scan (the grep recipe in `references/tell-scan.md`) returns zero watchlist hits in exec/high-level copy, every remaining hit in technical copy is a deliberate register-appropriate term, and the claims re-check on rewritten lines is clean. Report the counts as before → after per register.

## Conventions

Always use `[CLIENT]` as the placeholder for the customer name — never write the real name.
