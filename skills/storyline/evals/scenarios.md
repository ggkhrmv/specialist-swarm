# storyline evals

## Scenario 1 — narrative structure
**Prompt:** "Here are the raw points for our platform proposal [list]. Help me structure the storyline."
**Expected behavior:**
- Produces an explicit one-sentence governing thought (the "Answer" of SCQA).
- Frames Situation / Complication / Question before the Answer.
- Groups supporting arguments MECE under the governing thought.
- Drafts action titles (full-sentence, so-what) for each group.
- Runs the title-read-through: reading titles top-to-bottom yields the whole argument.
**RED baseline (without skill):** produces a topic outline with noun-phrase headings ("Overview", "Solution", "Commercials"), no governing thought, no so-what titles.

**Observed RED gap (Step 2 reasoning):** CONFIRMED. Without this skill, a default LLM response to "help me structure the storyline" will cluster bullet points into thematic sections and label them with noun phrases — "Platform Overview", "Security Approach", "Commercial Model". The output looks organized but carries no argument. There is no governing thought because the model has no prompt to synthesize one. There is no SCQA frame because the model treats the task as information architecture, not narrative. The section headings do not claim anything, so reading them top-to-bottom produces no inference — just a list of topics. The skill closes this gap by requiring the model to first articulate the Answer (governing thought), then build the Situation/Complication/Question that earns it, then group evidence MECE under supporting claims, then write each claim as a full-sentence action title.

---

## Scenario 2 — altitude
**Prompt:** "This deck is for the CIO and their architects. Check the altitude."
**Expected behavior:**
- Asks/confirms target altitude (executive / architect / mixed).
- Flags sections pitched at the wrong altitude for their job.
- Does NOT globally ban why-us or hooks; judges by the section's purpose and asset type.
**RED baseline:** generic "make it clearer" feedback with no altitude concept.

---

## Scenario 3 — action title fix
**Prompt:** "Fix these slide titles: 'Our Approach', 'Architecture', 'Next Steps'."
**Expected behavior:** rewrites each as a full-sentence claim carrying the so-what; verifies the sequence reads as an argument.
**RED baseline:** minor wordsmithing, still noun phrases.

---

## Step 5 GREEN verification note

Re-read SKILL.md + references as if triggered by Scenario 1 (a raw bullet list for a sovereign-Kubernetes platform proposal):

1. SKILL.md workflow line 1 says "state the governing thought in one sentence." A user following the skill immediately asks: what is the single claim this document must land? That forces synthesis before structure.
2. `references/scqa-minto.md` shows the worked sovereign-K8s example with governing thought filled in, SCQA frame complete, and three MECE groups labeled. A model with this context reproduces the pattern for the user's content.
3. `references/action-titles.md` gives five before/after pairs and the read-through gate. The model rewrites noun headings into claims and checks that reading them in order produces an argument.
4. `references/altitude.md` is not triggered by Scenario 1 but is available; no conflict.

Conclusion: following SKILL.md + references closes the RED gap for Scenario 1. The governing thought, SCQA frame, MECE grouping, and action-title read-through are all produced. PASS.

---

## New scenarios (v2 — anti-fragmentation, house spine)

## Scenario 4 — anti-fragmentation
**Prompt:** "This deck has four separate sections all circling the same idea and it feels like everything and nothing. Help." 
**Expected behavior:** runs the anti-fragmentation check — recognizes one idea sprawled across sections that belong together, proposes **consolidating** them into one coherent section with a spine the reader can hold, and notes that a structural re-cut re-enters the Frame+Storyline gate (align on the new spine before rebuilding).
**RED baseline:** polishes each of the four sections in place; never questions whether they should be one.
**RED reasoning:** the default optimizes within the given structure — it tightens prose section by section but has no prompt to ask whether the sections should exist separately at all, so the sprawl survives. This was a real, repeated frustration. Confirmed RED.
**GREEN:** SKILL.md's "anti-fragmentation and the house spine" section and workflow step 3 make consolidating a sprawling argument an explicit, expected move. Addressed.

## Scenario 5 — house spine for a DACH exec audience
**Prompt:** "Structure this for a German board — they want it clear and front-loaded."
**Expected behavior:** offers the **WHY → WHAT → HOW** house spine (situation/what-forces-a-decision → target state, concretely → phased path) beneath the governing thought, notes it's what DACH exec audiences expect, and cross-refers the `voice` skill's localization for tone; does not impose it by reflex where another spine serves better.
**RED baseline:** applies a generic narrative arc with no explicit, front-loaded skeleton.
**RED reasoning:** the default has no notion of an audience-specific house spine or DACH structural expectations; it produces a serviceable but unstructured narrative. Confirmed RED.
**GREEN:** SKILL.md's house-spine subsection defines WHY/WHAT/HOW, ties it to SCQA and to `voice` localization, and cautions against reflexive use. Addressed.
