#!/usr/bin/env python3
"""
Project Phoenix — Demo Update: New Login Users + Dashboards
Adds QA Reviewer and GC Administrator to login screen.
Creates minimal but functional dashboards for both roles.

Files modified:
  templates/index.html
  app.py
  modules/provider.py

Files created:
  templates/provider/qa_reviewer_dashboard.html
  templates/provider/gc_admin_dashboard.html
"""

import os

BASE = '/Users/justin.woller/Documents/project-phoenix-demo'
changes = []

# ─────────────────────────────────────────────────────────────────────────────
# 1. UPDATE app.py — add 2 new roles
# ─────────────────────────────────────────────────────────────────────────────
app_path = os.path.join(BASE, 'app.py')
with open(app_path, 'r') as f:
    app = f.read()

if "'qa_reviewer'" not in app:
    app = app.replace(
        "    'admin':       'Chris Navarro',",
        "    'admin':       'Chris Navarro',\n    'qa_reviewer': 'Rachel Chen, QA Reviewer',\n    'gc_admin':    'Dana Cooper, GC Admin',"
    )
    app = app.replace(
        "    'admin':       'admin.dashboard',",
        "    'admin':       'admin.dashboard',\n    'qa_reviewer': 'provider.qa_reviewer_dashboard',\n    'gc_admin':    'provider.gc_admin_dashboard',"
    )
    with open(app_path, 'w') as f:
        f.write(app)
    changes.append('app.py: added qa_reviewer and gc_admin roles')
else:
    changes.append('app.py: SKIP — roles already present')

# ─────────────────────────────────────────────────────────────────────────────
# 2. UPDATE modules/provider.py — add 2 new routes
# ─────────────────────────────────────────────────────────────────────────────
provider_path = os.path.join(BASE, 'modules', 'provider.py')
with open(provider_path, 'r') as f:
    prov = f.read()

if 'qa_reviewer_dashboard' not in prov:
    prov += '''

@bp.route("/qa-reviewer")
def qa_reviewer_dashboard():
    return render_template("provider/qa_reviewer_dashboard.html")

@bp.route("/gc-admin")
def gc_admin_dashboard():
    return render_template("provider/gc_admin_dashboard.html")
'''
    with open(provider_path, 'w') as f:
        f.write(prov)
    changes.append('modules/provider.py: added qa_reviewer_dashboard and gc_admin_dashboard routes')
else:
    changes.append('modules/provider.py: SKIP — routes already present')

# ─────────────────────────────────────────────────────────────────────────────
# 3. UPDATE templates/index.html — add 2 new user cards (Row 4)
# ─────────────────────────────────────────────────────────────────────────────
index_path = os.path.join(BASE, 'templates', 'index.html')
with open(index_path, 'r') as f:
    idx = f.read()

NEW_ROW = '''
    <!-- Row 4: QA Reviewer, GC Administrator -->
    <div class="user-card">
      <div class="user-avatar" style="background:#B45309">RC</div>
      <div class="user-name">Rachel Chen</div>
      <div class="user-role">QA Reviewer<br>Provider Portal</div>
      <a href="{{ url_for('login', role='qa_reviewer') }}" class="login-btn">Log in as Rachel</a>
    </div>

    <div class="user-card">
      <div class="user-avatar" style="background:#0E7490">DC</div>
      <div class="user-name">Dana Cooper</div>
      <div class="user-role">GC Administrator<br>Provider Portal</div>
      <a href="{{ url_for('login', role='gc_admin') }}" class="login-btn">Log in as Dana</a>
    </div>

'''

if 'Log in as Rachel' not in idx:
    idx = idx.replace('  </div>\n\n  <!-- Change 4', NEW_ROW + '  </div>\n\n  <!-- Change 4')
    with open(index_path, 'w') as f:
        f.write(idx)
    changes.append('templates/index.html: added QA Reviewer and GC Administrator cards')
else:
    changes.append('templates/index.html: SKIP — cards already present')

