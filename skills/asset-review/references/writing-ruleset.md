# Writing ruleset

## Purpose

Write for the actual context.

The goal is prose that fits the medium, the task, and the reader. If it does that well, it will usually read as human-authored as a side effect. Do not optimize for "sounding human." Do not optimize for beating detectors. Both produce worse writing.

Some rules below are prose-quality defaults. Some target common chatbot defaults. They are not the same thing.

## Precedence

When rules conflict:

1. Truth, safety, accessibility, and platform/legal requirements
2. Explicit user instructions
3. Genre and medium norms
4. Core rules
5. Optional watchlists and heuristics

If the user asks for bullets, use bullets. If accessibility, platform rules, or the medium require structure, use structure. If the user asks for a neutral summary, do not force first person or extra stance into it.

## Scope

This document is for drafting and revising text. It is not a reliable method for deciding whether existing text was written by a human or an AI, and it is not an authorship-adjudication tool. In high-stakes settings, provenance beats surface style; see Provenance in high-stakes contexts below.

## Core workflow

1. Identify the medium, audience, reader need, and job of the text.
2. If it is task-oriented, identify the answer or next action that belongs first.
3. If it is long-form, decide the through-line and one concrete example, moment, or case that can carry real weight in the piece.
4. Draft to fit that context, not an abstract idea of "good writing."
5. Run the required checks for the length and stakes of the piece.
6. Cut what sounds generic, ceremonial, over-engineered, suspiciously over-specific, or too cleanly modular.

## Medium routing

- **Chat, comments, replies, DMs, forum posts:** running prose by default. Use lists only when the information is naturally list-like or the user asked for one. Avoid decorative formatting and canned support tone. In plain-text contexts, prefer straight ASCII quotes and apostrophes by default; curly quotes, curly apostrophes, and single-character ellipses often read like pasted or auto-formatted text. They are fine in typeset or publication-facing prose. If text arrived by copy-paste, normalize it before sending. In the same contexts, prefer commas, colons, conjunctions, subordinate clauses, or full stops over em dashes unless the dash clearly earns its keep. Do not replace every dash with a period; if the second thought is still part of the first turn, keep the sentence moving.
- **Email between colleagues:** usually prose first; lists are fine for discrete items, decisions, or action points.
- **Documents, specs, reports, technical writing:** structure is expected. Use headings, bullets, and sequence when they help scanning and precision.
- **Web pages, help centers, UI text, public docs:** put the answer or next action early. Preserve scannability and accessibility: descriptive headings, lists for steps, descriptive link text, plain alt text when images carry information. Do not flatten useful structure just to avoid looking templated.
- **Long-form posts, articles, criticism, retrospectives:** use structure on purpose. Pick an angle. Do not let dates, named milestones, or neat category buckets become the spine unless the user explicitly asked for that structure.

## Safety rails

These are not AI tells by themselves: em dashes, semicolons, "however," competent punctuation, well-formed paragraphs, and the right word even if it appears on somebody's banned list.

Do not invent typos. Do not break grammar on purpose. Do not inject slang, profanity, fake uncertainty, or staged messiness to simulate humanity. No mandatory "actually" turn. No manufactured negativity. No programmatic sentence-length wobble. This is not a preference for short sentences; natural variety comes from the relationship between thoughts, not from alternating sentence lengths by formula.

Do not make text less usable or less accessible in the name of sounding less AI-written. Removing needed headings, lists, descriptive links, citations, caveats, or next steps is not a style improvement.

The recurring problem is regularity and mismatch, not any one feature. Use em dashes where they belong; do not reach for them as a default connective. If you keep using the same punctuation move in the same role, vary it rather than banning it. In casual internet prose, paragraph-after-paragraph em dashes are now a socially recognized AI cue, so prefer commas, colons, conjunctions, subordinate clauses, or full stops unless the dash clearly earns its keep. A full stop is not the automatic replacement; sometimes the fix is to make the relationship between the clauses clearer. For temporary compound modifiers, hyphenate before the noun and usually open after it; do not let the model turn every compound into a hyphenated unit.

## Core rules

**1. Anchor to the actual context before drafting.** Decide what the text is, who it is for, what register it uses, what answer or next action the reader needs, and, in replies, what thread, person, or community it is responding to. A reply that could be pasted into any thread on the same topic will often read generic even if the prose is clean. Keep register stable across the piece.

**2. Fit the format to the medium.** Format is part of register. Over-structuring casual writing makes it feel templated. Under-structuring technical writing makes it harder to use. Match the format to the medium instead of obeying a global ban on bullets, headers, or emphasis.

