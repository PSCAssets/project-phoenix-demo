# Project Phoenix Demo — Meeting Update Script v2
# June 17, 2026 — 12 Changes from Demo Review Meeting
# Run this entire prompt in Claude Code from: ~/Documents/project-phoenix-demo/

---

## CONTEXT

This script implements 12 changes from the June 17 Project Phoenix demo review meeting. All edits are to existing Flask/Jinja2 HTML templates in `~/Documents/project-phoenix-demo/templates/`. Do not modify `project_phoenix.db`. After all changes, run the QA check at the bottom.

---

## CHANGE 1 — Provider Queue: Add Patient Identifiers (DOB, Gender, Full Name)

**File:** `templates/provider/queue.html`

Currently the patient name column shows initials only (e.g., "M.J."). Update every patient row in the queue table to show:
- **Full name** (e.g., "Marcus Johnson") as the clickable link instead of initials
- **DOB** below the name in smaller text (e.g., "DOB: 04/12/1985")
- **Gender** as a small badge next to DOB (e.g., "M" or "F" in a pill)

The `.patient-dob` CSS class already exists. Use it for DOB. Add a `.patient-gender` badge styled as a small rounded pill: gray background `#E5E7EB`, text `#374151`, font-size 10px, padding 1px 6px.

Replace the initials in all patient rows with realistic full names. Keep all existing href links, care product badges, and action buttons exactly as-is. Only the name cell changes.

Name/DOB/gender mappings (keep same row order):
- M.J. → Marcus Johnson, DOB: 04/12/1985, M
- P.W. → Patricia Wells, DOB: 09/23/1962, F
- D.K. → David Kim, DOB: 07/07/1978, M
- R.L. → Rosa Lopez, DOB: 11/30/1990, F
- T.C. → Thomas Chen, DOB: 03/15/1982, M
- A.N. → Alicia Nash, DOB: 06/01/1995, F
- B.M. → Brian Mitchell, DOB: 08/19/1970, M
- J.R. → Jennifer Rivera, DOB: 02/27/1988, F
- E.V. → Elena Vasquez, DOB: 05/14/1975, F
- M.G. → Michael Grant, DOB: 12/03/1959, M
- D.R. → Diana Ross, DOB: 01/22/1967, F
- S.G. → Samuel Greene, DOB: 10/08/1993, M
- O.T. → Olivia Torres, DOB: 04/29/1980, F
- C.D. → Carlos Diaz, DOB: 07/17/1986, M
- H.O. → Hannah O'Brien, DOB: 09/11/1972, F

---

## CHANGE 2 — Provider Chart: Remove Breadcrumb Header Bar

**File:** `templates/provider/chart.html`

The chart currently has a top bar showing `← Back to Dashboard | Marcus Johnson — CST-2026-10849`. This wastes real estate — the patient name is already displayed in the patient info section below, and navigation back to the home page is handled by the left nav bar.

**Remove this entire breadcrumb/header bar div completely.** The chart body should start directly with the patient info header section (the one showing "Testosterone Care · Phone consult · Follow-up · CST-2026-10849" and the patient avatar/name/DOB row).

Look for a div containing text like "Back to Dashboard" or a back-arrow link near the top of the chart template and delete it entirely.

---

## CHANGE 3 — Provider Chart: Replace Numbered Stages with Named Workflow Stages

**File:** `templates/provider/chart.html`

The chart currently shows a step indicator with numbered circles (1, 2, 3, 4, 5, 6) that are not meaningful to providers. Replace this with **named workflow stages** that clearly show what has been completed and what is upcoming.

### New stage bar design:

Replace the numbered circles with a horizontal named-stage tracker using these 6 stages:
1. Intake Submitted
2. MA Review
3. Provider Assigned
4. Consult
5. Documentation
6. Complete

Visual design for each stage:
- **Completed stages** (stages before current): filled dark circle `#1F2937` with white `✓` checkmark inside, stage name below in gray `#6B7280`, font-size 11px
- **Current/active stage**: filled purple circle `#6B21A8` with white stage number inside, stage name below in purple bold, font-size 11px
- **Upcoming stages**: hollow circle with gray border `#D1D5DB`, gray stage name below, font-size 11px
- Connecting lines between circles: solid dark line for completed segments, dashed gray for upcoming
- Below the stage bar: `"Currently: [Stage Name] · Assigned to: [Role]"` — keep the existing text format

For the demo, set **Stage 2 (MA Review)** as the active/current stage (Stage 1 complete, Stages 3–6 upcoming). Update the label: `"Currently: MA Review · Assigned to: MA"`.