# ─────────────────────────────────────────────────────────────────────────────
# 4. CREATE templates/provider/qa_reviewer_dashboard.html
# ─────────────────────────────────────────────────────────────────────────────
qa_path = os.path.join(BASE, 'templates', 'provider', 'qa_reviewer_dashboard.html')
if not os.path.exists(qa_path):
    qa_html = '''{% extends "base.html" %}
{% block title %}QA Review Queue — Project Phoenix{% endblock %}
{% block head %}
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #FAF7F2; }
.qr-shell { margin-top: 60px; }
.qr-topbar { background: #B45309; color: #fff; padding: 0 24px; height: 52px; display: flex; align-items: center; gap: 14px; }
.qr-topbar-title { font-size: 16px; font-weight: 700; }
.qr-topbar-sub { font-size: 12px; color: #FDE68A; }
.qr-body { max-width: 1100px; margin: 0 auto; padding: 28px 24px; }
.page-title { font-size: 20px; font-weight: 700; color: #111827; margin-bottom: 4px; }
.page-sub { font-size: 13px; color: #6B7280; margin-bottom: 24px; }
.stat-row { display: flex; gap: 14px; margin-bottom: 24px; flex-wrap: wrap; }
.stat-card { background: #fff; border: 1px solid #E5E0D8; border-radius: 10px; padding: 16px 20px; min-width: 160px; flex: 1; }
.stat-label { font-size: 11px; font-weight: 600; color: #6B7280; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 6px; }
.stat-value { font-size: 28px; font-weight: 700; }
.stat-value.amber { color: #B45309; }
.stat-value.green { color: #059669; }
.stat-value.red { color: #DC2626; }
.queue-card { background: #fff; border: 1px solid #E5E0D8; border-radius: 10px; overflow: hidden; margin-bottom: 20px; }
.queue-header { padding: 14px 20px; border-bottom: 1px solid #E5E0D8; display: flex; align-items: center; gap: 10px; }
.queue-title { font-size: 14px; font-weight: 700; color: #111827; flex: 1; }
.badge { font-size: 11px; font-weight: 700; padding: 2px 10px; border-radius: 20px; }
.badge-amber { background: #FEF3C7; color: #92400E; }
.badge-green { background: #D1FAE5; color: #065F46; }
table { width: 100%; border-collapse: collapse; }
thead th { padding: 9px 16px; text-align: left; font-size: 11px; font-weight: 600; color: #6B7280; text-transform: uppercase; letter-spacing: 0.04em; background: #F9F5EE; border-bottom: 1px solid #E5E0D8; }
tbody td { padding: 13px 16px; font-size: 13px; color: #374151; border-bottom: 1px solid #E5E0D8; vertical-align: middle; }
tbody tr:last-child td { border-bottom: none; }
.p-name { font-weight: 600; color: #111827; }
.p-id { font-size: 11px; color: #9CA3AF; }
.cp-tag { display: inline-block; font-size: 10px; font-weight: 600; padding: 2px 7px; border-radius: 4px; background: #EDE9FE; color: #5B21B6; }
.trigger-badge { font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px; }
.trigger-minor { background: #DBEAFE; color: #1D4ED8; }
.trigger-poa { background: #FEF3C7; color: #92400E; }
.trigger-third { background: #F3E8FF; color: #6B21A8; }
.action-btn { padding: 5px 14px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; border: 1.5px solid; margin-right: 6px; }
.btn-review { border-color: #6B21A8; color: #6B21A8; background: #fff; }
.btn-review:hover { background: #F5F0FB; }
.btn-approve { border-color: #059669; color: #059669; background: #fff; }
.btn-approve:hover { background: #D1FAE5; }
.btn-reject { border-color: #DC2626; color: #DC2626; background: #fff; }
.btn-reject:hover { background: #FEF2F2; }
.qa-note { font-size: 11px; color: #6B7280; font-style: italic; }
.completed-tag { font-size: 11px; font-weight: 600; color: #059669; background: #D1FAE5; padding: 2px 8px; border-radius: 4px; }
</style>
{% endblock %}
{% block content %}
<div class="qr-shell">
  <div class="qr-topbar">
    <div class="qr-topbar-title">QA Review Queue — Rachel Chen</div>
    <div class="qr-topbar-sub">Role: QA Reviewer · Read-only access · Approve / Reject only</div>
  </div>

  <div class="qr-body">
    <div class="page-title">QA Review Queue</div>
    <div class="page-sub">Review submitted documentation for minor, POA, and third-party consults. You may approve or reject — all decisions are audit-logged.</div>

    <div class="stat-row">
      <div class="stat-card"><div class="stat-label">Pending Review</div><div class="stat-value amber">4</div></div>
      <div class="stat-card"><div class="stat-label">Approved Today</div><div class="stat-value green">7</div></div>
      <div class="stat-card"><div class="stat-label">Rejected Today</div><div class="stat-value red">1</div></div>
      <div class="stat-card"><div class="stat-label">SLA Breach Risk</div><div class="stat-value amber">1</div></div>
    </div>

    <!-- Pending Queue -->
    <div class="queue-card">
      <div class="queue-header">
        <div class="queue-title">Pending Review</div>
        <span class="badge badge-amber">4 items</span>
      </div>
      <table>
        <thead><tr><th>Patient</th><th>Consult</th><th>Care Product</th><th>QA Trigger</th><th>Submitted By</th><th>Submitted</th><th>Documents</th><th>Actions</th></tr></thead>
        <tbody>
          <tr>
            <td><div class="p-name">Emily W. (minor)</div><div class="p-id">PT-2026-00602</div></td>
            <td>CST-2026-11221</td>
            <td><span class="cp-tag">BRCA Hereditary</span></td>
            <td><span class="trigger-badge trigger-minor">Minor — Under 18</span></td>
            <td>Taylor Brooks, GC</td>
            <td>Today 8:14 AM</td>
            <td>2 documents uploaded ✓</td>
            <td>
              <button class="action-btn btn-review" onclick="openReview('CST-2026-11221')">Review Docs</button>
              <button class="action-btn btn-approve" onclick="approveQA('CST-2026-11221')">Approve ✓</button>
              <button class="action-btn btn-reject" onclick="rejectQA('CST-2026-11221')">Reject ✗</button>
            </td>
          </tr>
          <tr>
            <td><div class="p-name">Robert C. (POA)</div><div class="p-id">PT-2026-00587</div></td>
            <td>CST-2026-11198</td>
            <td><span class="cp-tag">GLP-1 Weight</span></td>
            <td><span class="trigger-badge trigger-poa">POA — Third-party order</span></td>
            <td>Jordan Patel, RN</td>
            <td>Today 9:02 AM</td>
            <td>1 document uploaded ✓</td>
            <td>
              <button class="action-btn btn-review" onclick="openReview('CST-2026-11198')">Review Docs</button>
              <button class="action-btn btn-approve" onclick="approveQA('CST-2026-11198')">Approve ✓</button>
              <button class="action-btn btn-reject" onclick="rejectQA('CST-2026-11198')">Reject ✗</button>
            </td>
          </tr>
          <tr>
            <td><div class="p-name">Maria S.</div><div class="p-id">PT-2026-00614</div></td>
            <td>CST-2026-11244 <span style="font-size:10px;color:#DC2626;font-weight:700;">⚠ SLA at risk</span></td>
            <td><span class="cp-tag">Hereditary Cancer</span></td>
            <td><span class="trigger-badge trigger-third">Third-party order</span></td>
            <td>Taylor Brooks, GC</td>
            <td>Yesterday 3:45 PM</td>
            <td>3 documents uploaded ✓</td>
            <td>
              <button class="action-btn btn-review" onclick="openReview('CST-2026-11244')">Review Docs</button>
              <button class="action-btn btn-approve" onclick="approveQA('CST-2026-11244')">Approve ✓</button>
              <button class="action-btn btn-reject" onclick="rejectQA('CST-2026-11244')">Reject ✗</button>
            </td>
          </tr>
          <tr>
            <td><div class="p-name">Thomas K. (minor)</div><div class="p-id">PT-2026-00631</div></td>
            <td>CST-2026-11267</td>
            <td><span class="cp-tag">BRCA Hereditary</span></td>
            <td><span class="trigger-badge trigger-minor">Minor — Under 18</span></td>
            <td>Alex Kim, MA</td>
            <td>Today 10:33 AM</td>
            <td>Documents pending upload</td>
            <td>
              <button class="action-btn btn-review" onclick="openReview('CST-2026-11267')" style="opacity:0.4;cursor:not-allowed;" disabled>Review Docs</button>
              <button class="action-btn btn-approve" style="opacity:0.4;cursor:not-allowed;" disabled>Approve ✓</button>
              <button class="action-btn btn-reject" style="opacity:0.4;cursor:not-allowed;" disabled>Reject ✗</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Completed Today -->
    <div class="queue-card">
      <div class="queue-header">
        <div class="queue-title">Completed Today</div>
        <span class="badge badge-green">8 items</span>
      </div>
      <table>
        <thead><tr><th>Patient</th><th>Consult</th><th>Care Product</th><th>QA Trigger</th><th>Decision</th><th>Time</th></tr></thead>
        <tbody>
          <tr>
            <td><div class="p-name">Linda P.</div><div class="p-id">PT-2026-00571</div></td>
            <td>CST-2026-11175</td>
            <td><span class="cp-tag">Testosterone</span></td>
            <td><span class="trigger-badge trigger-third">Third-party order</span></td>
            <td><span class="completed-tag">✓ Approved</span></td>
            <td>7:58 AM</td>
          </tr>
          <tr>
            <td><div class="p-name">James O.</div><div class="p-id">PT-2026-00388</div></td>
            <td>CST-2026-11119</td>
            <td><span class="cp-tag">ED Treatment</span></td>
            <td><span class="trigger-badge trigger-poa">POA — Third-party order</span></td>
            <td><span style="font-size:11px;font-weight:600;color:#DC2626;background:#FEF2F2;padding:2px 8px;border-radius:4px;">✗ Rejected — Missing POA doc</span></td>
            <td>8:22 AM</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div style="background:#FEF3C7;border:1px solid #FDE68A;border-radius:8px;padding:14px 18px;font-size:13px;color:#92400E;">
      <strong>Role reminder:</strong> As QA Reviewer, you may review documents and approve or reject the QA stage. You cannot edit clinical content or consult notes. All decisions are logged to the audit trail.
    </div>
  </div>
</div>
{% endblock %}
{% block scripts %}
{% raw %}
<script>
function openReview(id) {
  alert('Opening document viewer for consult ' + id + '\\n\\nDocuments loaded in read-only view.\\nReview all uploaded files before approving or rejecting.');
}
function approveQA(id) {
  if (confirm('Approve QA stage for consult ' + id + '?\\n\\nThe consult workflow will automatically resume.')) {
    alert('✓ Approved — Consult ' + id + ' resumed. GC notified.');
    location.reload();
  }
}
function rejectQA(id) {
  var reason = prompt('Reject reason for consult ' + id + ':\\n(Required — will be sent to GC Administrator queue)');
  if (reason) {
    alert('✗ Rejected — Consult ' + id + ' routed to GC Administrator queue.\\nReason: ' + reason);
    location.reload();
  }
}
</script>
{% endraw %}
{% endblock %}
'''
    with open(qa_path, 'w') as f:
        f.write(qa_html)
    changes.append('templates/provider/qa_reviewer_dashboard.html: created')
