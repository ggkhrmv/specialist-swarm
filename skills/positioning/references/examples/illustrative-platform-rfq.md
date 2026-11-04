# Example: Sovereign Kubernetes Managed-Platform Bid (illustrative)

**This is an example, not a template.** The plays used here fit the specific situation described. A different sovereign platform bid with different competitive dynamics, different client maturity, or a different commercial context would make different choices.

**The case is fictional.** The numbers, names, and references are invented to keep the example concrete; they describe no real client or tender. Use it to see how the plays work together in one scenario. `[CLIENT]` is the placeholder for the customer, `[FIRM]` for the bidder, and `[REFERENCE-A]` / `[REFERENCE-B]` for named reference engagements.

---

## Situation

[CLIENT] runs 26 Kubernetes clusters across two cloud providers (GKE and AKS), supporting business-critical applications under a 24/7 SLA. The current estate works operationally. A regulatory review flagged that the control plane dependency on two hyperscalers fails [CLIENT]'s data sovereignty requirements, and the remediation window is 24 months. [CLIENT] issued an RfQ with 62 requirements across 7 clusters. We are a late entrant, invited after the first shortlist, so the response has to earn attention quickly.

---

## Intake reading

Key facts from the brief that drive play selection:

- Sovereignty is a hard requirement, not a preference. Control plane must stay on [CLIENT] infrastructure.
- 100% open-source. No proprietary forks or license traps.
- Very few internal FTEs. Limited experience with large external partners.
- KubeVirt consolidation of ~400 legacy Linux VMs is a stated strategic goal with no validated path.
- RfQ mixes abstraction layers (VMware, OpenStack, and bare metal listed as potential targets — contradictory with sovereignty goals).
- We are a late entrant — the proposal must be compelling and honest about boundaries.
- Operations can be staffed globally; 24/7 SLA is required.
- AI readiness (natural language operations, MCP-based platform admin) must be addressed.

**Play selection rationale:**

The situation calls for defensive plays first — the scope is genuinely uncertain and the RfQ has immature requirements. Offensive plays follow, because there is a real win-theme around sovereignty and open-source expertise that the hyperscaler incumbents cannot match.

Phased-entry is appropriate here: there is a realistic build/run runway if the assessment validates the path. The primary commercial target is the Assessment phase; build/run are shown as outlook only.

---

## Win-theme candidates

Four themes fit this situation. Confirm against [CLIENT]'s stated priorities before finalizing.

**1. Control-plane sovereignty on [CLIENT]'s own infrastructure**
The hyperscaler incumbents can offer managed Kubernetes, but not with a control plane on [CLIENT]'s own infrastructure without architectural compromises. [FIRM] delivers sovereign Kubernetes with the control plane under [CLIENT]'s governance from day one. Evidence: named references from comparable on-premises sovereign programs.

**2. No proprietary forks, with full operational SLA accountability**
We operate fully on open-source components (no proprietary forks) and take managed-service accountability for uptime. This combination — open-source stack plus operational SLA — is the specific gap the RfQ is trying to fill. Evidence: platform programs where open-source stack compliance was a contractual requirement.

**3. Assessment-first means [CLIENT] commits with evidence, not optimism**
We propose an Assessment phase that produces a validated inventory, dependency map, and risk-adjusted options before any build or run commitment. [CLIENT] sees the real picture before signing for delivery scope. This matters because the RfQ has immature requirements (the VMware/OpenStack/bare-metal ambiguity, the unvalidated KubeVirt path) that need resolution before anyone can credibly commit.

**4. Managed operations that scale without FTE growth**
[CLIENT]'s team is small and inexperienced with large external partners. Our on-/near-/offshore delivery model provides 24/7 coverage without requiring [CLIENT] to hire for it. Knowledge transfer is built into the program so [CLIENT]'s team grows capability over the engagement, not after it.

---

## Tiered scope options

Three options structured to avoid a binary yes/no.

**Option A — Full scope**
Assessment + Build + Run. Includes 24/7 managed operations, KubeVirt consolidation of the legacy VM estate, full knowledge transfer program, and AI readiness layer (MCP-based platform administration). 20-month program. Addresses all 62 RfQ requirements.

