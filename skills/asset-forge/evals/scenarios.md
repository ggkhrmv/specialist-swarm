# asset-forge evals

## Scenario 1 — end-to-end start
**Prompt:** "Help me build a proposal for [CLIENT] from scratch."
**Expected behavior:**
- Runs Intake: gathers brief + side-channel intel, builds stakeholder map, captures submission mechanics, and ASKS for missing context instead of assuming.
- Runs Qualify (bid/no-bid) before framing.
- Delegates Frame -> positioning, Storyline -> storyline, Review -> asset-review.
- Writes and updates asset-forge-state.md.
**RED baseline:** jumps straight to drafting slides; no intake questions, no qualify, no state file.

## Scenario 2 — gate discipline under pressure
**Prompt:** "Skip the storyline, we're in a hurry — just build the deck."
**Expected behavior:** honors the iterative-checkpoint intent — offers a quick strawman for alignment but does NOT sink effort into a polished build before a governing thought is agreed; explains why in one line. Does not silently comply.
**RED baseline:** immediately builds a full polished deck.

## Scenario 3 — build branching + render opt-in
**Prompt:** "Build the RfP response document." vs "Build the pitch deck."
**Expected behavior:** document path (prose, no render) for the RfP response; deck path for the pitch deck; asks before any token-heavy render-verify; treats HTML as deliverable OR PPTX intermediate per user choice.
**RED baseline:** always produces an HTML deck; auto-renders.

## Scenario 4 — no double-trigger
**Prompt:** "Draft the SCQA storyline for this deck."
**Expected behavior:** the storyline skill fires; asset-forge does NOT hijack the whole workflow for a single-phase request.
**RED baseline / risk:** orchestrator over-triggers on any asset noun.

---

## Step 2 — RED baseline reasoning

**S1.** Without this skill, the model treats the user's opening prompt as a brief and starts producing content. It has no Intake phase concept, no qualify step, and no state-file mechanism. All four expected behaviors are absent. Confirmed RED.

**S2.** Under time pressure, the default behavior is silent compliance: the model interprets "skip" as permission and builds. The iterative-checkpoint concept — strawman as the fast path rather than a full skip — does not exist in default reasoning. Confirmed RED.

**S3.** The default model defaults to the output format it finds most tractable. For a deck prompt, HTML or markdown slides are the natural output, produced without asking. The document-vs-deck branch and the render opt-in rule do not exist without instruction. Confirmed RED.

**S4.** Without the SKILL.md description's explicit disambiguation ("For a single phase... invoke that sub-skill directly instead"), an orchestrator pattern tends to frame any asset-related prompt as the start of a full workflow. This is a real trigger risk. Confirmed risk.

---

## Step 5 — GREEN verification

**S1 GREEN.** SKILL.md's "Guide behavior" section instructs asking for what is missing. `references/intake-checklist.md` provides the full question set. The state-file rule mandates writing `asset-forge-state.md` at Intake. The Qualify phase is an explicit gate before Frame. The three REQUIRED SUB-SKILL markers in the phase table route Frame to positioning, Storyline to storyline, and Review to asset-review. All four expected behaviors are now addressed.

**S2 GREEN.** `references/gates.md` Gate 2 (Storyline) names "I'll draft a few slides to show what I mean" as an explicit red flag for skipping. The rationalization table addresses the time-pressure case ("The strawman is the fast path"). SKILL.md's guide-behavior section instructs offering the fastest path that still honors the governing gate. The behavior is addressed.

**S3 GREEN.** `references/phases.md` Phase 5 (Build) documents both deck path and document path explicitly. The render opt-in rule (ask first, state token cost, default skip) is written into the deck path. The HTML-vs-PPTX handoff is stated. The document path specifies no render step. Branching and render opt-in are addressed.

**S4 GREEN.** The SKILL.md frontmatter description ends with: "For a single phase (just the positioning, just the storyline, or just a review), invoke that sub-skill directly instead." This is visible at trigger time and disambiguates single-phase requests before the orchestrator engages. Risk addressed.

---

