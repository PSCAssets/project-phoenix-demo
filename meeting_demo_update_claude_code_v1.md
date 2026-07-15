# Project Phoenix Demo — Meeting Update Script
# June 17, 2026 — 9 Changes from Demo Review Meeting
# Run this entire prompt in Claude Code from: ~/Documents/project-phoenix-demo/

---

## CONTEXT

This script implements 9 changes from the June 17 Project Phoenix demo review meeting. All edits are to existing Flask/Jinja2 HTML templates in `~/Documents/project-phoenix-demo/templates/`. Do not modify `project_phoenix.db`. After all changes, run the QA check at the bottom.

---

## CHANGE 1 — Provider Queue: Add Patient Identifiers (DOB, Gender, Full Name)

**File:** `templates/provider/queue.html`

Currently the patient name column shows initials only (e.g., "M.J."). Update every patient row in the queue table to show:
- **Full name** (e.g., "Marcus Johnson") as the clickable link instead of initials
- **DOB** below the name in smaller text (e.g., "DOB: 04/12/1985")
- **Gender** as a small badge next to DOB (e.g., "M" or "F" in a pill)

The `.patient-dob` CSS class already exists. Use it for DOB. Add a `.patient-gender` badge styled as a small rounded pill: gray background `#E5E7EB`, text `#374151`, font-size 10px, padding 1px 6px.

Replace the initials in all patient rows with realistic full names matching the care product context. Keep all existing href links, care product badges, and action buttons exactly as-is. Only the name cell changes.

Use these name/demo mappings (keep same row order):
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

## CHANGE 2 — Provider Chart: Remove SOAP Note Tab + Care Team Tab

**File:** `templates/provider/chart.html`

The right panel currently has 4 tabs (after previous fixes): Documentation, SOAP Note, Lab Results, Communication, Care Team.

**Remove the SOAP Note tab and the Care Team tab entirely.**

The tab bar should become exactly 3 tabs:
```
Documentation | Lab Results | Communication
```

- Remove the `<button>` for SOAP Note (index 1) and Care Team (index 4) from the `.right-tabs` div
- Remove the corresponding panel divs: `id="rightPanel1"` (SOAP Note content) and `id="rightPanel4"` (Care Team content)
- Renumber remaining panels so they match the new tab indices:
  - `rightPanel0` = Documentation (keep as-is, already index 0, active)
  - `rightPanel1` = Lab Results (was rightPanel2)
  - `rightPanel2` = Communication (was rightPanel3)
- Update `switchRightTab` to loop 0–2 only and update `RIGHT_PANEL_FLEX` to `{0: true, 2: true}` (Documentation and Communication use flex)
- Update the `DOMContentLoaded` call to `switchRightTab(0)` (unchanged)
- Update tab button onclick indices: Documentation=0, Lab Results=1, Communication=2

---

## CHANGE 3 — Provider Chart: Expandable Documentation + Resizable Middle Panel

**File:** `templates/provider/chart.html`

The chart has a 3-column layout: left sidebar | middle content | right panel. The right panel (Documentation/Labs/Communication) is too small for providers to work in comfortably.

### 3a — Resizable middle/right divider
Add a vertical drag handle between the middle column and the right panel. Implementation:
- Add a `<div id="chartDragHandle" class="chart-drag-handle"></div>` between the middle column div and the right panel wrapper div
- CSS for `.chart-drag-handle`: width 4px, cursor col-resize, background #E5E0D8, flex-shrink 0, hover background #6B21A8 with transition
- Add JS drag logic: on mousedown on the handle, track mousemove to resize the middle column and right panel widths proportionally. Store the initial widths and apply delta. Min width for middle: 280px, min width for right: 320px. Use `user-select: none` on body during drag.

### 3b — Right panel expand/collapse button
Add an expand button `⤢` (or `⬡`) in the right panel header area (next to the tab buttons). When clicked:
- Toggles a CSS class `expanded` on the right panel wrapper
- In expanded mode: right panel takes up `65%` of the chart body width, middle column shrinks to its minimum (280px)
- Button label toggles between `⤢ Expand` and `⤡ Collapse`
- Add smooth CSS transition `width 0.2s ease`

### 3c — Remove fixed height constraints on Documentation panel
The Documentation panel (`rightPanel0`) currently has `padding:0;overflow:hidden`. Change `overflow:hidden` to `overflow-y:auto` so the full form content is scrollable and not clipped. Ensure the panel's flex column fills the available height without a hard cap.

---

