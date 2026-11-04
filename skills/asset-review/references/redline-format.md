# Redline format

## Table schema

| Loc | Current | Suggested | Why | Priority | Status |
|-----|---------|-----------|-----|----------|--------|

**Loc** — slide number, section heading, or paragraph identifier. Be precise enough that the author can navigate there without reading the whole document. Examples: "Slide 4 / Para 2", "§3.2 title", "Executive Summary / Para 3 / sentence 2".

**Current** — verbatim text from the draft. Do not paraphrase. If the issue is structural (missing content, wrong order, no content at all), quote the nearest anchor sentence and describe the gap in Why.

**Suggested** — the replacement text, or a specific action ("move this paragraph to §3.1", "delete", "replace 4.2.1.3 with 4.5.2"). If the fix requires author judgment, describe the direction rather than inventing a sentence they would not recognize as theirs.

**Why** — one sentence. Make it specific enough that the author can tell whether they agree or disagree. "Unclear" is not a Why. "The referenced clause covers Base Platform, not SLAs, so the evaluator scoring SLA criteria will not find a response here" is a Why.

**Priority** — P0, P1, P2, or D.

**Status** — the adjudication verdict: CONFIRMED, FALSE POSITIVE, or JUDGEMENT. See below.

---

## Adjudication — before anything enters the table

Merging is not transcription. A persona reads a flattened text extract, not the rendered asset, and
it may be working from a ground-truth file that predates a decision the author has since made. Label
every finding before it becomes a row:

**CONFIRMED** — you reproduced it. For a numeric finding this means re-deriving the figure from the
source data or the script that produced it, not re-reading the sentence. For a "garbled / duplicated /
missing text" finding it means checking the markup, because inline-styled fragments, chips, and
view-toggled blocks read as garbled in an extract while rendering correctly.

**FALSE POSITIVE** — the persona was wrong. Say why in one line, and keep the row: the author needs to
know the board was audited too, not just the asset. Two recurring sources — an extraction artefact,
and a reviewer reading a stale ground-truth file and confidently reporting the current, correct value
as an error.

**JUDGEMENT** — there is no fact to check; it is the author's call. These usually become `D` rows.

Two rules that follow:

- **Check every finding against the state file's decision log.** A finding that contradicts a logged,
  dated decision is a **conflict to surface**, not an entry to apply. Cite the log entry as the
  rationale for rejecting it. This is the most common false-positive class in a repeat review — do not
  silently revert an owner's decision because a reviewer had older information.
- **If adjudication shows your own earlier report was wrong, log it as a correction.** Say so plainly,
  old value beside new. Do not fix it silently.

Report the board's **negative** result alongside the findings: name what it attacked and could not
break. That is what tells the author which parts of the asset are load-bearing.

---

## Priority levels

**P0 — must fix before sending.** The asset cannot go out with this issue. The threshold is whether the error creates a scoring penalty, a factual misrepresentation, or a contractual gap the recipient will act on. Examples: wrong RfQ requirement ID that misdirects a scoring evaluator; factual error in a client name or technology claim; a MUST requirement from the RfQ with no response anywhere in the document. Also: any claim the asset's **own** evidence layer contradicts, and any figure that fails a `number-check.md` check.

**P1 — strong recommend.** The asset survives but will be meaningfully weaker without the fix. Examples: a win theme stated in the introduction but not supported by evidence anywhere in the body; an executive summary whose opening paragraph does not answer the governing question; a section pitched at the wrong altitude for its audience.

**P2 — polish.** Fix if time allows; the asset is shippable without it. Examples: a noun-phrase section title that should be a declarative claim; a paragraph that runs 40% longer than it needs to; a formatting inconsistency across slides.

**D — deferred, the author's call.** Not applied. A finding is D rather than P0 when acting on it would change the asset's **commercial, political, or scope posture**, or when two valid readings exist and no fact decides between them. A D row states the finding, the options, and the cost of each — **including the cost of doing nothing**, which is the one authors most often underestimate. Examples: whether to put a price on the page at all; whether to name a team whose data carries a negative finding; whether to concede a scope boundary a reviewer wants expanded.

Every D must come back with a recorded ruling, logged in the state file. **A D silently dropped is worse than a P1 ignored** — the author believes they decided something they never saw.

---

## Presenting the redline

Do not hand over a flat list. Split it into three groups, and put only the second and third to the
author as questions:

1. **Applied** — findings you verified and fixed, reported as before → after. Cluster them by the
   single underlying decision they share, so a whole theme takes one approval rather than fifteen.
2. **Content gaps** — findings needing a number, a fact, or a judgement only the author has. Never
   invent these.
3. **Deferred / conflicts** — the `D` rows and any genuine persona conflict you deliberately did not
   resolve.

Order the deferred set by **what blocks the decision the asset is asking for**, and work through them
interactively in small batches. When an answer implies a number, derive it and check it before
committing; if the data cannot support it, say so and ship it labelled.

**Rank by convergence.** State how many personas raised each theme independently. A finding raised by
three personas outranks a single-persona P0 — convergence is what lets the author triage quickly.

---

## Verbatim-current rule

Always quote the Current field verbatim, even if the text is awkward or embarrassing. Two reasons: the author needs to locate it in the draft quickly, and quoting verbatim prevents the reviewer's paraphrase from being mistaken for the suggested replacement.

For structural issues where there is no offending sentence to quote, use the nearest section heading or anchor sentence as the Loc/Current pair and describe the structural problem in Why.

---

## Order

Sort rows by page or slide number, then by priority within the same location (P0 before P1 before P2). This order is intentional: it lets the author work through the document once from front to back and resolve issues in priority order within each location.

---

## Worked example

Three rows from a sovereign-Kubernetes proposal for [CLIENT]:

| Loc | Current | Suggested | Why | Priority |
|-----|---------|-----------|-----|----------|
| Slide 6 / §3.2 / sentence 1 | "As required by clause 4.2.1.3, we provide a fully managed control plane with 99.9% availability." | "As required by clause 4.5.2, we provide a fully managed control plane with 99.9% availability." | RfQ clause 4.2.1.3 covers Base Platform; the managed-control-plane SLA requirement is under 4.5.2. The evaluator scoring SLA criteria (cluster 5) will not find a response here. | P0 |
| Slide 9 / §4 title | "Observability and FinOps Tooling" | "Grafana and OpenCost give [CLIENT] a single view of cost and availability from day one" | Noun-phrase titles conceal the claim. An evaluator reading only titles should be able to reconstruct the argument; this one tells them the topic, not the conclusion. | P1 |
| Slide 11 / Para 1 | "This approach is not a legacy migration, but rather a forward-looking transformation that empowers [CLIENT] to own its platform destiny." | "This approach migrates the 25-cluster estate to a sovereign open-source stack, beginning with the lowest-criticality test clusters." | "Not X, but Y" framing plus vague empowerment language; the concrete migration sequence is the claim that earns credibility. | P1 |
