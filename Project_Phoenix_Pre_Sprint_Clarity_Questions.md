# Project Phoenix — Pre-Sprint Requirements Clarity Questions
**Prepared:** July 15, 2026  
**Status: ALL ITEMS RESOLVED ✓** — Updated July 15, 2026  
**Purpose:** Consolidated list of open questions that must be answered before engineering sprints begin. Sourced from: (1) full DB scan of 1,364 active requirements and (2) technical developer gap assessment.  
**Owner to Answer:** Justin Woller, with escalation to relevant stakeholders noted per item.

---

## GROUP A — Legal & Compliance Decisions ✓ RESOLVED

**A1. Guardian Access to Minor Patient Accounts (M01-GRD-004) ✓**  
**Resolution:** STI is universal across all 50 states — minors have independent consent rights for STI care everywhere. Since Everlywell currently only offers STI products, a simple platform-wide hardcoded block on guardian visibility for all minor patient records is sufficient for v1.0. No per-state configuration table needed. v2.0 will add a per-state config table when additional care products (mental health, reproductive health) are introduced.  
*DB updated: M01-GRD-004 → Active*

**A2. Patient Insurance / Coverage Section Scope (M03-ACCT-002) ✓**  
**Resolution:** Patients can view and update their insurance information, including uploading front and back card images. Real-time eligibility verification (270/271 EDI) is not available in v1.0 — eligibility is handled manually or through existing back-office processes. The section is self-service UI only.  
*DB updated: M03-ACCT-002 → Active*

**A3. Audit Log vs. Access Log Table — Architecture Decision (access_log vs AU-001) ✓**  
**Resolution:** The `access_log` table in the demo environment is a temporary dev artifact for login tracking. The real system uses the full M12 audit log (AU-001) as the authoritative immutable record for all user actions including logins. The two are separate for the demo only — in production, `access_log` functionality should be consolidated into the M12 audit trail. No automated purge logic — data stays indefinitely.  
*DB updated: AU-004 → Active*

**A4. HIPAA Audit Log Retention Period (AU-004) ✓**  
**Resolution:** No automated purges. Retention is indefinite — data stays in the audit table. If storage is a concern, records can be archived to an external table but not deleted. This exceeds HIPAA's 6-year minimum. California's longer requirements are covered by indefinite retention.  
*DB updated: AU-004 → Active*

---

## GROUP B — Clinical & Operational Decisions ✓ RESOLVED

**B1. Urgent Adverse Effect SLA Window (PS-003) ✓**  
**Resolution:** Any reported adverse effect triggers an Urgent Message immediately to all clinical users. If not resolved within 30 minutes, escalation fires to the Escalation Team via SMS + in-app alert. Escalation Team is a new admin-configurable role (ESCL-001) with minimum 1 verified mobile member required.  
*DB updated: PS-003 → Active. ESCL-001 created → Active*

**B2. After-Hours Service Access Window (AH-005) ✓**  
**Resolution:** Default business hours are 8 AM–8 PM. Hours are configured per day of week in the Org Profile (ORG-001) in the Admin Portal. Org Profile also stores company name, address, and org timezone. AH-005 references the Org Profile as its source of truth for the business hours window.  
*DB updated: AH-005 → Active. ORG-001 created → Active*

**B3. Post-Results Resource Menu — Static vs. Dynamic (M03-RES-001) ✓**  
**Resolution:** Static per care product. Everlywell's clinical team defines a table of approved resources and guidelines (educational links, referral options, follow-up guidance) based on clinical interpretation standards. Resources are NOT dynamically driven by individual patient result values — the lab report handles in-range/out-of-range display separately. All patients on a given care product see the same resource menu. Admin Portal allows the clinical team to manage the resource list per care product.  
*DB updated: M03-RES-001 → Active (Genevieve meeting not needed)*

