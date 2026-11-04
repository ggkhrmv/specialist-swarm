---
name: capability-map
description: Build a reusable capability and maturity assessment as a single self-contained HTML file that an enterprise architect (or an AI agent) fills out for a specific client — a capability map. Capabilities are grouped into layers, each scored current vs target on a 0–4 maturity scale with per-capability reasoning notes and level rubrics; state is baked into the source so a filled copy travels as one file, with localStorage for live edits and JSON export/import. The file carries an embedded agent-guide comment (how an agent fills it, what to edit, the neutral scoring method) and offers two views — a scoring view and a presentation/map view — plus a brownfield/greenfield mode. Engine- and framework-agnostic by construction: encode the method, not client- or vendor-specific instances. Use when creating a capability model, maturity assessment, readiness assessment, or target-architecture scoring tool that must be reusable across clients and fillable by an architect or an agent. Not for a linear pitch deck or narrative document (see asset-forge Build) and not for data charts (see dataviz).
---

# capability-map

## What this asset is

A **capability map** is a self-contained HTML assessment: a set of capabilities grouped into
layers, each scored on maturity, that an enterprise architect or an AI agent fills out for a
specific client. It is a reusable asset type — build the base once, then produce a client copy
for each engagement. The offering it supports (e.g. a diagnostic + an offering site) cross-links
to it; it is often the paid, in-depth deliverable behind a lighter free diagnostic.

It has to satisfy three properties that an ordinary slide does not, which is why it is its own
skill:

1. **Fillable by an agent *or* a human**, with an embedded guide telling an agent exactly how.
2. **State baked into the source**, so a filled copy opens already showing its scores and notes
   and travels as one file — plus localStorage for live edits and JSON export/import.
3. **Engine- and framework-agnostic by construction** — it encodes a *method*, not a specific
   client's or vendor's instances, so it is genuinely reusable.

## Anatomy

Read [references/anatomy.md](references/anatomy.md) for the full data model and JS contract. In
brief, the file holds:

- **MODEL** — the capability groups/layers, each capability with `cur` (today) and `tgt` (goal),
  integers on the **0–4 scale**: 0 Absent · 1 Initial · 2 Developing · 3 Established · 4 Leading.
- **NOTES** — one reasoning note per capability id (why current, why target): editable in scoring
  view, read-only in the presentation view.
- **DETAIL** — per-capability rubric text spelling out what each 0–4 level means.
- **GREEN_CUR + mode** — a brownfield/greenfield toggle; greenfield seeds different current
  values via `GREEN_CUR` and a `dirty` flag so switching before any edit reseeds defaults.
- **Views** — a scoring view (editable) and a presentation/map view (read-only), toggled by a
  `data-view` control; print and no-JS show the map.
- **Persistence** — source-baked defaults, `localStorage` for the live session, JSON
  export/import; an agent folds an exported client JSON back into a copy's source.

## The embedded agent guide

Every capability map opens with an HTML-comment **agent guide** — effectively a small skill
baked into the artifact — telling an agent how to fill it. Read
[references/agent-guide.md](references/agent-guide.md) for the template and the neutral scoring
method (score along constraint axes — environment/stage, compliance, operating-model /
responsibility split, risk/autonomy, scale/tenancy — encoding the method, never baked client or
industry examples). The guide must contain no `--` sequences (they close HTML comments) and must
stay fully agnostic.

## Workflow

1. **Define the capability model with the architect** (or reuse an existing base): the layers,
   the capabilities under each, and the 0–4 rubric per capability. Keep it MECE and keep the
   layer names canonical (they will be referenced by the offering — align with the `positioning`
   terminology ledger). **The model stays open:** when the owner raises an adjacent concern, test
   whether it fits an existing capability's *definition*; if it is adjacent but outside, add a
   capability rather than stretching a neighbour to absorb it — stretched definitions destroy MECE and
   make the grade meaningless. Adding or removing one is a model change with a wide ripple; work the
   checklist in [references/alignment-interview.md](references/alignment-interview.md).
2. **Build the base file** to the anatomy contract. Treat it as read-only; never score the base.
3. **Write the agent guide** (agnostic method only) and the DETAIL rubrics.
4. **Walk the model with the owner.** Targets before current scores, one capability per turn, rubric
   levels stated as concrete observable ability rather than adjectives. Expect to be graded down, and
   keep one deliberately low target as the honesty anchor. Method in
   [references/alignment-interview.md](references/alignment-interview.md).
5. **Score against the evidence discipline:** demonstrated not designed; field-validated not merely
   running (code plus green tests plus CI is level 1); adjacent-org and adjacent-layer evidence is
   *reference*, not your grade. Rules and the grading-agent evidence contract in
   [references/scoring-discipline.md](references/scoring-discipline.md).
6. **Produce a client copy** for an engagement: `cp` the base, set `cur`/`tgt`/notes in the copy's
   source (or let the agent fill it via the guide), pick the mode.
7. **Validate analytically** with the `asset-forge` Build checklist (tags, dup ids, JS parses via
   `node --check`, every `getElementById` target exists, agent-guide comment has no `--`), and via
   `diagram-spec` for any map SVG. Confirm every control is reachable from the views that need it, and
   that every stated capability count matches the model. Hand the visual pass to the user.

## Reference files

- [references/anatomy.md](references/anatomy.md) — data model and JS contract, the `SUBS` components
  block, the gap-radar spec, control visibility
- [references/agent-guide.md](references/agent-guide.md) — the embedded agent-guide template and the
  neutral scoring method
- [references/scoring-discipline.md](references/scoring-discipline.md) — what evidence may lift a
  grade, and what is reference-only
- [references/alignment-interview.md](references/alignment-interview.md) — walking targets and scores
  with the owner; the model-change ripple checklist

## Conventions

Always use `[CLIENT]` as the placeholder. Keep the base engine-agnostic: a specific engine (e.g.
Crossplane) may be named only as *one example* in a description, never as the required substrate.
