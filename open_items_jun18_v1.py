#!/usr/bin/env python3
"""
Open Items — June 18, 2026
Adds 3 unresolved items to requirements DB as OPEN status
pending Jessica Wheeler and Riley clarification
"""

import sqlite3
from datetime import date

DB_PATH = '/Users/justin.woller/Documents/project-phoenix-demo/project_phoenix.db'
TODAY = str(date.today())

requirements = [

    ('OPEN-006', 'M08 - Notification Engine', 'IVR / Outbound Contact', 'All',
     'Platform must support IVR and AI-assisted initial outbound contact with the ability to transfer to a live agent.',
     'Current workflows use IVR and AI for initial outbound patient contacts. The new platform must maintain this capability — automated initial contact followed by a live agent transfer option when the patient engages. Full operational design pending team input.',
     'IVR/AI initial contact fires before a live agent is assigned. Patient can opt into live agent at any point during the automated contact. Transfer to live agent is logged to the activity timeline.',
     'TBD — pending operational details from Care Team and Engineering.',
     'TBD',
     'High', 'Open', 'M08', 'Engineering / Care Team Ops',
     'Jun 18 Care Team meeting — noted as existing capability to preserve', TODAY, TODAY, None),

    ('OPEN-007', 'M02 - Provider Portal', 'Provider Patient History', 'Provider Portal',
     'Confirm whether the provider portal can display a full patient history across all care products and client programs the provider is contracted for.',
     'Open legal question: can a provider see a patient\'s full consultation history across all programs (Everlywell ecosystem and potentially cross-client) when they access the patient chart? Or is the provider view scoped strictly to the consult they were assigned? Jessica Wheeler must review before this requirement can be finalized.',
     'TBD — pending Jessica Wheeler legal review.',
     'TBD — pending legal determination.',
     'If cross-program history is permitted, data isolation rules between PWN ecosystem and Everlywell ecosystem still apply.',
     'High', 'Open', 'M02', 'Legal / Engineering',
     'Jun 18 Care Team meeting — action item for Justin → Jessica Wheeler', TODAY, TODAY, None),

    ('OPEN-008', 'M02 - Provider Portal', 'Critical Alert Service', 'Provider Portal',
     'Confirm operational details of the third-party critical alert service currently used to route critical lab values to RN queue.',
     'Current critical alert workflow involves a third-party service. Before the M02-CT-002 requirement (critical alerts → RN queue with QA audit trail) can be fully designed, the operational details of this service must be confirmed — specifically: what triggers the alert, how it currently interfaces with Zendesk, and what the integration path to Project Phoenix looks like. Action item: Justin to verify with Riley.',
     'TBD — pending Riley / operational team clarification.',
     'TBD — pending operational details.',
     'Current requirement M02-CT-002 covers the platform behavior for critical alerts. This open item covers the integration path from the third-party service into the platform.',
     'High', 'Open', 'M02', 'Engineering / Clinical Ops',
     'Jun 18 Care Team meeting — action item for Justin → Riley', TODAY, TODAY, None),

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
print(f'\nDone. Inserted: {inserted} | Skipped: {skipped}')

# Show all open items
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("SELECT req_id, substr(user_story,1,70), owner FROM requirements WHERE status = 'Open' ORDER BY req_id")
rows = c.fetchall()
print(f'\n--- All Open Items ({len(rows)} total) ---')
for r in rows:
    print(f'  {r[0]}: {r[1]}')
    print(f'         Owner: {r[2]}')
conn.close()
