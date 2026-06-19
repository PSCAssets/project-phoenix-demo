#!/usr/bin/env python3
"""
Project Phoenix — Demo Update: Wizard New Steps + Linked Consultations Expansion
Adds Pre-Consult Checklist and QA Stage Setup as named sub-steps after Workflow Configuration.
Expands Linked Consultations step with consult link types and NIH ACMG81 config.

Files modified:
  templates/admin/wizard.html

Requirements covered:
  M04-CHK-001 — Pre-consult checklist config per care product/role
  M04-QA-001  — QA stage configuration per care product
  M04-NIH-001 — Research consult linkage config in care product wizard
"""

import os

BASE = '/Users/justin.woller/Documents/project-phoenix-demo'
wiz_path = os.path.join(BASE, 'templates', 'admin', 'wizard.html')

with open(wiz_path, 'r') as f:
    html = f.read()

changes = []

# ─────────────────────────────────────────────────────────────────────────────
# 1. Insert two new nav items after sni11 (Workflow Configuration)
# ─────────────────────────────────────────────────────────────────────────────
NAV_ANCHOR = '      <div class="step-nav-item" onclick="goToStep(12)" id="sni12"><div class="step-num">10</div><div class="step-name">SLA Configuration</div></div>'
NAV_INSERT = '''      <div class="step-nav-item" onclick="goToStep('preconsult_chk')" id="sni_preconsult_chk"><div class="step-num">&#9670;</div><div class="step-name">Pre-Consult Checklist</div></div>
      <div class="step-nav-item" onclick="goToStep('qa_stage')" id="sni_qa_stage"><div class="step-num">&#9670;</div><div class="step-name">QA Stage Setup</div></div>
'''

if 'sni_preconsult_chk' not in html:
    html = html.replace(NAV_ANCHOR, NAV_INSERT + NAV_ANCHOR)
    changes.append('Nav: inserted Pre-Consult Checklist and QA Stage Setup items')
else:
    changes.append('Nav: SKIP — already present')

