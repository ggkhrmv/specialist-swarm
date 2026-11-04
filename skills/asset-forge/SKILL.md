---
name: asset-forge
description: Orchestrate the end-to-end creation of a consulting asset (proposal, RfP or RfQ response, pitch deck, point of view, readout, presentation site, capability map / maturity assessment, or a multi-artifact system of these) through a phased workflow — Intake, Qualify (bid/no-bid), Frame, Storyline, Build, Review, and a Rework loop the asset re-enters every time feedback comes back — with a durable living-log state file and discipline gates (including a Frame+Storyline gate that locks the positioning frame before any polished build, and an align-before-rewrite checkpoint). Guides the user throughout and delegates to positioning, storyline, and asset-review, plus voice (author-voice, localization, de-slop), diagram-spec (SVG diagrams), and capability-map (assessment assets). Use when starting a consulting asset from scratch, running the full proposal or bid process end to end, or reworking one across review cycles. For a single phase (just the positioning, just the storyline, or just a review), invoke that sub-skill directly instead. If a request combines a proposal or RfQ context with a branded HTML deliverable, start here and let the Build phase delegate to presentation-websites; use presentation-websites directly only when the workflow is already done and only the HTML artifact remains.
---

# asset-forge

## What this skill is

This is a **workflow checklist**, not a runtime engine. It cannot route work automatically or enforce gates programmatically. It instructs you — the user working with Claude — through a phased process, asks the right questions at the right moments, and delegates substantive work to the capability skills. It sets the agenda; it does not drive the work on its own.

## The phases

Six phases carry an asset from brief to reviewed draft; a seventh — Rework — is the loop the asset re-enters every time feedback comes back, which in practice is where most of the work happens. Each phase has a clear entry and exit condition. The full playbook — purpose, inputs, exit condition — is in [references/phases.md](references/phases.md).

| Phase | What happens | Delegation |
|---|---|---|
| **1. Intake** | Gather the brief, source docs (incl. ingesting any reference/house deck — pptx/pdf→md, structure preserved), side-channel intel, stakeholder map, and submission mechanics. Ask for what is missing. | — |
| **2. Qualify** | Bid/no-bid decision. Explicit go/no-go before any framing work. | — |
| **3. Frame** | Positioning frame, win themes, discriminators, scope options, commercial model, terminology ledger, proof/metrics sourcing, compliance matrix. | **REQUIRED SUB-SKILL:** positioning |
| **4. Storyline** | Governing thought, SCQA frame, MECE argument tree (anti-fragmentation), action titles, house spine (e.g. WHY/WHAT/HOW). | **REQUIRED SUB-SKILL:** storyline |
| **5. Build** | Produce the asset in its target format — deck, document, presentation site, or capability map. Validate analytically; hand the visual pass to the user. | Optional: presentation-websites, diagram-spec, capability-map |
| **6. Review** | Multi-persona critique, redline, humanization + voice, claims + technical-soundness check, consistency/terminology gate, compliance-matrix sign-off. | **REQUIRED SUB-SKILL:** asset-review |
| **7. Rework (loop)** | Ingest a feedback batch → triage accept/reject/defer → **align before rewrite** → scope the change → execute → re-verify → log the increment. Re-entered repeatedly. | asset-review (re-run slice), voice, build skills |

## Gates

Three gates enforce discipline at the boundaries where effort escalates. Details, rationalization tables, and red-flags lists are in [references/gates.md](references/gates.md).

- **Qualify gate** (after Intake): produces a go/no-go decision. No framing or writing begins before this gate passes.
- **Frame + Storyline gate** (after Frame, before Build): before polished production, **three** things are locked and signed off together — the **positioning frame** (what the asset is for and what it is *not*, e.g. enabler vs guardrail — the decision that, taken wrong, forces a whole-asset reframe after build), the **governing thought**, and the **two-level outline**. This gate is **iterative** — a strawman for alignment is encouraged and expected; sinking effort into a polished build before these are agreed is not.
- **Review gate** (after Build): the asset-review skill must complete before the asset is declared done. For tender responses, compliance-matrix sign-off is part of this gate.

**Align before rewrite.** After any review — persona board, practice-lead read, or client markup — state back what each note means and get the change set agreed *before* editing. This is the rework-loop equivalent of the Frame + Storyline gate: align on direction before sinking effort into a large rewrite. See the checkpoint in [references/phases.md](references/phases.md).

## Guide behavior

Ask for what is missing. Do not assume brief quality, stakeholder configuration, or submission mechanics. The intake phase is the structured place to surface gaps; the checklist is in [references/intake-checklist.md](references/intake-checklist.md).

If the user is under time pressure, acknowledge it and offer the fastest path that still honors the governing gate. For the Storyline gate, the fast path is a strawman — a rough governing thought and two-level outline — not a skip.

**The visual pass belongs to the user.** Report what you verified analytically, then hand it over — every time, not once. Offering to render is fine when a specific question needs it; deciding for them is not.

**Every finding states the decision it funds.** A finding can be true, measured, and rigorous and still fail, because the reader's natural response is a cheap internal fix rather than the ask. Name the decision and the objection it invites before it enters the asset.

**Close each increment with one named next step,** not an open "anything else?". When a decision you presented goes unanswered, make the call, say it is your call and why, and offer the reversal.

## State file

Write `asset-forge-state.md` at the end of Intake, then keep it as a **living log** — updated at every phase boundary and every rework increment, not once. It carries decisions across sessions because conversation notes do not persist, and it becomes the most-used artifact of the workflow. It holds append-only **decision / reviewer / change logs**, the locked **positioning frame** and **governing thought**, the **voice bar** (fed to the `voice` skill), a **terminology ledger** (canonical names, enforced in Review), an **artifact registry** for multi-file systems, and a live **open-items / next-increments** queue. Schema and a filled example are in [references/state-file-template.md](references/state-file-template.md).

## Reference files

- [references/phases.md](references/phases.md) — full phase playbook (purpose, inputs, sub-skill delegation, exit condition)
- [references/intake-checklist.md](references/intake-checklist.md) — intake questions, stakeholder map, submission mechanics, how to handle missing context
- [references/qualify.md](references/qualify.md) — bid/no-bid checklist; lightweight variant for non-competitive assets
- [references/gates.md](references/gates.md) — gate discipline rules, rationalization tables, red-flags lists, letter-vs-spirit clauses
- [references/state-file-template.md](references/state-file-template.md) — living-log state-file schema (current-truth block, decision/reviewer/change logs, locked rulings, evidence-continuity map, constraint register, voice bar, terminology ledger, artifact registry) and filled example
- [references/build-validation.md](references/build-validation.md) — analytical validation checklist for self-contained HTML assets (structure, geometry, content scans, dual-view integrity, post-cut orphan check); the visual pass stays with the user
- [references/dispatch.md](references/dispatch.md) — the shared subagent method for every fan-out in the suite: brief structure, model routing by work type, concurrency, and how to treat returns
- [references/export-paths.md](references/export-paths.md) — PDF and single-view exports (print-CSS discovery, the specificity trap, pagination by artifact type, blank-proofing)

## Conventions

Always use `[CLIENT]` as the placeholder for the customer name — never write the real name.