The stage bar sits in the same location as the existing numbered step indicator — replace it in-place, same row.

---

## CHANGE 4 — Provider Chart: SLA Warning Display Logic

**File:** `templates/provider/chart.html`

Currently the SLA time remaining is always shown as a warning (amber/orange color) regardless of where it falls in the SLA window. This is incorrect — warnings should only appear when the SLA threshold is being approached or breached.

### Fix the SLA display logic with these rules:

The SLA display in the chart header (e.g., "1h 24m") and the SLA badge on the stage bar (e.g., "SLA: 6h remaining") should use this color logic:

- **Green** `#16A34A` — More than 50% of SLA time remaining. Label: `"SLA: Xh Ym"` (no warning word)
- **Amber** `#D97706` — Between 20% and 50% of SLA time remaining. Label: `"⚠ SLA: Xh Ym remaining"`
- **Red** `#DC2626` — Less than 20% of SLA time remaining or SLA breached. Label: `"🚨 SLA: Xh Ym — Action Required"`

For the demo, set the SLA values so they demonstrate the logic correctly:
- The chart header SLA box: show `"6h 24m"` in **green** (plenty of time — this is a 48h SLA with 6h 24m elapsed, not a warning state)
- Remove the amber/orange styling that makes it look like a warning when it isn't one
- The stage bar SLA badge: show `"SLA: 6h remaining"` in green styling (light green background `#DCFCE7`, green text `#16A34A`)

Add a comment in the JS: `// SLA color logic: green >50% remaining, amber 20-50%, red <20%`

---

## CHANGE 5 — Provider Chart: Remove SOAP Note Tab + Care Team Tab

**File:** `templates/provider/chart.html`

The right panel currently has tabs including Documentation, SOAP Note, Lab Results, Communication, and Care Team.

**Remove the SOAP Note tab and the Care Team tab entirely.**

The tab bar should become exactly 3 tabs:
```
Documentation | Lab Results | Communication
```

- Remove the `<button>` elements for SOAP Note and Care Team from the `.right-tabs` div
- Remove the corresponding panel divs for SOAP Note content (`id="rightPanel1"`) and Care Team content (`id="rightPanel4"`)
- Renumber remaining panels to match new tab indices:
  - `rightPanel0` = Documentation (active, flex layout)
  - `rightPanel1` = Lab Results (block layout)
  - `rightPanel2` = Communication (flex layout)
- Update `switchRightTab` to loop 0–2 only
- Update `RIGHT_PANEL_FLEX` to `{0: true, 2: true}`
- Update tab button onclick values: Documentation=0, Lab Results=1, Communication=2

---

## CHANGE 6 — Provider Chart: Expandable Documentation + Resizable Middle Panel

**File:** `templates/provider/chart.html`

### 6a — Drag-to-resize handle between middle and right panels
Add a `<div id="chartDragHandle" class="chart-drag-handle"></div>` element between the middle column div and the right panel wrapper.

CSS for `.chart-drag-handle`:
- width: 4px
- cursor: col-resize
- background: #E5E0D8
- flex-shrink: 0
- transition: background 0.15s
- On hover: background #6B21A8

JS drag logic:
- On mousedown on the handle, capture starting mouse X and starting widths of middle column and right panel
- On mousemove, compute delta and apply new widths
- Min width for middle column: 280px
- Min width for right panel: 320px
- Set `document.body.style.userSelect = 'none'` during drag, restore on mouseup

### 6b — Expand/Collapse button on right panel
Add a small button in the right panel header area (next to the tabs row, aligned right):
- Label: `⤢ Expand` — clicking it adds class `panel-expanded` to the right panel wrapper
- In expanded mode: right panel width becomes 65% of chart body, middle column shrinks to 280px
- Button label changes to `⤡ Collapse` when expanded
- CSS transition: `width 0.2s ease`

### 6c — Remove overflow clipping on Documentation panel
The Documentation panel (`rightPanel0`) has `overflow:hidden` in its inline style. Change it to `overflow-y:auto` so the full form scrolls naturally. The panel should fill all available height in its flex container.

---

## CHANGE 7 — Provider Chart: Video/Audio Modality Toggle

**File:** `templates/provider/chart.html`

Add a segmented Video/Audio modality toggle in the chart header bar, to the left of the "Join Call" green button.