**3. Prefer concrete specificity over polished generality.** Each substantial paragraph should carry at least one concrete anchor. What counts: a proper noun the reader could look up; a specific number that is not only a date or version; a direct quote; a named decision, moment, or thread; a checkable detail. What does not count: "many/various/several," "in ways that mattered," "the standard X arc," vague intensifiers ("essentially, fundamentally, ultimately"), or milestone names/dates/titles standing alone with no material consequence attached. If the most concrete thing in a paragraph is a name and a date, the paragraph is still probably too generic.

**4. Specificity must be earned.** When writing about real entities, milestones, people, dates, quotes, events, public metrics, planned releases, or numbers, prefer fewer verified facts to many guessed ones. Do not use specificity theater: invented milestone names, suspiciously exact claims, synthetic quotes, or decorative factuality added only to avoid sounding generic. Be especially careful with hidden-mechanism claims: internal logic, unseen motives, back-end behavior. If the reader could not observe it and you cannot verify it, do not narrate it as fact. Do not launder analysis through vague authority ("experts say, observers note, research suggests") unless you can name the source and stay within what it supports. Treat exact quotes, close paraphrases, public metrics, future claims, and causal claims as high-fragility. If the support is weaker, narrow the claim ("coincided with, appeared alongside, was followed by") or cut it.

**5. Use plain words. Allow ordinary repetition. Prefer verbs.** Do not chase synonyms for basic words like problem, change, system, work, or people. Repeat the ordinary word when it is the right word. Prefer "we changed it" to "the implementation of the change," "latency dropped" to "a reduction in latency was observed." Prefer actions happening to people over abstractions being observed by systems.

**6. Cohere through reference and sentence shape.** Use pronouns and continued reference when the reader can track them. Do not restate the full frame in every paragraph. Treat signpost openers ("Furthermore, Moreover, Additionally, Importantly, Notably") as things to justify, not defaults. Let closely related thoughts share a sentence when the relationship is tight: coordination for equal-weight thoughts (and, but, so), subordination for unequal ones (because, although, when, if, which, that), colons or semicolons when the second clause explains or turns the first. A period should mark a real pause, shift, or emphasis, not merely where an adjacent thought arrived. Do not turn every idea into its own sentence for crispness.

**7. Do not perform.** Avoid keynote cadence, mission-statement phrasing, applause-line endings, and ceremonial wrap-ups. Also avoid service-desk tone: no "Great question," "Absolutely," or canned praise unless the situation calls for it; no "I hope this helps," "Feel free to reach out," or canned closers. Start where the answer starts. Stop where the answer stops.

**8. Calibrate confidence, stance, and voice to genre.** Be confident where evidence is strong, explicit where it is weak or interpretive. If the genre carries a visible writer (review, opinion, personal post), let the writer appear. If the genre aims at neutrality (summary, documentation, news-style reporting), do not inject first person or attitude just to feel human. Keep language globally legible and inclusive for public/technical/instructional writing; avoid culturally specific jokes, ableist figures of speech, and slang unless the audience genuinely calls for them.

**9. Show concrete things before generalizing.** Do not open with abstract diagnosis when the reader has nothing concrete to attach it to. This is not a ban on leading with the conclusion in web/docs/email/news; if you lead with the conclusion, make it concrete enough to be useful. Usual order: what happened → where the pattern appeared → what constraint mattered → what failed or changed → what that seems to mean.

**10. Watch regularity.** LLM writing becomes suspicious when its most visible feature is its own regularity. Watch for repeated moves: parallel enumeration and reflexive three-part cadence inside sentences; multiple sentences doing hidden list work; concession-plus-positive rhythm ("not X, but Y; may sound X, but Y"); paragraph-closing type definitions ("the kind of X where Y"); identical paragraph arcs; one neat claim sentence atop every paragraph followed by orderly elaboration; the same punctuation move in every paragraph; the same controlling metaphor returning until it feels too tidy; repeated thesis-like openings; stacked mini-sentences for impact. Three-item parallel lists still count. The fix is not random variation; it is to break the repeated pattern where it starts to dominate. One common over-correction is false crispness: splitting every clause into its own sentence.

**11. Let the thought develop.** Longer pieces should not feel pre-solved. If the prose moves in a perfectly efficient straight line from claim to conclusion, it can feel rushed. Let the thought develop through a concrete example, a noticed detail, a sentence that gathers related material, or a brief doubling-back when the material allows. Development can happen inside a sentence: a cumulative sentence can start with the main claim and add the reason, qualification, or consequence that belongs with it.

