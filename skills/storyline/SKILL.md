---
name: storyline
description: Structure and tighten the narrative of a consulting asset using SCQA and the Minto pyramid — an explicit governing thought, MECE argument grouping, action titles with a so-what read-through, altitude calibration, and a stand-alone executive summary. Use when drafting or sharpening the storyline or narrative of a proposal, deck, POV, or readout, when writing or fixing action titles or slide titles, or when a narrative does not hang together. Not for slide visual design (see presentation-websites) or prose humanization (see asset-review or humanizer).
---

# storyline

## When to use

Use this skill when the structure of a consulting asset needs work: the argument is not clear, the section order is wrong, the headings are noun phrases instead of claims, or the narrative lacks a governing thought. Also use it for a targeted action-title pass without restructuring the whole document.

Do not use it for prose editing or humanization (the `humanizer` skill handles that), for slide visual or layout design (see `presentation-websites`), or for positioning strategy — defining win themes and differentiators belongs to the `positioning` skill.

## Method in brief

The method is the Minto pyramid with an SCQA front end.

Identify the **governing thought** first — a single declarative sentence that is the Answer to the reader's key Question. This sentence is the apex of the pyramid and the action title for the first substantive slide. Every other argument in the document either supports or qualifies it.

Write the **SCQA frame** to earn the governing thought: Situation (shared context the reader already accepts) → Complication (what changed or broke) → Question (what the Complication forces the reader to ask) → Answer (the governing thought).

Build the **MECE argument tree**: group the supporting evidence into mutually exclusive, collectively exhaustive clusters. Each cluster gets a claim sentence. Each claim is supported by specific evidence points (one per node — no repetition across branches). Use deductive structure (premise → premise → conclusion) for speed; inductive (observations → synthesis) for credibility building.

Write **action titles** as full declarative sentences — one claim per title, no noun phrases. Apply the so-what test and the read-through gate (titles alone should reproduce the argument).

Run an **altitude pass**: confirm each section is pitched at the right altitude for its audience and purpose. See `references/altitude.md`.

Draft or check the **executive summary** last: governing thought first, three supporting paragraphs (one per MECE group), then the ask. Must stand alone.

## Anti-fragmentation and the house spine

**Anti-fragmentation.** The most common structural failure is not a wrong argument but a *scattered* one: a single idea spread across four sections that should be one, so the reader never gets a spine to hold and the asset feels like "everything and nothing." When building or diagnosing, actively ask: does this argument sprawl across sections that belong together? Would the reader be able to name the through-line? Consolidating N sections into one coherent section is a legitimate and frequent move — prefer it to leaving related beats flowing separately. A structural re-cut re-enters the Frame + Storyline gate (align on the new spine before rebuilding).

**House spine.** Beneath the governing thought, a repeatable section spine helps — most often **WHY → WHAT → HOW** (situation and what forces a decision → the target state/capability, concretely → the path, phased), optionally extended with WHO / WHEN / Next steps. This is the section skeleton; SCQA earns the governing thought above it and the two work together. WHY/WHAT/HOW is also the structure DACH/German exec audiences expect (see the `voice` skill's localization reference). Use it where an audience rewards an explicit, front-loaded skeleton; do not impose it by reflex where a different spine serves the argument better.

Spine labels are **unique addresses, not reusable brackets** — never nest a second instance of a label inside the spine. When three or more consecutive sections wear the same label doing different jobs, the argument usually has four buckets competing for three slots; see "House-spine overload" in [references/scqa-minto.md](references/scqa-minto.md).

## Workflow

1. State the governing thought in one sentence. If you cannot, the argument is not ready — gather more input.
2. Write the SCQA frame that earns the governing thought.
3. Build the MECE argument tree: group evidence, label each group with a claim sentence. Run the anti-fragmentation check — consolidate any idea that has sprawled across sections that belong together. Check for spine overload.
4. Write action titles for each group and major slide.
5. Run the title-read-through gate **mechanically**: titles alone must reproduce the argument, and *count* the titles that are noun phrases or subordinate fragments (one is a defect; two consecutive is a P1). Assert first-use ordering — the section defining each canonical term precedes every section using it.
6. **De-slop the titles now, before any build**, via the `voice` tell-scan, and lock the set in the state file. Titles regress worst and get touched most; cleaning them inside the artifact means cleaning them again after every rework. Retitle all or none, and present the full set as one before→after table for approval.
7. Run the altitude pass: confirm each section matches its audience.
8. Draft or check the executive summary.

## Reference files

Read these when the task calls for it — not all at once:

- [references/scqa-minto.md](references/scqa-minto.md) — read this when building or diagnosing a narrative from scratch; contains the full SCQA definition, pyramid logic (vertical/horizontal), MECE rules, and a worked sovereign-K8s example.
- [references/action-titles.md](references/action-titles.md) — read this when writing or fixing slide titles; contains the so-what test, read-through gate, rules, and five before/after examples.
- [references/altitude.md](references/altitude.md) — read this when the audience mix is unclear or the deck needs an altitude check; covers executive / architect / mixed altitudes and three mismatch examples.
- [references/exec-summary.md](references/exec-summary.md) — read this when drafting or reviewing an executive summary; covers the stands-alone test, structure, relationship to win themes (from the `positioning` skill), and a worked example.

## Interface contract (for asset-forge orchestration)

A storyline artifact produced by this skill must contain, in order:
1. A labeled **governing thought** line (one sentence).
2. The SCQA frame.
3. The MECE argument tree with claim sentences.
4. A list of action titles that pass the read-through gate.

The `asset-forge` orchestrator checks for the governing thought line before proceeding to the asset-production phase.

## Conventions

Always use `[CLIENT]` as the placeholder for the customer name and `[FIRM]` for the bidding firm — never use the real names.
