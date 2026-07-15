#!/usr/bin/env python3
"""
apply_qa_fixes_v2.py — QA patch batch 2
Covers: role-persistent nav, notification links, Edit Availability removal,
        day-view card click, avatar initials, RN notifications.

Run from project root:
  python3 apply_qa_fixes_v2.py
Then: python3 /Users/justin.woller/Documents/project-phoenix-demo/qa_check.py
"""
import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))

def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def patch(path, old, new, label="", allow_zero=False):
    full = os.path.join(BASE, path)
    content = read(full)
    count = content.count(old)
    if count == 0 and not allow_zero:
        print(f"  ✗ MISS [{label or path}] — string not found")
        sys.exit(1)
    if count > 1:
        print(f"  ✗ AMBIGUOUS [{label or path}] — found {count} matches (expected 1)")
        sys.exit(1)
    write(full, content.replace(old, new))
    print(f"  ✓ {label or path}")

def patch_all(path, old, new, label="", min_count=1):
    """Replace ALL occurrences; fail if fewer than min_count found."""
    full = os.path.join(BASE, path)
    content = read(full)
    count = content.count(old)
    if count < min_count:
        print(f"  ✗ MISS [{label or path}] — found {count} (need ≥{min_count})")
        sys.exit(1)
    write(full, content.replace(old, new))
    print(f"  ✓ {label or path} ({count} replacements)")


# ─────────────────────────────────────────────────────────────
# 1. provider.py — add /provider/home route (role-based redirect)
# ─────────────────────────────────────────────────────────────
print("\n[1] provider.py — add /provider/home route")

HOME_ROUTE = '''
@bp.route("/home")
def provider_home():
    """Role-aware dashboard redirect — fixes nav persistence across all provider pages."""
    from flask import redirect
    role = session.get('role', 'provider_md')
    dest_map = {
        'provider_np': '/provider/np',
        'provider_rn': '/provider/rn',
        'provider_gc': '/provider/gc',
        'provider_ma': '/provider/ma',
    }
    return redirect(dest_map.get(role, '/provider/'))

'''

patch(
    'modules/provider.py',
    '@bp.route("/")\ndef dashboard():',
    HOME_ROUTE + '@bp.route("/")\ndef dashboard():',
    "add /provider/home route"
)

# ─────────────────────────────────────────────────────────────
# 2. All 11 provider templates — fix Dashboard nav link
#    window.location.href='/provider/' → /provider/home
# ─────────────────────────────────────────────────────────────
print("\n[2] Provider templates — fix Dashboard nav (11 files)")

NAV_TEMPLATES = [
    'templates/provider/billing.html',
    'templates/provider/schedule.html',
    'templates/provider/notifications.html',
    'templates/provider/queue.html',
    'templates/provider/chart.html',
    'templates/provider/messages.html',
    'templates/provider/oversight.html',
    'templates/provider/pharmacy.html',
    'templates/provider/settings.html',
    'templates/provider/alerts.html',
    'templates/provider/new_patient.html',
]

for tpl in NAV_TEMPLATES:
    patch(
        tpl,
        "window.location.href='/provider/'",
        "window.location.href='/provider/home'",
        os.path.basename(tpl)
    )

# ─────────────────────────────────────────────────────────────
# 3. notifications.html — fix hardcoded "SL" avatar
# ─────────────────────────────────────────────────────────────
print("\n[3] notifications.html — dynamic avatar initials")

NOTIF = 'templates/provider/notifications.html'

patch(
    NOTIF,
    '<div class="provider-avatar">SL</div>',
    '<div class="provider-avatar" id="provAvatarInit">SL</div>',
    "add id to avatar div"
)

# Inject avatar-init script just before {% raw %} in the scripts block
patch(
    NOTIF,
    '{% block scripts %}\n{% raw %}',
    '''{% block scripts %}
<script>
(function(){
  var dn = "{{ session.get('display_name', 'Sarah Lee') }}";
  var parts = dn.split(',')[0].split(' ').filter(function(w){ return w.length > 2; });
  if (!parts.length) parts = dn.split(',')[0].split(' ');
  var init = (parts[0]||'S')[0] + (parts.length > 1 ? (parts[parts.length-1]||'L')[0] : '');
  var el = document.getElementById('provAvatarInit');
  if (el) el.textContent = init.toUpperCase();
})();
</script>
{% raw %}''',
    "avatar init script"
)

