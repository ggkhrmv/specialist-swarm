# Evidence you produce yourself — the claim side

When a claim rests on the client's own data (tickets, repositories, logs, chat, config) rather than on
an external source, you are not citing evidence — you are **producing** it. That makes you responsible
for the properties below before the number reaches the page.

This file covers what makes a produced number *publishable*. The analysis machinery — answer keys,
error propagation, window discipline, replication, fan-out contracts — lives in the `evidence` skill.

## Coverage denominator

**State what fraction of the real population your corpus covers, and what it excludes, with every
rate.**

A rate computed over whatever data was locally convenient is not a rate; it is a sample of your own
tooling. In practice a first pass saw 17 of 130 repositories — 13% of the estate — and missed the
single largest source entirely. The second pass covered 130 of 130, and the objection closed either
way, because the coverage was stated.

Say explicitly whether coverage could change the *direction* of the finding, not just its magnitude.
Close this before a reviewer opens it.

## The single-instrument fallacy

**A count drawn from one system of record measures what that system captures, not what happens.**

Before you use a low count to weaken, demote, or drop a claim, ask what channel the work would flow
through if nobody filed a record: artifact repositories (commits, infrastructure-as-code, config),
chat and side channels, or a second tracker. **Absence in the primary instrument is a finding about
the instrument** until you have checked at least one independent channel.

This inverted a headline finding once. A 6.1% ticket rate looked like a small problem; the user
objected that the work happened by default and nobody filed tickets for it. The declarative
configuration repositories showed 1,940 declared resources against 31 requests — the opposite
conclusion. The post-mortem: *"I treated a low ticket count as a small problem, when it actually
meant the gap was being absorbed silently."*

**When a practitioner's lived experience contradicts your number, the number is the suspect.**

## Negative control and the reverse direction

**No rate goes into an asset alone.** Ship it with both:

- **A negative control** — the same measurement over a population where the rate *should* be low, and
  it is. Ideally produced by a channel the classifier never saw. This is what makes an evidence block
  unattackable: a red team's verdict on one such block was *"I have no attack on it that does not
  require alleging fabrication."*
- **The reverse direction**, for any asymmetry claim, on explicitly correct denominators. A rate whose
  reverse is equal or larger is not a floor — it is noise. Three candidate metrics were killed this
  way (17 forward vs 21 reverse; 4 vs 9; 2.2% vs 4.1%), and one near-miss inverted to 0.5× on correct
  denominators after looking publishable.

## The robustness triad

Before a rate enters the asset, test three sensitivities and report them:

- **Unit of analysis** — does the number move if you count the other natural unit? One headline moved
  8.3% → 24.9% depending on whether it counted commits or pull requests.
- **Collection artefact** — does it move with a tooling or process policy unrelated to the claim? One
  rate was 49.2% where a branch name survived and 8.2% where it did not: a 6× swing driven purely by
  a branch-deletion policy.
- **Concentration** — what share of the sample comes from one entity? A group-level claim resting on
  46% from one person, or on n≈4, is not a group-level claim.

A rate that swings materially on any of the three is a caveat, not a headline.

## Robustness cut

Publish the headline under a **deliberately conservative** definition as well as your own (74% → 57%).
Volunteering the unflattering version of your own number is read as evidence that you treated the rest
the same way.

## Two convergent estimates

When two estimates of the same quantity are derived by methods sharing **no inputs**, compute and
publish the convergence — it turns a modelling assumption into an evidenced gap. State that the inputs
are disjoint, or the convergence proves nothing.

The independence test is not optional and it is easy to fail: two derivations that share a scoping
input are **not** independent, and a headline that is merely their midpoint should say so. "We took the
midpoint" is stronger than a verb that hides it.

## Figure provenance

**Every number that appears in the asset comes from a named, committed script that can be re-run** —
never hand-typed into the markup. When a figure changes, edit the script and re-run it. After any
figure rework, re-run *all* figure-producing scripts and confirm they still reproduce.

A convenient rounded intermediate you typed yourself is a fabricated claim, however small. Caught in
practice mid-edit: *"The 0.75 quarters I put in is a number I invented — exactly what I told you I'd
avoid."*

## What decision does this fund?

Before a finding enters the asset, state **the decision it funds** and **the objection it invites**.

A finding can be true, measured, and rigorous and still fail, because the reader's natural response is
a cheap internal fix rather than your ask. "Your traceability is poor" invites "so fix your commit
messages" — it does not fund anything. Prefer a finding whose implication *is* the ask; park the rest.

## Measurement-gap-as-finding

When the client's own systems cannot evidence a claim the asset needs, **publish the gap instead of a
proxy**: state what cannot currently be traced, name the two or three cheap instrumentation fixes, and
scope a first-phase measurement track with a baseline date.

This is stronger than a defensible-sounding proxy, and it converts a dead end into a funded
workstream. Use it only when the gap genuinely blocks a decision the client cares about.

## Estimating a number nobody measured

Never pick an estimated figure by judgement alone. Build a small reproducible model: a script plus a
**written assumption ledger** with named sensitivity levers. Derive the figure at least two ways. Get
the model signed off *before* it touches the asset.

Then publish at the precision the model supports — decimals on a modelled figure assert a measurement
you do not have. Round them.

## Refuse the flattering number

Where a figure would favour your own case and you cannot measure it honestly, **state that you are not
counting it, and why**. Counting a benefit produced by the thing you are asking to fund is circular,
and saying so out loud costs one sentence.

Three separate reviewer personas independently named a refusal of this kind the single most credible
sentence in an asset. Do not let a later polish pass remove it — this and the negative control are the
first things a tidying edit deletes.
