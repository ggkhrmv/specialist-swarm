# The investment case — quantifying the ask

## Why this is its own reference

Across a full engagement with three review rounds, this was the dominant finding in **every round**,
raised independently by the economic buyer, the exec/MD, and the red team — and it was still open at
the end. It is the most reliably-missed thing in an asset that asks for something.

The pattern is always the same: the problem gets measured exhaustively and the return gets described
in adjectives. Reviewers say it bluntly.

> "No euro figure, no FTE count, no duration anywhere in the doc. 'Bounded' is never bounded. I
> cannot approve a budget line with no number."

> "The asset spends its entire evidentiary budget quantifying the problem and spends nothing
> quantifying the solution."

> "A section titled 'what we are asking to fund' that never states a cost. Silence reads as evasion;
> an explicit deferral does not."

**A measured problem with an adjectival return is a named defect.** Treat it as one.

## The three numbers

Any asset that asks for a decision, funding, or endorsement carries three numbers **in the default
reader view**, expressed in the unit the approver actually controls (usually headcount and time, not
abstract value):

**1. The ask — bounded.** People × duration, or money × duration. At least two of {people, money,
duration}. Later phases may be explicitly deferred, but the *first* phase is always bounded. "A
bounded first phase" without numbers is not bounded; it is a word.

**2. The status-quo baseline — the cost of doing nothing, in the same unit.** This is the one most
often missing, and it is what makes the ask land. An ask presented naked invites "that is a lot of
money". An ask netted against a measured cost invites a comparison. If you have measured the problem
at all, you can express it in the approver's unit — if the problem costs nine engineers' capacity
today, say so, and the ask for four is a different conversation.

**3. At least one target outcome, tied to a figure you already measured.** The honesty rule forbids
presenting a hoped-for delta as if it were measured. It does **not** forbid a clearly labelled
target. Label it `TARGET`, tie it to the same metric the problem was measured in, and say where the
baseline will be set if you do not have one yet — "a target of absorbing 40% of the measured toil,
baselined at the first gate."

A target that is only a hypothesis is still a target. An adjective is not.

## Falsifiable gates

Every phase transition states what "pass" means and what a no-go triggers. **A gate that cannot fail
is not a gate** — "a feasibility check" is undefined, so the review cannot fail, so the gate provides
no risk control and a reviewer will say so.

Write each gate as: the criterion, the threshold, and the consequence of missing it. Include what
would make you *stop*, not only what would let you continue. A stated stop condition is the single
cheapest credibility purchase in the whole asset.

## When a number is genuinely not yours to give

Say so on the page. Silence on cost reads as evasion; an explicit deferral does not.

> "Rates are set by [the commercial function]; this section states effort in engineer-quarters and
> the rate card is applied separately."

That sentence costs nothing and closes the objection. What it must not be is a bracketed placeholder
left in live copy — see the placeholder rule in `asset-forge/references/build-validation.md`. And
prepare the **off-page answer**: if the audience will ask anyway, have the band ready verbally even
when it stays off the page.

## The correspondence check

Cross the asset's own three lists against each other: **the diagnosis** · **the dependencies and
mechanisms you called critical** · **the resourcing and schedule**.

- Every problem you diagnosed has a line item that addresses it.
- Every dependency you called binding has a track, an owner, and a slot.
- Every mechanism you claim makes the plan work — pairing, enablement, review, adoption — has
  capacity actually assigned to it.

This is where assets supply their own ammunition. Real examples, each a top-three pick by the
sharpest reviewer on the board:

- "You diagnosed an adoption failure and budgeted no adopters." The problem section said a working
  self-service platform went unadopted; the next gate required adoption by two teams; no role in the
  plan carried it.
- A dependency the asset called "the dependency", which the following phase gated on, was **not among
  the funded tracks** — while an item the asset explicitly allowed to fail had one.
- Six engineers, one per track, means nobody pairs with anybody — while pairing was the named
  mechanism for retaining the capability.

An item named critical and left unfunded, or funded behind something you said could fail, is the
first thing a skeptic finds. Run this check before the review board does.

## Reporting

State the three numbers, the gate criteria, and the correspondence result as a short block the author
can check at a glance. If any of the three numbers is absent, say which and why — do not let it pass
silently into a review, where it will consume the top finding of every persona on the board.
