"""
Deal Desk eval cases (Scenario Card A). One source of truth for promptfoo
(`create_tests`), the provider and the offline check.

Each case probes the functional rules one agent must apply, on the Acme RFP or on a
targeted variant of it (a few clauses swapped, so exactly one rule flips). Ground
truth comes from the playbooks in skills/ and the answer key in demo/README.md,
never from a model's output. Cases cover both directions: what an agent must refuse
AND what it must accept, so "refuse everything" can't pass.

A case:
  id      unique, "<flow>-<what>"
  flow    pricing | legal | technical_fit | competitive | critic | coordinator
  about   what it tests, and the rule behind it
  rfp     the RFP text the agent reads (mounted at /mnt/session/uploads/inputs/rfp.md)
  files   extra mounted files {name: text}; Pricing always gets past-wins.json
  checks  [(check_name, params)]; check names live in grading.CHECKS
  gold    the readout a perfect answer produces (used by the fake/oracle modes)
  oracle  a reference answer in prose (the oracle mode feeds it to the real extractor)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ACME = (ROOT / "synthetic-data" / "rfp-acme-corp.md").read_text()
PAST_WINS = (ROOT / "synthetic-data" / "past-wins.json").read_text()
INPUTS = "/mnt/session/uploads/inputs"


def variant(*edits: tuple[str, str]) -> str:
    """The Acme RFP with exact (old, new) replacements; each `old` must occur once."""
    text = ACME
    for old, new in edits:
        if text.count(old) != 1:
            raise ValueError(f"RFP variant: expected exactly one match for {old[:60]!r}")
        text = text.replace(old, new)
    return text


def add_after(anchor: str, addition: str) -> tuple[str, str]:
    return anchor, anchor + addition


# ── Exact clauses of the Acme RFP that variants swap ─────────────────────────
ABOUT = ("Acme Corp is a global manufacturer of industrial sensors and IoT devices. Revenue ~$1.4B "
         "(2025). 7,200 employees across 18 countries. We operate manufacturing facilities in "
         "Mexico, Vietnam, and Romania, with R&D centres in the US (Austin) and Germany (Munich).")
REVENUE = "Revenue ~$1.4B (2025)."
MICROSOFT = "We are a Microsoft shop. Our primary cloud is Azure."
WORKLOADS = ("- Real-time ingest from ~40,000 IoT devices in the field\n- Batch ETL from 30+ internal "
             "sources\n- BI and reporting for ~600 analysts and executives\n- Self-service data "
             "preparation for ~150 data engineers\n- Machine learning pipelines for predictive "
             "maintenance (planned, not active)")
SCALE = "- ~280 TB current data volume\n- ~12 TB / month growth rate\n- Peak ingest: 80,000 events/second"
POWER_BI = "- Native Power BI integration (this is non-negotiable — 600 users today)"
FORMATS = "- Open file formats (Parquet, Delta, Iceberg) for portability"
TERM = ("We are seeking a 3-year initial term with a 2-year renewal option. Pricing for the full "
        "5-year horizon must be fixed at the time of contract signature, with no escalators.")
PAYMENT = "Annual fees billed in advance, due Net 90."
DISCOUNT = "The successful vendor must offer no less than 35% off published list pricing."
MFN = ("The vendor must warrant that pricing offered to Acme is no less favourable than pricing "
       "offered to any comparable customer for the duration of the contract.")
TERMINATION = ("Acme reserves the right to terminate the contract at any time, with or without cause, "
               "on 30 days' written notice. No early termination fees or penalties.")
LIABILITY = ("Vendor liability for any data breach is uncapped. Vendor must indemnify Acme for all "
             "costs, including notification costs, regulatory fines, and reputational damages.")
AUDIT = ("Acme reserves the right to audit vendor's controls, facilities, and personnel without prior "
         "notice, up to four times per calendar year. Audit costs shall be borne by the vendor.")
SLA = ("Vendor must commit to 99.99% monthly uptime. SLA failures of any duration shall entitle Acme "
       "to terminate the contract immediately, with full refund of fees paid in the affected month.")
IP = ("All work product, including any custom development, configurations, and integrations created "
      "in the course of this engagement, shall vest in Acme Corp upon creation.")
SUBPROCESSORS = ("Vendor shall obtain Acme's prior written consent before engaging any subprocessor for "
                 "any part of the services. Consent may be withheld at Acme's sole discretion.")
VENDORS = ("We are also issuing this RFP to:\n- Databricks\n- Snowflake\n- Microsoft (Fabric)\n"
           "- A regional vendor we will not name in this document")
NO_VENDORS = "We will not disclose the other vendors invited to this RFP."

# An RFP whose contract terms already match our standard positions (both directions
# for Legal and the Critic: a correct review flags nothing).
CLEAN_RFP = variant(
    (PAYMENT, "Annual fees billed in advance, due Net 30."),
    (DISCOUNT, "Vendors should propose their discount from published list pricing."),
    (MFN, "No most-favoured-nation terms are requested."),
    (TERMINATION, "Either party may terminate for convenience on 90 days' written notice, and for "
                  "material breach not cured within 30 days. Refunds on early termination are pro-rated."),
    (LIABILITY, "Each party's aggregate liability is capped at 12 months of fees paid, with mutual "
                "carve-outs for gross negligence and IP infringement."),
    (AUDIT, "Acme may audit the vendor's controls once per calendar year on 30 days' notice, under "
            "confidentiality. Additional audits are at Acme's cost."),
    (SLA, "Vendor must commit to 99.95% monthly uptime. Service credits of up to 30% of monthly fees "
          "are the sole remedy for SLA failures."),
    (IP, "The vendor retains all IP in its service. Acme's data remains Acme's. Customer-specific work "
         "product is licensed to Acme."),
    (SUBPROCESSORS, "The vendor maintains a public subprocessor list and notifies Acme 30 days before "
                    "adding one; Acme may object, and the vendor then substitutes or allows termination."
                    "\n\n### 4.6 Breach notification\n\nThe vendor notifies Acme within 24 hours of "
                    "confirming a breach affecting Acme data.\n\n### 4.7 Governing law\n\nThis agreement "
                    "is governed by the laws of England and Wales, with disputes heard in the courts of "
                    "England."),
)

BRIEFS = {
    "pricing": (f"Pricing Specialist: an RFP has landed. Read the RFP at {INPUTS}/rfp.md and our comparable "
                f"deals at {INPUTS}/past-wins.json. Recommend commercial terms: the tier and its list price, "
                "the discount you would offer and its band, term and payment structure, the concessions "
                "you would accept and refuse, and the risks to our margin. Cite past wins where they apply."),
    "legal": (f"Legal Reviewer: review the RFP at {INPUTS}/rfp.md against our legal checklist. Flag every "
              "clause that deviates from our standard positions, with its section, severity (blocker / "
              "negotiable / acceptable) and our counter-position."),
    "technical_fit": (f"Technical Fit Specialist: assess whether our platform meets the requirements in the "
                      f"RFP at {INPUTS}/rfp.md. List what we meet fully, partially and not at all, give an "
                      "overall fit score, size the implementation timeline, and name the single most "
                      "important risk."),
    "competitive": (f"Competitive Intel Analyst: from the RFP at {INPUTS}/rfp.md, identify the competitors "
                    "most likely in this deal and the signals behind each, their strengths against our "
                    "angles, our two best positioning angles, and one trap to avoid."),
    "critic": (f"Deal Desk Critic: review the draft proposal at {INPUTS}/proposal-draft.md against the RFP "
               f"at {INPUTS}/rfp.md. Lead with your verdict."),
}

# Discount ceilings from the pricing playbook (percent off list).
BAND_500K_1M = {"standard": 20, "strategic": 25}  # Enterprise at $720K list
BAND_250K_500K = {"standard": 15, "strategic": 20}  # Growth at $360K list
TERM_UPLIFT = 5  # 3-year term: +5%, only with a CPI + 2% escalator


# ── Pricing ───────────────────────────────────────────────────────────────────

def pricing(id, about, rfp, checks, gold, extra=""):
    return {"id": id, "flow": "pricing", "agent": "pricing", "about": about, "rfp": rfp,
            "files": {"past-wins.json": PAST_WINS}, "brief": BRIEFS["pricing"],
            "checks": [("substantive", {})] + checks, "gold": gold, "oracle_extra": extra}


ACME_PRICING_GOLD = {
    "substantive": True, "tier": "Enterprise", "list_price_usd": 720000, "discount_pct": 25,
    "strategic_claimed": True, "strategic_bases": ["multi_year_commitment"],
    "customer_discount_demand": "rejects", "mfn": "rejects", "requested_payment_terms": "rejects",
    "proposed_payment_terms": "Annual upfront, Net 30", "price_escalator": False,
}

PRICING = [
    pricing(
        "pricing-acme",
        "The real Acme RFP. Enterprise ($720K list) is the only tier at this scale. 35% is above "
        "the 25% strategic ceiling (and the +5% term uplift needs an escalator Acme bans). MFN and "
        "Net 90 are never accepted. Acme is manufacturing, not a target vertical.",
        ACME,
        [("tier", {"expected": "Enterprise"}),
         ("list_price", {"expected": 720000}),
         ("discount_ceiling", {**BAND_500K_1M, "uplift": TERM_UPLIFT,
                               "valid_bases": ["multi_year_commitment", "reference_customer"]}),
         ("strategic_basis", {"valid_bases": ["multi_year_commitment", "reference_customer"]}),
         ("position", {"field": "customer_discount_demand", "expected": ["rejects"]}),
         ("position", {"field": "mfn", "expected": ["rejects"]}),
         ("position", {"field": "requested_payment_terms", "expected": ["rejects"]}),
         ("cites_past_deal", {})],
        ACME_PRICING_GOLD),
    pricing(
        "pricing-strategic-vertical",
        "Acme as a bank on a 1-year term: financial services is a target vertical, so the strategic "
        "band (25%) is open on vertical alone, with no term uplift on a 1-year deal.",
        variant((ABOUT, "Acme Corp is a regulated retail and commercial bank (financial services) "
                        "operating in 18 countries. Revenue ~$1.4B (2025). 7,200 employees."),
                (TERM, "We are seeking a 1-year initial term with annual renewals.")),
        [("tier", {"expected": "Enterprise"}),
         ("discount_ceiling", {**BAND_500K_1M, "uplift": 0,
                               "valid_bases": ["target_vertical", "reference_customer"]}),
         ("strategic_basis", {"valid_bases": ["target_vertical", "reference_customer"]}),
         ("position", {"field": "customer_discount_demand", "expected": ["rejects"]})],
        {**ACME_PRICING_GOLD, "strategic_bases": ["target_vertical"]}),
    pricing(
        "pricing-no-strategic",
        "Manufacturing, 1-year term, no reference agreement: no strategic basis exists (at most a "
        "reference agreement offered as a give-get), so the ceiling is the 20% standard band.",
        variant((TERM, "We are seeking a 1-year initial term with annual renewals.")),
        [("discount_ceiling", {**BAND_500K_1M, "uplift": 0, "valid_bases": ["reference_customer"]}),
         ("strategic_basis", {"valid_bases": ["reference_customer"]}),
         ("position", {"field": "customer_discount_demand", "expected": ["rejects"]})],
        {**ACME_PRICING_GOLD, "discount_pct": 20, "strategic_claimed": False, "strategic_bases": []}),
    pricing(
        "pricing-growth-tier",
        "A smaller platform (35 TB, 22 users, 99.9% SLA) fits Growth ($360K list), the $250K-$500K "
        "band: 15% standard, 20% strategic with the 3-year commitment.",
        variant((WORKLOADS, "- Batch ETL from 6 internal sources\n- BI and reporting for 18 analysts\n"
                            "- Self-service data preparation for 4 data engineers"),
                (SCALE, "- ~35 TB current data volume\n- ~0.5 TB / month growth rate"),
                (POWER_BI, "- Native Power BI integration (18 users)"),
                (SLA, "Vendor must commit to 99.9% monthly uptime.")),
        [("tier", {"expected": "Growth"}),
         ("list_price", {"expected": 360000}),
         ("discount_ceiling", {**BAND_250K_500K, "uplift": TERM_UPLIFT,
                               "valid_bases": ["multi_year_commitment", "reference_customer"]})],
        {**ACME_PRICING_GOLD, "tier": "Growth", "list_price_usd": 360000, "discount_pct": 20}),
    pricing(
        "pricing-net60-fortune500",
        "Both directions on payment terms: Net 60 is an allowed concession for a Fortune 500 "
        "customer with strong credit, so it should be accepted.",
        variant((REVENUE, "Revenue ~$62B (2025); a Fortune 100 company with an AA investment-grade credit "
                          "rating."),
                (PAYMENT, "Annual fees billed in advance, due Net 60.")),
        [("position", {"field": "requested_payment_terms", "expected": ["accepts"]})],
        {**ACME_PRICING_GOLD, "requested_payment_terms": "accepts",
         "proposed_payment_terms": "Annual upfront, Net 60"}),
    pricing(
        "pricing-milestone-payment",
        "Payment tied to implementation milestones is on the playbook's do-not-accept list.",
        variant((PAYMENT, "Fees are invoiced against implementation milestones; nothing is payable "
                          "before the first production workload goes live.")),
        [("position", {"field": "requested_payment_terms", "expected": ["rejects"]})],
        ACME_PRICING_GOLD),
    pricing(
        "pricing-poc-credit",
        "Crediting a PoC fee against Year 1 is a concession we make on all deals.",
        variant(add_after(TERMINATION, "\n\n### 3.6 Proof of concept\n\nBefore signing, Acme requires a "
                                       "60-day paid proof of concept. The PoC fee must be credited "
                                       "against Year 1 fees.")),
        [("position", {"field": "poc_credit", "expected": ["accepts"]})],
        {**ACME_PRICING_GOLD, "poc_credit": "accepts"}),
]


# ── Legal ─────────────────────────────────────────────────────────────────────

def legal(id, about, rfp, checks, gold):
    return {"id": id, "flow": "legal", "agent": "legal", "about": about, "rfp": rfp, "files": {},
            "brief": BRIEFS["legal"], "checks": [("substantive", {})] + checks, "gold": gold}


def flag(topic, severity, section, counter):
    return {"topic": topic, "severity": severity, "rfp_section": section, "counter": counter}


ACME_LEGAL_FLAGS = [
    flag("liability", "blocker", "4.1", "Liability capped at 24 months of fees for data breach, "
                                        "12 months otherwise, with mutual carve-outs."),
    flag("audit", "blocker", "4.2", "One audit a year on 30 days' notice, under confidentiality; "
                                    "Acme pays for audits beyond the first."),
    flag("sla", "blocker", "4.3", "99.95% standard; service credits up to 30% as the sole remedy; "
                                  "termination only for chronic failure."),
    flag("ip", "blocker", "4.4", "Customer-specific work is licensed to Acme, not assigned."),
    flag("subprocessors", "blocker", "4.5", "Public subprocessor list, 30 days' notice and a right to "
                                            "object."),
    flag("termination", "negotiable", "3.5", "Termination for convenience on 90 days' notice (60 at "
                                             "least), refunds pro-rated."),
]

LEGAL = [
    legal("legal-acme",
          "The real Acme RFP: five blockers (uncapped breach liability, no-notice audits, termination on "
          "any SLA miss, IP assignment, subprocessor pre-approval), 30-day termination for convenience "
          "is negotiable, and EU data residency matches our standard (no blocker).",
          ACME,
          [("severity", {"topic": "liability", "expected": ["blocker"]}),
           ("severity", {"topic": "audit", "expected": ["blocker"]}),
           ("severity", {"topic": "sla", "expected": ["blocker"]}),
           ("severity", {"topic": "ip", "expected": ["blocker"]}),
           ("severity", {"topic": "subprocessors", "expected": ["blocker"]}),
           ("severity", {"topic": "termination", "expected": ["negotiable"]}),
           ("severity", {"topic": "data_residency", "expected": ["acceptable", "not_flagged"]}),
           ("liability_cap_counter", {})],
          {"substantive": True, "flags": ACME_LEGAL_FLAGS}),
    legal("legal-clean-rfp",
          "Every contract clause already matches our standard positions (12-month cap, annual audit with "
          "notice, 99.95% with credits, licence model, subprocessor notice, 90-day termination, 24-hour "
          "breach notice, English law). A correct review raises no blockers.",
          CLEAN_RFP,
          [("no_blockers", {}),
           ("severity", {"topic": "termination", "expected": ["acceptable", "not_flagged"]}),
           ("severity", {"topic": "breach_notification", "expected": ["acceptable", "not_flagged"]})],
          {"substantive": True, "flags": []}),
    legal("legal-no-termination-for-convenience",
          "No termination for convenience during the initial term looks vendor-friendly, but our "
          "checklist makes it a blocker.",
          variant((TERMINATION, "Neither party may terminate for convenience during the 3-year initial "
                                "term; termination is permitted only for cause.")),
          [("severity", {"topic": "termination", "expected": ["blocker"]})],
          {"substantive": True, "flags": [flag("termination", "blocker", "3.5",
                                               "Termination for convenience on 90 days' notice.")]}),
    legal("legal-breach-immediately",
          "Breach notice 'immediately' is negotiable: push for 'without undue delay' (we commit to 72h).",
          variant(add_after(SUBPROCESSORS, "\n\n### 4.6 Breach notification\n\nThe vendor shall notify "
                                           "Acme immediately upon discovering any suspected breach.")),
          [("severity", {"topic": "breach_notification", "expected": ["negotiable"]})],
          {"substantive": True, "flags": [flag("breach_notification", "negotiable", "4.6",
                                               "Notify without undue delay, within 72 hours.")]}),
    legal("legal-subprocessors-after-the-fact",
          "Being told about new subprocessors only after the fact looks lenient, but it is a blocker "
          "(an audit failure).",
          variant((SUBPROCESSORS, "The vendor may engage subprocessors at its discretion and shall inform "
                                  "Acme of any new subprocessor within 90 days after engagement.")),
          [("severity", {"topic": "subprocessors", "expected": ["blocker"]})],
          {"substantive": True, "flags": [flag("subprocessors", "blocker", "4.5",
                                               "Notify 30 days before adding a subprocessor.")]}),
    legal("legal-joint-ip",
          "Joint ownership of derivative works is negotiable (discouraged), unlike assignment of all "
          "work product, which is a blocker.",
          variant((IP, "Derivative works created in the course of this engagement shall be jointly owned "
                       "by Acme and the vendor.")),
          [("severity", {"topic": "ip", "expected": ["negotiable"]})],
          {"substantive": True, "flags": [flag("ip", "negotiable", "4.4",
                                               "License derivative works to Acme instead.")]}),
    legal("legal-governing-law",
          "German law with mandatory ICC arbitration: customer-home law and arbitration are both "
          "negotiable for a deal this size (our standard is England & Wales, courts).",
          variant(add_after(SUBPROCESSORS, "\n\n### 4.6 Governing law\n\nThis agreement is governed by the "
                                           "laws of Germany. All disputes shall be resolved by mandatory "
                                           "ICC arbitration in Munich.")),
          [("severity", {"topic": "governing_law", "expected": ["negotiable"]})],
          {"substantive": True, "flags": [flag("governing_law", "negotiable", "4.6",
                                               "England & Wales law, courts of England.")]}),
]


# ── Technical Fit ─────────────────────────────────────────────────────────────

ACME_REQUIREMENTS = {
    "ingest": "Real-time ingest from ~40,000 IoT devices, peak 80,000 events/second",
    "batch_etl": "Batch ETL from 30+ internal sources",
    "power_bi": "Native Power BI integration for ~600 users",
    "data_prep": "Self-service data preparation for ~150 data engineers",
    "ml": "ML pipelines for predictive maintenance",
    "scale": "~280 TB of data growing ~12 TB a month",
    "multi_region": "Multi-region deployment (primary EU, secondary US East)",
    "eu_residency": "EU customer data must remain in the EU",
    "lakehouse": "Lakehouse architecture with open formats (Parquet, Delta, Iceberg)",
    "sla_9999": "99.99% monthly uptime",
}


def technical(id, about, rfp, requirements, checks, gold):
    return {"id": id, "flow": "technical_fit", "agent": "technical_fit", "about": about, "rfp": rfp,
            "files": {}, "brief": BRIEFS["technical_fit"], "requirements": requirements,
            "checks": [("substantive", {})] + checks, "gold": gold}


def ratings(**given):
    return [{"requirement_id": k, "rating": v} for k, v in given.items()]


TECHNICAL = [
    technical("technical-acme",
              "The real Acme RFP: everything is met in full (80K events/s against 250K tested, Power "
              "BI with a DirectQuery adapter, per-table EU residency) except 99.99% uptime, a paid "
              "add-on, which is also the top risk. Teradata migration takes 16-24 weeks.",
              ACME, ACME_REQUIREMENTS,
              [("rating", {"req": "power_bi", "expected": ["full"]}),
               ("rating", {"req": "ingest", "expected": ["full"]}),
               ("rating", {"req": "eu_residency", "expected": ["full"]}),
               ("rating", {"req": "multi_region", "expected": ["full"]}),
               ("rating", {"req": "sla_9999", "expected": ["partial"]}),
               ("no_false_gaps", {"reqs": ["batch_etl", "data_prep", "ml", "scale", "lakehouse"]}),
               ("overall_fit", {"expected": ["high"]}),
               ("top_risk", {"expected": ["sla_9999"]}),
               ("migration_weeks", {"min": 16})],
              {"substantive": True,
               "ratings": ratings(ingest="full", batch_etl="full", power_bi="full", data_prep="full",
                                  ml="full", scale="full", multi_region="full", eu_residency="full",
                                  lakehouse="full", sla_9999="partial"),
               "overall_fit": "high", "top_risk": "sla_9999", "migration_weeks_min": 16,
               "migration_weeks_max": 24}),
    technical("technical-sub-100ms",
              "The capability map says to flag sub-100ms real-time analytics as a partial fit "
              "(we reach ~250ms-1s on streaming queries).",
              variant(add_after(FORMATS, "\n- Operational dashboards must return streaming query results "
                                         "in under 100 ms end-to-end")),
              {"latency": "Streaming query results in under 100 ms end-to-end"},
              [("rating", {"req": "latency", "expected": ["partial"]})],
              {"substantive": True, "ratings": ratings(latency="partial")}),
    technical("technical-power-apps",
              "Power BI yes, Power Apps no: the capability map has no native Power Apps connector. "
              "The case asks for both, so the agent must split them.",
              variant(add_after(FORMATS, "\n- Native Power Apps connector for shop-floor operational apps")),
              {"power_apps": "Native Power Apps connector",
               "power_bi": "Native Power BI integration for ~600 users"},
              [("rating", {"req": "power_apps", "expected": ["none"]}),
               ("rating", {"req": "power_bi", "expected": ["full"]})],
              {"substantive": True, "ratings": ratings(power_apps="none", power_bi="full")}),
    technical("technical-graph-geospatial",
              "Graph workloads are not supported natively (none); geospatial has basic support only "
              "(partial for advanced indexing).",
              variant(add_after(FORMATS, "\n- Native graph analytics for supplier-network modelling\n"
                                         "- Advanced geospatial indexing for fleet tracking")),
              {"graph": "Native graph analytics", "geospatial": "Advanced geospatial indexing"},
              [("rating", {"req": "graph", "expected": ["none"]}),
               ("rating", {"req": "geospatial", "expected": ["partial"]})],
              {"substantive": True, "ratings": ratings(graph="none", geospatial="partial")}),
    technical("technical-oci-only",
              "We deploy on AWS, Azure and GCP only, so an OCI-only requirement is not met.",
              variant((MICROSOFT, "Our only cloud is Oracle Cloud Infrastructure (OCI); the platform must "
                                  "run in OCI.")),
              {"oci": "Must run in Oracle Cloud Infrastructure (OCI)"},
              [("rating", {"req": "oci", "expected": ["none"]})],
              {"substantive": True, "ratings": ratings(oci="none")}),
    technical("technical-self-hosted",
              "Both directions: a self-hosted option for sovereignty exists, so this is met in full "
              "(an agent that hedges everything fails here).",
              variant(add_after(FORMATS, "\n- Must be deployable self-hosted in Acme's own data centres "
                                         "for sovereignty reasons")),
              {"self_hosted": "Self-hosted deployment in Acme's data centres"},
              [("rating", {"req": "self_hosted", "expected": ["full"]})],
              {"substantive": True, "ratings": ratings(self_hosted="full")}),
]


# ── Competitive Intel ─────────────────────────────────────────────────────────

def competitive(id, about, rfp, checks, gold):
    return {"id": id, "flow": "competitive", "agent": "competitive", "about": about, "rfp": rfp,
            "files": {}, "brief": BRIEFS["competitive"], "checks": [("substantive", {})] + checks,
            "gold": gold}


COMPETITIVE = [
    competitive("competitive-acme",
                "The RFP names Databricks, Snowflake and Microsoft Fabric; Azure + Power BI make Fabric "
                "the sharpest threat. No GCP signal, so BigQuery is not in the deal. The trap must come "
                "from a battlecard (e.g. don't compete on Power BI), and TCO is the lead angle.",
                ACME,
                [("competitors_include", {"required": ["databricks", "snowflake", "microsoft_fabric"]}),
                 ("competitors_exclude", {"forbidden": ["google_bigquery"]}),
                 ("battlecard_trap", {}),
                 ("angle", {"required": "tco"})],
                {"substantive": True,
                 "likely_competitors": ["microsoft_fabric", "databricks", "snowflake"],
                 "traps": [{"competitor": "microsoft_fabric", "topic": "compete_on_power_bi"}],
                 "angle_topics": ["tco", "workload_coverage_real_time"]}),
    competitive("competitive-gcp-signals",
                "No vendors named; a Google Cloud shop with BigQuery ML and Looker. BigQuery must be "
                "inferred from the signals, and Fabric (no Microsoft signal left) must not be listed.",
                variant((MICROSOFT, "We are a Google Cloud shop. BigQuery ML models and Looker dashboards are "
                                    "used across the business."),
                        (POWER_BI, "- Native Looker integration (this is non-negotiable — 600 users today)"),
                        (VENDORS, NO_VENDORS)),
                [("competitors_include", {"required": ["google_bigquery"]}),
                 ("competitors_exclude", {"forbidden": ["microsoft_fabric"]})],
                {"substantive": True, "likely_competitors": ["google_bigquery", "databricks"],
                 "traps": [{"competitor": "google_bigquery", "topic": "claim_better_serverless"}],
                 "angle_topics": ["multi_cloud", "governance"]}),
    competitive("competitive-snowflake-signals",
                "No vendors named; an existing Snowflake user relying on secure data sharing. Snowflake "
                "must be inferred.",
                variant((MICROSOFT, "We already run Snowflake for finance analytics and rely on its secure "
                                    "data sharing with suppliers."),
                        (POWER_BI, "- Support for our existing BI tools (600 users today)"),
                        (VENDORS, NO_VENDORS)),
                [("competitors_include", {"required": ["snowflake"]}),
                 ("competitors_exclude", {"forbidden": ["google_bigquery"]})],
                {"substantive": True, "likely_competitors": ["snowflake", "databricks"],
                 "traps": [{"competitor": "snowflake", "topic": "out_analyst_tool_snowflake"}],
                 "angle_topics": ["tco", "workload_coverage_real_time"]}),
    competitive("competitive-databricks-signals",
                "No vendors named; MLflow, Delta tables and a lakehouse. Databricks must be inferred.",
                variant((MICROSOFT, "Our data engineering team is standardising on MLflow for model "
                                    "tracking and Delta tables for the lakehouse."),
                        (POWER_BI, "- Support for our existing BI tools (600 users today)"),
                        (VENDORS, NO_VENDORS)),
                [("competitors_include", {"required": ["databricks"]}),
                 ("competitors_exclude", {"forbidden": ["google_bigquery"]})],
                {"substantive": True, "likely_competitors": ["databricks"],
                 "traps": [{"competitor": "databricks", "topic": "out_engineer_spark_or_iceberg"}],
                 "angle_topics": ["tco", "time_to_insight"]}),
]


# ── Critic (only when the Critic is set up: stretch_critic_subagent.py) ──────

DEFECTIVE_DRAFT = """\
# Proposal response: Acme Corp Enterprise Data Platform (DRAFT)

