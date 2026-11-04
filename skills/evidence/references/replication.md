# Replication — before you compare to a prior baseline

## The rule

Before comparing fresh numbers to any prior baseline, **re-run your method over that baseline's own
window** and report where it replicates and where it does not.

Replication licenses the comparison. Non-replication is a finding about **your instrument**, not a
number to quietly ship.

## Why it is worth the cost

This was the single decision that made every subsequent comparison in one engagement defensible. The
replication check reported: volume shares replicated (81% → 79.2%) but the work-type mix did **not**
(84% → 47%).

That failure was the useful part. It proved the cheap keyword rule was inadequate and justified the
expensive classification pass — which then replicated at 87% against 84%. Without the check, the cheap
rule's numbers would have been compared to the baseline directly and the divergence would have been
reported as a real change in the world.

## Running it

1. Take the prior baseline's window, definitions, and population as given.
2. Run your **current** method over that window.
3. Compare per metric, not in aggregate. Report each as replicated / diverged, with the two figures.
4. For each divergence, establish the cause before doing anything else.

## Diagnosing a divergence

Check these in order:

- **Definitional difference.** The most common cause, and the least interesting: the prior baseline
  counted something slightly different. State the definitional difference in the artifact instead of
  asserting a change.
- **Population difference.** Different filter, different source, different truncation (see
  `window-discipline.md`).
- **Method inadequacy.** Your instrument is weaker than the original's. This is the case that costs
  money, and the case where a cheap method has to be replaced.
- **A real change.** Only conclude this once the three above are ruled out.

## Do not smooth it over

A divergence you cannot explain goes in the artifact as a stated limitation, not into a footnote and
not averaged away. And where two measurements used **different counting methods**, they are not a trend
at all: keep the original figure with its date and source ("as of the [month] baseline"), and log the
re-measurement as a separate item.

## Report

State the baseline's window and definitions, the per-metric replication result with both figures, the
diagnosed cause of each divergence, and what the replication licensed you to compare.
