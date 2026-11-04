# Scoring discipline

Two rules bind every **current** score, and one bounds what counts as evidence for it. All three had
to be supplied by the asset owner mid-assessment, after grading agents proposed raises the owner
rejected — which means nothing in an unaided pass enforces them.

---

## 1. Demonstrated, not designed

**Breadth the design allows does not count. Only breadth that has actually been exercised.**

An engine built to be general, with exactly one consumer, is not a general engine yet. A grading agent
argued 3 on the strength of the architecture; the honest score was 2, because one consumer is what had
been demonstrated.

Score what the capability has done, not what it could do.

---

## 2. Field-validated, not merely running

**"The code exists, runs, and passes its own tests" is level 1.** Level 2 requires at least one real,
non-synthetic use that produced a real outcome.

A grading agent raised a capability from 1 to 2 citing "real engine, tests green, CI, serving
traffic". The owner's response: *"it is not tested yet though, so maybe we should not oversell?"* — and
on probing, "not tested" meant not that unit tests were missing, but that **the capability had never
been validated in real use**. It went back to 1.

So: **tests, CI, and architecture quality are plumbing evidence. They never lift a maturity grade on
their own.** Say so in the note, and drop "tested" as a maturity signal — it is ambiguous between two
very different claims.

The status ladder in `positioning/SKILL.md` is the same idea in the positioning context: code exists →
proven once → deployed → producing real ongoing output.

---

## 3. Score the unit the assessment names — nothing else

**Evidence from a sibling organisation, another team, a vendor programme, or an adjacent architectural
layer is *reference* evidence, not your grade.**

Three proposed raises (0→2, 1→2, 1→2) rested respectively on a deployed system in a sibling
organisation, an external vendor's programme, and mature isolation owned at a lower infrastructure
layer. All three were ruled reference-only.

Reference evidence is still valuable — cite it in the note, where it often **strengthens a low
target**: "already proven feasible elsewhere" is a good argument for aiming at 4. It just does not
move the current score.

**Before crediting an adjacent-layer mechanism, ask whether the graded unit actually inherits it.** A
shared central component that reaches *across* boundaries inherits nothing from per-boundary
isolation — that distinction sharpened a gap rather than closing it, and it came from the owner, not
from the evidence.

---

## Evidence requirements for a grading pass

Any agent or person producing a score must:

- **Cite repository, file and line, a commit, a run id, or a page id.** Never accept a README, a
  design document, or a roadmap as evidence of current state.
- **Place the capability on the status ladder** explicitly.
- **Receive the human's prior with an instruction to verify or challenge it** — this calibrates
  without anchoring.
- **Flag uncertainties for the human rather than resolving them.** The most useful returns look like:
  *"most subjective grade — flagged for human: 1 if primitives count, honestly 0 if enforced
  projection is required."*
- **Be told who will scrutinise this and why.**

An agent briefed this way will move a grade **down** as readily as up. That is the point.

---

## The honesty anchor

A map where everything is high reads as marketing. Expect the owner to grade **lower** than a first
pass — in one 16-capability interview the owner pulled four proposed 4s down to 3.

**One deliberately low target is the map's honesty anchor.** A map with restrained 3s and one
evaluate-only 2 reads as engineering; an all-4 map reads as a pitch and invites a reader to discount
every score on it.
