#!/usr/bin/env python3
"""
Care Team Requirements — DB Commit Script v1
June 18, 2026
Source: Care Team Workflow Overview docs + Justin/Care Team meeting (Jun 18)
Modules: M01, M02, M03, M04, M05, M08, M09, M10
"""

import sqlite3
from datetime import date

DB_PATH = '/Users/justin.woller/Documents/project-phoenix-demo/project_phoenix.db'
TODAY = str(date.today())

requirements = [

    # ─────────────────────────────────────────────
    # M01 — Roles & Responsibilities
    # ─────────────────────────────────────────────

    ('M01-PRF-008', 'M01 - Roles & Responsibilities', 'Profile Definitions', 'Provider Portal',
     'PSR — Patient Service Representative: Frontline outbound and inbound call agent for lab result delivery and consult scheduling.',
     'PSR is a non-clinical Care Team role. PSR can: read patient records and consult status; write outreach attempt logs to activity timeline; generate scheduling links; access the PSR queue. PSR cannot: write to clinical chart sections; prescribe; approve orders; access provider-only views.',
     'PSR rights: Read (patient record, consult status, lab results). Write (activity timeline notes, outreach logs). No Edit or Delete on clinical objects. Scheduling link generation enabled.',
     'PSR can view full patient consult context. PSR cannot alter clinical documentation or provider notes.',
     'PSR attempting to edit clinical chart receives permission denied. Scheduling link generation logs event to activity timeline automatically.',
     'High', 'Active', 'M01', 'Care Team Ops', 'Care Team Workflow Overview — Jun 2026', TODAY, TODAY, None),

    ('M01-PRF-009', 'M01 - Roles & Responsibilities', 'Profile Definitions', 'Provider Portal',
     'PCC — Patient Care Coordinator: Manages the telehealth consult lifecycle from referral review through physician oversight and prescription coordination.',
     'PCC is an operational Care Team role with elevated rights over PSR. PCC can: review and change referral status; reassign consults between providers; log physician TAT issues; manage Care Team queue; access prescription coordination tools. PCC cannot: write clinical documentation; prescribe; approve lab orders.',
     'PCC rights: Read (patient record, referral, consult, provider assignment). Write (referral status, outreach notes, activity timeline). Edit (referral assignment, consult routing). No Delete on clinical objects. TAT monitoring queue access enabled.',
     'PCC can move a consult from Open to any non-clinical status. PCC can reassign provider on a consult. PCC cannot modify clinical chart content.',
     'PCC reassigning a provider logs the action with timestamp and user ID to activity timeline. PCC cannot delete consult records.',
     'High', 'Active', 'M01', 'Care Team Ops', 'Care Team Workflow Overview — Jun 2026', TODAY, TODAY, None),

    ('M01-PRF-010', 'M01 - Roles & Responsibilities', 'Profile Definitions', 'Provider Portal',
     'GCA — Genetic Counseling Assistant: Provides operational and administrative support for the genetics program including consult scheduling, note processing, and client coordination.',
     'GCA is a genetics-specific Care Team role. GCA can: view patient records and lab results; schedule GC consults; add outreach notes to activity timeline; access the GCA/Genetics queue; review and submit GC consult notes within the platform. GCA cannot: write clinical documentation; prescribe; approve orders; access non-genetics care products.',
     'GCA rights: Read (patient record, lab results, GC consult notes). Write (activity timeline notes, GC scheduling). Edit (GC consult note submission status). Genetics queue access enabled. Non-genetics care product access disabled.',
     'GCA can schedule a GC consult from within the platform and log the scheduling event to the activity timeline.',
     'GCA attempting to access a non-genetics care product queue receives access denied. GCA note submissions trigger a review-complete event on the consult record.',
     'High', 'Active', 'M01', 'Care Team Ops', 'Care Team Workflow Overview — Jun 2026', TODAY, TODAY, None),

    ('M01-RGT-064', 'M01 - Roles & Responsibilities', 'Rights Inventory', 'All',
     'All user profiles must support four discrete object-level permissions: Read, Write, Edit, and Delete.',
     'The platform rights framework must implement four permission types on every controllable object and action — consistent with Salesforce object-level security model. When a profile is created or edited in the Admin Portal, each permission type is individually toggled on or off per functional area. Default state for all permissions is OFF (least privilege). Permissions must be enforced server-side, not only in the UI.',
     'Four permission types: Read (view data), Write (create new records/entries), Edit (modify existing records), Delete (remove records). Each is independently toggled per profile per object type. Combined permissions support all operational roles without requiring role duplication.',
     'A profile with Read-only access cannot create, edit, or delete records even if a UI element is accessible.',
     'Profiles created with no permissions explicitly enabled cannot access any platform data. Permission changes take effect on next login or session refresh.',
     'High', 'Active', 'M01', 'Platform Admin', 'Justin Woller — Jun 18 2026', TODAY, TODAY, None),

    ('M01-RGT-065', 'M01 - Roles & Responsibilities', 'Queue Rights', 'Provider Portal',
     'GCA and genetics-program roles must have access to a dedicated Genetics Queue showing pre- and post-test GC consults pending review, scheduling, and note submission.',
     'The Genetics Queue is a role-specific queue accessible only to GCA and GC roles. It surfaces: GC consults with pending note review; consults awaiting scheduling; pre-test consults pending physician approval; 28-day unreached patient items. Queue items are generated automatically by the platform based on consult status and elapsed time rules.',
     'Genetics Queue shows: consult ID, patient name, GC assigned, consult type (pre/post-test), status, days since last action. Items are sorted by urgency — ASAP consults first, then by age.',
     'GCA can action (schedule, submit note, log outreach) directly from the queue item without navigating to the full patient record.',
     'Genetics Queue is empty when no pending items exist. Queue auto-refreshes when a consult status changes.',
     'High', 'Active', 'M01', 'Care Team Ops', 'Care Team Workflow Overview + Jun 18 meeting', TODAY, TODAY, None),

    # ─────────────────────────────────────────────
    # M02 — Provider Portal
    # ─────────────────────────────────────────────

    ('M02-ZD-001', 'M02 - Provider Portal', 'Zendesk Integration', 'Provider Portal',
     'Patient chart must include a Zendesk tab in the right panel showing the active CS case for that patient.',
     'A Zendesk tab appears in the right panel of the patient chart alongside Documentation and Communication tabs. The tab displays the current Zendesk case context for that patient: case number, case type, case status (Open/Pending/Solved), last agent note, and assigned agent name. Only consult-related cases are displayed. Billing, demographics, and general CS tickets that are not tied to an active consult are not shown in the clinical chart.',
     'Zendesk tab shows: Case # (linked to Zendesk), Type (e.g., Consult Support), Status, Last Note (truncated, expandable), Assigned Agent. "Open in Zendesk" link navigates to the full ticket.',
     'If no active Zendesk case exists for the patient, the tab shows: "No active CS case for this patient."',
     'Zendesk tab does not display billing or demographic-only tickets. Tab content refreshes when the chart is opened.',
     'High', 'Active', 'M02', 'Care Team Ops', 'Justin Woller — Jun 18 2026', TODAY, TODAY, None),

    ('M02-CT-001', 'M02 - Provider Portal', 'Care Team Queue', 'Provider Portal',
     'Care Team queue must display client name on each consult row so agents know which client program the consult belongs to.',
     'Every consult row in the Care Team queue (PSR, PCC, Care Team Coordinator views) must show the client name associated with the care product. This ensures agents know which consults are available and relevant for that client program without consulting a separate reference tool. Available consult types for each client are driven by Admin Portal configuration.',
     'Client name displayed as a badge or column on each queue row. Color-coded per client for quick visual differentiation.',
     'Client name is required on all queue items. If client configuration is missing, the row shows "Unconfigured Client" and is flagged for admin review.',
     'Queue row without a client name displays a warning indicator. Agent cannot route or action an unconfigured-client consult.',
     'High', 'Active', 'M02', 'Care Team Ops', 'Jun 18 Care Team meeting — Beth Lewis request', TODAY, TODAY, None),

    ('M02-CT-002', 'M02 - Provider Portal', 'Care Team Queue', 'Provider Portal',
     'Critical lab alerts must be routed to the RN queue within the platform with a QA audit trail on resolution.',
     'Critical lab alerts (values meeting critical threshold criteria) are routed automatically to the RN queue as high-priority items. The RN reviews, takes action, and documents resolution within the platform. Admin and QA staff have a read-access view of all critical alert resolutions for quality review. Resolution notes, action taken, and timestamp are logged to the patient activity timeline.',
     'Critical alert queue item shows: patient name, alert type, lab value, threshold exceeded, time received. RN must log resolution action before item can be closed. QA view shows all resolved critical alerts with full audit trail.',
     'Critical alert not resolved within SLA threshold auto-escalates to supervisor queue.',
     'Attempting to close a critical alert without a resolution note returns a validation error. All critical alert events are immutable in the audit log.',
     'High', 'Active', 'M02', 'Clinical / Care Team', 'Jun 18 Care Team meeting — Stephanie Wiinamaki', TODAY, TODAY, None),

    ('M02-CT-003', 'M02 - Provider Portal', 'Modality Toggle', 'Provider Portal',
     'Provider chart must include a Video/Audio modality toggle allowing the provider to switch consult modality during an active session.',
     'A segmented pill toggle (Video / Audio) is displayed in the chart header bar during an active consult. Default state is Video when a video consult is active. Toggling to Audio switches the active modality indicator. The toggle does not control the actual call connection (that is handled by the telephony integration) but records the modality used in the session documentation.',
     'Toggle states: Video (purple active) / Audio (gray inactive). On toggle, modality selection is recorded to the consult record. Toggle is only visible during an active consult session.',
     'Toggling modality logs a modality-change event to the activity timeline with timestamp.',
     'Toggle is hidden when no active consult session is open.',
     'Medium', 'Active', 'M02', 'Engineering', 'Demo review Jun 17 2026', TODAY, TODAY, None),

    # ─────────────────────────────────────────────
    # M03 — Patient Portal
    # ─────────────────────────────────────────────

    ('M03-ACCT-001', 'M03 - Patient Portal', 'Account Model', 'Patient Portal',
     'Each patient must have a single persistent portal account that persists across care products, lab partners, and client programs.',
     'One-time scheduling links are eliminated. Every patient has a persistent authenticated account in the platform. Their account holds all consult history, lab results, and communication history regardless of which client program or lab partner originated the interaction. Patients use their account credentials to initiate telehealth consults — no separate link generation or disposable URL is required.',
     'Patient account persists indefinitely. Login credentials are email + password or SSO. All consults, results, and messages are accessible from one account view regardless of originating client.',
     'A patient who enrolled through a DXS/LabCorp program and later accesses Everlywell directly uses the same account.',
     'Disposable scheduling links are deprecated. Legacy link recipients are redirected to portal account creation or login.',
     'High', 'Active', 'M03', 'Engineering', 'Justin Woller — Jun 18 2026', TODAY, TODAY, None),

    ('M03-ACCT-002', 'M03 - Patient Portal', 'Account Model', 'Patient Portal',
     'Patient portal must support a no-branding isolated experience for client-specific programs (e.g., DXS/LabCorp) driven by subdomain routing.',
     'When a patient accesses the portal through a client-specific subdomain (e.g., quest.portal.everlywell.com), the platform loads the branded or no-branding experience configured for that client in the Admin Portal. For programs requiring client isolation (e.g., DXS): no Everlywell branding is shown, no other client products are visible or promoted, and the patient sees only care products associated with that client program. The patient account and health history still belong to the patient.',
     'Subdomain → branding config lookup happens at login. Isolated experience hides: Everlywell logo, cross-client product listings, competitor-adjacent navigation. Patient history is still accessible as it is the patient\'s own record.',
     'Patient accessing via neutral subdomain with no branding config sees the default Everlywell portal.',
     'Branding config is set in Admin Portal wizard Portal Branding step. Invalid subdomain redirects to default portal.',
     'High', 'Active', 'M03', 'Engineering', 'Justin Woller — Jun 18 2026', TODAY, TODAY, None),

    ('M03-ACCT-003', 'M03 - Patient Portal', 'Account Model', 'Patient Portal',
     'Patient portal must offer a direct-to-consumer cash-pay telehealth consult option when a patient\'s program does not include a covered consult.',
     'When a patient is enrolled in a care product where a telehealth consult is "not included" in their program, the platform must present a direct-to-consumer option: the patient can purchase a telehealth consult out-of-pocket. The consult is fulfilled by a provider who has access to the patient\'s full health history. This replaces the current workflow where patients can only be offered a non-prescriptive RN session.',
     'When consult is "not included": patient sees a "Get a Consult — Out of Pocket" option with price displayed. Patient completes payment and enters the scheduling flow. Provider assigned has read access to full patient history for that session.',
     'Cash-pay option is only shown when the care product config has consult set to "not included." If included, the standard covered consult flow is used.',
     'Cash-pay consult requires payment completion before scheduling slot is confirmed. Failed payment returns patient to the option screen.',
     'High', 'Active', 'M03', 'Product / Engineering', 'Jun 18 Care Team meeting', TODAY, TODAY, None),

    # ─────────────────────────────────────────────
    # M04 — Admin Portal
    # ─────────────────────────────────────────────

    ('M04-CPX-001', 'M04 - Admin Portal', 'Care Product Configuration', 'Admin Portal',
     'Each care product must be configurable with a consult availability flag: Included (covered) or Not Included (not covered / cash-pay only).',
     'In the Admin Portal care product setup wizard, the admin configures whether a telehealth consult is included in the patient\'s program or not. This flag drives the patient portal experience: Included = standard covered consult flow. Not Included = cash-pay direct-to-consumer option displayed. This replaces the current manual Retool lookup agents perform to check service availability per client.',
     'Consult availability options: Included, Not Included. Setting is per care product, not per client globally. Agent interface and patient portal both reference this flag to determine what is offered.',
     'Changing consult availability on an active care product takes effect for new enrollments only; existing active consults are not affected.',
     'Care product with no availability setting defaults to Not Included with an admin warning. Agents see the client name and consult availability status on each queue row.',
     'High', 'Active', 'M04', 'Admin / Product', 'Jun 18 Care Team meeting — Dana Garrett / Retool replacement', TODAY, TODAY, None),

    ('M04-CPX-002', 'M04 - Admin Portal', 'Care Product Configuration', 'Admin Portal',
     'Admin Portal must support configuration of treatment vs. non-treatment consult routing rules per care product and result type.',
     'For care products that involve lab result outreach, the Admin Portal must allow configuration of routing rules that determine consult type based on result status. Abnormal result = treatment consult workflow initiated. Normal result = no consult workflow initiated. Rules are configured per client program and per analyte/result type. These rules replace the current manual PSR judgment call on consult type determination.',
     'Rule configuration: result status (Abnormal / Normal / Critical) → consult type (Treatment / Non-Treatment / Educational / None). Rules are per care product. Admins can set client-specific overrides. Rules table is versioned and auditable.',
     'An abnormal result matching a configured rule auto-triggers the appropriate consult type in the workflow engine.',
     'Result with no matching rule defaults to no consult triggered and generates an admin alert for rule coverage gap.',
     'High', 'Active', 'M04', 'Admin / Clinical Ops', 'Justin Woller — Jun 18 2026', TODAY, TODAY, None),

    # ─────────────────────────────────────────────
    # M05 — Async Consultation
    # ─────────────────────────────────────────────

    ('M05-RES-001', 'M05 - Async Consultation', 'Result-Triggered Workflows', 'Provider Portal',
     'Abnormal lab result must automatically trigger a treatment consult workflow. Normal result must not trigger any consult workflow.',
     'When a lab result is received and parsed, the platform evaluates the result against the care product\'s routing rules. If any value is flagged as abnormal (out of reference range), the treatment consult workflow is initiated: a consult referral is created, the PSR queue is notified for outbound call, and a scheduling link (within the patient\'s persistent portal account) is prepared. If all values are normal, no consult workflow is triggered and the patient receives a standard result notification only.',
     'Abnormal result → create consult referral → notify PSR queue → prepare scheduling access within patient portal. Normal result → result notification only → no consult referral created.',
     'A result with mixed values (some normal, some abnormal) triggers the treatment workflow based on the abnormal flag only.',
     'Edge case: result received with no reference range data generates an admin alert and does not auto-trigger workflow until manually reviewed.',
     'High', 'Active', 'M05', 'Clinical / Engineering', 'Justin Woller — Jun 18 2026', TODAY, TODAY, None),

    # ─────────────────────────────────────────────
    # M08 — Notification Engine
    # ─────────────────────────────────────────────

    ('M08-CT-001', 'M08 - Notification Engine', 'Care Team Automation', 'Provider Portal',
     'All Care Team monitoring workflows currently performed via Slack channels must be replaced by automated queue events and notifications within the platform.',
     'The following Slack-based monitoring workflows are deprecated and replaced by platform automation: (1) #physician_issues → SLA Engine auto-triggers provider TAT alert and queue item at 2h and 4h marks. (2) #physician_monitoring → platform auto-detects consult status anomalies (stuck in scheduled, no report after 60 min) and surfaces queue items. (3) #new_referral_notes → provider note added event triggers Care Team notification and queue item. (4) #auth_monitoring → order pending alerts surfaced in admin queue automatically. (5) #gc_consult_monitoring → GC late-call and missing report alerts surface in Genetics Queue. Slack is not a platform integration and is not referenced in any workflow.',
     'Each deprecated Slack alert type maps 1:1 to a platform queue event type with: trigger condition, target role queue, SLA for response, escalation path if unresolved.',
     'Provider TAT miss at 4h auto-reassigns consult to available provider AND generates a PCC queue item confirming the reassignment occurred.',
     'If no provider is available for reassignment at 4h mark, a high-priority escalation item is created in the supervisor queue.',
     'High', 'Active', 'M08', 'Engineering', 'Justin Woller + Beth Lewis — Jun 18 2026', TODAY, TODAY, None),

    ('M08-CT-002', 'M08 - Notification Engine', 'Outreach Protocol Automation', 'Provider Portal',
     '28-day unreached patient protocol must be automated: a queue item surfaces automatically when no patient contact has been logged for 28 days.',
     'For any patient with an open consult or pending result outreach, the platform tracks days since last logged contact. When 28 days elapse with no contact event logged to the activity timeline, the platform automatically creates a queue item in the Care Team/GCA queue. The queue item shows: patient name, days since last contact, last contact attempt type, and a quick-action button to log a new outreach attempt.',
     'Queue item auto-created at day 28. Item includes: patient name, care product, days since contact, last attempt summary, action buttons (Log Call, Send Message, Cancel Outreach).',
     'If contact is logged before day 28, the auto-queue item is suppressed. Day count resets with each logged contact.',
     'Day 28 items not actioned within 48 hours auto-escalate to supervisor queue.',
     'High', 'Active', 'M08', 'Care Team Ops', 'Care Team Workflow Overview — Jun 2026', TODAY, TODAY, None),

    # ─────────────────────────────────────────────
    # M09 — Scheduling
    # ─────────────────────────────────────────────

    ('M09-RT-001', 'M09 - Scheduling', 'Real-Time Queue', 'Provider Portal',
     'Agents must be able to place a patient directly into the real-time queue for an immediate visit while on an active call with the patient.',
     'From within the patient record or the scheduling interface, an agent with scheduling rights can place a patient into the real-time on-demand queue during an active phone call. This action makes the patient immediately available for a provider to pick up without requiring the patient to navigate the scheduling flow independently. The agent selects the care product, confirms the patient is available, and clicks "Add to Real-Time Queue." The patient receives an immediate notification with instructions for the visit.',
     'Agent action: "Add to Real-Time Queue" button visible on patient record when agent is in an active call context. On click: patient enters real-time queue, provider queue is notified, patient receives SMS/email with visit link or portal access instructions.',
     'Patient added to real-time queue by agent is prioritized over self-scheduled real-time queue entries.',
     'Agent cannot add patient to real-time queue if no providers are currently available — system shows estimated wait time or offers scheduled alternative.',
     'High', 'Active', 'M09', 'Product / Engineering', 'Jun 18 Care Team meeting — Justin Woller', TODAY, TODAY, None),

    # ─────────────────────────────────────────────
    # M10 — Integrations
    # ─────────────────────────────────────────────

    ('M10-AWS-001', 'M10', 'AWS Connect Soft Phone', 'All',
     'AWS Connect must be integrated as the platform telephony layer for all Care Team inbound and outbound calling.',
     'AWS Connect is the soft phone solution for all PSR, PCC, and Care Team inbound/outbound calls. The integration must support: (1) click-to-dial from patient records in Project Phoenix; (2) auto-dial triggered by outbound alert call queue items; (3) call disposition written automatically to patient activity timeline on call end; (4) call recording stored in AWS per HIPAA retention requirements; (5) inbound call pop — when a call is received, the patient record auto-opens if the caller matches a known patient phone number; (6) agent status management (available, break, outbound, blended) synchronized with the platform queue.',
     'Click-to-dial: agent clicks phone number or "Call Patient" button in platform → AWS Connect initiates outbound call. On call end: disposition (answered/no-answer/voicemail), duration, and agent ID are written to activity timeline automatically.',
     'Click-to-dial is available from both Project Phoenix patient record and from Zendesk (bidirectional). Call log appears in both systems.',
     'If AWS Connect is unavailable, agent receives an error and can manually log a call attempt. Platform does not lose the call attempt record.',
     'High', 'Active', 'M10', 'Engineering / Integrations', 'Justin Woller — Jun 18 2026', TODAY, TODAY, None),

    ('M10-AWS-002', 'M10', 'AWS Connect Soft Phone', 'All',
     'Platform must support a vendor-agnostic translation/interpretation services launch button integrated into the call interface.',
     'A "Launch Translation" button is available in the active call interface for PSR and PCC roles. Clicking it initiates a three-way conference with the configured translation service provider (currently evaluating Eleven Labs). The button is vendor-agnostic — the translation service endpoint is configured in the Admin Portal and can be swapped without a code change. Use of translation services is logged to the activity timeline with language selected and duration.',
     'Launch Translation button visible in call interface when call is active. On click: connects translation service, logs event to activity timeline with timestamp and language.',
     'Translation service launch is optional on every call. If translation service is unavailable, agent receives an error and can manually note interpreter use.',
     'Translation service provider URL/config is set in Admin Portal Settings. Default label is "Launch Translation" regardless of vendor.',
     'Medium', 'Active', 'M10', 'Engineering / Integrations', 'Justin Woller — Jun 18 2026', TODAY, TODAY, None),

    ('M10-ZD-006', 'M10', 'Zendesk Integration', 'All',
     'Zendesk bidirectional integration must sync consult-related case activity between Zendesk and the Project Phoenix patient activity timeline in real time.',
     'Any Zendesk case event tied to an active patient consult must sync bidirectionally: (1) Agent creates or updates a case in Zendesk → event appears in patient activity timeline in Project Phoenix. (2) Provider or Care Team adds a note to a patient record in Project Phoenix → Zendesk case is updated and the assigned agent is notified. Billing questions, demographic updates, and general CS work that are not tied to an active consult are not synced to the clinical chart. The sync key is a unique patient/consult ID shared between both systems. Full integration design is a separate workstream — bidirectional sync is the architectural requirement.',
     'Sync filter: only consult-related Zendesk case types sync to the clinical chart. Non-consult case types (Billing, Demographics, General Inquiry) stay in Zendesk only. Sync is real-time or near-real-time (<30 seconds).',
     'If a Zendesk case type is miscategorized, the sync filter may incorrectly include or exclude it — case type taxonomy must be agreed between Care Team Ops and Engineering.',
     'Sync failures are logged and retried. A sync failure indicator appears on the Zendesk tab in the patient chart if data is stale.',
     'High', 'Active', 'M10', 'Engineering / Integrations', 'Justin Woller — Jun 18 2026', TODAY, TODAY, None),

    ('M10-LAB-002', 'M10', 'Lab Result Integration', 'All',
     'All incoming lab results must be parsed and stored as structured discrete data in the database — not stored only as PDF attachments.',
     'When a lab result is received through the lab partner integration, every discrete value must be extracted and written to the database: analyte name, result value, unit of measure, reference range (low/high), in-range/out-of-range flag, critical flag, specimen collection date, lab partner ID, and ordering provider. The PDF is also stored as an attachment for reference and regulatory requirements, but the PDF alone is insufficient. Structured data enables: abnormal/normal routing logic, HEDIS gap detection, historical trending, statistical analysis, and future AI-based rules.',
     'Lab result record in DB contains: all discrete values as structured fields, reference ranges, abnormal flags, critical flags, metadata. PDF stored separately as supplemental attachment. Both must be present for result to be considered complete.',
     'A result received with a PDF but no parseable discrete values is flagged as "Parsing Failed" and routed to a manual review queue before any automated workflow is triggered.',
     'Lab partners who deliver only PDF (no HL7/FHIR structured data) require a parsing middleware layer. This is an integration design requirement for each lab partner onboarding.',
     'High', 'Active', 'M10', 'Engineering / Data', 'Justin Woller — Jun 18 2026', TODAY, TODAY, None),

]

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

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
conn.close()

print(f'\nDone. Inserted: {inserted} | Skipped: {skipped} | Total attempted: {len(requirements)}')