**12. Choose structure consciously for longer pieces.** Default genre shapes are not wrong; they are a problem when used by reflex. For task pages, procedures, reference docs, and news briefs, the predictable structure is often clearest. For retrospectives, criticism, and feature writing, the obvious defaults are weak: "starting state → changes → verdict"; one topic bucket per paragraph; one paragraph per named milestone. Choose a through-line instead: one complaint that stopped mattering, one system that changed the rest, one shift in what people had to do, one mismatch between promise and reality, one constraint that started biting. Useful alternatives: thematic instead of chronological, reverse-chronological, perspective-led, counterfactual, opinion-first, single-example-led.

**13. Do not turn a piece into catalog prose or system-tour prose.** If a paragraph is mainly names, milestones, categories, feature nouns, or system labels, it is probably catalog prose. If each paragraph can be summarized with a single label ("background, mechanism, impact, response, ending"), it is probably system-tour prose. Pick one change and trace its consequence. Cross-wire the piece so paragraphs depend on each other instead of sitting like labeled boxes.

**14. Revise by reading and cutting.** Re-read as a first-time reader. Cut anything that is auditioning. Cut sentences whose only job is to announce the next sentence. Collapse paragraphs that restate each other. Replace the most generic clause in the piece with something specific, or delete it. Most edits should make the text shorter, but do not confuse concision with chopping: combining two tightly related sentences can be the cleaner edit when it restores the relationship between thoughts.

## Required checks

For pieces up to ~150 words or three short paragraphs, run checks 1-5, 7, and 10. For longer pieces, run all.

1. **Register fit.** Does the format, punctuation, and structure match the medium and the request? For web/docs/UI, did you preserve scannability and accessibility?
2. **Concrete-anchor audit.** For each substantial paragraph, point to one concrete anchor. In criticism/reportage/analysis, at least one paragraph should be built around a single concrete example or observed consequence.
3. **Fact discipline.** Pick the three most fragile factual claims (dates, milestone names, quotes, close paraphrases, public metrics, future claims, causal claims, motives, hidden-system explanations, vague-authority claims). If you cannot vouch for them, attribute, soften, or cut. If a citation is present, confirm it supports the exact claim.
4. **Source-fit check.** For factual writing, check every exact quote, close paraphrase, public metric, planned event, and causal claim. Do not keep "X caused/drove/proved/tracked with Y" unless the source supports the relationship.
5. **Regularity and sentence-continuity tripwire.** Name the single most repeated visible pattern. If it appears 3+ times or dominates two consecutive paragraphs, rewrite at least one occurrence. Scan for false crispness: neighboring short sentences whose thoughts are tightly related but split apart; combine one pair if a comma/conjunction/colon expresses the relationship more naturally.
6. **Repeated-frame check.** If a central metaphor, contrast, or wording family runs throughout, decide whether it is a useful motif or a too-neat scaffold. Keep it only where it adds force.
7. **Stance and voice.** If the genre expects a visible writer or evaluative stance, state the writer's view in one sentence. If the genre expects neutrality, keep it neutral.
8. **Developed thought.** For any piece longer than four paragraphs, identify one place where the prose pauses, doubles back, or notices a concrete detail off the main line.
9. **Shape and spine.** For any piece longer than three paragraphs, state the organizing principle in five words or fewer and the controlling claim in one sentence. If the shape is basically "starting state → changes → verdict," or paragraphs map one-to-one with milestones, or each paragraph is one labeled bucket, restructure.
10. **Over-correction.** Did you add fake-human moves (typos, slang, forced asides, random fragments, artificial sentence-length targets) just to break a pattern?

These are tripwires, not goals. Use them to catch genericity, visible regularity, false specificity, and modular structure — not to manufacture variation. These checks are for revision, not for visible self-reporting. Do not output the audit unless asked.

## Optional long-form diagnostics

Use only when the required checks are not enough for a longer piece: paragraph spread (vary one if all land at the same sentence count); sentence spread (vary one if all sit in the same length band); sentence architecture (combine a pair of close thoughts if most sentences are simple declaratives); punctuation audit (swap some em dashes/colons/parentheticals for commas or full stops if they keep doing the same job); lead audit; hidden-list audit (rewrite one sentence around a single consequence if 3+ do list work); causality audit (weaken to sequence/correlation where evidence only supports that); motif audit; cadence check (flatten a paragraph that reads like a press release); catalog audit; bucket audit (cross-wire at least one paragraph if each maps to a clean category heading).

