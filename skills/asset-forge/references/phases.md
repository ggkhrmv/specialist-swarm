# Phases

Full playbook for the six phases of the asset-forge workflow. For each phase: purpose, inputs, delegation, and the exit condition.

---

## Phase 1 — Intake

**Purpose.** Build a shared picture of the engagement before any framing or writing begins: what the asset is, who the audience is, what material exists, what is missing, and what the submission mechanics are.

**Inputs.** The user's opening prompt. May include an RfP/RfQ document, a briefing email, a previous deck, or just a verbal description.

**What to do.**

1. Establish the asset type: RfQ/RfP response, pitch deck, point of view, readout, or internal briefing. Ask if unclear.
2. Gather the brief and any source documents. Ask the user to share them; do not assume their contents. When a source is a slide deck or PDF (a client brief, a reference/house deck the asset should echo structurally), **ingest it to Markdown preserving the structure** — headings, section order, capability→benefit pairings — so it can actually be used downstream; confirm the extraction preserved the structure before relying on it. Names and titles from these sources are placeholders, not decisions (see the naming discipline in `positioning`).
3. Collect side-channel intel: prior conversations with the client, intelligence about who wrote the RfQ, known competition, relationship history. This often matters more than the formal brief.
4. Build the stakeholder map with four roles: economic buyer (who signs / approves budget), technical buyer (who evaluates the solution), coach (who inside the client wants you to win), and blocker (who will push back and why). Flag any unknown roles.
5. For tender responses, capture submission mechanics: deadline, page limits, mandated template, portal format, clarification window, and scoring criteria if stated.
6. Ask explicitly for what is missing. Do not assume reasonable defaults and proceed silently.
7. Write `asset-forge-state.md` with what you have at the end of this phase, including any open gaps.

**Exit condition.** Enough information exists to make a reasoned bid/no-bid decision: asset type confirmed, brief summarized, at least a partial stakeholder map, and the primary constraint identified (deadline, scope, commercial).

**Delegation.** None. This is a structured conversation.

---

## Phase 2 — Qualify

**Purpose.** Produce an explicit go/no-go decision before any framing work begins. This is the one moment when walk-away criteria can be evaluated while the cost of stopping is still low.

**Inputs.** The intake summary.

**What to do.**

1. Assess win probability across three factors: client relationship (do you have a coach or economic-buyer relationship?), scope fit (does the requirement set match your genuine strengths?), and competition (who else is bidding, and are you better positioned?).
2. Check walk-away criteria. Stop if: the timeline is impossible without cutting quality or honesty; the client has a preferred winner and is running a box-ticking exercise; the scope requires claiming capabilities you cannot evidence; the commercial model demanded is unsafe; there is a conflict of interest.
3. For non-competitive assets (internal POV, readout): confirm the purpose is clear, a real decision or action is required of the audience, and enough material exists to support the argument.
4. Present the assessment to the user: win probability, walk-away criteria hit or not, recommendation.
5. Get an explicit go / no-go. Record the decision and rationale in `asset-forge-state.md`.

**Exit condition.** User confirms go. If no-go, document the reason and stop.

**Delegation.** None. This is a structured assessment.

---

## Phase 3 — Frame

**Purpose.** Establish the commercial and strategic foundation: win themes, discriminators, scope options, commercial model, and — for tender responses — the compliance/traceability matrix and claims register.

**Inputs.** Intake summary, RfP/RfQ document (if tender), stakeholder map.

**What to do.**

1. Invoke the `positioning` skill. It selects the plays the intake reveals — offensive (win themes, discriminators, proof points) and defensive (tiered scope options, explicit assumptions, honest scope boundaries). Not all plays run on every deal.
2. For tender responses: extract and cluster requirements from the RfQ, preserving original IDs verbatim. Mark each requirement MUST or SHOULD (MUST = K.O. criterion). Open the compliance/traceability matrix. Open the claims register with initial entries labeled verified or aspirational.
3. Agree win themes with the user (the messages the evaluator should be able to repeat back). Agree the scope option (A/B/C or equivalent). Record both in `asset-forge-state.md`.

**Exit condition.** Win themes are agreed. Scope option is chosen or narrowed to two. For tenders, the compliance matrix and claims register are open.

**Delegation.** **REQUIRED SUB-SKILL:** positioning

---

## Phase 4 — Storyline

**Purpose.** Structure the argument before writing. The output is a governing thought, an SCQA frame, a MECE argument tree, and action titles — not prose, not slides.

**Inputs.** Win themes and scope option from Frame, any source material the user provides.

**What to do.**

