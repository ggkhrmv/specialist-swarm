# Semantic invariants — is the diagram *true*?

Geometry can be perfect while the diagram says something false. Every check here runs **before**
coordinates exist, because each of these errors costs a rebuild rather than a nudge.

Five diagram rebuilds in one engagement came from this file's contents, none from geometry.

---

## 1. Containment and ownership

**Declare which boundary owns every box before you compute a single coordinate.** Write the list:
each box, the domain that owns it, and which side of each frame it sits on.

Placing a box inside the wrong boundary **asserts a false ownership claim**. It is a content error
that a reader will read as fact — "in the current diagram it looks like the tenants have their own
knowledge bases, which is not the case."

Three defaults, each corrected into existence the hard way:

- **Anything shared by multiple consumers sits outside every consumer's frame.** A shared foundation
  drawn inside one consumer's boundary claims that consumer owns it.
- **A hand-off artifact sits outside both parties' frames.** It *is* the crossing, not a member of
  either side. "The approved-work box has to move out of the platform squad box, since it lives in the
  hand-off."
- **A scoping or authorization gate sits *on* the boundary line**, as the membrane. Not inside either
  domain.

Check each box against its frame's stated meaning, not against where it looks tidy.

---

## 2. Arrow sentences

**Write each connector as one sentence — `source · verb · target` — and confirm it is literally true
of the mechanism.** Do this before drawing. Reading the arrows back is the cheapest correctness check
in this file and it catches what nothing else does.

Real misses that passed every geometric check:

- An arrow from a live-state store to a knowledge-and-context box, when the context is *pulled on
  demand* rather than pushed — two different things conflated.
- An arrow from a provisioning step to a live-state store, when provisioning does not write there.
- An arrow to the wrong recipient entirely: the output went to a squad, not to the context box.

Two invariants that catch most of it:

**One concept per box.** If two things have different owners or different lifecycles, they are two
boxes. A store you query on demand is **not** the querier's internal state. Merging them produces an
arrow that cannot be true of either.

**No shortcut edges.** If A changes B, and the actor learns about it via a later read of B, draw
*both* edges — A→B and actor→B. A single A→actor edge asserts a notification mechanism that does not
exist.

And where the diagram assigns items to a taxonomy, check each assignment independently against the
category definition. "Why is this under 'repo and composition'? Shouldn't that be knowledge from the
knowledge base?"

---

## 3. Conditionals cannot be drawn as a single path

**A diagram over-generalises, because one path cannot express a condition.**

If the prose or table says "A runs automatically, B needs approval", a diagram with one approval gate
on the single path asserts that *everything* is gated — which negates the automatic tier and
contradicts the text beside it. Either draw two entry paths, or soften the text. This survived
multiple review rounds in one asset precisely because no check owned it.

So: **restate in one line what the diagram asserts** — who acts, in what order, what is mandatory
versus conditional — and diff that against the prose and tables describing the same rules. Report the
assertion line together with the geometry report, so the author can check it.

---

## 4. Abstraction register

Fix the register before drawing and record it:

- **Capability register** — no product, vendor, repository, or tool names. The diagram describes
  capabilities and information flows: "reads platform status", "semantic layer", "knowledge base".
  Use this whenever the target architecture is **not yet decided**. Naming a tool commits the client
  to a choice nobody has made.
- **Concrete register** — only where the diagram depicts something that exists and is available
  today.

A single asset can legitimately hold both: a mockup of a real interaction stays concrete while the
architecture views stay agnostic.

**Enforce mechanically.** Keep a forbidden-name list and grep the diagram source, reporting the count
("zero tool names"). This is the check that held when the instruction had to be restated to every
subagent.

The underlying rule: **"grounded in the research" means accurate, not named.** Being told to read the
source material is not licence to label boxes with the product names you found there.

---

## 5. Diagram sets

In a multi-diagram section, the same entity carries **the same label and the same colour token** in
every diagram it appears in. That repetition is what makes the set read as one system; two names or
two colours for one thing reads as two unrelated pictures.

**Prefer two legible diagrams at two zoom levels over one merged diagram.** Merging is how altitude
discipline gets lost. Join them by naming the seam in the sentence between them — "that crossing, the
one thing that passes between them, is where the next picture picks up."

Also: **parallel diagrams must label the same object identically.** A full form in one and a short
form in the other is a defect — a reader comparing the two sees two names for one thing. And every
canonical name must appear on the artifact that depicts it; a descriptive label standing in for the
name becomes a de facto third synonym.

---

## 6. Count coherence

Adding or removing a diagram element makes every count word referring to it stale. Grep the number in
**all** its forms — digit and word — across the section standfirst, the figure caption, the
`aria-label`, any deep-dive block, the close or summary rows, and the `<meta>` description. Update the
terminology ledger's load-bearing count.

A fifth box was added to a flow diagram and the deep-dive block still read "four outcomes" a full
increment later.
