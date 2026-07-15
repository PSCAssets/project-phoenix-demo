#!/usr/bin/env python3
"""
apply_qa_fixes_v1.py — QA Demo Fixes (Jun 19, 2026)

Fixes applied:
  1. chart.html        — Replace horizontal right-panel tabs with vertical icon sidebar
  2. chart.html        — Update switchRightTab JS for 5 panels + vertical nav
  3. chart.html        — Add "Conduct Consult Now" button in visit detail actions
  4. chart.html        — Add patient message (Marcus Johnson, Jun 8) in async timeline
  5. chart.html        — Functional Expand feature on all 3 event entries + event-extra divs
  6. queue.html        — Remove "+ New Patient" for provider roles entirely (not just disabled)
  7. queue.html        — Fix Dashboard nav icon (grid → house)
  8. queue.html        — IS_NP variable + JS filter (TX/IL only for NP role)
  9. schedule.html     — Fix Dashboard nav icon (grid → house)
 10. schedule.html     — Rename "Add to Real-Time Queue" → "Conduct Consult Now"
 11. np_dashboard.html — Fix Dashboard nav icon (grid → house)
 12. np_dashboard.html — Add licensed states indicator (TX · IL)

Run from: ~/Documents/project-phoenix-demo/
"""

import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
ops = 0
fails = 0


def patch(filepath, old, new, label):
    global ops, fails
    path = os.path.join(BASE, filepath)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f'  ✗  FILE NOT FOUND: {filepath}')
        fails += 1
        return
    count = content.count(old)
    if count == 0:
        print(f'  ⚠  NOT FOUND — {label}')
        fails += 1
        return
    if count > 1:
        print(f'  ⚠  AMBIGUOUS ({count} matches) — {label}')
        fails += 1
        return
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.replace(old, new, 1))
    print(f'  ✓  {label}')
    ops += 1


# ═══════════════════════════════════════════════════════════════════════
# CHART.HTML FIXES
# ═══════════════════════════════════════════════════════════════════════
print('\n── chart.html ──────────────────────────────────────────────────')
CHART = 'templates/provider/chart.html'

# ── 1a. Add CSS for vertical icon nav sidebar ────────────────────────
patch(CHART,
'.right-panel::-webkit-scrollbar-thumb { background: #E5E0D8; border-radius: 3px; }',
'''.right-panel::-webkit-scrollbar-thumb { background: #E5E0D8; border-radius: 3px; }
/* ── Vertical right-panel icon sidebar ── */
.chart-right { position: relative; }
.right-panel { padding-right: 52px !important; }
.rp-vnav {
  position: absolute; top: 0; right: 0; bottom: 0; width: 44px;
  background: #F8F6F2; border-left: 1px solid #E5E0D8;
  display: flex; flex-direction: column; align-items: center;
  padding: 8px 0; gap: 2px; z-index: 10; overflow: hidden;
}
.rp-vnav-btn {
  width: 36px; height: 36px; border: none; background: none;
  border-radius: 8px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-size: 15px; color: #9CA3AF; position: relative;
  transition: background .15s, color .15s;
}
.rp-vnav-btn:hover { background: rgba(107,33,168,0.08); color: #6B21A8; }
.rp-vnav-btn.active { background: rgba(107,33,168,0.12); color: #6B21A8;
  border-right: 3px solid #6B21A8; }
.rp-vnav-btn .vnav-tip {
  display: none; position: absolute; right: 46px; top: 50%;
  transform: translateY(-50%); background: #1F2937; color: #fff;
  font-size: 11px; font-weight: 500; padding: 4px 8px; border-radius: 5px;
  white-space: nowrap; pointer-events: none; z-index: 200;
}
.rp-vnav-btn:hover .vnav-tip { display: block; }
.rp-vnav-divider { width: 28px; height: 1px; background: #E5E0D8; margin: 4px 0; }
.rp-vnav-expand {
  margin-top: auto; width: 36px; height: 28px; border: 1px solid #E5E0D8;
  border-radius: 6px; background: #fff; color: #6B7280; font-size: 12px;
  cursor: pointer; display: flex; align-items: center; justify-content: center;
}
.rp-vnav-expand:hover { background: #F3F4F6; }
.event-extra { display:none; margin-top:6px; padding:8px 10px;
  border-radius: 0 6px 6px 0; font-size:11px; color:#374151; line-height:1.6; }
.event-expand { font-size:11px; color:#6B21A8; text-decoration:none;
  display:inline-block; margin-top:4px; font-weight:500; }
.event-expand:hover { text-decoration:underline; }''',
'Add vertical nav CSS + event-extra styles')

