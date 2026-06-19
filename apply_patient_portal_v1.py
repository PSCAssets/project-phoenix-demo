#!/usr/bin/env python3
"""Apply patient_portal_demo_v1.md Change 3 — Wizard updates.
   Files 1/2/4 already handled via Write/Edit tools (new templates, app.py, index.html, qa_check.py).
   This script handles wizard.html: 2 new steps + Portal Branding enhancement.
"""

WIZARD = '/Users/justin.woller/Documents/project-phoenix-demo/templates/admin/wizard.html'

with open(WIZARD, 'r', encoding='utf-8') as f:
    html = f.read()

changes = []

# ──────────────────────────────────────────────────────────────
# 3a — Add Ecosystem Classification + Provider Eligibility to sidebar nav
# ──────────────────────────────────────────────────────────────

old_nav = '''      <div class="step-nav-item" onclick="goToStep('branding')" id="sni_branding"><div class="step-num">★</div><div class="step-name">Portal Branding</div></div>
      <div class="step-nav-item" onclick="goToStep(2)" id="sni2">'''
new_nav = '''      <div class="step-nav-item" onclick="goToStep('branding')" id="sni_branding"><div class="step-num">★</div><div class="step-name">Portal Branding</div></div>
      <div class="step-nav-item" onclick="goToStep('ecosystem')" id="sni_ecosystem"><div class="step-num">&#9670;</div><div class="step-name">Ecosystem</div></div>
      <div class="step-nav-item" onclick="goToStep(2)" id="sni2">'''
if old_nav in html:
    html = html.replace(old_nav, new_nav, 1)
    changes.append('3a: Ecosystem Classification nav item added after Portal Branding')
else:
    changes.append('3a MISS: portal branding nav anchor not found')

old_nav3 = '''      <div class="step-nav-item" onclick="goToStep(3)" id="sni3"><div class="step-num">2</div><div class="step-name">Provider Type</div></div>
      <div class="step-nav-item" onclick="goToStep(4)" id="sni4">'''
new_nav3 = '''      <div class="step-nav-item" onclick="goToStep(3)" id="sni3"><div class="step-num">2</div><div class="step-name">Provider Type</div></div>
      <div class="step-nav-item" onclick="goToStep('eligibility')" id="sni_eligibility"><div class="step-num">&#9670;</div><div class="step-name">Provider Eligibility</div></div>
      <div class="step-nav-item" onclick="goToStep(4)" id="sni4">'''
if old_nav3 in html:
    html = html.replace(old_nav3, new_nav3, 1)
    changes.append('3a: Provider Eligibility nav item added after Provider Type')
else:
    changes.append('3a MISS: provider type nav anchor not found')

# ──────────────────────────────────────────────────────────────
# 3b — Add Ecosystem Classification step panel (between step_branding and step2)
# ──────────────────────────────────────────────────────────────

ECOSYSTEM_PANEL = '''
      <!-- STEP: Ecosystem Classification -->
      <div class="step-panel" id="step_ecosystem">
        <div class="step-heading">Ecosystem Classification</div>
        <div class="step-sub">Configure how this care product's patient portal is managed. This setting cannot be changed once patients are enrolled.</div>

        <div style="display:flex;flex-direction:column;gap:12px;max-width:560px;margin-bottom:20px;">

          <div id="ecoCard0" onclick="selectEcoCard(0)" style="border:1px solid #E5E7EB;border-radius:8px;padding:16px;background:#fff;cursor:pointer;display:flex;align-items:flex-start;gap:14px;transition:border 0.15s;">
            <div style="margin-top:2px;width:18px;height:18px;border:2px solid #D1D5DB;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;" id="ecoRadio0"></div>
            <div>
              <div style="font-size:14px;font-weight:700;color:#374151;margin-bottom:4px;">Everlywell Platform</div>
              <div style="font-size:12px;color:#6B7280;line-height:1.5;">Patient portal is under the Everlywell umbrella. Patients can access multiple programs via the program switcher. Everlywell or client co-branding applies.</div>
            </div>
          </div>

          <div id="ecoCard1" onclick="selectEcoCard(1)" style="border:2px solid #6B21A8;border-radius:8px;padding:16px;background:#FAFAF9;cursor:pointer;display:flex;align-items:flex-start;gap:14px;transition:border 0.15s;">
            <div style="margin-top:2px;width:18px;height:18px;border:2px solid #6B21A8;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;" id="ecoRadio1">
              <div style="width:8px;height:8px;background:#6B21A8;border-radius:50%;"></div>
            </div>
            <div>
              <div style="font-size:14px;font-weight:700;color:#374151;margin-bottom:4px;">Isolated Partner <span style="font-size:11px;background:#EDE9FE;color:#6B21A8;padding:2px 7px;border-radius:8px;font-weight:600;margin-left:6px;">Selected</span></div>
              <div style="font-size:12px;color:#6B7280;line-height:1.5;">Patient portal is completely isolated. Partner branding only — no Everlywell references. Patient data is hard-isolated from the Everlywell ecosystem. Required for white-label contracts.</div>
            </div>
          </div>
        </div>

        <div style="background:#FEF3C7;border:1px solid #FCD34D;border-radius:6px;padding:12px 14px;max-width:560px;font-size:12px;color:#92400E;line-height:1.5;">
          <strong>&#9888; Important:</strong> This setting cannot be changed once the first patient account is created under this care product.
        </div>
      </div>

'''

