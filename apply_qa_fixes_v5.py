#!/usr/bin/env python3
"""
apply_qa_fixes_v5.py — QA fixes batch 5 for Project Phoenix demo
Fixes:
  1. np_dashboard.html   — Remove duplicate home icon (sidebar-back anchor)
  2. schedule.html       — Fix RTQ modal z-index (800→2500, above apptDetailModal at 2000)
  3. schedule.html       — Make provider name dynamic in schedule header + modal notes
  4. schedule.html       — GC-role appointment names → genetics test names
  5. chart.html          — Move expand arrow from bottom → top of vnav bar
  6. queue.html          — Replace Readiness column with Program / DOB / Gender columns
  7. queue.html          — Update program badge names (Everlywell360, Humana-A1C, Elevance-AV)
  8. np_dashboard.html   — Add State column to Active Consults table (TX/IL only)
"""

import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
errors = []

def apply(filepath, old, new, label):
    full = os.path.join(BASE, filepath)
    with open(full, 'r', encoding='utf-8') as f:
        content = f.read()
    if old not in content:
        errors.append(f"  [MISS] {label} — anchor not found in {filepath}")
        return False
    count = content.count(old)
    if count > 1:
        print(f"  [WARN] {label} — {count}x occurrences, replacing all")
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content.replace(old, new))
    print(f"  [OK]  {label}")
    return True


# ===========================================================================
# OP 1: np_dashboard.html — remove sidebar-back that shows as duplicate home icon
# ===========================================================================
print("\n=== OP 1: np_dashboard.html — remove duplicate home icon ===")
apply(
    'templates/provider/np_dashboard.html',
    '''    <a href="/provider/np" class="sidebar-back" title="My Dashboard">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
      </svg>
      <span class="nav-label" style="color:#6B21A8;font-weight:600;">My Dashboard</span>
    </a>''',
    '',
    'Remove sidebar-back duplicate home icon'
)

# ===========================================================================
# OP 2: schedule.html — fix RTQ modal z-index so it appears above apptDetailModal
# ===========================================================================
print("\n=== OP 2: schedule.html — fix RTQ modal z-index 800→2500 ===")
apply(
    'templates/provider/schedule.html',
    '<div id="rtQueueModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.45);z-index:800;align-items:center;justify-content:center;">',
    '<div id="rtQueueModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.45);z-index:2500;align-items:center;justify-content:center;">',
    'RTQ modal z-index 800→2500'
)

# ===========================================================================
# OP 3: schedule.html — dynamic provider name in schedule header
# ===========================================================================
print("\n=== OP 3: schedule.html — dynamic provider name in header ===")
apply(
    'templates/provider/schedule.html',
    '<div style="font-size:13px;color:#6B7280;">Dr. Sarah Lee, MD</div>',
    '<div style="font-size:13px;color:#6B7280;">{{ session.get(\'display_name\', \'Dr. Sarah Lee, MD\') }}</div>',
    'Dynamic provider name in schedule header'
)

# OP 3b: dynamic provider name in appointment modal notes
apply(
    'templates/provider/schedule.html',
    "document.getElementById('apptDetailNotes').textContent = '\"' + patient + ' — ' + product + ' consult. Duration: ' + dur + ' min. Provider: Dr. Sarah Lee, MD.\"';",
    "var provName = document.getElementById('schedProviderName') ? document.getElementById('schedProviderName').textContent : 'Dr. Sarah Lee, MD';\n  document.getElementById('apptDetailNotes').textContent = '\"' + patient + ' — ' + product + ' consult. Duration: ' + dur + ' min. Provider: ' + provName + '.\"';",
    'Dynamic provider name in appointment modal notes'
)

# OP 3c: add hidden span with provider name for JS to read
apply(
    'templates/provider/schedule.html',
    '<div style="font-size:13px;color:#6B7280;">{{ session.get(\'display_name\', \'Dr. Sarah Lee, MD\') }}</div>',
    '<div style="font-size:13px;color:#6B7280;" id="schedProviderName">{{ session.get(\'display_name\', \'Dr. Sarah Lee, MD\') }}</div>',
    'Add id to provider name element for JS reference'
)

