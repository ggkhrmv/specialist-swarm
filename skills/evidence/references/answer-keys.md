# Answer keys and the GO/NO-GO gate

## The move

Before building an asset claim on a proxy measure — a classifier, a keyword rule, a heuristic join, an
LLM adjudication — construct a small **answer key** from a channel *independent of the signal you are
testing*, and measure the proxy against it. Gate the expensive full run on that result, with the
threshold stated **before** you dispatch.

This was the decisive move in the most data-heavy engagement in the record. Pairs were established
purely from one side of the join — a ticket that linked its own pull request, so the answer was known
without reading the commit at all. That gave a key which settled the method in one cheap measurement
instead of four expensive attempts.

## What makes a key independent

The key must not be derived from the thing you are testing. If your proxy reads commit messages, the
key cannot come from commit messages. Look for:

- A record that links the two objects directly, so the pairing is known a priori.
- A second system that recorded the same event for a different reason.
- A human-curated subset — a list someone maintained by hand for their own purposes.

An answer key drawn from the same channel as the proxy measures self-consistency, not accuracy.

## The gate

State it before dispatching, as a number:

> GO if the proxy reaches ≥ X% precision and ≥ Y% recall on the key. NO-GO otherwise, and the fallback
> is Z.

Write the fallback down too. A gate with no stated fallback becomes a gate you argue your way past
when the result disappoints — and the whole point is to spend the expensive run only when it will
produce something publishable.

Honour a NO-GO. In practice one NO-GO saved a full run over 4,120 units, and the reframe that followed
(publishing the measurement gap instead of a weak proxy) was stronger than the metric would have been.

## Audit the key for leakage

A key that exists *because* of an artifact may carry the answer into your inputs through that same
artifact.

The concrete failure: the key existed because a link sat in the record — and the record also rendered
the artifact's **own title** into the candidate text the adjudicator read. Nine of twenty-one correct
answers in the first run were correct for that reason alone. The sanitiser was rewritten to strip the
title and the run was redone blinded.

So, after building the key and before trusting the result:

1. Ask what makes each key item *knowable*, and whether that same thing appears in the input.
2. Strip it. Titles, ids, canonical names, timestamps that only the linked record would carry.
3. **Re-run blinded** and compare. If the score drops materially, the first score was leakage.

## Report

Report the key's size, how it was constructed, what independence claim you are making for it, the
sanitisation applied, and the blinded score. A key whose construction is not described cannot be
audited, and a proxy validated on an unauditable key is not validated.
