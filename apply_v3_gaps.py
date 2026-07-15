#!/usr/bin/env python3
"""Fix 2 genuine gaps found in meeting_demo_update_claude_code_v3 implementation:
   - Change 5:  Lab Results tab absent (only 2 tabs instead of 3)
   - Change 8b: logToChart/useInternalMsg show toasts instead of timeline entry / nav tooltip
"""

CHART = '/Users/justin.woller/Documents/project-phoenix-demo/templates/provider/chart.html'

with open(CHART, 'r', encoding='utf-8') as f:
    html = f.read()

changes = []

# ══════════════════════════════════════════════════════════════════
# CHANGE 5 — Add Lab Results tab back (Documentation|LabResults|Communication)
# ══════════════════════════════════════════════════════════════════

# 5a — Tab buttons: insert Lab Results between Documentation and Communication
old_tabs = '''        <button class="right-tab-btn active" onclick="switchRightTab(0)">Documentation</button>
        <button class="right-tab-btn" onclick="switchRightTab(1)">Communication</button>'''
new_tabs = '''        <button class="right-tab-btn active" onclick="switchRightTab(0)">Documentation</button>
        <button class="right-tab-btn" onclick="switchRightTab(1)">Lab Results</button>
        <button class="right-tab-btn" onclick="switchRightTab(2)">Communication</button>'''
if old_tabs in html:
    html = html.replace(old_tabs, new_tabs, 1)
    changes.append('5a: Lab Results tab button inserted at index 1')
else:
    changes.append('5a MISS: tab buttons not found')

# 5b — Rename Communication panel: rightPanel1 → rightPanel2
old_comm_open = '      <!-- Communication — Activity Composer -->\n      <div class="right-panel" id="rightPanel1" style="padding:0;overflow:hidden;display:flex;flex-direction:column;">'
new_comm_open = '      <!-- Communication — Activity Composer -->\n      <div class="right-panel" id="rightPanel2" style="padding:0;overflow:hidden;display:flex;flex-direction:column;">'
if old_comm_open in html:
    html = html.replace(old_comm_open, new_comm_open, 1)
    changes.append('5b: Communication panel renamed rightPanel1 → rightPanel2')
else:
    changes.append('5b MISS: Communication panel opening tag not found')

# 5c — Insert new Lab Results panel (rightPanel1) just before the Communication panel
LAB_PANEL = '''      <!-- Lab Results panel -->
      <div class="right-panel" id="rightPanel1" style="padding:14px 16px;overflow-y:auto;display:none;">
        <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#6B7280;margin-bottom:4px;">Lab Results</div>
        <div style="font-size:11px;color:#9CA3AF;margin-bottom:12px;">Collected: Apr 24, 2026 &middot; Quest Diagnostics</div>
        <div class="lab-row"><span class="lab-name">Total Testosterone</span><span class="lab-val">485 ng/dL</span><span class="lab-range">300&ndash;1000 ng/dL</span><span class="lab-flag flag-norm">NL</span></div>
        <div class="lab-row"><span class="lab-name">Free Testosterone</span><span class="lab-val">12.4 pg/mL</span><span class="lab-range">9&ndash;26 pg/mL</span><span class="lab-flag flag-norm">NL</span></div>
        <div class="lab-row"><span class="lab-name">LH</span><span class="lab-val">4.2 mIU/mL</span><span class="lab-range">1.5&ndash;9.3 mIU/mL</span><span class="lab-flag flag-norm">NL</span></div>
        <div class="lab-row"><span class="lab-name">FSH</span><span class="lab-val">3.8 mIU/mL</span><span class="lab-range">1.4&ndash;18.1 mIU/mL</span><span class="lab-flag flag-norm">NL</span></div>
        <div class="lab-row"><span class="lab-name">SHBG</span><span class="lab-val">48 nmol/L</span><span class="lab-range">10&ndash;57 nmol/L</span><span class="lab-flag flag-norm">NL</span></div>
        <div class="lab-row"><span class="lab-name">Estradiol</span><span class="lab-val">22 pg/mL</span><span class="lab-range">10&ndash;40 pg/mL</span><span class="lab-flag flag-norm">NL</span></div>
        <div class="lab-row"><span class="lab-name">Hematocrit</span><span class="lab-val">47.2%</span><span class="lab-range">41&ndash;53%</span><span class="lab-flag flag-norm">NL</span></div>
        <div class="lab-row"><span class="lab-name">PSA</span><span class="lab-val">0.8 ng/mL</span><span class="lab-range">&lt;4.0 ng/mL</span><span class="lab-flag flag-norm">NL</span></div>
        <div style="background:#D1FAE5;border:1px solid #6EE7B7;border-radius:6px;padding:8px 10px;margin-top:10px;font-size:11px;color:#065F46;">
          <strong>Provider note:</strong> All values within range. Follow-up recheck in 90 days. Dosing stable &mdash; no adjustments required this visit.
        </div>
      </div>

'''
if '      <!-- Communication — Activity Composer -->' in html:
    html = html.replace('      <!-- Communication — Activity Composer -->', LAB_PANEL + '      <!-- Communication — Activity Composer -->', 1)
    changes.append('5c: Lab Results rightPanel1 inserted before Communication panel')
