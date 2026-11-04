"""
Reference answers for the oracle modes, rendered from each case's `gold` readout.

EVAL_MODE=oracle feeds these to the real judge: a correct grader scores them ~100%.
EVAL_MODE=fake-oracle pairs them with the perfect readout to test the wiring at $0.
They are deliberately plain; they show what a passing answer must contain, not style.
"""

from __future__ import annotations

from create_specialists import SPECIALISTS

SEVERITY = {"blocker": "BLOCKER", "negotiable": "Negotiable", "acceptable": "Acceptable"}
BASES = {"target_vertical": "a target vertical (financial services)",
         "multi_year_commitment": "the 3-year commitment", "reference_customer": "a reference agreement"}
ISSUE_TEXT = {
    "discount_above_band": "The 35% discount is above our 25% strategic ceiling.",
    "net90_accepted": "Net 90 is on the do-not-accept list; counter with Net 30.",
    "mfn_accepted": "The MFN warranty must go: we never grant most-favoured-nation pricing.",
    "uncapped_liability_accepted": "Uncapped breach liability is uninsurable; cap it at 24 months of fees.",
    "ip_assignment_accepted": "IP assignment of all work product: license customer-specific work instead.",
    "sla_9999_promised_free": "99.99% uptime is a paid add-on, not part of the standard subscription.",
}


def pricing(g: dict) -> str:
    lines = [f"Tier: {g['tier']}, list price ${g['list_price_usd']:,.0f} a year."]
    if g["strategic_claimed"]:
        lines.append(f"Recommended discount: {g['discount_pct']}%, the strategic band (VP Sales sign-off), "
                     f"justified by {', '.join(BASES[b] for b in g['strategic_bases'])}.")
    else:
        lines.append(f"Recommended discount: {g['discount_pct']}%, the standard band. The strategic band "
                     "does not apply here.")
    lines.append({"rejects": "We decline the RFP's minimum discount demand: it is above our ceiling.",
                  "accepts": "We accept the RFP's discount demand."}.get(g["customer_discount_demand"], ""))
    lines.append({"rejects": "We refuse the most-favoured-nation clause.",
                  "accepts": "We accept the MFN clause."}.get(g["mfn"], ""))
    lines.append({"rejects": f"We do not accept the requested payment terms; we counter with "
                             f"{g['proposed_payment_terms']}.",
                  "accepts": f"We accept the requested payment terms ({g['proposed_payment_terms']})."
                  }.get(g["requested_payment_terms"], ""))
    lines.append("The term uplift would need a CPI + 2% escalator, which the RFP bans, so we don't take it."
                 if not g.get("price_escalator") else "We include an annual CPI + 2% escalator (capped at 5%).")
    if g.get("poc_credit") == "accepts":
        lines.append("We will credit the PoC fee against Year 1 fees.")
    lines.append("Comparable deal: Initech Sensors, a similar profile, settled at 15% on 3-year TCO.")
    return "\n".join(line for line in lines if line)


def legal(g: dict) -> str:
    if not g["flags"]:
        return ("I reviewed every contractual clause against the legal checklist. Each one matches our "
                "standard position, so there is nothing to flag and no blocker.")
    return "\n\n".join(f"ITEM: {f['topic'].replace('_', ' ').upper()}\nRFP says: section {f['rfp_section']}\n"
                       f"Severity: {SEVERITY[f['severity']]}\nCounter: {f['counter']}" for f in g["flags"])


def technical(case: dict, g: dict) -> str:
    labels = {"full": "met fully", "partial": "met partially", "none": "not met"}
    lines = [f"- {case['requirements'][r['requirement_id']]}: {labels[r['rating']]}" for r in g["ratings"]]
    if g.get("overall_fit") and g["overall_fit"] != "not_stated":
        lines.append(f"Overall fit: {g['overall_fit']}.")
    if g.get("top_risk") and g["top_risk"] not in ("not_stated", "other"):
        lines.append(f"Most important risk: {case['requirements'][g['top_risk']]}.")
    if g.get("migration_weeks_min", -1) > 0:
        lines.append(f"Implementation, including the Teradata migration: {g['migration_weeks_min']:.0f}-"
                     f"{g['migration_weeks_max']:.0f} weeks.")
    return "\n".join(lines)