# ─────────────────────────────────────────────────────────────
# 4. notifications.html — remove onclick="return false;" from all action links
# ─────────────────────────────────────────────────────────────
print("\n[4] notifications.html — remove onclick='return false;' from action links")

patch_all(
    NOTIF,
    ' onclick="return false;"',
    '',
    "remove dead onclick handlers",
    min_count=8
)

# ─────────────────────────────────────────────────────────────
# 5. notifications.html — fix specific action link destinations
# ─────────────────────────────────────────────────────────────
print("\n[5] notifications.html — fix action link hrefs")

# "View Consult →" should open chart in async/consult view
patch(
    NOTIF,
    'href="/provider/queue">View Consult &#8594;',
    'href="/provider/chart/1?type=async">View Consult &#8594;',
    "View Consult → chart async"
)

# "View Labs →" should open chart in lab view
patch(
    NOTIF,
    'href="/provider/chart/1">View Labs &#8594;',
    'href="/provider/chart/1?type=lab">View Labs &#8594;',
    "View Labs → chart lab view"
)

# "Review →" (refill request) should open chart for clinical review
patch(
    NOTIF,
    'href="/provider/queue">Review &#8594;',
    'href="/provider/chart/1?type=async">Review &#8594;',
    "Review → chart async"
)

# ─────────────────────────────────────────────────────────────
# 6. notifications.html — role-aware notification header
#    Show role-appropriate content for RN vs MD
# ─────────────────────────────────────────────────────────────
print("\n[6] notifications.html — add RN-specific notifications section")

RN_NOTIFS = '''  <!-- Unread notifications -->
  {% if session.get('role') == 'provider_rn' %}
  <!-- RN-specific notifications -->
  <div class="notif-row unread" data-type="sla">
    <div class="notif-dot dot-unread"></div>
    <div class="notif-body">
      <div class="notif-title">Vital Signs Review — Marcus Johnson <span class="notif-type-tag nt-sla">SLA Alert</span></div>
      <div class="notif-msg">Pre-visit vitals for Marcus Johnson have been recorded. MD review of BP 142/88 flagged for attention before consult.</div>
      <div class="notif-footer">
        <span class="notif-time">10 min ago</span>
        <a class="notif-action" href="/provider/chart/1?type=async">Open Chart &#8594;</a>
      </div>
    </div>
  </div>
  <div class="notif-row unread" data-type="labs">
    <div class="notif-dot dot-unread"></div>
    <div class="notif-body">
      <div class="notif-title">Lab Collection Task — Thomas Chen <span class="notif-type-tag nt-lab">Lab</span></div>
      <div class="notif-msg">Dr. Lee ordered a metabolic panel for Thomas Chen. Specimen collection required before 12:00 PM. Patient checked in at front desk.</div>
      <div class="notif-footer">
        <span class="notif-time">45 min ago</span>
        <a class="notif-action" href="/provider/chart/1?type=lab">View Order &#8594;</a>
      </div>
    </div>
  </div>
  <div class="notif-row unread" data-type="messages">
    <div class="notif-dot dot-unread"></div>
    <div class="notif-body">
      <div class="notif-title">Care Coordination — Rosa Lopez <span class="notif-type-tag nt-msg">Message</span></div>
      <div class="notif-msg">Dr. Lee requests follow-up coordination for Rosa Lopez post-consult. Ensure medication instructions have been communicated to patient.</div>
      <div class="notif-footer">
        <span class="notif-time">2h ago</span>
        <a class="notif-action" href="/provider/messages">View Task &#8594;</a>
      </div>
    </div>
  </div>
  <div class="notif-row unread" data-type="refills">
    <div class="notif-dot dot-unread"></div>
    <div class="notif-body">
      <div class="notif-title">Patient Education — David Kim <span class="notif-type-tag nt-refill">Task</span></div>
      <div class="notif-msg">Semaglutide injection technique education session scheduled for David Kim. Review materials and confirm patient readiness for self-administration.</div>
      <div class="notif-footer">
        <span class="notif-time">3h ago</span>
        <a class="notif-action" href="/provider/queue">View Schedule &#8594;</a>
      </div>
    </div>
  </div>
  {% else %}
  <!-- MD/NP/default notifications -->
'''

