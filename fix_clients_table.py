"""
fix_clients_table.py
Creates the missing 'clients' table in project_phoenix.db with demo data.
Run ONCE with the Flask app stopped:
  python3 ~/Documents/project-phoenix-demo/fix_clients_table.py
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "project_phoenix.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Check if table already exists
existing = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clients'").fetchone()
if existing:
    print("clients table already exists — no action needed.")
    conn.close()
    exit()

# Create the clients table
cur.execute("""
CREATE TABLE clients (
    client_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    client_name   TEXT NOT NULL,
    client_type   TEXT,
    primary_contact TEXT,
    contact_email TEXT,
    contact_phone TEXT,
    status        TEXT DEFAULT 'Active',
    date_added    TEXT
)
""")

# Insert sample demo data
clients = [
    ("Everlywell Direct",        "DTC",          "Justin Woller",   "justin.woller@everlywell.com", "512-555-0101", "Active",   "2026-01-15"),
    ("Acme Health Partners",     "Partner",      "Sarah Mitchell",  "smitchell@acmehealth.com",     "512-555-0102", "Active",   "2026-02-01"),
    ("Blueprint Genetics",       "Partner",      "Tom Reynolds",    "treynolds@blueprint.com",      "512-555-0103", "Active",   "2026-03-10"),
    ("CareFirst Insurance",      "Health Plan",  "Diana Chen",      "dchen@carefirst.com",           "512-555-0104", "Active",   "2026-03-22"),
    ("Southwest Regional Health","Health System","Mark Torres",     "mtorres@srh.org",               "512-555-0105", "Active",   "2026-04-05"),
    ("GeneDx Referral Program",  "Partner",      "Lisa Park",       "lpark@genedx.com",             "512-555-0106", "Active",   "2026-04-18"),
    ("PWN Health (Legacy)",      "Legacy",       "Brian Scott",     "bscott@pwnhealth.com",         "512-555-0107", "Inactive", "2025-11-01"),
]

cur.executemany("""
    INSERT INTO clients (client_name, client_type, primary_contact, contact_email, contact_phone, status, date_added)
    VALUES (?,?,?,?,?,?,?)
""", clients)

conn.commit()
count = cur.execute("SELECT COUNT(*) FROM clients").fetchone()[0]
print(f"✅ clients table created with {count} rows.")
print("You can now restart the Flask demo app.")
conn.close()