# ── 1b. Replace horizontal tab bar with vertical icon nav ─────────────
patch(CHART,
'''      <div style="display:flex;align-items:center;border-bottom:1px solid #E5E0D8;flex-shrink:0;">
      <div class="right-tabs" style="border-bottom:none;flex:1;">
        <button class="right-tab-btn active" onclick="switchRightTab(0)">Documentation</button>
        <button class="right-tab-btn" onclick="switchRightTab(1)">Communication</button>
        <button class="right-tab-btn zendesk" onclick="switchRightTab(2)">🎫 Zendesk</button>
        <button class="right-tab-btn" onclick="switchRightTab(3)" style="color:#7C3AED;">📚 Clinical Resources</button>
        <button class="right-tab-btn" onclick="switchRightTab(4)" style="color:#0E7490;">🔗 Linked Consults</button>
      </div>
      <button class="panel-expand-btn" id="panelExpandBtn" onclick="togglePanelExpand()">⤢ Expand</button>
      </div>''',
'''      <!-- Vertical right-panel icon nav (replaces horizontal tab bar) -->
      <nav class="rp-vnav" id="rpVnav">
        <button class="rp-vnav-btn active" id="rpVnavBtn0" onclick="switchRightTab(0)">
          📄<span class="vnav-tip">Documentation</span>
        </button>
        <button class="rp-vnav-btn" id="rpVnavBtn1" onclick="switchRightTab(1)">
          💬<span class="vnav-tip">Communication</span>
        </button>
        <button class="rp-vnav-btn" id="rpVnavBtn2" onclick="switchRightTab(2)">
          🎫<span class="vnav-tip">Zendesk</span>
        </button>
        <div class="rp-vnav-divider"></div>
        <button class="rp-vnav-btn" id="rpVnavBtn3" onclick="switchRightTab(3)">
          📚<span class="vnav-tip">Clinical Resources</span>
        </button>
        <button class="rp-vnav-btn" id="rpVnavBtn4" onclick="switchRightTab(4)">
          🔗<span class="vnav-tip">Linked Consults</span>
        </button>
        <button class="rp-vnav-expand" id="panelExpandBtn" onclick="togglePanelExpand()" title="Expand panel">⤢</button>
      </nav>''',
'Replace horizontal tab bar with vertical icon nav')

# ── 1c. Update switchRightTab JS — 5 panels, rp-vnav-btn ─────────────
patch(CHART,
'''var RIGHT_PANEL_FLEX = {0: true, 1: true, 2: true};
document.addEventListener('DOMContentLoaded', function() { switchRightTab(0); });
function switchRightTab(idx) {
  document.querySelectorAll('.right-tab-btn').forEach(function(b, i) { b.classList.toggle('active', i === idx); });
  for (var i = 0; i < 3; i++) {
    var p = document.getElementById('rightPanel' + i);
    if (!p) continue;
    var isActive = (i === idx);
    p.classList.toggle('active', isActive);
    if (!isActive) {
      p.style.display = 'none';
    } else {
      p.style.display = RIGHT_PANEL_FLEX[i] ? 'flex' : 'block';
    }
  }
}''',
'''var RIGHT_PANEL_FLEX = {0: true, 1: true, 2: true, 3: true, 4: true};
document.addEventListener('DOMContentLoaded', function() { switchRightTab(0); });
function switchRightTab(idx) {
  document.querySelectorAll('.rp-vnav-btn').forEach(function(b, i) { b.classList.toggle('active', i === idx); });
  for (var i = 0; i < 5; i++) {
    var p = document.getElementById('rightPanel' + i);
    if (!p) continue;
    var isActive = (i === idx);
    p.classList.toggle('active', isActive);
    if (!isActive) {
      p.style.display = 'none';
    } else {
      p.style.display = RIGHT_PANEL_FLEX[i] ? 'flex' : 'block';
    }
  }
}''',
'Update switchRightTab — 5 panels + vertical nav buttons')

