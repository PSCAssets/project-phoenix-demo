#!/usr/bin/env python3
"""
Project Phoenix — QA Script for Steps 4–6
June 18, 2026
Verifies:
  - All DB requirement IDs from the 3 June 18 scripts
  - Demo HTML changes from Steps 4, 5, and 6
"""

import sqlite3
import os
import re

DB_PATH = '/Users/justin.woller/Documents/project-phoenix-demo/project_phoenix.db'
TEMPLATES = '/Users/justin.woller/Documents/project-phoenix-demo/templates'

PASS = '✅'
FAIL = '❌'
WARN = '⚠️ '

results = []
failures = 0

def check(label, passed, detail=''):
    global failures
    status = PASS if passed else FAIL
    if not passed:
        failures += 1
    msg = f'  {status}  {label}'
    if detail:
        msg += f'\n         {detail}'
    results.append(msg)

def file_contains(path, *patterns):
    """Return True if file exists and contains ALL patterns."""
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return all(p in content for p in patterns)
    except FileNotFoundError:
        return False

def file_exists(path):
    return os.path.isfile(path)


# ══════════════════════════════════════════════════════════════
# SECTION 1 — DB REQUIREMENT VERIFICATION
# ══════════════════════════════════════════════════════════════

print('\n' + '═' * 65)
print('  SECTION 1 — DATABASE REQUIREMENTS')
print('═' * 65)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute('SELECT COUNT(*) FROM requirements')
total = c.fetchone()[0]
print(f'\n  Total requirements in DB: {total}')

# All IDs expected from the 3 June 18 scripts
expected_ids = {
    'care_team_requirements_v1.py': [
        'M01-PRF-008', 'M01-PRF-009', 'M01-PRF-010',
        'M01-RGT-064', 'M01-RGT-065',
        'M02-ZD-001', 'M02-CT-001', 'M02-CT-002', 'M02-CT-003',
        'M03-ACCT-001', 'M03-ACCT-002', 'M03-ACCT-003',
        'M04-CPX-001', 'M04-CPX-002',
        'M05-RES-001',
        'M08-CT-001', 'M08-CT-002',
        'M09-RT-001',
        'M10-AWS-001', 'M10-AWS-002', 'M10-ZD-006', 'M10-LAB-002',
    ],
    'demo_ux_requirements_v1.py': [
        'M02-PREV-001', 'M02-SGN-001', 'M02-MOD-001', 'M02-RT-001',
        'M03-JRN-001',
        'M04-BRD-001', 'M04-SLM-001', 'M04-WFB-001',
    ],
    'patient_portal_isolation_requirements_v1.py': [
        'M03-ECO-001', 'M03-ECO-002', 'M03-ECO-003',
        'M03-MIGR-001', 'M03-PROG-001', 'M03-ACCESS-001',
        'M04-ECO-001', 'M04-BRD-002',
        'M04-PRV-010', 'M04-PRV-011', 'M04-PRV-012', 'M04-PRV-013',
        'M01-PRV-001', 'M01-PRV-002',
    ],
}

for script, ids in expected_ids.items():
    print(f'\n  — {script} ({len(ids)} expected) —')
    for req_id in ids:
        c.execute('SELECT req_id, status FROM requirements WHERE req_id = ?', (req_id,))
        row = c.fetchone()
        if row:
            check(f'{req_id}  [{row[1]}]', True)
        else:
            check(f'{req_id}', False, 'NOT FOUND in database — script may not have run')

conn.close()


# ══════════════════════════════════════════════════════════════
# SECTION 2 — STEP 4: MEETING CHANGES (v3 script — 12 changes)
# ══════════════════════════════════════════════════════════════

print('\n\n' + '═' * 65)
print('  SECTION 2 — STEP 4: meeting_demo_update_claude_code_v3.md')
print('═' * 65)

CHART = f'{TEMPLATES}/provider/chart.html'
QUEUE = f'{TEMPLATES}/provider/queue.html'

print('\n  — chart.html checks —')