## CHANGE 4 — Provider Chart: Video/Audio Modality Toggle

**File:** `templates/provider/chart.html`

In the chart header area (near the "Join Call" green button), add a Video/Audio toggle button. This represents the provider switching modality during an active consult.

Design:
- A segmented toggle: `🎥 Video | 📞 Audio` — two buttons side-by-side styled as a pill toggle
- Default state: Video is active (purple background `#6B21A8`, white text)
- When Audio is clicked: Audio gets active style, Video goes inactive (gray border, gray text)
- CSS class `.modality-toggle` wrapper with `display:flex; border:1.5px solid #6B21A8; border-radius:20px; overflow:hidden`
- Each button: `.mod-btn` with padding `5px 14px`, font-size 12px, font-weight 600, no border, cursor pointer
- Active `.mod-btn.active`: background `#6B21A8`, color white
- Inactive: background white, color `#6B21A8`
- On click, swap active class between the two buttons. No other logic needed.

Place the toggle in the chart header bar, to the left of the "Join Call" button.

---

## CHANGE 5 — Provider Chart: Routing Category Dropdown + Patient Message Prompt

**File:** `templates/provider/chart.html`

### 5a — Routing dropdown
There is an existing escalate/route button or action area in the chart (look for "escalat", "route", "redistribute", or the patient action buttons near the left sidebar or middle panel). Find the routing/escalation action and add a **Problem Type** dropdown that appears when the provider initiates a route/escalation.

The dropdown options are:
- Billing Question
- Clinical Question
- Care Team Follow-up
- Escalation — Urgent
- Lab Question
- Prescription/Refill
- Scheduling

When a category is selected and "Route" is confirmed, show a brief success toast: `"✓ Routed to [Category]"` for 2 seconds.

### 5b — Route-to-Individual prompt
If there is any "message staff" or "message team member" action in the chart context (or if you add a "Message Individual" option to the routing area), add a modal prompt:

**Prompt text:**
> "Is this message related to **[Patient Name]**'s consultation?"
>
> **Yes, log to patient chart** → closes modal, adds a note to the activity timeline area: `"📋 Internal message logged to patient chart — [timestamp]"`
>
> **No — use Internal Messaging** → closes modal and shows a tooltip: `"For general messages not related to a patient consult, use Internal Messages in the nav bar."`

Style the modal with the existing purple brand color scheme. Add a "Message Individual" option to the routing dropdown (as the last item) to trigger this prompt.

---

## CHANGE 6 — Admin Portal: Provider Real-Time Scheduling Opt-In Toggle

**File:** `templates/admin/providers.html`

Find the provider detail/edit section or provider profile card. Add a new configuration row labeled **"Real-Time Availability"** with a toggle switch.

Design:
- Section label: `"Consultation Availability Settings"` (add as a subsection if editing an individual provider)
- Toggle label: `"Available for Real-Time / On-Demand Consultations"`
- Sub-label: `"When enabled, this provider appears in the instant-booking queue for on-demand patient requests"`
- Toggle: standard iOS-style toggle switch using CSS — pill shape, 44px wide, 24px tall. Active = purple `#6B21A8`. Inactive = gray `#D1D5DB`. Knob is white circle with shadow.
- Default state: ON for demo
- Add a second toggle below it: `"Available for Scheduled Consultations"` — default ON
- These two toggles can be independent.

If there is a table of providers, add an "Availability" column showing a green `●` (Real-Time) or gray `●` (Scheduled Only) indicator per row.

---

## CHANGE 7 — Admin Portal Wizard: Enhance State Configuration to Matrix Format

**File:** `templates/admin/wizard.html`

Step 4 (`id="step4"`) is currently the State Configuration step. Replace its content with a **consult modality matrix** format.

The new matrix table:
- **Header row**: State | On-Demand | Scheduled | Async | Initial Visit Must Be Video
- Each data row = one US state (include all 50 states)
- **On-Demand, Scheduled, Async**: each cell is a checkbox (checked = allowed in that state for this care product)
- **Initial Visit Must Be Video**: last column, single checkbox — when checked, forces first consult in that state to be video modality
- **Select All / Unselect All** buttons above each of the 4 checkbox columns
- Default all checkboxes to checked for demo purposes, except:
  - Montana, North Dakota, South Dakota, Wyoming: uncheck On-Demand (these are low-volume states)
  - Texas: check "Initial Visit Must Be Video"
  - New York: check "Initial Visit Must Be Video"

