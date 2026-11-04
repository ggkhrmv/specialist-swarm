# RfP / RfQ Mechanics

This file covers the mechanical work of responding to a formal tender: extracting requirements, tracking them, clustering them, and mapping the response. Read this before starting any tender response — the choices made at intake are hard to undo later.

---

## Requirement extraction

Extract every requirement from the source document. Preserve the original ID exactly as it appears — do not renumber, abbreviate, or rephrase. If the RfQ uses `4.2.1.3`, carry `4.2.1.3` through every artifact: the compliance matrix, the response text, the claims register.

Why this matters: evaluators score against their own ID list. If your matrix uses different IDs, they cannot trace your coverage without doing a mapping exercise, and they will not bother.

When extracting, capture for each requirement:
- Original ID
- Full requirement text (verbatim, or a faithful short form with the source text quoted in a note)
- MUST or SHOULD designation

Do not interpret at extraction time. Extract first, cluster second, respond third.

---

## MUST / SHOULD treatment

MUST requirements are K.O. criteria. A single uncovered MUST is grounds for disqualification, regardless of how well you address the SHOULD requirements. Treat them accordingly: every MUST gets an explicit, traceable answer in the compliance matrix before anything else.

SHOULD requirements matter — they affect scoring — but they do not knock you out. You may address them partially, with conditions, or defer them to later phases. Document your treatment clearly.

Common mistake: treating a SHOULD as optional because it sounds like one. Read the RfQ's scoring section if present. Some evaluators weight SHOULD requirements heavily in the technical score.

---

## Clustering

After extraction, group requirements into clusters before you start writing. The clusters should reflect the logical structure of the work, not necessarily the RfQ's section structure (though often they align).

Good clusters are coherent enough that a single section of the response can address all requirements in the cluster through one unified argument, rather than answering each requirement in sequence.

Aim for 5-10 clusters for a 40-70 requirement RfQ. More than 10 clusters usually means you are treating requirements as atomic rather than grouped.

Label each cluster with a short name and list the requirement IDs it contains. This becomes the mapping structure for your response.

**Example:** An RfQ with 62 requirements across platform, security, networking, observability, SLA, transition, and commercial topics clusters naturally into 7 groups. The cluster names become section headings in the response. Within each section, requirements are addressed through the section argument — individual IDs are cross-referenced in the compliance matrix, not repeated in prose.

---

## Response structure: map to clusters, not to requirements

The response document is organized by cluster, not by requirement line. Each cluster section makes a claim (the argument) and supports it with specific, evidence-backed assertions that collectively cover every requirement in the cluster.

At the end of each section, add a cross-reference: a small table or list linking requirement IDs to where in the section they are addressed. This keeps the narrative readable while maintaining traceability.

Do not write a response that answers requirement 3.1, then 3.2, then 3.3 in sequence with a paragraph each. That produces a document that reads like a checklist answer, not a proposal. It signals that you have no perspective — you are just filling boxes.

---

## Compliance matrix

The matrix is the traceability artifact that ties the response back to the source requirements. Schema: one row per requirement, with columns for requirement ID, MUST/SHOULD, covered (yes/partial/no), where in the response, and any qualifying notes. Populate it as you write — not after. A matrix built after the fact often discovers coverage gaps when it is too late to fix them.

---

## Claims register

As you write each cluster section, log claims in the claims register (schema: `claim | verified/aspirational | source`). Any statement of capability, track record, or delivery approach that an evaluator might rely on when scoring should appear in the register.

Flag aspirational claims as you go. Do not compress them into confident language to make the proposal look stronger — that creates a problem at delivery if the claim is not met, and it creates a credibility risk if the evaluator is sophisticated enough to ask for evidence.
