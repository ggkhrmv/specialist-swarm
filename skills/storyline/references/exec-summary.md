# Executive Summary

## What it must do

The exec summary is the one artifact a CIO or VP will read even if they read nothing else. It must be self-contained: a reader who stops after the exec summary should understand the situation, the recommendation, and the ask — without relying on the rest of the document to fill in the logic.

It is not an introduction. It does not say "this document covers X, Y, Z." It makes the argument in compressed form.

## Structure: governing thought → three supports → ask

**Governing thought (1–2 sentences):** The same sentence that sits at the pyramid apex. This is the first sentence of the exec summary, not buried at the bottom. If the reader agrees with the governing thought, the rest of the summary explains why. If they disagree, it gives them a target to argue against — which is better than a document they cannot engage with.

**Three supporting claims (1 paragraph each, ~3–4 sentences):** These correspond to the three MECE groups from the pyramid. Each paragraph states the group claim, cites one or two specific evidence points, and makes the implication explicit. Do not list every proof point — pick the one that is hardest to argue with.

**Ask (2–4 sentences):** What do you want the reader to decide or approve? Be specific. "We recommend [CLIENT] approve a six-week Assessment engagement beginning in April, with a defined go/no-go gate before any build-phase commitment." is an ask. "We look forward to the opportunity to work together" is not.

## Relationship to win themes

Win themes are the two or three differentiating reasons [CLIENT] should choose [FIRM] over any other bidder. They come from the `positioning` skill (specifically from the intake work that maps [CLIENT]'s stated priorities against [FIRM]'s strongest proof points). The exec summary does not generate win themes; it uses them.

Each supporting paragraph in the exec summary should carry at least one win theme signal — a reference to the capability, the precedent, or the framing that positions [FIRM] distinctively. If a paragraph has no win theme in it, it is descriptive rather than persuasive.

## Stands-alone test

Read the exec summary with the rest of the document hidden. Ask:
1. Can a reader state the recommendation after reading it? (Yes → pass)
2. Does the reader know what to decide or approve? (Yes → pass)
3. Is there a claim that requires the body of the document to be understood? (Yes → fail — promote the context or rewrite the claim to be self-contained)

If the exec summary fails the stands-alone test, it is functioning as an introduction rather than a compressed argument. Rewrite from the governing thought down.

## Length and format

One page is a target, not a rule. A two-page exec summary for a 60-page proposal is defensible. A three-page exec summary is usually a sign that the argument has not been synthesized.

Avoid bullet lists in the exec summary. Bullets atomize; the exec summary should synthesize. Flowing paragraphs force the logical connectives ("because", "therefore", "however") that hold the argument together.

## Common failure modes

**Chronological narrative instead of argument.** "In February, [CLIENT] issued an RfQ. In April, the shortlist was reopened. In June, conversations revealed…" The exec summary is not a timeline. Cut the history and start from the current situation.

**All three support paragraphs at the same altitude.** One paragraph on technology, one on process, one on commercials — all written at the same level of abstraction — reads as a checkbox exercise. Vary depth: the paragraph on the most contentious claim needs more evidence than the paragraph on the obvious one.

**Weak ask.** "We hope to partner with [CLIENT] on this initiative." No decision, no timeline, no gate. Replace with: who decides, what they are deciding, and by when.

**No governing thought in the first sentence.** Many exec summaries bury the recommendation in the final paragraph. The reader who stops halfway through has no idea what you are recommending. Put it first.

## Worked example structure (sovereign Kubernetes proposal)

**Governing thought:** [CLIENT] should adopt a sovereign, open-source Managed Kubernetes Platform through an Assessment-first engagement, because the technical dependencies and governance gaps in the current estate make a direct migration too risky to commit to before a structured discovery sprint.

**Support 1 (technical risk):** The current 26-cluster estate spans two cloud providers and depends on proprietary service meshes and ingress controllers that conflict with the RfQ's open-source and sovereignty requirements. A dependency audit — completed in the Assessment phase — is the only way to produce a validated migration path rather than a plan built on assumptions.

**Support 2 (capacity and governance):** [CLIENT]'s platform team has limited experience managing a large external delivery engagement, and the T&M model required by the RfQ demands governance structures that do not currently exist. The Assessment phase builds these structures and produces the staffing and knowledge-transfer plan before build scope is committed.

**Support 3 (commercial protection):** An Assessment-first structure gives [CLIENT] a contractual gate before any build or run commitment, limits financial exposure in the discovery phase, and produces the evidence needed to choose between Options A (full scope), B (reduced scope), and C (minimal scope) based on findings rather than estimates.

**Ask:** We recommend [CLIENT] approve a six-week Assessment engagement beginning in Q2, with a defined scope decision gate at week five before any build-phase contract is signed.