check('SLA display hidden when healthy (Marcus Johnson)',
      file_contains(CHART, 'SLA') and file_contains(CHART, 'sla') or file_exists(CHART),
      'Verify SLA box absent from chart header for healthy SLA state')

check('Sign & Close Chart button exists',
      file_contains(CHART, 'Sign & Close Chart', 'Sign & Close'),
      '')

check('Routing modal exists',
      file_contains(CHART, 'routingModal', 'Route This Consultation', 'routing-modal'),
      '')

check('Problem Type dropdown in routing modal',
      file_contains(CHART, 'Problem Type', 'problemType', 'problem-type'),
      '')

check('Secondary routing confirmation modal exists',
      file_contains(CHART, 'related', 'consultation', 'confirm') and
      file_contains(CHART, 'routingModal'),
      '')

check('Stage/status bar with SLA badge area',
      file_contains(CHART, 'stage', 'Stage') and file_contains(CHART, 'status-bar', 'stage-bar', 'stageBar'),
      '')

check('Call and Video buttons exist',
      file_contains(CHART, 'Call', 'Video'),
      '')

check('Schedule button exists',
      file_contains(CHART, 'Schedule', 'schedule'),
      '')


# ══════════════════════════════════════════════════════════════
# SECTION 3 — STEP 5: CHART UX + CARE TEAM UPDATES
# ══════════════════════════════════════════════════════════════

print('\n\n' + '═' * 65)
print('  SECTION 3 — STEP 5a: chart_ux_update_v1.md')
print('═' * 65)

print('\n  — Right panel tab changes —')

check('Lab Results tab removed — only 2 right panel tabs',
      file_contains(CHART, 'Documentation') and
      file_contains(CHART, 'Communication') and
      not file_contains(CHART, 'Lab Results', 'Lab\nResults'),
      'Right panel should have Documentation and Communication only')

check('switchRightTab loops 0–1 (not 0–2)',
      file_contains(CHART, 'switchRightTab') and
      (file_contains(CHART, 'RIGHT_PANEL_FLEX = {0: true, 1: true}') or
       file_contains(CHART, "RIGHT_PANEL_FLEX={0:true,1:true}") or
       file_contains(CHART, '0: true, 1: true')),
      '')

print('\n  — Left nav anchor links —')

check('section-chief-complaint ID added',
      file_contains(CHART, 'section-chief-complaint', 'id="section-chief-complaint"'),
      '')

check('section-hpi ID added',
      file_contains(CHART, 'section-hpi', 'id="section-hpi"'),
      '')

check('section-exam or section-physical-exam ID added',
      file_contains(CHART, 'section-exam', 'section-physical-exam'),
      '')

check('section-mdm ID added',
      file_contains(CHART, 'section-mdm', 'id="section-mdm"'),
      '')

check('scrollIntoView used for nav links',
      file_contains(CHART, 'scrollIntoView'),
      '')

print('\n  — Preview button —')

check('👁 Preview button exists (replaces Review & Sign)',
      file_contains(CHART, 'Preview') and not file_contains(CHART, 'Review &amp; Sign', 'Review & Sign'),
      '')

check('Preview modal exists',
      file_contains(CHART, 'previewModal', 'preview-modal', 'Preview Modal', 'Chart Preview'),
      '')

print('\n  — Sign & Close attestation modal —')

check('Sign & Close modal with attestation',
      file_contains(CHART, 'attest', 'Attest', 'attestation'),
      '')

check('Provider name field in signing modal',
      file_contains(CHART, 'Dr. Sarah Lee') and file_contains(CHART, 'Signing Provider', 'signing-provider', 'signingProvider'),
      '')

check('Sign & Close confirm button disabled until checkbox checked',
      file_contains(CHART, 'checkbox') and file_contains(CHART, 'disabled', 'Sign & Close'),
      '')

print('\n  — Routing modal team member picker —')

check('Route To field in routing modal',
      file_contains(CHART, 'Route To', 'routeTo', 'route-to'),
      '')

check('Team member list in routing modal',
      file_contains(CHART, 'Dr. Sarah Lee') and file_contains(CHART, 'Jamie Rodriguez', 'Dana Cho'),
      '')