**Option B — Focused scope**
Assessment + Build + supported handover to [CLIENT]-led operations. KubeVirt consolidation scoped separately as a Phase 2 decision after Assessment output. AI readiness included as a roadmap deliverable, not a built feature. 12-14 month engagement. Addresses all MUST requirements; SHOULD coverage at ~85%.

**Option C — Assessment only**
Six-week Assessment. Deliverables: validated infrastructure baseline, full dependency map for GKE/AKS migration, risk register, and a priced recommendation for Options A and B. [CLIENT] takes the output to market or executes internally. No build or run commitment. Addresses no MUST requirements directly (Assessment is a precondition, not a delivery).

---

## Explicit assumptions

The RfQ contains ambiguities that must be surfaced rather than absorbed silently.

1. **Infrastructure target:** The RfQ lists VMware, OpenStack, and bare metal as potential underlying infrastructure, but these operate at different abstraction layers and cannot all apply. Assumption: [CLIENT]'s current VMware estate is the migration baseline. If OpenStack or bare metal is in scope, the migration toolchain and dependency map change materially.

2. **KubeVirt consolidation:** Treated as aspirational in Options A and B. Assumption: [CLIENT] has not validated whether the legacy VM workloads are KubeVirt-compatible. The Assessment will test this; consolidation scope may contract.

3. **24/7 SLA continuity:** Assumption: [CLIENT]'s A-applications (24/7 SLA) remain on the existing GKE/AKS estate during migration. Blue/green migration approach; no planned downtime for A-applications.

4. **AI readiness (MCP):** Assumption: natural language platform operations are a readiness requirement, not a current capability. Treated as a roadmap deliverable in Option B, a delivered feature in Option A.

---

## Honest scope boundaries

[FIRM]'s scope in all three options covers the Kubernetes control plane, platform tooling, managed operations (Options A/B), and knowledge transfer. It does not cover:

- Application development or workload migration for individual applications. [CLIENT]'s application teams own workload migration, supported by runbooks.
- Underlying physical infrastructure provisioning. [CLIENT] is responsible for compute, storage, and networking capacity meeting the specifications [FIRM] defines in the Assessment.
- Legacy VM platform management outside the KubeVirt consolidation scope. The ~400 legacy VMs remain under [CLIENT]'s current management until consolidated under Option A.

---

## Discriminators

Against the two likely incumbents:

**Incumbent A (hyperscaler managed Kubernetes):** Strong on cloud-native workloads and developer experience. Cannot offer control-plane sovereignty without structural changes to their managed service that they have not offered. Their strength — global managed infrastructure — is precisely what [CLIENT]'s sovereignty requirement rules out.

**Incumbent B (systems integrator, generalist delivery):** Can staff a large program but has no documented sovereign Kubernetes references at comparable scale. Likely to propose a longer engagement with higher FTE counts. Their commercial model may not fit [CLIENT]'s preference for lean governance.

[FIRM]'s position: the only bidder with documented sovereign, open-source Kubernetes delivery at comparable scale, proposing an Assessment-first model that reduces [CLIENT]'s commitment risk.

---

## Claims register (starter)

| claim | verified/aspirational | source |
|---|---|---|
| [FIRM] delivers sovereign Kubernetes with on-premises control plane | verified | [REFERENCE-A] — on-premises platform engagement for a European logistics group (see references section) |
| Open-source stack with no proprietary forks | verified | [REFERENCE-B] — platform program for a regional public-sector IT provider |
| Assessment-first reduces re-scope risk | verified | [REFERENCE-A], [REFERENCE-B] — assessment phase identified late-stage risks before build |
| MCP-based platform administration (AI readiness) | aspirational | [FIRM]'s AI platform team — capability built, no Kubernetes-specific client reference yet |
| 24/7 SLA coverage via on-/near-/offshore staffing | verified | Multiple managed services references |
| KubeVirt consolidation of legacy VMs | aspirational | KubeVirt is open-source and in production use; [CLIENT]-specific consolidation path not yet validated |