if '      <!-- STEP 2: Basic Info -->' in html:
    html = html.replace('      <!-- STEP 2: Basic Info -->', ECOSYSTEM_PANEL + '      <!-- STEP 2: Basic Info -->', 1)
    changes.append('3b: Ecosystem Classification step panel inserted before Step 2')
else:
    changes.append('3b MISS: Step 2 comment anchor not found')

# ──────────────────────────────────────────────────────────────
# 3c — Add Provider Eligibility step panel (after step3, before step4)
# ──────────────────────────────────────────────────────────────

ELIGIBILITY_PANEL = '''
      <!-- STEP: Provider Eligibility -->
      <div class="step-panel" id="step_eligibility">
        <div class="step-heading">Provider Eligibility Configuration</div>
        <div class="step-sub">Define which providers are eligible to deliver this care product and configure program-type-specific assignment rules.</div>

        <div class="form-group" style="max-width:480px;">
          <label class="form-label">Program Type <span class="req">*</span></label>
          <div class="radio-group">
            <label class="radio-opt"><input type="radio" name="progType" value="commercial" checked onchange="onProgTypeChange(this.value)"> Commercial <span style="font-size:11px;color:#9CA3AF;">(default — all licensed providers eligible)</span></label>
            <label class="radio-opt"><input type="radio" name="progType" value="medicare" onchange="onProgTypeChange(this.value)"> Medicare Program</label>
            <label class="radio-opt"><input type="radio" name="progType" value="medicaid" onchange="onProgTypeChange(this.value)"> Medicaid Program</label>
          </div>
        </div>

        <!-- Medicare/Medicaid assignment table (hidden for Commercial) -->
        <div id="providerAssignmentSection" style="display:none;margin-bottom:24px;">
          <div style="height:1px;background:#E5E7EB;margin:16px 0;"></div>
          <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#9CA3AF;margin-bottom:10px;" id="assignmentSectionLabel">Medicare Program — Provider Assignment</div>
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
            <div style="font-size:13px;font-weight:600;color:#374151;">Assigned Providers</div>
            <button style="font-size:12px;font-weight:600;color:#6B21A8;background:#F5F3FF;border:1px solid #DDD6FE;border-radius:6px;padding:5px 12px;cursor:pointer;">+ Add Provider</button>
          </div>
          <div style="border:1px solid #E5E7EB;border-radius:8px;overflow:hidden;">
            <div style="padding:14px 16px;border-bottom:1px solid #E5E7EB;background:#FAFAFA;display:flex;align-items:flex-start;justify-content:space-between;">
              <div>
                <div style="font-size:13px;font-weight:700;color:#111827;margin-bottom:3px;">Dr. Sarah Lee</div>
                <div style="font-size:12px;color:#6B7280;margin-bottom:3px;">NPI: 1234567890</div>
                <div style="font-size:12px;color:#6B7280;margin-bottom:5px;">Licensed States: CA, TX, FL, NY, CO</div>
                <span style="font-size:11px;font-weight:600;background:#D1FAE5;color:#065F46;padding:2px 8px;border-radius:8px;">&#9679; Medicare Active &mdash; exp. 12/31/2027</span>
              </div>
              <button style="font-size:16px;color:#9CA3AF;background:none;border:none;cursor:pointer;padding:0 4px;" title="Remove">&times;</button>
            </div>
            <div style="padding:14px 16px;display:flex;align-items:flex-start;justify-content:space-between;">
              <div>
                <div style="font-size:13px;font-weight:700;color:#111827;margin-bottom:3px;">Dr. Marcus Webb</div>
                <div style="font-size:12px;color:#6B7280;margin-bottom:3px;">NPI: 0987654321</div>
                <div style="font-size:12px;color:#6B7280;margin-bottom:5px;">Licensed States: CA, TX, AZ, NV</div>
                <span style="font-size:11px;font-weight:600;background:#D1FAE5;color:#065F46;padding:2px 8px;border-radius:8px;">&#9679; Medicare Active &mdash; exp. 06/30/2027</span>
              </div>
              <button style="font-size:16px;color:#9CA3AF;background:none;border:none;cursor:pointer;padding:0 4px;" title="Remove">&times;</button>
            </div>
          </div>
        </div>

        <!-- Exclusion list (shown only for Commercial) -->
        <div id="exclusionSection">
          <div style="height:1px;background:#E5E7EB;margin:16px 0;"></div>
          <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#9CA3AF;margin-bottom:10px;">Exclusion List</div>
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
            <div style="font-size:13px;color:#374151;">Providers excluded from this care product</div>
            <button style="font-size:12px;font-weight:600;color:#6B7280;background:#F3F4F6;border:1px solid #E5E7EB;border-radius:6px;padding:5px 12px;cursor:pointer;">+ Add Exclusion</button>
          </div>
          <div style="border:1px solid #E5E7EB;border-radius:8px;padding:14px 16px;font-size:12px;color:#9CA3AF;font-style:italic;">
            No exclusions. All licensed providers are eligible by default.
          </div>
        </div>
      </div>

'''