Table styling:
- Compact rows: row height 32px, font-size 12px
- Alternating... actually NO alternating row shading (plain white rows only)
- Purple checkbox accent color matching brand
- Sticky header row
- Table is scrollable within the step panel (max-height 420px, overflow-y auto)
- Column widths: State = 180px, each checkbox column = 110px

Add a summary line below the table: `"X of 50 states enabled for On-Demand · Y for Scheduled · Z for Async"` that updates dynamically as checkboxes are toggled.

---

## CHANGE 8 — Admin Portal Wizard: Add Branding Configuration Step

**File:** `templates/admin/wizard.html`

Add a new step **"Portal Branding"** to the wizard, positioned after Step 1 (Select Client) and before Step 2 (Basic Info). This means the existing steps 2–18 shift up by one (become 3–19). You only need to add the step nav item and step panel — do not need to renumber all existing panels if the `goToStep` function handles it by ID.

**New step nav item** (insert after sni1, before sni2):
```
Portal Branding
```
Group label: keep under "Foundation"

**New step panel content** (`id="step_branding"` or insert as new step 2):

**Heading:** `Step — Portal Branding`
**Sub:** `Configure how patients experience this care product's portal. Branding controls what they see at login and throughout their session.`

### Section 1: Branding Type
Three radio card options (styled as selectable cards with border, checkmark on selection):

1. **Everlywell Branded** — `"Full Everlywell logo, colors, and navigation. Patient can see all Everlywell care products they are enrolled in."` — Show small Everlywell logo placeholder
2. **Client Branded** — `"Display client's logo and colors. Patient sees only care products associated with this client."` — Show upload logo placeholder + color picker field
3. **No Branding** — `"Neutral portal with no logo. Patient sees only the care product name. Used for white-label and third-party network integrations."`

Default selection: Everlywell Branded

### Section 2: Patient Sign-In Source
Label: `"Patient Sign-In Source URL"`
Sub-label: `"The subdomain or landing page URL patients use to access this care product's portal. This determines which branding experience is loaded at login."`
Input field: text input, placeholder `"e.g., quest.portal.everlywell.com or app.everlywell.com"`
Below input: `"Leave blank to use the default Everlywell portal URL"`

### Section 3: Client Branding Fields (shown only when "Client Branded" is selected)
- Logo Upload: file input styled as drag-drop zone `"Upload client logo (PNG, SVG — max 2MB)"`
- Primary Color: color picker input, label `"Primary Brand Color"`, default `#6B21A8`
- Portal Display Name: text input, label `"Portal Name shown to patients"`, placeholder `"e.g., Quest Telehealth Portal"`

---

## CHANGE 9 — Patient Portal: Prescription / Care Journey Tracker

**File:** `templates/patient/dashboard.html`

Add a **"Your Care Journey"** tracker section to the patient dashboard. This is a visual "Domino's-style" status tracker showing where the patient is in their current care product workflow.

**Placement:** Add as a prominent card/section near the top of the dashboard, below the welcome header but above the appointments section.

**Design — horizontal step tracker:**

```
[✓] Order        [✓] Consultation    [⟳] Provider      [ ] Prescription    [ ] Complete
    Placed           Complete            Review              Sent
```

- Steps: `Order Placed` → `Consultation Complete` → `Provider Review` → `Prescription Sent` → `Complete`
- Each step is a circle with icon + label below
- **Completed steps**: filled purple circle `#6B21A8` with white checkmark `✓`
- **Current/active step**: pulsing purple ring animation, showing `⟳` or clock icon, label in purple bold
- **Upcoming steps**: gray empty circle, gray label
- Connecting lines between circles: solid purple for completed segments, dashed gray for upcoming
- For demo: set "Provider Review" as the active step (steps 1 and 2 complete, steps 4 and 5 pending)

**Below the tracker:** A status message in a light purple card:
> `"⏱ Provider Review in Progress — Dr. Sarah Lee is reviewing your consultation. Estimated completion: within 4 hours."`

**SLA indicator:** A thin progress bar below the status message showing time elapsed vs. SLA. For demo: 60% filled (amber color `#F59E0B`), label `"SLA: 4 hrs · 2h 24m remaining"`

Style the entire tracker card with white background, subtle border `1px solid #E5E0D8`, border-radius 12px, padding 20px.

---

## FINAL STEP — QA Check

After completing all 9 changes, run:

```bash
python3 /Users/justin.woller/Documents/project-phoenix-demo/qa_check.py
```

Paste the full output here before finishing.
