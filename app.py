import os
import csv
import logging
from datetime import datetime, timedelta, timezone
from flask import Flask, render_template, session, redirect, url_for, request
from modules import provider, patient, admin, care_team, scheduler
import workflow_config

app = Flask(__name__)
app.secret_key = 'project-phoenix-demo-secret-2026'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)

# ── Demo Environment Gate ──────────────────────────────────────────────────
# Only active when DEMO_GATE=true is set (Render only — never local dev).
# Visitors must enter name + @everlywell.com email before accessing anything.
DEMO_GATE = os.environ.get('DEMO_GATE', '').lower() == 'true'
GATE_BYPASS_ROUTES = {'gate_login', 'gate_login_post', 'static'}

# In-memory access log (persists for the lifetime of this server process)
_gate_access_log = []
_GATE_LOG_FILE   = os.path.join(os.path.dirname(__file__), 'gate_access_log.csv')

def _record_gate_access(name, email, ip):
    """Write one access entry to the in-memory log, CSV file, and server stdout."""
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    entry = {'timestamp': ts, 'name': name, 'email': email, 'ip': ip}
    _gate_access_log.append(entry)
    # Append to CSV (survives server restarts on persistent-disk Render plans)
    write_header = not os.path.exists(_GATE_LOG_FILE)
    with open(_GATE_LOG_FILE, 'a', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['timestamp', 'name', 'email', 'ip'])
        if write_header:
            w.writeheader()
        w.writerow(entry)
    # Also emit to stdout so Render's log dashboard captures it
    logging.info('DEMO_ACCESS | %s | %s | %s | %s', ts, name, email, ip)

@app.before_request
def enforce_demo_gate():
    if not DEMO_GATE:
        return
    if request.endpoint in GATE_BYPASS_ROUTES:
        return
    if session.get('gate_verified'):
        return
    return redirect(url_for('gate_login', next=request.url))

@app.route('/demo-access', methods=['GET'])
def gate_login():
    error = request.args.get('error', '')
    return render_template('gate_login.html', error=error, next=request.args.get('next', ''))

@app.route('/demo-access', methods=['POST'])
def gate_login_post():
    name     = request.form.get('name', '').strip()
    email    = request.form.get('email', '').strip().lower()
    next_url = request.form.get('next', '').strip()
    error = ''
    if not name:
        error = 'Please enter your name.'
    elif not email.endswith('@everlywell.com'):
        error = 'Please use your @everlywell.com email address.'
    if error:
        return render_template('gate_login.html', error=error, name=name, email=email, next=next_url)
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr or 'unknown').split(',')[0].strip()
    _record_gate_access(name, email, ip)
    session.permanent = True
    session['gate_verified']  = True
    session['gate_name']      = name
    session['gate_email']     = email
    session['gate_timestamp'] = ts
    return redirect(next_url or url_for('index'))

@app.route('/demo-access/log')
def gate_access_log():
    """Simple access log viewer — readable from in-memory + CSV fallback."""
    rows = list(_gate_access_log)
    # Also pull from CSV in case the process restarted
    if os.path.exists(_GATE_LOG_FILE):
        seen = {(r['timestamp'], r['email']) for r in rows}
        with open(_GATE_LOG_FILE, newline='') as f:
            for row in csv.DictReader(f):
                if (row['timestamp'], row['email']) not in seen:
                    rows.append(row)
                    seen.add((row['timestamp'], row['email']))
    rows.sort(key=lambda r: r['timestamp'], reverse=True)
    return render_template('gate_access_log.html', entries=rows)
# ──────────────────────────────────────────────────────────────────────────

ROLE_NAMES = {
    'provider_md': 'Dr. Sarah Lee, MD',
    'provider_np': 'Jamie Rivera, NP',
    'provider_rn': 'Jordan Patel, RN',
    'provider_ma': 'Alex Kim, MA',
    'provider_gc': 'Taylor Brooks, GC',
    'scheduler':   'David Nguyen',
    'care_team':   'Casey Torres',
    'patient':     'Marcus Johnson',
    'admin':       'Chris Navarro',
    'qa_reviewer': 'Rachel Chen, QA Reviewer',
    'gc_admin':    'Dana Cooper, GC Admin',
}

ROLE_DESTINATIONS = {
    'provider_md': 'provider.dashboard',
    'provider_np': 'provider.np_dashboard',
    'provider_rn': 'provider.rn_dashboard',
    'provider_ma': 'provider.ma_dashboard',
    'provider_gc': 'provider.gc_dashboard',
    'scheduler':   'scheduler.dashboard',
    'care_team':   'care_team.dashboard',
    'admin':       'admin.dashboard',
    'qa_reviewer': 'provider.qa_reviewer_dashboard',
    'gc_admin':    'provider.gc_admin_dashboard',
    'patient':     'patient.dashboard',
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login/<role>")
def login(role):
    if role not in ROLE_DESTINATIONS:
        return redirect(url_for('index'))
    session.permanent = True
    session['role'] = role
    session['display_name'] = ROLE_NAMES.get(role, role)
    return redirect(url_for(ROLE_DESTINATIONS[role]))

@app.route("/login", methods=["POST"])
def login_post():
    role = request.form.get("role", "")
    if role not in ROLE_DESTINATIONS:
        return redirect(url_for('index'))
    session.permanent = True
    session['role'] = role
    session['display_name'] = ROLE_NAMES.get(role, role)
    return redirect(url_for(ROLE_DESTINATIONS[role]))

@app.route("/switch-user", methods=["POST"])
def switch_user():
    role = request.form.get("role", "")
    if role in ROLE_DESTINATIONS:
        session.permanent = True
        session['role'] = role
        session['display_name'] = ROLE_NAMES.get(role, role)
        next_url = request.form.get('next') or request.referrer or url_for(ROLE_DESTINATIONS[role])
        return redirect(next_url)
    return redirect(request.referrer or url_for('index'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

# Change 1 — PWN Health isolated patient portal
@app.route('/pwn/login')
def pwn_login():
    return render_template('patient/login_pwn.html')

@app.route('/pwn/portal')
def pwn_portal():
    return render_template('patient/portal_pwn.html')

# Change 2 — Everlywell multi-program patient portal
@app.route('/patient/login')
def patient_login_page():
    return render_template('patient/login.html')

@app.route('/patient/portal')
def patient_portal_page():
    return render_template('patient/portal.html')

# M02 — Provider Portal (includes async consultation workflow)
app.register_blueprint(provider.bp, url_prefix="/provider")

# M03 — Patient Portal
app.register_blueprint(patient.bp, url_prefix="/patient")

# M04 — Admin Portal
app.register_blueprint(admin.bp, url_prefix="/admin")

# Care Team Portal
app.register_blueprint(care_team.bp, url_prefix="/care-team")

# Scheduler
app.register_blueprint(scheduler.bp, url_prefix="/scheduler")

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
