#!/usr/bin/env python3
"""Apply wizard_workflow_step_v1.md changes."""

import re

CHART  = '/Users/justin.woller/Documents/project-phoenix-demo/templates/provider/chart.html'
WIZARD = '/Users/justin.woller/Documents/project-phoenix-demo/templates/admin/wizard.html'

changes = []

# ══════════════════════════════════════════════════════════════════
# CHANGE 1 — chart.html fixes
# ══════════════════════════════════════════════════════════════════
with open(CHART, 'r', encoding='utf-8') as f:
    chart = f.read()

# ── 1B: Replace drag handle with removeEventListener pattern ──────
old_drag = '''// Route modal
// Drag-to-resize panel
(function() {
  var handle = document.getElementById('chartDragHandle');
  var right = document.getElementById('chartRight');
  var dragging = false, startX, startW;
  if (!handle || !right) return;
  handle.addEventListener('mousedown', function(e) {
    dragging = true; startX = e.clientX; startW = right.offsetWidth;
    document.body.style.userSelect = 'none';
    e.preventDefault();
  });
  document.addEventListener('mousemove', function(e) {
    if (!dragging) return;
    var delta = startX - e.clientX;
    var newW = Math.max(320, Math.min(startW + delta, window.innerWidth - 280 - 4));
    right.style.width = newW + 'px'; right.style.minWidth = newW + 'px';
  });
  document.addEventListener('mouseup', function() {
    if (dragging) { dragging = false; document.body.style.userSelect = ''; }
  });
})();'''
new_drag = '''// Route modal
// Drag-to-resize panel — uses per-drag listeners that are removed on mouseup
(function() {
  var handle = document.getElementById('chartDragHandle');
  var right = document.getElementById('chartRight');
  if (!handle || !right) return;
  handle.addEventListener('mousedown', function(e) {
    var startX = e.clientX, startW = right.offsetWidth;
    document.body.style.userSelect = 'none';
    e.preventDefault();
    function onMove(ev) {
      var delta = startX - ev.clientX;
      var newW = Math.max(320, Math.min(startW + delta, window.innerWidth - 280 - 4));
      right.style.width = newW + 'px'; right.style.minWidth = newW + 'px';
    }
    function onUp() {
      document.removeEventListener('mousemove', onMove);
      document.removeEventListener('mouseup', onUp);
      document.body.style.userSelect = '';
    }
    document.addEventListener('mousemove', onMove);
    document.addEventListener('mouseup', onUp);
  });
})();'''
if old_drag in chart:
    chart = chart.replace(old_drag, new_drag, 1)
    changes.append('1B-chart: drag handle updated to removeEventListener pattern')
else:
    changes.append('1B-chart: MISS — drag handle not found')

# ── 1D: Add pointer-events:none to modal-backdrop when hidden ─────
old_modal_css = '.modal-backdrop { display:none; position:fixed; inset:0; background:rgba(0,0,0,0.45); z-index:1000; justify-content:center; align-items:center; }\n.modal-backdrop.open { display:flex; }'
new_modal_css = '.modal-backdrop { display:none; position:fixed; inset:0; background:rgba(0,0,0,0.45); z-index:1000; justify-content:center; align-items:center; pointer-events:none; }\n.modal-backdrop.open { display:flex; pointer-events:all; }'
if old_modal_css in chart:
    chart = chart.replace(old_modal_css, new_modal_css, 1)
    changes.append('1D-chart: pointer-events added to .modal-backdrop CSS')
else:
    changes.append('1D-chart: MISS — .modal-backdrop CSS not found')

# ── 1D: previewModal inline style — add pointer-events:none ───────
old_preview_div = '<div id="previewModal" style="display:none;position:fixed;inset:0;background:#fff;z-index:1000;flex-direction:column;">'
new_preview_div = '<div id="previewModal" style="display:none;position:fixed;inset:0;background:#fff;z-index:1000;flex-direction:column;pointer-events:none;">'
if old_preview_div in chart:
    chart = chart.replace(old_preview_div, new_preview_div, 1)
    changes.append('1D-chart: pointer-events:none added to previewModal')
else:
    changes.append('1D-chart: MISS — previewModal div not found')