patch(
    NOTIF,
    '  <!-- Unread notifications -->',
    RN_NOTIFS,
    "add RN notification block"
)

# Close the {% else %} block before the read notifications section
patch(
    NOTIF,
    '  <!-- Read notifications -->',
    '  {% endif %}\n  <!-- Read notifications -->',
    "close RN conditional block"
)

# ─────────────────────────────────────────────────────────────
# 7. schedule.html — remove "Edit Availability" button
# ─────────────────────────────────────────────────────────────
print("\n[7] schedule.html — remove Edit Availability button")

SCHED = 'templates/provider/schedule.html'

patch(
    SCHED,
    '    <button onclick="editAvailability()" style="background:#fff;border:1.5px solid #E5E0D8;border-radius:7px;padding:7px 14px;font-size:12px;font-weight:600;cursor:pointer;color:#374151;">Edit Availability</button>\n',
    '',
    "remove Edit Availability button"
)

# ─────────────────────────────────────────────────────────────
# 8. schedule.html — extend apptDetailModal with inline edit mode
# ─────────────────────────────────────────────────────────────
print("\n[8] schedule.html — add edit capability to appointment modal")

# Replace the modal footer to add an Edit button
patch(
    SCHED,
    '''    <div class="appt-detail-ft">
      <a href="#" onclick="closeApptDetail();return false;" style="font-size:12px;color:#9CA3AF;text-decoration:none;">Close</a>
      <a id="apptDetailChartLink" href="/provider/chart/1" class="btn-open-chart">Open Chart →</a>
    </div>''',
    '''    <div class="appt-detail-ft" id="apptDetailFt">
      <a href="#" onclick="closeApptDetail();return false;" style="font-size:12px;color:#9CA3AF;text-decoration:none;">Close</a>
      <button onclick="enterApptEditMode()" id="apptEditBtn" style="background:#6B21A8;color:#fff;border:none;border-radius:7px;padding:7px 14px;font-size:12px;font-weight:600;cursor:pointer;">✎ Edit</button>
      <a id="apptDetailChartLink" href="/provider/chart/1" class="btn-open-chart">Open Chart →</a>
    </div>
    <!-- Edit mode form (hidden by default) -->
    <div id="apptEditForm" style="display:none;padding:0 16px 14px;">
      <div style="font-size:11px;font-weight:700;color:#6B21A8;text-transform:uppercase;letter-spacing:.05em;margin-bottom:10px;">Edit Appointment</div>
      <div style="display:grid;gap:8px;">
        <div><label style="font-size:11px;color:#6B7280;display:block;margin-bottom:3px;">Patient</label><input id="editPatientName" style="width:100%;padding:6px 9px;border:1.5px solid #E5E0D8;border-radius:6px;font-size:13px;box-sizing:border-box;" /></div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
          <div><label style="font-size:11px;color:#6B7280;display:block;margin-bottom:3px;">Start Time</label><input id="editStartTime" type="time" style="width:100%;padding:6px 9px;border:1.5px solid #E5E0D8;border-radius:6px;font-size:13px;box-sizing:border-box;" /></div>
          <div><label style="font-size:11px;color:#6B7280;display:block;margin-bottom:3px;">Duration (min)</label><input id="editDuration" type="number" min="15" max="120" step="15" style="width:100%;padding:6px 9px;border:1.5px solid #E5E0D8;border-radius:6px;font-size:13px;box-sizing:border-box;" /></div>
        </div>
        <div><label style="font-size:11px;color:#6B7280;display:block;margin-bottom:3px;">Notes</label><textarea id="editNotes" rows="3" style="width:100%;padding:6px 9px;border:1.5px solid #E5E0D8;border-radius:6px;font-size:12px;resize:vertical;box-sizing:border-box;"></textarea></div>
      </div>
      <div style="display:flex;justify-content:flex-end;gap:8px;margin-top:12px;">
        <button onclick="cancelApptEdit()" style="background:#F3F4F6;border:none;border-radius:7px;padding:7px 14px;font-size:12px;font-weight:600;cursor:pointer;color:#374151;">Cancel</button>
        <button onclick="saveApptEdit()" style="background:#6B21A8;color:#fff;border:none;border-radius:7px;padding:7px 16px;font-size:12px;font-weight:600;cursor:pointer;">Save Changes</button>
      </div>
    </div>''',
    "extend modal with edit form"
)