# ── 1d. Add toggleExpand JS function ─────────────────────────────────
patch(CHART,
'// Documentation section toggle',
'''// Expand / collapse event timeline entries
function toggleExpand(el) {
  var body = el.closest('.event-body');
  if (!body) return;
  var extra = body.querySelector('.event-extra');
  if (!extra) return;
  var open = extra.style.display === 'block';
  extra.style.display = open ? 'none' : 'block';
  el.textContent = open ? 'Expand ↓' : 'Collapse ↑';
}

// Documentation section toggle''',
'Add toggleExpand function')

# ── 1e. "Conduct Consult Now" button in visit detail actions ──────────
patch(CHART,
'<button onclick="openPreviewModal()" style="border:1.5px solid #6B21A8;color:#6B21A8;background:#fff;border-radius:8px;padding:8px 16px;font-weight:600;font-size:12px;cursor:pointer;display:inline-flex;align-items:center;gap:5px;white-space:nowrap;">&#128065; Preview</button>',
'''<button onclick="alert('Initiating real-time consult for Marcus Johnson...\n\nPatient has been notified and added to the Real-Time Queue.\nExpected connection in under 2 minutes.')" style="background:#6B21A8;color:#fff;border:none;border-radius:8px;padding:8px 16px;font-weight:700;font-size:12px;cursor:pointer;display:inline-flex;align-items:center;gap:5px;white-space:nowrap;">&#9889; Conduct Consult Now</button>
      <button onclick="openPreviewModal()" style="border:1.5px solid #6B21A8;color:#6B21A8;background:#fff;border-radius:8px;padding:8px 16px;font-weight:600;font-size:12px;cursor:pointer;display:inline-flex;align-items:center;gap:5px;white-space:nowrap;">&#128065; Preview</button>''',
'Add Conduct Consult Now button in visit detail actions')

# ── 1f. Patient message from Marcus Johnson (Jun 8) ───────────────────
patch(CHART,
'            <div class="event-day-sep">Jun 5, 2026</div>',
'''            <div class="event-day-sep">Jun 8, 2026</div>
            <div class="event-entry">
              <div class="event-border" style="background:#22C55E;"></div>
              <div class="event-body">
                <div class="event-meta">
                  <span class="event-badge" style="background:#DCFCE7;color:#15803D;">PATIENT</span>
                  <span class="event-name">Marcus Johnson</span>
                  <span class="event-ts">Jun 8 · 11:23 AM</span>
                </div>
                <div class="event-title">Patient Message — Secure Portal</div>
                <div class="event-text">Hi Dr. Lee, I've been experiencing increased fatigue lately, especially in the afternoons around 3pm. My energy has dropped compared to last quarter and I'm having trouble focusing at work...</div>
                <div class="event-extra" style="background:#F0FDF4;border-left:3px solid #22C55E;">
                  Hi Dr. Lee,<br><br>
                  I've been experiencing increased fatigue lately, especially in the afternoons around 3pm. My energy has dropped compared to last quarter and I'm having trouble focusing during work meetings.<br><br>
                  I'm also noticing my mood has been a bit off — some irritability that my wife mentioned. My libido has also decreased since my last check-in. I'm wondering if this could be related to my testosterone levels or if my dosing schedule needs adjustment.<br><br>
                  I have a work trip coming up mid-June and want to make sure I'm on the right track. Should I come in for labs sooner than my scheduled 90-day follow-up, or should I just complete the questionnaire you sent?<br><br>
                  Thank you,<br>
                  Marcus Johnson
                </div>
                <a href="#" onclick="toggleExpand(this);return false;" class="event-expand">Expand &#8595;</a>
              </div>
            </div>
            <div class="event-day-sep">Jun 5, 2026</div>''',
'Add Marcus Johnson patient message (Jun 8) in async timeline')

