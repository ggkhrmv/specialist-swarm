# Deal Desk swarm: demo kit

What to say, what to show, and how to prove it, on the synthetic Acme RFP or on real data.

- [The 60-second version](#the-60-second-version)
- [What makes it special](#what-makes-it-special)
- [The demo case: 13 traps in the Acme RFP](#the-demo-case-13-traps-in-the-acme-rfp)
- [Run of show (5 minutes, with a 2-minute cut)](#run-of-show)
- [Demo modes and fallbacks](#demo-modes-and-fallbacks)
- [Running it on real data](#running-it-on-real-data)
- [Prep checklist](#prep-checklist)
- [Questions you will get](#questions-you-will-get)

---

## The 60-second version

**Problem.** An RFP lands. Pricing, Legal, Solutions and Competitive Intel each review it on their own, over days of
email, and a partner stitches the answers together. The worst risks sit *between* the lanes: a discount justified by a
3-year commitment that a 30-day exit clause makes worthless. Nobody owns those seams.

**What we built.** A Senior Partner agent reads the RFP and briefs four specialist agents **in parallel**. Each one
judges the RFP against the firm's own rulebook for its lane (pricing playbook, legal checklist, capability map,
battlecards). The partner then **checks the reports against each other**, resolves the conflicts, and writes a
**branded, send-ready proposal (.docx)**.

**Why it matters.** A cross-functional deal review in minutes instead of days. It follows the firm's actual policy, not
the model's general knowledge, so every counter-position traces back to a rule a named team owns. And the seams get
checked every time.

> One line for the room: *"It's your deal desk: a partner and four specialists working to your playbooks, in parallel,
> who actually read each other's notes."*

## What makes it special

| # | Claim | What to show as proof |
| --- | --- | --- |
| 1 | **Organised like the firm.** One coordinator and four specialists, each with its own context, rulebook and model. Specialists never see each other's work, so they judge independently, and wall-clock time is the slowest lane, not the sum. | Terminal: four `[brief →]` lines within seconds of each other. Console trace: four separate threads. |
| 2 | **The firm's knowledge is a file the business owns.** The playbooks are plain markdown Skills (`skills/*/SKILL.md`). The pricing desk edits the pricing playbook, `setup_swarm.py` uploads a new version, and the next deal follows the new rule. No code changes, no retraining. | Open `skills/pricing-playbook/SKILL.md` next to the RFP's 35% demand. Optional act: change one rule and show the answer change. |
| 3 | **The seams get checked.** The partner reads the reports against each other (pricing assumptions against legal positions, the SLA against its price) before writing a word. | The 5 `[seam]` rows in the scorecard, and the risk section of the docx. |
| 4 | **Honest by construction.** The capability map lists our weaknesses, and Technical Fit treats anything not in the map as unsupported. The swarm says "99.99% costs extra" instead of "yes". | The SLA section of the docx (trap C8). |
| 5 | **The output is the deliverable.** A branded Word document with the structure the RFP asked for, not a chat transcript. | `outputs/proposal-response.docx`. |
| 6 | **Governed and cheap to operate.** Every session has a spend cap ($10 on `demo`, $3 on `dev`). Specialists get read-only tools, inputs are mounted read-only, every thread is traced, and every run's cost and time are logged. A $0 offline check gates every change in CI. | The cost line and run history printed at the end of the run. |

What it is **not**: it doesn't send anything, sign anything or make the final call. A human partner reviews the document.

## The demo case: 13 traps in the Acme RFP

`synthetic-data/rfp-acme-corp.md` reads like a normal enterprise RFP, but 13 of its requests collide with the firm's
own rules. That makes it a good demo case: a generic "AI writes a proposal" tool says yes to most of them, while a desk
that follows its playbooks has to push back, put a price on things and reconcile its lanes.

**Seam** = a trap that is only visible when two lanes' reports are read together. These are the ones to narrate.

| # | RFP asks (section) | Collides with | Lanes | A good answer says |
| --- | --- | --- | --- | --- |
| C1 | **35% off list** (3.3) | Playbook ceiling for a $500K–$1M deal: 20% standard, 25% strategic (3+ years committed). The 3-year +5% only comes with an escalator, which Acme bans. | Pricing (+ Competitive) | Refuse 35%. Offer up to 25%, and sell TCO, not headline price. Pied Piper (`past-wins.json`) is the warning: we lost at 30% against Databricks' 40% and "should have walked away earlier". Initech, a similar profile, settled at 15% on TCO. |
| C2 | **5-year fixed price, no escalators** (3.1) | The 3-year term discount requires a CPI+2% escalator (capped at 5%) | Pricing | Choose one: the escalator *or* no term uplift. Price the renewal years explicitly. |
| C3 | **Net 90** (3.2) | "Do not accept Net 90+" | Pricing | Net 30. Quarterly billing is the allowed concession. Net 60 is only for Fortune 500 customers, and Acme isn't one. |
| C4 | **Most favoured nation** (3.4) | "MFN: never. The single most poisonous clause" | Pricing + Legal | Decline. Offer price protection on the committed term instead. |
| C5 | **Terminate at will, 30 days, no fees** (3.5) | Legal: push for 60+ days (our standard is 90). Pricing: pro-rated refunds only. | **Seam:** Legal × Pricing | The strategic discount is justified by a 3-year *commitment*, and a 30-day exit right cancels it. Tie the discount to the commitment, or lengthen the notice. |
| C6 | **Uncapped breach liability, incl. reputational damages** (4.1) | Blocker: insurance won't cover it | Legal + Pricing | Cap at 24 months of fees for data breach (12 months general), with mutual carve-outs. |
| C7 | **4 audits a year, no notice, vendor pays** (4.2) | "Without notice" is a blocker; more than 2 a year is negotiable | Legal | Once a year on 30 days' notice, under confidentiality. Acme pays beyond the first. |
| C8 | **99.99% uptime** (4.3) | We offer 99.95%. 99.99% is a custom add-on with active-active multi-region, at $80–120K a year. | **Seam:** Technical Fit × Pricing | Say yes *at a price*: the add-on goes into the commercial proposal, which moves the deal size. Only visible when the tech report and the pricing report are read together. |
| C9 | **Terminate on any SLA miss + full monthly refund** (4.3) | Blocker. Service credits up to 30% are the sole remedy. | **Seam:** Legal × Technical Fit | Service credits capped at 30% as the sole remedy, with termination only for chronic failure. |
| C10 | **All work product vests in Acme on creation** (4.4) | Blocker: we license customer-specific work, we don't assign it | **Seam:** Legal × Pricing's data | License it to Acme. The precedent is in Pricing's file, not Legal's: Stark Industries accepted a licence-back of derivative works. Only the partner sees both. |
| C11 | **Prior consent for every subprocessor** (4.5) | Blocker: too heavy to operate | Legal | Public subprocessor list, 30 days' notice, a right to object, then we substitute or allow termination. |
| C12 | **Power BI is non-negotiable; Microsoft Fabric is bidding** (2.3, 6) | Tech: Power BI is our most mature integration. Battlecard: "Don't compete on Power BI. We integrate, they own." | **Seam:** Competitive × Technical Fit | Confirm full Power BI support (dedicated DirectQuery adapter), but don't lead with it. Name "free with E5" and reframe it as TCO. Lead with real-time ingest, which beat Fabric at Initech. |
| C13 | **Teradata decommission through 2027** (1) | 16 weeks for a Teradata migration, 24 for multi-region and multi-source | Technical Fit | A 16–24 week plan from the June 30 award. Don't promise faster. |

**Not traps** (a good answer confirms them briefly): a peak of 80K events/s against 250K tested; EU residency through
per-table pinning; lakehouse with Delta, Iceberg and Parquet; Azure deployment; ML pipelines (registry and feature
store). The likely shortlist is named in the RFP: Databricks, Snowflake and Microsoft Fabric.

**The headline a good run reaches:** *bid, with conditions.* Enterprise list plus the 99.99% add-on comes to about
$800–840K a year. The ceiling is 25% off, about $600–630K a year, or 30% if Acme accepts the 3-year escalator. Decline
MFN, Net 90, uncapped liability, no-notice audits, IP assignment and the subprocessor veto. Win on TCO and real-time
ingest, not on Power BI.

### What the rehearsals produced (2026-11-04, `demo` profile)

Three rehearsals, all checked by hand against the documents. **Present run 3:** it ran on the current swarm, with
the pitch deck from #9, so it matches what will run live. All three runs' files are in `~/deal-desk-rehearsal/` on the
presenting laptop.

**Run 3 (current swarm: docx + deck), the moments to point at:**
- **The fan-out, measured:** four specialists briefed within 0.7 s, and four reports in **60 s of wall time for 149 s of
  specialist work**. Read the `[fan-in]` line out at 2:00.
- **One clear price:** 20% off, **$576K a year, flat for all five years with no escalators**, $2.88M in total (C1, C2).
  It takes the playbook's standard band without the 3-year uplift, so no escalator is needed.
- **Seam C5 on the page:** termination for convenience on 90 days' notice with a pro-rated refund and no exit fee,
  but *"before month 36, fees used are re-rated to the one-year price"*. The discount is earned by the commitment that
  justifies it.
- **99.99% is a priced option:** $120K a year on an EU active-active design, outside the base price (C8). The SLA remedy
  is service credits up to 30%, with termination only for chronic failure, 3 misses in 6 months (C9).
- **The commercial and legal table answers every clause:** Net 30 or quarterly (C3), MFN declined because the fixed
  price already protects Acme (C4), plus liability, audit, IP and subprocessor counters (C6, C7, C10, C11).
- **The deck (`outputs/pitch-deck.html`):** five slides in the same voice. It is the only place that names the
  competition: *"Chosen over Microsoft Fabric before"*, the Initech precedent on real-time ingest.
- **Judgment calls to own:** Fabric is answered on real-time ingest, not on E5 or TCO (C12, partial in all three runs).
  Legal should confirm the month-36 re-rating isn't a "penalty fee"; run 1's notes raised the same question.
- **The coordinator re-briefed two specialists** (Technical Fit and Pricing) before writing. If it happens live, that's
  the "one follow-up" rule working: say so.

**What varies between runs.** All three opened at 20% and $576K a year, but the structure changes. Run 2 offered two
options (25% only for a committed three-year term), and run 1 wrote unprompted `internal-deal-notes.md` with the
walk-away line (25% only with commitment, reference and escalator, VP Sales sign-off). Run 2 offered Net 60, which the
playbook reserves for Fortune 500 customers. Technical Fit's first report came back blank in runs 2 and 3, and the
coordinator caught it both times. In run 1, Competitive Intel sent its report three times. **Don't promise a specific
structure or the notes file live:** show the rehearsed run 3 and describe the rest as range.

### Proving it: the scorecard

```bash
uv run python demo/scorecard.py                       # outputs/: the proposal, plus notes and deck if the same run wrote them
uv run python demo/scorecard.py <file> ... --show     # specific files; prints the paragraph behind each ✓
```

It costs $0, runs offline and uses only the standard library. It prints one line per trap and ends with
`Traps handled: N/13   cross-lane seams: M/5`. A hit found outside the proposal (in the notes or the deck) is marked
with the file name. A file left over from an earlier run is skipped. It's a keyword proximity check,
not a judge. Calibration, each result matching a hand check: the raw RFP scores **0/13** (it raises every trap and
answers none), a hand-written good answer **13/13**, run 1 **13/13** (12 in the proposal, C12 in the notes), and runs 2
and 3 **12/13** (C12 partial, see above; the run 3 deck alone scores 9/13). Before you quote a ✗ on stage, confirm it in the document.

## Run of show

The fan-out happens in the first minute of a run, and that's the visual. Building the document takes longer, so plan on
**starting live and finishing on the rehearsed docx** (mode B below). The numbers come from the rehearsal; update
them if a later run differs.

| Time | Screen | What happens | What you say |
| --- | --- | --- | --- |
| 0:00 | RFP, §3–4 highlighted | | "Acme wants 35% off, a 30-day exit, uncapped liability and 99.99% uptime. Four teams would spend a week on this. Watch." |
| 0:30 | Terminal | `uv run python run_deal_desk.py`. Four `[brief →]` lines, then `[fan-out] 4 specialists briefed within 0.7s`. | "One partner, four specialists, briefed in the same instant. None of them sees the others' work, so nobody anchors on anybody." |
| 1:00 | `skills/pricing-playbook/SKILL.md` | | "This is the pricing desk's own rulebook, in plain text. They own it. Change a line and the next deal follows it. No code." |
| 1:30 | Console trace (URL printed at start) | One specialist thread reading its skill and the RFP | "Every thread is traced. You can audit why it said what it said." |
| 2:00 | Terminal | `[report ←]` lines come back, and the partner cross-checks | Read out the `[fan-in]` line, e.g. "60 seconds of wall time for 149 seconds of specialist work" (46–60 s in rehearsals). Then: "Now the part nobody has time for: reading the reports *against each other*." |
| 2:45 | Rehearsed `proposal-response.docx`, then `pitch-deck.html` | Title page, exec summary, commercial, contract approach, risks; then the five slides | Walk the price: 20% off, fixed for five years, with the discount re-rated on an exit before month 36 (seam C5). Show C8: "yes to 99.99%, at a price". Flick through the deck: "same swarm, same run, the executive version." |
| 4:00 | Terminal | `uv run python demo/scorecard.py` | "13 traps in this RFP. It handled 12, including 4 of the 5 that only show when two teams compare notes. The one it softened, Fabric, it answered on real-time ingest rather than cost." Quote the score of the document you actually show. |
| 4:30 | Run history (end of the live run) | Cost and time | "That review, the proposal and the deck cost under two dollars and took about six minutes. Your playbooks, your format, every deal." |

**2-minute cut:** the 0:30 fan-out, the 2:00 seam, the docx headline and the scorecard number. The deck for it is
[`slides.html`](slides.html): open it in a browser and use the arrow keys. Press `N` for the speaker notes with each
slide's time slot, `T` for a rehearsal clock against 2:00, and `F` for full screen. It prints to PDF one slide per page
as a backup. Its numbers and commercial excerpt are run 3's (table below), so present them with run 3's docx and deck. The diagrams were made with the `diagram-design`
skill (dark skin).

| Time | Slide | The point |
| --- | --- | --- |
| 0:00–0:20 | 1. The asks | Acme's four demands, and which one hides a seam |
| 0:20–0:50 | 2. How it works | Partner, four specialists in parallel, playbooks as Skills, cross-check, docx and deck |
| 0:50–1:10 | 3. Live | Switch to the terminal: four `[brief →]` lines within a second, then the fan-in line |
| 1:10–1:35 | 4. The seam (C5) | Pricing's 25% needs a 3-year commitment and Legal allows an exit at will; the partner keeps the exit but re-rates the fees on an exit before month 36 |
| 1:35–2:00 | 5. Proof | 12/13 traps, 4/5 seams, $1.79, 6.3 minutes; edit a markdown file to change a rule |

**Optional act: change the rule, change the answer (+2 min).** This is the strongest proof of claim 2. In a separate
worktree, change one line of a playbook, e.g. make Net 60 acceptable for every enterprise deal in
`pricing-playbook`. Re-run there, and keep both documents. On stage, show the one-line `git diff` and the two
commercial sections side by side. Prepare it in advance: it costs a second run, and doing it in a worktree leaves the
`main` demo swarm untouched.

## Demo modes and fallbacks

| Mode | When | How |
| --- | --- | --- |
| **A. Fully live** | The rehearsed run time fits the slot with margin | Start at 0:30 and narrate until the docx arrives. |
| **B. Live start, rehearsed finish** (recommended) | Default | Start live for the fan-out, walk the rehearsal docx, and come back to the live run for its cost line, or note that it's still working. |
| **C. No network** | Wi-Fi or API trouble | Play a screen recording of the rehearsal terminal and open the saved docx. `uv run python tests/offline_check.py -v` shows the whole pipeline running against a fake client at $0. |
| **D. Real data** | The audience brings an RFP, or you have one cleared | See below. Always pre-run it. Never run an unvetted document live for the first time. |

## Running it on real data

There are two levels. Start with level 1.

**Level 1: a real RFP against the synthetic firm.** This shows the swarm generalises beyond one document. The playbooks
are still BTS-Synthetic's, so prices and positions are illustrative.

```bash
pdftotext -layout their-rfp.pdf ~/deal-desk-private/rfp.txt     # or: pandoc rfp.docx -o rfp.md
DEAL_RFP=~/deal-desk-private/rfp.txt uv run python run_deal_desk.py
uv run python download_deliverable.py                             # if the download needs a retry
```

`DEAL_RFP` swaps the RFP. `past-wins.json` is still mounted for Pricing, and the session is titled after the file.
`.md` and `.txt` are accepted: specialists have read-only file tools, so convert PDFs and Word files first.

**Level 2: a real RFP against real firm knowledge (a pilot).** Replace the content of the four `SKILL.md` files with
the firm's real, cleaned playbooks, and `past-wins.json` with an anonymised CRM export. Do it in a **private** copy,
not this repository. Then re-run `setup_swarm.py` and score the result against an expert's blind answer key (step 3
below).

**Guardrails. Read these before you touch real data.**

1. **This repository is public.** Keep real RFPs, playbooks and outputs outside it, e.g. in `~/deal-desk-private/`.
   `outputs/` is gitignored, but your input files are not.
2. **The files go to the Anthropic API** (Files API, then the session container). Get the data owner's permission
   first, and remove client names and personal data unless that permission covers them.
3. **The scorecard's answer key only fits Acme.** For a real RFP, have a deal-desk expert list 5–10 traps *before*
   the run, then compare. That blind comparison is also the most convincing evidence you can show a sceptical audience.
4. **The coordinator still brands the document as BTS-Synthetic** (`prompts/coordinator.md`). Change that prompt in
   your private copy if the document will be shown outside the team.

**Steps for a real-data demo:** clear the data (1 day ahead) → convert to text → pre-run on `demo` and keep the docx
outside `outputs/` → expert writes a blind answer key → compare and pick the 2–3 best seams to narrate → on stage, run
mode B with the real document.

## Prep checklist

**The day before**
- [ ] After the last merge: in the main checkout, `git pull`, then `uv run python setup_swarm.py` (`demo` profile).
- [ ] Full rehearsal: `uv run python run_deal_desk.py`. Copy `outputs/proposal-response.docx` outside `outputs/`,
      because the next run overwrites it.
- [ ] `uv run python demo/scorecard.py --show`, then check every ✗ by hand.
- [ ] Fill in the blanks below and in the run of show.
- [ ] Record the rehearsal terminal for mode C.
- [ ] Optional act: prepare both documents and the one-line diff in a worktree.

**One hour before**
- [ ] `uv run python tests/offline_check.py` passes, and the API key works (a `setup_swarm.py` re-run is free and
      idempotent).
- [ ] Windows open: the terminal (large font), the RFP with §3–4 highlighted, `pricing-playbook/SKILL.md`, the
      rehearsal docx, and a browser for the Console.

**Rehearsal numbers** (from the run history and the scorecard)

| Date | Session | Swarm | Minutes | Cost | Traps | Seams |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-04 | `sesn_01WhtcNNpDUwUrza15Vh4Htm` | `demo`, before #3 and #6 | 5.4 | $1.31 | 13/13 (12 in the docx) | 5/5 |
| 2026-11-04 | `sesn_019zRXdTu6K1DS7fi2tWR3Vo` | `demo`, with #3 and #6 | 4.3 | $1.11 | 12/13 | 4/5 |
| 2026-11-04 | `sesn_01KUVcS11hHMPXp6hP2UsEpY` | `demo`, current (with #9: docx + deck) | 6.3 | $1.79 | 12/13 | 4/5 |

The rehearsal files are kept outside the repo, in `~/deal-desk-rehearsal/<date>-demo/` on the presenting laptop.

## Questions you will get

- **"Why not one big prompt?"** Four isolated contexts can't anchor on each other, they run in parallel, each lane runs
  on the model it needs (Haiku for battlecard lookups, Sonnet for judgment, Opus for synthesis), and each rulebook has
  one owner. The partner's cross-check only works because the reports were written independently.
- **"Does it make things up?"** Each specialist is told to judge by its skill. The capability map says anything not
  listed is unsupported, and lists our weaknesses. Every thread is traced. The scorecard, or an expert's blind key,
  checks the result.
- **"How do we make it ours?"** Edit four markdown files, then run `setup_swarm.py`. The firm-voice skill (stretch S1)
  changes the tone the same way.
- **"What does it cost?"** The three rehearsals cost $1.11–$1.79 at list price and took 4.3–6.3 minutes for the
  whole review and the deliverables. The current swarm, which also builds the deck, cost $1.79 and took 6.3 minutes. Every session has a hard cap ($10 on `demo`).
- **"What if a specialist is wrong?"** The partner sends one follow-up when a report misses something material. The
  optional Critic agent (stretch S2) reviews the draft before it ships. A human signs off before anything is sent.
- **"Is our data safe?"** It runs on the Anthropic API only. Inputs are mounted read-only, specialists can't write or
  browse, and sessions are capped. For client data, see the guardrails above.
