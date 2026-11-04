# evidence — eval scenarios

Each scenario is drawn from a real failure. RED baselines are what an unaided pass did.

## Scenario 1 — a low count in one system of record
**Prompt:** "Size how often teams have to request infrastructure changes. The ticket tracker is at `./export.json`."
**Expected behavior:** computes the rate, then **tests the instrument before trusting it**: asks what channel the work would flow through if nobody filed a ticket, and checks at least one independent channel (declarative config repositories, commit history, chat) before letting a low count weaken the claim. Reports the coverage denominator with the rate.
**RED baseline:** reports the low rate as a measured finding and recommends demoting the claim ("only 6.1% of tickets show this, so it is a smaller problem than assumed").
**RED reasoning:** the default treats the available corpus as the population. Confirmed RED — this inverted a headline finding in practice: the configuration repositories showed 1,940 declared resources against 31 requests, the opposite conclusion, and the post-mortem was "I treated a low ticket count as a small problem, when it actually meant the gap was being absorbed silently."
**GREEN:** `positioning/references/evidence-from-client-data.md` carries the single-instrument fallacy and the coverage denominator; SKILL.md step 3 makes coverage an explicit step. Addressed.

## Scenario 2 — a recorded constraint that was never tested
**Prompt:** "The state file says nothing in the corpus measures effort, so estimate the figure instead."
**Expected behavior:** treats the constraint as an **assumption**, tests it before building on it (does any record carry a worklog, duration, or equivalent field?), and — because this constraint blocks a headline claim — re-tests rather than accepting it a second time. On finding it false, sweeps both the asset and the state file for prose that rested on it, and logs the correction with the reason.
**RED baseline:** accepts the recorded constraint and proceeds to estimate, labelling every derived figure an estimate.
**RED reasoning:** a state file reads as established fact. Confirmed RED — the constraint was false (over half the items carried a worklog), it had capped the asset for days, and it had blocked the reviewer's top ask.
**GREEN:** the constraint register in `asset-forge/references/state-file-template.md` records who tested what and when; SKILL.md's core discipline and step 2 require re-testing any constraint that blocks a headline claim. Addressed.

## Scenario 3 — validating a proxy before the expensive run
**Prompt:** "Classify all 4,120 records with the LLM and give me the rate."
**Expected behavior:** builds a small **answer key from a channel independent of the signal being tested**, states a GO/NO-GO threshold *before* dispatching, measures the proxy against the key, then audits the key for leakage — if the key exists because of an artifact that also carries the answer into the inputs, sanitises and re-runs blinded. Honours a NO-GO.
**RED baseline:** runs the classification over all records and reports the resulting rate with a spot-check of a handful of examples.
**RED reasoning:** without a key there is no accuracy figure, so the rate ships unqualified. Confirmed RED. In practice the key was decisive twice: it produced a NO-GO that saved the full run, and the leakage audit found 9 of 21 first-pass correct answers were correct only because the record rendered the artifact's own title into the candidate text.
**GREEN:** `references/answer-keys.md` covers independence, the pre-stated gate, the leakage audit, and the blinded re-run. Addressed.

## Scenario 4 — a chained metric judged on its components
**Prompt:** "Step 1 has 88% recall, step 2 is 71.4% accurate, step 3 is near-perfect. Can we publish the pipeline's number?"
**Expected behavior:** refuses to answer from the component figures and **propagates the error to the output**, reporting the overstatement factor and the share of the reported number that is real. Sets the publish threshold before computing, and on failure reaches for the measurement-gap-as-finding play rather than a weaker proxy.
**RED baseline:** reasons that the components are individually acceptable and publishes the pipeline figure with a caveat about step 2.
**RED reasoning:** per-step accuracy reads as adequate while the composition collapses. Confirmed RED — one such pipeline would have reported ~2,840 events against a truth of ~360: an 8× overstatement with 13% of the reported figure real.
**GREEN:** `references/error-propagation.md` requires the output-side numbers and a pre-set threshold. Addressed.

## Scenario 5 — a window that hides a reversal and truncates the population
**Prompt:** "Give me year-to-date figures so we can show whether the measures worked, plus the current backlog age."
**Expected behavior:** splits the window at the intervention date and reports PRE/POST rather than an average spanning the change. Separately, recognises that a backlog-age metric describes items that may have started before the window opened, so the date filter cannot be applied to the population — only to the events.
**RED baseline:** reports a year-to-date average and a backlog age computed over the same filtered extract.
**RED reasoning:** both queries look correct and neither error is visible in the output. Confirmed RED — the average hid a reversal (21.6% → 30.9% once split), and the truncation made three already-reported figures wrong (backlog 238→296, over-90-days 104→167, 172→351).
**GREEN:** `references/window-discipline.md` carries the intervention split and the truncation check. Addressed.

## Scenario 6 — comparing to a prior baseline
**Prompt:** "Compare these numbers to the snapshot from the last assessment."
**Expected behavior:** re-runs the current method over the **baseline's own window** first and reports per-metric where it replicates and where it does not, diagnosing each divergence (definitional / population / method inadequacy / real change) before comparing anything.
**RED baseline:** compares the two sets directly and reports the deltas as changes in the world.
**RED reasoning:** the prior figures look like a fixed reference point. Confirmed RED — in practice volume shares replicated (81% → 79.2%) while the work-type mix did not (84% → 47%), which proved the cheap keyword rule inadequate and justified the expensive classification pass. Reported as a delta, it would have been a fabricated trend.
**GREEN:** `references/replication.md` requires the replication run and the divergence diagnosis. Addressed.

## Scenario 7 — relaying a subagent's headline figure
**Prompt:** [an analysis subagent returns "odds ratio 68, p < 0.001, strongly significant"]
**Expected behavior:** recomputes the load-bearing number from the raw data before relaying it, states that it did, and reports any divergence — including divergence that does not change the conclusion.
**RED baseline:** relays the subagent's figure to the user as established.
**RED reasoning:** a structured, confident return reads as a result rather than as a finding. Confirmed RED — one such figure reproduced as ~52 rather than 68 under a continuity correction (same conclusion), and in a separate case an agent's correction of the orchestrator's own number was only confirmed by re-checking the raw fields.
**GREEN:** SKILL.md's core discipline and `references/analysis-dispatch.md` both require independent recomputation before relay. Addressed.
