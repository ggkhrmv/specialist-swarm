---
name: positioning
description: Shape the win strategy and positioning of a competitive or advisory asset — win themes, discriminators and why-us, commercial and price-to-win posture, proof points, tiered scope options, and explicit-assumptions and honest-boundary plays; for tenders, extract and cluster requirements (MUST/SHOULD, preserved IDs) and maintain a compliance/traceability matrix and a claims register. Use when deciding how to position a proposal, bid, or pitch, choosing scope options, defining win themes, or responding to an RfP or RfQ. Not for narrative structure (see storyline) or slide build (see presentation-websites).
---

# positioning

## When to use

Use this skill when you need to decide how to enter a competitive bid or advisory engagement: what win themes to lead with, where you genuinely differ from the alternatives, what commercial model fits, and how to handle scope that is uncertain or immature.

Use it for tender mechanics when an RfP or RfQ is in scope: extracting and clustering requirements, tracking MUST/SHOULD status, building the compliance/traceability matrix, and maintaining the claims register.

Do not use it for narrative structure — how sections flow and hang together belongs to the `storyline` skill. Do not use it for slide build or visual layout (see `presentation-websites`). Do not use it for prose quality or AI-language review (see `asset-review`).

## The positioning frame (first output, before anything else)

Before any play, state the **frame** in one line: what this asset is *for* and, crucially, what it is *not*. The frame is the single decision that, taken wrong, invalidates every section and forces a whole-asset rebuild after it is already built — e.g. an asset built as a *guardrail / governance* pitch when it should have sold an *AI enabler / accelerator*. It is cheap to decide up front and ruinously expensive to discover after Build.

Schema: `Positioned as [subject] gaining [frame], owned by [scope], NOT [the frame it is often mistaken for].`

The frame must fix three things, and all three get read back to the user:

- **The subject that gains the capability** — the client's system, service, or organisation, not your team, capability, or offering. Confusing the builder with the thing built inflates the claim and reads as a land-grab.
- **The owner scope** — one team, or a cross-team effort.
- **What it is not** — the frame it would be mistaken for.

**The protagonist test.** Read the frame aloud as a sentence and ask who the actor is. If the actor is *us* — "we become their X", "our capability is the Y" — rewrite it with the client's asset as the subject and test again. This matters because frames with us as protagonist **survive review of the wording and fail review of the angle**: in practice a frame passed its gate, was built, was reviewed, and was declared complete before the wrong subject surfaced — costing a full structural re-cut, a rebuild, and a second review board.

Agree the frame line with the user, record it in the state file's decision log, and carry it into the Frame + Storyline gate alongside the governing thought. Every win theme, discriminator, and section must serve this frame. A change to the subject or the owner scope is a structural re-cut, not a copy pass.

## Plays

Plays are selected based on what the intake material reveals — a specific competitive threat, a scope ambiguity, a commercial decision the client has not framed yet. Pick the plays the situation calls for. Do not run them all.

**Offensive** — use when actively competing and evaluator attention is the constraint:
- win-themes: the messages the evaluator should be able to repeat back after reading
- discriminators/why-us: where you are genuinely different from the specific alternatives in this deal
- commercial/price-to-win: T&M vs managed, value- vs cost-based framing, phased land-and-expand
- proof-points/references: named client evidence mapped to the win themes, not generic industry claims

- dimension-the-ask: bounded envelope, labelled targets, falsifiable gates, accountability line — for any asset that asks for funding or an endorsement

**Defensive** — use when scope is uncertain, the brief is immature, or over-committing risks disqualification or delivery failure:
- tiered-scope-options: define A/B/C or equivalent levels; avoids a binary yes/no that either disqualifies you or traps you
- lead-don't-answer-the-checklist: structure the response around clusters and arguments, not 1:1 to every requirement line
- phased-entry/diagnose-in-first-phase: scope assessment as the first commercial milestone; use only when a build or run phase is a realistic next step
- make-assumptions-explicit: surface the scope boundaries the client has not named, so they own residual ambiguity
- honest-scope-boundaries: state what falls outside scope and why; do not leave gaps the client will discover after signing
- answer-the-cheaper-alternative: name the cheapest remedy a skeptic would propose instead — especially the one your own diagnosis supports — and show you sequence it rather than replace it
- publish-the-counter-evidence: negative control, robustness cut, what moved against you, refuse circular credit
- measurement-gap-as-finding: when the client's systems cannot evidence the claim, publish the gap and scope the instrumentation rather than shipping a proxy

Read [references/plays.md](references/plays.md) for each play in full (name · when · how · one example).

## Tender mechanics

When the asset is a formal response to an RfP or RfQ, read [references/rfp-mechanics.md](references/rfp-mechanics.md) before starting any work. It covers requirement extraction (preserving original IDs verbatim), MUST/SHOULD treatment (MUST = K.O. criterion, not a preference), and the clustering method. The response maps to clusters, not to individual requirement lines.

## Win themes

Produce 3-4 win themes at the end of the Frame phase. Each theme is a short declarative sentence paired with its proof point. The orchestrator records them in `asset-forge-state.md` under the Win themes section; they are consumed downstream by the `storyline` exec summary (governing thought alignment) and by the `asset-review` altitude check (win theme coverage — any win theme asserted without supporting evidence is flagged as a P1 redline entry).

