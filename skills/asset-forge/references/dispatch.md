# Dispatching subagents — the shared method

This is the common doctrine for every fan-out in the suite: review personas (`asset-review`),
evidence and analysis work (`evidence`), diagram enhancement (`diagram-spec`), and research sweeps
during Intake. Skill-specific detail stays in the calling skill; what is here applies to all of them.

Use `superpowers:dispatching-parallel-agents` for the mechanics. This file covers what to put in the
brief, how to pick the model, and how to treat what comes back.

## Model routing

Do not send every task to the strongest model, and do not send every task to the cheapest. Route by
the *kind of thinking* the task needs. Use tier names rather than model ids so this survives model
releases, and pin the tier explicitly on each dispatch rather than inheriting silently.

| Work type | Tier | Why |
|---|---|---|
| Adversarial review, red-teaming, judging, refuting a claim | **Strong**, high effort | Rewards reasoning depth; under-powering it produces agreeable output that misses the real objection |
| Design and synthesis — layout proposals, storyline options, estimation models | **Strong**, medium–high | Genuine judgement with many valid answers |
| Grading and scoring against a rubric | **Strong**, medium | The rubric constrains the answer, but the evidence call is judgement |
| Reading a corpus and returning conclusions | **Mid** | Comprehension, not invention |
| Mechanical sweeps — greps, extraction, file collection, counting, reformatting | **Cheap/fast**, low effort | Deterministic work; a strong model adds cost and nothing else |
| Classification against a fixed codebook at scale | **Cheap/fast**, pinned | Volume matters more than depth — but pin **one** tier across the whole fan-out so outputs stay comparable |

Three rules on top:

- **If cost is a constraint, cut the agent *count*, not the per-agent capability.** Four
  well-powered reviewers beat eight weak ones.
- **Pin one tier across a fan-out** whose outputs will be compared or aggregated. Mixed tiers make
  the variance uninterpretable.
- **Tell the user what you pinned**, so they can override.

A calling skill may override this table where it has a specific reason — `asset-review` pins its
analytical personas high regardless of budget, for example. State the override and why.

## The brief

A brief is a contract, not a topic. Seven blocks; include the ones that apply.

**1. The single job, and explicit non-goals.** One job per agent. Name what a parallel agent owns so
two agents do not both do it — "your only job is X; a separate agent is building Y, do not classify".

**2. The proven method.** Verify the method yourself first, then hand it over. An agent that has to
rediscover how to reach the data spends its context on discovery instead of the task.

**3. Read-first / do-not-redo.** The artifacts already produced and the specific facts already
established. Include *why the previous attempt failed*, with the file to read, so it is not repeated.

**4. Navigation contract.** How to reach every layer of the artifact: toggle selectors, hidden-block
class names, which view is default, and any wrapper that must be stripped (an embedded base64 font
block will otherwise consume the agent's context before it reaches the content). **An agent that
reads only the default view reviews half the asset and reports false gaps.**

**5. Stipulations and locked rulings.** What is settled and out of bounds — the decisions already
made, the critiques that do not apply to this asset. Without this, a board spends its budget
re-arguing settled ground, and the same finding returns every cycle.

**6. What changed in this revision.** For any re-review. Weigh it hardest; read everything for
consistency. Omit this and the agent reviews the version it remembers.

**7. The output contract.** What it must return, and what the decision its result gates is. For a
large fan-out: an exact item list, one record per item, and at least one field verifiable against the
source (a verbatim quote). Plus **explicit permission to return a negative** — "do not round in our
favour; a negative is an acceptable result." Agents given this move a grade *down* as readily as up,
which is the point.

Add a **read-only clause** where the agent must not write: "find problems, propose fixes, apply
nothing." Name protected files explicitly.

## Concurrency

**Pilot one, then fan out in waves of about six.** Validate the pilot's output before committing the
rest.

A fan-out at the platform's concurrency maximum does not queue gracefully. In practice, launching 20
at once produced 10 that worked and 10 that froze at their first tool call and held their slots for
~40 minutes without writing anything. Relaunched in waves of six, every wave landed in about five
minutes.

Detect a stall by comparing elapsed time against the observed duration of agents that *did* finish —
not by waiting longer. A stalled agent holds its slot until you stop it explicitly.

## Handling what comes back

**Hold the whole board.** Do not edit, or announce conclusions, on a partial return. Acknowledge each
arrival and wait. While they work, run the deterministic checks yourself so they merge alongside the
agent findings.

**A subagent's report is a finding, not a fact.** Never publish a subagent's headline figure
unverified: recompute the one or two numbers the conclusion rests on, from the raw data, yourself.
State that you did, and report any divergence — including divergence that does not change the
conclusion.

**Verify before applying.** An agent reads a flattened extract, not the rendered artifact.
Inline-styled fragments, chips, and view-toggled blocks read as garbled in an extract while rendering
correctly. Re-derive numeric findings; check "garbled / duplicated / missing" claims against the
markup.

**Check against the decision log.** A finding that contradicts a logged, dated decision is a conflict
to surface, not an entry to apply — an agent working from a ground-truth file that predates a decision
will confidently report the current, correct value as an error.

**A zero-tool-use return is a spurious stop, not a verdict.** Re-dispatch it. Require **self-proving
output** — have the agent list what it actually found (the titles, the section order, the file paths)
so a plan-instead-of-findings return is obvious at a glance. And a slow agent is not a dead one: note
the absence, do not conclude without it.

**Validate against what the agent actually read**, not your upstream original. Your own preprocessing
will otherwise produce false failures. Repair individual defects surgically rather than re-running a
whole batch. A uniform or degenerate return is a data signal until you have inspected that slice.

**Merge by convergence.** Rank findings by how many agents raised each independently, and state the
count. Distinct frames are the point of a fan-out — do not average agents into a consensus before
merging.

## Testing a proposed method

When a reviewer or an agent proposes a method — a measurement, a sizing approach, a structural cut —
implement and test **their** specification end to end, including every safeguard step they included,
before judging it. A verdict on a simplified variant is not a verdict on their method. If you must
simplify, say which step you dropped and that the result is therefore not about their design.
