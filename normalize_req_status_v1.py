#!/usr/bin/env python3
"""
Project Phoenix — Normalize Requirements Status
Remaps all status values to the correct Project Phoenix convention:
  Approved   — requirement is defined and in scope (default)
  Open       — blocked by an unresolved open question
  Deprecated — removed from scope
  v2.0       — future phase, not in current build scope

Run from: ~/Documents/project-phoenix-demo/
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'project_phoenix.db')

STATUS_MAP = {
    # → Approved
    'active':       'Approved',
    'Active':       'Approved',
    'Not Started':  'Approved',
    'Pending':      'Approved',
    'Backlog':      'Approved',
    'Approved':     'Approved',   # already correct, no-op

    # → Open
    'open':         'Open',
    'Open':         'Open',       # already correct, no-op

    # → Deprecated
    'deprecated':   'Deprecated',
    'Deprecated':   'Deprecated', # already correct, no-op
    'Moved to M08': 'Deprecated',
    'N/A':          'Deprecated',

    # → v2.0
    'Future':       'v2.0',
    'Deferred':     'v2.0',
}

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Snapshot counts before
c.execute('SELECT status, COUNT(*) FROM requirements GROUP BY status ORDER BY COUNT(*) DESC')
before = c.fetchall()

changes = {}
for old_status, new_status in STATUS_MAP.items():
    if old_status == new_status:
        continue  # skip no-ops
    c.execute('UPDATE requirements SET status = ? WHERE status = ?', (new_status, old_status))
    n = c.rowcount
    if n > 0:
        changes[old_status] = (new_status, n)

conn.commit()

# Snapshot counts after
c.execute('SELECT status, COUNT(*) FROM requirements GROUP BY status ORDER BY COUNT(*) DESC')
after = c.fetchall()

conn.close()

print('\n── normalize_req_status_v1.py ──')
print('\nChanges applied:')
for old, (new, n) in changes.items():
    print(f'  "{old}" → "{new}": {n} rows')

print('\nStatus breakdown after normalization:')
for row in after:
    print(f'  {row[0]}: {row[1]}')

total = sum(r[1] for r in after)
print(f'\n  Total requirements: {total}')
print('\n  Done.\n')
