#!/usr/bin/env python3
"""
Project Phoenix — Demo Update: Chart Right Panel New Tabs
Adds Clinical Resources tab and Linked Consults tab to the provider chart right panel.

Files modified:
  templates/provider/chart.html

Requirements covered:
  M02-CLB-001 — Clinical content library access from chart
  M02-LNK-001 — Linked consult view + prior note import
"""

import os

BASE = '/Users/justin.woller/Documents/project-phoenix-demo'
chart_path = os.path.join(BASE, 'templates', 'provider', 'chart.html')

with open(chart_path, 'r') as f:
    html = f.read()

changes = []

# ─────────────────────────────────────────────────────────────────────────────
# 1. Add two new tab buttons after Zendesk
# ─────────────────────────────────────────────────────────────────────────────
TAB_ANCHOR = '        <button class="right-tab-btn zendesk" onclick="switchRightTab(2)">🎫 Zendesk</button>'
TAB_INSERT = '''        <button class="right-tab-btn zendesk" onclick="switchRightTab(2)">🎫 Zendesk</button>
        <button class="right-tab-btn" onclick="switchRightTab(3)" style="color:#7C3AED;">📚 Clinical Resources</button>
        <button class="right-tab-btn" onclick="switchRightTab(4)" style="color:#0E7490;">🔗 Linked Consults</button>'''

if 'Clinical Resources' not in html:
    html = html.replace(TAB_ANCHOR, TAB_INSERT)
    changes.append('Tab bar: added Clinical Resources and Linked Consults buttons')
else:
    changes.append('Tab bar: SKIP — already present')

