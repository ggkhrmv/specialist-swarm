# Anatomy — data model and JS contract

A capability map is one self-contained HTML file. State lives in the source as JS data blocks;
`localStorage` mirrors live edits; JSON is the exchange format. This file specifies the contract.

## Data blocks (in the `<script>`)

```js
// MODEL — the capability model. Groups/layers, each with capabilities.
// cur = current maturity today; tgt = target maturity goal. Integers 0..4.
const MODEL = [
  { id: "layer-a", name: "<Layer name>", caps: [
      { id: "cap-a1", name: "<Capability>", cur: 0, tgt: 3 },
      { id: "cap-a2", name: "<Capability>", cur: 1, tgt: 3 },
  ]},
  // ... more layers
];

// NOTES — one reasoning note per capability id. Why this current, why this target.
const NOTES = {
  "cap-a1": "",
  "cap-a2": "",
};

// DETAIL — per-capability rubric: what each level 0..4 means for this capability.
const DETAIL = {
  "cap-a1": { rubric: ["Absent: …","Initial: …","Developing: …","Established: …","Leading: …"] },
};

// GREEN_CUR — current values for the greenfield ("no self-service platform yet") framing.
// Only needed if the copy will be presented in greenfield mode.
const GREEN_CUR = { "cap-a1": 0, "cap-a2": 0 };

// SUBS — the components / sub-items under each capability, with a three-state verdict each.
// state: "have" | "partial" | "gap".  A needed-but-missing item is listed as "gap", NOT omitted —
// absence must be as visible as presence, or the grade cannot be audited.
// note: EVERY list is either exhaustive or explicitly labelled exemplary. Say which.
const SUBS = {
  "cap-a1": {
    exhaustive: true,            // false ⇒ the list is exemplary; say so in the UI too
    note: "exhaustive of the engine surface; single-lifecycle adoption is the gap",
    items: [
      { name: "<Component>", state: "have" },
      { name: "<Component>", state: "partial" },
      { name: "<Component needed but absent>", state: "gap" },
    ],
  },
};
```

**Exhaustive or explicitly exemplary.** Any enumerated list inside the assessment — components,
sub-capabilities, evidence items — carries that label. A silently partial list reads as carelessness
and quietly inflates the score, because the reader assumes what they see is all there is. This came
from the owner directly: *"some capabilities do not have all — either we mark as exemplary, or add
all components."*

## The 0–4 scale (fixed)

`0 Absent · 1 Initial · 2 Developing · 3 Established · 4 Leading.` Every capability spells out
what each level means in `DETAIL[id].rubric`. Keep target defaults honest — defaulting most
capabilities to 4/Leading inflates the implied build; reserve 4 for genuine differentiators and
default the rest to 3, with a note that target is a business choice.

## Mode (brownfield / greenfield)

A toggle frames the assessment for a client who already has a self-service platform (brownfield)
vs one who does not (greenfield). Greenfield seeds current values from `GREEN_CUR`. Use a `dirty`
flag so switching the mode *before any edit* reseeds the defaults, but switching *after* edits
does not silently wipe the user's work. Keep current-vs-target scoring available in both modes.

## Persistence

- **Source-baked defaults** — `cur`/`tgt`/notes in the source are what a freshly opened copy
  shows. This is the source of truth for a delivered copy.
- **localStorage** — the live-edit store during a scoring session (`{ mode, scores: {id: {cur,
  tgt, note}} }`).
- **JSON export/import** — export the current state to JSON; import folds a client's exported
  JSON back in. An agent folds an exported JSON into a copy's source (`MODEL`/`NOTES`) so the
  baked state matches.
- Use an `esc()` helper for safe interpolation of notes into the DOM.

## Functions (typical contract)

`seed()` (populate defaults, mode-aware) · `load()` (from localStorage or seed) · `save()` (to
localStorage) · `export`/`import` (JSON) · `render…()` (scoring view controls; presentation/map
view; print view). Every `getElementById`/`querySelector` target must exist in the DOM.

## Views

- **Scoring view** — editable: per-capability `cur`/`tgt` controls and an editable notes
  `<textarea>`.
- **Presentation / map view** — read-only: the capability map with scores and non-empty notes
  rendered read-only. This is the client-facing view.
- Toggle with a `data-view` control (mirror the offering site's toggle pattern). **Print and
  no-JS show the presentation/map view** so the file is useful without scripting.

## The gap radar

The map ships with a radar chart built from the scores — it is what makes the gap legible at a glance,
and the spec below is the one that survived four rounds of tuning.

- **One axis per capability.** Current as a solid polygon with a **very light tint**; target as a
  **dashed outline**. **No area fill between them** — filling the gap band reads as noise.
- **Non-zero inner radius (~15–16px).** A 0 score must draw as a small visible ring, not collapse into
  the hub. (Tuned from 30px, which read as "too big"; 16 was right.)
- **Ring labels 0–4** along one axis, so the scale is readable without a legend lookup.
- **Right-hand legend, colour-coded by layer, sorted largest-gap-first.** The sort is the point: the
  reader's first question is where the biggest gaps are.
- **Avg current / Avg target / Avg gap tiles** alongside.

Scoring inputs are **sliders**, not dropdowns, with the level meter as a live display. A general 0–4
legend (level name plus a one-line meaning) sits **at the top of the page**; the per-capability rubrics
stay in the cards.

## Control visibility

**Any control that must work in every view lives outside a view-scoped group.**

The classic bug: export and import buttons placed inside a `scoring-only` toolbar group, therefore
hidden in the default presentation view — so "we cannot export as JSON" was a layout error, not a
missing feature. Audit each control against the views it must be reachable from.

## Validation

Validate with the `asset-forge` Build checklist: tags balanced; JS parses (`node --check`); no
duplicate static ids; every `getElementById` target exists; the agent-guide comment contains no
`--`. Any map diagram's geometry goes through `diagram-spec`.

Additionally: every control reachable in the views that need it; every `SUBS` list labelled exhaustive
or exemplary; every stated capability **count** in prose matching the model (digit and word form); and
the radar iterating the full capability set after any model change.