# ── 1g. Functional Expand — Provider Working Note (Jun 14) ───────────
patch(CHART,
'                <div class="event-text">Patient reports continued fatigue despite therapy. Questionnaire reviewed — no red flags. Reviewing testosterone levels before responding.</div>\n                <a href="#" onclick="return false;" class="event-expand">Expand ↓</a>',
'''                <div class="event-text">Patient reports continued fatigue despite therapy. Questionnaire reviewed — no red flags. Reviewing testosterone levels before responding.</div>
                <div class="event-extra" style="background:#F9F5FF;border-left:3px solid #7C3AED;">
                  <strong>Full working note:</strong><br>
                  Patient reports continued fatigue on current Testosterone Cypionate 200mg/mL IM q2w protocol. Questionnaire reviewed — 18/18 questions answered, no red flags. No suicidal ideation, no CV symptoms.<br><br>
                  Labs: Total T 485 ng/dL (nl 300-1000), Free T 12.3 pg/mL (low-normal). Patient's pre-treatment baseline was 320 ng/dL. Subjective improvement noted but fatigue persists, particularly 3-4 days post-injection (trough window).<br><br>
                  <strong>Plan:</strong> Consider adjusting injection interval from q14d to q10d to reduce trough symptoms. Recommend lab recheck at 90-day follow-up (Total T, Free T, HCT, PSA). Patient education on trough vs. peak symptom patterns.
                </div>
                <a href="#" onclick="toggleExpand(this);return false;" class="event-expand">Expand &#8595;</a>''',
'Make Expand functional — Provider Working Note (Jun 14)')

# ── 1h. Functional Expand — Async Questionnaire Submitted (Jun 10) ───
patch(CHART,
'                <div class="event-text">Patient completed 18/18 intake questions. Primary concern: fatigue and low energy. Reports afternoon fatigue around 3pm.</div>\n                <a href="#" onclick="return false;" class="event-expand">Expand ↓</a>',
'''                <div class="event-text">Patient completed 18/18 intake questions. Primary concern: fatigue and low energy. Reports afternoon fatigue around 3pm.</div>
                <div class="event-extra" style="background:#F0FDF4;border-left:3px solid #22C55E;">
                  <strong>Full questionnaire responses:</strong><br>
                  Q1 Chief concern: Fatigue and low energy, especially afternoons (3-5pm window).<br>
                  Q2 Onset: Gradually worsening over 8-12 weeks.<br>
                  Q3 Severity (1-10): 6/10 — affecting work performance and motivation.<br>
                  Q4 Sleep quality: Adequate (7h avg), no insomnia reported.<br>
                  Q5 Libido: Decreased from baseline (4/10 vs. prior 7/10).<br>
                  Q6 Mood: Mild irritability, not depressed. No PHQ-9 flags.<br>
                  Q7 Concentration: Slightly impaired during afternoon hours.<br>
                  Q8-18: No ED, no CV symptoms, no headaches, medications unchanged (Lisinopril 10mg QD), no recent illness, exercise 3x/wk, diet unchanged, BMI stable at 26.4, no new major stressors, alcohol 2-3 drinks/wk, no tobacco/cannabis.
                </div>
                <a href="#" onclick="toggleExpand(this);return false;" class="event-expand">Expand &#8595;</a>''',
'Make Expand functional — Async Questionnaire (Jun 10)')

