#!/usr/bin/env python3
"""
apply_qa_fixes_v4.py — QA fixes batch 4 for Project Phoenix demo
Fixes:
  1. chart.html      — Move right-panel vnav from RIGHT → LEFT side; widen panel to 420px; add directional expand arrow
  2. schedule.html   — Remove "Conduct Consult Now" from topbar; add it inside apptDetailFt modal footer
  3. queue.html      — NP state filter (TX/IL) persists through tab switching / applyFilters() calls
  4. 11 templates    — Replace grid SVG → house SVG for Dashboard nav icon everywhere

Workflow: run locally first, review at localhost:5000, then commit only after approval.
"""

import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
TMPL = os.path.join(BASE, 'templates', 'provider')

errors = []

def apply(filepath, old, new, label):
    full = os.path.join(BASE, filepath) if not os.path.isabs(filepath) else filepath
    with open(full, 'r', encoding='utf-8') as f:
        content = f.read()
    if old not in content:
        errors.append(f"  [MISS] {label} — anchor not found in {filepath}")
        return False
    count = content.count(old)
    if count > 1:
        print(f"  [WARN] {label} — anchor found {count}x in {filepath}, replacing all")
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content.replace(old, new))
    print(f"  [OK]  {label}")
    return True


# ===========================================================================
# OP 1: chart.html — widen panel from 360px → 420px
# ===========================================================================
print("\n=== OP 1: chart.html — widen right panel to 420px ===")
apply(
    'templates/provider/chart.html',
    '.chart-right { width: 360px; min-width: 360px; background: #fff; border-left: 1px solid #E5E7EB; display: flex; flex-direction: column; overflow: hidden; flex-shrink: 0; }',
    '.chart-right { width: 420px; min-width: 420px; background: #fff; border-left: 1px solid #E5E7EB; display: flex; flex-direction: column; overflow: hidden; flex-shrink: 0; }',
    'chart-right width 360→420px'
)

# ===========================================================================
# OP 2: chart.html — move vnav from right → left (border-left → border-right)
# ===========================================================================
print("\n=== OP 2: chart.html — move vnav to left side ===")
apply(
    'templates/provider/chart.html',
    '  position: absolute; top: 0; right: 0; bottom: 0; width: 44px;\n  background: #F8F6F2; border-left: 1px solid #E5E0D8;',
    '  position: absolute; top: 0; left: 0; bottom: 0; width: 44px;\n  background: #F8F6F2; border-right: 1px solid #E5E0D8;',
    'rp-vnav: right→left, border-left→border-right'
)

# OP 2b: flip right-panel padding from right → left
apply(
    'templates/provider/chart.html',
    '.right-panel { padding-right: 52px !important; }',
    '.right-panel { padding-left: 52px !important; }',
    'right-panel padding-right→padding-left'
)

# OP 2c: active button indicator — border-right → border-left
apply(
    'templates/provider/chart.html',
    '.rp-vnav-btn.active { background: rgba(107,33,168,0.12); color: #6B21A8;\n  border-right: 3px solid #6B21A8; }',
    '.rp-vnav-btn.active { background: rgba(107,33,168,0.12); color: #6B21A8;\n  border-left: 3px solid #6B21A8; }',
    'rp-vnav-btn.active border-right→border-left'
)

# OP 2d: tooltip position — show to the right of the left-side nav (left:46px instead of right:46px)
apply(
    'templates/provider/chart.html',
    '  display: none; position: absolute; right: 46px; top: 50%;',
    '  display: none; position: absolute; left: 46px; top: 50%;',
    'vnav-tip tooltip: right:46px → left:46px'
)

# ===========================================================================
# OP 3: chart.html — update expand button to use directional arrow
# ===========================================================================
print("\n=== OP 3: chart.html — directional expand arrow ===")
apply(
    'templates/provider/chart.html',
    '<button class="rp-vnav-expand" id="panelExpandBtn" onclick="togglePanelExpand()" title="Expand panel">⤢</button>',
    '<button class="rp-vnav-expand" id="panelExpandBtn" onclick="togglePanelExpand()" title="Expand/collapse panel" style="font-size:14px;">&#9655;</button>',
    'expand button: ⤢ → ▷ directional arrow'
)

# OP 3b: update togglePanelExpand JS to swap arrow direction
apply(
    'templates/provider/chart.html',
    '''function togglePanelExpand() {
  var right = document.getElementById('chartRight');
  var btn = document.getElementById('panelExpandBtn');
  if (!right) return;
  if (right.classList.contains('panel-expanded')) {
    right.classList.remove('panel-expanded');
    right.style.width = ''; right.style.minWidth = '';
    if (btn) btn.textContent = '⤢ Expand';
  } else {
    right.classList.add('panel-expanded');
    right.style.width = '65%'; right.style.minWidth = '65%';
    if (btn) btn.textContent = '⤡ Collapse';
  }
}''',
    '''function togglePanelExpand() {
  var right = document.getElementById('chartRight');
  var btn = document.getElementById('panelExpandBtn');
  if (!right) return;
  if (right.classList.contains('panel-expanded')) {
    right.classList.remove('panel-expanded');
    right.style.width = ''; right.style.minWidth = '';
    if (btn) btn.innerHTML = '&#9655;'; // ▷ expand
  } else {
    right.classList.add('panel-expanded');
    right.style.width = '65%'; right.style.minWidth = '65%';
    if (btn) btn.innerHTML = '&#9665;'; // ◁ collapse
  }
}''',
    'togglePanelExpand: swap arrow glyphs'
)