Schema: `theme | proof point`. Win themes are a persisted output of this skill alongside the claims register.

## Proof points and metrics sourcing

Proof points and any headline metric must be **sourced, not invented**. When the win themes need external evidence (industry benchmarks, DORA-type findings, market stats), research them — web search is allowed and expected — and record each with its source. Two hard rules:

- **Never present a hoped-for client delta as if it were measured.** "Cuts provisioning time by 40%" is a fabrication unless a named source says so for a comparable case. If the number is a target, label it a target.
- **Every metric enters the claims register** as `verified` (named source) or `aspirational` (a goal/illustration), so the `asset-review` claims check can confirm it. An illustrative external result (e.g. a vendor's published benchmark) is `verified-as-external-illustration`, not a promise about the client's platform.
- **Check that the metric measures what you are claiming with it.** A proxy that measured something adjacent is worse than no number, because it looks sourced. Confirm the sample supports the inference too — a rate over 46 items does not carry a population claim. If the data cannot support the figure, do not manufacture a derivation: ship it labelled as a target with no measured baseline, name where and when the baseline gets set, and record the flag in the open-items queue so it resurfaces if challenged.
- **Verify your own side's maturity before a claim rests on it.** See the status ladder below.

## Own-side maturity — the status ladder

Before locking a frame or a claim that rests on your *own* capability being real, place it on this
ladder and record which step it actually reaches:

1. **Code or configuration exists** in a repository.
2. **Proven once** — a demo, an end-to-end run, a spike.
3. **Deployed** to an environment.
4. **Running on a schedule, producing real ongoing output.**

**Never accept a README, a design document, a roadmap, or a subagent's summary as evidence of step 3
or 4.** Require the artifact: a run id, a commit, a log, a real output record.

This exists because a research pass reported a capability as "live-verified end-to-end", the whole
positioning frame was built on "proof we already have", and the user caught it — the recurring runs
were smoke tests, the key path was unmerged, and it had been proven once by hand. Verification found
step 2 where the asset claimed step 4.

If the honest answer is step 1–2, the frame is **"de-risked, not done"** — which is the more
defensible frame anyway, because nobody in the room can puncture it.

## The investment case

Any asset that asks for a decision, funding, or endorsement must state the ask, the status-quo
baseline, and at least one measured-metric target — in the unit the approver controls — plus
falsifiable gate criteria. A measured problem with an adjectival return is a named defect, and it is
the single most reliably-missed thing in an asset that asks for something. Method, the correspondence
check, and what to do when a number is not yours to give: [references/investment-case.md](references/investment-case.md).

## Terminology ledger and naming discipline

Coherence across an asset (and across a multi-artifact system) depends on calling each concept by **one** name. Drift here reads as imprecision and breaks MECE continuity.

- **Lock canonical names** in the terminology ledger (a table in the state file): concept → the name to use everywhere → names *not* to use → any load-bearing count or fact (e.g. "exactly six"). Inventing a synonym for a concept that already has a name is a defect, not variety — "the six dimensions" does not become "the six jobs" three sections later.
- **Never carry a name verbatim from a source input.** Labels lifted straight from a screenshot, a reference deck, or an RfQ ("Orbit agent", a borrowed section title) are placeholders, not decisions. Propose a name deliberately, agree it, and lock it in the ledger.
- **Guard load-bearing counts and phrases** — "one API" vs "multiple APIs", "four layers" vs "five" — the ledger is the single source of truth; the `asset-review` consistency gate checks the asset against it.

## Claims register

Every capability claim written in the asset should be marked as `verified` (you have a named reference, a live project, a published datasheet) or `aspirational` (planned, intended, or believed). Aspirational claims are not wrong — they become dangerous only when they are hidden inside confident language. The `asset-review` skill checks the register at the Review gate.

Schema: `claim | verified/aspirational | source`. Open the register as you write the first claim; do not backfill at the end.

## Compliance/traceability matrix

The matrix tracks how every requirement in the RfQ is addressed. Schema and sign-off workflow in [references/compliance-matrix.md](references/compliance-matrix.md). It is maintained from Intake through Review; the `asset-review` skill signs it off.

## Reference files

Read these when the task calls for it:

- [references/plays.md](references/plays.md) — every play with when/how/example
- [references/investment-case.md](references/investment-case.md) — the three numbers (ask, status-quo baseline, labelled target), falsifiable gates, the correspondence check
- [references/evidence-from-client-data.md](references/evidence-from-client-data.md) — read when a claim rests on the client's own data: coverage denominators, the single-instrument fallacy, negative controls, the robustness triad, figure provenance, estimating an unmeasured number
- [references/rfp-mechanics.md](references/rfp-mechanics.md) — tender mechanics (read only for tender responses)
- [references/compliance-matrix.md](references/compliance-matrix.md) — matrix schema, cautionary example, sign-off
- [references/examples/illustrative-platform-rfq.md](references/examples/illustrative-platform-rfq.md) — one fictional worked case (sovereign Kubernetes platform bid); this is an example, not a template

## Conventions

Always use `[CLIENT]` as the placeholder for the customer name and `[FIRM]` for the bidding firm — never write the real names.
