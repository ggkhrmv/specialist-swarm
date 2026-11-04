# Window discipline

## Split at the intervention

When a figure is meant to show whether something **changed**, never report a period average that spans
the change. Split at the intervention date and report PRE / POST.

A year-to-date figure averaging the pre-measure and post-measure periods together hid a reversal: split
properly, one indicator moved from 21.6% to 30.9%. The average was arithmetically correct and
substantively misleading, which is the worst combination — it survives a number check and fails a
reader.

Identify the intervention date explicitly and state it in the artifact. If measures were introduced
progressively rather than on a date, say which date you chose and why.

## Check for truncation

**Any "age of open items", backlog, or duration metric needs the unfiltered population**, because a
date-filtered corpus silently drops exactly the oldest cases the metric is about.

This one cost three already-reported figures. A year-to-date extraction omitted items created earlier,
so every age-based figure was wrong: backlog 238 → 296, over-90-days 104 → 167, another 172 → 351. The
query looked correct. The population was wrong.

Before trusting any window-filtered extraction, ask: **does the metric describe things that could have
started before the window opened?** If yes, the window cannot be applied to the population — only to
the events.

## Scope expansion

When you expand evidence scope mid-engagement:

1. **Test the inclusion condition before ingesting anything**, and report the test. If the user
   authorised the source conditionally ("only if X applies"), establish X first — in one case 12 of 29
   candidates qualified, which changed what the source could support.
2. **Take a defined slice, not the whole source.** Record on each record *why* it was included
   (`included_because`), so any inclusion can be audited later.
3. **Never silently merge a new source into figures already compared against a baseline.** Segregate
   it, state the scope rule in the artifact ("findings 1–11 remain single-source so they stay
   comparable to the earlier baseline"), and treat the overlap as a **replication check** rather than
   as additional volume.

Segregation pays twice: it protects the comparison, and the overlap becomes independent corroboration.
In one case the headline landed within 1.4 points across the two sources, which was worth more than
the extra records would have been.

## Report

State the window, the intervention date and the reason for it, whether the population or only the
events were filtered, and — for any expansion — the inclusion condition, the slice size against the
source total, and what stayed segregated.