Design:
- Two-button pill toggle: `🎥 Video` and `📞 Audio`
- Wrapper: `.modality-toggle` — `display:flex; border:1.5px solid #6B21A8; border-radius:20px; overflow:hidden`
- Each button `.mod-btn`: `padding:5px 14px; font-size:12px; font-weight:600; border:none; cursor:pointer`
- Active state `.mod-btn.active`: `background:#6B21A8; color:#fff`
- Inactive state: `background:#fff; color:#6B21A8`
- Default: Video is active
- On click, swap active class. No other behavior needed.

---

## CHANGE 8 — Provider Chart: Routing Category Dropdown + Route-to-Individual Prompt

**File:** `templates/provider/chart.html`

### 8a — Problem Type routing dropdown
Find the existing escalate/route/redistribute button or action area in the chart. Add a **Problem Type** modal that appears when the provider clicks the route/escalate action.

The modal shows:
- Title: `"Route This Consultation"`
- A labeled dropdown: `"Problem Type"` with these options:
  - Billing Question
  - Clinical Question
  - Care Team Follow-up
  - Escalation — Urgent
  - Lab Question
  - Prescription/Refill
  - Scheduling
  - Message Individual
- A `"Route"` confirm button (purple) and `"Cancel"` button
- On confirm: show a 2-second toast `"✓ Routed to [Selected Category]"` and close modal

### 8b — Route-to-Individual prompt
When `"Message Individual"` is selected from the dropdown and Route is clicked, instead of the normal toast, show a secondary modal:

**Title:** `"Is this message related to this patient's consultation?"`

**Two buttons:**
1. `"Yes — Log to Patient Chart"` (purple) → closes modal, appends a timestamped note to the activity timeline area: `"📋 Internal message logged to patient chart — [current time]"`
2. `"No — Use Internal Messaging"` (outline) → closes modal, shows a 3-second tooltip near the nav bar: `"For general messages not related to a patient consult, use Internal Messages in the nav bar."`

---

## CHANGE 9 — Admin Portal: Provider Real-Time Scheduling Opt-In Toggle

**File:** `templates/admin/providers.html`

Find the provider detail/edit section or provider profile card area. Add a **"Consultation Availability Settings"** subsection with two iOS-style toggle switches:

**Toggle 1:**
- Label: `"Available for Real-Time / On-Demand Consultations"`
- Sub-label: `"When enabled, this provider appears in the instant-booking queue for on-demand patient requests"`
- Default: ON

**Toggle 2:**
- Label: `"Available for Scheduled Consultations"`
- Sub-label: `"When enabled, this provider accepts future scheduled appointments"`
- Default: ON

Toggle CSS (iOS-style pill):
- Wrapper: `width:44px; height:24px; border-radius:12px; position:relative; cursor:pointer`
- Active background: `#6B21A8`
- Inactive background: `#D1D5DB`
- Knob: `width:20px; height:20px; border-radius:50%; background:#fff; box-shadow:0 1px 3px rgba(0,0,0,0.2); position:absolute; top:2px; transition:left 0.2s`
- Active knob position: `left:22px`
- Inactive knob position: `left:2px`

If there is a providers list/table, add an `"Availability"` column with a green `●` dot for Real-Time enabled or gray `●` for Scheduled Only.

---

## CHANGE 10 — Admin Portal Wizard: State Configuration Matrix Format

**File:** `templates/admin/wizard.html`