1. Invoke the `storyline` skill.
2. Produce the four required outputs in order: (a) governing thought — a single declarative sentence that is the Answer to the reader's key Question; (b) SCQA frame that earns the governing thought; (c) MECE argument tree with claim sentences for each group; (d) action titles that pass the read-through gate (titles alone reproduce the argument).
3. Present the governing thought and two-level outline to the user for sign-off before building anything.
4. If the user disagrees, iterate on the governing thought first, then the argument tree, then the titles. This gate is iterative — revise until the governing thought is agreed. Do not build a polished asset to illustrate an alternative argument.
5. Record the approved governing thought and a pointer to the storyline document in `asset-forge-state.md`.

**Exit condition.** The governing thought is approved. Titles pass the read-through gate.

**Delegation.** **REQUIRED SUB-SKILL:** storyline

---

## Phase 5 — Build

**Purpose.** Produce the asset in its target format. The branch (deck or document) is determined at Intake.

**Inputs.** Approved storyline from Phase 4, win themes and positioning outputs from Phase 3, brand guidelines or templates if applicable.

### Build discipline (all HTML paths)

These apply across the deck, presentation-site, and capability-map paths:

- **Every section and every graphic earns its keep.** Before adding or keeping a block, ask what it does that an adjacent block or diagram does not. Cut prose that restates a diagram; cut decoration. A full restructure to consolidate a sprawling argument is a legitimate move, not a failure — but a structural re-cut re-enters the Frame + Storyline gate first.
- **Two-reader altitude, when the audience is mixed.** A common and effective pattern is one self-contained file with two views — a high-level pitch view (exec: claim + consequence, zero AI tells) and a low-level view (architect: mechanism and precision, technical register kept) — toggled in-page, with print/no-JS showing both. When you relocate detail from high to low, keep the claim up top and the mechanism below, and keep the back-links resolving.
- **Diagrams via `diagram-spec`.** Author and verify every inline SVG through the `diagram-spec` skill (layout invariants + analytical geometry verification).
- **Validate analytically; the visual pass is the user's.** After each build, run [references/build-validation.md](build-validation.md). Report the structural and geometry counts, then hand the visual pass over — that is the default every time, and a previous yes does not carry forward. You may *offer* to render when a specific question would be settled by it, naming that question; render only on an explicit yes. Never claim a render is impossible.
- **Self-consistency, during Build.** Where the asset carries its own honest layer (a maturity table, a basis column, caveats), compare the persuasive layer against it now rather than waiting for the review board — by then the fix is a re-cut, not an edit. Method in `asset-review/references/self-consistency.md`.
- **Voice on the copy.** Route every fragment you write through the `voice` skill — not only headlines and section titles, though those regress worst. Close with the machine tell-scan, scoped to what you wrote in this increment.

### Deck path

For pitch decks, executive presentations, and visual-first deliverables:

1. **ASCII mockup in terminal.** Before any HTML, sketch the slide sequence and rough layout in ASCII. Fast to change; catches structural problems before they are expensive.
2. **Single-file HTML — always via `presentation-websites`.** Build the presentation as one self-contained HTML file, and take the **format**, not the brand, as the reason to use the framework. Any single-file HTML asset for a brand whose tokens, fonts, and logo can be supplied goes through `presentation-websites`; the brand kit is the only variable. There is no "not our house brand, so build it plain" branch — that fork sent one asset outside the component library entirely and it then needed its own geometry, print-CSS, and de-slop tooling rebuilt from scratch. If no brand kit exists at all, the framework still supplies the structure and component library: pick one named fallback family, say so, and flag it.
3. **Validate analytically; the visual pass is the user's.** Run the analytical Build validation ([references/build-validation.md](build-validation.md)) as the default — structure, geometry, and content scans computed from source. Then hand the visual pass (16:9 proportions, no overflow) to the user. Offer a render only when a specific question needs it, and name the question.
4. **Output format.** HTML is a valid deliverable. If the target is PPTX, note the manual handoff: export the HTML and convert in PowerPoint or an equivalent tool. There is no automated HTML-to-PPTX path in this workflow.

### Document path

For RfP/RfQ responses, points of view, and readouts:

1. **Outline first.** Draft a section outline aligned to the approved storyline. Get user sign-off on the structure before writing prose.
2. **Prose in mandated format.** Write the document in Word, Markdown, or portal form — whichever the submission requires. Follow any page limits or template structure from the intake mechanics.
3. **No render step.** Documents do not go through the HTML or render pipeline.
4. **Structural patterns.**
   - POV: thesis / why-now / evidence. Lead with the thesis sentence; earn it with why this matters now; support with specific evidence (not generic claims).
   - Readout: findings then implications then recommendation then decision-ask. Each section moves the reader forward; none is a data dump.
   - Both patterns draw their narrative structure from the storyline outputs — the governing thought, SCQA frame, and MECE argument tree drive the section order and headings.

