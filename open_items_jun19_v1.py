#!/usr/bin/env python3
"""
Project Phoenix — Open Items June 19, 2026
Adds 2 unresolved items to requirements DB as OPEN status

OPEN-009: Eli Lilly blinded study patient intake
OPEN-010: Texas state routing for ExomeDx / GeneDx portal
"""

import sqlite3
from datetime import date

DB_PATH = '/Users/justin.woller/Documents/project-phoenix-demo/project_phoenix.db'
TODAY = str(date.today())

requirements = [

    ('OPEN-009', 'M07 - Intake Process', 'Blinded Study Patient Intake', 'All',
     'Confirm how patient identity is handled in the new platform for blinded clinical study referrals where standard patient identifiers are replaced by study participant IDs.',
     'The Eli Lilly APOE/LAKI study workflow uses a study participant ID (PID) and year of birth instead of standard patient name and date of birth for identity verification. The referral from Eli Lilly does not include the patient\'s full identifying information. The current GCA workflow requires manual verification by matching the PID on the result report against the PID in the referral notes. Before this intake pattern can be designed in Project Phoenix, the following must be confirmed: (1) Does Project Phoenix store the patient\'s actual name and DOB internally for HIPAA-compliant record-keeping while presenting only the study PID externally to Eli Lilly? (2) How does the platform map an incoming Eli Lilly referral (PID + year of birth) to an internal patient record if the patient has had a prior consult? (3) Does the LAKI Diversity Addendum dual-PID scenario (original PID and new PID) require special handling in the intake system? All three questions require confirmation with the Eli Lilly integration team before requirements can be finalized.',
     'TBD — pending confirmation on blinded study patient identity architecture and Eli Lilly integration design.',
     'TBD — pending operational and legal review of blinded study data handling.',
     'LAKI Diversity Addendum adds a secondary PID complexity — participants may have two PIDs (original and new) that must both be recognized.',
     'High', 'Open', 'M07', 'Engineering / Legal / Eli Lilly Integration',
     'WI GC Consult Prep — Eli Lilly APOE/LAKI blinded study workflow; left open Jun 19 2026', TODAY, TODAY, None),

    ('OPEN-010', 'M09 - Scheduling', 'Texas State Routing — ExomeDx', 'Provider Portal',
     'Confirm whether Texas-specific provider routing logic for ExomeDx (Probably Genetic) needs to be built into Project Phoenix scheduling.',
     'The current WI GC Consult Prep document includes a step for ExomeDx (Probably Genetic) consults: if the patient\'s state is Texas, the GCA must add a referral note: "PT in TX. Please assign Dr. Abraham as provider in GeneDx portal." This appears to reference routing in an external third-party portal (GeneDx), not in the PWN/Project Phoenix platform. Before building any state-based routing requirement, confirm: (1) Is this routing logic in GeneDx\'s external portal only, and therefore not applicable to Project Phoenix? (2) Or does Project Phoenix need to enforce a Texas-specific provider assignment rule for ExomeDx care products, directing assignment to a specific credentialed provider? (3) If yes, is this a general pattern (state-specific provider assignment rules per care product) that should be built as a configurable feature in the Admin Portal?',
     'TBD — pending confirmation on whether Texas ExomeDx routing is external (GeneDx portal only) or requires a Project Phoenix requirement.',
     'TBD — pending operational review.',
     'If this is a general pattern (state-specific provider assignment overrides), it would be configured as part of the Provider Eligibility step in the care product wizard and would apply beyond just ExomeDx.',
     'Medium', 'Open', 'M09', 'Engineering / Operations',
     'WI GC Consult Prep — Texas patient ExomeDx routing note; left open Jun 19 2026', TODAY, TODAY, None),

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

# Show all open items
c.execute("SELECT req_id, substr(user_story,1,80), owner FROM requirements WHERE status = 'Open' ORDER BY req_id")
rows = c.fetchall()
print(f'\n--- All Open Items ({len(rows)} total) ---')
for r in rows:
    print(f'  {r[0]}: {r[1]}')
    print(f'         Owner: {r[2]}')
conn.close()

print(f'\nDone. Inserted: {inserted} | Skipped: {skipped}')
