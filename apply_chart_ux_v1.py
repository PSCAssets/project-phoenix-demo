#!/usr/bin/env python3
"""Apply chart_ux_update_v1.md changes to chart.html.
Changes B-F already implemented in a prior session.
Only Change A (remove Lab Results tab) needs to be applied here.
"""

CHART = '/Users/justin.woller/Documents/project-phoenix-demo/templates/provider/chart.html'

with open(CHART, 'r', encoding='utf-8') as f:
    html = f.read()

changes = []

# ═══════════════════════════════════════════════════════════
# CHANGE A — Remove Lab Results tab + panel, renumber
# ═══════════════════════════════════════════════════════════

# A1: Remove Lab Results tab button from the tab bar
# Also change Communication onclick from 2 → 1
old_tabs = '''        <button class="right-tab-btn active" onclick="switchRightTab(0)">Documentation</button>
        <button class="right-tab-btn" onclick="switchRightTab(1)">Lab Results</button>
        <button class="right-tab-btn" onclick="switchRightTab(2)">Communication</button>'''
new_tabs = '''        <button class="right-tab-btn active" onclick="switchRightTab(0)">Documentation</button>
        <button class="right-tab-btn" onclick="switchRightTab(1)">Communication</button>'''
if old_tabs in html:
    html = html.replace(old_tabs, new_tabs, 1)
    changes.append('A1: Lab Results tab button removed; Communication shifted to index 1')
else:
    changes.append('A1 MISS: tab buttons not found')

# A2: Remove the entire Lab Results panel div (rightPanel1)
old_lab_panel = '''      <!-- Lab Results panel -->
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
if old_lab_panel in html:
    html = html.replace(old_lab_panel, '', 1)
    changes.append('A2: Lab Results rightPanel1 div removed')
else:
    changes.append('A2 MISS: Lab Results panel div not found')

# A3: Rename Communication panel: rightPanel2 → rightPanel1
old_comm_id = '      <div class="right-panel" id="rightPanel2" style="padding:0;overflow:hidden;display:flex;flex-direction:column;">'
new_comm_id = '      <div class="right-panel" id="rightPanel1" style="padding:0;overflow:hidden;display:flex;flex-direction:column;">'
if old_comm_id in html:
    html = html.replace(old_comm_id, new_comm_id, 1)
    changes.append('A3: Communication panel id renamed rightPanel2 → rightPanel1')
else:
    changes.append('A3 MISS: Communication panel id not found')

# A4: Update RIGHT_PANEL_FLEX comment, map, and loop count
old_flex = '''// Panel map: 0=Documentation(flex), 1=Lab Results(block), 2=Communication(flex)
var RIGHT_PANEL_FLEX = {0: true, 2: true};
document.addEventListener('DOMContentLoaded', function() { switchRightTab(0); });
function switchRightTab(idx) {
  document.querySelectorAll('.right-tab-btn').forEach(function(b, i) { b.classList.toggle('active', i === idx); });
  for (var i = 0; i < 3; i++) {'''
new_flex = '''// Panel map: 0=Documentation(flex), 1=Communication(flex)
var RIGHT_PANEL_FLEX = {0: true, 1: true};
document.addEventListener('DOMContentLoaded', function() { switchRightTab(0); });
function switchRightTab(idx) {
  document.querySelectorAll('.right-tab-btn').forEach(function(b, i) { b.classList.toggle('active', i === idx); });
  for (var i = 0; i < 2; i++) {'''
if old_flex in html:
    html = html.replace(old_flex, new_flex, 1)
    changes.append('A4: RIGHT_PANEL_FLEX = {0:true,1:true}, loop set to i<2')
else:
    changes.append('A4 MISS: RIGHT_PANEL_FLEX block not found')

with open(CHART, 'w', encoding='utf-8') as f:
    f.write(html)

print('Applied chart_ux_update_v1.md changes:')
for c in changes:
    icon = '❌' if 'MISS' in c else '✅'
    print(f'  {icon} {c}')

misses = [c for c in changes if 'MISS' in c]
print(f'\n{"All clear." if not misses else str(len(misses)) + " MISS(ES) — check manually."}')