### Presentation site path

For self-contained HTML websites used as visual aids — screen-shared live or handed off for standalone offline viewing:

1. **Horizontal viewport first.** The primary layout constraint is a 16:9 presentation screen. Build and check at that ratio — a layout that looks balanced in portrait is often cut off or mis-proportioned when screen-shared.
2. **Single scrolling page.** Prefer one long page with anchor-linked sections over multi-page navigation. Multi-page navigation breaks in screen-share contexts and complicates offline use.
3. **Self-contained.** The file must open offline without network dependency: fonts embedded (base64 or local path), logos as inline SVG strings, no CDN links.
4. **Simulation components.** Mockups of tool interactions — chat interfaces, terminals, CLI output — are common in capability showcases. Strip them to convey the feel of an exchange rather than replicate it verbatim: if text is on screen, the audience reads it instead of listening. Build them through `presentation-websites` like everything else on this path; see its component rules for mockup fidelity and the illustrative-label requirement.

   **Label any depiction of an unbuilt state as illustrative, on the artifact itself.** A scripted mockup of a capability that does not exist yet was called the single weakest section in an asset by its red-team reviewer: it rendered the unproven core bet as a flawless finished demo, with invented precision and no caveat. The more polished and specific the mockup, the more it reads as a finished demo. The label goes on the figure — not in a footnote, not two sections away.
5. **Audience-visible content only.** Speaker notes, demo cues, and presenter flow belong outside the HTML. Anything visible on screen will be read by the audience.
6. **Before handoff:** run the analytical Build validation ([references/build-validation.md](build-validation.md)); confirm no simulation carries enough text to compete with the presenter; confirm no speaker notes are visible in the file; then hand the user the visual pass to confirm the layout holds at 16:9 horizontal.
7. **Exports, if asked.** PDF and single-view variants have their own failure modes — print CSS that defeats a view split, a specificity fight that silently ships the wrong layer, pagination that slices a diagram. See [references/export-paths.md](export-paths.md).

### Capability-map path

For a capability model / maturity assessment / readiness or target-architecture scoring tool — a reusable, architect- or agent-fillable HTML asset (often the paid, in-depth deliverable behind a lighter free diagnostic):

1. **Invoke the `capability-map` skill.** It owns the anatomy (MODEL / NOTES / DETAIL / GREEN_CUR, the 0–4 scale, dual scoring + presentation views, brownfield/greenfield mode, source-baked state + localStorage + JSON export/import) and the embedded agent-guide comment.
2. **Keep the model MECE and its layer names canonical** — they are referenced by the sibling offering; align with the `positioning` terminology ledger so the whole artifact system is consistent.
3. **Build the base as engine-agnostic** (a specific engine named only as one example), then produce a client copy per engagement.
4. Validate via the Build checklist + `diagram-spec` for any map SVG; hand the visual pass to the user.

This path is a common member of a **multi-artifact system** (e.g. free diagnostic → offering site → paid capability map), all cross-linked and tracked in the state file's artifact registry.

**Exit condition.** A complete draft in the target format exists and the user has reviewed it.

**Delegation.** Optional: `presentation-websites` (branded deck and presentation-site paths, using the brand kit the user supplies), `diagram-spec` (any inline SVG diagram), `capability-map` (capability-map path), `voice` (copy on any path).

---

## Phase 6 — Review

**Purpose.** Structured critique and quality verification before the asset reaches an MD or client.

**Inputs.** The complete draft, the claims register, the compliance matrix (for tenders), win themes from positioning.

**What to do.**

1. Invoke the `asset-review` skill.
2. It runs: persona critique (parallel read-only passes on a strong model at high effort — including author-credibility and, when relevant, the practice lead), human-feedback integration, redline merge into a page-by-page table, altitude + marketing-drift check, consistency/terminology check against the ledger, humanization + `voice` pass (with a machine tell-scan exit check), claims verification (provenance + technical soundness), and — for tender responses — compliance-matrix sign-off.
3. Apply redline changes to the draft.
4. For tender responses: confirm the compliance-matrix sign-off is complete before closing this phase. Every MUST requirement must be addressed and locatable by the evaluator.
5. Update `asset-forge-state.md` to mark Review complete.

**Exit condition.** The redline is applied. The claims register is signed off. For tender responses, the compliance matrix is signed off.

**Delegation.** **REQUIRED SUB-SKILL:** asset-review

---

## Phase 7 — Rework (the iterate loop)

