# Action Titles

## What an action title is

An action title is a full declarative sentence that states the claim the slide or section proves. The reader should be able to read the title and know what you are arguing — not just what topic the page covers.

A noun-phrase heading ("Our Approach", "Architecture") is a label, not a claim. It signals that content exists on the page but makes no argument. A reader skimming only the titles of a noun-phrase deck learns nothing.

## The so-what test

For every title, ask: "So what?" If the answer to "so what?" is the information on the slide, the title is a label. If "so what?" returns a shrug — the title already contains the so-what — the title is an action title.

"Architecture" → so what? → fails (the slide content is the answer)
"Open-source control-plane components eliminate [CLIENT]'s proprietary lock-in risk." → so what? → returns a shrug, because the claim is already in the title. Pass.

## The read-through gate

Read the action titles of a deck or section top-to-bottom, without looking at any slide content. The titles alone should reproduce the argument. If you lose the thread between two slides, there is a gap in the argument — either the missing claim should be added or the order is wrong.

This is the final check before a deck goes to a client. If a sceptical reader gets the full argument from titles only, the deck will survive a 30-second skim.

**Make it mechanical, not a feel.** A read-through self-check once reported "the read-through holds" on an asset where a review board immediately found three consecutive non-claim titles. So **count**: how many titles are noun phrases or subordinate fragments rather than claims? **One is a defect; two consecutive is a P1.** Report the count, not the impression.

**First-use ordering.** Assert that the section which *defines* each canonical term precedes every section that uses it. A reader who meets a named entity before its definition silently loses the argument — in practice this was caught only incidentally, which means nothing catches it deliberately. It is also the cheapest check to re-run after any section reorder.

## De-slop the titles at the gate, before any build

Run the `voice` tell-scan over the action titles **at the Storyline gate**, while they are still a list.

Titles are the copy that regresses worst and gets touched most. Cleaned inside the artifact instead, they get cleaned again after every rework — in one cycle they were written, built, de-slopped in the HTML, partially re-slopped during a later rework, then cleaned twice more. Scanning the fresh list caught real tells (connective em dashes in three titles, a balanced antithesis plus rule-of-three in one, an "X, not Y" in another), and all of them were fixed once and locked.

Lock the de-slopped set in the state file and do not re-touch it during Build.

**Retitle all or none.** A partial recut leaves label titles stranded beside claim titles and breaks the read-through. Present the whole set as one before→after table, marking `keep` where unchanged, and get it approved as a set.

**One exception:** the hero or cover title may be a formal noun phrase. On a cover it reads more executive than a sentence, and it does not license noun-phrase titles for the sections below it.

## Rules

1. One claim per title. If you need a comma-joined compound sentence, you have two slides, not one.
2. Subject + verb + consequence, in that order where possible. "The migration timeline compresses to 12 months if [CLIENT] begins the dependency audit in Q1" is better than "By beginning the dependency audit in Q1, the migration timeline can be compressed to 12 months."
3. Quantify where you have numbers. "Three of the five proprietary components have open-source equivalents already validated in production" is stronger than "Most components have open-source equivalents."
4. Avoid "we" as subject unless the slide is explicitly about your own proposal. On a diagnostic slide, the subject is [CLIENT]'s situation.
5. Do not hedge the title. If a claim is uncertain, it should be on the slide with the caveat, not softened into a noun phrase.

## Five before/after examples

**1.**
Before: "Platform Overview"
After: "[CLIENT]'s current Kubernetes estate spans 26 clusters across two cloud providers, creating a mixed-sovereignty baseline that cannot meet the RfQ control-plane requirements as-is."

**2.**
Before: "Security Approach"
After: "Zero-trust network policy and OPA/Gatekeeper admission control together satisfy all nine MUST requirements in Cluster 4 without proprietary tooling."

**3.**
Before: "Our Approach"
After: "[FIRM]'s Assessment-first engagement resolves the four open technical unknowns before [CLIENT] commits to build or run scope."

**4.**
Before: "Next Steps"
After: "A six-week Assessment starting in March produces the dependency map and risk-adjusted options [CLIENT] needs to decide on scope before the regulatory window closes."

**5.**
Before: "Commercial Model"
After: "A T&M contract with capped phases gives [CLIENT] cost visibility while preserving the flexibility to adjust scope as the Assessment findings land."

## Common failure modes

**Answering a different question.** The action title claims something the slide does not actually prove. Check that every bullet on the slide is evidence for the title's claim, not for some other claim.

**Burying the so-what in the last bullet.** The title is still a noun phrase, and the real claim is hidden as a bolded sentence at the bottom of the slide. Promote it to the title.

**Stacking two slides' worth of claims.** The title is grammatically a sentence but contains two distinct arguments joined by "and" or a semicolon. Split the slide.

**Action verb without a specific object.** "We will accelerate delivery" — accelerate what, by how much, relative to what baseline? Specificity is what separates a claim from a slogan.
