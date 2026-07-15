#!/usr/bin/env python3
"""
Project Phoenix — June 18 Meeting Requirements v1
Source documents:
  - WI: GC Consult Prep (current-state workflow)
  - Dana/Justin Patient Scheduling meeting (2026-06-18)
  - Stephanie/Justin GC Workflow meeting (2026-06-18)
  - Blurb Writing SOP

25 new requirements across 8 modules:
  M01 (2), M02 (2), M04 (5), M05 (3), M07 (4), M08 (4), M09 (4), M10 (1)
"""

import sqlite3
from datetime import date

DB_PATH = '/Users/justin.woller/Documents/project-phoenix-demo/project_phoenix.db'
TODAY = str(date.today())

requirements = [

    # ══════════════════════════════════════════════════════════════
    # M01 — Roles & Responsibilities
    # ══════════════════════════════════════════════════════════════

    ('M01-RGT-066', 'M01 - Roles & Responsibilities', 'Care Team Roles', 'Admin Portal',
     'System must include a QA Reviewer role with rights scoped exclusively to documentation verification before consults proceed.',
     'The QA Reviewer role is assigned to staff responsible for verifying that required documentation (POA, guardian authorization, insurance cards) is correctly loaded in the system before a consult is allowed to proceed. Rights: view patient documentation uploaded to a consult record, approve or reject the QA stage on a consult, add notes to a QA review decision. The QA Reviewer cannot modify clinical documentation, schedule consults, or access provider chart content. QA stage defaults to required for all minors and patients requiring POA documentation; the QA stage can be disabled per care product in the Admin Portal.',
     'QA Reviewer can approve or reject the QA stage. Rejection blocks consult workflow and routes to GC Administrator queue. QA Reviewer cannot edit clinical records, modify patient demographic data, or access provider chart content.',
     'If no QA Reviewer is available and a consult approaches its scheduled time, the system generates an escalation alert to the GC Administrator queue.',
     'QA Reviewer role has no access to provider-facing chart content, consult notes, lab result details, or billing records.',
     'High', 'Active', 'M01', 'Clinical Ops / Compliance',
     'Jun 18 GC Workflow meeting — QA stage formalization', TODAY, TODAY, None),

    ('M01-RGT-067', 'M01 - Roles & Responsibilities', 'Care Team Roles', 'Admin Portal',
     'System must include a GC Administrator role with supervisory rights over the GCA team, clinical content library, QA failure resolution, and blurb workflow.',
     'The GC Administrator role is a supervisory clinical operations role with rights including: (1) Resolving QA failures routed from the QA stage — reviewing documentation, requesting resubmission from patients or care team, and approving resolution; (2) Managing the clinical content library — reviewing, publishing, archiving, and versioning blurb articles submitted as drafts by GCs; (3) Overseeing GCA queue management and consult prep workflow; (4) Managing the blurb request and assignment queue, including reassignment when a GC cannot complete an assigned blurb; (5) Read access to consult records and patient charts across assigned programs. GC Administrator does not have prescribing rights, clinical note authoring rights, or billing modification rights.',
     'GC Administrator receives all QA failure queue items. GC Administrator can publish and archive content library articles. GC Administrator can reassign blurb requests. GC Administrator has visibility into all GCA queue items across assigned programs.',
     'If GC Administrator resolves a QA failure and approves documentation, the consult workflow resumes automatically from the point it was blocked.',
     'GC Administrator does not have prescribing, clinical note editing, or billing modification rights. Access is scoped to their assigned programs.',
     'High', 'Active', 'M01', 'Clinical Ops',
     'Jun 18 GC Workflow meeting + WI GC Consult Prep — supervisory role above GCA', TODAY, TODAY, None),

    # ══════════════════════════════════════════════════════════════
    # M02 — Provider Portal
    # ══════════════════════════════════════════════════════════════

    ('M02-CLB-001', 'M02 - Provider Portal', 'Clinical Content Library', 'Provider Portal',
     'GCs and GCAs must be able to access the clinical content library from within the patient chart to reference blurbs and clinical articles during consult prep.',
     'A Clinical Resources panel is accessible from the provider chart view for users with GC or GCA roles. Users can search and browse published articles by gene name, topic, care product tag, or keyword. Articles open in a read-only side panel within the chart so the user does not lose their place in the consult prep workflow. Articles cannot be edited from within the chart view — editing requires navigation to the Admin Portal content library. The panel shows the article publication date and version. If a gene-level research study eligibility flag is set on the article, the panel displays a Research Eligible indicator to alert the GCA. If no published article exists for a searched gene, the panel displays a "Request Blurb" action that pre-populates the blurb request queue with the gene name and consult details.',
     'Clinical Resources panel accessible from patient chart for GC and GCA roles. Search by gene, topic, care product tag, keyword. Articles display publication date and version. Research eligibility flag shown when set. Request Blurb action available when no article exists.',
     'Draft (unpublished) articles are not visible in the chart panel — only Published articles appear. GC Administrators see draft articles in the Admin Portal content library management view.',
     'Clinical Resources panel is read-only from the chart. No article editing is available in the chart context.',
     'High', 'Active', 'M02', 'Engineering / UX',
     'WI GC Consult Prep + Jun 18 GC Workflow meeting — blurb access during consult prep', TODAY, TODAY, None),

    ('M02-LNK-001', 'M02 - Provider Portal', 'Consult Management', 'Provider Portal',
     'Providers and GCAs must be able to view linked consults within a patient chart and import prior consult notes from linked consults into the current consult.',
     'When a consult is linked to another consult (pre-test/post-test pair, NIH research consult, rescheduled consult), a Linked Consults section appears in the patient chart sidebar. Each linked consult shows: consult ID, type, date, status, and link type label (Pre-Test, Post-Test, NIH Research, Rescheduled From). The user can click a linked consult to view its details in a read-only side panel. If the linked consult has a completed or draft note, an Import Note action is available. Import copies the note content into the current consult draft note field. The source note is not modified. The import event is logged to the activity timeline with a reference to the source consult ID.',
     'Linked Consults section visible in chart when at least one linked consult exists. Link type is labeled for each linked consult. Prior note importable into current draft. Import is a copy — source note is not modified. Import logged to activity timeline.',
     'A consult can be linked to multiple prior consults (e.g., a post-test consult may have both a pre-test consult and a rescheduled prior attempt). All linked consults are shown in the sidebar.',
     'Consult linking is not retroactively available for historical consults from the legacy platform unless explicitly migrated.',
     'High', 'Active', 'M02', 'Engineering',
     'WI GC Consult Prep (pre/post-test note import) + Jun 18 NIH linked consult discussion', TODAY, TODAY, None),

    # ══════════════════════════════════════════════════════════════
    # M04 — Admin Portal
    # ══════════════════════════════════════════════════════════════

    ('M04-CLB-001', 'M04 - Admin Portal', 'Clinical Content Library', 'Admin Portal',
     'Admin Portal must include a clinical content library where administrators and authorized GCs can create, manage, and publish clinical articles accessible to the care team.',
     'The Clinical Content Library is a database-driven content management system within the Admin Portal. V1 features: (1) Article creation — GCs can create Draft articles; GC Administrators review and publish; (2) Article workflow states: Draft → Review → Published → Archived; (3) Rich text editor for article body content; (4) Article search and browse by gene name, topic, care product tag, author, and publication date; (5) Version history — each published update creates a new version with prior versions archived and retrievable; (6) Published articles are accessible in the provider chart Clinical Resources panel. V2 enhancement: AI-assisted content generation and application of blurb content to consult note drafting.',
     'GCs can create Draft articles. GC Administrators publish articles. Articles progress through Draft → Review → Published → Archived states. Version history maintained per article. Published articles accessible in provider chart panel.',
     'An article submission for a gene that already has a Published article prompts the reviewer: "A current article exists for this gene. Publish this version to supersede it?"',
     'Published articles cannot be deleted — they must be archived. Archived articles remain in the admin library for reference but are not visible in the chart panel.',
     'High', 'Active', 'M04', 'Engineering / Clinical Ops',
     'Jun 18 GC Workflow meeting — retire spreadsheets, blurb library to platform DB', TODAY, TODAY, None),

    ('M04-CLB-002', 'M04 - Admin Portal', 'Clinical Content Library', 'Admin Portal',
     'Each article in the clinical content library must carry structured metadata that enables search, version management, and care team decision support.',
     'Required metadata fields for every article: (1) Title — gene name or topic; (2) Gene symbol — standardized HGNC gene symbol; (3) Topic category — from controlled list (Oncology, Cardiology, Neurology, PGx, Carrier Screening, Research); (4) Care product tags — associated care products this article applies to; (5) Inheritance pattern — Autosomal Dominant, Autosomal Recessive, X-Linked, Mitochondrial, Multiple; (6) Variant classification applicability — PV, LPV, VUS, Carrier; (7) Author — submitting GC name; (8) Published by — GC Administrator who approved; (9) Publication date and version number; (10) Last reviewed date; (11) Research study eligibility flag — Boolean indicating whether the gene qualifies for research study linked consult creation (e.g., NIH ACMG81). The research study eligibility flag drives the Research Eligible indicator in the chart Clinical Resources panel and the NIH research consult prompt logic.',
     'All required metadata fields must be completed before an article can be submitted for review. Research study eligibility flag is configurable per article. Flag is surfaced in the chart panel to alert GCA when positive.',
     'An article can have multiple gene symbols and multiple care product tags. Articles without a last reviewed date within 12 months generate an admin alert prompting review.',
     'Gene symbol is a required field and must match an entry in the HGNC standard gene symbol list — free-text gene symbols that do not match are flagged for confirmation.',
     'High', 'Active', 'M04', 'Engineering / Clinical Ops',
     'Blurb Writing SOP + WI GC Consult Prep — article metadata for search and eligibility', TODAY, TODAY, None),

    ('M04-QA-001', 'M04 - Admin Portal', 'QA Stage Configuration', 'Admin Portal',
     'Admin Portal must allow care product administrators to configure the QA documentation review stage per care product, including trigger conditions and default behavior.',
     'A QA Stage Configuration step in the care product wizard allows admins to: (1) Enable or disable the QA stage for this care product — default is enabled; (2) Configure automatic trigger conditions — QA stage is automatically triggered when: patient is under 18, orderer is not the patient (third-party order), or POA documentation is flagged as required; (3) Allow manual trigger — GCA can manually flag any consult for QA review regardless of automatic trigger conditions; (4) QA failure behavior is fixed and cannot be disabled — a failed QA stage always blocks the consult workflow and routes a resolution task to the GC Administrator queue; (5) Configure resolution notification recipients — who is notified when QA is resolved (GCA, scheduling team, patient).',
     'QA stage can be enabled or disabled per care product. Default is enabled. Trigger conditions are configurable. QA failure always blocks workflow and routes to GC Administrator queue — this behavior is not configurable. QA stage appears as a tracked stage in the consult workflow timeline.',
     'If QA is disabled for a care product, consults for that product bypass the QA stage entirely regardless of patient age or order type.',
     'QA stage configuration changes apply to new consults only — consults already in progress are not affected.',
     'High', 'Active', 'M04', 'Engineering / Compliance',
     'Jun 18 GC Workflow meeting — QA stage formalization, configurable per care product', TODAY, TODAY, None),

    ('M04-CHK-001', 'M04 - Admin Portal', 'Pre-Consult Checklist Configuration', 'Admin Portal',
     'Admin Portal must allow administrators to configure a role-based pre-consult checklist per care product that GCAs and care team staff complete in the patient chart before each consult.',
     'A Pre-Consult Checklist configuration step in the care product wizard allows admins to: (1) Enable or disable the pre-consult checklist for this care product — default is disabled until configured; (2) Add checklist items from a library of standard item types: Document Verify (confirm a document is uploaded and readable), Field Confirm (verify a data field is populated with expected value), Checkbox (confirm a manual step is complete), Free Text Note (care team adds a freeform prep note); (3) Assign each item to a user role — GCA, PSR, PCC, or RN — role-assigned items are only visible to users with that role; (4) Mark each item as Required or Optional; (5) Add per-item instructional text visible to the care team member; (6) Reorder items via drag-and-drop. When active, the checklist appears as a Consult Prep tracked stage in the consult workflow. All Required items must be completed before the consult can advance.',
     'Checklist items are role-assigned — each role sees only their assigned items. Required items block workflow advancement until completed. Optional items generate a reminder but do not block. Checklist stage is tracked in the consult workflow timeline. Configurable per care product.',
     'A care product can have up to 30 checklist items. Items can be assigned to multiple roles (e.g., both GCA and PSR must confirm results are uploaded).',
     'If a consult is rescheduled after the checklist was partially completed, completed items are retained and only incomplete required items must be finished.',
     'High', 'Active', 'M04', 'Engineering / Clinical Ops',
     'Jun 18 GC Workflow meeting — configurable care team review fields with visual confirmation', TODAY, TODAY, None),

    ('M04-NIH-001', 'M04 - Admin Portal', 'Research Consult Configuration', 'Admin Portal',
     'The care product wizard must allow configuration of research study linked consult creation, so that GCAs are prompted to create a linked research consult when a patient meets eligibility criteria.',
     'A Research Consult Configuration step in the care product wizard allows admins to: (1) Enable research study consult linkage for this care product — default is disabled; (2) Select the research program type from a configured list (e.g., NIH ACMG81 Gene Panel); (3) Configure eligibility trigger — system prompts GCA to create a linked research consult when the content library article for the patient\'s result gene has the Research Study Eligibility flag set to Yes and the variant classification is PV or LPV; (4) Configure prompt behavior — prompt only (GCA decides) or auto-create linked consult. When a GCA is prompted, they can initiate the research consult creation from within the current consult chart. The research consult is created as a linked consult with link type "Research" and pre-populated with the originating consult ID, patient data, and care product.',
     'Research consult linkage is configurable per care product. Eligibility trigger uses content library article research flag and variant classification. GCA is prompted when criteria are met. Research consult created as a linked consult. Link type labeled "Research".',
     'A patient may only have one active linked research consult per research program per originating consult.',
     'Research consult linkage is not retroactively applied to historical consults. Automated eligibility algorithm (evaluating gene inheritance patterns) is V2 scope.',
     'Medium', 'Active', 'M04', 'Engineering / Clinical Research',
     'Jun 18 discussion — NIH eligibility is a linked consult type, configured in care product wizard', TODAY, TODAY, None),

    # ══════════════════════════════════════════════════════════════
    # M05 — Async Consultation
    # ══════════════════════════════════════════════════════════════

    ('M05-LNK-001', 'M05 - Async Consultation', 'Consult Linking', 'Provider Portal',
     'Platform must support linking two consult records together with a defined relationship type to enable pre/post-test continuity, research consults, and reschedule continuity.',
     'Consult linking allows two consult records to be associated with a defined relationship type: (1) Pre-Test — this consult is the pre-test consult for a linked post-test consult; (2) Post-Test — this consult is the post-test following a prior pre-test consult; (3) Research — this consult is a research study consult linked to an originating clinical consult; (4) Rescheduled From — this consult is a rescheduled replacement of a prior cancelled consult. A consult can participate in multiple links (e.g., a post-test consult may be linked to a pre-test AND to an NIH research consult). Links are visible in the consult record detail and in the chart sidebar. Links can be created manually by GCA or GC Administrator, or automatically by the system based on care product configuration. All link creation events are logged to the activity timeline.',
     'Consult links have defined relationship types. A consult can have multiple links. Links are bidirectional — both consults display the link. Link creation logged to activity timeline. Manual and system-generated link creation both supported.',
     'A pre-test/post-test link prefers continuity of the same GC — when the post-test consult is assigned to a different GC, the system flags this in the scheduling interface and prompts for confirmation.',
     'Consult links cannot be deleted — they can only be marked inactive. This preserves the full audit trail of consult relationships.',
     'High', 'Active', 'M05', 'Engineering',
     'WI GC Consult Prep (pre/post-test continuity) + Jun 18 NIH research consult discussion', TODAY, TODAY, None),

    ('M05-LNK-002', 'M05 - Async Consultation', 'Consult Note Continuity', 'Provider Portal',
     'When a consult is linked to a prior consult, the prior consult draft or completed note must be importable into the current consult note field.',
     'For any consult with a linked prior consult, the chart note interface displays an Import from Linked Consult option when the linked consult has a draft or completed note available. When selected, the user is shown a read-only preview of the prior note. Confirming the import copies the note content into the current consult draft note field — the source note is not modified. The import event is logged to the activity timeline with a reference to the source consult ID and the source consult date. The user can edit the imported note after import. For rescheduled consults specifically, the system proactively prompts the GCA during consult prep: "A prior note exists from consult [ID]. Import it into this consult?" This prompt only appears once per consult if the GCA has not already imported a note.',
     'Import option shown only when a linked consult has an available note or draft. Import is a copy — source note unchanged. Import event logged to activity timeline with source consult reference and date. Proactive prompt shown for rescheduled consults during consult prep.',
     'For post-test consults where the same GC is not available and a different GC is assigned, the import option is still available so the new GC can review the prior pre-test note.',
     'Note import is not available for Research link type — research consults are independent clinical encounters.',
     'High', 'Active', 'M05', 'Engineering / Clinical Ops',
     'WI GC Consult Prep — prior consult note import on reschedule and pre/post-test continuity', TODAY, TODAY, None),

    ('M05-CPX-001', 'M05 - Async Consultation', 'Consult Record Fields', 'Provider Portal',
     'Each consult record must capture the consult initiator, indicating whether the consult was initiated by the platform/clinical team or by the patient.',
     'A Consult Initiator field on each consult record captures one of two values: (1) Platform-Initiated — the consult was triggered by the clinical team, automated care product logic, or an abnormal result workflow; (2) Patient-Initiated — the patient requested the consult themselves. This field is set by the GCA during consult prep or automatically by the system during consult creation (system-generated consults default to Platform-Initiated; patient self-scheduled consults default to Patient-Initiated). GCA can override the default value. The Consult Initiator field is used for billing classification, operational reporting, and audit purposes. It is visible in the consult detail view and included in all data exports.',
     'Consult Initiator field is required on all consult records. System-generated consults default to Platform-Initiated. Patient self-scheduled consults default to Patient-Initiated. GCA can override the default. Field is included in exports and visible in consult detail.',
     'For care products where all consults are one type (e.g., all Stratify consults are platform-initiated), the field can be pre-set in the care product configuration to eliminate the need for GCA override.',
     'Consult Initiator is immutable after the consult note is signed and the chart is closed.',
     'Medium', 'Active', 'M05', 'Engineering / Billing',
     'WI GC Consult Prep — Complexity Level field (PWN-initiated vs. patient-initiated)', TODAY, TODAY, None),

    # ══════════════════════════════════════════════════════════════
    # M07 — Intake Process
    # ══════════════════════════════════════════════════════════════

    ('M07-MIN-001', 'M07 - Intake Process', 'Minor Patient Ordering', 'All',
     'Platform must enforce that test orders and consult intakes for minor patients are placed only by a confirmed parent or legal guardian.',
     'When intake is initiated for a patient under 18 years of age, the platform requires the orderer to confirm their relationship: Parent, Legal Guardian, or Other. If Other is selected, the intake flags a POA documentation requirement and cannot proceed until documentation is provided. This rule is a hard platform enforcement — minor intake cannot complete without a confirmed parent or guardian relationship or documented POA. The rule applies uniformly across all care products and clients; no client-specific exceptions are permitted. The GCA receives a notification when a minor consult enters the queue that includes the relationship confirmation status. If a patient turns 18 before their consult date, the minor flag is automatically cleared.',
     'All intake for minors requires orderer relationship confirmation. Parent or Legal Guardian clears the requirement. Other triggers POA documentation requirement. Intake cannot complete without confirmation. Applies across all care products with no exceptions. Minor flag auto-clears when patient turns 18.',
     'If patient age cannot be determined from the record at intake, the system applies the minor requirement by default until age is confirmed.',
     'The age threshold for minor status is under 18 years. Patients who are exactly 18 on the intake date are not considered minors.',
     'High', 'Active', 'M07', 'Engineering / Compliance',
     'Jun 18 GC Workflow meeting — standardize minor intake across all partners; company-wide policy', TODAY, TODAY, None),

    ('M07-POA-001', 'M07 - Intake Process', 'POA Documentation', 'All',
     'Platform must require and track Power of Attorney or consent documentation when a consult is ordered by someone other than the adult patient themselves.',
     'When the orderer of a consult is not the patient (third-party order: parent for an adult patient, spouse, sibling, caregiver, or other), the platform requires POA or consent documentation before the consult can advance past the QA stage. Accepted documentation forms: (1) Uploaded POA document; (2) Verbal consent attestation documented by GCA with date and GCA name; (3) Written consent form. The POA requirement is flagged on the consult record as a pending documentation item. GCA is responsible for obtaining documentation and uploading or attesting to it. POA documentation is stored on the consult record and is accessible in the patient chart. If a prior consult for the same patient already has a documented POA from the same third party, the GCA is shown a reference to the prior POA and must confirm it is still valid.',
     'Third-party order triggers POA documentation requirement on the consult record. Accepted forms: uploaded document, GCA verbal attestation, written consent. POA must be documented before consult can advance past QA stage. Prior POA surfaced as reference for GCA confirmation.',
     'POA requirement does not apply when the orderer is the patient themselves or when a minor is ordered for by a confirmed parent or legal guardian.',
     'Consult cannot proceed to the GC without documented POA when required. This is enforced by the QA stage — QA cannot be approved without POA documentation complete.',
     'High', 'Active', 'M07', 'Engineering / Compliance / Legal',
     'Jun 18 GC Workflow meeting — POA enforcement; WI GC Consult Prep — POA workflow', TODAY, TODAY, None),

    ('M07-MBR-001', 'M07 - Intake Process', 'Member Lookup at Intake', 'All',
     'During intake for health plan channel patients, the system must look up the patient in the Members database and pre-populate demographic and eligibility data.',
     'When a consult or order is initiated for a health plan channel patient, the intake process performs a Member lookup using available identifiers (name + date of birth or member ID). If a matching member record is found in the Members DB, eligible demographic fields are pre-populated: first name, last name, date of birth, address, insurance plan, health plan name, coverage dates, and care product eligibility flags. The intake agent or patient can review and confirm pre-populated fields rather than entering them manually. Confirmed fields are locked for the intake session. If no member record is found, intake proceeds with manual entry and a No Eligibility Match flag is raised on the consult record for eligibility verification follow-up. If multiple records match the lookup criteria, the agent is shown a selection list.',
     'Member lookup at intake for health plan channel. Match on member ID or name + DOB. Pre-populated fields shown for confirmation. No-match flag raised on consult record. Multiple matches prompt agent selection. DTC channel patients do not use member lookup.',
     'If a member record is found but coverage dates are expired, the intake proceeds with a Coverage Expired warning displayed to the agent.',
     'Direct-to-consumer (DTC) patients do not go through Member lookup — intake proceeds with standard manual demographic entry.',
     'High', 'Active', 'M07', 'Engineering',
     'Dana/Justin scheduling meeting Jun 18 — eligibility CSV pre-population, members DB architecture', TODAY, TODAY, None),

    ('M07-MBR-002', 'M07 - Intake Process', 'Member to Patient Conversion', 'All',
     'A health plan member must be automatically promoted to a full patient record upon creation of their first consult.',
     'Health plan members exist in the Members database before their first consult. When a consult is created for a member, the system promotes the member to a patient record: (1) A patient account is created using the member demographic data as the foundation; (2) The member record in the Members DB is flagged as Converted to Patient with a reference to the patient ID and conversion date; (3) The patient record links back to the originating member record for audit purposes; (4) Patient portal access is provisioned upon patient record creation; (5) Subsequent intakes for the same person use the patient record — the member record is not updated after conversion. Members who never have a consult remain as member-only records without patient portal access.',
     'First consult creation triggers member-to-patient promotion. Patient record inherits member demographic data. Member record flagged as converted with patient reference. Portal access provisioned at conversion. All future lookups use patient record.',
     'If a member has already been converted to a patient and a new consult intake performs a member lookup, the system surfaces the existing patient record and skips the conversion step.',
     'Member-to-patient conversion is irreversible. A converted member cannot be reverted to member-only status.',
     'High', 'Active', 'M07', 'Engineering',
     'Dana/Justin scheduling meeting Jun 18 — members become patients on first consult', TODAY, TODAY, None),

    # ══════════════════════════════════════════════════════════════
    # M08 — Notification Engine
    # ══════════════════════════════════════════════════════════════

    ('M08-BLB-001', 'M08 - Notification Engine', 'Blurb Request Queue', 'Provider Portal',
     'Platform must generate a blurb request queue event when a GCA identifies that a required clinical content article does not exist or is outdated for an upcoming consult.',
     'When a GCA determines during consult prep that a gene blurb is missing or outdated (no published article in the content library for that gene, or the existing article is dated before 1/1/2025), the GCA triggers a blurb request from the chart Clinical Resources panel. The request is submitted as a queue event and automatically includes: gene name, consult date and time, assigned GC name, link to the patient lab results page (not the consult page — for PHI protection), care product tag, and variant classification. The request appears in the GC Administrator queue and is visible to authorized GCs who can claim blurb assignments. Requests are not patient-identifying in the queue view — they show gene name and consult details only. This replaces the current Slack #unusual_gc_cases workflow.',
     'Blurb request includes gene name, consult date/time, GC name, lab results link, care product tag, variant classification. Queue item is not patient-identifying — no patient name or PHI in queue view. Appears in GC Administrator queue and GC-assignable blurb queue.',
     'If a blurb request is submitted for a gene that already has a published article dated after 1/1/2025, the system warns: "A current article exists for this gene. Are you sure you want to request a new one?"',
     'Blurb requests for the same gene within the same 7-day window are deduplicated — a second request updates the existing open request rather than creating a duplicate.',
     'High', 'Active', 'M08', 'Engineering / Clinical Ops',
     'Blurb Writing SOP + WI GC Consult Prep — replaces Slack #unusual_gc_cases workflow', TODAY, TODAY, None),

    ('M08-BLB-002', 'M08 - Notification Engine', 'Blurb SLA Tracking', 'Provider Portal',
     'Platform must track and enforce a 24-hour SLA on blurb requests from submission to completion, with escalation to GC Administrator when the SLA is at risk.',
     'Each blurb request carries two SLA windows: (1) 24 hours from submission to GC claim; (2) 24 hours from claim to article submission for review. SLA status is displayed on the queue item using a color indicator: Green (more than 12 hours remaining), Amber (6 to 12 hours remaining), Red (less than 6 hours remaining). When a request reaches Amber without a GC claim, a notification is sent to the GC team. When a request reaches Red, the GC Administrator receives an alert and must claim or reassign the blurb. When a blurb is published before the consult, the SLA is marked Met. If a consult occurs without a completed blurb, the SLA is logged as Missed. For consults scheduled within 24 hours of the request, SLA windows are compressed proportionally and flagged as Urgent. SLA clock pauses and resets when a consult is rescheduled.',
     'Two SLA windows: 24 hours to claim, 24 hours from claim to submission. Color-coded status on queue item. Amber triggers GC team notification. Red triggers GC Administrator alert. Met and Missed SLA outcomes logged per request. Urgent flag for short-notice consults.',
     'If a blurb request is associated with a consult that is subsequently cancelled, the request is automatically marked Cancelled and removed from the active queue.',
     'SLA tracking applies to the overall request from submission to publication — partial completion (draft submitted but not published) does not count as SLA met.',
     'High', 'Active', 'M08', 'Engineering / Clinical Ops',
     'Blurb Writing SOP — 24-hour completion target before consult', TODAY, TODAY, None),

    ('M08-QAF-001', 'M08 - Notification Engine', 'QA Failure Routing', 'All',
     'When a QA Reviewer rejects a consult QA stage, the platform must block the consult workflow and route a resolution task to the GC Administrator queue.',
     'When a QA Reviewer rejects a consult QA stage (documentation incomplete, incorrect, or missing), the platform: (1) Blocks the consult workflow — the consult cannot advance past the QA stage; (2) Creates a QA failure queue item in the GC Administrator queue containing: consult ID, patient name, scheduled consult date and time, reason for failure entered by the QA Reviewer, list of missing or incorrect documents, and the QA Reviewer name; (3) Sends a notification to the assigned GCA with the required corrective action; (4) Allows the GCA or GC Administrator to trigger a patient notification from within the queue item when patient action is required (e.g., re-upload a document); (5) Automatically resumes the consult workflow from the blocked stage when the GC Administrator approves the QA resolution. If the QA failure occurs within 24 hours of the scheduled consult, the queue item is flagged Urgent with a countdown timer.',
     'QA failure creates a GC Administrator queue item. Consult workflow blocked until GC Administrator re-approves. GCA notified with corrective action. Patient notification can be triggered from the queue item. Workflow resumes automatically on GC Administrator approval. Urgent flag within 24 hours of consult.',
     'Multiple QA failures on the same consult accumulate in the consult activity timeline — each failure and resolution is logged separately.',
     'QA failure queue items are visible only to GC Administrators and the assigned GCA. They are not visible to the patient or to clinical providers.',
     'High', 'Active', 'M08', 'Engineering / Compliance',
     'Jun 18 GC Workflow meeting — QA failure blocks workflow, routes to GC Administrator queue', TODAY, TODAY, None),

    ('M08-TZ-001', 'M08 - Notification Engine', 'Timezone-Aware GC Notifications', 'Provider Portal',
     'All consult-related notifications sent to a Genetic Counselor must display the consult date and time in the GC\'s configured local timezone.',
     'When a notification is sent to a GC regarding a consult (new assignment, prep reminder, schedule change, cancellation), the consult date and time in the notification body must be displayed in the GC\'s configured local timezone, not in UTC or system time. A timezone label is always shown alongside the time (e.g., "2:00 PM EST"). The GC\'s timezone is configured in their provider profile and defaults to the timezone of their primary licensed practice state. When a notification is also sent to the GCA who prepped the consult, the consult time is displayed in the GCA\'s configured timezone. Timezone-aware formatting applies to all notification channels: in-platform, email, and SMS.',
     'Consult time in GC notifications uses GC configured timezone. Timezone label always shown. GCA receives time in their timezone. GC timezone configurable in provider profile. Applies to in-platform, email, and SMS channels.',
     'If a GC has not configured a timezone in their profile, the system uses the timezone of the care product primary service state as a fallback.',
     'Timezone conversion applies at notification generation time — stored notification records retain UTC timestamps internally.',
     'Medium', 'Active', 'M08', 'Engineering',
     'WI GC Consult Prep — "note consult ID, scheduled date and time in GC\'s own time zone"', TODAY, TODAY, None),

    # ══════════════════════════════════════════════════════════════
    # M09 — Scheduling
    # ══════════════════════════════════════════════════════════════

    ('M09-CHK-001', 'M09 - Scheduling', 'Pre-Consult Checklist Stage', 'Provider Portal',
     'When a care product has an active pre-consult checklist, the checklist must appear as a tracked Consult Prep stage in the workflow, accessible to the GCA in the patient chart.',
     'For care products with an active pre-consult checklist, a Consult Prep stage appears in the consult workflow timeline after scheduling and before the consult session. In the patient chart, the GCA sees the checklist panel showing all items assigned to their role. Item interactions: Document Verify items show document upload status with a Confirm button; Field Confirm items show the current field value with a Confirm button; Checkbox items are manually checked off; Free Text items provide a text input field. The stage header shows overall progress (e.g., 4 of 6 required items complete). All Required items must be complete before the consult can advance. The completed checklist stage is logged to the activity timeline. If a consult is rescheduled after partial completion, completed items are retained.',
     'Checklist stage appears in workflow for care products with active checklist. GCA sees only their role-assigned items. Required items must all be complete before workflow advances. Progress shown on stage header. Completion logged to activity timeline. Partial progress retained on reschedule.',
     'If a GCA completes the checklist and a consult is later rescheduled, a prompt asks the GCA to re-verify time-sensitive items (e.g., results upload confirmation) since documents may have changed.',
     'The checklist stage is completely skipped for care products that do not have a checklist configured.',
     'High', 'Active', 'M09', 'Engineering / UX',
     'Jun 18 GC Workflow meeting — configurable care team review fields with visual confirmation', TODAY, TODAY, None),

    ('M09-PRV-001', 'M09 - Scheduling', 'Provider Relationship Indicators', 'Provider Portal',
     'The scheduling interface must display prior relationship indicators on provider selection to support continuity of care preferences.',
     'In the provider selection step of the scheduling interface, providers with whom the patient has had at least one prior completed consult show a Prior Consult badge with the date of their most recent consult. When care product logic requires same-GC continuity (e.g., post-test consult following a linked pre-test), the scheduling interface pre-selects the prior GC and shows a note explaining the reason. The scheduler can override the pre-selection at any time. If the preferred prior provider is unavailable at the requested time, the system shows both the next available time with that specific provider and the next available time with any provider, so the scheduler can choose.',
     'Prior Consult badge shown with most recent date when patient has prior consult history with a provider. Pre-selection applied when care product continuity logic requires same GC. Override always available. Unavailability handled by showing next available options for preferred vs. any provider.',
     'Prior relationship indicators are scoped to the care product — a prior consult in a different care product does not generate a badge unless the same GC is licensed for both.',
     'Prior relationship data is derived from the consult record history. It is not configurable by the scheduler.',
     'Medium', 'Active', 'M09', 'Engineering / UX',
     'Dana/Justin scheduling meeting Jun 18 — provider preference based on prior relationship', TODAY, TODAY, None),

    ('M09-PRV-002', 'M09 - Scheduling', 'Provider Preference Filters', 'Provider Portal',
     'The scheduling interface must support preference filters for provider attributes including gender preference, to support patient preferences and care product requirements.',
     'The scheduling interface includes a provider preference filter panel. Available filters: (1) Gender preference — Male, Female, No preference (default: No preference); (2) Language spoken — available when provider language data is configured in provider profiles; (3) State license — auto-applied based on patient state of residence and cannot be deselected. Selected filters narrow the available provider list. If no providers match the applied filters for the requested time slot, the system shows: the next available date and time with providers matching the filters. Filters can be cleared to show all licensed available providers. Patient preference filters (gender, language) are stored on the patient record and pre-applied on future scheduling interactions — patients or schedulers can change stored preferences.',
     'Gender and language preference filters available. State license filter auto-applied and not removable. No-match shows next available time with matching providers. Filters can be cleared. Stored preference pre-applied on future scheduling.',
     'Provider attribute data (gender, languages) is configured in the provider profile in the Admin Portal and must be populated for filters to function.',
     'Preference filters do not override state license requirements. A provider must be licensed in the patient state regardless of other preference filters.',
     'Medium', 'Active', 'M09', 'Engineering / UX',
     'Dana/Justin scheduling meeting Jun 18 — provider preference filters including gender', TODAY, TODAY, None),

    ('M09-SVC-001', 'M09 - Scheduling', 'Service Type Duration Validation', 'Provider Portal',
     'At scheduling, the platform must validate that the booked consult duration matches the configured service type duration for the care product and auto-correct or alert on mismatches.',
     'Each care product in the Admin Portal has a service type configuration mapping service type name to required consult duration (e.g., Results Delivery = 30 minutes, Pre-Test Consult = 60 minutes). At scheduling, the platform validates the booked duration against the configuration. Validation behavior by scheduling channel: (1) Patient self-scheduling links — only the correct duration is offered; no mismatch is possible; (2) External scheduling or API intake — if a wrong duration is received, the platform auto-corrects it to the configured duration and logs a Correction event to the consult record with the original and corrected durations; (3) Manual scheduling by GCA or scheduler — if a wrong duration is selected, a validation warning is shown before save: "This service type requires a [X]-minute session. Saving will set the duration to [X] minutes." Both the original submitted duration and the corrected duration are logged.',
     'Self-scheduling links offer configured duration only. External and API scheduling auto-corrects with logged correction event. Manual scheduling shows validation warning before save. Original and corrected durations both logged.',
     'If a care product has multiple service types with different required durations, validation applies per service type — the system must know which service type applies to correctly validate.',
     'Service type duration validation applies to new consult creation only. Rescheduled consults inherit the service type and duration from the original consult.',
     'High', 'Active', 'M09', 'Engineering',
     'WI GC Consult Prep — GCA must manually correct wrong durations; Jun 18 service type enforcement', TODAY, TODAY, None),

    # ══════════════════════════════════════════════════════════════
    # M10 — Integrations
    # ══════════════════════════════════════════════════════════════

    ('M10-ELG-001', 'M10 - Integrations', 'Eligibility Data Ingestion', 'All',
     'Platform must support ingestion of health plan eligibility CSV files into a Members database to enable demographic pre-population at scheduling and intake.',
     'Health plan eligibility data is received as structured CSV files from health plan partners. Required fields per record: member ID, first name, last name, date of birth, address, insurance plan name, health plan identifier, coverage start date, coverage end date, care product eligibility flags. The ingestion process: (1) Validates file format and required fields before loading — files with validation errors are rejected and an error report is generated; (2) Creates new member records for members not yet in the DB; (3) Updates existing member records on subsequent file loads (matched on member ID or name + DOB); (4) Flags members whose coverage end date is in the past as Coverage Expired; (5) Generates an ingestion summary report: records added, records updated, coverage expired flags set, validation errors. The Members DB is a separate data store from the Patient DB. Members are promoted to patients only upon first consult creation (see M07-MBR-002). Eligibility files are processed on a configurable schedule: daily automated load, weekly, or manual on-demand upload.',
     'CSV validated before loading — invalid files rejected with error report. New members created. Existing members updated on re-load. Expired coverage flagged. Ingestion summary report generated after each run. Members DB separate from Patient DB. Schedule configurable.',
     'If an eligibility file contains a record for a member already converted to a patient, the patient record demographics are updated rather than creating a new member record.',
     'Eligibility files must be transmitted via secure file transfer (SFTP or equivalent). Unsecured transmission is not accepted.',
     'High', 'Active', 'M10', 'Engineering / Partnerships',
     'Dana/Justin scheduling meeting Jun 18 — health plan eligibility CSV into members DB', TODAY, TODAY, None),

]

# ══════════════════════════════════════════════════════════════
# DB INSERT
# ══════════════════════════════════════════════════════════════

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute('SELECT COUNT(*) FROM requirements')
count_before = c.fetchone()[0]

inserted = 0
skipped = 0
for req in requirements:
    req_id = req[0]
    c.execute('SELECT req_id FROM requirements WHERE req_id = ?', (req_id,))
    if c.fetchone():
        print(f'  SKIP (exists): {req_id}')
        skipped += 1
    else:
        c.execute('''INSERT INTO requirements
            (req_id, module_id, section, portal, user_story, requirement, rule, acceptance, edge_cases,
             priority, status, jira_epic, owner, source, date_added, last_updated, exported_version)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', req)
        print(f'  INSERTED: {req_id}')
        inserted += 1

conn.commit()

c.execute('SELECT COUNT(*) FROM requirements')
count_after = c.fetchone()[0]
conn.close()

print(f'\nDone.')
print(f'  Before : {count_before}')
print(f'  Inserted: {inserted}')
print(f'  Skipped : {skipped}')
print(f'  After   : {count_after}')
print(f'\nExpected 25 insertions.')