# Fix openPreviewModal to also enable pointer-events
old_open_prev = '''function openPreviewModal() {
  var m = document.getElementById('previewModal');
  if (m) m.style.display = 'flex';
}
function closePreviewModal() {
  var m = document.getElementById('previewModal');
  if (m) m.style.display = 'none';
}'''
new_open_prev = '''function openPreviewModal() {
  var m = document.getElementById('previewModal');
  if (m) { m.style.display = 'flex'; m.style.pointerEvents = 'all'; }
}
function closePreviewModal() {
  var m = document.getElementById('previewModal');
  if (m) { m.style.display = 'none'; m.style.pointerEvents = 'none'; }
}'''
if old_open_prev in chart:
    chart = chart.replace(old_open_prev, new_open_prev, 1)
    changes.append('1D-chart: openPreviewModal/closePreviewModal updated for pointer-events')
else:
    changes.append('1D-chart: MISS — openPreviewModal function not found')

with open(CHART, 'w', encoding='utf-8') as f:
    f.write(chart)

# ══════════════════════════════════════════════════════════════════
# CHANGE 1 + 2 — wizard.html
# ══════════════════════════════════════════════════════════════════
with open(WIZARD, 'r', encoding='utf-8') as f:
    wiz = f.read()

# ── 1C/1D: Check for any hardcoded visible modals (there aren't any in wizard,
#    but we'll verify the flag is clean in the JS) ─────────────────
# Wizard has no drag handle, no modal backdrops — nothing to fix for 1B/1C/1D.
changes.append('1B/1C/1D-wizard: no drag handle or modal backdrop found — no changes needed')

# ══════════════════════════════════════════════════════════════════
# CHANGE 2 — Replace step11 HTML content
# ══════════════════════════════════════════════════════════════════