## Examples of useful corrections

- **Generic → specific.** Avoid: "The change had broad implications across the team." Prefer: "The change cut review time, but it also pushed more edge cases into the escalation queue."
- **Puffery → observable consequence.** Avoid: "a testament to the team's commitment to innovation." Prefer: "reduced the weekly handoff from three meetings to one written checklist."
- **Hidden mechanism → observable consequence.** Avoid: "The internal logic finally understood what mattered." Prefer: "After the change, obviously irrelevant outcomes stopped showing up in routine cases."
- **Vague attribution → supported claim.** Avoid: "Experts say the redesign improved trust." Prefer: "In the support queue, billing complaints fell after the pricing table stopped hiding plan limits."
- **Causal overreach → relationship restraint.** Avoid: "The redesign drove trust higher." Prefer: "After the redesign, refund questions fell in the support queue." If trust was not measured, do not claim it moved.
- **Catalog prose → argument prose.** Avoid: "First came change A, then B, then C." Prefer: "The important shift was not more pieces; it was that later changes introduced friction where the earlier version let people coast."
- **Choppy → connected.** Avoid: "The term does real work. It names a pattern that was floating unnamed." Prefer: "The term does real work: it names a pattern that was floating unnamed."
- **Period-as-dash replacement → clearer clause relation.** Avoid: "The post would land harder. It should stop at the number and draw the consequence directly." Prefer: "The post would land harder if it stopped at the number and drew the consequence directly."

## Optional audit reference (not bans — places to scan when default LLM writing slips into formula)

**Formula phrases / sentence moves to scrutinize:** "It's important to note that," "It's worth noting that," "When it comes to," "In conclusion," "in today's fast-paced world," "ever-evolving landscape," "at the end of the day," "dive deep into," "embark on a journey," "navigate" as a vague metaphor, "It's not X, it's Y," "Not because X, but because Y," "What matters is…," "The real issue is…," "This is not just…, it is…," "is a testament to," "serves as / stands as" when "is/has" is clearer, "plays a key/pivotal role," "reflects broader / symbolizes / showcases / highlights / underscores" attached to generic significance, vague source laundering ("experts say, observers note, research suggests, critics argue, many believe"), unsupported causality ("drove, proved, showed that, made clear that, tracked with, led directly to"), "X today is not the X it was at the start," "found its feet / found its identity," "proof of concept," paragraph-closing type definitions ("the kind of X where Y"), reflexive triadic rhythm ("clearer, faster, cheaper"), one-thought-per-sentence strings, fake-human hedge chains, forced register lowering, decorative emoji/checkmark bullets in prose, generic-to-the-platform replies.

**Jargon defaults to scrutinize** (use only when plainly right): delve into, tapestry, realm, leverage, harness, foster, empower, unlock, unveil, vibrant, crucial, pivotal, compelling, robust, seamless, holistic, multifaceted, paradigm-shifting, underscore, testament, valuable insights, rich, profound, enhance, showcase, boast/boasts, ever-changing, ever-evolving, ever-growing. The problem is repeated fallback diction, not the existence of any one word.

**Formatting artifacts in plain text:** smart quotes, curly apostrophes, single-character ellipses, other copy-paste artifacts that don't fit the medium.

**Compound-modifier hyphenation:** hyphenate temporary compounds before the noun ("a well-known author, a high-quality service, a long-term plan"); open them after a linking verb ("the author is well known, the plan is long term"). Watch predicative over-hyphenation ("is well-known"), -ly adverb compounds ("highly-qualified"), reflexive ever- compounds, and set phrases where the hyphen adds nothing ("high school, ice cream"). Keep hyphens that prevent ambiguity or are conventional ("state-of-the-art, cost-effective, user-friendly"). The problem is the reflex, not the mark.

## Provenance in high-stakes contexts

If authorship matters, stronger signals than surface style include: draft history, revision history, citations that actually support the claims, notes/outlines/source traces, and disclosed AI use when it occurred. Use surface-style checks to improve prose; use provenance to support authorship claims.

---

**How this fits the skill:** this is the authoritative humanization standard for `asset-review`, run with EQUAL weight alongside the `humanizer` skill (when installed). The ruleset is a writing philosophy; `humanizer` is mechanical pattern detection. Both run; neither replaces the other. Do not optimize for "sounding human" or for beating detectors.
