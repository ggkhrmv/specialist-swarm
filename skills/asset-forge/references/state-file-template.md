# State-file template — asset-forge-state.md

Write this file at the end of Intake. **Then keep it as a living log** — update it at every phase boundary and every rework increment, not once. Conversation notes do not persist between sessions; this file is what carries the engagement forward, and in practice it becomes the single most-used artifact of the whole workflow.

Place `asset-forge-state.md` in the working directory for the engagement (the folder where the asset lives).

## How to keep it

- **The decision log, reviewer log, and change log are append-only.** Add dated entries; do not overwrite history. A decision that was reversed is recorded as a new entry that supersedes the old one, so the reasoning is not lost.
- **The status tables and open-items queue are live** — edit them in place to reflect the current truth.
- **Convert relative dates to absolute** ("next week" → the date) so the log still makes sense in a later session.
- **Multi-artifact engagements** (a system of cross-linked files — e.g. an offering site + a diagnostic + a capability map) use the artifact registry to track each file and the cross-links between them.

### Keeping it legible at scale

Append-only preserves history and destroys legibility. A real engagement file reached 136 KB, 571 lines
and 38 top-level sections against a schema of about twenty — with two pairs of same-named sections
coexisting in the body, one superseding the other. Three rules keep it usable:

- **Regenerate the `Current truth` block at the top, in place.** It is the one part of the file that is
  not append-only. A new session should read thirty lines to know where things stand, not five hundred.
- **Move superseded sections below a `## Superseded` divider** at the end of the file, with the date and
  what replaced them. Never leave two same-named sections in the body — the reader cannot tell which is
  live.
- **Keep the user-decision queue separate from the working queue.** Items only the human can rule on,
  each with what it blocks. A decision waiting on the author is not a task.

When a section outgrows its slot — the voice bar in particular, which reached a sixty-line profile in
practice — move it to its own file and leave a pointer.

---

## Schema

