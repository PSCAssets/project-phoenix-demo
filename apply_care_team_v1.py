#!/usr/bin/env python3
"""Apply care_team_demo_update_v1.md changes:
  Change 1: Add Zendesk tab to chart.html right panel
  Change 2: Add Real-Time Queue button + modal to schedule.html
  Change 3: Add client name badges to queue.html (via JS)
  Change 4: Fix wizard Step 1 Save & Continue auto-select
"""

import os
BASE = '/Users/justin.woller/Documents/project-phoenix-demo/templates'
CHART   = f'{BASE}/provider/chart.html'
SCHED   = f'{BASE}/provider/schedule.html'
QUEUE   = f'{BASE}/provider/queue.html'
WIZARD  = f'{BASE}/admin/wizard.html'

changes = []

# ═══════════════════════════════════════════════════════════
# CHANGE 1 — Add Zendesk tab (chart.html)
# Precondition: chart_ux_update_v1.md Change A already applied
# Current tabs: Documentation(0) | Communication(1)
# After: Documentation(0) | Communication(1) | 🎫 Zendesk(2)
# ═══════════════════════════════════════════════════════════

with open(CHART, 'r', encoding='utf-8') as f:
    html = f.read()

# 1a: Add Zendesk tab button after Communication
old_tab2 = '''        <button class="right-tab-btn active" onclick="switchRightTab(0)">Documentation</button>
        <button class="right-tab-btn" onclick="switchRightTab(1)">Communication</button>'''
new_tab2 = '''        <button class="right-tab-btn active" onclick="switchRightTab(0)">Documentation</button>
        <button class="right-tab-btn" onclick="switchRightTab(1)">Communication</button>
        <button class="right-tab-btn" onclick="switchRightTab(2)">&#127917; Zendesk</button>'''
if old_tab2 in html:
    html = html.replace(old_tab2, new_tab2, 1)
    changes.append('1a: Zendesk tab button added at index 2')
else:
    changes.append('1a MISS: tab buttons not found for Zendesk insertion')

# 1b: Insert Zendesk panel (rightPanel2) before Documentation comment
ZENDESK_PANEL = '''      <!-- Zendesk panel -->
      <div class="right-panel" id="rightPanel2" style="padding:16px;overflow-y:auto;display:none;flex-direction:column;gap:12px;">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:4px;">
          <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#6B7280;">&#127917; Zendesk &mdash; Active Case</div>
          <button onclick="showRouteToast('Refreshed')" style="font-size:11px;font-weight:600;color:#6B21A8;border:1px solid #6B21A8;background:#fff;border-radius:6px;padding:3px 10px;cursor:pointer;">Refresh</button>
        </div>
        <div style="border:1px solid #E5E7EB;border-radius:8px;padding:12px 14px;background:#FAFAFA;">
          <div style="display:flex;gap:10px;margin-bottom:6px;"><span style="font-size:12px;font-weight:700;color:#374151;min-width:88px;">Case #</span><span style="font-size:12px;color:#1F2937;font-weight:600;">ZD-293847</span></div>
          <div style="display:flex;gap:10px;margin-bottom:6px;"><span style="font-size:12px;font-weight:700;color:#374151;min-width:88px;">Type</span><span style="font-size:12px;color:#1F2937;">Consult Support</span></div>
          <div style="display:flex;gap:10px;margin-bottom:6px;"><span style="font-size:12px;font-weight:700;color:#374151;min-width:88px;">Status</span><span style="font-size:11px;font-weight:600;background:#D1FAE5;color:#059669;padding:2px 8px;border-radius:10px;">&#9679; Open</span></div>
          <div style="display:flex;gap:10px;"><span style="font-size:12px;font-weight:700;color:#374151;min-width:88px;">Assigned</span><span style="font-size:12px;color:#374151;">Beth Lewis</span></div>
        </div>
        <div>
          <div style="font-size:11px;font-weight:700;color:#6B7280;margin-bottom:6px;">Last Agent Note (2h ago)</div>
          <div style="background:#F9FAFB;border-radius:6px;padding:12px;font-size:12px;color:#4B5563;font-style:italic;line-height:1.5;">"Patient called re: consult timeline. Advised 24&ndash;48hr window. Patient confirmed availability for video this week."</div>
          <a href="#" onclick="return false;" style="font-size:12px;font-weight:600;color:#6B21A8;text-decoration:none;display:block;margin-top:8px;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">View Full Case in Zendesk &#8599;</a>
        </div>
        <div>
          <div style="font-size:11px;font-weight:700;color:#6B7280;margin-bottom:6px;">&#10022; Add Note to Case</div>
          <textarea id="zdNoteArea" placeholder="Type a note to sync to Zendesk..." style="width:100%;border:1px solid #E5E7EB;border-radius:6px;min-height:80px;padding:8px 10px;font-size:12px;color:#374151;resize:vertical;box-sizing:border-box;"></textarea>
          <button onclick="addNoteToZendesk()" style="margin-top:6px;background:#6B21A8;color:#fff;border:none;border-radius:6px;padding:6px 16px;font-size:12px;font-weight:600;cursor:pointer;">Add Note</button>
        </div>
      </div>

      <!-- Documentation -->'''