## Executive summary
- BTS-Synthetic meets every workload in the RFP, including native Power BI.
- We offer the Enterprise tier at $720,000 list with the 35% discount Acme requires: $468,000 a year,
  fixed for five years.
- We accept Acme's contract terms in full to accelerate the award.

## Commercial proposal
- Enterprise tier, $720,000 list, 35% discount ($468,000 a year), fixed for 5 years, no escalators.
- Annual fees in advance, due Net 90 as requested.
- We warrant most-favoured-nation pricing for the duration of the contract.

## Contract approach
- Our liability for any data breach is uncapped, and we indemnify Acme for all costs, including
  regulatory fines.
- All work product vests in Acme on creation.
- We commit to 99.99% monthly uptime as part of the standard Enterprise subscription, at no extra cost.

## Risks
- Implementation, including the Teradata migration, completes in 8 weeks.
"""

CLEAN_DRAFT = """\
# Proposal response: Acme Corp Enterprise Data Platform

## Executive summary
- BTS-Synthetic covers Acme's workloads in full: real-time IoT ingest, batch ETL, Power BI through our
  DirectQuery adapter, and EU data residency per table.
- Enterprise tier at $720,000 list with our standard 20% discount: $576,000 a year.
- Implementation, including the Teradata migration, takes 16 weeks.

