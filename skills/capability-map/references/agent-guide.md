# The embedded agent guide + neutral scoring method

Every capability map opens with an HTML-comment guide that lets an AI agent (or a person) fill
it out correctly without any outside instructions — a small skill baked into the artifact. It
must be fully **agnostic**: encode the *method*, never baked client/industry examples, and never
a `--` sequence (that closes an HTML comment).

## Template (adapt the specifics; keep it agnostic)

```html
<!--
============================================================================
  AGENT GUIDE  ·  how an AI agent (or a user) fills out this assessment
============================================================================

  WHAT THIS FILE IS
  A capability and maturity assessment for <domain>. It is engine-agnostic.
  This file is a BASE template; treat it as read-only.

  THE WORKFLOW (never edit the base)
  1. Copy the base to a client-specific file, e.g.
       cp <base>.html client-<name>-assessment.html
     Work only in the copy, so the base is never lost.
  2. Set values and notes directly in the copy's source (see WHAT TO EDIT).
     State is baked into the source, so opening the copy shows the scores and
     notes already filled in, and they travel with the file.
  3. Hand the finished copy to the architect or client. They can still adjust
     anything live in scoring mode.

  WHAT TO EDIT (all in the <script> block below)
  * MODEL     : each capability has cur: and tgt: (integers 0 to 4). cur is
                today's maturity, tgt is the goal.
  * NOTES     : one entry per capability id. Write WHY you set current and
                target. Notes render read-only in the presentation view and as
                editable fields in scoring mode.
  * GREEN_CUR : only if the copy is presented in the greenfield starting point.

  THE 0 TO 4 SCALE
  0 Absent · 1 Initial · 2 Developing · 3 Established · 4 Leading.
  Every capability spells out each level in DETAIL[id].rubric below.

  HOW TO SCORE (the method, not instances)
  Judge each capability against the client's real constraints, scoring along
  neutral axes:
    - environment / stage (dev vs regulated production)
    - compliance / regulatory exposure
    - operating model / responsibility split (platform team vs consumers)
    - risk / autonomy tolerance
    - scale / tenancy
  Set tgt as a business choice, not a reflex to 4. Reserve 4 for genuine
  differentiators; default most to 3. Record the reasoning in NOTES.
-->
```

## Rules for the guide

- **Agnostic method, no instances.** Do not bake in a specific client, industry, regulation, or
  vendor scenario. Encode how to reason, so the base is reusable across clients.
- **No `--` anywhere in the comment** — it prematurely closes the HTML comment. Validate this.
- **Match the neutral axes to the scoring UI** so an agent and a human reach the same scores.
- **A copy-to-clipboard agent prompt** (an agnostic prompt a user can paste to an agent) is a
  useful addition, mirroring the offering's user-manual view.

## Fold-back

When a client returns an exported JSON, the agent folds it into the copy's source (`MODEL`
`cur`/`tgt`, `NOTES`) so the baked state matches the live state, then re-validates.