# ===========================================================================
# OP 4: schedule.html — GC role: rename appointment types to genetics tests
# ===========================================================================
print("\n=== OP 4: schedule.html — GC genetics appointment names ===")
# Inject GC-specific day-view appointment override after opening script tag
# We use a JS block that renames appointments when role is GC
GC_APPT_JS = '''
{% if session.get('role') == 'provider_gc' %}
<script>
// GC role: rename appointment titles to genetics test types
document.addEventListener('DOMContentLoaded', function() {
  var gcApptMap = {
    'Annual Visit':       'BRCA Genetic Counseling',
    'A1C Treat Consult':  'Hereditary Cancer Panel',
    'Telehealth Consult': 'Carrier Screening Consult',
    'Phone Consult':      'Prenatal Genetics Consult',
    'Follow-up':          'Variant of Uncertain Significance Follow-up',
  };
  document.querySelectorAll('.day-appt-name').forEach(function(el) {
    for (var key in gcApptMap) {
      if (el.textContent.startsWith(key)) {
        el.textContent = el.textContent.replace(key, gcApptMap[key]);
        break;
      }
    }
  });
  document.querySelectorAll('.day-appt-meta').forEach(function(el) {
    var metaMap = {
      'A1C Mgmt':      'GeneDx Panel',
      'Women\'s Health': 'Blueprint Genetics',
      'STI Panel':       'Prenatal Carrier Screen',
      'Weight Mgmt':     'Hereditary Risk Assessment',
      'ED Treatment':    'BRCA1/2 Analysis',
    };
    for (var key in metaMap) {
      if (el.textContent.includes(key)) {
        el.textContent = el.textContent.replace(key, metaMap[key]);
      }
    }
  });
});
</script>
{% endif %}
'''
apply(
    'templates/provider/schedule.html',
    '{% endraw %}\n{% endblock %}',
    GC_APPT_JS + '{% endraw %}\n{% endblock %}',
    'GC genetics appointment names (JS rename on DOM load)'
)

# ===========================================================================
# OP 5: chart.html — move expand arrow from bottom to top of vnav bar
# ===========================================================================
print("\n=== OP 5: chart.html — move expand arrow to top of vnav ===")

# Remove margin-top: auto from expand button CSS
apply(
    'templates/provider/chart.html',
    '.rp-vnav-expand {\n  margin-top: auto; width: 36px; height: 28px; border: 1px solid #E5E0D8;\n  border-radius: 6px; background: #fff; color: #6B7280; font-size: 12px;\n  cursor: pointer; display: flex; align-items: center; justify-content: center;\n}',
    '.rp-vnav-expand {\n  width: 36px; height: 28px; border: 1px solid #E5E0D8;\n  border-radius: 6px; background: #fff; color: #6B7280; font-size: 12px;\n  cursor: pointer; display: flex; align-items: center; justify-content: center;\n  margin-bottom: 6px;\n}',
    'Remove margin-top:auto, add margin-bottom for spacing after arrow'
)

# Move expand button HTML from bottom to top of the nav
apply(
    'templates/provider/chart.html',
    '        <button class="rp-vnav-btn active" id="rpVnavBtn0" onclick="switchRightTab(0)">\n          📄<span class="vnav-tip">Documentation</span>\n        </button>',
    '        <button class="rp-vnav-expand" id="panelExpandBtn" onclick="togglePanelExpand()" title="Expand/collapse panel" style="font-size:14px;">&#9655;</button>\n        <button class="rp-vnav-btn active" id="rpVnavBtn0" onclick="switchRightTab(0)">\n          📄<span class="vnav-tip">Documentation</span>\n        </button>',
    'Move expand button to top of nav'
)

# Remove expand button from original bottom position
apply(
    'templates/provider/chart.html',
    '        <button class="rp-vnav-expand" id="panelExpandBtn" onclick="togglePanelExpand()" title="Expand/collapse panel" style="font-size:14px;">&#9655;</button>\n      </nav>',
    '      </nav>',
    'Remove expand button from bottom position'
)

# ===========================================================================
# OP 6: queue.html — replace Readiness column header with Program / DOB / Gender
# ===========================================================================
print("\n=== OP 6: queue.html — replace Readiness column header ===")
apply(
    'templates/provider/queue.html',
    '          <th>Readiness</th>\n          <th style="text-align:right;"><button id="showInProgressBtn" onclick="toggleInProgress(this)" style="padding:4px 12px;border-radius:6px;font-size:12px;font-weight:600;border:1.5px solid #E5E0D8;background:#fff;color:#6B7280;cursor:pointer;">Show In Progress</button></th>',
    '          <th>Program</th>\n          <th>DOB</th>\n          <th>Gender</th>\n          <th></th>',
    'Replace Readiness header with Program/DOB/Gender, remove duplicate Show-In-Progress btn'
)

