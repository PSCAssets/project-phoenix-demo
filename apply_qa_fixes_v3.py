#!/usr/bin/env python3
"""
apply_qa_fixes_v3.py — QA patch batch 3
Covers: settings page dynamic names, GC dashboard name fix,
        GC queue genetics-specific consults, client name polish.

Run from project root:
  python3 apply_qa_fixes_v3.py
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
    full = os.path.join(BASE, path)
    content = read(full)
    count = content.count(old)
    if count < min_count:
        print(f"  ✗ MISS [{label or path}] — found {count} (need ≥{min_count})")
        sys.exit(1)
    write(full, content.replace(old, new))
    print(f"  ✓ {label or path} ({count} replacements)")


# ─────────────────────────────────────────────────────────────
# 1. provider.py — update settings route to pass role_label
# ─────────────────────────────────────────────────────────────
print("\n[1] provider.py — settings route role_label")

patch(
    'modules/provider.py',
    "@bp.route(\"/settings\")\ndef settings():\n    return render_template(\"provider/settings.html\")",
    """@bp.route("/settings")
def settings():
    role = session.get('role', 'provider_md')
    role_labels = {
        'provider_md': 'Physician (MD)',
        'provider_np': 'Nurse Practitioner (NP)',
        'provider_rn': 'Registered Nurse (RN)',
        'provider_gc': 'Genetic Counselor (GC)',
        'provider_ma': 'Medical Assistant (MA)',
        'provider_do': 'Physician (DO)',
        'scheduler': 'Scheduler',
        'gc_admin': 'GC Admin',
        'qa_reviewer': 'QA Reviewer',
    }
    return render_template("provider/settings.html", role_label=role_labels.get(role, 'Provider'))""",
    "settings route with role_label"
)

# ─────────────────────────────────────────────────────────────
# 2. settings.html — fix all hardcoded "Dr. Sarah Lee" instances
# ─────────────────────────────────────────────────────────────
print("\n[2] settings.html — dynamic names")

SETT = 'templates/provider/settings.html'

# Sidebar avatar SL → dynamic
patch(
    SETT,
    '<div class="sib-avatar">SL</div>',
    '<div class="sib-avatar" id="settAvatarInit">SL</div>',
    "sidebar avatar id"
)

# Inject avatar init script before {% raw %} in scripts block
# First check if {% block scripts %} exists in settings.html
s_content = read(os.path.join(BASE, SETT))
if '{% block scripts %}' in s_content and '{% raw %}' in s_content:
    patch(
        SETT,
        '{% block scripts %}\n{% raw %}',
        '''{% block scripts %}
<script>
(function(){
  var dn = "{{ session.get('display_name', 'Sarah Lee') }}";
  var parts = dn.split(',')[0].split(' ').filter(function(w){ return w.length > 2; });
  if (!parts.length) parts = dn.split(',')[0].split(' ');
  var init = (parts[0]||'S')[0] + (parts.length > 1 ? (parts[parts.length-1]||'L')[0] : '');
  var el = document.getElementById('settAvatarInit');
  if (el) el.textContent = init.toUpperCase();
})();
</script>
{% raw %}''',
        "settings avatar init script"
    )
else:
    # If no raw block, just append a script at the end of the block
    print("  ⚠ No {% raw %} block in settings.html — skipping avatar script injection")

# Page subtitle: "Dr. Sarah Lee, MD — Provider Portal" → dynamic
patch(
    SETT,
    '    <p>Dr. Sarah Lee, MD — Provider Portal</p>',
    '    <p>{{ session.get(\'display_name\', \'Dr. Sarah Lee, MD\') }} — Provider Portal</p>',
    "settings subtitle dynamic"
)

# Full Name field value
patch(
    SETT,
    'value="Dr. Sarah Lee, MD"',
    'value="{{ session.get(\'display_name\', \'Dr. Sarah Lee, MD\') }}"',
    "Full Name field dynamic"
)

# Role field value
patch(
    SETT,
    'value="Physician (MD)"',
    'value="{{ role_label }}"',
    "Role field dynamic"
)

# "← My Dashboard" back link (still points to /provider/)
patch(
    SETT,
    '<a href="/provider/">← My Dashboard</a>',
    '<a href="/provider/home">← My Dashboard</a>',
    "My Dashboard link fix"
)

# ─────────────────────────────────────────────────────────────
# 3. gc_dashboard.html — fix hardcoded "Lisa" / "Lisa Park" names
# ─────────────────────────────────────────────────────────────
print("\n[3] gc_dashboard.html — dynamic names")

GC = 'templates/provider/gc_dashboard.html'

# Sidebar footer avatar LP + "Lisa Park" text → dynamic
patch(
    GC,
    '    <div class="provider-avatar" title="Lisa Park, MS CGC">LP</div>\n    <div style="font-size:9px;color:#6B7280;text-align:center">Lisa Park</div>',
    '''    <div class="provider-avatar" id="gcAvatarInit" title="{{ session.get('display_name', 'Taylor Brooks, GC') }}">LP</div>
    <div style="font-size:9px;color:#6B7280;text-align:center" id="gcSidebarName">Taylor Brooks</div>''',
    "GC avatar + name dynamic"
)

# "Good morning, Lisa" → dynamic first name
patch(
    GC,
    '        <h2>Good morning, Lisa</h2>',
    '''        <h2>Good morning, {% set _gcdn = session.get('display_name', 'Taylor Brooks, GC').split(',')[0].split() %}{{ (_gcdn[1] if _gcdn|length > 2 else _gcdn[0]) if _gcdn else 'there' }}</h2>''',
    "GC greeting dynamic"
)

# Page title tag
patch(
    GC,
    '{% block title %}GC Dashboard — Lisa Park | Project Phoenix{% endblock %}',
    "{% block title %}GC Dashboard — {{ session.get('display_name', 'Taylor Brooks, GC').split(',')[0] }} | Project Phoenix{% endblock %}",
    "GC page title dynamic"
)

# Inject avatar init script in GC dashboard
# Find where scripts block is
gc_content = read(os.path.join(BASE, GC))
if '{% block scripts %}' in gc_content and '{% raw %}' in gc_content:
    patch(
        GC,
        '{% block scripts %}\n{% raw %}',
        '''{% block scripts %}
<script>
(function(){
  var dn = "{{ session.get('display_name', 'Taylor Brooks, GC') }}";
  var parts = dn.split(',')[0].split(' ').filter(function(w){ return w.length > 2; });
  if (!parts.length) parts = dn.split(',')[0].split(' ');
  var init = (parts[0]||'T')[0] + (parts.length > 1 ? (parts[parts.length-1]||'B')[0] : '');
  var el = document.getElementById('gcAvatarInit');
  if (el) { el.textContent = init.toUpperCase(); el.title = dn; }
  var nameEl = document.getElementById('gcSidebarName');
  if (nameEl) {
    var firstName = parts.length > 2 ? parts[1] : parts[0];
    nameEl.textContent = firstName || 'Taylor';
  }
})();
</script>
{% raw %}''',
        "GC avatar init script"
    )
else:
    # Try to add before </body>
    patch(
        GC,
        '{% endblock %}',
        '''<script>
(function(){
  var dn = "{{ session.get('display_name', 'Taylor Brooks, GC') }}";
  var parts = dn.split(',')[0].split(' ').filter(function(w){ return w.length > 2; });
  if (!parts.length) parts = dn.split(',')[0].split(' ');
  var init = (parts[0]||'T')[0] + (parts.length > 1 ? (parts[parts.length-1]||'B')[0] : '');
  var el = document.getElementById('gcAvatarInit');
  if (el) { el.textContent = init.toUpperCase(); }
  var nameEl = document.getElementById('gcSidebarName');
  if (nameEl) { nameEl.textContent = parts[1] || parts[0] || 'Taylor'; }
})();
</script>
{% endblock %}''',
        "GC avatar init script (no raw block)",
        allow_zero=True
    )

# ─────────────────────────────────────────────────────────────
# 4. queue.html — add GC-specific genetics consult rows
#    Wrapped in {% if session.get('role') == 'provider_gc' %}
# ─────────────────────────────────────────────────────────────
print("\n[4] queue.html — GC-specific genetics rows")

GC_ROWS = '''      <tbody id="queueTableBody">

        {% if session.get('role') == 'provider_gc' %}
        <!-- GC Genetics Queue — shown only for provider_gc role -->

        <tr class="sla-red" data-type="async" data-sla="overdue" data-assigned="unassigned" data-product="BRCA Counseling" data-status="overdue">
          <td class="icon-cell"><i class="ti ti-alert-triangle" style="color:var(--red);font-size:16px;"></i></td>
          <td><a class="patient-link" href="/provider/chart?type=async&amp;view_only=1">Jennifer Walsh</a><div class="patient-dob">DOB: 03/14/1990 <span class="patient-gender">F</span></div><span class="client-badge" style="background:#EEF2FF;color:#3730A3;font-size:10px;font-weight:700;border-radius:4px;padding:1px 5px;">Blueprint Genetics</span></td>
          <td class="age-cell">34y</td>
          <td class="consult-id">CST-2026-10901</td>
          <td><span class="type-pill t-async">Async</span></td>
          <td class="program-cell">BRCA Counseling</td>
          <td style="font-size:12px;font-weight:600;color:#6B7280;">TX</td>
          <td class="wait-time red">4h 22m</td>
          <td><span class="sla-badge sb-red" title="SLA Overdue — 22 min past limit">⚠ 22 min ago</span></td>
          <td></td>
          <td class="actions-cell">
            <button class="take-btn">Take</button>
            <button class="route-btn" onclick="toggleRoute(this.closest('tr'),1)">Route</button>
            <button class="escalate-btn" title="Escalate"><i class="ti ti-arrow-up"></i></button>
          </td>
        </tr>

        <tr class="sla-orange" data-type="video" data-sla="urgent" data-assigned="unassigned" data-product="Hereditary Cancer Panel" data-status="urgent">
          <td class="icon-cell"><i class="ti ti-clock" style="color:var(--orange);font-size:16px;"></i></td>
          <td><a class="patient-link" href="/provider/chart?type=video&amp;view_only=1">Robert Kim</a><div class="patient-dob">DOB: 07/22/1979 <span class="patient-gender">M</span></div><span class="client-badge" style="background:#EEF2FF;color:#3730A3;font-size:10px;font-weight:700;border-radius:4px;padding:1px 5px;">GeneDx Referral</span></td>
          <td class="age-cell">45y</td>
          <td class="consult-id">CST-2026-10902</td>
          <td><span class="type-pill t-video">Video</span></td>
          <td class="program-cell">Hereditary Cancer Panel</td>
          <td style="font-size:12px;font-weight:600;color:#6B7280;">CA</td>
          <td class="wait-time orange">2h 15m</td>
          <td><span class="sla-badge sb-orange">⚠ 45 min</span></td>
          <td></td>
          <td class="actions-cell">
            <button class="take-btn">Take</button>
            <button class="route-btn" onclick="toggleRoute(this.closest('tr'),2)">Route</button>
            <button class="escalate-btn" title="Escalate"><i class="ti ti-arrow-up"></i></button>
          </td>
        </tr>

        <tr class="sla-yellow" data-type="async" data-sla="warning" data-assigned="unassigned" data-product="Carrier Screening" data-status="active">
          <td class="icon-cell"><i class="ti ti-clock" style="color:var(--yellow);font-size:16px;"></i></td>
          <td><a class="patient-link" href="/provider/chart?type=async&amp;view_only=1">Angela Torres</a><div class="patient-dob">DOB: 11/05/1994 <span class="patient-gender">F</span></div><span class="client-badge" style="background:#EEF2FF;color:#3730A3;font-size:10px;font-weight:700;border-radius:4px;padding:1px 5px;">CareFirst Insurance</span></td>
          <td class="age-cell">29y</td>
          <td class="consult-id">CST-2026-10903</td>
          <td><span class="type-pill t-async">Async</span></td>
          <td class="program-cell">Carrier Screening</td>
          <td style="font-size:12px;font-weight:600;color:#6B7280;">TX</td>
          <td class="wait-time yellow">1h 41m</td>
          <td><span class="sla-badge sb-yellow">2h remaining</span></td>
          <td></td>
          <td class="actions-cell">
            <button class="take-btn">Take</button>
            <button class="route-btn" onclick="toggleRoute(this.closest('tr'),3)">Route</button>
            <button class="escalate-btn" title="Escalate"><i class="ti ti-arrow-up"></i></button>
          </td>
        </tr>

        <tr data-type="video" data-sla="ok" data-assigned="unassigned" data-product="Prenatal Carrier Screening" data-status="active">
          <td class="icon-cell"></td>
          <td><a class="patient-link" href="/provider/chart?type=video&amp;view_only=1">Sarah Chen</a><div class="patient-dob">DOB: 02/19/1991 <span class="patient-gender">F</span></div><span class="client-badge" style="background:#EEF2FF;color:#3730A3;font-size:10px;font-weight:700;border-radius:4px;padding:1px 5px;">Blueprint Genetics</span></td>
          <td class="age-cell">33y</td>
          <td class="consult-id">CST-2026-10904</td>
          <td><span class="type-pill t-video">Video</span></td>
          <td class="program-cell">Prenatal Carrier Screening</td>
          <td style="font-size:12px;font-weight:600;color:#6B7280;">IL</td>
          <td class="wait-time">52m</td>
          <td><span class="sla-badge sb-green">Within SLA</span></td>
          <td></td>
          <td class="actions-cell">
            <button class="take-btn">Take</button>
            <button class="route-btn" onclick="toggleRoute(this.closest('tr'),4)">Route</button>
            <button class="escalate-btn" title="Escalate"><i class="ti ti-arrow-up"></i></button>
          </td>
        </tr>

        <tr data-type="async" data-sla="ok" data-assigned="unassigned" data-product="Hereditary Risk Assessment" data-status="active">
          <td class="icon-cell"></td>
          <td><a class="patient-link" href="/provider/chart?type=async&amp;view_only=1">Michael Grant</a><div class="patient-dob">DOB: 12/03/1972 <span class="patient-gender">M</span></div><span class="client-badge" style="background:#EEF2FF;color:#3730A3;font-size:10px;font-weight:700;border-radius:4px;padding:1px 5px;">GeneDx Referral</span></td>
          <td class="age-cell">52y</td>
          <td class="consult-id">CST-2026-10905</td>
          <td><span class="type-pill t-async">Async</span></td>
          <td class="program-cell">Hereditary Risk Assessment</td>
          <td style="font-size:12px;font-weight:600;color:#6B7280;">NV</td>
          <td class="wait-time">28m</td>
          <td><span class="sla-badge sb-green">Within SLA</span></td>
          <td></td>
          <td class="actions-cell">
            <button class="take-btn">Take</button>
            <button class="route-btn" onclick="toggleRoute(this.closest('tr'),5)">Route</button>
            <button class="escalate-btn" title="Escalate"><i class="ti ti-arrow-up"></i></button>
          </td>
        </tr>

        <tr data-type="async" data-sla="ok" data-assigned="unassigned" data-product="BRCA Counseling" data-status="active">
          <td class="icon-cell"></td>
          <td><a class="patient-link" href="/provider/chart?type=async&amp;view_only=1">Diana Ross</a><div class="patient-dob">DOB: 01/22/1957 <span class="patient-gender">F</span></div><span class="client-badge" style="background:#EEF2FF;color:#3730A3;font-size:10px;font-weight:700;border-radius:4px;padding:1px 5px;">CareFirst Insurance</span></td>
          <td class="age-cell">68y</td>
          <td class="consult-id">CST-2026-10906</td>
          <td><span class="type-pill t-async">Async</span></td>
          <td class="program-cell">BRCA Counseling</td>
          <td style="font-size:12px;font-weight:600;color:#6B7280;">NV</td>
          <td class="wait-time">12m</td>
          <td><span class="sla-badge sb-green">Within SLA</span></td>
          <td></td>
          <td class="actions-cell">
            <button class="take-btn">Take</button>
            <button class="route-btn" onclick="toggleRoute(this.closest('tr'),6)">Route</button>
            <button class="escalate-btn" title="Escalate"><i class="ti ti-arrow-up"></i></button>
          </td>
        </tr>

        {% else %}
        <!-- Standard MD/NP queue rows below -->

'''

patch(
    'templates/provider/queue.html',
    '      <tbody id="queueTableBody">\n\n        <tr class="sla-red"',
    GC_ROWS + '        <tr class="sla-red"',
    "inject GC rows + conditional open"
)

# Close the {% else %} ... {% endif %} right before </tbody>
patch(
    'templates/provider/queue.html',
    '      </tbody>\n    </table>',
    '        {% endif %}\n      </tbody>\n    </table>',
    "close GC conditional before </tbody>"
)

print("\n─────────────────────────────────────────────────────────")
print("All patches applied. Running qa_check.py...\n")
os.system("python3 /Users/justin.woller/Documents/project-phoenix-demo/qa_check.py")
