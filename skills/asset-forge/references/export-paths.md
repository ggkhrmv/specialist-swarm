# Export paths — PDF and single-view variants

Exporting a self-contained HTML asset looks trivial and is not. Two engagements invented this from
scratch at roughly a dozen turns each, and both hit failures that a naive print produced silently.

## Read the artifact's own print CSS first

**Before anything else, read the asset's `@media print` block.** It usually already encodes which view
should export — the author wrote it for a reason — so inspect it before asking the user what they want.

It is also where the worst failure hides. One asset's print rule was:

```css
@media print { body[data-view] .architect-only { display: block !important; } }
```

Correct for the full export. For the exec-only export it would have **silently leaked all six evidence
blocks into the executive PDF** — the one thing that export existed to prevent.

## Drive the asset's own view API

Generate each variant by calling the asset's own view function (`setView()` or equivalent) and
injecting the print CSS that variant needs **at render time, in the export script**. Never hand-edit
the view state, and never edit the shared source file to produce one export — the next export inherits
it.

## The specificity trap

An injected override must **match or exceed the source rule's selector specificity**. `!important` on
both sides does not save you: `body[data-view] .architect-only` (0,2,1) beats a plain
`.architect-only` (0,1,0) regardless.

This shipped a wrong export once, and the render *looked* right. It was caught by an expected-delta
check, not by eye:

> "The exec PDF (16374px) is barely shorter than the full one (16598px). Hiding all the architect
> blocks should have cut far more than ~220px."

So: **predict the expected delta** — height, page count, byte size — and investigate any shortfall.
A suspiciously small delta is the signature of an override that did not apply.

## Verify by counting, not by looking

Confirm the toggle applied by **counting elements in the DOM**: present versus visible under print
emulation, reported as `0/N visible`. Eyeballing a render passed a broken export.

## Pagination is a choice about the artifact

There is no universal answer — pick deliberately by what the artifact *is*:

- **A scrolling presentation site or web one-pager** exports as **one continuous page sized to the
  measured document height**. Paper pages cut sections and diagrams mid-block.
- **A slide deck in HTML** exports **paginated** — A4 (or the deck's own slide geometry), one slide per
  page. That is the artifact's native unit, and a continuous page destroys it.

State which model you used and why.

## Prove the PDF is not blank

A valid header and a plausible byte count prove nothing. **Rasterize the PDF back to an image and look
at it.**

Text extraction is not a substitute: brand fonts subsetted into the file use glyph-index encoding with
no ToUnicode map, so extraction returns false negatives on everything and a correct PDF reads as empty.

Page-count pitfall: grepping `/Type /Page` also matches `/Type /Pages`, the tree root. Expect an
off-by-one.

## De-UI-ify the artifact

A paper artifact has no interface. Suppress view toggles, nav, and hover affordances. Then handle
cross-view pointers, which become dead instructions:

- A pure pointer ("Switch to the Architect view for the evidence") → **drop it**.
- A pointer that carries real content behind a UI prefix → **keep the content, drop the prefix**.

Re-run the dual-view reference sweep from `build-validation.md` after the export: dropping a layer turns
every reference into it into a dead end.

## Register and stale-mark

Save the export as a **re-runnable script**, and record each variant in the state file's artifact
registry with the asset version it was built from. Mark every export stale on the next increment, and
flag any superseded file left in the output directory — a pre-revision PDF that circulates is worse
than no PDF.

Name variants by audience, and state in the handoff which layer each one carries and which placeholders
(if any) are baked into it.