# ─────────────────────────────────────────────────────────────────────────────
# 2. Insert two new step panels after step11 (Workflow Configuration panel)
# ─────────────────────────────────────────────────────────────────────────────
PANEL_ANCHOR = '      <!-- STEP 10: SLA Configuration -->'
PANEL_INSERT = '''
      <!-- Pre-Consult Checklist (named step — sub-step of Workflow Configuration) -->
      <div class="step-panel" id="step_preconsult_chk">
        <div class="step-heading">Pre-Consult Checklist Configuration</div>
        <div class="step-sub">Define mandatory pre-consult checklist items that care team members must complete before a consult enters the provider queue. Items are role-scoped and can be marked as required or advisory.</div>
        <div class="form-card" style="margin-bottom:16px;">
          <div class="form-card-title">Enable Pre-Consult Checklist</div>
          <div class="toggle-row" style="margin-bottom:12px;">
            <label class="toggle"><input type="checkbox" id="pcc_enabled" checked onchange="togglePcc()"><span class="toggle-slider"></span></label>
            <span class="toggle-label">Require checklist completion before consult advances to provider queue</span>
          </div>
        </div>
        <div id="pcc_config">
          <div class="form-card">
            <div class="form-card-title">Checklist Items</div>
            <table class="wiz-table">
              <thead><tr><th>Checklist Item</th><th>Role</th><th>Requirement</th><th></th></tr></thead>
              <tbody id="pccRows">
                <tr>
                  <td><input type="text" class="form-input" value="Patient identity confirmed" style="width:100%"></td>
                  <td>
                    <select class="form-input" style="width:100%">
                      <option>MA</option><option>PSR</option><option>RN</option><option>GCA</option><option>Any</option>
                    </select>
                  </td>
                  <td>
                    <select class="form-input" style="width:100%">
                      <option selected>Required</option><option>Advisory</option>
                    </select>
                  </td>
                  <td><button class="btn-sm" onclick="this.closest('tr').remove()">✕</button></td>
                </tr>
                <tr>
                  <td><input type="text" class="form-input" value="Insurance eligibility verified" style="width:100%"></td>
                  <td><select class="form-input" style="width:100%"><option>MA</option><option>PSR</option><option>RN</option><option>GCA</option><option selected>Any</option></select></td>
                  <td><select class="form-input" style="width:100%"><option selected>Required</option><option>Advisory</option></select></td>
                  <td><button class="btn-sm" onclick="this.closest('tr').remove()">✕</button></td>
                </tr>
                <tr>
                  <td><input type="text" class="form-input" value="Consent forms signed" style="width:100%"></td>
                  <td><select class="form-input" style="width:100%"><option>MA</option><option>PSR</option><option>RN</option><option selected>GCA</option><option>Any</option></select></td>
                  <td><select class="form-input" style="width:100%"><option selected>Required</option><option>Advisory</option></select></td>
                  <td><button class="btn-sm" onclick="this.closest('tr').remove()">✕</button></td>
                </tr>
                <tr>
                  <td><input type="text" class="form-input" value="Health profile complete" style="width:100%"></td>
                  <td><select class="form-input" style="width:100%"><option>MA</option><option>PSR</option><option>RN</option><option>GCA</option><option selected>Any</option></select></td>
                  <td><select class="form-input" style="width:100%"><option>Required</option><option selected>Advisory</option></select></td>
                  <td><button class="btn-sm" onclick="this.closest('tr').remove()">✕</button></td>
                </tr>
              </tbody>
            </table>
            <button class="btn-sm" style="margin-top:10px;" onclick="addPccRow()">+ Add item</button>
          </div>
          <div class="form-card">
            <div class="form-card-title">Blocking Behavior</div>
            <div class="form-group">
              <label class="form-label">When required items are incomplete</label>
              <div class="radio-group">
                <label class="radio-opt"><input type="radio" name="pcc_block" value="hard" checked> Hard block — consult cannot advance</label>
                <label class="radio-opt"><input type="radio" name="pcc_block" value="warn"> Soft warning — supervisor override allowed</label>
              </div>
            </div>
          </div>
          <div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:8px;padding:12px 16px;font-size:12px;color:#065F46;">
            <strong>M04-CHK-001</strong> — Pre-consult checklist completion will be tracked as a discrete workflow stage visible on the consult timeline.
          </div>
        </div>
      </div>

      <!-- QA Stage Setup (named step — sub-step of Workflow Configuration) -->
      <div class="step-panel" id="step_qa_stage">
        <div class="step-heading">QA Stage Setup</div>
        <div class="step-sub">Configure quality assurance review requirements for this care product. When enabled, a QA Reviewer must approve each consult before it proceeds to chart close. Consults that fail QA route to the GC Administrator queue for resolution.</div>
        <div class="form-card" style="margin-bottom:16px;">
          <div class="form-card-title">Enable QA Review Stage</div>
          <div class="toggle-row" style="margin-bottom:12px;">
            <label class="toggle"><input type="checkbox" id="qa_enabled" checked onchange="toggleQa()"><span class="toggle-slider"></span></label>
            <span class="toggle-label">Require QA approval before chart close for this care product</span>
          </div>
        </div>
        <div id="qa_config">
          <div class="form-card">
            <div class="form-card-title">QA Triggers — When is QA required?</div>
            <p style="font-size:12px;color:#6B7280;margin-bottom:12px;">Select the conditions that trigger mandatory QA review. At least one trigger is required when QA is enabled.</p>
            <div class="check-group" style="flex-direction:column;gap:8px;">
              <label class="check-opt"><input type="checkbox" checked> Minor patient (under 18)</label>
              <label class="check-opt"><input type="checkbox" checked> Third-party order (order placed by someone other than patient)</label>
              <label class="check-opt"><input type="checkbox" checked> POA / guardian documentation required</label>
              <label class="check-opt"><input type="checkbox"> First consult for this care product (all patients)</label>
              <label class="check-opt"><input type="checkbox"> Variant of uncertain significance (VUS) found in results</label>
              <label class="check-opt"><input type="checkbox"> Provider flagged for clinical escalation</label>
              <label class="check-opt"><input type="checkbox"> All consults (blanket QA)</label>
            </div>
          </div>
          <div class="form-card">
            <div class="form-card-title">QA Role Assignments</div>
            <table class="wiz-table">
              <thead><tr><th>Function</th><th>Assigned Role</th><th>SLA (hours)</th></tr></thead>
              <tbody>
                <tr>
                  <td>QA Reviewer — approve / reject</td>
                  <td><select class="form-input" style="width:100%"><option selected>QA Reviewer</option><option>GC Supervisor</option><option>Any Provider</option></select></td>
                  <td><input type="number" class="form-input" value="24" style="width:70px;"></td>
                </tr>
                <tr>
                  <td>QA Failure Resolution — GC Admin queue</td>
                  <td><select class="form-input" style="width:100%"><option selected>GC Administrator</option><option>Program Manager</option></select></td>
                  <td><input type="number" class="form-input" value="24" style="width:70px;"></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="form-card">
            <div class="form-card-title">Failure Routing</div>
            <div class="form-group">
              <label class="form-label">When a consult fails QA review</label>
              <div class="radio-group">
                <label class="radio-opt"><input type="radio" name="qa_fail" value="gc_admin" checked> Route to GC Administrator queue (override or return to GC)</label>
                <label class="radio-opt"><input type="radio" name="qa_fail" value="provider"> Return directly to assigned GC for correction</label>
              </div>
            </div>
          </div>
          <div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:8px;padding:12px 16px;font-size:12px;color:#065F46;">
            <strong>M04-QA-001</strong> — QA stage is automatically inserted into the workflow between "Counseling Plan" and "Chart Close" when enabled. All QA decisions are audit-logged to the consult timeline.
          </div>
        </div>
      </div>

'''