else:
    changes.append('templates/provider/qa_reviewer_dashboard.html: SKIP — already exists')

# ─────────────────────────────────────────────────────────────────────────────
# 5. CREATE templates/provider/gc_admin_dashboard.html
# ─────────────────────────────────────────────────────────────────────────────
gc_admin_path = os.path.join(BASE, 'templates', 'provider', 'gc_admin_dashboard.html')
if not os.path.exists(gc_admin_path):
    gc_html = '''{% extends "base.html" %}
{% block title %}GC Administrator — Project Phoenix{% endblock %}
{% block head %}
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #FAF7F2; }
.ga-shell { margin-top: 60px; }
.ga-topbar { background: #0E7490; color: #fff; padding: 0 24px; height: 52px; display: flex; align-items: center; gap: 14px; }
.ga-topbar-title { font-size: 16px; font-weight: 700; }
.ga-topbar-sub { font-size: 12px; color: #A5F3FC; }
.ga-body { max-width: 1200px; margin: 0 auto; padding: 28px 24px; }
.page-title { font-size: 20px; font-weight: 700; color: #111827; margin-bottom: 4px; }
.page-sub { font-size: 13px; color: #6B7280; margin-bottom: 20px; }
.tab-bar { display: flex; gap: 0; border-bottom: 2px solid #E5E0D8; margin-bottom: 24px; }
.ga-tab { padding: 10px 22px; font-size: 13px; font-weight: 600; color: #6B7280; cursor: pointer; border-bottom: 3px solid transparent; margin-bottom: -2px; }
.ga-tab.active { color: #0E7490; border-bottom-color: #0E7490; }
.ga-tab:hover:not(.active) { color: #374151; }
.panel { display: none; }
.panel.active { display: block; }
.stat-row { display: flex; gap: 14px; margin-bottom: 24px; flex-wrap: wrap; }
.stat-card { background: #fff; border: 1px solid #E5E0D8; border-radius: 10px; padding: 16px 20px; min-width: 150px; flex: 1; }
.stat-label { font-size: 11px; font-weight: 600; color: #6B7280; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 6px; }
.stat-value { font-size: 26px; font-weight: 700; }
.stat-value.teal { color: #0E7490; }
.stat-value.red { color: #DC2626; }
.stat-value.amber { color: #B45309; }
.stat-value.green { color: #059669; }
.queue-card { background: #fff; border: 1px solid #E5E0D8; border-radius: 10px; overflow: hidden; margin-bottom: 20px; }
.queue-header { padding: 14px 20px; border-bottom: 1px solid #E5E0D8; display: flex; align-items: center; gap: 10px; }
.queue-title { font-size: 14px; font-weight: 700; color: #111827; flex: 1; }
.badge { font-size: 11px; font-weight: 700; padding: 2px 10px; border-radius: 20px; }
.badge-red { background: #FEE2E2; color: #B91C1C; }
.badge-amber { background: #FEF3C7; color: #92400E; }
.badge-teal { background: #CFFAFE; color: #164E63; }
.badge-green { background: #D1FAE5; color: #065F46; }
table { width: 100%; border-collapse: collapse; }
thead th { padding: 9px 16px; text-align: left; font-size: 11px; font-weight: 600; color: #6B7280; text-transform: uppercase; letter-spacing: 0.04em; background: #F9F5EE; border-bottom: 1px solid #E5E0D8; }
tbody td { padding: 13px 16px; font-size: 13px; color: #374151; border-bottom: 1px solid #E5E0D8; vertical-align: middle; }
tbody tr:last-child td { border-bottom: none; }
.p-name { font-weight: 600; color: #111827; }
.p-id { font-size: 11px; color: #9CA3AF; }
.cp-tag { display: inline-block; font-size: 10px; font-weight: 600; padding: 2px 7px; border-radius: 4px; background: #EDE9FE; color: #5B21B6; }
.action-btn { padding: 5px 14px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; border: 1.5px solid; margin-right: 6px; }
.btn-resolve { border-color: #0E7490; color: #0E7490; background: #fff; }
.btn-resolve:hover { background: #CFFAFE; }
.btn-approve-cl { border-color: #059669; color: #059669; background: #fff; }
.btn-approve-cl:hover { background: #D1FAE5; }
.sla-pill { font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 4px; }
.sla-ok { background: #D1FAE5; color: #065F46; }
.sla-warn { background: #FEF3C7; color: #92400E; }
.sla-breach { background: #FEE2E2; color: #B91C1C; }
.cl-status { font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 4px; }
.cl-draft { background: #F3F4F6; color: #6B7280; }
.cl-pending { background: #FEF3C7; color: #92400E; }
.cl-published { background: #D1FAE5; color: #065F46; }
.reject-note { font-size: 11px; color: #DC2626; background: #FEF2F2; border: 1px solid #FECACA; border-radius: 6px; padding: 6px 10px; margin-top: 4px; }
</style>
{% endblock %}
{% block content %}
<div class="ga-shell">
  <div class="ga-topbar">
    <div class="ga-title">GC Administrator — Dana Cooper</div>
    <div class="ga-topbar-sub">Supervisory · QA Resolution · Blurb Queue · Content Library</div>
  </div>

  <div class="ga-body">
    <div class="page-title">GC Administrator Dashboard</div>
    <div class="page-sub">Manage QA failures, blurb requests, and clinical content library publishing.</div>

    <div class="stat-row">
      <div class="stat-card"><div class="stat-label">QA Failures Pending</div><div class="stat-value red">2</div></div>
      <div class="stat-card"><div class="stat-label">Blurb Requests</div><div class="stat-value amber">5</div></div>
      <div class="stat-card"><div class="stat-label">Overdue Blurbs (>24h)</div><div class="stat-value red">1</div></div>
      <div class="stat-card"><div class="stat-label">Articles Pending Publish</div><div class="stat-value teal">3</div></div>
      <div class="stat-card"><div class="stat-label">Published Articles</div><div class="stat-value green">47</div></div>
    </div>

    <div class="tab-bar">
      <div class="ga-tab active" onclick="switchTab('qa')">🔴 QA Failure Queue (2)</div>
      <div class="ga-tab" onclick="switchTab('blurb')">📋 Blurb Requests (5)</div>
      <div class="ga-tab" onclick="switchTab('library')">📚 Content Library</div>
    </div>

    <!-- QA Failure Queue Panel -->
    <div class="panel active" id="panelQa">
      <div class="queue-card">
        <div class="queue-header">
          <div class="queue-title">QA Failures — Requires Resolution</div>
          <span class="badge badge-red">2 blocked consults</span>
        </div>
        <table>
          <thead><tr><th>Patient</th><th>Consult</th><th>Care Product</th><th>GC</th><th>Reject Reason</th><th>Blocked Since</th><th>Actions</th></tr></thead>
          <tbody>
            <tr>
              <td><div class="p-name">James O.</div><div class="p-id">PT-2026-00388</div></td>
              <td>CST-2026-11119</td>
              <td><span class="cp-tag">ED Treatment</span></td>
              <td>Taylor Brooks, GC</td>
              <td><div class="reject-note">Missing POA document — patient's legal guardian documentation not uploaded before consult submission.</div></td>
              <td>Today 8:22 AM<br><span style="font-size:11px;color:#DC2626;font-weight:600;">1h 43m blocked</span></td>
              <td>
                <button class="action-btn btn-resolve" onclick="resolveQA('CST-2026-11119')">Resolve &amp; Resume →</button>
              </td>
            </tr>
            <tr>
              <td><div class="p-name">Sarah T. (minor)</div><div class="p-id">PT-2026-00619</div></td>
              <td>CST-2026-11188</td>
              <td><span class="cp-tag">BRCA Hereditary</span></td>
              <td>Jordan Patel, RN</td>
              <td><div class="reject-note">Parent/guardian consent form unsigned — patient is 16 years old, guardian signature required on all documentation.</div></td>
              <td>Yesterday 4:17 PM<br><span style="font-size:11px;color:#DC2626;font-weight:600;">18h 6m blocked</span></td>
              <td>
                <button class="action-btn btn-resolve" onclick="resolveQA('CST-2026-11188')">Resolve &amp; Resume →</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Blurb Request Queue Panel -->
    <div class="panel" id="panelBlurb">
      <div class="queue-card">
        <div class="queue-header">
          <div class="queue-title">Blurb Requests — Clinical Content Queue</div>
          <span class="badge badge-amber">5 open · 1 overdue</span>
        </div>
        <table>
          <thead><tr><th>Request</th><th>Submitted By</th><th>Patient / Topic</th><th>SLA Status</th><th>Notes</th><th>Actions</th></tr></thead>
          <tbody>
            <tr style="background:#FEF2F2;">
              <td><strong>BLB-2026-041</strong></td>
              <td>Taylor Brooks, GC</td>
              <td>CST-2026-11099<br><span class="p-id">BRCA2 variant — unusual presentation</span></td>
              <td><span class="sla-pill sla-breach">⚠ OVERDUE — 26h 14m</span></td>
              <td>Unusual BRCA2 splice variant, unclear clinical significance. Need literature summary for patient letter.</td>
              <td>
                <button class="action-btn btn-resolve" onclick="reviewBlurb('BLB-2026-041')">Review &amp; Publish</button>
              </td>
            </tr>
            <tr>
              <td><strong>BLB-2026-044</strong></td>
              <td>Alex Kim, MA</td>
              <td>CST-2026-11187<br><span class="p-id">Lynch syndrome — MMR variant</span></td>
              <td><span class="sla-pill sla-warn">⏱ 18h 32m remaining</span></td>
              <td>Patient asking about surveillance recommendations for MLH1 variant.</td>
              <td>
                <button class="action-btn btn-resolve" onclick="reviewBlurb('BLB-2026-044')">Review &amp; Publish</button>
              </td>
            </tr>
            <tr>
              <td><strong>BLB-2026-046</strong></td>
              <td>Taylor Brooks, GC</td>
              <td>CST-2026-11204<br><span class="p-id">APOE4 — Alzheimer risk</span></td>
              <td><span class="sla-pill sla-ok">✓ 21h 5m remaining</span></td>
              <td>Need plain-language explanation of APOE4 carrier risk for patient disclosure.</td>
              <td>
                <button class="action-btn btn-resolve" onclick="reviewBlurb('BLB-2026-046')">Review &amp; Publish</button>
              </td>
            </tr>
            <tr>
              <td><strong>BLB-2026-047</strong></td>
              <td>Jordan Patel, RN</td>
              <td>CST-2026-11218<br><span class="p-id">VUS in ATM gene</span></td>
              <td><span class="sla-pill sla-ok">✓ 22h 41m remaining</span></td>
              <td>ATM variant of uncertain significance — patient requesting clarification on cancer risk.</td>
              <td>
                <button class="action-btn btn-resolve" onclick="reviewBlurb('BLB-2026-047')">Review &amp; Publish</button>
              </td>
            </tr>
            <tr>
              <td><strong>BLB-2026-048</strong></td>
              <td>Taylor Brooks, GC</td>
              <td>CST-2026-11229<br><span class="p-id">PALB2 hereditary breast</span></td>
              <td><span class="sla-pill sla-ok">✓ 23h 58m remaining</span></td>
              <td>PALB2 pathogenic variant — patient wants comparison to BRCA2 risk for family planning.</td>
              <td>
                <button class="action-btn btn-resolve" onclick="reviewBlurb('BLB-2026-048')">Review &amp; Publish</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Content Library Panel -->
    <div class="panel" id="panelLibrary">
      <div class="queue-card">
        <div class="queue-header">
          <div class="queue-title">Clinical Content Library</div>
          <span class="badge badge-teal">47 published · 3 pending · 8 drafts</span>
        </div>
        <table>
          <thead><tr><th>Article Title</th><th>Gene / Topic</th><th>Inheritance</th><th>Research Flag</th><th>Author</th><th>Status</th><th>Actions</th></tr></thead>
          <tbody>
            <tr>
              <td><strong>BRCA2 Splice Variant — Patient Summary</strong></td>
              <td>BRCA2</td>
              <td>Autosomal dominant</td>
              <td>—</td>
              <td>Taylor Brooks, GC</td>
              <td><span class="cl-status cl-pending">Pending Publish</span></td>
              <td>
                <button class="action-btn btn-approve-cl" onclick="publishArticle('BRCA2 Splice Variant')">Publish ✓</button>
              </td>
            </tr>
            <tr>
              <td><strong>Lynch Syndrome — Surveillance Guide</strong></td>
              <td>MLH1, MSH2, MSH6</td>
              <td>Autosomal dominant</td>
              <td>✓ Eligible for NIH ACMG81</td>
              <td>Taylor Brooks, GC</td>
              <td><span class="cl-status cl-pending">Pending Publish</span></td>
              <td>
                <button class="action-btn btn-approve-cl" onclick="publishArticle('Lynch Syndrome')">Publish ✓</button>
              </td>
            </tr>
            <tr>
              <td><strong>PALB2 — Hereditary Breast Cancer Risk</strong></td>
              <td>PALB2</td>
              <td>Autosomal dominant</td>
              <td>—</td>
              <td>Alex Kim, MA</td>
              <td><span class="cl-status cl-pending">Pending Publish</span></td>
              <td>
                <button class="action-btn btn-approve-cl" onclick="publishArticle('PALB2')">Publish ✓</button>
              </td>
            </tr>
            <tr>
              <td><strong>BRCA1 — Patient Education Overview</strong></td>
              <td>BRCA1</td>
              <td>Autosomal dominant</td>
              <td>✓ Eligible for NIH ACMG81</td>
              <td>Taylor Brooks, GC</td>
              <td><span class="cl-status cl-published">Published</span></td>
              <td><button class="action-btn" style="border-color:#E5E0D8;color:#6B7280;" onclick="alert('View article')">View</button></td>
            </tr>
            <tr>
              <td><strong>APOE4 — Alzheimer Risk Disclosure</strong></td>
              <td>APOE</td>
              <td>Complex / Multi-factorial</td>
              <td>—</td>
              <td>Jordan Patel, RN</td>
              <td><span class="cl-status cl-published">Published</span></td>
              <td><button class="action-btn" style="border-color:#E5E0D8;color:#6B7280;" onclick="alert('View article')">View</button></td>
            </tr>
            <tr>
              <td><strong>ATM — VUS Patient Communication</strong></td>
              <td>ATM</td>
              <td>Autosomal dominant</td>
              <td>—</td>
              <td>Taylor Brooks, GC</td>
              <td><span class="cl-status cl-draft">Draft</span></td>
              <td><button class="action-btn" style="border-color:#E5E0D8;color:#6B7280;">Edit Draft</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
{% endblock %}
{% block scripts %}
{% raw %}
<script>
function switchTab(tab) {
  document.querySelectorAll('.ga-tab').forEach((t, i) => t.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  const tabs = ['qa','blurb','library'];
  const idx = tabs.indexOf(tab);
  document.querySelectorAll('.ga-tab')[idx].classList.add('active');
  document.getElementById('panel' + tab.charAt(0).toUpperCase() + tab.slice(1)).classList.add('active');
}
function resolveQA(id) {
  var action = prompt('Resolve QA failure for consult ' + id + ':\\n1. Override — approve despite rejection\\n2. Return to GC — request corrected docs\\n\\nEnter 1 or 2:');
  if (action === '1') alert('Override applied — consult ' + id + ' resumed. QA Reviewer and GC notified. Audit logged.');
  else if (action === '2') alert('Returned to GC — request for corrected documentation sent. Consult remains paused.');
}
function reviewBlurb(id) {
  alert('Opening blurb request ' + id + '\\n\\nReview GC notes, draft content, and attached case context.\\nPublish to add to patient-facing letter queue.');
}
function publishArticle(title) {
  if (confirm('Publish article: "' + title + '"?\\n\\nThis will make the article available to GCs when composing patient letters.')) {
    alert('✓ Published — "' + title + '" is now live in the Clinical Content Library.');
  }
}
</script>
{% endraw %}
{% endblock %}
'''
    with open(gc_admin_path, 'w') as f:
        f.write(gc_html)
    changes.append('templates/provider/gc_admin_dashboard.html: created')
else:
    changes.append('templates/provider/gc_admin_dashboard.html: SKIP — already exists')

# ─────────────────────────────────────────────────────────────────────────────
print('\n── apply_login_new_users_v1.py ──')
for c in changes:
    print('  ' + c)
print(f'\n  {len(changes)} operations complete.')
print('\nRun qa_check.py to verify all new routes return 200.\n')