## New scenarios (v2 — expanded workflow: rework loop, frame gate, new asset types)

Each scenario carries its own RED baseline and GREEN verification inline.

## Scenario 5 — the rework loop
**Prompt:** "The client sent back a page of comments on the deck — here they are. [pastes notes]"
**Expected behavior:** logs each reviewer/note in the reviewer log; triages every note **accept / reject / defer** with a one-line rationale (rejecting a bad note is legitimate); **aligns before rewrite** — states back what it will change and won't, and why, and gets sign-off *before* editing; scopes the change (copy pass / section rework / structural re-cut, the last re-entering the Frame+Storyline gate); executes, re-verifies with the Build checklist + relevant review slice, and logs the increment.
**RED baseline:** starts editing immediately on the first pass of understanding, applies every note uncritically, no triage, no alignment, no state-file update.
**RED reasoning:** the default treats a feedback batch as an instruction list to execute top-to-bottom. There is no concept of triage (accept/reject/defer), no align-before-rewrite checkpoint, and no reviewer/change log — so conflicting notes get half-applied and the reasoning is lost. Confirmed RED.
**GREEN:** `references/phases.md` Phase 7 (Rework) defines capture → triage → align → scope → execute → re-verify → log; the align-before-rewrite checkpoint is stated in both phases.md and SKILL.md; the state-file template carries reviewer/decision/change logs. Addressed.

## Scenario 6 — positioning-frame gate before build
**Prompt:** "We both know this is about AI — just build the deck."
**Expected behavior:** before any polished build, locks the **positioning frame** in one line — what the asset is *for* and, crucially, what it is *not* (e.g. "enabler, not a guardrail pitch") — alongside the governing thought and outline; explains in one line why (a wrong frame invalidates every section and is only discovered after an expensive build). Offers a fast strawman, not a skip.
**RED baseline:** builds a polished deck on an unstated frame; the frame turns out wrong and the whole asset is reworked.
**RED reasoning:** the default has no concept that "what this is for and not" is a separate, must-lock decision; it infers a plausible frame silently and builds. This is exactly the failure that forced a whole-asset reframe in real use. Confirmed RED.
**GREEN:** `references/gates.md` Gate 2 (Frame+Storyline) requires the positioning-frame line locked before build, with a rationalization row ("The frame is obvious…") and the failure named. `positioning` produces the frame line. Addressed.

## Scenario 7 — capability-map asset type
**Prompt:** "Build a reusable maturity assessment our architects can fill in per client."
**Expected behavior:** recognizes the capability-map asset type; delegates to the `capability-map` skill (self-contained, agent-or-human-fillable HTML: MODEL/NOTES/DETAIL/GREEN_CUR, 0–4 scale, dual view, source-baked state + JSON, agent-guide comment, brownfield/greenfield mode); keeps it engine-agnostic and MECE with canonical layer names.
**RED baseline:** builds a static slide or a one-off table with no fill-in mechanism, no persistence, no reusability.
**RED reasoning:** the default produces a presentation artifact, not a reusable, fillable tool with baked state — it has no pattern for an agent-fillable HTML asset. Confirmed RED.
**GREEN:** the Build phase now lists a capability-map path delegating to the `capability-map` skill; the asset type appears in the phase table and description. Addressed.

## Scenario 8 — analytical validation, no auto-render
**Prompt:** "Is the site finished?"
**Expected behavior:** runs the analytical Build validation (tag balance, dup ids, dangling anchors, self-contained, JS parses, content scans), reports counts, and states plainly that the **visual pass is the user's** — does not auto-screenshot/render (blank + token cost) and does not claim visual correctness it cannot verify.
**RED baseline:** declares it done, or attempts a render to "confirm," burning tokens on a blank result.
**RED reasoning:** the default equates "looks structurally complete" with "done" and reaches for a screenshot to verify — which returns blank here. It has no analytical-validation checklist and no norm of handing the visual pass to the user. Confirmed RED.
**GREEN:** `references/build-validation.md` defines the analytical checklist and the render-only-on-request + hand-off-visual-pass rules; the Build phase points to it on every path. Addressed.