if '      <!-- Documentation -->' in html:
    html = html.replace('      <!-- Documentation -->', ZENDESK_PANEL, 1)
    changes.append('1b: Zendesk rightPanel2 inserted before Documentation panel')
else:
    changes.append('1b MISS: <!-- Documentation --> anchor not found')

# 1c: Update RIGHT_PANEL_FLEX and loop for 3 panels
old_flex3 = '''// Panel map: 0=Documentation(flex), 1=Communication(flex)
var RIGHT_PANEL_FLEX = {0: true, 1: true};
document.addEventListener('DOMContentLoaded', function() { switchRightTab(0); });
function switchRightTab(idx) {
  document.querySelectorAll('.right-tab-btn').forEach(function(b, i) { b.classList.toggle('active', i === idx); });
  for (var i = 0; i < 2; i++) {'''
new_flex3 = '''// Panel map: 0=Documentation(flex), 1=Communication(flex), 2=Zendesk(flex)
var RIGHT_PANEL_FLEX = {0: true, 1: true, 2: true};
document.addEventListener('DOMContentLoaded', function() { switchRightTab(0); });
function switchRightTab(idx) {
  document.querySelectorAll('.right-tab-btn').forEach(function(b, i) { b.classList.toggle('active', i === idx); });
  for (var i = 0; i < 3; i++) {'''
if old_flex3 in html:
    html = html.replace(old_flex3, new_flex3, 1)
    changes.append('1c: RIGHT_PANEL_FLEX = {0:true,1:true,2:true}, loop extended to i<3')
else:
    changes.append('1c MISS: RIGHT_PANEL_FLEX block not found')

# 1d: Add addNoteToZendesk function to JS (before closing </script> of main block)
ZD_JS = '''function addNoteToZendesk() {
  var area = document.getElementById('zdNoteArea');
  if (area) area.value = '';
  showRouteToast('\\u2713 Note synced to Zendesk case ZD-293847');
}
'''
if 'addNoteToZendesk' not in html:
    # Insert before the closing </script> of the raw block
    html = html.replace('function showRouteToast(msg) {', ZD_JS + 'function showRouteToast(msg) {', 1)
    changes.append('1d: addNoteToZendesk() function added')
else:
    changes.append('1d: addNoteToZendesk already present — skipped')

with open(CHART, 'w', encoding='utf-8') as f:
    f.write(html)

# ═══════════════════════════════════════════════════════════
# CHANGE 2 — Real-Time Queue button + modal (schedule.html)
# ═══════════════════════════════════════════════════════════

with open(SCHED, 'r', encoding='utf-8') as f:
    sched = f.read()

