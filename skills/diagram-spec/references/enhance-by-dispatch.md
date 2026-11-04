# Enhancing a diagram by dispatch

## The premise

**A sketch or example list the user supplies is a floor, not a spec.** When someone says "something
like this", they are pointing at a direction with the two or three elements that came to mind — not
enumerating what the diagram needs. Building exactly what they drew produces a thin diagram and a
disappointed reader.

The author's own framing, twice: *"I only gave you a nudge with my examples, but there might be more
to it, so get creative and enhance the diagram"* — and, on method: *"start sub-agents to do the tasks,
be the orchestrator; we need fresh context in sub-agents to remove the biases."*

Fresh context is the point. An agent that has already seen the current version will defend it.

---

## The pair

Dispatch two agents **in parallel**, on fresh context. Shared dispatch doctrine is in
`asset-forge/references/dispatch.md`; these are the two roles.

### The designer

Bound by the constraints, returns a layout.

Brief it with: the **abstraction register** (capability or concrete — see `semantic-invariants.md`),
the **containment map** if boundaries exist, the altitude ("this is exec-facing; it carries the claim,
not the mechanism catalogue"), the corpus to ground itself in, and the output contract — boxes, arrows,
frames, and a proposed layout, as data rather than as SVG.

### The completeness critic

Told what the **minimal** version shows, and asked what is missing.

The brief that worked: *"A minimal version of this diagram would show only X and Y. That is too thin.
Enumerate everything the subject genuinely relies on, and for each item return a verdict —
**must-show / nice-to-have / omit** — with a one-line why."*

The verdict field is what makes it usable. A critic that returns a flat list of twenty candidate
elements has moved the problem rather than solved it; a critic that ranks them lets you take the top
tier and defend the cut. In practice this pair surfaced the governance elements the user had not named
and would have missed.

---

## Synthesis

You are the orchestrator, not a merge function:

1. Take the designer's layout as the base.
2. Walk the critic's must-show items; add the ones that survive the altitude constraint.
3. **State which additions you accepted and which you deliberately dropped to protect altitude** — the
   dropped list is as informative as the kept one, and it is what stops the next round re-proposing
   them.
4. Take the ASCII sketch to the user for approval before writing SVG (see the align-before-rewrite
   checkpoint in `asset-forge/references/phases.md` — visual structure counts).

---

## Grounding in the corpus

When the diagram belongs to a multi-artifact system, it is a **continuity surface**: the same entities
appear in the assessment, the sibling artifacts, and the prose around it.

Before drawing, sweep the underlying corpus with parallel read-only agents that **return conclusions,
not file dumps**, and extract three things per element:

- the **canonical name** (from the terminology ledger),
- its **honest maturity** (from the evidence-continuity map — what it actually is today),
- any **load-bearing count**.

Persist that as the state file's evidence-continuity map if it is not already there. It is what stops
a later polish pass from silently upgrading a spike into a capability, and it keeps sibling artifacts
telling the same story.

And remember the register rule: grounding a diagram in the research means it is **accurate**, not that
it names the products you found there.
