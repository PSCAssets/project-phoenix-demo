import os
import time
import sqlite3
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
# Enabled on Render (DEMO_GATE=true) OR whenever not running locally.
# Falls back to checking FLASK_ENV / PORT so local `python app.py` is unaffected.
_IS_LOCAL = os.environ.get('FLASK_ENV') == 'development' or (
    not os.environ.get('RENDER') and os.environ.get('PORT', '5000') == '5000'
    and not os.environ.get('DEMO_GATE')
)
DEMO_GATE = not _IS_LOCAL
GATE_TIMEOUT_SECONDS = 15 * 60   # 15 minutes of inactivity
GATE_BYPASS_ROUTES   = {'gate_login', 'gate_login_post', 'static'}

_DB_PATH = os.path.join(os.path.dirname(__file__), 'project_phoenix.db')

def _gate_db():
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('''
        CREATE TABLE IF NOT EXISTS demo_access_log (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp  TEXT    NOT NULL,
            name       TEXT    NOT NULL,
            email      TEXT    NOT NULL,
            ip         TEXT,
            login_num  INTEGER NOT NULL DEFAULT 1
        )
    ''')
    conn.commit()
    return conn

def _record_gate_access(name, email, ip):
    """Persist one login to the DB, increment that user's total count."""
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    conn = _gate_db()
    row  = conn.execute(
        'SELECT COUNT(*) AS cnt FROM demo_access_log WHERE email = ?', (email,)
    ).fetchone()
    login_num = (row['cnt'] or 0) + 1
    conn.execute(
        'INSERT INTO demo_access_log (timestamp, name, email, ip, login_num) VALUES (?,?,?,?,?)',
        (ts, name, email, ip, login_num)
    )
    conn.commit()
    conn.close()
    logging.info('DEMO_ACCESS | %s | %s | %s | login #%d | ip:%s', ts, name, email, login_num, ip)
    return ts, login_num

@app.before_request
def enforce_demo_gate():
    if not DEMO_GATE:
        return
    if request.endpoint in GATE_BYPASS_ROUTES:
        return
    # Check inactivity timeout — expire gate_verified after 15 min of no activity
    if session.get('gate_verified'):
        last = session.get('gate_last_activity', 0)
        if time.time() - last > GATE_TIMEOUT_SECONDS:
            # Session timed out — clear gate flags but keep name/email for pre-fill
            _prev_name  = session.get('gate_name', '')
            _prev_email = session.get('gate_email', '')
            session.clear()
            session['gate_prefill_name']  = _prev_name
            session['gate_prefill_email'] = _prev_email
            return redirect(url_for('gate_login', next=request.url, timeout='1'))
        # Refresh activity timestamp on every request
        session['gate_last_activity'] = time.time()
        return
    return redirect(url_for('gate_login', next=request.url))

@app.route('/demo-access', methods=['GET'])
def gate_login():
    timeout = request.args.get('timeout', '')
    # Pre-fill from previous session if they timed out
    prefill_name  = session.pop('gate_prefill_name',  '')
    prefill_email = session.pop('gate_prefill_email', '')
    return render_template('gate_login.html',
        error   = 'Your session expired after 15 minutes of inactivity. Please sign in again.' if timeout else '',
        timeout = bool(timeout),
        name    = prefill_name,
        email   = prefill_email,
        next    = request.args.get('next', ''))

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
    ip = request.headers.get('X-Forwarded-For', request.remote_addr or 'unknown').split(',')[0].strip()
    ts, login_num = _record_gate_access(name, email, ip)
    session.permanent = True
    session['gate_verified']      = True
    session['gate_name']          = name
    session['gate_email']         = email
    session['gate_timestamp']     = ts
    session['gate_login_num']     = login_num
    session['gate_last_activity'] = time.time()
    return redirect(next_url or url_for('index'))

@app.route('/demo-access/log')
def gate_access_log():
    """Access log viewer — reads from DB, shows all logins newest first."""
    conn = _gate_db()
    rows = conn.execute(
        'SELECT timestamp, name, email, ip, login_num FROM demo_access_log ORDER BY id DESC'
    ).fetchall()
    conn.close()
    return render_template('gate_access_log.html', entries=[dict(r) for r in rows])
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
