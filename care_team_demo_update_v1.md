# Project Phoenix Demo — Care Team Demo Update v1
# June 18, 2026 — Care Team session changes + Admin Portal wizard fix
# Run this entire prompt in Claude Code from: ~/Documents/project-phoenix-demo/

---

## CONTEXT

This script applies demo changes from the June 18 Care Team session and fixes a broken Admin Portal wizard flow. All edits are to existing Flask/Jinja2 HTML templates in `~/Documents/project-phoenix-demo/templates/`. Do not modify `project_phoenix.db`. After all changes, run the QA check at the bottom.

---

## CHANGE 1 — Add Zendesk Tab to Patient Chart Right Panel

**File:** `templates/provider/chart.html`

The right panel currently has 2 tabs: Documentation | Communication (after chart_ux_update_v1.md applied Lab Results removal).

Add a third tab: **Zendesk**

Updated tab order:
```
Documentation | Communication | Zendesk
```

**Tab button:**
- Label: `"🎫 Zendesk"`
- Same style as other tab buttons (white/gray when inactive, purple bottom border when active)
- `onclick="switchRightTab(2)"` (Communication becomes tab 1, Zendesk becomes tab 2)

**Zendesk panel content (`id="rightPanel2"`):**

```
┌─────────────────────────────────────────────────────────────────┐
│  🎫  Zendesk — Active Case                              [Refresh]│
├─────────────────────────────────────────────────────────────────┤
│  Case #: ZD-293847                                               │
│  Type:   Consult Support                                         │
│  Status: ● Open                                                  │
│  Assigned Agent: Beth Lewis                                      │
├─────────────────────────────────────────────────────────────────┤
│  Last Agent Note (2h ago):                                       │
│  "Patient called re: consult timeline. Advised 24–48hr window.  │
│  Patient confirmed availability for video this week."            │
│                                                                  │
│  [View Full Case in Zendesk ↗]                                   │
├─────────────────────────────────────────────────────────────────┤
│  ✦ Add Note to Case                                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Type a note to sync to Zendesk...                        │   │
│  └──────────────────────────────────────────────────────────┘   │
│  [Add Note]                                                      │
└─────────────────────────────────────────────────────────────────┘
```

**Implementation details:**

- Panel background: white
- Section header: gray `#6B7280`, small caps, 11px
- Case # and fields: bold labels `#374151`, values `#1F2937`
- Status pill: green dot + "Open" in `#059669`, small pill `#D1FAE5` bg
- Agent name: `#374151`
- Last Agent Note: light background `#F9FAFB`, border-radius 6px, padding 12px, italic text `#4B5563`
- "View Full Case in Zendesk ↗" link: `#6B21A8`, text-decoration underline on hover
- "Add Note" textarea: full-width, border `1px solid #E5E7EB`, border-radius 6px, min-height 80px, placeholder text gray
- "Add Note" button: purple, small, on click shows toast: `"✓ Note synced to Zendesk case ZD-293847"` for 2 seconds

Update `switchRightTab` to loop 0–2. Update `RIGHT_PANEL_FLEX` to `{0: true, 1: true, 2: true}`.

---

## CHANGE 2 — Add Real-Time Queue Button to Scheduling Interface

**File:** `templates/provider/schedule.html` (or whichever template contains the scheduling/queue view for providers)

In the scheduling interface, add a prominent **"+ Add to Real-Time Queue"** button that allows an agent to place a patient into the on-demand queue during an active call.

**Button placement:** At the top of the scheduling interface, in the header bar area, to the right of the page title. Or, if there is a patient card or consult detail area, add it as a secondary action button there.

**Button style:**
- Label: `"⚡ Add to Real-Time Queue"`
- Style: purple filled, border-radius 8px, padding 10px 20px, font-weight 600
- Or orange/amber if purple is already used for primary actions in this view — use `#D97706` bg, white text if so

**On click:** Show a confirmation modal:

