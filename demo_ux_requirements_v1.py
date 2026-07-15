#!/usr/bin/env python3
"""
Demo UX Requirements — DB Commit Script v1
June 18, 2026
Covers: demo changes not yet backed by DB requirements
- Chart Preview modal (M02)
- Sign & Close Chart attestation workflow (M02)
- Video/Audio modality toggle (M02)
- Route-to team member picker (M02)
- Patient Care Journey tracker (M03)
- Portal Branding wizard step (M04)
- State licensure matrix (M04)
- Configurable named workflow stages (M04)
"""

import sqlite3
from datetime import date

DB_PATH = '/Users/justin.woller/Documents/project-phoenix-demo/project_phoenix.db'
TODAY = str(date.today())

requirements = [

    # ─────────────────────────────────────────────
    # M02 — Provider Portal
    # ─────────────────────────────────────────────

    ('M02-PREV-001', 'M02 - Provider Portal', 'Chart Signing Workflow', 'Provider Portal',
     'Provider must be able to preview a read-only summary of all chart sections before signing and closing the chart.',
     'A "Preview" button in the chart action bar opens a full-screen read-only modal showing a clean print-style summary of all completed chart sections: Chief Complaint, HPI, Review of Systems, Physical Exam, Assessment & Plan, and MDM/Billing. The preview is read-only — no fields are editable inside the modal. The provider can close the preview or proceed directly to "Sign & Close Chart" from within the preview modal. This replaces the previous "Review & Sign" button which created confusion about the signing workflow.',
     'Preview modal is read-only. All populated chart sections are shown. Empty sections display a placeholder. Provider can click "Sign & Close Chart" directly from the preview modal.',
     'Chart with no completed sections shows preview with all sections labeled "Not yet completed."',
     'Provider cannot edit content inside the preview modal. Any click on a content field in preview mode does nothing.',
     'High', 'Active', 'M02', 'Engineering / UX', 'Demo review Jun 17 2026 — Justin Woller', TODAY, TODAY, None),

    ('M02-SGN-001', 'M02 - Provider Portal', 'Chart Signing Workflow', 'Provider Portal',
     'Provider must complete an attestation and confirm their name before a chart can be signed and closed.',
     'Clicking "Sign & Close Chart" opens a signing confirmation modal. The modal contains: (1) an attestation statement that the provider has reviewed the chart and the documentation is accurate; (2) a provider name field pre-filled with the logged-in provider\'s name, editable; (3) a checkbox the provider must check to confirm the attestation; (4) a summary of the MDM complexity level and billing codes. The "Sign & Close" confirm button remains disabled until the checkbox is checked. On confirm, the chart is locked, a signed event is written to the activity timeline, and billing submission is triggered.',
     'Checkbox must be checked before "Sign & Close" activates. Provider name field is required. On signature: chart status changes to Closed, signed event logged to activity timeline, billing codes submitted.',
     'Provider can edit the pre-filled name (e.g., if signing on behalf of a different provider in a supervised care model).',
     'Attempting to submit the signing form without checking the checkbox returns a validation error. Signed charts are immutable — no edits permitted after chart closure.',
     'High', 'Active', 'M02', 'Engineering / Clinical Compliance', 'Demo review Jun 17 2026 — Justin Woller', TODAY, TODAY, None),

    ('M02-MOD-001', 'M02 - Provider Portal', 'Consult Modality', 'Provider Portal',
     'The provider chart must display a Video/Audio modality toggle that records the modality used during an active consult session.',
     'A segmented pill toggle (Video / Audio) is displayed in the chart action bar when a consult is in an active session state. The toggle records the modality for clinical documentation purposes — it does not control the actual call connection. Default is Video for video consults and Audio for phone consults based on the consult type. Toggling writes a modality-change event to the activity timeline. The toggle is hidden when no active consult session is open.',
     'Toggle states: Video / Audio. Selecting a modality writes a clinical documentation event. Toggle is only shown during active consult session. Modality is reflected in the consult record and billing documentation.',
     'Provider can toggle modality mid-session to reflect a switch (e.g., video dropped to audio-only).',
     'Toggle hidden when chart is open in review mode (no active session). Modality change events are immutable in the audit log.',
     'Medium', 'Active', 'M02', 'Engineering', 'Demo build — Jun 2026', TODAY, TODAY, None),

    ('M02-RT-001', 'M02 - Provider Portal', 'Routing & Communication', 'Provider Portal',
     'When routing a message to an individual team member, the provider must be able to select the specific recipient from a team member list.',
     'In the routing modal, when the provider selects "Message Individual" as the routing type, a second field "Route To" appears with a dropdown list of available team members. The provider selects the specific recipient. The "Route" confirm button remains disabled until both the message type and recipient are selected. The confirmation displays the selected recipient\'s name. The message notification and activity log entry include the recipient\'s name so there is a clear audit trail of who the message was directed to.',
     'Route To field is required when Message Individual is selected. Recipient list includes all active team members in the practice. Routing confirmation shows recipient name. Activity timeline entry includes sender, recipient, and message category.',
     'If Message Individual is selected with no recipient, the Route button remains disabled with a tooltip: "Select a team member to route to."',
     'Route To field is hidden for all routing types other than Message Individual. Recipient list is dynamically populated based on active users in the practice.',
     'Medium', 'Active', 'M02', 'Engineering / UX', 'Demo review Jun 17 2026 — Justin Woller', TODAY, TODAY, None),

    # ─────────────────────────────────────────────
    # M03 — Patient Portal
    # ─────────────────────────────────────────────

    ('M03-JRN-001', 'M03 - Patient Portal', 'Care Journey Tracker', 'Patient Portal',
     'The patient portal must display a Care Journey tracker showing the patient\'s real-time progress through their active telehealth consult workflow.',
     'A Care Journey tracker is displayed prominently on the patient\'s home dashboard and consult detail page. It shows a horizontal stage-by-stage progress tracker matching the workflow configured for their care product. Completed stages show a checkmark. The current active stage is highlighted with a progress indicator. Upcoming stages are shown in gray. Stage names are plain-language patient-friendly descriptions (e.g., "Your Request Received," "Provider Review," "Consult Scheduled"). An SLA progress bar beneath the active stage shows remaining time as an amber bar when within 25% of the SLA window. The tracker updates automatically when consult status changes.',
     'Care Journey tracker shows: completed stages (✓), active stage (highlighted, with SLA bar), upcoming stages (gray). Refreshes automatically on status change. SLA bar is amber when within 25% remaining.',
     'A consult with no stages configured shows a simplified 3-step tracker: Request Received → Provider Review → Complete.',
     'Care Journey tracker is read-only for patients. Patients cannot interact with stage items. SLA bar is hidden when no SLA threshold has been triggered.',
     'High', 'Active', 'M03', 'Engineering / UX', 'Demo build — Jun 2026', TODAY, TODAY, None),

    # ─────────────────────────────────────────────
    # M04 — Admin Portal
    # ─────────────────────────────────────────────

    ('M04-BRD-001', 'M04 - Admin Portal', 'Portal Branding', 'Admin Portal',
     'The Admin Portal care product wizard must include a Portal Branding step where admins configure the patient-facing portal experience for each client program.',
     'A Portal Branding step in the care product wizard allows admins to configure: (1) Branding type — Client Branded (show client logo, colors) or No Branding (generic, no Everlywell or client marks); (2) Subdomain — the URL subdomain patients use to access this client\'s portal experience (e.g., "quest" for quest.portal.domain.com); (3) Logo upload for Client Branded experiences; (4) Primary color for Client Branded experiences. The subdomain configuration drives which branding experience loads at patient login. This supports white-label and no-branding requirements for partners like DXS and LabCorp.',
     'Branding type: Client Branded or No Branding. Subdomain: alphanumeric, unique per client, validated on save. Logo: required for Client Branded, hidden for No Branding. Primary color: required for Client Branded, hidden for No Branding.',
     'Subdomain "everlywell" is reserved and cannot be used by partner configurations.',
     'Duplicate subdomain returns a validation error: "This subdomain is already in use." Logo files must be PNG or SVG under 2MB.',
     'High', 'Active', 'M04', 'Engineering / Partnerships', 'Justin Woller — Jun 18 2026', TODAY, TODAY, None),

    ('M04-SLM-001', 'M04 - Admin Portal', 'Provider Configuration', 'Admin Portal',
     'The Admin Portal must include a state licensure matrix configuration where admins define which providers are licensed to practice in which states per care product.',
     'The state licensure matrix is configured per care product in the Admin Portal. For each care product, admins can map: which states are serviced, which providers hold active licenses in each state. The matrix is used by the scheduling and provider assignment engine to match patients to licensed providers. Only providers with an active license in the patient\'s state of residence are eligible for assignment on that consult. License status and expiration dates are configurable per provider per state.',
     'Matrix rows: states. Matrix columns: active providers. Cell value: Licensed / Not Licensed / Expired. Provider assignment engine filters to Licensed providers only for a given patient state.',
     'Adding a new state to the matrix triggers a notification to all providers without a license for that state, prompting license submission.',
     'An expired license automatically removes that provider from the eligible pool for that state without requiring manual admin intervention. Admin is notified of any upcoming license expirations (30-day warning).',
     'High', 'Active', 'M04', 'Engineering / Compliance', 'Demo build — Jun 2026', TODAY, TODAY, None),

    ('M04-WFB-001', 'M04 - Admin Portal', 'Workflow Configuration', 'Admin Portal',
     'Admins must be able to define named workflow stages that form the telehealth consult pipeline for each care product.',
     'The Workflow Configuration step in the Admin Portal care product wizard allows admins to build a custom pipeline from a library of available stages. Available stages include: Patient Intake, Identity Verification, Insurance Verification, MA Review, Provider Assignment, Async Review, Consult (Phone/Video), Lab Order, Lab Review, Prescription/Rx, Referral, Follow-up Consult, Care Coordination Review, Patient Education, Provider Documentation, and Chart Closure. For each stage added, the admin configures: SLA hours allowed, Required or Optional designation. The configured pipeline defines the Care Journey tracker stages shown to patients and the workflow simulation used in training. Stages can be reordered via drag-and-drop. Pre-built templates (Standard Phone/Video, Async Only, Hybrid, Chronic Care Management) are available as starting points.',
     'Stage library contains all available stage types. Admin selects and orders stages for their care product. Each stage requires: name (from library), SLA hours, Required/Optional. Summary bar shows total stages, estimated total SLA, and roles involved. On save, the pipeline is applied to all new consults for that care product.',
     'Required stages cannot be removed from an active care product without admin confirmation that existing open consults will not be affected.',
     'An empty workflow (no stages) cannot be saved — at minimum one Required stage is needed. SLA value of 0 is not valid and returns a validation error.',
     'High', 'Active', 'M04', 'Engineering / Product', 'Demo review Jun 17 2026 — wizard Step 11', TODAY, TODAY, None),

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
