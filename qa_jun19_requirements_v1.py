#!/usr/bin/env python3
"""
Project Phoenix — QA Script for June 19 Requirements
Verifies all 25 new requirements from jun18_meeting_requirements_v1.py
and 2 OPEN items from open_items_jun19_v1.py
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
        msg += f'\n         {detail}'
    results.append(msg)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute('SELECT COUNT(*) FROM requirements')
total = c.fetchone()[0]

print('\n' + '═' * 65)
print('  SECTION 1 — jun18_meeting_requirements_v1.py (25 expected)')
print('═' * 65)

expected_jun18 = [
    # M01
    'M01-RGT-066', 'M01-RGT-067',
    # M02
    'M02-CLB-001', 'M02-LNK-001',
    # M04
    'M04-CLB-001', 'M04-CLB-002', 'M04-QA-001', 'M04-CHK-001', 'M04-NIH-001',
    # M05
    'M05-LNK-001', 'M05-LNK-002', 'M05-CPX-001',
    # M07
    'M07-MIN-001', 'M07-POA-001', 'M07-MBR-001', 'M07-MBR-002',
    # M08
    'M08-BLB-001', 'M08-BLB-002', 'M08-QAF-001', 'M08-TZ-001',
    # M09
    'M09-CHK-001', 'M09-PRV-001', 'M09-PRV-002', 'M09-SVC-001',
    # M10
    'M10-ELG-001',
]

for req_id in expected_jun18:
    c.execute('SELECT req_id, status, module_id FROM requirements WHERE req_id = ?', (req_id,))
    row = c.fetchone()
    if row:
        check(f'{req_id}  [{row[1]}]  {row[2]}', True)
    else:
        check(f'{req_id}', False, 'NOT FOUND in database')

print('\n' + '═' * 65)
print('  SECTION 2 — open_items_jun19_v1.py (2 expected)')
print('═' * 65)

expected_open = ['OPEN-009', 'OPEN-010']

for req_id in expected_open:
    c.execute("SELECT req_id, status FROM requirements WHERE req_id = ?", (req_id,))
    row = c.fetchone()
    if row:
        check(f'{req_id}  [{row[1]}]', row[1] == 'Open', 'Status should be Open')
    else:
        check(f'{req_id}', False, 'NOT FOUND in database')

print('\n' + '═' * 65)
print('  SECTION 3 — All Open Items Summary')
print('═' * 65)
c.execute("SELECT req_id, substr(user_story,1,65) FROM requirements WHERE status = 'Open' ORDER BY req_id")
open_rows = c.fetchall()
print(f'\n  Total open items: {len(open_rows)}')
for r in open_rows:
    print(f'  {r[0]}: {r[1]}')

conn.close()

print('\n\n' + '═' * 65)
print('  RESULTS')
print('═' * 65)
for r in results:
    print(r)

total_checks = len(results)
passed_checks = total_checks - failures
print('\n' + '─' * 65)
print(f'  Total requirements in DB : {total}')
print(f'  Checks run               : {total_checks}')
print(f'  Passed                   : {passed_checks}')
print(f'  Failed                   : {failures}')
if failures == 0:
    print('\n  🎉  ALL CHECKS PASSED — Jun 19 requirements fully verified.')
else:
    print(f'\n  ⚠️   {failures} check(s) failed — review items marked ❌ above.')
print('─' * 65 + '\n')
