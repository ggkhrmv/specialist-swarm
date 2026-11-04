# Operational de-slop — the marked-up-file method

Prose skills tell you *what* an AI tell is. This file is about *operating* on a real
marked-up artifact (HTML, SVG, Markdown) so the de-slop pass is repeatable and provable.
Three things break here that don't break on plain prose: the tells hide inside HTML
entities, the naive edit method silently fails, and the right target differs by register.

---

## 1. The fragment-edit discipline (read this before you edit anything)

**Never replace a whole paragraph with a literal string in marked-up copy.** It silently
fails and wastes a pass. Reasons:

- **Mixed entity encodings.** The same visible em dash may be a literal `—`, `&mdash;`, or
  `&#8212;` on different lines — sometimes within one file. A whole-paragraph literal
  match fails on the first character that isn't the encoding you typed. (This exact failure
  cost a rebuild: a whole-paragraph exact-match batch failed on mixed `—` / `&mdash;`.)
- **Invisible whitespace / soft wraps / nested tags** inside the paragraph break the match.

**Do this instead:** edit the **smallest unique fragment** that carries the tell, and match
the entity variants explicitly. Match em dashes as a class, never as one literal:

```
(?:—|&mdash;|&#8212;|&#x2014;)
```

Change one fragment at a time. If you must batch, batch by fragment-regex, not by
whole-paragraph literal.

---

## 2. Register-awareness — set the target before you scan

The target is not "zero tells everywhere." It is register-dependent:

- **Exec / high-level copy** (hero, section titles, the pitch view): target **zero**
  watchlist hits. This is where AI voice is most damaging and most visible.
- **Technical / low-level copy** (architect view, deep-dives): keep the technical register.
  `day-2`, `reconciles state`, `reads state back`, `bidirectional`, `admission webhook` are
  precise domain terms here, **not** tells. Do not flatten them.
- **Scannable fragments** — table cells, column headers, stat-tile captions, chips, eyebrows,
  axis and diagram labels: these are **not prose**, and a voice pass does not apply to them.
  Keep them as short noun phrases, parallel in form and comparable in length across a row or
  column. Turning a cell into a clause destroys scannability even when the resulting sentence
  reads more human — in one delegated pass three table cells had to be reverted for exactly
  this, and a fourth was left ending on a dangling fragment. Put them on the do-not-touch list
  before the pass and re-check them after it.

Decide the register map first (which sections are which), then scan each against its own bar.
A nominated **voice-reference anchor** (see `voice-matching.md`) is usually exec copy that
already sits at zero — de-slop the rest to match it.

---

## 3. The tell watchlist (grep-able)

These are the patterns that recurred in real asset work, on top of the `humanizer` and
`writing-ruleset` catalogs. Each is a *scan target*, not an automatic ban — confirm each hit
is actually a tell in context before editing.

**Structural / rhetorical tells (the ones that survived generic humanization):**

| Tell | What it looks like | Fix |
|---|---|---|
| Balanced-antithesis slogan | "Intent in. Governed infrastructure out." · "the more X, the more Y" | Say the thing plainly in one clause. |
| `X, not Y` negative parallelism | "matches intent, not just schema" · "not an afterthought" · "not fire-and-forget" · "not the cluster directly" | State what it *is*; drop the foil. |
| `not just … but` | "not just faster, but safer" | Keep one claim; cut the escalation. |
| Manufactured punchline | "None of this is theory." · "This isn't a trick." | Delete. The evidence is the punchline. |
| Neat closer / applause line | a tidy one-liner that wraps a section | End on the last real point. |
| Signposting openers | "Furthermore," "Moreover," "Importantly," "Notably," | Justify or cut. |
| Rule of three / triadic | "clearer, faster, cheaper" · three-item lists by reflex | Break the cadence; keep what's load-bearing. |
| `X becomes Y` transformation cadence | "provisioning becomes a conversation" | Describe the concrete change. |
| Em-dash-as-default connective | em dashes doing comma/colon/period work, repeatedly | Vary: comma, colon, subordinate clause, full stop. |

