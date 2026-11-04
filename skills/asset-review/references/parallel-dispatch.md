# Parallel dispatch — the persona board

**The shared dispatch doctrine is in `asset-forge/references/dispatch.md`** — brief structure, model
routing, concurrency limits, stall detection, and how to treat what comes back. Read it first. This
file covers only what is specific to a persona board.

## Pattern

Dispatch personas as parallel read-only subagents using the `superpowers:dispatching-parallel-agents` skill. Each persona receives the full draft text and its persona prompt. They run concurrently and return independent finding lists. Do not have them read each other's output; independence is the point.

Parallel dispatch means the review time is roughly constant regardless of how many personas run, because they work concurrently. Token cost scales with persona count; wall-clock time stays roughly flat because personas run concurrently.

## The persona brief

Beyond the persona prompt itself, every brief carries five blocks. Writing these out each time is the
norm — they are what separates a board that finds real defects from one that reports false gaps.

1. **The asset text with register and view markers** — `[ARCHITECT-VIEW ONLY]`, `[TITLE]`,
   `[EYEBROW]`, `[SUB]` — so each line is judged at its own altitude, plus the navigation contract for
   reaching hidden layers. A persona that reads only the default view reviews half the asset.
2. **Context** — the ask, the audience, the spine.
3. **What is new in this revision** — weigh it hardest; read everything for consistency.
4. **Stipulations and locked rulings** — what is settled, and what critique is out of bounds for this
   asset ("you are already bought in on the premise — do not ask to be sold on it"). Pass the state
   file's locked-rulings register in verbatim, with: *these are settled; do not re-raise them. If you
   believe a ruling is now wrong because the asset has changed, say so once and say why.* Without
   this, a dominant finding returns every round and the board's credibility decays.
5. **Role-specific payload** — the terminology ledger for the practice lead ("enforce it; every drift
   is a finding"); an inventory of what a changed section already contains, for the redundancy
   persona; diagram ids and what each shows, for the technical and redundancy personas.

Plus a **read-only clause**: "this is read-only — find problems, propose fixes, apply nothing."

State which layer each persona should weight. The exec persona reads the default view and flags detail
bleeding into it; it does not critique the technical layer's register.

## Before you dispatch

Grep visible copy for bracketed placeholders and resolve or annotate every hit. A placeholder sitting
in the ask or the commercial box consumes the **top finding of every persona** — in one board, six
personas each spent a P0 rediscovering a single gap the author already knew about. If a gap must stay
open, say so in the brief and put it out of scope.

## Persona cap

**Minimum viable default: 3 personas. Maximum: 7.** Nine roles are defined; a full proposal often runs five to seven (the buyer/red-team/exec set plus author-credibility and, when relevant, the practice lead).

Choosing the right subset matters more than running more personas. A red-team pass on an internal readout is waste; a legal pass on a proposal with no SLA language is noise. Select by asking which roles will have genuine concerns about this specific asset.

## Model and effort

Persona review is adversarial reasoning, not retrieval — it rewards a strong model. **Dispatch the reviewer subagents on a strong model at high reasoning effort by default** (this was the pattern that produced trusted output in practice: a capable model pinned at high effort). Pin the model and effort explicitly on each dispatch rather than inheriting silently, and tell the user what you pinned so they can override. The analytical personas — red-team, exec/MD, author-credibility, practice lead — benefit most; do not under-power them to save tokens. If cost is a constraint, cut the persona *count*, not the per-persona capability.

This is a deliberate override of the general routing table in `asset-forge/references/dispatch.md`: a
persona board is the one fan-out where every agent sits in the top tier regardless of budget, because
an under-powered reviewer produces agreeable output that misses the real objection.

Typical subsets by asset type:

| Asset type | Suggested subset |
|---|---|
| Full competitive proposal (RfP/RfQ) | Economic buyer, technical buyer, procurement, red-team, exec/MD — add legal if SLAs or IP terms are present |
| Internal readout or POV | Technical buyer, exec/MD |
| Short pitch or capabilities overview | Economic buyer, red-team, exec/MD |

These are starting points. Override them based on what the intake material reveals.

## Token cost

Each persona reads the full draft. A 40-slide proposal dispatched to five personas costs roughly 5x the tokens of a single pass. Account for this before dispatching the full six-persona board on a 100-page document.

For very long assets, consider splitting the dispatch: run economic buyer, red-team, and exec/MD over the full document; run technical buyer and procurement over the technical and commercial sections only.

## Merging outputs

**Hold the whole board.** Do not edit, or announce conclusions, on a partial return — acknowledge each
arrival and wait. While the personas work, run the deterministic steps yourself (self-consistency,
number integrity, terminology, the tell-scan) so they are ready to merge alongside the persona findings.

After all personas return:

1. Collect all finding lists into a single working table.
2. **Adjudicate every finding** — CONFIRMED / FALSE POSITIVE / JUDGEMENT — before it becomes a row. Re-derive numeric findings; check findings against the state file's decision log. Full method in `redline-format.md`.
3. De-duplicate by location and issue: if two personas flag the same sentence for the same reason, keep one entry and note both sources in Why — and **record the convergence count**, because a finding raised independently by three personas outranks a single-persona P0.
4. Where personas conflict (one recommends cutting, another recommends expanding), keep both entries at their respective priorities and flag the conflict explicitly rather than resolving it silently. The author decides.
5. Sort by page number, then by priority within each page (P0 first, then P1, P2, then D).
6. Output as the standard redline table (Loc | Current | Suggested | Why | Priority | Status), split into applied / content gaps / deferred.
7. **Report the negative result**: name what the board attacked and could not break. That is what tells the author which parts of the asset are load-bearing.

Distinct frames are the point of the merge; do not average personas into a consensus before merging.

## Acting on a finding that says "cut this visual"

A recommendation to cut a diagram or figure is a destructive, hard-to-reverse change. Do not act on a
persona's word alone, and never fold it into a batch of verbal fixes. Put the artifact in front of the
user first — offer to render it in isolation — then present three things together: what it duplicates
and where (naming the higher-fidelity replacement), the strongest case for keeping it, and your own
lean. The decision is the author's.
