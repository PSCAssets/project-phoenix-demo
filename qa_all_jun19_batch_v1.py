#!/usr/bin/env python3
"""
Project Phoenix — Comprehensive QA for June 18–19 Batch
Covers all 3 scripts from this batch:
  1. open_items_jun18_v1.py    →  OPEN-006, OPEN-007, OPEN-008
  2. jun18_meeting_requirements_v1.py  →  25 requirements (M01–M10)
  3. open_items_jun19_v1.py    →  OPEN-009, OPEN-010

Total checks: 30 (25 requirements + 5 open items)
"""

import sqlite3

DB_PATH = '/Users/justin.woller/Documents/project-phoenix-demo/project_phoenix.db'

PASS = '✅'
FAIL = '❌'

results = []
failures = 0

def check(label, passed, detail=''):
    global failures
    status = PASS if passed else FAIL
    if not passed:
        failures += 1
    msg = f'  {status}  {label}'
    if detail:
        msg += f'\n         └─ {detail}'
    results.append(msg)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute('SELECT COUNT(*) FROM requirements')
total_db = c.fetchone()[0]

# ─────────────────────────────────────────────────────────────────────────────
print('\n' + '═' * 68)
print('  SCRIPT 1 — open_items_jun18_v1.py (3 open items expected)')
print('═' * 68)
# ─────────────────────────────────────────────────────────────────────────────

script1_open = {
    'OPEN-006': 'IVR / Outbound Contact',
    'OPEN-007': 'Provider Patient History',
    'OPEN-008': 'Critical Alert Service',
}
for req_id, label in script1_open.items():
    c.execute('SELECT req_id, status FROM requirements WHERE req_id = ?', (req_id,))
    row = c.fetchone()
    if row:
        is_open = row[1] == 'Open'
        check(f'{req_id}  [{row[1]}]  — {label}', is_open,
              'Status should be Open' if not is_open else '')
    else:
        check(f'{req_id}  — {label}', False, 'NOT FOUND in database')

# ─────────────────────────────────────────────────────────────────────────────
print('\n' + '═' * 68)
print('  SCRIPT 2 — jun18_meeting_requirements_v1.py (25 requirements)')
print('═' * 68)
# ─────────────────────────────────────────────────────────────────────────────

script2 = {
    # M01 — Roles & Responsibilities
    'M01-RGT-066': ('M01', 'QA Reviewer role'),
    'M01-RGT-067': ('M01', 'GC Administrator role'),

    # M02 — Provider Portal
    'M02-CLB-001': ('M02', 'Clinical content library access from chart'),
    'M02-LNK-001': ('M02', 'Linked consult view + prior note import'),

    # M04 — Admin Portal
    'M04-CLB-001': ('M04', 'Admin Portal clinical content library feature'),
    'M04-CLB-002': ('M04', 'Article metadata fields'),
    'M04-QA-001':  ('M04', 'QA stage configuration per care product'),
    'M04-CHK-001': ('M04', 'Pre-consult checklist config per care product/role'),
    'M04-NIH-001': ('M04', 'Research consult linkage config in care product wizard'),

    # M05 — Async Consultation
    'M05-LNK-001': ('M05', 'Consult linking (Pre-Test/Post-Test/Research/Rescheduled)'),
    'M05-LNK-002': ('M05', 'Prior note import from linked consult'),
    'M05-CPX-001': ('M05', 'Consult initiator field (platform vs. patient)'),

    # M07 — Intake Process
    'M07-MIN-001': ('M07', 'Minor patient ordering enforcement'),
    'M07-POA-001': ('M07', 'POA documentation enforcement for third-party orders'),
    'M07-MBR-001': ('M07', 'Member lookup at intake from Members DB'),
    'M07-MBR-002': ('M07', 'Member → patient conversion on first consult'),

    # M08 — Notification Engine
    'M08-BLB-001': ('M08', 'Blurb request queue (replaces Slack #unusual_gc_cases)'),
    'M08-BLB-002': ('M08', 'Blurb 24-hour SLA tracking with escalation'),
    'M08-QAF-001': ('M08', 'QA failure routing → GC Administrator queue'),
    'M08-TZ-001':  ('M08', 'Timezone-aware GC consult notifications'),

    # M09 — Scheduling
    'M09-CHK-001': ('M09', 'Pre-consult checklist as tracked workflow stage'),
    'M09-PRV-001': ('M09', 'Provider prior relationship indicators on scheduling'),
    'M09-PRV-002': ('M09', 'Provider gender/language preference filters'),
    'M09-SVC-001': ('M09', 'Service type duration validation at scheduling'),

    # M10 — Integrations
    'M10-ELG-001': ('M10', 'Health plan eligibility CSV ingestion into Members DB'),
}

