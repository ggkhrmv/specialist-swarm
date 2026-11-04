# Request for Proposal — Kestrel Logistics Group Analytics Platform Modernisation

**From:** Kestrel Logistics Group, Strategic Sourcing (sourcing@kestrel-synthetic.example)
**To:** Vendor — BTS-Synthetic
**Issued:** 2026-10-28
**Response due:** 2026-11-18 (21 days)
**Award expected:** 2026-12-18

## 1. About Kestrel Logistics Group

Kestrel Logistics Group is a European freight and contract-logistics operator, headquartered in Rotterdam. Revenue ~$1.0B (2025). 5,400 employees, 62 cross-dock and warehouse sites in 11 countries (including the UK). We run a fleet of ~9,000 trucks and ~3,200 refrigerated and dry trailers, all fitted with telematics.

Our primary cloud is AWS (eu-west-1 and eu-central-1). Our Nordic business unit, acquired with Nordlys Freight in 2024, still runs on Azure. Analytics today is split across an on-premises Oracle Exadata warehouse (end of support December 2027), a Hadoop cluster we are retiring, and a Snowflake pilot that two teams have used since early 2025.

## 2. Scope

We are seeking one analytics platform to replace the Exadata warehouse and the Hadoop cluster, and to decide the future of the Snowflake pilot.

### 2.1 Workloads
- Streaming telematics from ~12,000 vehicles and trailers: GPS position, cold-chain temperature, engine and driver-behaviour data
- Batch ETL from 25+ sources, including SAP S/4HANA, our transport management system, three warehouse management systems and customs platforms
- BI and reporting for ~400 users: Tableau is the group standard (~300 users), with ~100 Power BI users in the Nordic unit
- Self-service data preparation for ~60 data engineers and analysts
- ETA and route-prediction models (one production model on a single lane today, to scale across the network in 2027)
- Live shipment-tracking views for our key accounts, refreshed within 2 seconds of a telematics event

### 2.2 Scale
- ~140 TB current data volume
- ~6 TB / month growth rate
- Peak ingest: 45,000 events/second (Q4 peak season)

### 2.3 Capabilities
- Runs on AWS in the EU. No customer or employee data leaves the EU/EEA; UK site data stays in the UK.
- Open table formats (Iceberg preferred) so we can change vendors without a migration project
- Supported, certified connectors for both Tableau and Power BI
- Driver-level telematics is personal data under GDPR: pseudonymisation by default, and controls our works councils in Germany and the Netherlands will accept
- Geofencing and route-deviation detection over the GPS stream

## 3. Commercial requirements

### 3.1 Term
A 4-year term. Prices are fixed for the full term, with no escalators.

### 3.2 Payment
Fees billed quarterly in arrears, due Net 75.

### 3.3 Price
Our budget envelope is **$550K per year, all-in**. We expect at least 30% off published list pricing. Price is the single largest evaluation criterion, and we will shortlist the two lowest compliant bids for final presentations.

### 3.4 Price benchmarking
Kestrel may benchmark the vendor's pricing once a year against comparable customers. If the vendor's price is above the benchmark, the vendor shall reduce it to match from the next quarter.

### 3.5 Termination
Kestrel may terminate for convenience on 60 days' written notice, with a pro-rata refund of any prepaid fees.

## 4. Contractual requirements

### 4.1 Liability
Vendor liability capped at 3× annual fees, except for data-protection breaches, where liability is uncapped.

### 4.2 IP
All configurations, pipelines, data models, ML models and dashboards created by the vendor in the course of this engagement vest in Kestrel.

### 4.3 Service levels
99.95% monthly uptime. Service credits of up to 25% of monthly fees for SLA failures.

### 4.4 Exit
On expiry or termination, the vendor provides 6 months of transition assistance at no charge and a full export of all data in open formats.

### 4.5 Subprocessors
Vendor shall give 30 days' notice of any new subprocessor. Kestrel may object, and if the objection is not resolved, terminate without penalty.

## 5. Evaluation criteria

| Criterion | Weight |
| --- | --- |
| Price (annual fees) | 35% |
| Functional fit (workloads + capabilities) | 30% |
| Implementation plan and risk | 20% |
| References in logistics or transport | 15% |

## 6. Vendors being evaluated

We are also issuing this RFP to:
- Snowflake (incumbent pilot)
- Databricks
- An AWS-native proposal from our current systems integrator

## 7. Response format

Please respond by 2026-11-18 with:
- Executive summary (1 page)
- Technical proposal, including how you meet the Exadata end-of-support date
- Commercial proposal with full pricing for all 4 years
- Implementation plan with key milestones
- Two customer references (logistics or transport preferred)

## 8. Contact

Direct all questions and the response to: sourcing@kestrel-synthetic.example
Sourcing lead: Ingrid Vos, Head of Strategic Sourcing
Technical lead: Tomasz Nowak, Director of Data & Analytics