# ─────────────────────────────────────────────────────────────────────────────
# 2. Add Clinical Resources panel (rightPanel3) and Linked Consults panel (rightPanel4)
#    Insert before the Documentation panel (rightPanel0)
# ─────────────────────────────────────────────────────────────────────────────
PANEL_ANCHOR = '      <!-- Documentation -->'
PANEL_INSERT = '''      <!-- Clinical Resources panel — M02-CLB-001 -->
      <div class="right-panel" id="rightPanel3" style="padding:14px 16px;overflow-y:auto;display:none;flex-direction:column;gap:12px;">
        <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#6B7280;margin-bottom:4px;">📚 Clinical Resources</div>
        <div style="background:#F5F3FF;border:1px solid #DDD6FE;border-radius:8px;padding:12px 14px;font-size:12px;color:#5B21B6;margin-bottom:4px;">
          Published articles and blurbs from the Clinical Content Library relevant to this care product and diagnosis.
        </div>

        <div style="border:1.5px solid #E5E0D8;border-radius:8px;overflow:hidden;background:#fff;margin-bottom:4px;">
          <div style="padding:10px 14px;background:#F5F3FF;border-bottom:1px solid #E5E0D8;display:flex;align-items:center;gap:8px;">
            <span style="font-size:12px;font-weight:700;color:#5B21B6;flex:1;">BRCA1 — Patient Education Overview</span>
            <span style="font-size:10px;font-weight:700;background:#D1FAE5;color:#065F46;padding:2px 7px;border-radius:4px;">Published</span>
          </div>
          <div style="padding:10px 14px;font-size:12px;color:#374151;line-height:1.6;">
            BRCA1 is a tumor suppressor gene. A pathogenic variant significantly increases lifetime risk of breast and ovarian cancer. Surveillance and risk-reduction options are available.<br>
            <span style="font-size:11px;color:#9CA3AF;">Gene: BRCA1 · Inheritance: Autosomal dominant · NIH ACMG81 eligible</span>
          </div>
          <div style="padding:8px 14px;border-top:1px solid #E5E0D8;display:flex;gap:8px;">
            <button onclick="insertBlurb('BRCA1 Patient Education Overview')" style="padding:5px 14px;background:#6B21A8;color:#fff;border:none;border-radius:6px;font-size:11px;font-weight:600;cursor:pointer;">Insert into Letter</button>
            <button style="padding:5px 12px;border:1px solid #E5E0D8;border-radius:6px;font-size:11px;background:#fff;cursor:pointer;">View Full</button>
          </div>
        </div>

        <div style="border:1.5px solid #E5E0D8;border-radius:8px;overflow:hidden;background:#fff;margin-bottom:4px;">
          <div style="padding:10px 14px;background:#F5F3FF;border-bottom:1px solid #E5E0D8;display:flex;align-items:center;gap:8px;">
            <span style="font-size:12px;font-weight:700;color:#5B21B6;flex:1;">Lynch Syndrome — Surveillance Guide</span>
            <span style="font-size:10px;font-weight:700;background:#D1FAE5;color:#065F46;padding:2px 7px;border-radius:4px;">Published</span>
          </div>
          <div style="padding:10px 14px;font-size:12px;color:#374151;line-height:1.6;">
            Lynch syndrome is caused by variants in MMR genes (MLH1, MSH2, MSH6, PMS2). Carriers have elevated risk for colorectal, endometrial, and other cancers. Annual colonoscopy recommended from age 25.<br>
            <span style="font-size:11px;color:#9CA3AF;">Gene: MLH1, MSH2, MSH6 · NIH ACMG81 eligible</span>
          </div>
          <div style="padding:8px 14px;border-top:1px solid #E5E0D8;display:flex;gap:8px;">
            <button onclick="insertBlurb('Lynch Syndrome Surveillance Guide')" style="padding:5px 14px;background:#6B21A8;color:#fff;border:none;border-radius:6px;font-size:11px;font-weight:600;cursor:pointer;">Insert into Letter</button>
            <button style="padding:5px 12px;border:1px solid #E5E0D8;border-radius:6px;font-size:11px;background:#fff;cursor:pointer;">View Full</button>
          </div>
        </div>

        <div style="border:1.5px solid #FDE68A;border-radius:8px;overflow:hidden;background:#fff;margin-bottom:4px;">
          <div style="padding:10px 14px;background:#FEF9EE;border-bottom:1px solid #FDE68A;display:flex;align-items:center;gap:8px;">
            <span style="font-size:12px;font-weight:700;color:#92400E;flex:1;">BRCA2 Splice Variant — Patient Summary</span>
            <span style="font-size:10px;font-weight:700;background:#FEF3C7;color:#92400E;padding:2px 7px;border-radius:4px;">Pending Publish</span>
          </div>
          <div style="padding:10px 14px;font-size:12px;color:#374151;line-height:1.6;">
            This article is pending review by the GC Administrator before it becomes available for use in patient letters.
          </div>
          <div style="padding:8px 14px;border-top:1px solid #FDE68A;display:flex;gap:8px;">
            <button disabled style="padding:5px 14px;background:#9CA3AF;color:#fff;border:none;border-radius:6px;font-size:11px;font-weight:600;cursor:not-allowed;">Insert into Letter</button>
          </div>
        </div>

        <div style="margin-top:4px;">
          <button onclick="requestBlurb()" style="width:100%;padding:9px;border:1.5px dashed #DDD6FE;border-radius:8px;background:#F5F3FF;color:#6B21A8;font-size:12px;font-weight:600;cursor:pointer;">
            + Request New Clinical Content (Blurb Request)
          </button>
        </div>
      </div>

      <!-- Linked Consults panel — M02-LNK-001 -->
      <div class="right-panel" id="rightPanel4" style="padding:14px 16px;overflow-y:auto;display:none;flex-direction:column;gap:12px;">
        <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#6B7280;margin-bottom:4px;">🔗 Linked Consults</div>
        <div style="background:#CFFAFE;border:1px solid #A5F3FC;border-radius:8px;padding:10px 14px;font-size:12px;color:#164E63;margin-bottom:4px;">
          Episode ID: <strong>EP-2026-00849</strong> · 2 linked consults in this episode
        </div>

        <!-- Pre-Test linked consult -->
        <div style="border:1.5px solid #E5E0D8;border-radius:8px;overflow:hidden;background:#fff;margin-bottom:4px;">
          <div style="padding:10px 14px;background:#F0FDF4;border-bottom:1px solid #E5E0D8;display:flex;align-items:center;gap:8px;">
            <span style="font-size:10px;font-weight:700;background:#D1FAE5;color:#065F46;padding:2px 7px;border-radius:4px;">Pre-Test</span>
            <span style="font-size:12px;font-weight:700;color:#111827;flex:1;">CST-2026-11003</span>
            <span style="font-size:11px;color:#059669;font-weight:600;">Closed</span>
          </div>
          <div style="padding:10px 14px;font-size:12px;color:#374151;">
            <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:8px;">
              <span><span style="color:#9CA3AF;font-size:11px;">Provider</span><br>Taylor Brooks, GC</span>
              <span><span style="color:#9CA3AF;font-size:11px;">Date</span><br>May 14, 2026</span>
              <span><span style="color:#9CA3AF;font-size:11px;">Care Product</span><br>BRCA Hereditary Cancer</span>
            </div>
            <div style="font-size:11px;color:#6B7280;background:#F9F5EE;border-radius:6px;padding:8px 10px;line-height:1.5;">
              <strong>Note excerpt:</strong> Patient presents with significant family history of breast cancer (mother: BRCA2+, maternal aunt: BRCA1+). Pre-test counseling completed. Patient understands implications of testing. Consent obtained for ACMG81 secondary findings.
            </div>
          </div>
          <div style="padding:8px 14px;border-top:1px solid #E5E0D8;display:flex;gap:8px;">
            <button onclick="importPriorNote('CST-2026-11003')" style="padding:5px 14px;background:#0E7490;color:#fff;border:none;border-radius:6px;font-size:11px;font-weight:600;cursor:pointer;">Import Note into Current</button>
            <button style="padding:5px 12px;border:1px solid #E5E0D8;border-radius:6px;font-size:11px;background:#fff;cursor:pointer;">View Full Chart</button>
          </div>
        </div>

        <!-- Current consult indicator -->
        <div style="border:2px solid #6B21A8;border-radius:8px;overflow:hidden;background:#F5F3FF;margin-bottom:4px;">
          <div style="padding:10px 14px;border-bottom:1px solid #DDD6FE;display:flex;align-items:center;gap:8px;">
            <span style="font-size:10px;font-weight:700;background:#EDE9FE;color:#5B21B6;padding:2px 7px;border-radius:4px;">Post-Test</span>
            <span style="font-size:12px;font-weight:700;color:#6B21A8;flex:1;">CST-2026-10849 (current)</span>
            <span style="font-size:11px;color:#D97706;font-weight:600;">In Progress</span>
          </div>
          <div style="padding:10px 14px;font-size:12px;color:#5B21B6;">
            This is the currently open consult.
          </div>
        </div>

        <div style="margin-top:4px;">
          <button onclick="linkConsult()" style="width:100%;padding:9px;border:1.5px dashed #CBD5E1;border-radius:8px;background:#F9FAFB;color:#6B7280;font-size:12px;font-weight:600;cursor:pointer;">
            + Link another consult to this episode
          </button>
        </div>
      </div>

      <!-- Documentation -->'''