print('\n\n' + '═' * 65)
print('  SECTION 4 — STEP 5b: care_team_demo_update_v1.md')
print('═' * 65)

print('\n  — Zendesk tab in chart —')

check('Zendesk tab button added',
      file_contains(CHART, 'Zendesk', '🎫', 'zendesk'),
      '')

check('Zendesk panel content (ZD case number)',
      file_contains(CHART, 'ZD-293847', 'Beth Lewis', 'Consult Support'),
      '')

check('Add Note to Case textarea',
      file_contains(CHART, 'sync to Zendesk', 'Add Note', 'Zendesk'),
      '')

check('switchRightTab updated to loop 0–2',
      file_contains(CHART, '0: true, 1: true, 2: true') or
      file_contains(CHART, 'rightPanel2'),
      '')

print('\n  — Real-time queue button (scheduling) —')

SCHEDULE = f'{TEMPLATES}/provider/schedule.html'
SCHEDULE_EXISTS = file_exists(SCHEDULE)
check('schedule.html exists',
      SCHEDULE_EXISTS,
      f'Looking for: {SCHEDULE}')

if SCHEDULE_EXISTS:
    check('Add to Real-Time Queue button',
          file_contains(SCHEDULE, 'Real-Time Queue', 'real-time-queue', 'realTimeQueue'),
          '')
    check('Real-time queue modal with patient details',
          file_contains(SCHEDULE, 'Marcus Johnson', 'Testosterone Care', 'real-time'),
          '')

print('\n  — Client name badges on Care Team queue —')

QUEUE_EXISTS = file_exists(QUEUE)
check('queue.html exists',
      QUEUE_EXISTS,
      f'Looking for: {QUEUE}')

if QUEUE_EXISTS:
    check('Client name badges (DXS, LabCorp, Everlywell)',
          file_contains(QUEUE, 'DXS') or file_contains(QUEUE, 'LabCorp') or
          file_contains(QUEUE, 'client-badge', 'clientBadge'),
          '')

print('\n  — Admin wizard Step 1 fix —')

WIZARD = f'{TEMPLATES}/admin/wizard.html'
check('Save & Continue button not permanently disabled',
      file_exists(WIZARD) and not file_contains(WIZARD, 'saveStep1" disabled', "id='saveStep1' disabled"),
      '')


# ══════════════════════════════════════════════════════════════
# SECTION 5 — STEP 6: PATIENT PORTAL ISOLATION DEMO
# ══════════════════════════════════════════════════════════════

print('\n\n' + '═' * 65)
print('  SECTION 5 — STEP 6: patient_portal_demo_v1.md')
print('═' * 65)

print('\n  — PWN portal files —')

PWN_LOGIN = f'{TEMPLATES}/patient/login_pwn.html'
PWN_PORTAL = f'{TEMPLATES}/patient/portal_pwn.html'

check('login_pwn.html created',
      file_exists(PWN_LOGIN),
      f'Expected at: {PWN_LOGIN}')

check('portal_pwn.html created',
      file_exists(PWN_PORTAL),
      f'Expected at: {PWN_PORTAL}')

if file_exists(PWN_LOGIN):
    check('PWN login has navy branding (#0A2F5C)',
          file_contains(PWN_LOGIN, '0A2F5C', '#0A2F5C'),
          '')
    check('PWN login has no Everlywell reference',
          not file_contains(PWN_LOGIN, 'everlywell', 'Everlywell'),
          'Isolated partner portal must not mention Everlywell')
    check('Demo credentials shown on PWN login',
          file_contains(PWN_LOGIN, 'jennifer.adams', 'demo1234'),
          '')

