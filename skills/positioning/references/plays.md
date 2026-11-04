# Positioning Plays

Each play: name, when to use, how to execute, one example. Plays are selected from intake guidance — do not apply them all.

---

## Offensive plays

### win-themes

**When:** You are in a competitive bid and need the evaluator to carry specific messages out of the room after reading. Win themes are not the same as selling points — a selling point is something you have; a win theme is a message the evaluator repeats to a colleague.

**How:** Draft 3-4 short declarative sentences that answer the evaluator's implicit question: "Why them, specifically?" Each theme should be tied to something the client cares about most (from intake), falsifiable by a competitor (otherwise it is not a discriminator), and supported by at least one named proof point.

Run a quick test: could your closest competitor claim the same theme with the same words? If yes, the theme is not differentiated enough.

**Example:** For a sovereign Kubernetes platform bid where the client's stated priority is control-plane independence:
- "[FIRM] delivers sovereign Kubernetes management with zero proprietary lock-in, validated across three comparable central-European infrastructure programs."
- "Our Assessment-first model means [CLIENT] sees a dependency map and priced options before committing to build or run scope — no other bidder has offered that."
- "Our on-/near-/offshore delivery model can staff [CLIENT]'s 24/7 SLA requirement without the FTE overhead of a fully onshore model."

---

### discriminators/why-us

**When:** You know who the other bidders are (or can infer from the market), and you need to name concrete reasons the client should choose you over them.

**How:** For each key competitor, identify one or two areas where the evaluator's top priorities intersect with a genuine gap in the competitor's position. Be specific — a discriminator is a named capability, reference, or structural advantage, not a vague claim like "our people are better." Then flip it: what is the competitor's likely best argument, and how do you blunt it?

**Example:** Against an incumbent hyperscaler competing on an open-source managed Kubernetes bid:
- Discriminator: "We operate the control plane on [CLIENT]'s own infrastructure; the hyperscaler cannot offer that without forking its managed service."
- Counter to their likely best argument: "Their scale advantage is real for cloud-native workloads but not for on-premises sovereign control planes — different competency."

---

### commercial/price-to-win

**When:** The commercial model and price point are not yet fixed, or you are deciding whether to lead on cost or on value framing.

**How:** Three decisions in sequence:
1. **Model:** T&M (transparency, easy scope adjustment, shared risk) vs managed-price/fixed-scope (client wants predictability, you have high confidence). Phased land-and-expand starts T&M in assessment, moves to managed in build/run once scope is validated.
2. **Framing:** Value-based (price anchored to the risk you are removing or the revenue you are protecting) vs cost-based (price anchored to day rates and resource counts). Value framing requires you to quantify the client's exposure; cost framing is defensible on transparency but invites comparison on rate cards alone.
3. **Price-to-win:** What is the highest price the client will pay, given their budget signals, the competition, and their sensitivity to delivery risk? Work backward from that number to check whether your cost structure allows a margin.

**Phased land-and-expand:** Price assessment at a level that removes friction to starting. Do not compress margin on build/run to fund a cheap assessment — that sets a bad anchor and is hard to recover.

**Example:** For an assessment-first managed Kubernetes engagement:
- Assessment: T&M, time-capped (6 weeks), priced at €X to remove the "what are we signing up for?" objection.
- Build: T&M with a milestone-based structure; scope confirmed by assessment output.
- Run: Managed price once the steady-state is known. Optional, offered as outlook only.

---

### proof-points/references

**When:** You have won-themes and discriminators but no evidence behind them — or your evidence is generic ("we have done many Kubernetes projects") rather than specific.

**How:** For each win theme, map at least one named client reference with: client name (or sector if confidential), scale of engagement comparable to this one, and the specific outcome relevant to this theme. A reference that proves "[FIRM] can do Kubernetes" is weaker than one that proves "[FIRM] has run a sovereign, on-premises Kubernetes platform for a regulated European enterprise."

Flag any theme that has no named reference — add it to the claims register as `aspirational`.

**Example:** Win theme: "Assessment-first reduces re-scope risk in sovereign platform programs."
- Reference: [REFERENCE-A] (European logistics group) — platform migration engagement where a six-week assessment phase identified two dependency chains that would have caused production outages; migration path redesigned before build began.
- Reference: [REFERENCE-B] (regional public-sector IT provider) — open-source migration assessment that scoped three regulatory compliance gaps before any infrastructure was touched.

---

## Defensive plays

### tiered-scope-options