# ── 1i. Functional Expand — SOAP Note Signed (Jun 5) ─────────────────
patch(CHART,
'                <div class="event-text">Chart signed and closed for prior consult CST-2026-10721. All sections complete.</div>\n                <a href="#" onclick="return false;" class="event-expand">Expand ↓</a>',
'''                <div class="event-text">Chart signed and closed for prior consult CST-2026-10721. All sections complete.</div>
                <div class="event-extra" style="background:#F9F5FF;border-left:3px solid #7C3AED;">
                  <strong>SOAP Note Summary — CST-2026-10721:</strong><br>
                  <em>Subjective:</em> Patient reports ~40% energy improvement since initiating TC. Sleep quality improved. Mild injection site soreness at administration site. No ED. Libido rated 6/10 (improved from 3/10 at baseline).<br><br>
                  <em>Objective:</em> Total T 485 ng/dL (&#8593; from 320 baseline). HCT 46.1% (within normal limits). Weight 182 lbs (stable). BP 124/78 mmHg.<br><br>
                  <em>Assessment:</em> Testosterone deficiency responding to therapy. Labs trending positively. Trough symptom pattern noted (mild fatigue days 12-14 of cycle).<br><br>
                  <em>Plan:</em> Continue TC 200mg/mL IM q2w. Discuss injection interval adjustment at next visit if trough symptoms persist. Recheck Total T, Free T, HCT, PSA at 90-day follow-up. Patient education on injection site rotation completed.
                </div>
                <a href="#" onclick="toggleExpand(this);return false;" class="event-expand">Expand &#8595;</a>''',
'Make Expand functional — SOAP Note (Jun 5)')


# ═══════════════════════════════════════════════════════════════════════
# QUEUE.HTML FIXES
# ═══════════════════════════════════════════════════════════════════════
print('\n── queue.html ──────────────────────────────────────────────────')
QUEUE = 'templates/provider/queue.html'

# ── 2a. Fix Dashboard nav icon: grid → house ─────────────────────────
patch(QUEUE,
'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>\n      <span class="sib-label">Dashboard</span>',
'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>\n      <span class="sib-label">Dashboard</span>',
'Fix Dashboard icon — grid → house')

# ── 2b. Remove "+ New Patient" button for provider roles entirely ──────
patch(QUEUE,
'''    {% if session.get('role') in ['provider_md','provider_np','provider_do','provider_rn','provider_gc'] %}
    <span style="margin-left:auto;display:inline-flex;align-items:center;gap:6px;background:#6B21A8;color:#fff;border:none;border-radius:8px;padding:7px 14px;font-size:12px;font-weight:600;text-decoration:none;opacity:0.35;pointer-events:none;cursor:not-allowed;">+ New Patient</span>
    {% else %}
    <a href="/provider/new-patient" style="margin-left:auto;display:inline-flex;align-items:center;gap:6px;background:#6B21A8;color:#fff;border:none;border-radius:8px;padding:7px 14px;font-size:12px;font-weight:600;text-decoration:none;">+ New Patient</a>
    {% endif %}''',
'''    {% if session.get('role') not in ['provider_md','provider_np','provider_do','provider_rn','provider_gc'] %}
    <a href="/provider/new-patient" style="margin-left:auto;display:inline-flex;align-items:center;gap:6px;background:#6B21A8;color:#fff;border:none;border-radius:8px;padding:7px 14px;font-size:12px;font-weight:600;text-decoration:none;">+ New Patient</a>
    {% endif %}''',
'Remove + New Patient for provider roles (not just disabled — gone)')

# ── 2c. Add IS_NP var + NP state filter JS ────────────────────────────
patch(QUEUE,
'const SHOW_OWN_ONLY = {% endraw %}{{ show_own_only | tojson }}{% raw %};',
r'''const SHOW_OWN_ONLY = {% endraw %}{{ show_own_only | tojson }}{% raw %};
const IS_NP = {% endraw %}{{ (session.get('role') == 'provider_np') | tojson }}{% raw %};''',
'Add IS_NP Jinja2 variable to queue JS block')

