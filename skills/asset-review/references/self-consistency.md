# Self-consistency — the asset against its own evidence

## Why this is its own pass

Spotting a contradiction is not the hard part. A fresh reader with the whole asset in front of them
finds these readily. The failure is **when** they get found: without a named step, contradictions
surface at the post-build review board, after the copy has been written, polished, and voice-matched.
By then the fix is a re-cut, not an edit.

So this pass runs **during Build and after every rework increment**, not only at Review. It is cheap:
it needs no personas and no render.

The asymmetry that makes it matter: a skeptic needs **one click** to use your own evidence table
against your own headline. Anything the asset itself contradicts is the cheapest possible attack.

## When it applies

Any asset that carries both:

- a **persuasive layer** — hero, section titles, callouts, stat labels, the close, diagram labels; and
- an **honest layer** — a maturity or capability map, a basis/status column, a graded heatmap, a
  caveats or limitations section, a "what we did not measure" note.

The more honest the second layer, the more exposed the first one is. Assets with no self-assessment
are not safer — they just fail a different check (see `claims-check.md`).

## The pass

Read the persuasive layer **as a list of assertions**, ignoring the prose around them. For each
assertion, find where the asset's own evidence layer speaks to it and compare.

Anything the asset's own evidence contradicts is **P0**, not P1. This is a deliberate priority
override: a claim that another *document* contradicts is a fact-check problem, but a claim the *same
document* contradicts is a self-inflicted wound, and it discredits every adjacent correct claim.

### Two shapes that recur

**The absolute qualified elsewhere.** An unhedged claim — "the risk is retired", "safe by
construction", "every crossing is gated", "nothing merges without review" — that the honest layer
qualifies or the maturity grade contradicts.

Fix by **splitting the claim along the same axis the evidence splits**. Do not simply soften it into
mush; find the part that is genuinely true and say that part strongly:

> Before: "Every hard mechanism is de-risked. The risk is retired."
> After: "The delivery mechanisms are proven. The safety boundaries are designed, not built — that is
> what the first phase funds."

The second version is more confident *and* more honest, because it names something real.

**Present tense on something unbuilt.** A capability graded 0–2, or with a basis of "to build" /
"designed" / "proven once", written in the present indicative — or called "non-negotiable from day
one" while scheduled for the last phase.

Fix by moving to design-intent or destination voice ("designed to be gated", "by design nothing
merges…", "proven once in a spike, not yet in operation"), not by deleting the claim. The vision
stays confident; the current-state claims get honest.

### Two checks the obvious read misses

**Exec-view reconciliation.** In a two-view asset, a tension between two claims **both visible in
the default view** must be reconciled **in that view**. A reconciliation that lives only in the
architect or deep layer does not exist for the default reader — and unreconciled, the tension reads
as spin rather than as nuance. Check: for each contradiction you resolve with an explanatory
sentence, confirm that sentence renders in the same view as both claims it reconciles.

**Promotion check.** The asset's most credible sentence is usually a concession or a boundary — and
concessions drift into the technical view, where the decision-maker never reaches them. After the
pass, ask: what is the most disarming line in this asset, and which view is it in? If it is only in
the low view, promote it. The exec view carries the claim **and** the strongest concession behind it;
the technical view carries the mechanism.

This inverts the usual instinct. A refusal to claim a flattering number, or an openly stated limit,
buys more credibility with a senior reader than another supporting figure does — and it is the thing
a polish pass is most likely to quietly remove.

## Reporting

Report as a table so the author can see the axis at a glance:

| Persuasive claim | Where | The asset's own evidence | Where | Fix |
|---|---|---|---|---|

Close with the two checks stated explicitly: which reconciliations you confirmed are in-view, and
what you promoted (or that you found nothing worth promoting).

## What this pass does not do

It does not check claims against the outside world — that is `claims-check.md` (provenance and
technical soundness). It does not check arithmetic — that is `number-check.md`. This pass compares
the asset only against **itself**, which is why it can run without any external source.