```markdown
# asset-forge-state.md

## Current truth  ← NOT append-only; regenerate in place every increment
- Version: [current asset version] · Phase: [current phase] · Date: [today]
- Positioning frame: [one line, as locked]
- Governing thought: [one line, as locked]
- Published figures: [the load-bearing numbers currently in the asset, with source and date]
- Next action: [the one named next increment]
- Blocked on: [what is waiting on the author, if anything]

## Brief + intel summary
[2-5 sentences: what the engagement is, who the client is, what is known about their situation
and priorities, from both the formal brief and side-channel intel. Note what is still unknown.]

## Asset type
[One or more of: RfQ/RfP response | pitch deck | point of view | readout | internal briefing |
presentation site | capability map / maturity assessment | multi-artifact system | other.]

## Positioning frame  ← locked at Gate 2, before Build
[One line: what this asset is FOR and what it is NOT — the frame it takes.
e.g. "Positioned as an AI enabler/accelerator, NOT a guardrail/governance pitch."]

## Governing thought  ← locked at Gate 2, before Build
[The single declarative sentence, once approved.]

## Stakeholder map
| Role | Name / description | Known? |
|---|---|---|
| Economic buyer | | |
| Technical buyer | | |
| Coach | | |
| Blocker | | |
| Practice / capability lead (whose name is also on it) | | |
| Evaluators (if tender) | | |

## Submission mechanics (tender responses only)
- Deadline · Page/word limit · Mandated template · Submission format · Clarification window · Scoring criteria

## Qualify decision
- Go / No-go · Win probability (high/med/low) · Walk-away criteria triggered (list) · Rationale

## Chosen scope option
[A / B / C or equivalent — one line on what's in and what's out.]

## Win themes
| Theme | Proof point |
|---|---|

## Voice bar  ← the locked voice/de-AI rules for THIS asset (fed to the `voice` skill)
- Voice sample / bank: [pointer to the author's phrasing corpus, e.g. examples-writing.md]
- In-asset voice-reference anchor: [which section is the zero-tell exemplar to match]
- Author fingerprint: [1-3 lines: rhythm, connectives, what they never do]
- Hard bans for this asset: [the specific tells to keep out — e.g. em dashes in visible copy;
  X-not-Y antitheses; manufactured punchlines; balanced-antithesis slogans; signposting]
- Market/localization: [e.g. DACH/German exec structure — WHY/WHAT/HOW, source every number]
- Register map: [which parts are exec (target: zero tells) vs technical (keep the register)]

## Terminology ledger  ← canonical names; inventing synonyms is banned; enforced in Review
| Concept | Canonical name (use everywhere) | Do NOT call it | Load-bearing count/fact |
|---|---|---|---|
| [e.g. the platform capability groups] | [e.g. "the six dimensions"] | ["six jobs", "six pillars"] | [e.g. exactly six] |

## Locked rulings (append-only)  ← do not relitigate; passed verbatim into every review board
| Ruling | Scope | Rationale | Exceptions the author DID accept | Date |
|---|---|---|---|---|
| [e.g. present tense is deliberate vision voice for this asset] | [hero, cards, close, titles] | [author's reasoning] | [e.g. current-state capability claims still get honest tense] | |

A ruling belongs here when a review board keeps raising a finding the author has already decided. Pass
the whole table into every persona dispatch: *these are settled — do not re-raise them; if you believe
a ruling is now wrong because the asset has changed, say so once and say why.* Report in the board
output whether any ruling was relitigated. Without this, a dominant-cluster finding returns every
round and the board's credibility decays.

Also record here: content the author ruled **out** of the asset (keep the underlying evidence in the
backing analysis with a note on why it is not published), and any **off-page answer** prepared for a
question the audience will ask even though it stays off the page. An option the author did **not**
select is itself a decision — log it.

## Evidence-continuity map  ← what diagrams, mockups and captions may claim
| Element as labelled in the asset | Real backing thing | Verified current state | Honest ceiling |
|---|---|---|---|
| [canonical label used everywhere] | [the actual system/repo/process] | [step on the maturity ladder] | [e.g. "target, not built"; "proven once in a spike, not production"] |

Every diagram label, mockup line, and figure caption draws from this table. It is what stops a later
polish pass from silently re-upgrading a spike into a capability, and it is the cheapest way to keep a
multi-artifact system consistent. Maturity ladder in `positioning/SKILL.md`.

## Constraint register  ← assumptions about what the data can and cannot show
| Constraint | Tested by | How | Date | Blocks |
|---|---|---|---|---|
| [e.g. "nothing in the corpus measures effort"] | [who] | [the actual check] | | [which claim or ask] |

A recorded constraint is an **assumption**, not a fact. One such entry was false — over half the items
carried the field in question — and it had capped the asset for days and blocked a reviewer's top ask.
Any constraint blocking a headline claim or a reviewer's top ask is re-tested before it is accepted a
second time. When one falls, sweep the asset *and* this file for prose that rested on it.

## Artifact registry (multi-artifact systems)
| File | Role | Audience | Status | Built from version | Cross-links to |
|---|---|---|---|---|---|

Exports (PDFs, single-view variants) are derived artifacts: record the asset version each was built
from, and mark them stale on every increment so a pre-revision file cannot circulate.

## Approved storyline
- Governing thought (above) · Storyline file · Approved by user (yes/pending) · Section spine

## Selected reviewer personas
[The personas chosen for asset-review and why each is live for this asset.]

## Phase status
| Phase | Status | Notes |
|---|---|---|
| Intake | not started / in progress / complete | |
| Qualify | | |
| Frame | | |
| Storyline | | |
| Build | | |
| Review | | |
| Rework (loop) | n/a until first review returns | current increment / version |

## Decision log (append-only, dated)
| Date | Decision | Rationale | Supersedes |
|---|---|---|---|

## Reviewer log (append-only) — every batch of feedback that came in
| Date | Reviewer | Thrust of feedback | Triage (accept/reject/defer) | Status |
|---|---|---|---|---|

## Change log (append-only) — one entry per build/rework increment
| Date | Version | What changed | Validated? |
|---|---|---|---|

## Open items / next increments (live queue)  ← work you can do
- [ ] [item] — blocks: [what] — owner: [who]

## Awaiting the author (live queue)  ← decisions only the human can make
- [ ] [the decision] — blocks: [what it holds up] — presented on: [date]

Keep this separate from the working queue. A decision waiting on the author is not a task, and mixing
the two hides the ones that are actually blocking. Every deferred (`D`) review finding lands here until
it has a recorded ruling.

## Parked content
[Content cut but possibly reusable, with a pointer to where it's stored, e.g. v6-parked.md.]

## Open gates
[Any gate not yet passed, with the specific blocking condition.]

## Superseded
[Sections moved here when replaced, each with its supersede date and what replaced it. Nothing in the
body above should have a same-named twin.]
```