for req_id, (module, label) in script2.items():
    c.execute('SELECT req_id, status, module_id FROM requirements WHERE req_id = ?', (req_id,))
    row = c.fetchone()
    if row:
        check(f'{req_id}  [{row[1]}]  {row[2]}  — {label}', True)
    else:
        check(f'{req_id}  {module}  — {label}', False, 'NOT FOUND in database')

# ─────────────────────────────────────────────────────────────────────────────
print('\n' + '═' * 68)
print('  SCRIPT 3 — open_items_jun19_v1.py (2 open items expected)')
print('═' * 68)
# ─────────────────────────────────────────────────────────────────────────────

script3_open = {
    'OPEN-009': 'Eli Lilly blinded study patient intake',
    'OPEN-010': 'Texas state routing — ExomeDx / GeneDx',
}
for req_id, label in script3_open.items():
    c.execute('SELECT req_id, status FROM requirements WHERE req_id = ?', (req_id,))
    row = c.fetchone()
    if row:
        is_open = row[1] == 'Open'
        check(f'{req_id}  [{row[1]}]  — {label}', is_open,
              'Status should be Open' if not is_open else '')
    else:
        check(f'{req_id}  — {label}', False, 'NOT FOUND in database')

# ─────────────────────────────────────────────────────────────────────────────
print('\n' + '═' * 68)
print('  SECTION 4 — Open Items Full Register')
print('═' * 68)
# ─────────────────────────────────────────────────────────────────────────────

c.execute('''SELECT req_id, section, owner
             FROM requirements
             WHERE status = \'Open\'
             ORDER BY req_id''')
open_rows = c.fetchall()
print(f'\n  Total open items in DB: {len(open_rows)}')
for r in open_rows:
    print(f'  {r[0]}  {r[1]}')
    print(f'         Owner: {r[2]}')

# ─────────────────────────────────────────────────────────────────────────────
print('\n' + '═' * 68)
print('  SECTION 5 — Module Coverage Summary (this batch)')
print('═' * 68)
# ─────────────────────────────────────────────────────────────────────────────

batch_ids = list(script2.keys()) + list(script1_open.keys()) + list(script3_open.keys())
module_counts = {}
for req_id in batch_ids:
    if req_id.startswith('OPEN'):
        bucket = 'OPEN'
    else:
        bucket = req_id.split('-')[0]
    module_counts[bucket] = module_counts.get(bucket, 0) + 1

print()
for module in sorted(module_counts):
    c.execute('SELECT COUNT(*) FROM requirements WHERE req_id LIKE ?', (f'{module}%',))
    total_module = c.fetchone()[0]
    batch_count = module_counts[module]
    print(f'  {module:<6}  +{batch_count} this batch  ({total_module} total in DB)')

conn.close()

# ─────────────────────────────────────────────────────────────────────────────
print('\n\n' + '═' * 68)
print('  RESULTS')
print('═' * 68)
# ─────────────────────────────────────────────────────────────────────────────

for r in results:
    print(r)

total_checks = len(results)
passed_checks = total_checks - failures

print('\n' + '─' * 68)
print(f'  Total requirements in DB : {total_db}')
print(f'  Checks run               : {total_checks}  (Scripts 1 + 2 + 3)')
print(f'  Passed                   : {passed_checks}')
print(f'  Failed                   : {failures}')
if failures == 0:
    print('\n  🎉  ALL 30 CHECKS PASSED — Jun 18-19 batch fully verified.')
else:
    print(f'\n  ⚠️   {failures} check(s) failed — review items marked ❌ above.')
print('─' * 68 + '\n')