```
┌─────────────────────────────────────────────────────────────┐
│  Add Patient to Real-Time Queue                         [✕]  │
├─────────────────────────────────────────────────────────────┤
│  Patient: Marcus Johnson                                      │
│  Care Product: Testosterone Care                             │
│                                                              │
│  Adding this patient to the real-time queue will notify      │
│  available providers immediately.                            │
│                                                              │
│  Estimated wait: ~8 minutes                                  │
│                                                              │
│  Agent note (optional):                                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ e.g., patient is on hold and ready to connect...     │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│                        [Cancel]  [Add to Queue]              │
└─────────────────────────────────────────────────────────────┘
```

On "Add to Queue" confirm: show green toast `"✓ Marcus Johnson added to real-time queue — providers notified"` for 3 seconds.

---

## CHANGE 3 — Display Client Name in Care Team Agent Interface

**File:** `templates/provider/queue.html` (or the Care Team queue view — whichever template shows the list of consults/cases in the agent's working queue)

Each consult row in the Care Team queue must show a **client name badge** so agents know which client program the consult belongs to.

**Where to add it:** On each consult row card, add a client name badge near the consult type or patient name. It should be visually distinct so agents can quickly scan by client.

**Badge design:**
- Small pill/badge, rounded, 11px font, font-weight 600
- Color-coded per client:
  - `DXS` → purple bg `#EDE9FE`, text `#6B21A8`
  - `LabCorp` → blue bg `#DBEAFE`, text `#1D4ED8`
  - `Everlywell` → green bg `#D1FAE5`, text `#065F46`
  - `PWN Health` → orange bg `#FEF3C7`, text `#92400E`
  - Default/Other → gray bg `#F3F4F6`, text `#374151`

**For demo data:** Apply client badges to existing queue rows. Assign clients as follows (use whatever patient names/consults exist in the current queue):
- First 2 rows: `DXS`
- Next 2 rows: `LabCorp`
- Remaining rows: `Everlywell`

Place the badge on the right side of the patient name, or directly below the consult type label — whichever fits better in the existing card layout.

---

## CHANGE 4 — Fix Admin Portal Wizard "Save & Continue" on Step 1

**File:** `templates/admin/wizard.html`

The "Save & Continue" button on Step 1 of the Admin Portal care product wizard is grayed out and not responding to clicks. Diagnose and fix.

**Likely causes — check in this order:**

**A — Button disabled attribute stuck:** The button has `disabled` attribute or `pointer-events: none` CSS set and is never being removed/unset. Check:
```javascript
// Look for any code that sets the button disabled and confirm the enable logic runs
// Pattern to look for:
document.getElementById('saveBtn1').disabled = true; // Is there corresponding code to enable it?
```
Fix: Ensure the enable/disable logic is triggered correctly. If the button is disabled pending form validation, confirm the validation function runs on DOMContentLoaded and properly enables the button if the required fields have default values.

**B — JavaScript error preventing execution:** An uncaught JS error in an earlier script block may be preventing the button's click handler from being attached. Check for syntax errors in the `<script>` blocks above the Step 1 button definition.

**C — Form validation required fields:** Step 1 may require certain fields to be filled before the button enables. If the form validation is checking required fields that don't have default values, pre-fill them with demo defaults:
- Care Product Name: `"Testosterone Care"`
- Product Code: `"TC-001"`
- Category: `"Men's Health"` (or whatever the first select option is)
- Status: `"Active"`

**D — Missing event listener:** The button may be missing its click event listener entirely (perhaps accidentally removed in a previous edit). Confirm a click handler exists:
```javascript
document.getElementById('saveStep1').addEventListener('click', function() {
  goToStep(2); // or however step navigation works
});
```
If missing, add it.

After fixing, verify:
- Step 1 "Save & Continue" is clickable and advances to Step 2
- All subsequent step navigation still works (goToStep, back buttons)
- The Step 11 workflow builder (from wizard_workflow_step_v1.md) still functions

---

## FINAL STEP — QA Check

After completing all changes, run:

```bash
python3 /Users/justin.woller/Documents/project-phoenix-demo/qa_check.py
```

Paste the full output here before finishing.
