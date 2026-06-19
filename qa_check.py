"""
Project Phoenix Demo — QA Check Script
Run: python3 qa_check.py
Paste the full output into the Claude chat for review.
"""

import urllib.request
import urllib.error
from datetime import datetime

BASE = "http://127.0.0.1:5000"

ROUTES = [
    ("/",                   "Login screen",             ["Select your account", "Log in as"]),
    ("/provider/",          "MD Dashboard",             ["Dr. Sarah Lee", "Dashboard"]),
    ("/provider/queue",     "MD Queue",                 ["Queue", "Patient"]),
    ("/provider/chart/1",       "Patient Chart (A1C)",     ["Marcus Johnson", "Testosterone"]),
    ("/provider/chart?product=awv", "AWV Chart (D.R.)",    ["Annual Wellness Visit", "PRAPARE", "DEXA"]),
    ("/provider/chart/1/async", "Async Consult",           ["Questionnaire", "Provider Response"]),
    ("/provider/chart/1/phone", "Phone Consult",           ["Phone Consultation", "SOAP"]),
    ("/provider/chart/1/video", "Video Consult",           ["Video Consultation", "Join"]),
    ("/provider/new-patient",   "New Patient Intake",      ["Demographics", "Care Product"]),
    ("/provider/schedule",  "Schedule screen",           ["Schedule", "Week"]),
    ("/provider/messages",  "Messages screen",           ["Staff Messages", "Jennifer Martinez"]),
    ("/provider/alerts",    "Alerts screen",             ["Alerts", "SLA"]),
    ("/provider/settings",  "Settings",                 []),
    ("/provider/notifications", "Provider Notifications", ["Notifications", "SLA"]),
    ("/provider/rn",        "RN Dashboard",             ["Jennifer Martinez", "RN"]),
    ("/provider/ma",        "MA Dashboard",             ["Michael Torres", "MA"]),
    ("/provider/np",        "NP Dashboard",             ["Maria Rodriguez", "NP"]),
    ("/provider/gc",        "GC Dashboard",             ["Lisa Park", "Genetic"]),
    ("/provider/lab-orders",    "Lab Orders stub",          ["Lab Order"]),
    ("/provider/oversight",     "Provider Oversight",       ["Attestation Board", "Lab Order"]),
    ("/provider/future-visits", "Future Visits",            ["Future Visits", "Scheduled"]),
    ("/care-team/",         "Care Team Dashboard",      ["Alex Kim", "My Patient Activity"]),
    ("/patient/",               "Patient Dashboard",   ["Jamie Rivera", "Testosterone"]),
    ("/patient/consultations",  "My Consultations",    ["Consultation", "Dr. Sarah Lee"]),
    ("/patient/appointments",   "Appointments",        ["Jun 18", "Video"]),
    ("/patient/messages",       "Patient Messages",    ["Dr. Sarah Lee", "lab results"]),
    ("/patient/labs",           "Lab Results",         ["Testosterone Panel", "Results Ready"]),
    ("/patient/labs/detail?lab=testosterone", "Lab Detail — Testosterone", ["Testosterone Panel", "Normal"]),
    ("/patient/labs/detail?lab=hba1c",        "Lab Detail — HbA1c",        ["HbA1c", "Elevated"]),
    ("/patient/health-profile", "Health Profile",      ["Jamie Rivera", "Testosterone"]),
    ("/patient/enroll",     "Enrollment",               []),
    ("/patient/care-plan",  "Care Plan",                []),
    ("/admin/",                "Admin Dashboard",      ["Care Products", "Chris Navarro"]),
    ("/admin/care-products",   "Care Products List",   ["Testosterone", "Add Care Product"]),
    ("/admin/care-product/new","Care Product Wizard",  ["Step 1", "Select Client", "A1C Management", "Humana"]),
    ("/admin/clients",        "Client Management",    ["Client Management", "CareFirst"]),
    ("/admin/clients/new",    "Add Client form",      ["Add Client", "Client Name"]),
    ("/admin/clients/1/edit", "Edit Client form",     ["Edit Client", "Humana"]),
    ("/admin/providers",       "Provider Listing",      ["Provider Listing", "Verifiable"]),
    ("/patient/documents",     "Patient Documents",     ["My Documents", "Telehealth Consent"]),
    ("/patient/settings",      "Patient Settings",      ["Account Settings", "Notifications"]),
    ("/admin/users",           "Admin User Mgmt",       ["User Management", "Sarah Lee"]),
    ("/admin/integrations",    "Admin Integrations",    ["Integration Health", "Athena"]),
    ("/admin/sla-config",      "Admin SLA Config",      ["SLA Configuration", "Testosterone"]),
    ("/admin/notifications",   "Admin Notifications",   ["Notification Templates", "SLA"]),
    ("/admin/audit-log",       "Admin Audit Log",       ["Audit Log", "Chris Navarro"]),
    ("/admin/reports",         "Admin Reports",         ["Reports", "Provider Activity"]),
    ("/logout",             "Logout redirect",          []),
    ("/scheduler/",           "Scheduler Dashboard",       ["David Nguyen", "Today's Appointments"]),
    ("/scheduler/schedule",   "Scheduling Tool",           ["Scheduling Tool", "Patient First"]),
    ("/scheduler/search-patient", "Patient Search",        ["Patient Search", "Member Lookup"]),
    ("/admin/coordinator",   "Coordinator Dashboard",     ["Coordinator Dashboard", "SLA Monitor"]),
    ("/provider/pharmacy",   "Pharmacy Fulfillment",      ["Pharmacy Fulfillment", "GoGoMeds"]),
    ("/provider/billing",    "Billing & Compensation",    ["Billing", "Athena"]),
    # Change 1 — PWN Health isolated portal
    ("/pwn/login",            "PWN Login",                 ["PWN Health", "jennifer.adams"]),
    ("/pwn/portal",           "PWN Portal",                ["PWN Health", "Jennifer Adams", "Genetic Counseling"]),
    # Change 2 — Everlywell multi-program portal
    ("/patient/login",        "Everlywell Login",          ["everlywell", "marcus.johnson"]),
    ("/patient/portal",       "Everlywell Portal",         ["everlywell", "Marcus Johnson", "Testosterone"]),
]