# Add edit mode JS functions after closeApptDetail function
patch(
    SCHED,
    'function closeApptDetail() {\n  document.getElementById(\'apptDetailModal\').classList.remove(\'open\');\n}',
    '''function closeApptDetail() {
  document.getElementById('apptDetailModal').classList.remove('open');
  cancelApptEdit(); // reset edit mode on close
}
function enterApptEditMode() {
  var body = document.getElementById('apptDetailModal').querySelector('.appt-detail-body');
  var editForm = document.getElementById('apptEditForm');
  var editBtn = document.getElementById('apptEditBtn');
  if (body) body.style.display = 'none';
  if (editForm) editForm.style.display = 'block';
  if (editBtn) editBtn.style.display = 'none';
  // Pre-fill edit fields from display values
  var patient = document.getElementById('apptDetailPatient');
  var dur = document.getElementById('apptDetailDuration');
  var notes = document.getElementById('apptDetailNotes');
  if (patient) document.getElementById('editPatientName').value = patient.textContent;
  if (dur) {
    var durText = dur.textContent; // e.g. "45 min · 8:00 AM"
    var durMatch = durText.match(/^(\\d+)/);
    if (durMatch) document.getElementById('editDuration').value = durMatch[1];
    var timeMatch = durText.match(/(\\d+:\\d+\\s*[AP]M)/);
    if (timeMatch) {
      // convert to HH:MM for time input
      var t = timeMatch[1].trim();
      var ampm = t.slice(-2);
      var parts = t.replace(/[AP]M/,'').trim().split(':');
      var h = parseInt(parts[0]);
      var m = parseInt(parts[1]);
      if (ampm === 'PM' && h !== 12) h += 12;
      if (ampm === 'AM' && h === 12) h = 0;
      document.getElementById('editStartTime').value = (h<10?'0'+h:h)+':'+(m<10?'0'+m:m);
    }
  }
  if (notes) document.getElementById('editNotes').value = notes.textContent.replace(/^"|"$/g,'');
}
function cancelApptEdit() {
  var body = document.getElementById('apptDetailModal').querySelector('.appt-detail-body');
  var editForm = document.getElementById('apptEditForm');
  var editBtn = document.getElementById('apptEditBtn');
  if (body) body.style.display = '';
  if (editForm) editForm.style.display = 'none';
  if (editBtn) editBtn.style.display = '';
}
function saveApptEdit() {
  // In demo: update the display values and show a confirmation toast
  var patient = document.getElementById('editPatientName').value;
  var dur = document.getElementById('editDuration').value;
  var notes = document.getElementById('editNotes').value;
  var patEl = document.getElementById('apptDetailPatient');
  var durEl = document.getElementById('apptDetailDuration');
  var notesEl = document.getElementById('apptDetailNotes');
  if (patEl) patEl.textContent = patient;
  if (durEl) {
    var t = document.getElementById('editStartTime').value;
    var timeDisplay = '';
    if (t) {
      var parts = t.split(':');
      var h = parseInt(parts[0]), m = parseInt(parts[1]);
      var ampm = h >= 12 ? 'PM' : 'AM';
      var h12 = h > 12 ? h - 12 : (h === 0 ? 12 : h);
      timeDisplay = ' · ' + h12 + (m ? ':' + (m<10?'0'+m:m) : ':00') + ' ' + ampm;
    }
    durEl.textContent = dur + ' min' + timeDisplay;
  }
  if (notesEl) notesEl.textContent = '"' + notes + '"';
  cancelApptEdit();
  closeApptDetail();
  // Show save toast
  var toast = document.getElementById('editToast');
  if (toast) {
    toast.textContent = '✓ Appointment updated';
    toast.style.display = 'block';
    setTimeout(function(){ toast.style.display = 'none'; toast.textContent = 'Availability editing mode — click any slot to modify'; }, 2500);
  }
}''',
    "add edit mode JS functions"
)