if '      <!-- STEP 3: State Configuration -->' in html:
    html = html.replace('      <!-- STEP 3: State Configuration -->', ELIGIBILITY_PANEL + '      <!-- STEP 3: State Configuration -->', 1)
    changes.append('3c: Provider Eligibility step panel inserted before Step 4')
else:
    changes.append('3c MISS: Step 3 State Configuration comment anchor not found')

# ──────────────────────────────────────────────────────────────
# 3d — Enhance Portal Branding step with color pickers + live preview
# ──────────────────────────────────────────────────────────────

# Insert enhanced color picker + live preview before the closing </div> of step_branding
# The closing tag is: "        </div>\n      </div>\n\n      <!-- STEP 2: Basic Info -->"
# But step_ecosystem panel was already inserted. So now the anchor changes.
# Instead, look for the clientBrandFields closing and step_branding closing.

BRANDING_ENHANCEMENT = '''
        <div style="margin-top:20px;">
          <div style="font-size:13px;font-weight:700;color:#374151;margin-bottom:14px;">Color Configuration</div>
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;max-width:580px;margin-bottom:16px;">
            <div>
              <label class="form-label">Primary Color</label>
              <div style="display:flex;align-items:center;gap:8px;">
                <input type="color" id="brandPrimary" value="#0A2F5C" style="width:40px;height:36px;padding:2px;border:1px solid #E5E7EB;border-radius:6px;cursor:pointer;" oninput="updateBrandPreview()">
                <input type="text" value="#0A2F5C" id="brandPrimaryHex" style="width:80px;border:1px solid #E5E7EB;border-radius:6px;padding:5px 8px;font-size:12px;font-family:monospace;" oninput="syncColorPicker('brandPrimary','brandPrimaryHex')">
              </div>
            </div>
            <div>
              <label class="form-label">Secondary Color</label>
              <div style="display:flex;align-items:center;gap:8px;">
                <input type="color" id="brandSecondary" value="#00BFB3" style="width:40px;height:36px;padding:2px;border:1px solid #E5E7EB;border-radius:6px;cursor:pointer;" oninput="updateBrandPreview()">
                <input type="text" value="#00BFB3" id="brandSecondaryHex" style="width:80px;border:1px solid #E5E7EB;border-radius:6px;padding:5px 8px;font-size:12px;font-family:monospace;" oninput="syncColorPicker('brandSecondary','brandSecondaryHex')">
              </div>
            </div>
            <div>
              <label class="form-label">Header Background</label>
              <div style="display:flex;align-items:center;gap:8px;">
                <input type="color" id="brandHeader" value="#0A2F5C" style="width:40px;height:36px;padding:2px;border:1px solid #E5E7EB;border-radius:6px;cursor:pointer;" oninput="updateBrandPreview()">
                <input type="text" value="#0A2F5C" id="brandHeaderHex" style="width:80px;border:1px solid #E5E7EB;border-radius:6px;padding:5px 8px;font-size:12px;font-family:monospace;" oninput="syncColorPicker('brandHeader','brandHeaderHex')">
              </div>
            </div>
          </div>

          <div style="font-size:13px;font-weight:700;color:#374151;margin-bottom:8px;">Live Preview</div>
          <div id="brandLivePreview" style="border:1px solid #E5E7EB;border-radius:8px;overflow:hidden;max-width:540px;">
            <div id="previewHeader" style="background:#0A2F5C;color:#fff;padding:10px 16px;display:flex;align-items:center;justify-content:space-between;font-size:13px;">
              <div style="display:flex;align-items:center;gap:6px;">
                <span id="previewIcon" style="color:#00BFB3;font-size:16px;">&#9672;</span>
                <span id="previewBrandName" style="font-weight:700;">PWN Health</span>
              </div>
              <span style="color:rgba(255,255,255,0.7);font-size:12px;">Patient Portal</span>
              <span style="color:rgba(255,255,255,0.8);font-size:12px;">J. Adams &#8599;</span>
            </div>
          </div>
          <div style="font-size:11px;color:#9CA3AF;margin-top:6px;">Preview updates as you adjust colors above.</div>
          <div style="margin-top:10px;background:#FEF3C7;border-radius:6px;padding:10px 12px;font-size:12px;color:#92400E;max-width:540px;">For Isolated Partner ecosystems, logo and primary color are required before this care product can be published.</div>
        </div>
'''