else:
    changes.append('5c MISS: Communication panel comment anchor not found')

# 5d — Update RIGHT_PANEL_FLEX and comment
old_flex_block = '''// Right panel tabs — targets by ID so DOM order doesn't matter
// Panel map: 0=Documentation(flex), 1=Communication(flex)
var RIGHT_PANEL_FLEX = {0: true, 1: true};
document.addEventListener('DOMContentLoaded', function() { switchRightTab(0); });
function switchRightTab(idx) {
  document.querySelectorAll('.right-tab-btn').forEach(function(b, i) { b.classList.toggle('active', i === idx); });
  for (var i = 0; i < 2; i++) {'''
new_flex_block = '''// Right panel tabs — targets by ID so DOM order doesn't matter
// Panel map: 0=Documentation(flex), 1=Lab Results(block), 2=Communication(flex)
var RIGHT_PANEL_FLEX = {0: true, 2: true};
document.addEventListener('DOMContentLoaded', function() { switchRightTab(0); });
function switchRightTab(idx) {
  document.querySelectorAll('.right-tab-btn').forEach(function(b, i) { b.classList.toggle('active', i === idx); });
  for (var i = 0; i < 3; i++) {'''
if old_flex_block in html:
    html = html.replace(old_flex_block, new_flex_block, 1)
    changes.append('5d: RIGHT_PANEL_FLEX updated to {0:true,2:true}, loop extended to 3')
else:
    changes.append('5d MISS: RIGHT_PANEL_FLEX block not found')

# ══════════════════════════════════════════════════════════════════
# CHANGE 8b — logToChart: append timestamped entry to activity timeline
#             useInternalMsg: show tooltip near nav bar (not a toast)
# ══════════════════════════════════════════════════════════════════

old_log = '''function logToChart() {
  document.getElementById('msgIndividualModal').classList.remove('open');
  var name = window._routeToName || '';
  showRouteToast('✓ Message sent to ' + (name || 'team member') + ' — logged to patient chart');
}
function useInternalMsg() {
  document.getElementById('msgIndividualModal').classList.remove('open');
  var name = window._routeToName || '';
  showRouteToast('✓ Message sent to ' + (name || 'team member') + ' via Internal Messaging');
}'''

new_log = '''function logToChart() {
  document.getElementById('msgIndividualModal').classList.remove('open');
  var now = new Date();
  var timeStr = now.toLocaleTimeString('en-US', {hour:'numeric', minute:'2-digit', hour12:true});
  // Append timestamped note to activity timeline (event-log-body)
  var logBody = document.querySelector('.event-log-body');
  if (logBody) {
    var entry = document.createElement('div');
    entry.style.cssText = 'padding:10px 14px;border-bottom:1px solid #F3F4F6;background:#F0FDF4;flex-shrink:0;';
    entry.innerHTML = '<div style="font-size:10px;color:#6B7280;margin-bottom:2px;">' + timeStr + '</div>' +
      '<div style="font-size:12px;color:#374151;font-weight:500;">&#128203; Internal message logged to patient chart &mdash; ' + timeStr + '</div>';
    logBody.insertBefore(entry, logBody.firstChild);
  }
  showRouteToast('\\u2713 Message logged to patient chart');
}
function useInternalMsg() {
  document.getElementById('msgIndividualModal').classList.remove('open');
  // Show tooltip near nav bar (not a toast)
  var tip = document.getElementById('navMsgTooltip');
  if (!tip) {
    tip = document.createElement('div');
    tip.id = 'navMsgTooltip';
    tip.style.cssText = 'position:fixed;left:60px;top:120px;background:#1F2937;color:#fff;font-size:12px;padding:10px 14px;border-radius:8px;z-index:2000;max-width:260px;line-height:1.5;box-shadow:0 4px 16px rgba(0,0,0,0.25);pointer-events:none;display:none;';
    document.body.appendChild(tip);
  }
  tip.textContent = 'For general messages not related to a patient consult, use Internal Messages in the nav bar.';
  tip.style.display = 'block';
  setTimeout(function(){ tip.style.display = 'none'; }, 3000);
}'''

if old_log in html:
    html = html.replace(old_log, new_log, 1)
    changes.append('8b: logToChart now appends timestamped entry to .event-log-body timeline')
    changes.append('8b: useInternalMsg now shows fixed tooltip near nav bar for 3s')
else:
    changes.append('8b MISS: logToChart/useInternalMsg block not found')

with open(CHART, 'w', encoding='utf-8') as f:
    f.write(html)

print('Applied changes:')
for c in changes:
    icon = '❌' if 'MISS' in c else '✅'
    print(f'  {icon} {c}')

misses = [c for c in changes if 'MISS' in c]
print(f'\n{"All clear." if not misses else str(len(misses)) + " MISS(ES) — check manually."}')
