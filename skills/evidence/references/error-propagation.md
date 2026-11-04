# Error propagation — judge the output, not the components

## The rule

A metric assembled from chained steps is judged on **the number you intend to publish**, not on the
accuracy of its parts. Propagate each step's measured error through to the headline, and state two
things: the **overstatement factor** and the **share of the reported number that is real**.

"Step 2 is 71.4% accurate" is not publishable. "The headline overstates by 2.5×, and 24% of it is real"
is a decision.

## Why component accuracy misleads

Steps compose multiplicatively, and a step that looks respectable in isolation can destroy the output.
Two worked cases from the same engagement:

- A three-step pipeline whose components each looked usable would have reported ~2,840 events. The
  truth was ~360. **It overstated by ~8×, and only 13% of what it reported was real.**
- A later variant reported 912 against a true 365 — **2.5× overstatement, with step-2 error accounting
  for three-quarters of the excess.**

Neither was visible from the per-step figures. Both were obvious once propagated.

## How to do it

For each step, measure its error on the answer key (see `answer-keys.md`) — precision and recall
separately, because they propagate differently. Then compute forward:

- **Recall** compounds: each step can only find what the previous step passed through.
- **Precision** compounds the other way: each step's false positives pass downstream and get multiplied
  by the next step's expansion factor.

Report as a table so the collapse is visible:

| Step | Recall | Precision | Items passed | True items | Share real |
|---|---|---|---|---|---|

End with the two headline numbers: overstatement factor, and share-real.

## The publish decision

Set the threshold before you compute. A useful default: if the overstatement factor exceeds ~1.5× or
share-real falls below ~70%, the number is not a headline. It may still be a caveated directional
statement, or it may be nothing.

When the chain does not survive, do not reach for a weaker proxy — reach for
`positioning`'s measurement-gap-as-finding. Publishing the gap is stronger than publishing a number
that overstates by 8×, and it cannot be broken by a reviewer who recomputes it.

## Report

State each step's measured error and its source, the propagated output, the overstatement factor, the
share-real, the threshold you set in advance, and the publish/no-publish call that followed from it.