# ── 2d. Add NP state-filter function ─────────────────────────────────
patch(QUEUE,
'const allRows = Array.from(document.querySelectorAll(\'tbody tr\'));',
r'''const allRows = Array.from(document.querySelectorAll('tbody tr'));

// NP role: filter queue to licensed states only (TX and IL)
(function() {
  if (!IS_NP) return;
  var npStates = ['TX', 'IL'];
  allRows.forEach(function(row) {
    var stateCell = row.cells[6];
    if (!stateCell) return;
    var state = stateCell.textContent.trim();
    if (npStates.indexOf(state) === -1) {
      row.style.display = 'none';
    }
  });
  var footer = document.querySelector('.footer-info');
  if (footer) {
    var badge = document.createElement('span');
    badge.style.cssText = 'margin-left:12px;font-size:11px;background:#EDE9FE;color:#6B21A8;padding:2px 8px;border-radius:10px;font-weight:600;';
    badge.textContent = '🔒 Filtered: TX · IL only';
    footer.appendChild(badge);
  }
})();''',
'Add NP state filter — TX/IL only (JS runs on load)')


# ═══════════════════════════════════════════════════════════════════════
# SCHEDULE.HTML FIXES
# ═══════════════════════════════════════════════════════════════════════
print('\n── schedule.html ───────────────────────────────────────────────')
SCHED = 'templates/provider/schedule.html'

# ── 3a. Fix Dashboard nav icon: grid → house ─────────────────────────
patch(SCHED,
'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
'Fix Dashboard icon — grid → house')

# ── 3b. Rename button: "Add to Real-Time Queue" → "Conduct Consult Now"
patch(SCHED,
'&#9889; Add to Real-Time Queue',
'&#9889; Conduct Consult Now',
'Rename "Add to Real-Time Queue" → "Conduct Consult Now"')


# ═══════════════════════════════════════════════════════════════════════
# NP_DASHBOARD.HTML FIXES
# ═══════════════════════════════════════════════════════════════════════
print('\n── np_dashboard.html ───────────────────────────────────────────')
NP = 'templates/provider/np_dashboard.html'

# ── 4a. Fix Dashboard nav icon: grid → house ─────────────────────────
patch(NP,
'        <rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/>\n        <rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
'        <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
'Fix Dashboard icon — grid → house')

# ── 4b. Add TX · IL licensed states badge next to license warning ─────
patch(NP,
'<div class="topbar-license-warn">⚠ Texas NP license expires in <strong>24 days</strong> (Jun 21, 2026) — <a onclick="alert(\'Opening Verifiable license renewal portal...\')">Renew via Verifiable</a></div>',
'''<div class="topbar-license-warn">⚠ Texas NP license expires in <strong>24 days</strong> (Jun 21, 2026) — <a onclick="alert('Opening Verifiable license renewal portal...')">Renew via Verifiable</a></div>
          <div style="font-size:10px;margin-top:3px;display:flex;gap:6px;align-items:center;">
            <span style="color:#6B7280;font-weight:500;">Licensed states:</span>
            <span style="background:#EDE9FE;color:#6B21A8;padding:1px 7px;border-radius:10px;font-weight:700;font-size:10px;">TX</span>
            <span style="background:#EDE9FE;color:#6B21A8;padding:1px 7px;border-radius:10px;font-weight:700;font-size:10px;">IL</span>
            <span style="color:#9CA3AF;font-size:10px;">· Queue filtered to licensed states only</span>
          </div>''',
'Add TX/IL licensed states indicator in NP dashboard topbar')


# ═══════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════
print(f'\n── Result ──────────────────────────────────────────────────────')
print(f'  {ops} operations completed')
print(f'  {fails} failed\n')

if fails > 0:
    print('  ⚠  Some patches did not apply — check output above.')
    sys.exit(1)
else:
    print('  All QA fixes applied successfully.')
    print('\n  Next steps:')
    print('    python3 /Users/justin.woller/Documents/project-phoenix-demo/qa_check.py')
    print('    Paste the full output, then commit + push to Render.\n')
