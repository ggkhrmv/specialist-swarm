# SCQA + Minto Pyramid

## The four elements

**Situation** — the stable, shared context your reader already accepts. One or two sentences. No drama yet.

**Complication** — what changed, broke, or is about to. The tension that makes your question non-trivial.

**Question** — the question the Complication raises in the reader's mind. Make this explicit; do not assume it is obvious.

**Answer (= governing thought)** — the one sentence that answers the Question and is the apex of your pyramid. Every slide, section, and proof point below it either supports or qualifies this sentence. If you cannot write the governing thought, your argument is not ready.

## The governing thought

Write it as a full declarative sentence. It should be falsifiable — someone should be able to disagree with it. "We recommend a phased, open-source Managed Kubernetes platform because [CLIENT] cannot safely migrate without a structured dependency audit" is a governing thought. "Our platform approach" is not.

The governing thought is also the action title for the first substantive slide of a proposal (or the exec-summary headline). Every other action title in the deck answers: "Why? How? What does that mean for us?"

## MECE grouping

MECE: mutually exclusive, collectively exhaustive. The supporting arguments under the governing thought must:
- Not overlap (mutually exclusive): "Security" and "Compliance" are not MECE if compliance is a subset of security. Merge or split.
- Cover the field (collectively exhaustive): a sceptical reader should not be able to ask "but what about X?" and find X unaddressed.

Two structural patterns for the supporting groups:

**Deductive (top-down):** Major premise → Minor premise → Conclusion. Works when the reader already agrees with the major premise. Fastest for exec audiences.

**Inductive (bottom-up):** Three (or N) parallel observations → one synthesis claim. Works when you are building from evidence up to a conclusion the reader has not reached yet. Better for sceptical readers or new claims.

Use deductive when speed matters; use inductive when credibility building matters.

## Vertical and horizontal logic checks

**Vertical:** Does the governing thought answer the Question? Does each group's claim answer "so what does this group prove?" Does each evidence point directly support its group claim? No evidence point should prove something two levels up directly — it goes to its group claim first.

**Horizontal:** Within each group, do the supporting points add up to the group claim (inductive) or flow as major/minor/conclusion (deductive)? Pick one pattern per group and hold it.

**First use:** the section that *defines* each canonical term precedes every section that uses it. A reorder that satisfies the vertical and horizontal checks can still leave a named entity used two sections before it is introduced, and the reader silently loses the argument.

## House-spine overload

A house spine's labels — WHY / WHAT / HOW, or whatever the house uses — are **unique addresses, not reusable brackets**. Never nest a second instance of a spine label inside the spine. Two "How" eyebrows meaning different things ("how it works" versus "how we deliver it") is a legibility defect, not a nuance: the reader cannot tell which act they are in.

**The diagnostic:** three or more consecutive sections wearing the same spine label while doing visibly different jobs. The instinct is to nest the spine inside the overloaded act. That is the trap.

**The usual cause** is that the argument has **four** semantic buckets competing for three slots:

`justify` · `what it is` · `how it works` · `how we deliver it`

**The fix is re-badging, not nesting.** Justifying sections belong up in the first act. "How it works" belongs with *what it is*, not with *how we deliver it* — it describes the thing, not the engagement. That keeps three acts and gives every section one unambiguous address.

## Evidence-to-claim mapping (one proof point per box)

Each leaf node of the pyramid is one evidence point. It should be:
- Specific enough to be contested (a number, a named reference, a dated fact)
- Directly supporting its parent claim
- Not repeated under another branch

If you find yourself putting the same evidence under two branches, either the branches are not MECE or the evidence is stronger than you thought — promote it.

## Objection pre-emption

Identify the 1-2 strongest objections to the governing thought before finalizing the argument tree. An objection is a counter-claim a sceptical reader could raise: "that is not true," "that does not apply here," or "you have not shown the alternative is worse." Place the rebuttal inside the MECE structure — either as a dedicated group or as a named evidence point within the most relevant group. A rebuttal appended outside the pyramid signals the objection was not anticipated; that weakens rather than strengthens the argument.

---

## Worked example: sovereign Kubernetes platform proposal

**Situation:** [CLIENT] runs 26 Kubernetes clusters across two cloud providers, supporting business-critical applications that require 24/7 availability. The current estate is operationally functional.

**Complication:** [CLIENT]'s sovereignty requirements — mandating open-source tooling and on-premises control plane — cannot be met by either incumbent cloud provider under the current contracts. A regulatory review flagged this gap nine months ago, and the remediation window closes in 24 months.

**Question:** How should [CLIENT] move to a sovereign, fully open-source Managed Kubernetes Platform without disrupting live services?

**Governing thought (Answer):** [CLIENT] should adopt a phased, open-source Managed Kubernetes Platform under a structured Assessment-first engagement, because the technical and organizational risks of a direct migration outweigh the cost of a six-week discovery sprint before any commitment to build or run scope.

### Supporting argument tree (MECE, inductive)

**Group 1 — The technical risk is real and currently unquantified**
- 62 RfQ requirements span 7 clusters; 38 are MUST (K.O.) and include control-plane sovereignty, open-source license purity, and 24/7 SLA continuity.
- Current cluster inventory shows mixed GKE/AKS dependency on proprietary service meshes and ingress controllers not yet replaced by open-source equivalents.
- KubeVirt consolidation of ~400 legacy Linux VMs is a stated strategic goal with no validated migration path.

**Group 2 — [CLIENT]'s internal capacity cannot absorb a direct-migration effort alone**
- The platform team has few FTEs with limited experience managing a large external delivery engagement.
- A T&M delivery model with on-/near-/offshore staffing requires governance structures [CLIENT] does not currently have.
- Knowledge transfer is a hard requirement (Cluster 6), which only succeeds if [CLIENT] staff have capacity to absorb it — not guaranteed during a live migration.

**Group 3 — An Assessment phase resolves uncertainty before commitment**
- A six-week Assessment produces a validated infrastructure baseline, a dependency map, and a risk-adjusted migration path.
- The output directly scopes Options A/B/C (full/reduced/minimal), letting [CLIENT] pick commercial commitment after seeing evidence.
- Precedent from comparable engagements ([REFERENCE-A], [REFERENCE-B]) shows Assessment-first reduces total cost of change by removing late-stage re-scope risk.

### Action titles derived from groups

1. "Unquantified technical risk makes a direct migration to sovereign Kubernetes unsafe without a dependency audit." (Group 1 claim)
2. "[CLIENT]'s current team capacity means external delivery governance must be designed before build scope is committed." (Group 2 claim)
3. "A six-week Assessment resolves the key uncertainties and lets [CLIENT] choose commercial commitment with evidence." (Group 3 claim)

Reading titles 1-2-3 top-to-bottom: risk is real and unquantified → internal capacity is constrained → therefore: Assessment first. The governing thought follows naturally.