if 'step_preconsult_chk' not in html:
    html = html.replace(PANEL_ANCHOR, PANEL_INSERT + PANEL_ANCHOR)
    changes.append('Panels: inserted Pre-Consult Checklist and QA Stage Setup panels')
else:
    changes.append('Panels: SKIP — already present')

# ─────────────────────────────────────────────────────────────────────────────
# 3. Expand step18 (Linked Consultations) — add consult link types + NIH ACMG81
# ─────────────────────────────────────────────────────────────────────────────
OLD_STEP18_CONTENT = '''        <div class="step-heading">Step 18 — Linked Consultations</div>
        <div class="step-sub">Configure episode linking to track longitudinal patient care history within this product.</div>
        <div class="form-group">
          <label class="form-label">Enable Episode Reference ID</label>
          <div class="toggle-row">
            <label class="toggle"><input type="checkbox" id="s16_episode" checked onchange="toggleEpisode()"><span class="toggle-slider"></span></label>
            <span class="toggle-label">Group consultations under a shared Episode Reference ID</span>
          </div>
        </div>
        <div id="episode_config">
          <div style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:8px;padding:14px 16px;font-size:13px;color:#1E40AF;margin-bottom:16px;line-height:1.6;">
            All consultations for this care product will be grouped under an Episode Reference ID. This allows providers to view the full longitudinal history of a patient's care within this product.
          </div>
          <div class="form-group">
            <label class="form-label">Episode ID Format</label>
            <select class="form-input" style="max-width:320px">
              <option>Auto-generated (recommended)</option>
              <option>Manual entry</option>
              <option>Linked to Athena encounter</option>
            </select>
          </div>
        </div>'''

