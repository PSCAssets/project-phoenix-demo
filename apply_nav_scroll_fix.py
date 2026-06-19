#!/usr/bin/env python3
"""Fix left sidebar section nav scrolling in chart.html."""

CHART = '/Users/justin.woller/Documents/project-phoenix-demo/templates/provider/chart.html'

with open(CHART, 'r', encoding='utf-8') as f:
    html = f.read()

changes = []

# ── 1. Add section-* IDs to each .doc-sec-hd header div ────────────
SECTION_IDS = {
    1: 'section-chief-complaint',
    2: 'section-hpi',
    3: 'section-ros',
    4: 'section-vitals',
    5: 'section-lab-results',
    6: 'section-physical-exam',
    7: 'section-diagnoses',
    8: 'section-plan',
    9: 'section-hedis',
    10: 'section-mdm',
}
for n, sid in SECTION_IDS.items():
    old = f'<div class="doc-sec-hd" onclick="toggleDocSection({n})">'
    new = f'<div class="doc-sec-hd" id="{sid}" onclick="toggleDocSection({n})">'
    if old in html:
        html = html.replace(old, new, 1)
        changes.append(f'Added id="{sid}" to doc-sec-hd for section {n}')
    else:
        changes.append(f'MISS: doc-sec-hd for section {n} not found')

# ── 2. Fix docScrollTo: replace offsetTop with getBoundingClientRect ─
old_fn = '''function docScrollTo(n) {
  var sec = document.getElementById('docsec' + n);
  var center = document.getElementById('docCenter');
  if (sec && center) {
    if (!sec.classList.contains('open')) sec.classList.add('open');
    center.scrollTo({ top: sec.offsetTop - 8, behavior: 'smooth' });
  }
  document.querySelectorAll('.doc-nav-item').forEach(function(el, i) { el.classList.toggle('active', i + 1 === n); });
}'''

new_fn = '''function docScrollTo(n) {
  var sec = document.getElementById('docsec' + n);
  var center = document.getElementById('docCenter');
  if (sec && center) {
    if (!sec.classList.contains('open')) sec.classList.add('open');
    // offsetTop is relative to .chart-shell (position:fixed), not to #docCenter.
    // Use getBoundingClientRect to get the offset within the scroll container.
    var top = sec.getBoundingClientRect().top - center.getBoundingClientRect().top + center.scrollTop - 8;
    center.scrollTo({ top: top, behavior: 'smooth' });
  }
  document.querySelectorAll('.doc-nav-item').forEach(function(el, i) { el.classList.toggle('active', i + 1 === n); });
}'''

if old_fn in html:
    html = html.replace(old_fn, new_fn, 1)
    changes.append('Fixed docScrollTo: replaced offsetTop with getBoundingClientRect')
else:
    changes.append('MISS: docScrollTo function not found')

# ── 3. Verify IntersectionObserver root is correct (it should be) ──
if "root: center, threshold: 0.25" in html:
    changes.append('IntersectionObserver already uses root: center — no change needed')
else:
    changes.append('WARN: IntersectionObserver root may not be set correctly')

with open(CHART, 'w', encoding='utf-8') as f:
    f.write(html)

print('Applied changes:')
for c in changes:
    icon = '❌' if 'MISS' in c else ('⚠️' if 'WARN' in c else '✅')
    print(f'  {icon} {c}')

misses = [c for c in changes if 'MISS' in c]
print(f'\n{"All clear." if not misses else str(len(misses)) + " MISS(ES)"}')