**Vocabulary watchlist (scan, don't blanket-ban):** leverage, unlock, unlocks, seamless,
robust, holistic, empower, foster, harness, elevate, streamline, realm, tapestry, testament,
underscore, pivotal, crucial, compelling, ever-evolving, ever-growing, "makes it real",
"at its core", "under the hood" (as filler).

**Strategy-jargon cluster (a separate register of tell).** These survive generic humanization
untouched, because they read as consultant-competent rather than as machine-written — which is
exactly why a senior reader clocks them: *flywheel, bet(s), de-risk, compound(s), substrate,
unlock / "value unlocked", "multiplies capacity", "pays its own way", north-star (as filler),
agent-ready, welds / wires together*.

Two operating rules for this cluster:

- **Rewrite, do not delete.** The underlying idea usually earns its place; the word is the
  problem. "Flywheel" → "keeps improving, rather than a build that finishes once." Deleting the
  sentence loses a real claim.
- **Refresh from live external registers** at the start of a de-slop pass rather than relying only
  on the bundled list. Fetching two public AI-jargon registers in one pass sharpened the watchlist
  materially — it surfaced copula-avoidance, transformation cadence, and catalogue prose that this
  file did not yet name.

---

## 4. The machine tell-scan (the exit check)

Run grep over the visible copy and count residual hits **per register**. This is what makes
"de-slopped" a claim you can back, not a feeling.

### Prepare the extract first — a naive tag-strip lies

Three false-positive classes wasted rounds in four separate sessions. Fix them before scanning:

- **Split at block boundaries and insert a terminator.** Walk the DOM (or regex block-level tags)
  and end each of `p`, `li`, `td`, `th`, `h1`–`h4`, `figcaption`, and any component wrapper with a
  full stop. Adjacent inline and stat elements carry no terminal punctuation, so a naive strip
  concatenates them into a single fake mega-sentence and every length check fires. In practice this
  produced a "79-word sentence" that was three stat tiles, and one phantom persona finding
  reporting perfectly good copy as garbled.
- **Exclude embedded base64 before any grep.** A font blob matches almost any three-character
  token, and a naive grep over it is pathological — one hung and had to be killed. Strip the
  `<style>`/base64 region, or extract visible text in a script rather than grepping the raw file.
- **Partition registers per block, not by line range.** Walk the DOM and partition by the
  view-scoping class. A line-number heuristic mislabels architect-only copy as exec copy — this
  recurred three times in one session and each time cost a hand inspection.

Also: `<text>` inside SVG and `aria-label` values are **not** prose for length checks, but they
**are** prose for claim wording (see below). Classify a hit before editing it.

Then adapt the target file and the extraction (for HTML, scan the body copy; exclude `<style>`,
`<script>`, class names, and comments — a `leverage` in a CSS class name is not prose).

```bash
# Em dashes in visible copy (all encodings) — expect 0 in exec/high-level copy
grep -nE '(?:—|&mdash;|&#8212;|&#x2014;)' FILE

# Structural-tell sweep
grep -niE '\b(not just|isn'\''t just|none of this is|this isn'\''t a)\b' FILE
grep -niE ', not [a-z]' FILE          # X, not Y antitheses
grep -niE '\b(furthermore|moreover|importantly|notably|additionally)\b' FILE

# Vocabulary watchlist
grep -nioE '\b(leverage|unlocks?|seamless|robust|holistic|empower|foster|harness|elevate|streamline|realm|tapestry|testament|underscore|pivotal|crucial|compelling)\b' FILE | sort | uniq -c | sort -rn
```

**Reporting the result.** State the count per register, e.g. "high-level: 0 watchlist hits,
0 em dashes in visible copy; low-level: 4 em dashes (all in technical prose, kept), 1
`bidirectional` (domain term, kept)." A clean exec register with a still-technical low-level
register is the correct end state, not a failure.

**Caveat.** grep flags *candidates*. It cannot tell a genuine tell from a domain term or a
quotation. Confirm each hit in context; the count is a floor for attention, not a verdict.

---

## 5. Diff-scoped scanning during Build and Rework

The scan is not only an exit check. Run it **scoped to your own additions at the end of each edit
batch**, because the normal failure mode is re-violating a ban while enforcing it: six
self-introduced connective em dashes on an asset whose locked ban list forbade exactly that, and one
of them survived an entire session before being caught in a figure caption.

The method:

1. **Back up the file before the increment.** `cp asset.html backups/asset.html.<timestamp>-<purpose>`
2. Scan **the lines you touched**, not the whole file.
3. **Attribute every hit** as mine versus pre-existing, by diffing against that backup. Report as
   **before → after per register** — "exec em dashes: 11 before → 11 after, none are mine (title
   metadata, mockup, SVG labels)".
4. Fix yours immediately. **Report a pre-existing hit and leave it** — never silently edit prose the
   author did not ask you to touch.

Without the attribution step a whole-file count reads as a false regression, and you end up
"fixing" the author's own copy.

The bans apply to every line you write, including figure captions, `aria-label`s, diagram `<text>`,
and the HTML `<meta>` description — the low-visibility surfaces are where they survive longest.

---

## 6. One claim, six encodings

In a marked-up asset a single claim can exist in up to six places: **visible prose · a table cell ·
an SVG `<text>` label · an `aria-label` or `<title>` · a figure caption · a CSS class or id**.

When you change or soften a claim, **enumerate its encodings and change them together**. A softened
claim survived in a diagram label and an `aria-label` after the prose was fixed, on two separate
occasions, and a stale SVG label contradicted the edited prose beside it.

When a scan reports a residual hit, classify it first: visible prose, accessible text, or a class
name. The first two are prose you must edit. Class names and ids may keep the old vocabulary — they
are invisible — but **say so in the report** rather than leaving the hit unexplained. Same
discipline for structural comment markers after a block move.

---

## 7. Delegating the pass

When a subagent runs the voice pass on a live asset, the brief names: the file, the **exact in-scope
sections**, the voice bar or anchor to match, and a **protected-figures list** — the numbers and
canonical names that must survive verbatim.

On return, verify rather than accept:

- **Diff against the pre-pass backup** to prove scope discipline ("only the two in-scope sections
  changed; CSS, JS and SVG byte-identical").
- Confirm every protected figure is unchanged.
- Re-run the tell-scan **yourself** — a delegated zero-hit claim was wrong once, with 1 exec and 5
  technical hits present.
- Read the actual result, and check the scannable-fragment register (§2) survived.

Separate "introduced by this pass" from "pre-existing outside scope" when reporting residual tells.
A whole-file count otherwise reads as a regression the agent did not cause.