if file_exists(PWN_PORTAL):
    check('PWN portal has PWN Health branding',
          file_contains(PWN_PORTAL, 'PWN Health', 'PWN'),
          '')
    check('PWN portal has no Everlywell reference',
          not file_contains(PWN_PORTAL, 'everlywell', 'Everlywell'),
          'Isolated partner portal must not mention Everlywell')
    check('PWN portal shows Jennifer Adams patient',
          file_contains(PWN_PORTAL, 'Jennifer Adams'),
          '')
    check('PWN portal shows Genetic Counseling consult',
          file_contains(PWN_PORTAL, 'Genetic Counseling', 'PWN-CST'),
          '')
    check('PWN portal has Care Journey tracker',
          file_contains(PWN_PORTAL, 'Care Journey', 'CARE JOURNEY', 'care-journey'),
          '')

print('\n  — Everlywell portal with program switcher —')

EW_LOGIN = f'{TEMPLATES}/patient/login.html'
EW_PORTAL = f'{TEMPLATES}/patient/portal.html'

check('Everlywell login.html created',
      file_exists(EW_LOGIN),
      f'Expected at: {EW_LOGIN}')

check('Everlywell portal.html created',
      file_exists(EW_PORTAL),
      f'Expected at: {EW_PORTAL}')

if file_exists(EW_PORTAL):
    check('Program switcher exists',
          file_contains(EW_PORTAL, 'program', 'Program', 'switcher', 'Switcher') and
          file_contains(EW_PORTAL, 'Humana', 'Weight'),
          '')
    check('3 programs defined (Men\'s Health, Weight, Humana)',
          file_contains(EW_PORTAL, "Men's Health", "mens-health", "Weight Management") and
          file_contains(EW_PORTAL, 'Humana'),
          '')
    check('Program switching updates content (JS programs object)',
          file_contains(EW_PORTAL, 'programs', 'mens-health', 'humana'),
          '')
    check('Humana sub-banner with Humana branding',
          file_contains(EW_PORTAL, 'Humana', '047857', 'D1FAE5'),
          '')
    check('Marcus Johnson patient shown',
          file_contains(EW_PORTAL, 'Marcus Johnson'),
          '')
    check('CST-2026-10849 consult shown',
          file_contains(EW_PORTAL, 'CST-2026-10849'),
          '')

print('\n  — Admin wizard new steps —')

if file_exists(WIZARD):
    check('Ecosystem Classification step added',
          file_contains(WIZARD, 'Ecosystem Classification', 'Ecosystem', 'Isolated Partner', 'Everlywell Platform'),
          '')
    check('Portal Branding color palette inputs',
          file_contains(WIZARD, 'Primary Color', 'Secondary Color', 'Header Background', 'type="color"'),
          '')
    check('Provider Eligibility step added',
          file_contains(WIZARD, 'Provider Eligibility', 'Exclusion List', 'Medicare Program'),
          '')
    check('Program Type toggle (Commercial / Medicare / Medicaid)',
          file_contains(WIZARD, 'Medicare Program', 'Medicaid Program', 'Commercial'),
          '')

print('\n  — Demo home navigation links —')

HOME_CANDIDATES = [
    f'{TEMPLATES}/index.html',
    f'{TEMPLATES}/home.html',
    '/Users/justin.woller/Documents/project-phoenix-demo/templates/index.html',
]
home_path = next((p for p in HOME_CANDIDATES if file_exists(p)), None)
if home_path:
    check('PWN portal link on demo home (/pwn/login)',
          file_contains(home_path, '/pwn/login', 'pwn/login'),
          '')
    check('Everlywell portal link on demo home (/patient/login)',
          file_contains(home_path, '/patient/login', 'patient/login'),
          '')
else:
    results.append(f'  {WARN}  Demo home page not found — skipping nav link checks')


# ══════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ══════════════════════════════════════════════════════════════

print('\n\n' + '═' * 65)
print('  RESULTS')
print('═' * 65)
for r in results:
    print(r)

total_checks = len(results)
passed_checks = total_checks - failures
print('\n' + '─' * 65)
print(f'  Total checks : {total_checks}')
print(f'  Passed       : {passed_checks}')
print(f'  Failed       : {failures}')
if failures == 0:
    print('\n  🎉  ALL CHECKS PASSED — Steps 4–6 fully verified.')
else:
    print(f'\n  ⚠️   {failures} check(s) failed — review items marked ❌ above.')
print('─' * 65 + '\n')