BRANDING_CLOSE_ANCHOR = '''        </div>
      </div>

      <!-- STEP: Ecosystem Classification -->'''

if BRANDING_CLOSE_ANCHOR in html:
    html = html.replace(BRANDING_CLOSE_ANCHOR,
        BRANDING_ENHANCEMENT + '\n      </div>\n\n      <!-- STEP: Ecosystem Classification -->', 1)
    changes.append('3d: Color pickers + live preview added to Portal Branding step')
else:
    changes.append('3d MISS: Portal Branding closing anchor not found')

# ──────────────────────────────────────────────────────────────
# 3e — Add JS for new wizard steps (onProgTypeChange, selectEcoCard, brand preview)
# ──────────────────────────────────────────────────────────────

NEW_WIZ_JS = '''
// Ecosystem Classification card selection
var _ecoSelected = 1;
function selectEcoCard(idx) {
  _ecoSelected = idx;
  [0,1].forEach(function(i) {
    var card = document.getElementById('ecoCard' + i);
    var radio = document.getElementById('ecoRadio' + i);
    if (i === idx) {
      card.style.border = '2px solid #6B21A8';
      card.style.background = '#FAFAF9';
      radio.innerHTML = '<div style="width:8px;height:8px;background:#6B21A8;border-radius:50%;"></div>';
      radio.style.border = '2px solid #6B21A8';
    } else {
      card.style.border = '1px solid #E5E7EB';
      card.style.background = '#fff';
      radio.innerHTML = '';
      radio.style.border = '2px solid #D1D5DB';
    }
  });
}

// Provider Eligibility program type toggle
function onProgTypeChange(val) {
  var assignSection = document.getElementById('providerAssignmentSection');
  var exclSection = document.getElementById('exclusionSection');
  var label = document.getElementById('assignmentSectionLabel');
  if (val === 'commercial') {
    if (assignSection) assignSection.style.display = 'none';
    if (exclSection)   exclSection.style.display = '';
  } else {
    if (assignSection) { assignSection.style.display = ''; }
    if (label) label.textContent = (val === 'medicare' ? 'Medicare' : 'Medicaid') + ' Program — Provider Assignment';
    if (exclSection)   exclSection.style.display = 'none';
  }
}

// Portal Branding live preview
function updateBrandPreview() {
  var hdr = document.getElementById('previewHeader');
  var icon = document.getElementById('previewIcon');
  var primary = document.getElementById('brandPrimary');
  var secondary = document.getElementById('brandSecondary');
  var headerBg = document.getElementById('brandHeader');
  if (!hdr) return;
  hdr.style.background = headerBg ? headerBg.value : '#0A2F5C';
  if (icon && secondary) icon.style.color = secondary.value;
  // Update hex fields
  if (primary) { var phx = document.getElementById('brandPrimaryHex'); if (phx) phx.value = primary.value; }
  if (secondary) { var shx = document.getElementById('brandSecondaryHex'); if (shx) shx.value = secondary.value; }
  if (headerBg) { var hhx = document.getElementById('brandHeaderHex'); if (hhx) hhx.value = headerBg.value; }
}
function syncColorPicker(pickerId, hexId) {
  var hex = document.getElementById(hexId);
  var picker = document.getElementById(pickerId);
  if (!hex || !picker) return;
  var val = hex.value.trim();
  if (/^#[0-9A-Fa-f]{6}$/.test(val)) { picker.value = val; updateBrandPreview(); }
}
'''

# Insert before the closing </script> of the main raw block
if 'function selectEcoCard' not in html:
    html = html.replace('// Init\ngoToStep(1);', NEW_WIZ_JS + '\n// Init\ngoToStep(1);', 1)
    changes.append('3e: selectEcoCard, onProgTypeChange, updateBrandPreview JS added to wizard')
else:
    changes.append('3e: wizard JS already present — skipped')

with open(WIZARD, 'w', encoding='utf-8') as f:
    f.write(html)

print('Applied patient_portal_demo_v1.md wizard changes:')
for c in changes:
    icon = '❌' if 'MISS' in c else '✅'
    print(f'  {icon} {c}')

misses = [c for c in changes if 'MISS' in c]
print(f'\n{"All clear." if not misses else str(len(misses)) + " MISS(ES) — check manually."}')