**B4. Geographic Eligibility Check — Implementation Approach (M07-ELG-001) ✓**  
**Resolution:** Self-attestation in v1.0. When a patient initiates intake, the platform asks them to confirm their state. The patient selects/confirms from an existing pre-populated address on file from onboarding. This approach is already reflected in the demo environment.  
*DB updated: M07-ELG-001 → Active*

**B5. Provider Redistribution Notification Content (FE-005) ✓**  
**Resolution:** Everlywell's clinical team defines redistribution notification content per their clinical guidelines — the template is admin-configured. Content standard is driven by Everlywell's clinical interpretation and communication guidelines, not left to individual provider discretion. Note: FE-005 status remains v2.0 in the DB (deferred feature), but the content model is defined.  
*DB noted: FE-005 content model defined; status remains v2.0*

**B6. Softphone Integration — Acceptance Criteria (OPEN-006) ✓**  
**Resolution:** AWS Amazon Connect is the softphone vendor. The softphone is launched directly from the patient chart. Providers and care team members can initiate calls and log calls or emails in the activity timeline from within the chart. v1.0 is the real integration requirement (not a mock-only workflow).  
*DB updated: OPEN-006 → Active*

---

## GROUP C — State Machine & Business Logic Gaps ✓ RESOLVED

**C1. Unlimited Reassignment — Is There an Operational Ceiling? (CARS-002) ✓**  
**Resolution:** No hard lock on consecutive SLA misses. The system allows cycling indefinitely. However, 3 or more consecutive SLA misses on a single consult becomes a reporting metric in M13 dashboards — operational leadership reviews and intervenes manually. No automated hard-lock or admin freeze.  
*DB updated: CARS-002 created → Active*

**C2. SLA Clock on Invalid Document Upload (M02-SLA-005) ✓**  
**Resolution:** Industry standard confirmed (and adopted): the SLA clock always runs. SLA misses are attributed using reason codes — Provider Miss, Patient Delay, System Issue, or Administrative. A "Patient Delay" reason code is applied when a patient fails to upload valid documents, which protects provider performance metrics. The SLA clock does not pause waiting for valid replacement documents.  
*DB updated: M02-SLA-005 → Active with full reason code framework*

**C3. Cancelled Consult Admin Override (M02-STATUS-001) ✓**  
**Resolution:** Cancelled is a permanent terminal status. There is no admin override to reactivate a cancelled consult. The correct workflow when a cancellation needs to be reversed is to create a new consultation. This keeps the data model simple and the audit trail clean.  
*DB updated: M02-STATUS-001 → Active (admin override language removed)*

**C4. Lab Order Cancelled at Level 2 — Patient-Side Handling (M14-LAB-007) ✓**  
**Resolution:** When a lab order is cancelled at Level 2 physician review, it routes back to the GCA queue as an open task. GCA manages patient outreach proactively — no automated patient notification fires from the system. GCA determines next steps (re-order, patient contact, consult modification).  
*DB updated: M14-LAB-007 → Active*

---

## GROUP D — Third-Party Integration Mock Specifications ✓ DEFERRED TO ENGINEERING

All five integration mock spec questions (D1–D5) are deferred to a dedicated technical requirements session with Blake Lusenhop (Engineering). These are vendor/schema decisions that require the engineering team's input on existing middleware and integration contracts. They are not blocking the requirements layer — they are blocking the development sprint definition.

- D1. Verifiable License Check mock response schema (M01-LIC-001, M02-RX-002)
- D2. DoseSpot prescription data model (M02-CASE-006)
- D3. Daily.co video waiting room event simulation (M02-WS-010)
- D4. DDI/DGI drug interaction data source (M14-DDI-002)
- D5. Health Profile sync mock data structure (M03-HP-001)

*Owner: Blake Lusenhop + Engineering team. Action: Schedule integration technical requirements session.*

---

## GROUP E — Dashboard & Reporting Payload Specs ✓ RESOLVED

**E1. Consult Volume Dashboard Widget — Raw Data Payload (M02-DASH-011) ✓**  
**Resolution:** "Completed" = chart-closed (not provider-signed). Scoped to the logged-in provider only — not their full team. Team-level reporting is not in scope for the provider dashboard widget.  
*DB updated: M02-DASH-011 → Active*

