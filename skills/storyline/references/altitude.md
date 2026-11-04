# Altitude

## The three altitudes

**Executive:** The reader makes resource and direction decisions. They need to know: what is the situation, what is the risk/opportunity, what is the recommendation, and what do they need to decide or approve? They do not need implementation detail. They need confidence that someone who does understand the detail has synthesized it correctly. Executive readers have little time, so the exec summary must make its case on one page.

**Architect:** The reader designs or evaluates technical systems. They need to know: what are the constraints, what are the options, what are the trade-offs, and why does the recommended option perform better on the criteria that matter? They are skeptical of claims without specifications. They need enough detail to replicate the reasoning, not the full engineering spec.

**Mixed (exec + architect in the same room):** The most common and hardest case. The exec section of each slide carries the claim at executive altitude; the architect section carries the supporting detail. Physically, this often means an action title (exec altitude) + a visualization or table (architect altitude). The executive skims the titles; the architect reads the body.

## Choosing altitude from intake

Ask or infer:
- Who is in the room? Name the roles.
- What is the read path? (Will this be presented live, or sent to be read asynchronously?)
- What decision are they being asked to make?

If roles are mixed and the meeting is live-presented, default to mixed. If it is a written document sent for async review, bias toward executive (less detail survives reading without narration).

## Per-section altitude check

Not every section of a proposal runs at the same altitude. A useful default for a multi-section proposal:

| Section | Expected altitude |
|---|---|
| Exec summary | Executive |
| Situation diagnosis | Executive, with architect detail in appendix |
| Solution per requirement cluster | Mixed — claim at exec, evidence at architect |
| Implementation plan | Architect, summarized at exec in the intro slide |
| Commercial and contractual | Executive |
| References/CVs | Architect (they are evidence, not claims) |

Check each section against this table. If a references section is pitched at executive altitude (big claims, no specification), it will not satisfy architect skeptics. If an exec summary is pitched at architect altitude (long specifications, no recommendation), the exec will not read it.

## The promotion check (two-view assets)

Run this after any review, on any asset with two views or two altitudes.

**The asset's most credible sentence is usually a concession or a boundary — and concessions drift into the technical view, where the decision-maker never reaches them.**

Ask: what is the most disarming line in this asset, and which view is it in? If it is only in the low view, **promote it**. The exec view carries the claim **and** the strongest concession behind it; the technical view carries the mechanism.

This inverts the usual instinct, and the evidence for it is consistent. In one review, three separate personas independently named a refusal to claim a self-flattering number as the most credible content in the whole asset — and it was behind a toggle. In another, the single most disarming line (a concession that an estimate was sized as if the work were done entirely by hand) was in the technical view; promoting it into the headline cost box was applied as a P1.

Related: a **tension between two claims both visible in the default view must be reconciled in that view**. A reconciliation that lives only in the architect layer does not exist for the default reader, and unreconciled it reads as spin. See `asset-review/references/self-consistency.md`.

## Why-us and hooks are asset-type-conditional

Why-us content (your firm's credentials, track record, differentiators) and narrative hooks (stories, analogies, provocative framings) are not globally wrong at any altitude. The question is whether the section's purpose is diagnostic (here is what is true about [CLIENT]'s situation) or persuasive (here is why [FIRM] is the right partner).

**Diagnostic sections** — problem statements, requirement mappings, gap analyses — should not include why-us. The evidence should speak for itself. A problem statement that keeps circling back to the bidder's own capabilities reads as self-serving and undermines the diagnosis.

**Persuasive sections** — solution framing, commercial model, references — should include why-us. Omitting it in a persuasive section is a missed opportunity.

**Hooks and framing** work at executive altitude when they give the reader a mental model for the argument (a one-sentence analogy that makes the complication concrete). They fail when they are used to delay or avoid the governing thought.

**Use-case sections in capability showcases** have a specific opening pattern: anchor the section to a problem the specific audience owns, then show the capability addressing it. Capability-first openings read as vendor-led because they start from what you can do rather than what this room needs to solve. The problem anchor gives the demonstration a reason to exist for this audience.

## Three altitude-mismatch examples

**Example 1 — too low for exec**
Section: Exec Summary
Problem: Three pages of Kubernetes architecture diagrams with component labels, no recommendation visible in the first paragraph.
Fix: Lead with the governing thought as the first sentence. Move the architecture diagram to the solution section or appendix. The exec summary should be readable in 90 seconds.

**Example 2 — too high for architect**
Section: Solution — Cluster 4 (Security, Identity & Compliance)
Problem: "[FIRM] will ensure [CLIENT] meets all security requirements using industry best practices and our proven methodology."
Fix: Name the specific tools (OPA/Gatekeeper, Falco, SOPS, Vault), map them to specific requirement IDs (4.2.x), and state the constraint each tool addresses. Architects need to be able to disagree with the choice.

**Example 3 — why-us in wrong section**
Section: Gap analysis — current estate vs. RfQ requirements
Problem: Every gap identified ends with "[FIRM] has deep expertise in this area."
Fix: Remove the why-us from the diagnostic. The gap analysis should be cold — here is what exists, here is what is required, here is the gap. The why-us belongs in the solution section, where the response to each gap names the specific capability or reference [FIRM] brings.