# ===========================================================================
# OP 7: queue.html — replace client-badge IIFE with full column-restructuring IIFE
# ===========================================================================
print("\n=== OP 7: queue.html — new program/DOB/gender column JS ===")

OLD_IIFE = '''(function() {
  var clients = ['DXS','DXS','LabCorp','LabCorp'];
  var defaultClient = 'Everlywell';
  var styles = {
    DXS:        'background:#EDE9FE;color:#6B21A8',
    LabCorp:    'background:#DBEAFE;color:#1D4ED8',
    Everlywell: 'background:#D1FAE5;color:#065F46'
  };
  var rows = document.querySelectorAll('#queueTableBody tr');
  rows.forEach(function(row, i) {
    var client = clients[i] !== undefined ? clients[i] : defaultClient;
    var badge = document.createElement('span');
    badge.style.cssText = styles[client] + ';font-size:11px;font-weight:600;padding:2px 8px;border-radius:10px;margin-left:7px;vertical-align:middle;display:inline-block;';
    badge.textContent = client;
    var link = row.querySelector('.patient-link');
    if (link) link.insertAdjacentElement('afterend', badge);
  });
})();'''

NEW_IIFE = '''(function() {
  // Program names for MD/NP/RN/MA queue rows (in order)
  var programs = [
    'Everlywell360','Everlywell360','Humana - A1C','Elevance - AV',
    'Humana - A1C','Everlywell360','Elevance - AV','Everlywell360',
    'Humana - A1C','Elevance - AV','Everlywell360','Humana - A1C',
    'Elevance - AV','Everlywell360'
  ];
  var pStyles = {
    'Everlywell360': 'background:#D1FAE5;color:#065F46',
    'Humana - A1C':  'background:#DBEAFE;color:#1D4ED8',
    'Elevance - AV': 'background:#EDE9FE;color:#6B21A8',
    // GC-specific lab/plan labels
    'Blueprint Genetics': 'background:#EEF2FF;color:#3730A3',
    'GeneDx Referral':    'background:#EEF2FF;color:#3730A3',
    'CareFirst Insurance':'background:#FEF3C7;color:#92400E',
  };

  var rows = Array.from(document.querySelectorAll('#queueTableBody tr'));
  var mdIdx = 0;  // counter for MD/NP rows (GC rows use their own badge)

  rows.forEach(function(row) {
    // Hide patient-dob div (data moves to dedicated column)
    var dobDiv = row.querySelector('.patient-dob');
    var dob = '', gender = '';
    if (dobDiv) {
      var m = dobDiv.textContent.match(/DOB:\s*(\d{2}\/\d{2}\/\d{4})/);
      if (m) dob = m[1];
      var gEl = dobDiv.querySelector('.patient-gender');
      if (gEl) gender = gEl.textContent.trim();
      dobDiv.style.display = 'none';
    }

    // Determine program label
    var existingBadge = row.querySelector('.client-badge');
    var label = '';
    if (existingBadge) {
      label = existingBadge.textContent.trim();
      existingBadge.style.display = 'none';  // hide from patient cell
    } else {
      label = programs[mdIdx] || 'Everlywell360';
      mdIdx++;
    }

    // Build the 3 new cells
    var style = pStyles[label] || pStyles['Everlywell360'];
    var progTd = document.createElement('td');
    var badge = document.createElement('span');
    badge.style.cssText = style + ';font-size:11px;font-weight:600;padding:2px 8px;border-radius:10px;display:inline-block;white-space:nowrap;';
    badge.textContent = label;
    progTd.appendChild(badge);

    var dobTd = document.createElement('td');
    dobTd.style.cssText = 'font-size:12px;color:#6B7280;white-space:nowrap;';
    dobTd.textContent = dob;

    var genTd = document.createElement('td');
    genTd.style.cssText = 'font-size:12px;font-weight:600;color:#6B7280;text-align:center;';
    genTd.textContent = gender;

    // Find readiness TD (10th TD, index 9) and replace it
    var tds = row.querySelectorAll('td');
    var readinessTd = tds[9];  // 0-indexed: icon(0) patient(1) age(2) id(3) type(4) product(5) state(6) wait(7) sla(8) readiness(9) actions(10)
    if (readinessTd) {
      var parent = readinessTd.parentNode;
      parent.insertBefore(progTd, readinessTd);
      parent.insertBefore(dobTd, readinessTd);
      parent.insertBefore(genTd, readinessTd);
      parent.removeChild(readinessTd);
    }
  });
})();'''

