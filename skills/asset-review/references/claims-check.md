# Claims check

## Purpose

Every capability claim in a consulting asset sits in one of three categories. The check is about confirming which category each claim belongs to and making sure the language in the draft matches it.

**Verified** — the claim is backed by a named source: a delivered project, a published case study, a confirmed client reference, a certified tool in production. "We deployed Argo CD at [CLIENT] in 2023" is verified if there is a project on record. "We are an AWS Advanced Partner" is verified if the certificate exists.

**Aspirational** — the claim describes a planned capability, an intended direction, or something the team believes it can do but has not yet done in this form. Aspirational claims are not wrong. They become dangerous only when they are phrased in past tense or presented as credentials.

**Disallowed** — the claim is fabricated, unverifiable, or specifically contradicted by internal knowledge. A certification the person does not hold, a reference project that did not happen, a metric that was not measured. These must be removed, not softened.

---

## Workflow

1. Obtain the claims register from `positioning`. It should carry each claim with its current `verified / aspirational` label and a source column.

2. For every claim labeled `verified`, confirm the source column contains a named reference: project name and year, client name and context, or a link to a public document. If the source column is empty or reads "internal knowledge," treat it as aspirational until a source is supplied.

3. For every claim labeled `aspirational`, check whether the surrounding prose uses confident past-tense language ("we have delivered," "our platform provides," "the team has extensive experience in"). If it does, flag as a redline entry: the claim is aspirational and the language should say so ("we are building toward," "our approach is designed to," "based on our work in adjacent areas").

4. Scan the full draft for capability claims not in the register. Any sentence asserting what the vendor has done, delivered, or been certified for is a capability claim. Add it to the register and classify it.

5. Flag any claim that is fabricated or internally contradicted as disallowed. These are removed, not edited.

---

## Flag criteria

Flag a claim for review if any of the following applies:

- The source column is blank or uses generic language ("our extensive experience," "proven track record").
- The claim uses a certification, award, or credential name that the team cannot produce on request.
- The claim references a named client reference that is not on the approved reference list.
- The phrasing implies the capability is in production when it is planned ("we operate" vs. "we are designing").
- The claim is suspiciously specific: an exact metric, a named person, a precise date that no one on the team can confirm.

---

## Technical soundness — a separate axis from provenance

Provenance (verified / aspirational / disallowed) asks *"can we back this claim?"* Soundness asks a different question: *"is the mechanism actually correct?"* A claim can pass provenance and still fail soundness — it is honestly our own design, but the mechanism as described does not hold. These are the claims an expert challenges in the room, so they map directly to the **author-credibility** and **technical buyer** personas.

For every **load-bearing technical claim**, test the mechanism, not just the source:

- **Is the ordering/timing right?** "Policy engine X validates the change at [point]" — is that actually where and when it runs? (A real miss: asserting a policy engine gates at a point in the flow where it does not run.)
- **Is it stated more strongly than the mechanism supports?** "Prompt injection contained by design", "correct on the first pass", "server-side dry-run guarantees fidelity" (not all admission webhooks are dry-run-aware) — narrow to what actually holds ("aimed at first-pass correctness"; "the merge gate and admission remain the binding controls").
- **Is it internally consistent?** The same mechanism described one way in the exec layer and another in the technical layer is a soundness *and* a consistency defect (e.g. an identity model that is "the user's own identity" in one place and "a dedicated non-human identity" in another).

Flag an unsound mechanism as P0/P1 with a suggested correction that states only what holds. Correcting the mechanism is an architecture decision — surface it for the author, do not silently rewrite the technical model. Record the outcome in the claims register (a mechanism claim that is unsettled is `unsettled — needs an architecture decision`, not `verified`).

Two related checks:

- **A chained metric is judged on its output, not its components.** Propagate each step's measured error to the number you intend to publish, and state the overstatement factor and the share of the reported figure that is real. "Step 2 is 74% accurate" is not publishable; "the headline overstates by 2.8×, 36% of it real" is a decision. Method in the `evidence` skill.
- **Two derivations that share a scoping input are not independent.** A headline presented as the convergence of two methods, where both scoped from the same inventory, is a false claim about method — and the honest version ("we took the midpoint; the agreement rules out an order-of-magnitude error") is stronger.

---

## Voice-pass regression — re-check claims on rewritten lines

A voice or de-slop pass changes tense, modality, and hedging. That makes it **claims-affecting, not cosmetic**, and it is the most reliable way to silently reopen an honesty axis that earlier reviews had closed.

The concrete failure: after a full author-voice rewrite, three of six reviewer personas independently returned P0 overclaims **on lines the author had personally written** — "compliant infrastructure, governed strongly enough for a regulated [SECTOR]", "autonomously implements features and bug fixes", "The platform closes that gap". The voice pass had run a tell-scan and a terminology check. Neither looks at claims.

So: after any voice, de-slop, or author-rewrite pass, re-run this check over **the changed lines only**. For every rewritten headline, benefit card, close row, and title, confirm the new phrasing does not assert as present fact something the asset's own baseline grades as absent, designed, or not built.

**Author-supplied copy gets the same check as generated copy.** The author is writing in vision voice and is not tracking the maturity table line by line — that is your job. Where their wording overclaims, flag it for their ruling rather than rewriting it: their name is on it. And if the author has ruled that present tense is deliberate vision voice for this asset, that ruling goes in the state file's locked-rulings register and this check honours it — while still flagging the specific current-state claims a domain expert would challenge live.

---

## Worked example 1 — kubeVirt-style correction

**Draft text:** "Our platform team has extensive KubeVirt experience, having migrated VM workloads onto Kubernetes at three enterprise clients."

**Check result:** No KubeVirt delivery appears in the claims register. When asked, the team confirms they have run internal proof-of-concept work but have not delivered a KubeVirt migration for a paying client.

**Action:** Flag as aspirational, phrased as verified. Suggested replacement: "Our platform team has run internal KubeVirt proofs of concept and is actively building this capability; we have not yet delivered a production KubeVirt migration at a client site." If the commercial team judges this too damaging to include, the alternative is to remove the KubeVirt claim entirely rather than leave an unverified assertion in the document.

**Why this matters:** An evaluator who runs a reference check will ask for the three clients. If no names can be provided, the claim damages credibility on every other point in the proposal.

---

## Worked example 2 — fabricated credential in a CV

**CV text:** "Certified Kubernetes Security Specialist (CKS) — achieved 2022."

**Check result:** The CKS is a real certification from the Linux Foundation. The individual cannot produce the certificate and does not appear in any internal certification tracking system. The team lead confirms the person attempted the exam but did not pass.

**Action:** Flag as disallowed. Remove the certification from the CV. Do not replace it with a softer formulation ("pursuing CKS" or "CKS-ready") unless the person is actively enrolled in a sitting — and even then, describe it as in-progress, not achieved.

**Why this matters:** Certifications are verifiable. A client who checks will find the discrepancy. A single fabricated credential in a CV calls the entire staffing section into question.

---

## Schema reminder

The claims register schema from `positioning`:

| Claim | verified/aspirational | Source |
|-------|----------------------|--------|
| We deployed Argo CD at [CLIENT] in 2023 | verified | [CLIENT] delivery project, Q3 2023, PM: [name] |
| Our platform supports multi-cloud ingress federation | aspirational | Internal R&D roadmap, Q4 target |

Maintain this register from first draft through sign-off. Do not backfill at the end: claims written in the heat of drafting are the ones most likely to be aspirational phrased as verified.