---

## REQUIREMENT STUBS ✓ COMPLETED (17 items)

All 17 requirements that had missing rules and acceptance criteria have been filled in by Claude directly from the requirement content. No additional decisions from Justin were needed.

| Requirement | Description | Status |
|---|---|---|
| M09-SCHED-012 | RN/MA/CT schedule access permissions | ✓ Filled |
| M09-SCHED-013 | Multi-provider max 5, chip disable logic | ✓ Filled |
| M09-SCHED-014 | Provider color coding + legend | ✓ Filled |
| M09-SCHED-015 | Toggle chips + session persistence | ✓ Filled |
| M09-SCHED-016 | Day view side-by-side columns | ✓ Filled |
| M09-SCHED-017 | Week view color overlay | ✓ Filled |
| M09-SCHED-018 | Availability summary bar | ✓ Filled |
| M09-SCHED-019 | Select All / Clear All | ✓ Filled |
| M09-SCHED-020 | State filter dropdown | ✓ Filled |
| M02-DASH-020 | Quick Actions section (RN/MA/CT) | ✓ Filled |
| M02-DASH-021 | + New Patient header button | ✓ Filled |
| M02-QUEUE-014 | Nav links to role queues | ✓ Filled |
| M02-NAV-014 | Sidebar visual spec | ✓ Filled |
| M04-CPW-WIZ-021 | Step 6 heading spec | ✓ Filled |
| M04-CPW-WIZ-022 | Billing type + government program conditional panel | ✓ Filled |
| M05-CHART-020 | Lab recommendation custom dropdown | ✓ Filled |
| M07-INTAKE-010 | RN/MA/CT intake access entry points | ✓ Filled |

---

---

## SLACK GAP REVIEW — July 15, 2026 ✓ RESOLVED

Post-session Slack sweep surfaced 4 gaps. All addressed:

**Gap 1 — Zip Code Eligibility (NEW)** ✓  
Two new requirements written: M07-ELG-002 (intake gate — patient enters zip code, system validates against care product eligibility list) and M04-ELG-001 (Admin wizard config — per-product zip code list with CSV upload support).

**Gap 2 — Video Pre-Call Readiness (NEW)** ✓  
Care team tech check eliminated. New requirement M03-VID-001: patient portal self-serve video readiness test (camera, mic, connectivity) accessible from the appointment card. No care team action required.

**Gap 2b — WARM-TX-001 Updated** ✓  
Enriched with Jul 13 operational decisions: audio-only for immediate booking, 5-minute minimum window, provider-level configuration, parallel agent booking conflict resolution (first wins, second gets error).

**Gap 3 — NPI Sync (CLOSED — no action)** ✓  
No Healthie integration. Platform connects directly to Athena via API. No NPI sync disambiguation needed.

**Gap 4 — Video Join Window (NEW)** ✓  
New requirement M09-VID-001: "Join Call" button activates exactly 5 minutes before scheduled appointment start for both provider and patient. Disabled with countdown before that window. Deactivates 30 minutes after scheduled start if unused.

---

## FINAL SUMMARY

| Group | Items | Status |
|---|---|---|
| A — Legal & Compliance | 4 | ✓ All resolved — DB updated |
| B — Clinical & Operational | 6 | ✓ All resolved — DB updated |
| C — State Machine Logic | 4 | ✓ All resolved — DB updated |
| D — Integration Mock Specs | 5 | ⚙ Deferred to Engineering (Blake Lusenhop) |
| E — Reporting Payload | 1 | ✓ Resolved — DB updated |
| **Requirement Stubs** | **17** | **✓ All filled in DB** |
| **Slack Gap Review** | **4** | **✓ All resolved — 4 new reqs + 1 update** |
| **TOTAL** | **41 items** | **36 resolved, 5 to engineering** |
| **Active Requirements in DB** | **1,371** | **0 Open remaining** |