# 2a: Add button to topbar
old_topbar_end = '''    <button onclick="editAvailability()" style="background:#fff;border:1.5px solid #E5E0D8;border-radius:7px;padding:7px 14px;font-size:12px;font-weight:600;cursor:pointer;color:#374151;">Edit Availability</button>
  </div>'''
new_topbar_end = '''    <button onclick="editAvailability()" style="background:#fff;border:1.5px solid #E5E0D8;border-radius:7px;padding:7px 14px;font-size:12px;font-weight:600;cursor:pointer;color:#374151;">Edit Availability</button>
    <button onclick="openRTQueueModal()" style="margin-left:8px;background:#6B21A8;color:#fff;border:none;border-radius:7px;padding:7px 16px;font-size:12px;font-weight:600;cursor:pointer;">&#9889; Add to Real-Time Queue</button>
  </div>'''
if old_topbar_end in sched:
    sched = sched.replace(old_topbar_end, new_topbar_end, 1)
    changes.append('2a: ⚡ Add to Real-Time Queue button added to schedule topbar')
else:
    changes.append('2a MISS: topbar end anchor not found in schedule.html')

# 2b: Add modal HTML before closing </script> tag (before {% endraw %})
RT_MODAL = '''
<!-- Real-Time Queue Modal -->
<div id="rtQueueModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.45);z-index:800;align-items:center;justify-content:center;">
  <div style="background:#fff;border-radius:12px;max-width:480px;width:94%;padding:28px 28px 24px;box-shadow:0 8px 32px rgba(0,0,0,0.18);position:relative;">
    <button onclick="closeRTQueueModal()" style="position:absolute;top:14px;right:16px;background:none;border:none;font-size:20px;cursor:pointer;color:#9CA3AF;">&#x2715;</button>
    <div style="font-size:16px;font-weight:700;color:#111827;margin-bottom:16px;">Add Patient to Real-Time Queue</div>
    <div style="background:#F9FAFB;border-radius:8px;padding:14px 16px;margin-bottom:16px;">
      <div style="font-size:12px;color:#6B7280;margin-bottom:4px;">Patient</div>
      <div style="font-size:14px;font-weight:700;color:#111827;">Marcus Johnson</div>
      <div style="font-size:12px;color:#6B7280;margin-top:8px;margin-bottom:2px;">Care Product</div>
      <div style="font-size:13px;font-weight:600;color:#374151;">Testosterone Care</div>
    </div>
    <div style="font-size:13px;color:#374151;margin-bottom:12px;">Adding this patient to the real-time queue will notify available providers immediately.</div>
    <div style="background:#FEF3C7;border-radius:7px;padding:10px 14px;font-size:12px;color:#92400E;font-weight:600;margin-bottom:16px;">&#9203; Estimated wait: ~8 minutes</div>
    <div style="margin-bottom:16px;">
      <label style="font-size:12px;font-weight:600;color:#374151;display:block;margin-bottom:6px;">Agent note (optional)</label>
      <textarea id="rtQueueNote" placeholder="e.g., patient is on hold and ready to connect..." style="width:100%;border:1px solid #E5E7EB;border-radius:6px;padding:8px 10px;font-size:12px;color:#374151;resize:vertical;min-height:72px;box-sizing:border-box;"></textarea>
    </div>
    <div style="display:flex;justify-content:flex-end;gap:10px;">
      <button onclick="closeRTQueueModal()" style="border:1.5px solid #E5E0D8;background:#fff;border-radius:8px;padding:8px 20px;font-size:13px;font-weight:600;cursor:pointer;color:#374151;">Cancel</button>
      <button onclick="confirmRTQueue()" style="background:#6B21A8;color:#fff;border:none;border-radius:8px;padding:8px 22px;font-size:13px;font-weight:700;cursor:pointer;">Add to Queue</button>
    </div>
  </div>
</div>
<div id="rtQueueToast" style="display:none;position:fixed;bottom:28px;left:50%;transform:translateX(-50%);background:#111827;color:#fff;padding:10px 22px;border-radius:8px;font-size:13px;font-weight:600;z-index:900;white-space:nowrap;">&#10003; Marcus Johnson added to real-time queue &mdash; providers notified</div>

'''

