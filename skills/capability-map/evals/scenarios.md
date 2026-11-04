# capability-map evals

Each scenario carries its RED baseline and GREEN verification inline.

## Scenario 1 — build a reusable, fillable assessment
**Prompt:** "Build a capability and maturity assessment our enterprise architects can fill in per client."
**Expected behavior:** produces a single self-contained HTML file to the anatomy contract — MODEL (layers/capabilities with `cur`/`tgt`), NOTES (per-capability reasoning), DETAIL (0–4 rubrics), a scoring view and a read-only presentation/map view toggled by `data-view`, print/no-JS showing the map — with **state baked into the source** plus localStorage and JSON export/import, so a filled copy travels as one file.
**RED baseline:** a static slide, a flat table, or a fresh web app with no baked state, no dual view, no reusability.
**RED reasoning:** the default builds a presentation artifact or an ad-hoc form; it has no pattern for source-baked state, a scoring/presentation dual view, or JSON round-tripping — so the result is neither reusable nor fillable-in-place. Confirmed RED.
**GREEN:** `references/anatomy.md` specifies the data blocks, the 0–4 scale, the dual view, and the persistence contract; SKILL.md's workflow builds to it. Addressed.

## Scenario 2 — agent-fillable, engine-agnostic base
**Prompt:** "Make it so an AI agent can fill it out for a client, and keep it engine-agnostic."
**Expected behavior:** embeds the HTML-comment **agent guide** (never edit the base → cp a copy → edit MODEL/NOTES/GREEN_CUR → hand over), encodes the **neutral scoring method** (constraint axes: environment/stage, compliance, operating-model/responsibility-split, risk/autonomy, scale/tenancy) with no baked client/industry instances, keeps a specific engine as at most *one example*, and ensures the guide contains no `--` sequence.
**RED baseline:** bakes in a specific client/industry/vendor scenario; no embedded guide; or a guide that breaks the HTML comment.
**RED reasoning:** the default hard-codes the example it was given (losing reusability) and has no notion of an embedded agent guide or of encoding method-not-instances. Confirmed RED.
**GREEN:** `references/agent-guide.md` gives the guide template, the neutral scoring method, the no-`--` rule, and the agnostic-method principle. Addressed.

## Scenario 3 — honest targets + brownfield/greenfield mode
**Prompt:** "Set it up for both clients who already have a platform and greenfield ones."
**Expected behavior:** adds the brownfield/greenfield mode with `GREEN_CUR` seeds and a `dirty` flag (switching before edits reseeds; after edits does not wipe work); keeps current-vs-target scoring in both modes; defaults most targets to 3 (reserving 4 for genuine differentiators) with a note that target is a business choice.
**RED baseline:** single mode; defaults most targets to 4/Leading, inflating the implied build.
**RED reasoning:** the default builds one framing and, asked for maturity targets, reflexively maxes them — inflating scope. Confirmed RED.
**GREEN:** `references/anatomy.md` specifies the mode/`dirty`-flag behavior and the honest-target-defaults guidance. Addressed.

## Scenario 4 — validation + no double-capture
**Prompt:** "Is the assessment file done?" / "Chart the scores." 
**Expected behavior:** for "done", runs the `asset-forge` Build checklist (tags, dup ids, `node --check`, every getElementById target exists, agent-guide has no `--`) and `diagram-spec` for any map SVG, then hands the visual pass to the user; for "chart the scores", defers to dataviz — capability-map builds the assessment tool, not a data chart of results.
**RED baseline / risk:** claims done without analytical validation; or captures a pure charting request.
**GREEN:** SKILL.md's workflow step 5 routes validation to the Build checklist and diagram-spec; the description anti-triggers away from data charts. Addressed.
