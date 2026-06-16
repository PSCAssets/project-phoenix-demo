# Run this as a standalone Python script at:
# ~/Documents/project-phoenix-demo/write_pending_requirements.py

import sqlite3
from datetime import date

DB_PATH = '/Users/justin.woller/Documents/project-phoenix-demo/project_phoenix.db'
TODAY = str(date.today())

requirements = [
    # ── M02 Provider Portal ──────────────────────────────────────────────────
    ('M02-UX-001', 'M02 - Provider Portal', 'UX / SLA Display', 'Provider',
     'As a provider, I need SLA urgency communicated visually so I can triage at a glance without reading status text.',
     'SLA status must be displayed as an icon indicator only — triangle with exclamation mark (⚠). No text status labels on the indicator.',
     'Yellow (#F59E0B) when approaching threshold; Red (#DC2626) when exceeded/overdue; Green dot when on track. Tooltip on hover shows full detail.',
     'Icon renders correctly in dashboard, queue, chart, and oversight. Tooltip displays SLA time remaining or overdue duration.',
     'Screen reader must announce icon meaning. Color-blind mode requires shape distinction beyond color alone.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M02-UX-002', 'M02 - Provider Portal', 'UX / Queue Filters', 'Provider',
     'As a provider, I need one-click filter buttons to immediately isolate overdue, urgent, or unassigned patients in the queue.',
     'Status summary pills at the top of the queue (overdue count, urgent count, unassigned count) must function as one-click active filter toggles.',
     'Clicking a pill filters the list to show only matching rows. Clicking again deactivates. AND logic with existing dropdown filters. Active state: solid filled background. Replaces the red dismissible SLA breach banner.',
     'Clicking overdue pill shows only overdue rows. Combining pills with dropdowns narrows results correctly. Deactivating restores full list.',
     'If zero items match after filtering, show empty state message. Pills must update counts dynamically.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M02-UX-003', 'M02 - Provider Portal', 'UX / Queue', 'Provider',
     'As a clinical supervisor, I need the master queue to show only actionable patients by default so staff are not distracted by active consults.',
     'Master queue must hide In Progress rows by default. Default view shows: Assigned, Pending, Waiting, Unassigned only.',
     'A Show In Progress toggle (off by default) allows RN/CT/MA to reveal in-progress rows. Toggle state does not persist across sessions.',
     'On load, no In Progress rows appear. Toggling Show In Progress reveals them. Toggling off hides them again.',
     'If all patients are In Progress, queue shows empty state with toggle prompt.',
     'Medium', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M02-SET-001', 'M02 - Provider Portal', 'Settings / Profile', 'Provider',
     'As a provider, I need a settings page that manages my profile, licenses, communication preferences, and account security.',
     'Provider Settings must include: communication preferences, license summary (read-only from Verifiable), contact info (read-only from Verifiable), change password, signature upload/draw, out-of-office/coverage assignment, default patient panel view, notification quiet hours, two-factor authentication toggle, session timeout preference.',
     'License data sourced from Verifiable — read-only in this system. Contact info grayed out with source attribution. Licenses expiring within 90 days show amber warning.',
     'All fields save correctly. License table shows correct expiration warnings. Signature upload stores and renders on chart sign-off.',
     'If Verifiable sync is unavailable, show last-synced data with staleness warning.',
     'Medium', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M02-LIC-001', 'M02 - Provider Portal', 'UX / License Alert', 'Provider',
     'As a provider, I need to see license expiry warnings in context of my dashboard, not as a disruptive full-page banner.',
     'License expiry alerts must appear inline under the provider name in the dashboard sub-header. Not as a full-width sticky banner above the nav.',
     'Alert displays as compact amber text directly below the provider role/title line. Applies to all provider role dashboards.',
     'Alert appears correctly positioned on MD, NP, RN, MA, GC, and CT dashboards. Dismissed behavior TBD.',
     'If multiple licenses are expiring, show the most urgent one with a count indicator.',
     'Medium', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M02-INTAKE-001', 'M02 - Provider Portal', 'New Patient / Intake', 'Provider',
     'As a provider or care team member, I need two distinct patient entry paths depending on whether the patient is new to the platform or already has an account.',
     'New Patient entry point must offer two paths: (1) Existing Patient — New Consult: demographics pre-filled, flow is Care Product > Intake Q&A > Request Consult; (2) New Patient Registration: full flow including Contact & Insurance, Billing, Health Profile, Care Product, Intake Q&A, Request Consult.',
     'Path selection presented before Step 1. Existing Patient path skips billing/insurance. New Patient Registration path mirrors the patient-side online signup. New Patient Registration primarily initiated by MA/CT/Scheduler.',
     'Correct step count shown for each path. Existing patient demographics pre-populate. New patient registration captures all required fields.',
     'If patient is found in system during New Patient Registration, warn that patient already exists and offer to switch to Existing Patient path.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M02-INTAKE-002', 'M02 - Provider Portal', 'New Patient / Intake', 'Provider',
     'As a scheduler or provider, I need to select the consult type when initiating a patient request.',
     'Consult type selector must offer exactly three options: Phone, Video, Async.',
     'Phone and Video are schedulable. Async is queue-driven — selecting Async on the Request Consult step replaces the scheduling calendar with Send Intake Questionnaire action.',
     'All three options selectable. Async selection correctly suppresses calendar and shows questionnaire send action.',
     'Default selection may vary by care product configuration.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M02-INTAKE-003', 'M02 - Provider Portal', 'New Patient / Intake', 'Provider',
     'As a scheduler, I need to choose between scheduling an appointment or adding a patient to the real-time queue without unnecessary options.',
     'Request Consult step presents two side-by-side options: Schedule Appointment and Real-Time Queue. Schedule Appointment expands inline date/time picker. Real-Time Queue is a single action button. No Standard/Urgent priority selector — priority determined by SLA engine.',
     'If Async consult type selected, Schedule Appointment is replaced by Send Intake Questionnaire. Real-Time Queue is hidden for Async.',
     'Scheduled path captures date, time, and provider. Real-Time path immediately places patient in queue. Async path sends questionnaire.',
     'If no provider is available for selected date, show next available date suggestion.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    # ── M03 Patient Portal ───────────────────────────────────────────────────
    ('M03-MSG-001', 'M03 - Patient Portal', 'Messaging', 'Patient',
     'As a patient, I need to know whether my message is going to my care team about my treatment or to general support for billing and account issues.',
     'Patient-facing messages must be separated into two categories: (1) Care Messages — consultation-related communications from care team tied to active consult; (2) Support — general inquiries for billing, subscription, technical issues, questions about other care products.',
     'Two clearly labeled and separated tabs or sections. Care Messages tied to the specific care product context. Support routes to the support team.',
     'Care Messages display only care-product-related threads. Support tab routes to support queue. Labels make purpose unambiguous.',
     'If patient only has one care product, Care Messages tab still appears. Unread counts shown per tab.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M03-UX-001', 'M03 - Patient Portal', 'Care Product Cards', 'Patient',
     'As a patient, I need to always see what type of consultation is coming up next for each of my care products.',
     'Each care product card on the patient dashboard must always display the current upcoming consult type (Phone / Video / Async). Consult type reflects the current phase of the care product.',
     'Consult type updates dynamically as the phase progresses — e.g., Video for initial consult, Async for follow-up. Must be visible without expanding the card.',
     'Card shows correct consult type for each phase. Updating phase changes displayed type. Async consults show correctly distinct from scheduled types.',
     'If no upcoming consult is scheduled, card shows Next Step rather than consult type.',
     'Medium', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M03-PROF-001', 'M03 - Patient Portal', 'Health Profile', 'Patient',
     'As a patient, I need my health profile to capture all clinically relevant information so my provider has full context before a consultation.',
     'Health Profile must include: Demographics (DOB, Sex, Height, Weight, BMI calculated), Medical History (conditions, past surgeries, hospitalizations), Current Medications (name, dose, frequency, prescriber), Allergies (drug, food, environmental), Family History (Diabetes, Heart Disease, Cancer, Hypertension), Social History (smoking, alcohol, exercise), Vitals History (BP, HR, Temp last recorded), Preferred Pharmacy, Emergency Contact.',
     'All sections must be present. BMI calculated from height/weight. Sections collapsible for usability. Data flows into provider chart view.',
     'All fields save and render correctly. BMI calculates on weight/height entry. Emergency contact required before first consult.',
     'Partial profile allowed but flagged. Provider sees profile completeness indicator on chart.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    # ── M04 Admin Portal ─────────────────────────────────────────────────────
    ('M04-ARCH-001', 'M04 - Admin Portal', 'Architecture', 'Admin',
     'As a platform administrator, I need a system administration interface that manages configuration, not operations.',
     'Admin portal must follow a system administration format (not operational screens). Must NOT include MA Queue, Patients list, or provider operational dashboard. Required modules: Care Products, User Management, Provider Credentialing, Integration Health, SLA Configuration, Notification Templates, Audit Log, Reports.',
     'Each admin module is a distinct section. User Management supports invite, role assignment, deactivate/reactivate. Integration Health shows live status of all connected systems with last sync timestamp. SLA Configuration editable per care product.',
     'All 8 admin modules accessible and functional. User invite flow works. Integration status displays correctly.',
     'Admin access requires elevated role. All admin actions logged to Audit Log.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    # ── M09 Scheduling ───────────────────────────────────────────────────────
    ('M09-SCHED-001', 'M09 - Scheduling', 'Schedule Display', 'Provider',
     'As a provider, I need my schedule to reflect only time-blocked appointments so async work does not create false time conflicts.',
     'Async consults must NOT appear on the provider schedule calendar. Schedule shows only: Video Consult, Phone Consult, A1C Treat Consult, Annual Visit, Telehealth Consult, Follow-up.',
     'Async work is queue-driven and does not occupy scheduled time slots. If a provider is viewing their schedule and has active async consults, those do not appear as calendar blocks.',
     'No async entries appear on calendar. All other consult types appear correctly. Async work visible in queue only.',
     'Provider with 100% async caseload sees an empty calendar with only availability blocks.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M09-SCHED-002', 'M09 - Scheduling', 'Scheduler Dashboard', 'Provider',
     'As a scheduling coordinator, I need a simple landing screen that gives me immediate access to the three things I do most.',
     'Scheduler dashboard must present three primary actions: Search Patient (to find and schedule for an existing patient), New Patient (to register and schedule a new patient), Open Scheduler (to enter the full scheduling tool).',
     'Landing screen is simple — three prominent action buttons, minimal other content. Each button navigates to the correct workflow.',
     'All three buttons navigate correctly. Search Patient opens patient search. New Patient opens registration flow. Open Scheduler opens scheduling tool.',
     'If scheduler has pending reschedule requests, show a count badge on the dashboard.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M09-SCHED-003', 'M09 - Scheduling', 'Path A - Patient First', 'Provider',
     'As a scheduler, I need to start from a patient and find the right provider for them based on their state and care product.',
     'Path A: Search/select patient → identify care product (select if multiple) → system filters providers by patient state and care product → view provider availability → select consult type (Phone/Video) → book slot.',
     'Provider filter must apply both state licensing AND care product simultaneously. Only providers licensed in the patient state for the selected care product appear.',
     'Provider list correctly filters. Selecting a provider shows their available slots. Booking confirms appointment.',
     'If no licensed providers are available for that state/care product, show clear message with suggested alternatives.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M09-SCHED-004', 'M09 - Scheduling', 'Path B - Provider First', 'Provider',
     'As a scheduler, I need to start from a known provider and find a patient to schedule with them.',
     'Path B: Search/select provider → search/select patient → view provider schedule → select available slot → select consult type (Phone/Video) → book.',
     'Provider search available from scheduler landing. Patient search follows provider selection. Provider schedule displays with available slots highlighted.',
     'Provider schedule loads correctly. Patient can be assigned to an available slot. Booking creates confirmed appointment.',
     'Warn if selected patient is not in a state where the provider is licensed. Do not block booking but require acknowledgment.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M09-SCHED-005', 'M09 - Scheduling', 'Path C - Date First', 'Provider',
     'As a scheduler, I need to find all open slots on a specific date for a patient who has already told me their preferred day.',
     'Path C: Select date → select patient → select care product → select consult type → system shows all open slots on that date filtered by patient state + care product + consult type, grouped by provider.',
     'Results show only providers licensed in patient state for the care product with open slots on the selected date. Grouped by provider with time slots listed.',
     'Results display correctly filtered. Selecting a slot from any provider completes the booking.',
     'If no slots exist on selected date matching all criteria, show next available date across matching providers.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M09-SCHED-006', 'M09 - Scheduling', 'Provider Search Filters', 'Provider',
     'As a scheduler, I need the provider search to always enforce state licensing and care product eligibility to prevent improper bookings.',
     'Provider search and display in the scheduling tool must always filter by: patient state (provider must be licensed), care product (provider must be configured for it), date (provider must have availability), consult type (Phone/Video — Async excluded from scheduling).',
     'All four filters applied simultaneously. System must not surface providers who fail any filter criterion. Filter parameters visible to scheduler during search.',
     'Provider not licensed in patient state does not appear. Provider not configured for care product does not appear. Provider with no availability on date does not appear.',
     'Edge case: provider licensed in state but not yet configured for care product — excluded from results with admin notification.',
     'Critical', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M09-SCHED-007', 'M09 - Scheduling', 'Availability Management', 'Provider',
     'As a scheduler, I need to be able to add or modify provider availability blocks when coordinating with providers directly.',
     'Both the provider (in their Schedule screen) and the scheduler (in the scheduling tool) can add and modify availability blocks. Scheduler changes are attributed to the scheduler in the audit trail.',
     'Availability blocks added by scheduler appear immediately on the provider schedule. Changes are logged with scheduler identity. Provider can see and override scheduler-added blocks.',
     'Scheduler can add available and unavailable blocks for any provider. Provider sees the change in their schedule. Audit log records who made the change.',
     'If scheduler and provider make conflicting changes simultaneously, last-write wins with conflict notification.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M09-SCHED-008', 'M09 - Scheduling', 'Consult Type at Booking', 'Provider',
     'As a scheduler, I need to specify whether an appointment is a phone or video consultation at the time of booking.',
     'Scheduler selects consult type (Phone or Video) during the booking flow. Async is not available as a scheduled consult type. Selection recorded on the appointment and visible to both provider and patient.',
     'Consult type selection required before booking can be confirmed. Async option not presented in scheduling context.',
     'Phone and Video selectable. Async not present. Selected type appears on confirmation and calendar block.',
     'Care product default consult type may pre-select an option but scheduler can override.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M09-SCHED-009', 'M09 - Scheduling', 'Post-Booking Confirmation', 'Provider',
     'As a patient, I need to receive a confirmation after my appointment is scheduled.',
     'After any booking (via scheduler, MA, CT, or provider), the system must automatically send a confirmation to the patient via their preferred notification channel (email, SMS, or both) per their notification settings.',
     'Confirmation always fires — it is not optional. Message content includes: provider name, care product, consult type, date, time (in patient local time), and instructions for the consult type.',
     'Confirmation sent after successful booking. Content accurate. Patient receives via their configured channel.',
     'If patient has no notification method on file, flag for scheduler to confirm manually.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M09-SCHED-010', 'M09 - Scheduling', 'Cancellation', 'Provider',
     'As a scheduler, I need to cancel an appointment with a single action.',
     'Cancellation is a direct action — no rescheduling workflow is triggered automatically. Scheduler selects appointment and cancels. System records cancellation reason (dropdown) and timestamp.',
     'Cancellation removes the appointment from the schedule and the patient confirmation. Slot is returned to available. Patient notification of cancellation fires per notification settings.',
     'Appointment removed from all views. Slot reopens. Patient notified.',
     'If cancellation is within a defined window before appointment (e.g., less than 2 hours), system warns but allows.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M09-SCHED-011', 'M09 - Scheduling', 'Rescheduling', 'Provider',
     'As a scheduler, I need two ways to reschedule a patient — from their appointment on the calendar or by searching for them directly.',
     'Rescheduling has two entry points: (1) Click patient appointment on schedule → Reschedule option appears; (2) Search patient → find their appointment → Reschedule. Rescheduling opens the full scheduling flow pre-filled with patient and care product.',
     'Original appointment is cancelled and new appointment created. Patient receives cancellation notice and new confirmation. Old slot returns to available.',
     'Both entry points lead to same reschedule flow. New appointment created correctly. Patient notified of both cancellation and new booking.',
     'If patient reschedules more than N times (configurable), flag for care team review.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M09-SCHED-012', 'M09 - Scheduling', 'MA/CT Scheduling Access', 'Provider',
     'As a medical assistant or care team member, I need the same scheduling capability as a dedicated scheduler so I can book appointments during patient intake.',
     'MA and CT roles have full scheduling access equivalent to the Scheduler role: all three paths (patient-first, provider-first, date-first), full system-wide provider visibility, ability to add availability blocks.',
     'Same provider search filters apply: state licensing, care product, consult type. MA/CT see all providers in the system.',
     'MA/CT can complete a full booking using any of the three paths. Provider search returns correct results.',
     'MA/CT scheduling actions attributed to their identity in the audit log.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('M09-SCHED-013', 'M09 - Scheduling', 'Multi-Entity Access Control', 'Provider',
     'As a platform operator, I need scheduling access scoped correctly for internal staff vs external client schedulers.',
     'Internal users (Everlywell staff schedulers, MA, CT) can book patients across all legal entities — no entity restriction. External users (client-tied schedulers) can only see and schedule patients and providers within their assigned client entity.',
     'Entity assignment configured at the user level in Admin portal. External scheduler login automatically scopes all search results to their entity. Internal scheduler sees full system.',
     'External scheduler search returns only their entity patients and providers. Internal scheduler search returns all. Entity scope cannot be bypassed by external users.',
     'If an external scheduler attempts to access a patient outside their entity via direct URL, access is denied with appropriate error.',
     'Critical', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    # ── M14 Provider Oversight ───────────────────────────────────────────────
    ('M14-LAB-001', 'M14 - Provider Oversight & Authorization', 'Lab Order Authorization', 'Provider',
     'As a supervising physician, I need to authorize multiple lab orders at once when the queue is large.',
     'Lab Order Authorization screen must support bulk actions: checkbox on each row, Select All checkbox in header, Authorize Selected (N) button disabled when nothing selected, confirmation dialog before bulk execution.',
     'On confirm: all selected rows removed from queue, success banner shown with count. Rejected orders must still be handled individually.',
     'Select All checks all rows. Count updates in button label. Confirmation shows correct count. Authorized orders disappear from queue.',
     'If one order in a bulk batch fails authorization (e.g., missing data), process the rest and surface the failed one with error detail.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    # ── Cross-Module Role Behavior ───────────────────────────────────────────
    ('ROLE-001', 'M02 - Provider Portal', 'Role Configuration', 'Provider',
     'As a platform operator, I need NP and MD dashboards to be identical so that role differences are enforced by configuration, not by UI.',
     'The NP dashboard must be structurally and functionally identical to the MD dashboard. All widgets, columns, and actions are the same.',
     'Scope-of-practice differences enforced via Admin portal role configuration — not via dashboard UI differentiation. Any future role restriction applied in Admin propagates automatically.',
     'NP sees same layout, same widgets, same action buttons as MD. Admin role config can restrict specific actions without changing dashboard structure.',
     'If Admin restricts an NP action, the button grays out or hides — it does not restructure the dashboard.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('ROLE-002', 'M02 - Provider Portal', 'Role Configuration', 'Provider',
     'As a clinical operations manager, I need RN, MA, and CT staff to have a unified view of their patients and messages without navigating between a separate dashboard and queue.',
     'For RN, MA, and CT: My Dashboard and Queue merged into one unified screen. Top: stat cards. Middle: assigned patient activity (queue-style table with category badges, urgency, contextual actions). Bottom: internal messages directed to them. Master Queue accessible via dedicated nav button.',
     'Messages nav button routes to general internal staff communications only — not patient messages. Master Queue tab shows all patient activity system-wide.',
     'Unified screen loads correctly for each role. Patient table shows only assigned patients. Internal messages show only messages directed to that user. Master Queue nav works.',
     'If user has no assigned patients, patient table shows empty state with prompt to view Master Queue.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),

    ('ROLE-003', 'M02 - Provider Portal', 'Role Configuration', 'Provider',
     'As a genetic counselor, I need my queue and dashboard filtered to genetics patients only so I am not distracted by general telehealth cases.',
     'The GC role must have all queue, dashboard, and patient views filtered to genetics-related care products only (BRCA Counseling, Hereditary Cancer, Carrier Screening, Pharmacogenomics, and any future genetics-tagged care products).',
     'Filter applies to: My Queue, Master Queue My Queue tab, Active Consults widget, SLA Alerts, Pending Patient Response. GC does not see Testosterone, Weight Management, Skincare, ED, or other non-genetics care products.',
     'GC login shows only genetics consults in all views. Master Queue My Queue tab filtered. Non-genetics consults not accessible.',
     'Care products must be tagged as genetics in Admin portal configuration. Tag drives GC filter logic.',
     'High', 'Defined', None, 'Justin Woller', 'Demo Review Jun 2026', TODAY, TODAY, None),
]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

inserted = 0
skipped = 0
for req in requirements:
    try:
        cursor.execute('''
            INSERT INTO requirements
            (req_id, module_id, section, portal, user_story, requirement, rule,
             acceptance, edge_cases, priority, status, jira_epic, owner, source,
             date_added, last_updated, exported_version)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', req)
        inserted += 1
    except sqlite3.IntegrityError:
        skipped += 1
        print(f'SKIP (already exists): {req[0]}')

conn.commit()
conn.close()
print(f'\nDone. Inserted: {inserted}, Skipped: {skipped}')
