# Compliance / Traceability Matrix

The compliance matrix is the artifact that proves every requirement in the source RfQ is addressed somewhere in the response. It functions as a traceability map: evaluators use it to check coverage; the `asset-review` skill uses it at the Review gate to sign off completeness.

---

## Schema

| requirement ID | MUST/SHOULD | covered? | where in asset | notes |
|---|---|---|---|---|
| `4.2.1.3` | MUST | yes | Section 4 — Security, para 2 | Zero-trust network policy via Cilium |
| `5.4.2` | MUST | partial | Section 5 — Operations, para 4 | 24/7 SLA coverage confirmed; incident response SLA pending commercial sign-off |
| `6.1.3` | SHOULD | yes | Section 6 — Transition, para 1 | Knowledge transfer plan; runbook delivery in final milestone |
| `7.2.1` | MUST | no | — | Out of scope per Option B; covered in Option A |

**Columns:**
- `requirement ID`: exact ID from the source document, no changes
- `MUST/SHOULD`: from the source document
- `covered?`: yes / partial / no — be honest; a "partial" that is acknowledged is better than a "yes" that the evaluator disputes
- `where in asset`: section name, subsection, or paragraph reference — specific enough that the evaluator can find it without searching
- `notes`: anything that qualifies the coverage — conditions, scope option dependency, assumptions, items flagged as aspirational in the claims register

---

## Lifecycle

The matrix is opened at intake, when requirements are first extracted. It is maintained continuously as the response is written — do not treat it as a deliverable to produce at the end. A matrix built after the fact frequently discovers late-stage coverage gaps.

At the Review gate, `asset-review` checks:
1. Every MUST requirement has `covered?` = yes or has an explicit explanation in `notes` for why it is out of scope (with the scope option clearly stated).
2. No `where in asset` entry points to a section that does not exist in the current draft.
3. No row has `covered?` = yes while the claims register marks the supporting claim as aspirational without a plan to verify it before submission.

---

## Cautionary example

A proposal for a nine-cluster platform program had an executive summary that opened with: "Our solution addresses all nine requirement clusters." The compliance matrix attached at the back of the document had eight rows — Cluster 6 (Observability) was missing entirely. The evaluator noticed during scoring, not during internal review. The discrepancy was explained in a clarification round, but it raised questions about the team's attention to detail that followed the bid through the evaluation.

What went wrong: the matrix was built from a working draft of the proposal that had been restructured; Cluster 6 was merged into Cluster 5 during a revision, but neither the matrix nor the executive summary was updated. The matrix and the response structure fell out of sync.

The fix is simple: every time a section is restructured, updated, or removed, update the `where in asset` column in the matrix before moving on.

---

## Sign-off

At the Review gate, `asset-review` records a sign-off line at the bottom of the matrix:

```
Review gate: [date] — all MUSTs covered or explicitly scoped out; matrix current against [response document version]; aspirational claims reviewed in claims register.
```

If any MUST is uncovered without explanation, the matrix is not signed off and the asset does not pass the Review gate.