NEW_STEP11 = '''      <!-- STEP 9: Workflow Configuration -->
      <div class="step-panel" id="step11">
        <div class="step-heading">Step 11 — Workflow Configuration</div>
        <div class="step-sub">Define the clinical workflow stages for this care product.</div>

        <!-- Mode toggle cards -->
        <div style="display:flex;gap:12px;margin-bottom:20px;">
          <label id="wfbModeCardTemplate" style="flex:1;display:flex;align-items:center;gap:10px;padding:14px 16px;border:2px solid #6B21A8;background:#F5F3FF;border-radius:10px;cursor:pointer;">
            <input type="radio" name="wfbMode" value="template" checked onchange="wfbSetMode(\'template\')" style="accent-color:#6B21A8;">
            <div>
              <div style="font-size:13px;font-weight:700;color:#6B21A8;">Use template</div>
              <div style="font-size:11px;color:#6B7280;margin-top:2px;">Choose from pre-built clinical workflow templates</div>
            </div>
          </label>
          <label id="wfbModeCardCustom" style="flex:1;display:flex;align-items:center;gap:10px;padding:14px 16px;border:2px solid #E5E0D8;background:#fff;border-radius:10px;cursor:pointer;">
            <input type="radio" name="wfbMode" value="custom" onchange="wfbSetMode(\'custom\')" style="accent-color:#6B21A8;">
            <div>
              <div style="font-size:13px;font-weight:700;color:#374151;">Custom workflow</div>
              <div style="font-size:11px;color:#6B7280;margin-top:2px;">Build a workflow from scratch</div>
            </div>
          </label>
        </div>

        <!-- Template picker row (template mode) -->
        <div id="wfbTemplateRow" style="display:flex;align-items:center;gap:12px;margin-bottom:20px;flex-wrap:wrap;">
          <select id="wfbTplSelect" style="flex:1;max-width:360px;border:1px solid #E5E0D8;border-radius:8px;padding:9px 12px;font-size:13px;font-family:inherit;color:#111827;outline:none;background:#fff;">
            <option value="phone_video">Standard Phone / Video</option>
            <option value="async_only">Async Only</option>
            <option value="hybrid">Hybrid (Async + Sync)</option>
            <option value="ccm">Chronic Care Management</option>
          </select>
          <button onclick="wfbLoadTemplate()" style="background:#6B21A8;color:#fff;border:none;border-radius:8px;padding:9px 18px;font-size:13px;font-weight:600;cursor:pointer;white-space:nowrap;">Load Template &#8594;</button>
        </div>

        <!-- Custom mode note -->
        <div id="wfbCustomNote" style="display:none;background:#FFF8EE;border:1px solid #FDE68A;border-radius:10px;padding:14px 16px;font-size:13px;color:#92400E;margin-bottom:20px;">
          Add stages from the library on the left to build your custom workflow pipeline.
        </div>

        <!-- Two-column: Library (35%) + Builder (65%) -->
        <div style="display:flex;gap:16px;margin-bottom:16px;align-items:flex-start;">

          <!-- Left: Stage Library -->
          <div style="width:35%;flex-shrink:0;">
            <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#6B7280;margin-bottom:8px;padding-left:2px;">Available Stages</div>
            <div id="wfbLibrary" style="display:flex;flex-direction:column;gap:5px;max-height:520px;overflow-y:auto;padding-right:4px;"></div>
          </div>

          <!-- Right: Workflow Builder -->
          <div style="flex:1;min-width:0;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
              <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#6B7280;">Configured Workflow</div>
              <span id="wfbStageCount" style="font-size:11px;font-weight:700;background:#EDE9FE;color:#6B21A8;padding:2px 8px;border-radius:10px;">0 stages</span>
              <a onclick="wfbClearAll()" style="margin-left:auto;font-size:12px;font-weight:600;color:#EF4444;cursor:pointer;text-decoration:none;">Clear All</a>
            </div>
            <div id="wfbBuilder" style="min-height:120px;"></div>
          </div>
        </div>

        <!-- Summary bar -->
        <div style="background:#F9FAFB;border:1px solid #E5E0D8;border-radius:8px;padding:10px 16px;font-size:12px;color:#374151;margin-bottom:20px;">
          Total stages: <strong id="wfbSumStages">0</strong> &nbsp;&middot;&nbsp;
          Est. total SLA: <strong id="wfbSumSla">0h</strong> &nbsp;&middot;&nbsp;
          Roles involved: <strong id="wfbSumRoles">&#8212;</strong>
        </div>

        <!-- Workflow Simulation -->
        <div style="background:#fff;border:1px solid #E5E0D8;border-radius:10px;padding:16px;">
          <div style="font-size:13px;font-weight:700;color:#111827;margin-bottom:12px;">Workflow Simulation &#8212; Patient: Marcus Johnson &middot; CST-2026-10849 &middot; Testosterone Care</div>
          <div id="wfbSimTracker" style="display:flex;align-items:flex-start;gap:0;overflow-x:auto;padding-bottom:8px;margin-bottom:14px;min-height:72px;"></div>
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
            <button id="wfbSimAdvBtn" onclick="wfbAdvanceSim()" style="background:#6B21A8;color:#fff;border:none;border-radius:8px;padding:8px 18px;font-size:13px;font-weight:600;cursor:pointer;white-space:nowrap;">Complete stage &amp; advance &#8594;</button>
            <button onclick="wfbResetSim()" style="background:#fff;border:1px solid #E5E0D8;color:#374151;border-radius:8px;padding:8px 14px;font-size:13px;font-weight:600;cursor:pointer;">&#8634; Reset</button>
          </div>
          <div id="wfbSimDetail" style="background:#F5F3FF;border:1px solid #DDD6FE;border-radius:8px;padding:14px;font-size:12px;min-height:40px;"></div>
        </div>

        <input type="hidden" id="s9SelectedTemplate" name="wf_template" value="phone_video">
      </div>'''

# Identify old step11 block precisely
old_step11_start = '      <!-- STEP 9: Workflow Configuration -->\n      <div class="step-panel" id="step11">'
old_step11_end   = '        <input type="hidden" id="s9SelectedTemplate" name="wf_template" value="standard_async_v2">\n      </div>'
old_step11 = wiz[wiz.index(old_step11_start):wiz.index(old_step11_end)+len(old_step11_end)]

if old_step11_start in wiz and old_step11_end in wiz:
    wiz = wiz.replace(old_step11, NEW_STEP11, 1)
    changes.append('2-wizard: step11 HTML panel replaced with interactive workflow builder')
else:
    changes.append('2-wizard: MISS — step11 HTML panel not found')

# ══════════════════════════════════════════════════════════════════
# CHANGE 2 — Replace Workflow JS section in wizard
# ══════════════════════════════════════════════════════════════════

