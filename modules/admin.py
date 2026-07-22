import os
import sqlite3
from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint("admin", __name__)

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'project_phoenix.db')


def _db():
    return sqlite3.connect(DB_PATH)


# ── Patients / POA & Guardian Access (M03-POA-003a) ───────────────────────────
# Demo-only in-memory records — no live patient DB backs this app. Names/IDs
# match the corresponding entries already used in the QA Reviewer queue and
# the patient-portal POA upload demo, so the same case reads consistently
# across all three portals.
PATIENTS = {
    "PT-2026-00590": {
        "name": "Jamie Rivera", "dob": "1987-03-14", "care_products": ["Testosterone Care", "Weight Management"],
        "poa": {
            "holder_name": "Robert Chen", "phone": "(512) 555-0148", "email": "robert.chen@example.com",
            "relationship": "Power of Attorney", "status": "verified",
            "documents": ["Power of Attorney (4 pages)", "Government-Issued Photo ID"],
            "date_reviewed": "Jun 2, 2026", "reviewer": "Quinn Patel, QA Reviewer",
            "rejection_code": None, "expiry": None,
            "note": "Covers healthcare decisions for this account. Reused automatically per POA-009 — no new documents required for subsequent third-party requests.",
        },
        "audit": [
            {"date": "Jun 2, 2026 10:14 AM", "actor": "Quinn Patel, QA Reviewer", "action": "Verified POA for Robert Chen"},
            {"date": "Jun 2, 2026 9:47 AM", "actor": "Jamie Rivera (self-service)", "action": "Uploaded POA document + government ID"},
        ],
    },
    "PT-2026-00587": {
        "name": "Robert C.", "dob": "1979-11-02", "care_products": ["GLP-1 Weight Management"],
        "poa": {
            "holder_name": "Susan Cole", "phone": "(214) 555-0177", "email": "susan.cole@example.com",
            "relationship": "Power of Attorney (springing clause)", "status": "pending",
            "documents": ["Power of Attorney (3 pages)", "Physician's Certification of Incapacity", "Government-Issued Photo ID"],
            "date_reviewed": None, "reviewer": None, "rejection_code": None, "expiry": None,
            "note": "Springing clause disclosed at upload (POA-004) with certification attached. Awaiting QA Reviewer verification.",
        },
        "audit": [
            {"date": "Today 9:02 AM", "actor": "Jordan Patel, RN (submitted on patient's behalf)", "action": "Uploaded POA + Physician's Certification of Incapacity"},
        ],
    },
    "PT-2026-00659": {
        "name": "Ethan T. (minor)", "dob": "2014-06-21", "care_products": ["BRCA Hereditary Cancer"],
        "poa": {
            "holder_name": "Jennifer T.", "phone": "(919) 555-0122", "email": "jennifer.t@example.com",
            "relationship": "Legal Guardian (parent)", "status": "pending",
            "documents": ["Government-Issued Photo ID", "Guardianship/Parental Authority Documentation"],
            "date_reviewed": None, "reviewer": None, "rejection_code": None, "expiry": None,
            "note": "Guardian Access link created in Pending status at attestation + upload (M01-GRD-001). Cannot view or act on minor's portal until QA Reviewer verifies.",
        },
        "audit": [
            {"date": "Today 9:40 AM", "actor": "Jennifer T. (self-service)", "action": "Attested guardianship + uploaded government ID and guardianship order"},
        ],
    },
    "PT-2026-00699": {
        "name": "Diane H.", "dob": "1965-09-08", "care_products": ["Testosterone Care"],
        "poa": {
            "holder_name": "Michael H.", "phone": "(303) 555-0193", "email": "michael.h@example.com",
            "relationship": "Power of Attorney", "status": "clarify",
            "documents": ["Power of Attorney (5 pages)", "Government-Issued Photo ID"],
            "date_reviewed": None, "reviewer": "Quinn Patel, QA Reviewer", "rejection_code": None, "expiry": None,
            "note": "“General POA language is ambiguous on whether it covers healthcare decisions — needs Compliance/Legal read before I can approve or deny.” Escalated to CX Leadership / Compliance per POA-008. No PHI released; patient sees a neutral “under review” status, not a rejection.",
        },
        "audit": [
            {"date": "Yesterday 4:12 PM", "actor": "Quinn Patel, QA Reviewer", "action": "Escalated to Needs Clarification (POA-008) — routed to CX Leadership / Compliance"},
        ],
    },
    "PT-2026-00571": {
        "name": "Linda P.", "dob": "1958-01-30", "care_products": ["Testosterone Care"],
        "poa": {
            "holder_name": "Carol Peterson", "phone": "(646) 555-0165", "email": "carol.peterson@example.com",
            "relationship": "Power of Attorney", "status": "verified",
            "documents": ["Power of Attorney (2 pages)", "Government-Issued Photo ID"],
            "date_reviewed": "Today 7:58 AM", "reviewer": "Quinn Patel, QA Reviewer",
            "rejection_code": None, "expiry": "Jul 12, 2027",
            "note": "Third-party order. Verified and active.",
        },
        "audit": [
            {"date": "Today 7:58 AM", "actor": "Quinn Patel, QA Reviewer", "action": "Approved — POA verified"},
        ],
    },
    "PT-2026-00388": {
        "name": "James O.", "dob": "1991-05-17", "care_products": ["ED Treatment"],
        "poa": {
            "holder_name": "David Ortiz", "phone": "(602) 555-0139", "email": "david.ortiz@example.com",
            "relationship": "Power of Attorney (financial only)", "status": "revoked",
            "documents": ["Power of Attorney (3 pages)", "Government-Issued Photo ID"],
            "date_reviewed": "Today 8:22 AM", "reviewer": "Quinn Patel, QA Reviewer",
            "rejection_code": "Lacks Healthcare Decision-Making Authority", "expiry": None,
            "note": "Document is financial/fiduciary-only and does not explicitly grant authority over health information/PHI (POA-002, code 2). Patient notified with corrective-action message.",
        },
        "audit": [
            {"date": "Today 8:22 AM", "actor": "Quinn Patel, QA Reviewer", "action": "Rejected — Lacks Healthcare Decision-Making Authority"},
        ],
    },
    "PT-2026-00614": {
        "name": "Maria S.", "dob": "1972-08-25", "care_products": ["Everly Care — Diabetes"],
        "poa": None,
        "audit": [],
    },
}