Step 4 (`id="step4"`) is the State Configuration step. Replace its inner content (keep the step panel div, just replace what's inside) with a **consult modality matrix** table.

Matrix table structure:
- **Columns**: State | On-Demand | Scheduled | Async | Initial Visit Must Be Video
- **Rows**: All 50 US states, alphabetical order
- **On-Demand, Scheduled, Async columns**: checkbox per cell — checked = this modality is allowed in that state for this care product
- **Initial Visit Must Be Video**: checkbox — when checked, the first consult in that state must be video

Above the table, add per-column controls:
- `"Select All"` and `"Clear All"` links above each of the 4 checkbox columns, styled as small purple text links

Table styling:
- Row height: 32px, font-size: 12px
- NO alternating row shading — plain white rows only
- Purple checkbox accent (`accent-color: #6B21A8`)
- Sticky `<thead>` with light gray background `#F9FAFB`
- Table container: `max-height:420px; overflow-y:auto`
- Column widths: State=180px, checkbox columns=110px each

Default checkbox states:
- All states: On-Demand ✓, Scheduled ✓, Async ✓, Initial Visit Must Be Video ✗
- Exceptions — uncheck On-Demand for: Montana, North Dakota, South Dakota, Wyoming
- Exceptions — check Initial Visit Must Be Video for: New York, Texas

Below the table, add a dynamic summary line:
`"X of 50 states enabled for On-Demand · Y for Scheduled · Z for Async"` — updates live as checkboxes change.

---

## CHANGE 11 — Admin Portal Wizard: Add Portal Branding Step

**File:** `templates/admin/wizard.html`

Add a new **"Portal Branding"** step to the wizard. Insert it in the step nav after `sni1` (Select Client) and before `sni2` (Basic Info). Add a new step panel for it.

**Step nav item to insert:**
```html
<div class="step-nav-item" onclick="goToStep('branding')" id="sni_branding">
  <div class="step-num">★</div>
  <div class="step-name">Portal Branding</div>
</div>
```
Place this under the "Foundation" group label.

**Step panel** (`id="step_branding"`):

Heading: `"Portal Branding Configuration"`
Sub-text: `"Configure how patients experience this care product's portal. Controls branding at login and throughout their session."`

### Section 1 — Branding Type (3 selectable radio cards)

Card 1 — **Everlywell Branded** (default selected):
- Icon: purple EW monogram placeholder
- Description: `"Full Everlywell logo, colors, and navigation. Patient can access all Everlywell care products they are enrolled in."`

Card 2 — **Client Branded**:
- Icon: upload icon placeholder
- Description: `"Display client's logo and colors. Patient sees only care products associated with this client."`

Card 3 — **No Branding**:
- Icon: neutral circle icon
- Description: `"Neutral portal — no logo displayed. Patient sees only the care product name. For white-label and third-party network integrations."`

Selected card styling: purple border `2px solid #6B21A8`, light purple background `#F5F3FF`, checkmark badge top-right corner.
Unselected: gray border `1px solid #E5E7EB`, white background.

### Section 2 — Patient Sign-In Source URL

Label: `"Patient Sign-In Source URL"`
Sub: `"The subdomain or landing page URL that routes patients to this branded experience at login."`
Input: text field, placeholder `"e.g., quest.portal.everlywell.com or app.everlywell.com"`
Helper: `"Leave blank to use the default Everlywell portal (app.everlywell.com)"`

### Section 3 — Client Branding Fields (visible only when Card 2 is selected)

- **Logo Upload**: drag-and-drop zone, label `"Upload Client Logo (PNG or SVG, max 2MB)"`
- **Primary Brand Color**: `<input type="color">`, label `"Primary Brand Color"`, default `#6B21A8`
- **Portal Display Name**: text input, label `"Portal Name (shown to patients)"`, placeholder `"e.g., Quest Telehealth Portal"`

---

## CHANGE 12 — Patient Portal: Care Journey Tracker

**File:** `templates/patient/dashboard.html`

Add a **"Your Care Journey"** tracker card to the patient dashboard. Place it below the welcome/greeting header and above the appointments or care products section.

### Horizontal stage tracker

5 stages displayed left-to-right with connecting lines:
1. Order Placed
2. Consultation Complete
3. Provider Review ← active for demo
4. Prescription Sent
5. Complete

Per-stage visual:
- **Completed** (stages 1–2): filled circle `#6B21A8`, white `✓` inside, label below in gray `#6B7280`
- **Active** (stage 3): pulsing ring animation (CSS `@keyframes pulse`), purple outline circle, clock icon `⏱` inside, label in purple bold
- **Upcoming** (stages 4–5): hollow circle `border:2px solid #D1D5DB`, gray label

Connecting lines:
- Between completed stages: solid line `#6B21A8`, height 2px
- Between active→upcoming: dashed line `#D1D5DB`

### Status card below tracker

Light purple background `#F5F3FF`, border `1px solid #DDD6FE`, border-radius 8px, padding 12px 16px:
> `"⏱ Provider Review in Progress — Dr. Sarah Lee is reviewing your consultation notes. Estimated completion: within 4 hours."`

### SLA progress bar

Below the status card, a thin progress bar:
- Label left: `"SLA: 4 hrs"` — Label right: `"2h 24m remaining"`
- Bar: 60% filled, color `#F59E0B` (amber — approaching threshold)
- Bar background: `#FEF3C7`
- Height: 6px, border-radius 3px

**Important:** The amber color here is intentional for the patient portal demo — it shows the patient that their provider is in the later portion of the SLA window. This is separate from the provider-side SLA logic in Change 4 (which should show green because the same consult has ample time from the provider's perspective based on their configured SLA threshold).

Outer card: white background, `border:1px solid #E5E0D8`, border-radius 12px, padding 20px, margin-bottom 20px.

---

## FINAL STEP — QA Check

After completing all 12 changes, run:

```bash
python3 /Users/justin.woller/Documents/project-phoenix-demo/qa_check.py
```

Paste the full output here before finishing.