BLANK_SIGNALS = ["undefined", "null", "{{", "}}", "lorem ipsum",
                 "<body></body>", "<main></main>", "<div></div>"]

def check(path, label, keywords):
    url = BASE + path
    try:
        resp = urllib.request.urlopen(urllib.request.Request(url), timeout=5)
        status = resp.getcode()
        html = resp.read().decode("utf-8", errors="ignore").lower()
        missing = [k for k in keywords if k.lower() not in html] if keywords else []
        content_ok = "✅" if not missing else f"⚠️  missing: {', '.join(missing)}"
        if not keywords:
            content_ok = "✅" if len(html) > 500 else "⚠️  short response"
        blanks = [s for s in BLANK_SIGNALS if s in html]
        notes = (f" | ⚠️  blank signals: {blanks}" if blanks else "") + \
                (f" | ⚠️  very short ({len(html)} chars)" if len(html) < 300 and path != "/logout" else "")
    except urllib.error.HTTPError as e:
        status, content_ok, notes = e.code, "❌ HTTP error", ""
    except urllib.error.URLError:
        status, content_ok, notes = "DOWN", "❌ server not reachable", ""
    except Exception as e:
        status, content_ok, notes = "ERR", f"❌ {str(e)[:40]}", ""
    return status, content_ok, notes

print("=" * 70)
print(f"  PROJECT PHOENIX — DEMO QA REPORT")
print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  |  {BASE}")
print("=" * 70)
p = w = f = 0
rows = []
for path, label, keywords in ROUTES:
    status, content_ok, notes = check(path, label, keywords)
    ok = status == 200 and "❌" not in content_ok and "⚠️" not in content_ok
    fail = str(status) in ["DOWN","ERR"] or "❌" in content_ok
    if ok:   p += 1; icon = "✅"
    elif fail: f += 1; icon = "❌"
    else:    w += 1; icon = "⚠️ "
    rows.append((icon, status, label, path, content_ok, notes))
print(f"\n{'ST':>4}  {'SCREEN':<28}  {'PATH':<28}  CONTENT")
print("-" * 70)
for icon, status, label, path, content_ok, notes in rows:
    print(f"{icon} {str(status):>3}  {label:<28}  {path:<28}  {content_ok}{notes}")
print("\n" + "=" * 70)
print(f"  SUMMARY:  ✅ {p} pass  |  ⚠️  {w} warn  |  ❌ {f} fail  |  {len(ROUTES)} total")
print(f"  STATUS:   {'ALL CLEAR — demo ready' if f==0 and w==0 else 'WARNINGS PRESENT' if f==0 else 'FAILURES FOUND'}")
print("=" * 70)