NEW_STEP18_CONTENT = '''        <div class="step-heading">Step 18 — Linked Consultations</div>
        <div class="step-sub">Configure how consultations link together for longitudinal care tracking — episode grouping, pre-test/post-test sequences, and research study enrollment.</div>

        <!-- Episode Reference ID -->
        <div class="form-card" style="margin-bottom:16px;">
          <div class="form-card-title">Episode Reference ID</div>
          <div class="toggle-row" style="margin-bottom:12px;">
            <label class="toggle"><input type="checkbox" id="s16_episode" checked onchange="toggleEpisode()"><span class="toggle-slider"></span></label>
            <span class="toggle-label">Group consultations under a shared Episode Reference ID</span>
          </div>
          <div id="episode_config">
            <div style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:8px;padding:12px 14px;font-size:12px;color:#1E40AF;margin-bottom:12px;line-height:1.6;">
              All consultations for this care product will be grouped under an Episode Reference ID, allowing providers to view the full longitudinal care history.
            </div>
            <div class="form-group">
              <label class="form-label">Episode ID Format</label>
              <select class="form-input" style="max-width:320px">
                <option>Auto-generated (recommended)</option>
                <option>Manual entry</option>
                <option>Linked to Athena encounter</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Consult Link Types -->
        <div class="form-card" style="margin-bottom:16px;">
          <div class="form-card-title">Consult Link Types</div>
          <p style="font-size:12px;color:#6B7280;margin-bottom:14px;">Define the types of consult relationships allowed for this care product. Linked consults are visible to providers in the chart's Linked Consults panel.</p>
          <table class="wiz-table">
            <thead><tr><th>Link Type</th><th>Enabled</th><th>Description</th><th>Auto-link rule</th></tr></thead>
            <tbody>
              <tr>
                <td style="font-weight:600;">Pre-Test → Post-Test</td>
                <td><label class="toggle"><input type="checkbox" checked><span class="toggle-slider"></span></label></td>
                <td style="font-size:12px;color:#6B7280;">Pre-test counseling session linked to post-test results disclosure</td>
                <td><select style="font-size:12px;border:1px solid #E5E0D8;border-radius:6px;padding:4px 8px;"><option>Auto (same episode)</option><option>Manual link only</option></select></td>
              </tr>
              <tr>
                <td style="font-weight:600;">Rescheduled</td>
                <td><label class="toggle"><input type="checkbox" checked><span class="toggle-slider"></span></label></td>
                <td style="font-size:12px;color:#6B7280;">Original consult linked to the rescheduled replacement</td>
                <td><select style="font-size:12px;border:1px solid #E5E0D8;border-radius:6px;padding:4px 8px;"><option>Auto (system-generated)</option><option>Manual link only</option></select></td>
              </tr>
              <tr>
                <td style="font-weight:600;">Research Companion</td>
                <td><label class="toggle"><input type="checkbox"><span class="toggle-slider"></span></label></td>
                <td style="font-size:12px;color:#6B7280;">Standard consult linked to a parallel research/blinded study consult</td>
                <td><select style="font-size:12px;border:1px solid #E5E0D8;border-radius:6px;padding:4px 8px;"><option>Manual link only</option><option>Auto (same episode)</option></select></td>
              </tr>
              <tr>
                <td style="font-weight:600;">Follow-Up</td>
                <td><label class="toggle"><input type="checkbox" checked><span class="toggle-slider"></span></label></td>
                <td style="font-size:12px;color:#6B7280;">Subsequent consult linked to an earlier consult for continuity</td>
                <td><select style="font-size:12px;border:1px solid #E5E0D8;border-radius:6px;padding:4px 8px;"><option>Auto (same episode)</option><option>Manual link only</option></select></td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- NIH ACMG81 Research Linkage -->
        <div class="form-card" style="margin-bottom:16px;">
          <div class="form-card-title">NIH ACMG81 Research Consult Linkage <span style="font-size:11px;font-weight:400;background:#EDE9FE;color:#5B21B6;padding:2px 8px;border-radius:4px;margin-left:8px;">M04-NIH-001</span></div>
          <div class="toggle-row" style="margin-bottom:14px;">
            <label class="toggle"><input type="checkbox" id="nihEnabled" onchange="toggleNih()"><span class="toggle-slider"></span></label>
            <span class="toggle-label">Enable NIH ACMG81 secondary findings research consult linkage</span>
          </div>
          <div id="nihConfig" style="display:none;">
            <div style="background:#FEF3C7;border:1px solid #FDE68A;border-radius:8px;padding:12px 14px;font-size:12px;color:#92400E;margin-bottom:14px;line-height:1.5;">
              <strong>ACMG81 secondary findings</strong> — When enabled, patients who consent to ACMG81 secondary findings reporting will have a companion research consult automatically created and linked to their primary consult. The companion consult is blinded and managed separately.
            </div>
            <div class="form-group">
              <label class="form-label">Patient consent capture</label>
              <div class="radio-group">
                <label class="radio-opt"><input type="radio" name="nihConsent" value="intake" checked> At intake — include ACMG81 consent in intake questionnaire</label>
                <label class="radio-opt"><input type="radio" name="nihConsent" value="presession"> Pre-session — capture consent in pre-consult checklist</label>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">Research consult creation</label>
              <div class="radio-group">
                <label class="radio-opt"><input type="radio" name="nihCreate" value="auto" checked> Auto-create companion consult on consent</label>
                <label class="radio-opt"><input type="radio" name="nihCreate" value="manual"> Manual — staff initiates companion consult</label>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">Blinding rules</label>
              <div class="check-group" style="flex-direction:column;gap:8px;">
                <label class="check-opt"><input type="checkbox" checked> Research consult hidden from patient portal</label>
                <label class="check-opt"><input type="checkbox" checked> Research consult hidden from standard provider view</label>
                <label class="check-opt"><input type="checkbox"> Research coordinator role required to access</label>
              </div>
            </div>
          </div>
        </div>'''