# Insert modal before {% endraw %}
if 'rtQueueModal' not in sched:
    sched = sched.replace('</script>\n{% endraw %}', RT_MODAL + '</script>\n{% endraw %}', 1)
    changes.append('2b: Real-Time Queue modal HTML inserted into schedule.html')
else:
    changes.append('2b: rtQueueModal already present — skipped')

# 2c: Add JS functions
RT_JS = '''
function openRTQueueModal() {
  var m = document.getElementById('rtQueueModal');
  m.style.display = 'flex';
}
function closeRTQueueModal() {
  document.getElementById('rtQueueModal').style.display = 'none';
  document.getElementById('rtQueueNote').value = '';
}
function confirmRTQueue() {
  closeRTQueueModal();
  var t = document.getElementById('rtQueueToast');
  t.style.display = 'block';
  setTimeout(function(){ t.style.display = 'none'; }, 3000);
}
document.addEventListener('click', function(e) {
  var m = document.getElementById('rtQueueModal');
  if (m && e.target === m) closeRTQueueModal();
});
'''

if 'openRTQueueModal' not in sched:
    sched = sched.replace('})();\n</script>', '})();\n' + RT_JS + '\n</script>', 1)
    changes.append('2c: openRTQueueModal / closeRTQueueModal / confirmRTQueue JS added')
else:
    changes.append('2c: RT queue JS already present — skipped')

with open(SCHED, 'w', encoding='utf-8') as f:
    f.write(sched)

# ═══════════════════════════════════════════════════════════
# CHANGE 3 — Client name badges in queue.html (via JS)
# First 2 rows: DXS | Next 2: LabCorp | Rest: Everlywell
# ═══════════════════════════════════════════════════════════

with open(QUEUE, 'r', encoding='utf-8') as f:
    queue = f.read()

CLIENT_BADGE_JS = '''
// Change 3 — Client name badges (DXS/LabCorp/Everlywell per row)
(function() {
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
})();
'''

if 'client name badges' not in queue:
    queue = queue.replace('})();\n</script>', '})();\n' + CLIENT_BADGE_JS + '\n</script>', 1)
    changes.append('3: Client name badge JS added to queue.html (DXS/LabCorp/Everlywell per row)')
else:
    changes.append('3: Client badges already present — skipped')

with open(QUEUE, 'w', encoding='utf-8') as f:
    f.write(queue)

# ═══════════════════════════════════════════════════════════
# CHANGE 4 — Fix wizard Step 1 Save & Continue auto-select
# ═══════════════════════════════════════════════════════════

with open(WIZARD, 'r', encoding='utf-8') as f:
    wiz = f.read()

old_init = '(function() { var sel = document.getElementById(\'s0_client\'); if (sel && sel.value) onClientSelect(sel); })();'
new_init = '(function() { var sel = document.getElementById(\'s0_client\'); if (sel) { if (!sel.value && sel.options.length > 1) sel.selectedIndex = 1; if (sel.value) onClientSelect(sel); } })();'

if old_init in wiz:
    wiz = wiz.replace(old_init, new_init, 1)
    changes.append('4: Wizard Step 1 init now auto-selects first client option to enable Save & Continue')
elif 'onClientSelect' in wiz and 'sel.selectedIndex = 1' in wiz:
    changes.append('4: Wizard fix already applied — skipped')
else:
    changes.append('4 MISS: wizard init IIFE not found')

with open(WIZARD, 'w', encoding='utf-8') as f:
    f.write(wiz)

print('Applied care_team_demo_update_v1.md changes:')
for c in changes:
    icon = '❌' if 'MISS' in c else '✅'
    print(f'  {icon} {c}')

misses = [c for c in changes if 'MISS' in c]
print(f'\n{"All clear." if not misses else str(len(misses)) + " MISS(ES) — check manually."}')
