---
name: evidence
description: Use when a claim an asset needs must be measured from a client's or organisation's own systems — ticket trackers, code repositories, config, logs, chat exports — rather than cited from an external source. Triggers include sizing a problem from real data, building a classified corpus, validating a proxy metric, refreshing figures against a prior baseline, comparing a period before and after an intervention, reconciling a reviewer's conflicting number, or dispatching analysis subagents over a corpus. Also use when a figure already reported turns out to be wrong, or when the data appears unable to answer the question asked.
---

# evidence

## What this skill is

The measurement discipline for numbers you produce yourself. It covers the machinery: validating a
proxy before you spend on it, propagating error through chained steps, choosing windows, replicating a
prior baseline, and briefing the agents who do the extraction.

It is the counterpart to two other skills, and the split matters:

| Concern | Skill |
|---|---|
| Is this number *publishable* — coverage, controls, provenance, honesty | `positioning` → `references/evidence-from-client-data.md` |
| Is this number *right* — method, error, windows, replication | **this skill** |
| Does the asset's arithmetic hold together on the page | `asset-review` → `references/number-check.md` |

Read the `positioning` file alongside this one. This skill gets the number right; that one decides
whether it belongs in the asset.

## Why it exists

The most expensive errors in practice were not writing errors. They were measurement errors made
before any copy existed, and they were only caught by the user or by a review board much later:

- A constraint recorded as fact — "nothing in the corpus measures effort" — was **false**. Over half
  the items carried a worklog. The assumption had capped the asset for days and blocked a reviewer's
  top ask.
- A window filter silently truncated the population, making **three already-reported figures wrong**.
- A period average spanning an intervention hid a reversal; splitting it moved one indicator from
  21.6% to 30.9%.
- A chained metric reported ~2,840 events where the truth was ~360 — an 8× overstatement, with only
  13% of what it reported being real.

None of these were visible in the output. All were visible in the method.

## The core discipline

**A recorded constraint is an assumption until someone tested it.** "The data cannot show X" gets
logged with who tested it, how, and when — see the constraint register in the state file. Any
constraint that blocks a headline claim or a reviewer's top ask is **re-tested before it is accepted a
second time**. When it falls, sweep the asset *and* the state file for prose that rested on it.

**A subagent's report is a finding, not a fact.** Recompute the one or two numbers the conclusion rests
on, yourself, from the raw data, before relaying anything to the user.

**Prove the recipe before spending agents on it.** Verify the extraction method end to end yourself,
then hand the proven method to the agents so they do not spend their context rediscovering it.

## Workflow

Not every step applies to every question. Run the ones that do, in this order.

1. **State the question and the decision it funds.** If you cannot name the decision, stop — see
   `positioning`'s "what decision does this fund?".
2. **Test the constraints.** List what you believe the data cannot show, and test each belief before
   building on it.
3. **Establish coverage.** Enumerate the real population, then measure what fraction your corpus
   covers. Report it with every rate.
4. **Validate the method on an answer key** before the expensive run, with a stated GO/NO-GO.
   See [references/answer-keys.md](references/answer-keys.md).
5. **Choose the window deliberately.** Split at any intervention; check for truncation.
   See [references/window-discipline.md](references/window-discipline.md).
6. **Run the extraction**, dispatching agents where the volume needs it.
   See [references/analysis-dispatch.md](references/analysis-dispatch.md).
7. **Propagate the error** to the number you intend to publish.
   See [references/error-propagation.md](references/error-propagation.md).
8. **Replicate any prior baseline** before comparing to it.
   See [references/replication.md](references/replication.md).
9. **Hand to `positioning`** for the publishability checks (controls, robustness triad, provenance).

## Reference files

- [references/answer-keys.md](references/answer-keys.md) — building an independent answer key, the GO/NO-GO gate, leakage audits, blinded re-runs
- [references/window-discipline.md](references/window-discipline.md) — PRE/POST splits at an intervention, truncation traps, scope expansion
- [references/error-propagation.md](references/error-propagation.md) — judging a chained metric on its output; overstatement factor and share-real
- [references/replication.md](references/replication.md) — re-running your method over a prior baseline's own window; definitional divergence
- [references/analysis-dispatch.md](references/analysis-dispatch.md) — the analysis-agent brief and output contracts; extends `asset-forge/references/dispatch.md`

## Reporting a wrong figure

Once a figure has been reported to the user, changing it is a **correction, not an edit**. State it
plainly with old and new values side by side, carry a visible correction note in the artifact, and
append it to the state file's decision log **with the reason it was wrong** — so a later session cannot
reintroduce it.

Every headline figure carries its source, its date, and whether it is exact or approximate. When you
refresh the number, refresh that label too.

## Conventions

Always use `[CLIENT]` as the placeholder for the customer name — never write the real name. Anonymise
individuals to role: a person's name must never carry a negative finding.