**When:** The scope is too large, too uncertain, or too risky to commit to in full. A binary yes/no risks either disqualifying you or trapping you in a commitment you cannot deliver.

**How:** Define two or three scope levels with distinct deliverables, timelines, and prices. Each level must be coherent on its own — not "full minus some things" but a genuinely viable engagement at that scope. Name them descriptively (not just A/B/C) so the evaluator understands what they are buying at each level.

A/B/C is one instance of this pattern, not the rule. Two levels may be enough; four is usually too many for a client to decide between.

**Example (A/B/C instance for a platform program):**
- Option A (full scope): Assessment + Build + Run including 24/7 managed operations, KubeVirt consolidation, and full knowledge transfer to [CLIENT] team. 20-month program.
- Option B (focused scope): Assessment + Build, handover to [CLIENT]-led operations with support wrapper. KubeVirt consolidation as a Phase 2 option. 12-month engagement.
- Option C (minimal scope): Assessment only. Output: validated inventory, dependency map, risk-adjusted options for [CLIENT] to take to market or execute internally.

---

### lead-don't-answer-the-checklist

**When:** The RfP or RfQ has 40+ requirements and a 1:1 response would produce a table that no evaluator reads.

**How:** Cluster the requirements by theme — group by the logical structure of the work, not by the RfQ's section numbering (though the two often align). Aim for 5-10 clusters for a 40-70 requirement RfQ. Write one coherent response per cluster that addresses all requirements in that cluster through a single argument. Cross-reference requirement IDs at the end of each section so the evaluator can trace compliance without reading a 62-row table.

This is not a way to avoid answering requirements — every MUST requirement must be addressed. It is a way to make the response readable.

**Example:** Cluster 4 (Security, Identity & Compliance) has nine MUST requirements covering zero-trust network policy, identity federation, and admission control. Rather than answering each in sequence, write a single section titled "Zero-trust security with open-source tooling meets all nine MUST requirements in Cluster 4" and structure it as: network policy approach → identity federation design → admission control mechanism. End with a cross-reference table: requirement ID, covered in section, notes.

---

### phased-entry/diagnose-in-first-phase

**When:** The technical or organizational risk of a direct commitment to build or run is too high, AND there is a realistic delivery runway after the assessment phase.

**How:** Propose assessment as the first commercial milestone, with a defined output (dependency map, options analysis, risk register) that gates the decision to proceed. Make clear what decision the client is making at the assessment gate, and what the assessment does not decide.

Only use this play when the subsequent phases are genuinely possible — do not propose an assessment as a way of winning the work if you have no realistic path to delivering the build. The client will notice.

**Example:** For a Kubernetes platform with 26 clusters and unclear dependency chains: "A six-week Assessment produces a validated infrastructure baseline and a risk-adjusted migration path. At the Assessment gate, [CLIENT] decides which scope option (A/B/C) to proceed with and on what timeline. The Assessment does not commit [CLIENT] to a build or run engagement with [FIRM]."

---

### make-assumptions-explicit

**When:** The brief contains fuzzy requirements, technical contradictions, or scope items that depend on facts you do not have.

**How:** Write a numbered assumptions list early in the proposal. For each assumption, state: what you are assuming, why (what information is missing), and what changes if the assumption is wrong. Do not bury assumptions in footnotes or appendices.

Fuzzy requirements in a RfQ are not your problem to solve — they are the client's problem to clarify. Surface them explicitly so the client owns the residual ambiguity.

**Example:** For a RfQ that lists "VMware, OpenStack, or bare metal" as potential infrastructure targets without specifying which applies:
- Assumption 1: "[CLIENT]'s current VMware estate is the migration baseline. If OpenStack or bare metal is in scope, the dependency map and migration toolchain change materially."
- Assumption 2: "KubeVirt consolidation is aspirational, not committed. We have scoped Option A assuming it is in scope; Option B excludes it."

---

### honest-scope-boundaries

**When:** There are parts of the RfQ or client ask that fall outside your capability, your risk appetite, or the scope you are willing to commit to.

**How:** State the boundary explicitly and briefly. Name what you will not do and why — not defensively, but as a boundary that protects both parties. Follow immediately with what you will do instead, or what the client's options are for the out-of-scope item.

Do not hide out-of-scope items in vague language or commit and then re-scope during delivery.

**Example:** "Our scope covers the Kubernetes control plane, platform tooling, and managed operations. Day-2 application development and migration of individual workloads sits outside this scope. [CLIENT]'s application teams retain ownership of workload migration, supported by the runbook and knowledge transfer deliverables in Option A."