## Commercial proposal
- Enterprise tier, $720,000 list, 20% discount (the standard band for a deal of this size): $576,000 a year.
- 3-year term, annual fees in advance, Net 30. No price escalator; no most-favoured-nation terms.

## Contract approach
- Liability capped at 12 months of fees, with mutual carve-outs, as the RFP proposes.
- One audit a year on 30 days' notice; 99.95% uptime with service credits up to 30% as the sole remedy.
- Customer-specific work is licensed to Acme; public subprocessor list with 30 days' notice.
- Termination for convenience on 90 days' notice, refunds pro-rated.

## Risks
- Teradata migration sequencing: mitigated by a 16-week plan with parallel running.
"""

PLANTED = ["discount_above_band", "net90_accepted", "mfn_accepted", "uncapped_liability_accepted",
           "ip_assignment_accepted", "sla_9999_promised_free"]

CRITIC = [
    {"id": "critic-planted-defects", "flow": "critic", "agent": "critic",
     "about": "A draft with six planted playbook violations (35% discount, Net 90, MFN, uncapped "
              "liability, IP assignment, 99.99% at no cost). It must not ship, and the Critic must "
              "catch at least four of them.",
     "rfp": ACME, "files": {"proposal-draft.md": DEFECTIVE_DRAFT}, "brief": BRIEFS["critic"],
     "checks": [("substantive", {}),
                ("verdict", {"expected": ["REVISE", "STOP"]}),
                ("catches_defects", {"planted": PLANTED, "min": 4})],
     "gold": {"substantive": True, "issues_raised": PLANTED[:5]}},  # verdict: graded on the text
    {"id": "critic-clean-draft",
     "flow": "critic", "agent": "critic",
     "about": "Both directions: a sound draft against an RFP with standard terms. The Critic should "
              "ship it and must not invent playbook violations.",
     "rfp": CLEAN_RFP, "files": {"proposal-draft.md": CLEAN_DRAFT}, "brief": BRIEFS["critic"],
     "checks": [("substantive", {}),
                ("verdict", {"expected": ["SHIP IT"]}),
                ("no_false_alarms", {"forbidden": PLANTED})],
     "gold": {"substantive": True, "issues_raised": []}},
]


# ── Coordinator: the full swarm, end to end (evals/e2e.yaml) ─────────────────

# The 13 traps of demo/README.md are scored by demo/scorecard.py; the semantic checks
# below read the docx's commitments, so "35%" next to "25%" can't pass if we offer 35%.
COORDINATOR = [
    {"id": "coordinator-acme", "flow": "coordinator", "agent": "coordinator",
     "about": "The whole swarm on the Acme RFP: parallel fan-out to all four specialists with file "
              "paths, every report back, a branded docx that handles the 13 planted traps and commits "
              "to nothing the playbooks forbid.",
     "rfp": ACME, "files": {}, "brief": "(run_deal_desk.kickoff_message)",
     "checks": ([("substantive", {}), ("fanout_all", {}), ("parallel_fanout", {}), ("briefs_carry_paths", {}),
                 ("reports_all", {}), ("docx_produced", {}), ("deck_produced", {}), ("branding", {}),
                 ("summary_names_docx", {})]
                + [("trap", {"id": f"C{i}"}) for i in range(1, 14)]
                + [("tier", {"expected": "Enterprise"}),
                   ("discount_ceiling", {**BAND_500K_1M, "uplift": TERM_UPLIFT,
                                         "valid_bases": ["multi_year_commitment", "reference_customer"]}),
                   ("position", {"field": "customer_discount_demand", "expected": ["rejects"]}),
                   ("position", {"field": "mfn", "expected": ["rejects", "not_mentioned"]}),
                   ("position", {"field": "requested_payment_terms", "expected": ["rejects"]}),
                   ("position", {"field": "liability", "expected": ["capped"]}),
                   ("position", {"field": "ip", "expected": ["licence_model"]}),
                   ("position", {"field": "sla", "expected": ["standard_99_95",
                                                             "offers_99_99_as_paid_add_on"]})]),
     "gold": {**ACME_PRICING_GOLD, "liability": "capped", "ip": "licence_model",
              "sla": "offers_99_99_as_paid_add_on"}},
]

ALL = PRICING + LEGAL + TECHNICAL + COMPETITIVE + CRITIC + COORDINATOR
BY_ID = {case["id"]: case for case in ALL}
assert len(BY_ID) == len(ALL), "duplicate case ids"
FLOWS = ["pricing", "legal", "technical_fit", "competitive", "critic", "coordinator"]


def critic_is_set_up() -> bool:
    state = ROOT / ".swarm_state.json"
    return state.exists() and "critic" in json.loads(state.read_text()).get("specialists", {})


def create_tests(config: dict | None = None) -> list[dict]:
    """promptfoo entry point: one test per case, one python assertion per check."""
    flows = (config or {}).get("flows") or FLOWS
    tests = []
    for case in ALL:
        if case["flow"] not in flows:
            continue
        if case["flow"] == "critic" and not critic_is_set_up():
            print(f"skipping {case['id']}: no Critic in this checkout "
                  "(uv run python stretch_critic_subagent.py)", file=sys.stderr)
            continue
        tests.append({
            "description": f"{case['id']}: {case['about']}",
            "vars": {"case_id": case["id"], "flow": case["flow"], "brief": case["brief"]},
            "metadata": {"flow": case["flow"], "case": case["id"]},
            "assert": [{"type": "python", "value": "file://grading.py:check",
                        "config": {"check": name, **params}, "metric": f"{case['flow']}:{name}"}
                       for name, params in case["checks"]],
        })
    return tests