# ── Admin Dashboard ──────────────────────────────────────────────────────────

@bp.route("/")
def dashboard():
    return render_template("admin/dashboard.html")


# ── Care Products ─────────────────────────────────────────────────────────────

@bp.route("/care-products")
def care_products():
    return render_template("admin/care_products.html")

@bp.route("/care-product/new")
def care_product_new():
    conn = _db()
    clients = conn.execute(
        "SELECT client_id, client_name, client_type FROM clients WHERE status='Active' ORDER BY client_name"
    ).fetchall()
    conn.close()
    return render_template("admin/wizard.html", clients=clients)

@bp.route("/care-product/<int:product_id>")
def care_product_detail(product_id):
    return render_template("admin/care_product_stub.html", product_id=product_id)


# ── Client Management ─────────────────────────────────────────────────────────

@bp.route("/clients")
def clients():
    conn = _db()
    rows = conn.execute(
        "SELECT client_id, client_name, client_type, primary_contact, contact_email, status FROM clients ORDER BY client_name"
    ).fetchall()
    conn.close()
    return render_template("admin/client_management.html", clients=rows)

@bp.route("/clients/new", methods=["GET", "POST"])
def client_new():
    if request.method == "POST":
        conn = _db()
        conn.execute(
            "INSERT INTO clients (client_name, client_type, primary_contact, contact_email, contact_phone, status, date_added) VALUES (?,?,?,?,?,?,?)",
            [
                request.form["client_name"],
                request.form["client_type"],
                request.form.get("primary_contact", ""),
                request.form.get("contact_email", ""),
                request.form.get("contact_phone", ""),
                request.form.get("status", "Active"),
                date.today().isoformat(),
            ]
        )
        conn.commit()
        conn.close()
        return redirect(url_for("admin.clients"))
    return render_template("admin/client_form.html", client=None, action="Add Client")

@bp.route("/clients/<int:client_id>/edit", methods=["GET", "POST"])
def client_edit(client_id):
    conn = _db()
    if request.method == "POST":
        conn.execute(
            "UPDATE clients SET client_name=?, client_type=?, primary_contact=?, contact_email=?, contact_phone=?, status=? WHERE client_id=?",
            [
                request.form["client_name"],
                request.form["client_type"],
                request.form.get("primary_contact", ""),
                request.form.get("contact_email", ""),
                request.form.get("contact_phone", ""),
                request.form.get("status", "Active"),
                client_id,
            ]
        )
        conn.commit()
        conn.close()
        return redirect(url_for("admin.clients"))
    client = conn.execute("SELECT * FROM clients WHERE client_id=?", [client_id]).fetchone()
    conn.close()
    return render_template("admin/client_form.html", client=client, action="Edit Client")


# ── Other Admin Routes ────────────────────────────────────────────────────────

@bp.route("/patients")
def patients():
    return render_template("admin/patients_stub.html")

@bp.route("/patients/<patient_id>")
def patient_detail(patient_id):
    record = PATIENTS.get(patient_id)
    return render_template("admin/patient_detail.html", patient_id=patient_id, record=record)

@bp.route("/providers")
def providers():
    return render_template("admin/credentialing.html")

@bp.route("/reports")
def reports():
    return render_template("admin/reports.html")

@bp.route("/settings")
def settings():
    return render_template("admin/settings_stub.html")

@bp.route("/users")
def users():
    return render_template("admin/users.html")

@bp.route("/role-config")
def role_config():
    return render_template("admin/role_config.html")

@bp.route("/integrations")
def integrations():
    return render_template("admin/integrations.html")

@bp.route("/sla-config")
def sla_config():
    return render_template("admin/sla_config.html")

@bp.route("/notifications")
def notifications():
    return render_template("admin/notifications.html")

@bp.route("/audit-log")
def audit_log():
    return render_template("admin/audit_log.html")

@bp.route("/coordinator")
def coordinator():
    return render_template("admin/coordinator.html")


# ── Members DB / Eligibility Admin ─────────────────────────────────────────

@bp.route("/members-db")
def members_db():
    return render_template("admin/members_db.html")

@bp.route("/doh-config")
def doh_config():
    return render_template("admin/doh_config.html")

# ── Peer Review (M17) ────────────────────────────────────────────────────────

@bp.route("/scripting-config")
def scripting_config():
    return render_template("admin/scripting_config.html")


@bp.route("/peer-review")
def peer_review_config():
    return render_template("admin/peer_review_config.html")

@bp.route("/peer-review/reports")
def peer_review_reports():
    return render_template("admin/peer_review_reports.html")

@bp.route("/document-library")
def document_library():
    return render_template("admin/document_library.html")