if 'rightPanel3' not in html:
    html = html.replace(PANEL_ANCHOR, PANEL_INSERT)
    changes.append('Panels: added rightPanel3 (Clinical Resources) and rightPanel4 (Linked Consults)')
else:
    changes.append('Panels: SKIP — already present')

# ─────────────────────────────────────────────────────────────────────────────
# 3. Update switchRightTab JS to handle panels 3 and 4
# ─────────────────────────────────────────────────────────────────────────────
OLD_SWITCH = '// Panel map: 0=Documentation(flex), 1=Communication(flex), 2=Zendesk(flex)'
NEW_SWITCH = '// Panel map: 0=Documentation(flex), 1=Communication(flex), 2=Zendesk(flex), 3=ClinicalResources(flex), 4=LinkedConsults(flex)'

if '3=ClinicalResources' not in html:
    html = html.replace(OLD_SWITCH, NEW_SWITCH)
    changes.append('switchRightTab: updated panel map comment')

# Also update the function that hides panels — look for the panel hiding loop
OLD_PANEL_LOOP = "for (let i = 0; i < 3; i++) {"
NEW_PANEL_LOOP = "for (let i = 0; i < 5; i++) {"

if NEW_PANEL_LOOP not in html:
    html = html.replace(OLD_PANEL_LOOP, NEW_PANEL_LOOP, 1)
    changes.append('switchRightTab: updated loop to cover 5 panels')
else:
    changes.append('switchRightTab: SKIP — already updated')

# ─────────────────────────────────────────────────────────────────────────────
# 4. Add JS helper functions for new tabs
# ─────────────────────────────────────────────────────────────────────────────
JS_ANCHOR = 'function addNoteToZendesk()'
JS_INSERT = '''function insertBlurb(title) {
  alert('✓ Inserting clinical resource into patient letter draft:\\n\\n"' + title + '"\\n\\nContent will appear in the Documentation tab under Patient Letter.');
}
function requestBlurb() {
  alert('Blurb Request submitted to GC Administrator queue.\\nExpected response: within 24 hours (SLA: M08-BLB-002).');
}
function importPriorNote(consultId) {
  alert('Importing counseling notes from ' + consultId + ' into current consult.\\n\\nNote content will appear in the Documentation tab as an imported section, clearly attributed to the prior consult date.');
}
function linkConsult() {
  var id = prompt('Enter consult ID to link to this episode (e.g., CST-2026-10722):');
  if (id) alert('Consult ' + id + ' linked to Episode EP-2026-00849.\\nLink type: Follow-Up');
}

'''

if 'insertBlurb' not in html:
    html = html.replace(JS_ANCHOR, JS_INSERT + JS_ANCHOR)
    changes.append('JS: added insertBlurb, requestBlurb, importPriorNote, linkConsult')
else:
    changes.append('JS: SKIP — already present')

# ─────────────────────────────────────────────────────────────────────────────
with open(chart_path, 'w') as f:
    f.write(html)

print('\n── apply_chart_new_tabs_v1.py ──')
for c in changes:
    print('  ' + c)
print(f'\n  {len(changes)} operations complete.\n')
