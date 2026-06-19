# Project Phoenix Demo — Chart UX Update Script v1
# June 17, 2026 — Provider Chart Targeted Fixes
# Run this entire prompt in Claude Code from: ~/Documents/project-phoenix-demo/

---

## CONTEXT

This script applies targeted UX fixes to the provider chart and queue based on demo review feedback. All edits are to existing Flask/Jinja2 HTML templates in `~/Documents/project-phoenix-demo/templates/`. Do not modify `project_phoenix.db`. After all changes, run the QA check at the bottom.

---

## CHANGE A — Remove Lab Results Tab from Right Panel

**File:** `templates/provider/chart.html`

The right panel currently has 3 tabs: Documentation | Lab Results | Communication.

Remove the **Lab Results** tab entirely. Lab content is already visible within the Documentation section, and the Lab Results tab currently navigates to the wrong section (physician exam). The right panel should have exactly 2 tabs:

```
Documentation | Communication
```

- Remove the `<button>` for Lab Results from the `.right-tabs` div
- Remove the Lab Results panel div (`id="rightPanel1"`)
- Renumber remaining panels:
  - `rightPanel0` = Documentation (active, flex layout)
  - `rightPanel1` = Communication (flex layout)
- Update `switchRightTab` to loop 0–1 only
- Update `RIGHT_PANEL_FLEX` to `{0: true, 1: true}`
- Update tab button onclick values: Documentation=0, Communication=1

---

## CHANGE B — Fix Left Nav Section Links to Anchor Within Chart

**File:** `templates/provider/chart.html`

The left sidebar contains navigation links for chart sections (e.g., Chief Complaint, HPI, Physical Exam, Assessment, MDM/Billing, etc.). Currently clicking these links does not scroll to the correct section in the middle column.

Fix all left nav section links so they anchor-scroll to the correct section within the chart middle column:

1. Find each `<a>` or clickable item in the left sidebar nav list
2. Ensure each target section in the middle column has a matching `id` attribute (e.g., `id="section-chief-complaint"`, `id="section-hpi"`, `id="section-exam"`, `id="section-assessment"`, `id="section-mdm"`, etc.)
3. Update each left nav link's `href` to point to the matching anchor (e.g., `href="#section-chief-complaint"`)
4. Add smooth scroll behavior: add `scroll-behavior: smooth` to the middle column's CSS, or use a JS click handler that calls `document.getElementById(targetId).scrollIntoView({ behavior: 'smooth', block: 'start' })`
5. Add a subtle active state to the nav item whose section is currently in view (use an IntersectionObserver or scroll event to highlight the active link — active state: purple left border `3px solid #6B21A8`, purple text `#6B21A8`)

---

## CHANGE C — Update Action Bar: Replace "Review & Sign" with "Preview"

**File:** `templates/provider/chart.html`

The chart action bar currently shows: `Review & Sign | Sign & Close Chart | Call | Video | Schedule | Route`

Make the following changes:

1. **Remove** the `"Review & Sign"` button
2. **Add** a `"Preview"` button in its place (same position, leftmost action after the status badge)
   - Style: outline button, border `1.5px solid #6B21A8`, text `#6B21A8`, background white, border-radius 8px, padding 8px 16px, font-weight 600
   - Label: `"👁 Preview"`
3. Keep `"Sign & Close Chart"` exactly as-is (same style, same position)

Final action bar order: `STATUS (In Progress) | 👁 Preview | Sign & Close Chart | Call | Video | Schedule | Route`

---

## CHANGE D — Preview Button: Chart Preview Modal

**File:** `templates/provider/chart.html`

When the provider clicks `"👁 Preview"`, open a full-screen modal showing a read-only preview of the completed chart documentation.

**Modal design:**
- Full-screen overlay (z-index 1000), white background, close button `✕` top-right
- Header: `"Chart Preview — Marcus Johnson — CST-2026-10849"` with a `"Close Preview"` button and a `"Sign & Close Chart"` button (purple) in the top right
- Body: render a clean, print-style summary of all documentation sections:
  - Chief Complaint
  - HPI
  - Review of Systems
  - Physical Exam
  - Assessment & Plan
  - MDM / Billing (show selected complexity level and billing codes)
- Each section has a heading in dark gray `#1F2937` bold, content in `#374151`
- Read-only — no inputs, no editing
- Footer note: `"Review all sections before signing. Once signed, this chart will be closed and submitted."`

---

## CHANGE E — Sign & Close Chart: Signing Workflow Modal

**File:** `templates/provider/chart.html`

When the provider clicks `"Sign & Close Chart"`, open a signing confirmation modal (do not close the chart immediately).

**Modal design:**
- Centered modal (not full-screen), white background, border-radius 12px, max-width 520px
- Header: `"Sign & Close Chart"`
- Body content:

  **Attestation statement** (gray box, light background `#F9FAFB`, border-radius 8px, padding 16px):
  > *"I attest that I have reviewed this patient's chart, the documentation is accurate and complete to the best of my knowledge, and this consultation is ready for billing submission."*

  **Provider Name field:**
  - Label: `"Signing Provider"`
  - Input: text field, pre-filled with `"Dr. Sarah Lee"`, editable
  - Sub-label: `"Confirm or update your name as it will appear on the signed chart"`

  **Attestation checkbox:**
  - `☐ I confirm the above attestation and authorize chart closure`

  **MDM summary line** (compact): `"MDM Complexity: Moderate · Codes: 99457 + 99458 + G2066 · Total Time: 38 min"`

- Footer buttons:
  - `"Cancel"` (outline, left)
  - `"Sign & Close"` (purple, right) — disabled until checkbox is checked
  - On confirm: show a green success toast `"✓ Chart signed and closed — CST-2026-10849"` for 3 seconds, then the modal closes

---

## CHANGE F — Routing Modal: Add "Route To" Name Picker for Message Individual

**File:** `templates/provider/chart.html`

In the `"Route This Consultation"` modal (the one with the Problem Type dropdown), when the provider selects `"Message Individual"` from the Problem Type dropdown, a second field should appear immediately below it:

**New conditional field:**
- Label: `"Route To"`
- A searchable dropdown (or select) pre-populated with these team member names:
  - Dr. Sarah Lee (Physician)
  - Dr. Marcus Webb (Physician)
  - Jamie Rodriguez (MA)
  - Priya Nair (MA)
  - Dana Cho (Care Coordinator)
  - Alex Kim (Billing Specialist)
  - Rachel Torres (Clinical Pharmacist)
- Placeholder: `"— Select team member —"`
- This field only appears when `"Message Individual"` is selected — it should be hidden for all other Problem Type selections
- The `"Route"` confirm button should remain disabled until both Problem Type and Route To are filled

**Confirmation flow when Route To is filled:**
- On confirm: the secondary "Is this related to the patient?" modal (from Change 8b in the main v3 script) should show the selected person's name: `"Is this message related to [Patient Name]'s consultation? It will be sent to [Selected Team Member Name]."`
- Toast confirmation: `"✓ Message sent to [Team Member Name]"` instead of generic category toast

**CSS for the new field:**
- Same styling as the Problem Type dropdown above it
- Animate in with a smooth `max-height` transition (0 → auto) when it appears

---

## FINAL STEP — QA Check

After completing all changes, run:

```bash
python3 /Users/justin.woller/Documents/project-phoenix-demo/qa_check.py
```

Paste the full output here before finishing.
