# Number check — arithmetic a reader can break

## Why

In review boards run over real assets, quantitative defects were repeatedly the single largest
finding class — in one board, six P0s raised by five of six personas, all arithmetic. None were
modelling errors. Every one was a **presentation** defect: the model was right and the page was
wrong, or the page was right and the reader could not see it.

The governing asymmetry: a reader who breaks one number stops trusting all of them. In an asset
whose credibility rests on "measured from our own data", one visible arithmetic slip taints every
other correct figure by association.

Run this over every figure the asset publishes, after every increment that touches a number.

## The five consistency checks

**1. Parts vs whole.** Any table column or list a reader will instinctively add must equal the stated
total. If it legitimately does not — different bases, overlapping periods, rounding — say why **on
the page**, in one line. A column summing to 14 beside a stated peak of 8 is read as an error, not as
a subtlety.

**2. Stated direction vs computed series.** Does "rises to", "doubles", "falls", "worsens" match the
actual numbers? Check the series, not the endpoints. "Rises to about half" over 44% / 51% / 50% is
flat, not rising. A direction misstated in your own favour costs more credibility than the claim is
worth.

**3. Double-counting.** Is any entity counted inside one figure and outside another? A role counted
both in a headline count and in the workstreams it supports leaves the plan short and the reader
suspicious.

**4. Same-basis ranges.** Does a sensitivity band, range, or error bar derive from the **same basis**
as the headline it qualifies? A band computed from one derivation, published as though it reconciled
two, is a false precision claim about method, not just about magnitude.

**5. Traceability.** Every published figure reproduces from the backing model or data — **run now**,
not from memory of an earlier version. If a figure cannot be reproduced, it is not publishable.

## Reader-reproducibility

A figure the reader cannot reproduce **on the page** is a defect even when it is correct. Four
additional checks:

- **Show the intermediate.** If the visible operands do not yield the stated result, show the step
  that does. `3140 − 2610 = 530`, not the stated 412 — because the right subtrahend was 2728, which
  never appears on the page. The number was right and unverifiable, which reads identically to wrong.
- **No unit ambiguity.** No phrase that reads as an absolute and means a proportion, or the reverse.
  "Within about a quarter" reads first as one engineer-quarter and meant 25%.
- **Name the aggregation method.** "We took the midpoint" — never a verb that hides it. "Reconciled"
  described a figure that was exactly `(48 + 70) / 2`; the honest word is stronger, because the
  euphemism invites the reader to look for what you are covering.
- **Precision matches the method.** Decimals on a modelled figure assert a measurement you do not
  have. Round them.

## Stat integrity

For every number in exec-visible copy — stat tiles, hero figures, callouts — verify four things:

- **Figure** against its named source.
- **Label** states exactly what was measured, not a stronger adjacent claim. "81% is firefighting"
  when the measurement was 81% *concentrated in two teams* is a different claim.
- **Arithmetic consistency with its own sublabel.** A true figure beside a true detail drawn from a
  different baseline reads as a mistake. "30× growth" over "15 → 360" invites the reader to divide and
  get 24. Show one, or reconcile them explicitly.
- **Scope qualifier present.** Whose items, which team, which window. "512 tickets, one requester"
  where the real figure was 287 of 512 is a scope failure, not a rounding one.

And: a stat's number must cover **exactly** the population its label names. A figure computed on one
subgroup under a label naming the whole group is a factual misstatement, and it is the kind an
evaluator checks first.

## Leave-one-out

Recompute every headline figure with its largest single contributor removed.

A big number drawn from one class reads as cherry-picked and invites the reader to discount it. Lead
with the **aggregate over everything you measured**, and demote the largest instance to "the easiest
place to see it". State the sensitivity in the text so the objection is answered before it is asked.

This check cuts both ways: in one case, removing the largest contributor *raised* the claim from
61.2% to 77.8% — the "biggest" instance had been the weakest one in the set and was dragging the
headline down.

## Problem-side honesty

The no-overclaim rule applies to the problem, not only to the solution.

Do not overstate a named team's dysfunction to strengthen the case. The person who owns that team is
usually in the room, and they will challenge it. State pressure and trend, attributed to the specific
queue where the evidence sits — "stable but exposed", not "collapsing".

And: **a different counting method is not a trend.** If a re-measurement used a different method than
the original, the two are not comparable. Keep the original figure with its date and source ("as of
the [month] baseline") and log the re-measurement as a separate item rather than blending them into a
direction of travel.

## Reporting

Report per figure, not per section:

| Figure | Where | Reproduces? | Checks failed | Fix |
|---|---|---|---|---|

Any failure is **P0**. State explicitly which figures you re-derived and from what.