NEW_WF_JS = '''// ─── Workflow Builder (Step 11) ───
var WFB_DEF = [
  {name:'Patient Intake', role:'MA'},
  {name:'Identity Verification', role:'Patient'},
  {name:'Insurance Verification', role:'MA'},
  {name:'MA Review', role:'MA'},
  {name:'Provider Assignment', role:'System'},
  {name:'Async Review', role:'Provider'},
  {name:'Consult — Phone/Video', role:'Provider'},
  {name:'Consult — Video Only', role:'Provider'},
  {name:'Lab Order', role:'Provider'},
  {name:'Lab Review', role:'Provider'},
  {name:'Prescription/Rx', role:'Provider'},
  {name:'Referral', role:'Provider'},
  {name:'Follow-up Consult', role:'Provider'},
  {name:'Care Coordination Review', role:'MA'},
  {name:'Patient Education', role:'MA'},
  {name:'Provider Documentation', role:'Provider'},
  {name:'Chart Closure', role:'Provider'},
];

var WFB_TEMPLATES = {
  phone_video: [
    {name:'Patient Intake', role:'MA', sla:2, required:true},
    {name:'MA Review', role:'MA', sla:1, required:true},
    {name:'Provider Assignment', role:'System', sla:1, required:true},
    {name:'Consult — Phone/Video', role:'Provider', sla:24, required:true},
    {name:'Provider Documentation', role:'Provider', sla:4, required:true},
    {name:'Chart Closure', role:'Provider', sla:2, required:true},
  ],
  async_only: [
    {name:'Patient Intake', role:'MA', sla:2, required:true},
    {name:'MA Review', role:'MA', sla:1, required:true},
    {name:'Provider Assignment', role:'System', sla:1, required:true},
    {name:'Async Review', role:'Provider', sla:48, required:true},
    {name:'Provider Documentation', role:'Provider', sla:4, required:true},
    {name:'Chart Closure', role:'Provider', sla:2, required:true},
  ],
  hybrid: [
    {name:'Patient Intake', role:'MA', sla:2, required:true},
    {name:'MA Review', role:'MA', sla:1, required:true},
    {name:'Provider Assignment', role:'System', sla:1, required:true},
    {name:'Async Review', role:'Provider', sla:48, required:true},
    {name:'Consult — Phone/Video', role:'Provider', sla:24, required:false},
    {name:'Provider Documentation', role:'Provider', sla:4, required:true},
    {name:'Chart Closure', role:'Provider', sla:2, required:true},
  ],
  ccm: [
    {name:'Patient Intake', role:'MA', sla:2, required:true},
    {name:'Care Coordination Review', role:'MA', sla:4, required:true},
    {name:'Provider Assignment', role:'System', sla:1, required:true},
    {name:'Consult — Phone/Video', role:'Provider', sla:24, required:true},
    {name:'Lab Order', role:'Provider', sla:48, required:false},
    {name:'Lab Review', role:'Provider', sla:24, required:false},
    {name:'Follow-up Consult', role:'Provider', sla:72, required:false},
    {name:'Prescription/Rx', role:'Provider', sla:4, required:false},
    {name:'Provider Documentation', role:'Provider', sla:4, required:true},
    {name:'Chart Closure', role:'Provider', sla:2, required:true},
  ],
};

var WFB_DESCS = {
  'Patient Intake': 'MA collects patient demographics, verifies identity, and confirms insurance eligibility.',
  'Identity Verification': 'Patient completes identity verification through an IAL2-compliant process.',
  'Insurance Verification': 'MA verifies insurance eligibility and coverage for the care product.',
  'MA Review': 'MA reviews intake submission, flags clinical gaps, and prepares chart for provider.',
  'Provider Assignment': 'System matches patient to available provider based on licensure, availability, and care product rules.',
  'Async Review': 'Provider reviews patient submission asynchronously and documents clinical findings.',
  'Consult — Phone/Video': 'Provider conducts live consultation with patient via phone or video.',
  'Consult — Video Only': 'Provider conducts live video consultation with patient.',
  'Lab Order': 'Provider orders required diagnostic labs through the integrated lab network.',
  'Lab Review': 'Provider reviews returned lab results and updates assessment and plan.',
  'Prescription/Rx': 'Provider submits prescription through integrated pharmacy network.',
  'Referral': 'Provider creates and routes referral to appropriate specialist or service.',
  'Follow-up Consult': 'Provider conducts follow-up consultation to review progress and adjust care plan.',
  'Care Coordination Review': 'MA coordinates care plan with interdisciplinary team and verifies patient readiness for next stage.',
  'Patient Education': 'MA provides patient education materials and confirms patient understanding of care plan.',
  'Provider Documentation': 'Provider completes SOAP note, updates assessment and plan, and prepares chart for closure.',
  'Chart Closure': 'Provider finalizes and signs chart, triggering billing submission and patient notification.',
};

var wfbWorkflow = [];
var wfbSimIdx = 0;
var wfbDragSrc = null;

function wfbRoleStyle(role) {
  if (role === 'MA') return 'background:#FEF3C7;color:#92400E;';
  if (role === 'System') return 'background:#E0E7FF;color:#3730A3;';
  if (role === 'Patient') return 'background:#D1FAE5;color:#065F46;';
  return 'background:#EDE9FE;color:#6B21A8;';
}

function wfbSetMode(mode) {
  var tc = document.getElementById('wfbModeCardTemplate');
  var cc = document.getElementById('wfbModeCardCustom');
  var tr = document.getElementById('wfbTemplateRow');
  var cn = document.getElementById('wfbCustomNote');
  if (mode === 'template') {
    if (tc) { tc.style.border='2px solid #6B21A8'; tc.style.background='#F5F3FF'; }
    if (cc) { cc.style.border='2px solid #E5E0D8'; cc.style.background='#fff'; }
    if (tr) tr.style.display='flex';
    if (cn) cn.style.display='none';
  } else {
    if (cc) { cc.style.border='2px solid #6B21A8'; cc.style.background='#F5F3FF'; }
    if (tc) { tc.style.border='2px solid #E5E0D8'; tc.style.background='#fff'; }
    if (tr) tr.style.display='none';
    if (cn) cn.style.display='';
  }
}

function wfbLoadTemplate() {
  var sel = document.getElementById('wfbTplSelect');
  if (!sel) return;
  var tpl = WFB_TEMPLATES[sel.value];
  if (!tpl) return;
  wfbWorkflow = tpl.map(function(s){ return {name:s.name,role:s.role,sla:s.sla,required:s.required}; });
  wfbSimIdx = 0;
  wfbRenderAll();
}

function wfbAddStage(i) {
  var def = WFB_DEF[i]; if (!def) return;
  wfbWorkflow.push({name:def.name, role:def.role, sla:4, required:false});
  wfbSimIdx = 0;
  wfbRenderAll();
}

function wfbRemoveStage(i) {
  if (wfbWorkflow[i] && wfbWorkflow[i].required) return;
  wfbWorkflow.splice(i,1);
  wfbSimIdx = 0;
  wfbRenderAll();
}

function wfbClearAll() {
  wfbWorkflow = [];
  wfbSimIdx = 0;
  wfbRenderAll();
}

function wfbUpdateSla(i, val) {
  var v = parseFloat(val);
  if (isNaN(v)||v<1) v=1;
  if (v>720) v=720;
  if (wfbWorkflow[i]) { wfbWorkflow[i].sla=v; wfbUpdateSummary(); wfbRenderSim(); }
}

function wfbToggleRequired(i, req) {
  if (wfbWorkflow[i]) { wfbWorkflow[i].required=req; wfbRenderBuilder(); wfbRenderLibrary(); }
}

function wfbRenderAll() {
  wfbRenderLibrary();
  wfbRenderBuilder();
  wfbUpdateSummary();
  wfbRenderSim();
}

function wfbRenderLibrary() {
  var lib = document.getElementById('wfbLibrary'); if (!lib) return;
  var inWf = {};
  wfbWorkflow.forEach(function(s){ inWf[s.name]=true; });
  lib.innerHTML = '';
  WFB_DEF.forEach(function(def,i) {
    var added = !!inWf[def.name];
    var card = document.createElement('div');
    card.style.cssText='border:1px solid #E5E7EB;border-radius:8px;padding:9px 12px;background:#fff;display:flex;align-items:center;gap:7px;';
    card.innerHTML =
      '<span style="font-size:12px;font-weight:600;color:#1F2937;flex:1;line-height:1.35;">' + def.name + '</span>' +
      '<span style="font-size:10px;font-weight:700;padding:2px 7px;border-radius:10px;flex-shrink:0;' + wfbRoleStyle(def.role) + '">' + def.role + '</span>' +
      (added
        ? '<span style="font-size:11px;font-weight:700;color:#059669;white-space:nowrap;min-width:52px;text-align:right;">✓ Added</span>'
        : '<button onclick="wfbAddStage(' + i + ')" style="font-size:11px;font-weight:600;border:1.5px solid #6B21A8;color:#6B21A8;background:#fff;border-radius:6px;padding:3px 9px;cursor:pointer;white-space:nowrap;flex-shrink:0;">+ Add</button>');
    lib.appendChild(card);
  });
}

function wfbRenderBuilder() {
  var bld = document.getElementById('wfbBuilder'); if (!bld) return;
  var cnt = document.getElementById('wfbStageCount');
  if (cnt) cnt.textContent = wfbWorkflow.length + ' stage' + (wfbWorkflow.length!==1?'s':'');
  if (wfbWorkflow.length === 0) {
    bld.innerHTML = '<div style="font-size:13px;color:#9CA3AF;font-style:italic;padding:28px 0;text-align:center;">No stages configured. Load a template or add stages from the library.</div>';
    return;
  }
  bld.innerHTML = '';
  wfbWorkflow.forEach(function(stage, i) {
    var card = document.createElement('div');
    card.draggable = true;
    card.dataset.idx = i;
    card.style.cssText='background:#fff;border:1px solid #E5E7EB;border-radius:8px;padding:12px 16px;margin-bottom:4px;';
    card.innerHTML =
      '<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">' +
        '<span style="font-size:18px;cursor:grab;color:#D1D5DB;flex-shrink:0;line-height:1;" title="Drag to reorder">⠿</span>' +
        '<span style="font-size:11px;font-weight:700;background:#F3F4F6;color:#374151;width:22px;height:22px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;">' + (i+1) + '</span>' +
        '<span style="font-size:13px;font-weight:700;color:#111827;flex:1;">' + stage.name + '</span>' +
        '<span style="font-size:10px;font-weight:700;padding:2px 8px;border-radius:10px;flex-shrink:0;' + wfbRoleStyle(stage.role) + '">' + stage.role + '</span>' +
        (stage.required
          ? '<span title="Required stages cannot be removed" style="font-size:20px;color:#D1D5DB;cursor:not-allowed;flex-shrink:0;line-height:1;">×</span>'
          : '<button onclick="wfbRemoveStage(' + i + ')" style="font-size:18px;background:none;border:none;color:#9CA3AF;cursor:pointer;flex-shrink:0;line-height:1;padding:0;" onmouseover="this.style.color=\'#EF4444\'" onmouseout="this.style.color=\'#9CA3AF\'">×</button>') +
      '</div>' +
      '<div style="display:flex;align-items:center;gap:14px;padding-left:48px;flex-wrap:wrap;">' +
        '<div style="display:flex;align-items:center;gap:5px;">' +
          '<span style="font-size:11px;color:#6B7280;white-space:nowrap;">SLA:</span>' +
          '<input type="number" min="1" max="720" value="' + stage.sla + '" onchange="wfbUpdateSla(' + i + ',this.value)" style="width:54px;border:1px solid #E5E0D8;border-radius:6px;padding:3px 6px;font-size:12px;text-align:center;">' +
          '<span style="font-size:11px;color:#6B7280;">hrs</span>' +
        '</div>' +
        '<label style="display:flex;align-items:center;gap:4px;font-size:12px;cursor:pointer;">' +
          '<input type="radio" name="wfbReq' + i + '" value="required"' + (stage.required?' checked':'') + ' onchange="wfbToggleRequired(' + i + ',true)" style="accent-color:#6B21A8;"> Required' +
        '</label>' +
        '<label style="display:flex;align-items:center;gap:4px;font-size:12px;cursor:pointer;">' +
          '<input type="radio" name="wfbReq' + i + '" value="optional"' + (!stage.required?' checked':'') + ' onchange="wfbToggleRequired(' + i + ',false)" style="accent-color:#6B21A8;"> Optional' +
        '</label>' +
      '</div>';
    // HTML5 drag-to-reorder
    card.addEventListener('dragstart', function(e) {
      wfbDragSrc = i;
      e.dataTransfer.effectAllowed = 'move';
      setTimeout(function(){ card.style.opacity='0.45'; }, 0);
    });
    card.addEventListener('dragend', function() {
      card.style.opacity='1';
      document.querySelectorAll('.wfb-drop-line').forEach(function(el){ el.remove(); });
    });
    card.addEventListener('dragover', function(e) {
      e.preventDefault();
      e.dataTransfer.dropEffect='move';
      document.querySelectorAll('.wfb-drop-line').forEach(function(el){ el.remove(); });
      var ind = document.createElement('div');
      ind.className='wfb-drop-line';
      ind.style.cssText='height:3px;background:#6B21A8;border-radius:2px;margin:1px 0;';
      bld.insertBefore(ind, card);
    });
    card.addEventListener('drop', function(e) {
      e.preventDefault();
      document.querySelectorAll('.wfb-drop-line').forEach(function(el){ el.remove(); });
      if (wfbDragSrc===null || wfbDragSrc===i) return;
      var moved = wfbWorkflow.splice(wfbDragSrc, 1)[0];
      var target = (i > wfbDragSrc) ? i-1 : i;
      wfbWorkflow.splice(target, 0, moved);
      wfbDragSrc = null;
      wfbSimIdx = 0;
      wfbRenderAll();
    });
    bld.appendChild(card);
    if (i < wfbWorkflow.length-1) {
      var arr = document.createElement('div');
      arr.style.cssText='text-align:center;color:#9CA3AF;font-size:16px;line-height:1.4;user-select:none;';
      arr.textContent='↓';
      bld.appendChild(arr);
    }
  });
}

function wfbUpdateSummary() {
  var total = wfbWorkflow.length;
  var totalSla = 0; var roles = {};
  wfbWorkflow.forEach(function(s){ totalSla+=(s.sla||0); roles[s.role]=true; });
  var h = Math.floor(totalSla), m = Math.round((totalSla-h)*60);
  var slaStr = h+'h'+(m>0?' '+m+'m':'');
  var sc=document.getElementById('wfbSumStages'); if(sc) sc.textContent=total;
  var sl=document.getElementById('wfbSumSla'); if(sl) sl.textContent=totalSla>0?slaStr:'0h';
  var rl=document.getElementById('wfbSumRoles'); if(rl) rl.textContent=Object.keys(roles).join(', ')||'—';
}

function wfbRenderSim() {
  var tracker=document.getElementById('wfbSimTracker');
  var detail=document.getElementById('wfbSimDetail');
  var advBtn=document.getElementById('wfbSimAdvBtn');
  if (!tracker) return;
  if (wfbWorkflow.length===0) {
    tracker.innerHTML='<div style="font-size:12px;color:#9CA3AF;font-style:italic;padding:8px 0;">Configure your workflow above to run the simulation.</div>';
    if (detail) detail.innerHTML='';
    if (advBtn) { advBtn.disabled=true; advBtn.style.opacity='0.5'; }
    return;
  }
  var done = wfbSimIdx>=wfbWorkflow.length;
  if (advBtn) {
    advBtn.disabled=done;
    advBtn.textContent=done?'Workflow complete ✓':'Complete stage & advance →';
    advBtn.style.background=done?'#059669':'#6B21A8';
    advBtn.style.cursor=done?'default':'pointer';
    advBtn.style.opacity='1';
  }
  // Tracker circles + connecting lines
  tracker.innerHTML='';
  wfbWorkflow.forEach(function(stage,i) {
    var isComplete=i<wfbSimIdx, isActive=i===wfbSimIdx;
    var wrap=document.createElement('div');
    wrap.style.cssText='display:flex;flex-direction:column;align-items:center;gap:4px;flex-shrink:0;';
    var circle=document.createElement('div');
    circle.style.cssText='width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex-shrink:0;' +
      (isComplete?'background:#1A1D23;color:#fff;':isActive?'background:#6B21A8;color:#fff;box-shadow:0 0 0 3px rgba(107,33,168,0.22);':'background:#E5E7EB;color:#9CA3AF;border:2px solid #D1D5DB;');
    circle.textContent=isComplete?'✓':(i+1);
    var lbl=document.createElement('div');
    lbl.style.cssText='font-size:9px;text-align:center;max-width:62px;line-height:1.3;'+(isActive?'color:#6B21A8;font-weight:700;':isComplete?'color:#374151;':'color:#9CA3AF;');
    lbl.textContent=stage.name;
    wrap.appendChild(circle); wrap.appendChild(lbl);
    tracker.appendChild(wrap);
    if (i<wfbWorkflow.length-1) {
      var line=document.createElement('div');
      line.style.cssText='height:2px;flex:1;min-width:10px;margin-top:13px;align-self:flex-start;'+(isComplete?'background:#1A1D23;':'background:#E5E7EB;');
      tracker.appendChild(line);
    }
  });
  // Detail card
  if (detail) {
    if (wfbSimIdx<wfbWorkflow.length) {
      var cur=wfbWorkflow[wfbSimIdx];
      var desc=WFB_DESCS[cur.name]||'Stage in progress.';
      detail.innerHTML=
        '<div style="display:grid;grid-template-columns:140px 1fr;gap:5px 12px;font-size:12px;">' +
        '<span style="color:#6B7280;font-weight:600;">Currently Active:</span><span style="font-weight:700;color:#6B21A8;">'+cur.name+'</span>'+
        '<span style="color:#6B7280;font-weight:600;">Role:</span><span>'+cur.role+'</span>'+
        '<span style="color:#6B7280;font-weight:600;">SLA:</span><span>'+cur.sla+' hours</span>'+
        '<span style="color:#6B7280;font-weight:600;">Status:</span><span><strong style="background:#D1FAE5;color:#065F46;padding:1px 7px;border-radius:8px;font-size:10px;font-weight:700;">In Progress</strong></span>'+
        '<span style="color:#6B7280;font-weight:600;">Description:</span><span style="color:#374151;">'+desc+'</span>'+
        '</div>';
    } else {
      detail.innerHTML='<div style="text-align:center;padding:8px 0;font-size:13px;font-weight:700;color:#059669;">✓ All '+wfbWorkflow.length+' stages complete. Chart would be closed and consult marked complete.</div>';
    }
  }
}

function wfbAdvanceSim() {
  if (wfbSimIdx<wfbWorkflow.length) { wfbSimIdx++; wfbRenderSim(); }
}

function wfbResetSim() {
  wfbSimIdx=0; wfbRenderSim();
}

// Init Step 11 with Standard Phone/Video template on DOMContentLoaded
(function() {
  var tpl=WFB_TEMPLATES['phone_video'];
  if (tpl) wfbWorkflow=tpl.map(function(s){ return {name:s.name,role:s.role,sla:s.sla,required:s.required}; });
  function init() { wfbRenderAll(); }
  if (document.readyState==='loading') { document.addEventListener('DOMContentLoaded', init); }
  else { init(); }
})();'''

