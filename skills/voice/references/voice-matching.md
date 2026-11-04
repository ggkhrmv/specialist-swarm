# Voice-matching — sound like the author, not like "human AI"

"Make it more human" has a ceiling: it converges on a generic competent voice, which is why
copy can pass a humanization pass and still read as not-the-author. The fix is to match a
**real sample** of the person's writing. Two mechanisms: a voice-sample bank, and an in-asset
voice-reference anchor.

---

## 1. The voice-sample bank

A small corpus of the author's genuine writing, gathered once and reused across assets.

**Sourcing (3–10 samples is enough):** prior decks or POVs they wrote, longer Slack/Teams or
email messages, review comments they left, a blog post or talk transcript. Prefer unedited,
first-person, medium-length prose over polished marketing they may have delegated. (A
hand-built file of the author's real phrasing — the `examples-writing.md` pattern — is exactly
this bank; keep it with the engagement and point the asset's voice bar at it.)

**Extract a voice fingerprint** — describe, don't just collect:

- **Sentence rhythm:** typical length, and how much it varies. Do they run long cumulative
  sentences, or short and direct?
- **Connectives:** what joins their clauses — commas, colons, "and/but/so," subordinate
  clauses? Do they use em dashes at all, and if so how often?
- **Diction:** plain vs. formal; domain jargon they actually use vs. avoid; words they reach
  for repeatedly; words they never use.
- **Stance:** how direct, how hedged, how much first person; do they make claims flatly or
  qualify them?
- **Openings and closings:** how they start a point (straight in? with context?) and how they
  end one (do they wrap with a summary line, or just stop?).
- **What they never do:** the slogans, punchlines, or marketing moves absent from their real
  writing. These become hard bans for this author.

Record the fingerprint in the engagement's **voice bar** (in `asset-forge-state.md`) so it
survives across sessions and every rework pass edits toward the same target.

**A standing profile exists** in [voice-bar.md](voice-bar.md) — the default author for this
installation. Read it when the asset is theirs, and keep it current from every new rewrite. For a
different author, build a fresh profile in the engagement's voice bar using the method here and in
§1b below.

---

## 1b. The rewrite-diff sample — the best source there is

When the author returns **their own rewrite of your copy**, that diff is the richest voice sample
available. Each pair is a controlled contrast: same content, same context, only the voice changed.
It beats any external bank, because a bank shows you what they write and a diff shows you what they
**change**.

**Ask for whole passages, not sentence tweaks.** Scale matters more than volume: across two rounds
of nineteen samples, eight of sixteen recorded rules were invisible until the author rewrote whole
passages rather than single sentences. Compression ratio, reordering to end on the consequence, and
the ban on narrating the artifact ("the table below shows…") only appear at passage scale.

**The procedure:**

1. **Apply their verbatim edits first, unchanged.** Their wording is the target, not an input to
   your judgement.
2. **Derive the fingerprint from the deltas** — the *move* they made, not just the words. What they
   cut, what they renamed, what they shortened, what they never do. Measure the **compression
   ratio**: in one bank the author cut 40–65% of the words while keeping every load-bearing fact,
   which is a harder and more useful rule than any adjective.
3. **State the profile back and get it confirmed before propagating it** anywhere. A fingerprint
   applied across a whole asset on your own reading is a large unreviewed change.
4. **Record it** in the voice bar with the before/after pair that produced each rule, so a later
   session can see the evidence and not just the assertion.

Do not infer a fingerprint from a single rewritten paragraph.

**Two inversions of generic de-slopping**, both learned the hard way:

- **An intensifier or hedge the *author* introduced is not a tell.** Where their own phrasing hits
  the watchlist, **flag it and leave it** — their name is on the asset. Never strip it silently.
- **For a non-native author, keep a slip list** of habitual L2 grammar patterns to **fix silently**
  (comma before "that", agreement after "and", dropped articles) while preserving rhythm and stance.
  Ask once whether they want grammar fixed silently; then do it, and list any change you made beyond
  their wording so they can rule on it.

**Titles are in scope.** Section titles are the highest-visibility copy in the asset — either
include them in the pass or say explicitly that they are excluded and why. Retitle **all or none**:
a partial recut leaves label titles stranded beside claim titles and breaks the read-through. Present
the full set as one before→after table (marking `keep` where unchanged) for approval as a set.

---

## 2. The voice-reference anchor (the in-asset method)

The bank tells you the author's voice in general. The **anchor** is faster and more precise
during a de-slop pass: nominate **one section of the asset that is already in the author's
voice and already sits at zero tells**, and de-slop everything else to match *that*, not an
abstract ideal.

Why it works: matching a concrete, present exemplar is more reliable than matching a
description, and it keeps the whole asset internally consistent in voice.

**How to run it:**

1. With the author, pick the anchor — usually a passage they wrote or heavily rewrote, or the
   cleanest exec section. Confirm it passes the machine tell-scan at zero.
2. Read the anchor's fingerprint (rhythm, connectives, how it opens and closes).
3. For every other section, edit toward the anchor fragment by fragment (see
   `tell-scan.md` for the edit discipline). The question at each fragment is "would the anchor
   have said it this way?" — not "is this grammatical."
4. Re-scan; the whole exec register should now read as one voice.

"High-level is the voice reference — zero tells there; de-slop the rest to match it" is the
compressed form of this method.

---

## Guardrails

- **Never fabricate a voice.** If there is no sample and no clean anchor, say so and fall back
  to the `writing-ruleset` + `humanizer`. Do not invent quirks, typos, or fake informality to
  simulate a person — that is worse than a clean generic voice.
- **Match voice, not errors.** If the author's real writing has habitual grammar slips, do not
  reproduce them in a client-facing asset. Match rhythm, diction, and stance — not mistakes.
- **Voice serves the register.** An author's casual Slack voice is not their exec-readout
  voice. Sample the register you're writing in, or adjust the fingerprint for the register.