def competitive(g: dict) -> str:
    names = {"databricks": "Databricks", "snowflake": "Snowflake", "microsoft_fabric": "Microsoft Fabric",
             "google_bigquery": "Google BigQuery"}
    traps = {"compete_on_power_bi": "don't compete on Power BI integration: we integrate, they own it",
             "dismiss_e5_free_claim": "don't dismiss 'free with E5'; reframe it to TCO",
             "out_engineer_spark_or_iceberg": "don't try to out-engineer them on Spark or Iceberg",
             "out_analyst_tool_snowflake": "don't try to out-analyst-tool Snowflake on day 1",
             "claim_better_serverless": "don't claim better serverless than BigQuery"}
    angles = {"tco": "a 3-year total cost of ownership comparison", "workload_coverage_real_time":
              "real-time and semi-structured workload coverage", "multi_cloud": "multi-cloud flexibility",
              "governance": "governance and data-mesh maturity", "time_to_insight": "time-to-insight for analysts"}
    lines = [f"Most likely shortlist: {', '.join(names[c] for c in g['likely_competitors'])}."]
    lines += [f"Positioning angle: {angles[a]}." for a in g["angle_topics"]]
    lines += [f"Trap ({names[t['competitor']]}): {traps[t['topic']]}." for t in g["traps"]]
    return "\n".join(lines)


def critic(g: dict) -> str:
    verdict = "SHIP IT" if not g["issues_raised"] else "REVISE"
    body = ["The draft is solid; nothing beyond cosmetic edits."] if not g["issues_raised"] else \
        [f"{i}. {ISSUE_TEXT[t]}" for i, t in enumerate(g["issues_raised"], 1)]
    return f"VERDICT: {verdict}\n\n" + "\n".join(body)


PROPOSAL = """\
BTS-Synthetic: Proposal response to Acme Corp, Enterprise Data Platform

Acme gets a platform that keeps its 600 Power BI users and lands IoT data in real time.

Commercial: Enterprise tier, $720,000 list. Acme asks for 35% off list; we offer 25%, the strategic ceiling for a 3-year commitment.

We price the five years flat and forgo the term uplift, so no CPI escalator applies.

Payment: Net 90 is outside our terms; we propose annual upfront on Net 30, or quarterly billing.

We decline the MFN clause and offer price protection on the committed term instead.

Termination for convenience on 30 days would undo the 3-year commitment behind the discount; we propose 90 days' notice with pro-rated refunds.

Liability: uncapped breach liability is uninsurable. We cap liability at 24 months of fees for a data breach and 12 months otherwise.

Audits: once a year on 30 days' notice, under confidentiality.

99.99% uptime is available as a paid add-on with active-active multi-region, at $80K to $120K a year.

SLA remedy: service credits up to 30% as the sole remedy, and termination only for chronic failure.

Custom work product is licensed to Acme, following our licence-back precedent.

Subprocessors: a public list, 30 days' notice and a right to object.

Microsoft Fabric's 'free with E5' headline leaves out capacity and consulting costs; our 3-year TCO is lower.

The Teradata migration runs 16 to 24 weeks from the June 30 award.
"""


def run(case: dict) -> dict:
    """A reference run: the answer a perfect agent gives, and a perfect orchestration."""
    g = {**case["gold"]}
    if case["flow"] == "coordinator":
        names = [s["name"] for s in SPECIALISTS]
        return {"text": PROPOSAL, "agent_model": "", "files": ["proposal-response.docx", "pitch-deck.html"],
                "summary": "Saved /mnt/session/outputs/proposal-response.docx. Headline: $540,000 a year.",
                "expected_specialists": names,
                "briefs": [{"to": n, "text": "Read /mnt/session/uploads/inputs/rfp-acme-corp.md", "at": i}
                           for i, n in enumerate(names)],
                "reports": [{"from": n, "at": len(names) + i} for i, n in enumerate(names)]}
    render = {"pricing": lambda: pricing(g), "legal": lambda: legal(g),
              "technical_fit": lambda: technical(case, g), "competitive": lambda: competitive(g),
              "critic": lambda: critic(g)}[case["flow"]]
    return {"text": render(), "agent_model": ""}


def empty_run(case: dict) -> dict:
    run_ = {"text": "", "agent_model": ""}
    if case["flow"] == "coordinator":
        run_.update({"files": [], "summary": "", "briefs": [], "reports": [],
                     "expected_specialists": [s["name"] for s in SPECIALISTS]})
    return run_