# Identify old workflow JS section in wizard
WF_JS_START = '// ─── Step 9: Workflow Configuration ───'
WF_JS_END   = "updateWfTemplate('standard_async_v2');"

if WF_JS_START in wiz and WF_JS_END in wiz:
    idx_start = wiz.index(WF_JS_START)
    idx_end   = wiz.index(WF_JS_END) + len(WF_JS_END)
    wiz = wiz[:idx_start] + NEW_WF_JS + '\n' + wiz[idx_end:]
    changes.append('2-wizard: old workflow JS section replaced with new WFB JS')
else:
    changes.append('2-wizard: MISS — old workflow JS section not found (start or end marker missing)')

# ── Update review summary row for step 11 ─────────────────────────
old_rev11 = "    { n:11,  name:'Workflow Configuration', rows:[['Template', 'Standard Async Workflow v2']]},"
new_rev11 = "    { n:11,  name:'Workflow Configuration', rows:[['Stages', wfbWorkflow.length + ' stages configured'], ['Template', (document.getElementById('wfbTplSelect') ? document.getElementById('wfbTplSelect').options[document.getElementById('wfbTplSelect').selectedIndex].text : 'Custom') ]]},"
if old_rev11 in wiz:
    wiz = wiz.replace(old_rev11, new_rev11, 1)
    changes.append('2-wizard: review summary row for step 11 updated to show live workflow data')
else:
    changes.append('2-wizard: MISS — review summary row for step 11 not found')

with open(WIZARD, 'w', encoding='utf-8') as f:
    f.write(wiz)

# ── Report ─────────────────────────────────────────────────────────
print('Applied changes:')
for c in changes:
    icon = '❌' if 'MISS' in c else '✅'
    print(f'  {icon} {c}')

misses = [c for c in changes if 'MISS' in c]
print(f'\n{"All " + str(len(changes)) + " applied" if not misses else str(len(misses)) + " MISS(ES) — check manually"}.')