if 'Consult Link Types' not in html:
    html = html.replace(OLD_STEP18_CONTENT, NEW_STEP18_CONTENT)
    changes.append('step18: expanded with Consult Link Types and NIH ACMG81 config')
else:
    changes.append('step18: SKIP — already expanded')

# ─────────────────────────────────────────────────────────────────────────────
# 4. Add JS for new toggles
# ─────────────────────────────────────────────────────────────────────────────
JS_ANCHOR = 'function toggleEpisode()'
JS_INSERT = '''function togglePcc() {
  var enabled = document.getElementById('pcc_enabled').checked;
  document.getElementById('pcc_config').style.display = enabled ? '' : 'none';
}
function toggleQa() {
  var enabled = document.getElementById('qa_enabled').checked;
  document.getElementById('qa_config').style.display = enabled ? '' : 'none';
}
function addPccRow() {
  var tbody = document.getElementById('pccRows');
  var row = document.createElement('tr');
  row.innerHTML = '<td><input type="text" class="form-input" placeholder="Checklist item..." style="width:100%"></td><td><select class="form-input" style="width:100%"><option>MA</option><option>PSR</option><option>RN</option><option>GCA</option><option>Any</option></select></td><td><select class="form-input" style="width:100%"><option>Required</option><option>Advisory</option></select></td><td><button class="btn-sm" onclick="this.closest(\'tr\').remove()">✕</button></td>';
  tbody.appendChild(row);
}
function toggleNih() {
  var enabled = document.getElementById('nihEnabled').checked;
  document.getElementById('nihConfig').style.display = enabled ? '' : 'none';
}
'''

if 'togglePcc' not in html:
    html = html.replace(JS_ANCHOR, JS_INSERT + JS_ANCHOR)
    changes.append('JS: added togglePcc, toggleQa, addPccRow, toggleNih')
else:
    changes.append('JS: SKIP — already present')

# ─────────────────────────────────────────────────────────────────────────────
with open(wiz_path, 'w') as f:
    f.write(html)

print('\n── apply_wizard_new_steps_v1.py ──')
for c in changes:
    print('  ' + c)
print(f'\n  {len(changes)} operations complete.\n')