# ─────────────────────────────────────────────────────────────
# 9. schedule.html — make day-view appointment cards clickable
# ─────────────────────────────────────────────────────────────
print("\n[9] schedule.html — day-view card click handlers")

# Add cursor:pointer and onclick to each named appointment card in day view
# Annual Visit — Aisha N.
patch(
    SCHED,
    '<div class="day-appt-card annual"><div class="day-appt-name">Annual Visit — Aisha N.</div><div class="day-appt-meta">Women\'s Health · 45 min · No SLA</div></div>',
    '<div class="day-appt-card annual" style="cursor:pointer;" onclick="openApptDetail(\'Annual Visit\',\'Aisha N. · Women\\\'s Health\',\'annual\',45,8,0,2)"><div class="day-appt-name">Annual Visit — Aisha N.</div><div class="day-appt-meta">Women\'s Health · 45 min · No SLA</div></div>',
    "day-view Aisha N. card onclick"
)

# Phone Consult — James R.
patch(
    SCHED,
    '<div class="day-appt-card phone"><div class="day-appt-name">Phone Consult — James R.</div><div class="day-appt-meta">STI Panel · 15 min · SLA: OK</div></div>',
    '<div class="day-appt-card phone" style="cursor:pointer;" onclick="openApptDetail(\'Phone Consult\',\'James R. · STI Panel\',\'phone\',15,9,0,2)"><div class="day-appt-name">Phone Consult — James R.</div><div class="day-appt-meta">STI Panel · 15 min · SLA: OK</div></div>',
    "day-view James R. card onclick"
)

# A1C Treat Consult — Sandra G.
patch(
    SCHED,
    '<div class="day-appt-card async" style="background:#0D9488;"><div class="day-appt-name">A1C Treat Consult — Sandra G.</div><div class="day-appt-meta">A1C Mgmt · 15 min</div></div>',
    '<div class="day-appt-card async" style="background:#0D9488;cursor:pointer;" onclick="openApptDetail(\'A1C Treat Consult\',\'Sandra G. · A1C Mgmt\',\'a1c\',15,9,15,2)"><div class="day-appt-name">A1C Treat Consult — Sandra G.</div><div class="day-appt-meta">A1C Mgmt · 15 min</div></div>',
    "day-view Sandra G. card onclick"
)

# Follow-up — David K.
patch(
    SCHED,
    '<div class="day-appt-card" style="background:#7C3AED;"><div class="day-appt-name">Follow-up — David K.</div><div class="day-appt-meta">Weight Mgmt · 15 min · SLA: 2h remaining</div></div>',
    '<div class="day-appt-card" style="background:#7C3AED;cursor:pointer;" onclick="openApptDetail(\'Follow-up\',\'David K. · Weight Mgmt\',\'followup\',15,13,0,2)"><div class="day-appt-name">Follow-up — David K.</div><div class="day-appt-meta">Weight Mgmt · 15 min · SLA: 2h remaining</div></div>',
    "day-view David K. card onclick"
)

# Telehealth Consult — Owen T.
patch(
    SCHED,
    '<div class="day-appt-card video"><div class="day-appt-name">Telehealth Consult — Owen T.</div><div class="day-appt-meta">A1C Mgmt · Video · 15 min</div></div>',
    '<div class="day-appt-card video" style="cursor:pointer;" onclick="openApptDetail(\'Telehealth Consult\',\'Owen T. · A1C Mgmt\',\'video\',15,14,0,2)"><div class="day-appt-name">Telehealth Consult — Owen T.</div><div class="day-appt-meta">A1C Mgmt · Video · 15 min</div></div>',
    "day-view Owen T. card onclick"
)

print("\n─────────────────────────────────────────────────────────")
print("All patches applied. Running qa_check.py...\n")
os.system("python3 /Users/justin.woller/Documents/project-phoenix-demo/qa_check.py")
