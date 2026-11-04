# Dispatching analysis agents

**The shared dispatch doctrine is in `asset-forge/references/dispatch.md`** — brief structure, model
routing, concurrency limits, stall detection, and how to treat returns. Read it first. This file adds
what is specific to evidence and analysis work.

## Prove the recipe first

Verify the extraction method end to end **yourself**, on one real case, before dispatching anyone. Then
hand the proven method over.

An agent that has to rediscover how to reach the data spends its context on discovery instead of the
task, and each agent rediscovers it independently. Confirming the chain first — identity resolution,
the API calls, the date filtering, the scoping — turned four dispatches into usable work on the first
attempt each time.

## The seven-block analysis brief

Beyond the shared brief structure, an analysis agent needs these named explicitly:

**1. PROVEN METHOD.** The calls or queries you verified, verbatim, with the gotchas you hit. Label it
as verified by you.

**2. Inputs already produced — READ THESE FIRST, do not redo.** The files, and the specific facts
already established in them.

**3. Why the previous attempt failed.** With the file to read. Otherwise it repeats the failure — this
is the block most often omitted and most expensive to omit.

**4. Your single job, and explicit non-goals.** Name what a parallel agent owns: "your only job is
identity resolution — a separate agent is building the classifier; do not classify."

**5. Protected files.** What it must not write to.

**6. The decision this result gates**, and the metric that decides it. An agent that knows the
threshold reports against the threshold.

**7. Permission to return a negative.** Verbatim: *"Do not round in our favour. A negative result is an
acceptable and useful outcome — report what the data says."*

That last block is not politeness. Agents given it move a finding **down** as readily as up: across
four dispatches on one engagement, three returned negatives, and all three were correct. An agent
without it optimises for having found something.

## Output contracts for volume work

For any fan-out over many items:

- An **exact item list**, and one record per item, in order.
- At least one field **verifiable against the source** — a verbatim quote is ideal, because it is
  machine-checkable.
- **Validate against the material the agent actually read**, not your upstream original. A validator
  that checks against the pre-processed source will fail correct quotes — this happened, and the fix
  was to validate against the batch text the agent was given.
- **Pin one model tier across the whole fan-out** so outputs are comparable.
- **Repair individual defects surgically.** Do not re-run a batch for a handful of bad records. One
  fan-out returned 2,380 of 2,380 records with 5 mechanical defects (0.21%), all repaired individually.
- **A uniform or degenerate return is a data signal until inspected.** One agent returning the same
  label 48 times out of 48 was reporting real data, not failing.

## On return

**Recompute the load-bearing numbers yourself.** Never publish a subagent's headline figure unverified:
re-derive the one or two numbers the conclusion rests on, from the raw data, and state that you did.
Report divergence even when it does not change the conclusion — one agent's odds ratio of 68
reproduced as ~52 under a continuity correction, same conclusion, and saying so is what makes the rest
credible.

And where an agent's verdict contradicts the approach you recommended, verify its key numbers before
relaying the verdict — in both directions. An agent once corrected the orchestrator's own figure, and
the correction was only confirmed by re-checking the raw fields.