---

### dimension-the-ask

**When:** The asset asks for funding, headcount, or an endorsement — especially an internal one, where the instinct is to keep the ask soft and let the argument carry it.

**How:** A deliberately quiet ask still needs one small, concrete thing to say yes to. Carry four elements: a **bounded first-phase envelope** (people × duration, capped, with later phases explicitly deferred); **labelled TARGETs** tied to the metrics the problem was measured in; **one line of go/no-go criteria per phase transition**, including what would make you stop; and a **high-level accountability line** — who owns what, and how cross-team conflict is arbitrated — even when the detailed ownership split is deliberately out of scope.

Without these, the audience defers. Three reviewer personas independently made this the room-closer on one asset: *"The fund ask has no magnitude. I am being asked to sign a blank cheque"*, and *"'each phase gated' is the stated risk control, but only the first phase has gate criteria."*

Full method, the status-quo baseline requirement, and the correspondence check: [investment-case.md](investment-case.md).

**Example:** "Phase 0 is three engineers for one quarter. Phases 1–2 are scoped but not costed here; the Phase 0 gate decides whether they proceed. TARGET: absorb 40% of the measured 9-FTE operational load, baselined at the gate. No-go: if two of the six evaluation tracks fail, the programme stops and we publish what we learned."

---

### answer-the-cheaper-alternative

**When:** Always, for any recommendation — and urgently when your own diagnosis supports a cheaper remedy than the one you are proposing.

**How:** Name the cheapest alternative a skeptic would propose instead of your recommendation, **especially the one your own analysis points to**, and doubly so if the organisation has already prescribed it. Concede it in the asset. Then show that your proposal **sequences** it rather than replaces it.

Handled this way the strongest objection becomes your sequencing rationale. Omitted, it is the first thing said in the room — this was a P0 in two consecutive review rounds on one asset, found from opposite directions: *"You've mislabelled a governance/ownership problem as a toil-automation problem. Fix ownership and standardise the baseline first — that's cheaper and needs no new capability"*, then *"the problem framing hands the rival a cheaper answer, and it is the org's own prescribed remedy."*

**Example:** "The obvious cheaper answer is to fix the documentation and raise the abstraction level — and it is the right first move. This proposal amplifies a well-defined process and is worthless on an undefined one, which is exactly why the baseline and ownership work comes first, inside Phase 0, before any of the rest is funded."

---

### publish-the-counter-evidence

**When:** Any asset whose credibility rests on measurement you produced yourself.

**How:** Four moves, each costing a sentence, that together buy more credibility than any additional supporting figure:

- **Negative control** — the same measurement over a population where the effect should be absent, showing that it is.
- **Robustness cut** — the headline under a deliberately conservative definition as well as your own.
- **Publish what moved against you** — the indicators that worsened and the caveats that cut against your own reading, in the same place as the good news, not in an appendix.
- **Refuse circular credit** — where a benefit would be counted using the very thing you are asking to build, say so and decline to count it.

A skeptical reader takes these as evidence that the rest of the numbers were treated the same way. On one asset the red team's verdict on such a block was: *"I have no attack on it that does not require alleging fabrication."* And **do not let a later polish pass flatten any of them** — a tidying edit deletes exactly these sentences first.

Method and worked detail: [evidence-from-client-data.md](evidence-from-client-data.md).

**Example:** "Deflectable tickets book a 2.8h median; non-deflectable 12.0h. The classifier only ever read descriptions and never saw a worklog, so effort corroborates a classification built without it. Under the most conservative definition the share falls from 74% to 57%. We are not counting the loop's own productivity gain: counting the thing we propose to build would be circular, and it would flatter the case."

---

### measurement-gap-as-finding

**When:** The client's own systems cannot evidence a claim the asset needs, and you have exhausted the available channels.

**How:** Publish the gap rather than a proxy. State what cannot currently be traced, name the two or three cheap instrumentation fixes, and scope a first-phase measurement track with a baseline date. The instrumentation gap is a legitimate finding in its own right, and it converts a dead end into a funded workstream.

Use only when the gap genuinely blocks a decision the client cares about — otherwise it reads as an excuse.

**Example:** "There is no mechanism in the current data that traces platform work back to the demand that caused it — and that is the finding. Two configuration changes in the tracker plus one required field make it measurable; a baseline follows eight to twelve weeks later. Phase 0 carries that measurement track."