# ===========================================================================
# OP 4: schedule.html — remove "Conduct Consult Now" from topbar
# ===========================================================================
print("\n=== OP 4: schedule.html — remove Conduct Consult Now from topbar ===")
apply(
    'templates/provider/schedule.html',
    '\n    <button id="realTimeQueue" class="real-time-queue" onclick="openRTQueueModal()" style="margin-left:8px;background:#6B21A8;color:#fff;border:none;border-radius:7px;padding:7px 16px;font-size:12px;font-weight:600;cursor:pointer;">&#9889; Conduct Consult Now</button>',
    '',
    'Remove Conduct Consult Now from topbar'
)

# ===========================================================================
# OP 5: schedule.html — add "Conduct Consult Now" inside appointment detail modal footer
# ===========================================================================
print("\n=== OP 5: schedule.html — add Conduct Consult Now to apptDetailFt ===")
apply(
    'templates/provider/schedule.html',
    '      <a id="apptDetailChartLink" href="/provider/chart/1" class="btn-open-chart">Open Chart →</a>\n    </div>',
    '      <a id="apptDetailChartLink" href="/provider/chart/1" class="btn-open-chart">Open Chart →</a>\n      <button onclick="openRTQueueModal()" style="background:#059669;color:#fff;border:none;border-radius:7px;padding:7px 14px;font-size:12px;font-weight:600;cursor:pointer;margin-left:auto;">&#9889; Conduct Consult Now</button>\n    </div>',
    'Add Conduct Consult Now to apptDetailFt modal footer'
)

# ===========================================================================
# OP 6: queue.html — NP state filter persists through applyFilters() tab switches
# ===========================================================================
print("\n=== OP 6: queue.html — NP state filter persistence fix ===")
apply(
    'templates/provider/queue.html',
    '    row.style.display = show ? \'\' : \'none\';\n  });\n}',
    '''    // NP role: always enforce state filter — never let other filters un-hide non-TX/IL rows
    if (IS_NP) {
      var stateCell = row.cells[6];
      var state = stateCell ? stateCell.textContent.trim() : '';
      if (['TX', 'IL'].indexOf(state) === -1) { row.style.display = 'none'; return; }
    }
    row.style.display = show ? '' : 'none';
  });
}''',
    'NP state filter persistence in applyFilters()'
)

# ===========================================================================
# OP 7: Replace grid SVG → house SVG across all 11 templates
# Dashboard nav icon standardization
# ===========================================================================
print("\n=== OP 7: Replace grid SVG → house SVG across all templates ===")

GRID_SVG_COMMON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>'
HOUSE_SVG_COMMON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9,22 9,12 15,12 15,22"/></svg>'

# Files using the common inline pattern
common_icon_files = [
    'templates/provider/messages.html',
    'templates/provider/billing.html',
    'templates/provider/alerts.html',
    'templates/provider/notifications.html',
    'templates/provider/pharmacy.html',
    'templates/provider/new_patient.html',
    'templates/provider/settings.html',
    'templates/provider/oversight.html',
]

for fpath in common_icon_files:
    apply(fpath, GRID_SVG_COMMON, HOUSE_SVG_COMMON, f'House icon: {os.path.basename(fpath)}')

# gc_dashboard.html — multiline variant
apply(
    'templates/provider/gc_dashboard.html',
    '      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">\n        <rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/>\n        <rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>\n      </svg>',
    '      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">\n        <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9,22 9,12 15,12 15,22"/>\n      </svg>',
    'House icon: gc_dashboard.html (multiline)'
)

# rn_dashboard.html — width="18" height="18", no rx, different rect order
apply(
    'templates/provider/rn_dashboard.html',
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>',
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9,22 9,12 15,12 15,22"/></svg>',
    'House icon: rn_dashboard.html (w18 variant)'
)

# ma_dashboard.html — width="20" height="20", stroke-width="1.8", stroke-linecap/linejoin
apply(
    'templates/provider/ma_dashboard.html',
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9,22 9,12 15,12 15,22"/></svg>',
    'House icon: ma_dashboard.html (w20 variant)'
)

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
    print("  1. cd /path/to/project-phoenix-demo && python3 app.py")
    print("  2. Review at http://localhost:5000")
    print("  3. Approve → then commit and push")
