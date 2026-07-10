import os
import sqlite3
from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint("admin", __name__)

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'project_phoenix.db')


def _db():
    return sqlite3.connect(DB_PATH)


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

@bp.route("/peer-review")
def peer_review_config():
    return render_template("admin/peer_review_config.html")

@bp.route("/peer-review/reports")
def peer_review_reports():
    return render_template("admin/peer_review_reports.html")