---

## Filled example (abridged)

Based on a sovereign Kubernetes platform RfQ, showing the living-log sections in use.

```markdown
# asset-forge-state.md

## Brief + intel summary
[CLIENT] is running a formal RfQ for a sovereign, self-hosted open-source container platform
to replace 11 public-cloud managed clusters. The pre-bid call with the head of infrastructure revealed the real priorities
are control-plane sovereignty and operational continuity during transition. Evaluation panel
composition unknown.

## Asset type
RfQ/RfP response

## Positioning frame
Positioned as a sovereignty-and-continuity partner who leads the engagement — NOT a
lift-and-shift vendor responding line-by-line to the checklist.

## Governing thought
[CLIENT]'s platform needs a sovereign, fully open-source foundation — and the right way to get
there starts with a structured assessment, not a premature build commitment.

## Voice bar
- Voice sample: none supplied; using ruleset + humanizer only. Flagged to author.
- Register map: exec summary + cover = zero tells; technical annex keeps K8s register.
- Hard bans: no "unlock/leverage/seamless"; no em dashes in the exec summary.
- Market: DACH — WHY/WHAT/HOW spine, every number sourced.

## Terminology ledger
| Concept | Canonical name | Do NOT call it | Load-bearing |
|---|---|---|---|
| The delivery model | "Assessment-first, phased" | "land-and-expand" (internal) | 3 phases |

## Phase status
| Phase | Status | Notes |
|---|---|---|
| Intake | complete | Panel composition TBC |
| Qualify | complete | Go; override risk flagged (we initially declined) |
| Frame | complete | Win themes agreed; frame locked (enabler-of-sovereignty) |
| Storyline | complete | Governing thought approved 2025-09-19 |
| Build | in progress | Document path; outline approved |
| Review | not started | |
| Rework (loop) | n/a | — |

## Decision log (append-only)
| Date | Decision | Rationale | Supersedes |
|---|---|---|---|
| 2025-09-17 | Scope Option B (assessment-first) | Avoids overcommitting on build before baseline | — |
| 2025-09-19 | Frame = sovereignty partner, not lift-and-shift vendor | Pre-bid intel: they want a lead, not a responder | — |

## Reviewer log (append-only)
| Date | Reviewer | Thrust | Triage | Status |
|---|---|---|---|---|
| 2025-09-22 | MD (internal) | "Commercial section reads open-ended" | accept | applied v1.1 |

## Change log (append-only)
| Date | Version | What changed | Validated? |
|---|---|---|---|
| 2025-09-22 | v1.1 | Added not-to-exceed + phase gates to commercial section | yes |

## Open items / next increments
- [ ] Confirm submission format — blocks: final formatting — owner: procurement contact
- [ ] Panel composition — blocks: persona tuning — mitigation: default exec/technical/commercial

## Open gates
- Review gate: not passed. Blocking: Build not complete.
```
