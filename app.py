import os
from datetime import timedelta
from flask import Flask, render_template, session, redirect, url_for, request
from modules import provider, patient, admin, care_team, scheduler
import workflow_config

app = Flask(__name__)
app.secret_key = 'project-phoenix-demo-secret-2026'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)

ROLE_NAMES = {
    'provider_md': 'Dr. Sarah Lee, MD',
    'provider_np': 'Jamie Rivera, NP',
    'provider_rn': 'Jordan Patel, RN',
    'provider_ma': 'Alex Kim, MA',
    'provider_gc': 'Taylor Brooks, GC',
    'scheduler':   'Morgan Hayes',
    'care_team':   'Casey Torres',
    'patient':     'Marcus Johnson',
    'admin':       'Chris Navarro',
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