**This is not an edge case. It is where a real asset spends most of its life.** An asset is rarely one-and-done: it comes back from an internal review, a practice lead, or a client with a batch of feedback, and the engagement re-enters here — often many times (v3 → v3.1 → v4 → v5 → …). Model the rework explicitly instead of ad-hoc patching.

**Purpose.** Turn a batch of reviewer feedback into an agreed, scoped change set, execute it, and re-verify — without churning a polished build on a direction nobody has signed off.

**Inputs.** The current asset, the state file, and a batch of feedback (external human notes, a fresh `asset-review` pass, or the user's own review).

**What to do.**

1. **Capture the batch.** Log each reviewer and the thrust of their feedback in the **reviewer log** in `asset-forge-state.md`. One reviewer, one row, one summary of what they're really asking for.
2. **Triage every note: accept / reject / defer,** each with a one-line rationale. **Rejecting feedback is legitimate** — not every note is right, and conflicting notes cannot all be honored. Cluster the accepted notes into themes rather than a flat list.
3. **Align before rewrite** (checkpoint — see below). Present the triaged change set — what you will change, what you will not, and why — and get explicit sign-off *before* touching the asset.
4. **Scope the change.** Classify it: a **copy pass** (voice/wording), a **section rework** (content within the existing structure), or a **structural re-cut** (the spine changes). A structural re-cut **re-enters the Storyline gate first** — re-lock the governing thought and outline before rebuilding. Do not restructure a polished build freehand.
5. **Execute** the scoped change in Build.
6. **Re-verify.** Run the Build analytical-validation checklist over the changed artifact, and re-run the **relevant slice** of Review — the changed sections, plus the claims, consistency/terminology, and voice checks. A small copy pass does not need the full persona board; a structural re-cut does.
7. **Voice-pass every fragment you wrote, inside this increment.** Not just headlines and titles, and not on request. Run the `voice` skill over the new prose and close with the tell-scan scoped to your own additions. This is part of the increment, not a follow-up: in practice an increment was reported as "applied and verified" and the author then had to ask for the voice pass separately — which found six over-long sentences, four connective em dashes, and three banned constructions in copy that had just been declared done. And because a voice pass changes tense, modality, and hedging, it is **claims-affecting**: re-check the claims on every line it rewrote.
8. **Log the increment.** Append a dated entry to the state-file change log, update the open-items / next-increments queue, and move anything cut-but-possibly-useful to parked content. Close by naming **one** scoped next increment — what it touches, how big it is, what you would show for approval — rather than an open "anything else?". If a decision you presented goes unanswered, make the call, say it is your call with the one-line reason, and offer the reversal.

**Exit condition.** The agreed change set is applied, re-verified, **and voice-passed**; the state file records the increment, the remaining open items, and the named next increment.

**Delegation.** `asset-review` (for the re-run review slice); `voice` (for copy passes); `presentation-websites` / `diagram-spec` (for build changes) as applicable.

---

## The align-before-rewrite checkpoint

After **any** review — a persona board, a practice-lead read, a client markup — do not start editing on the first pass of understanding. State back what you think each note means and how you propose to act on it, surface anything you are not fully grasping, and get the change set agreed. Then rewrite.

This is cheap and prevents the most expensive failure mode: a confident large rewrite in the wrong direction that then has to be reworked again. It is the rework-phase equivalent of the Storyline gate — align on direction before sinking effort into production.

**This covers how things look, not only what they say.** A change to the **visual structure** of an artifact you have already shown re-enters this checkpoint exactly like a content rewrite. Restyling in place and presenting the result is the failure mode — it took four rounds of unilateral redesign before one author had to demand "consult me before you change the way things look, so I can approve". So: state the change list back as you understood it, show an ASCII sketch of the proposed layout, name the one or two shape decisions that are genuinely the author's (pipeline versus hub-and-spoke, merge two diagrams or keep them separate), get approval, then build. Honoured properly, the rebuild lands in one pass.

**Two rules for triage itself:**

- **Check every note against the decision log before accepting it.** A note that contradicts a dated, logged decision is rejected on that basis, citing the entry — a reviewer working from a ground-truth file that predates a decision will confidently report the current, correct value as an error. This is the most common false-positive class in a repeat review, and applying it silently reverts the author's own decisions.
- **On a conflicting number, check scope match, then propagate.** Do not average, and do not defer immediately. First test whether the two figures measure the **same scope** — what is included, at what stage of completeness. Then propagate the reviewer's number to the headline claim and read the resulting sentence aloud. If accepting it makes the asset claim something the author would not defend, *that* is the finding to bring back, not the number.