apply(
    'templates/provider/queue.html',
    OLD_IIFE,
    NEW_IIFE,
    'Replace client-badge IIFE with Program/DOB/Gender column restructuring IIFE'
)

# ===========================================================================
# OP 8: np_dashboard.html — add State column to Active Consults table
# ===========================================================================
print("\n=== OP 8: np_dashboard.html — add State column to Active Consults ===")

# Header: add State column after Type
apply(
    'templates/provider/np_dashboard.html',
    '                <th class="sortable" data-col="type" data-table="consultsTable" style="width:72px">Type <span class="sort-arrow"></span></th>\n                <th class="sortable" data-col="wait" data-table="consultsTable" style="width:70px">Wait Time <span class="sort-arrow"></span></th>',
    '                <th class="sortable" data-col="type" data-table="consultsTable" style="width:72px">Type <span class="sort-arrow"></span></th>\n                <th style="width:46px">State</th>\n                <th class="sortable" data-col="wait" data-table="consultsTable" style="width:70px">Wait Time <span class="sort-arrow"></span></th>',
    'Active Consults: add State header'
)

# Data rows — add state cell after Type cell for each consult row
# Patients: N.K.→TX, D.M.→IL, B.A.→TX, F.O.→IL, C.W.→TX, S.T.→IL, L.V.→TX, R.M.→IL
state_fixes = [
    ('N.K.</div><div class="cr-id">CST-2026-11021',  'TX'),
    ('D.M.</div><div class="cr-id">CST-2026-11014',  'IL'),
    ('B.A.</div><div class="cr-id">CST-2026-11028',  'TX'),
    ('F.O.</div><div class="cr-id">CST-2026-11033',  'IL'),
    ('C.W.</div><div class="cr-id">CST-2026-11041',  'TX'),
    ('S.T.</div><div class="cr-id">CST-2026-11045',  'IL'),
    ('L.V.</div><div class="cr-id">CST-2026-11052',  'TX'),
    ('R.M.</div><div class="cr-id">CST-2026-11037',  'IL'),
]
# For each patient, find their Type td and insert State td after it
# Pattern: <span class="cr-type">XXX</span></td> → add state td after it
# We'll key on the consult ID to ensure the right row
for patient_id_snippet, state in state_fixes:
    # Read current file state each time since we're doing multiple passes
    full_path = os.path.join(BASE, 'templates/provider/np_dashboard.html')
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Find the row block by patient ID snippet and add State td
    # The rows contain: cr-type span then cr-wait span
    # Find the row that contains this patient snippet
    start = content.find(patient_id_snippet)
    if start == -1:
        errors.append(f"  [MISS] State col row update: could not find {patient_id_snippet}")
        continue
    # Find the next </span></td> after cr-type within this row context
    cr_type_start = content.find('<span class="cr-type">', start)
    if cr_type_start == -1:
        errors.append(f"  [MISS] State col: cr-type not found near {patient_id_snippet}")
        continue
    cr_type_end = content.find('</td>', cr_type_start)
    if cr_type_end == -1:
        continue
    cr_type_td_end = cr_type_end + len('</td>')
    state_td = f'\n                <td style="font-size:11px;font-weight:700;color:#6B7280;text-align:center;">{state}</td>'
    # Check if state td already inserted (idempotency)
    next_snippet = content[cr_type_td_end:cr_type_td_end+80]
    if 'cr-wait' in next_snippet or 'cr-status' in next_snippet:
        # Not yet inserted
        content = content[:cr_type_td_end] + state_td + content[cr_type_td_end:]
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [OK]  State '{state}' added for row with {patient_id_snippet.split('<')[0]}")
    else:
        print(f"  [SKIP] State already inserted for {patient_id_snippet.split('<')[0]}")

# ===========================================================================
# Summary
# ===========================================================================
print("\n" + "="*60)
if errors:
    print(f"COMPLETED WITH {len(errors)} MISS(ES):")
    for e in errors:
        print(e)
    sys.exit(1)
else:
    print("ALL OPERATIONS COMPLETED SUCCESSFULLY")
    print("="*60)
    print("\nNext steps:")
    print("  1. python3 app.py → review at http://localhost:5000")
    print("  2. Approve → commit and push")
