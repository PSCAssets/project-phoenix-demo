# Project Phoenix Demo — Wizard Workflow Configuration Step v1
# June 17, 2026 — Step 11 Workflow Builder Enhancement + JS Fix
# Run this entire prompt in Claude Code from: ~/Documents/project-phoenix-demo/

---

## CONTEXT

Two things to fix in this script:
1. Diagnose and fix the JavaScript issue causing buttons to stop responding in the chart and wizard pages
2. Rebuild Step 11 (Workflow Configuration) in the admin wizard to be a fully interactive workflow stage builder

Do not modify `project_phoenix.db`. After all changes, run the QA check at the bottom.

---

## CHANGE 1 — Fix JavaScript Breakage Across Chart and Wizard Pages

**Files:** `templates/provider/chart.html` and `templates/admin/wizard.html`

Recent changes introduced JavaScript errors that are causing all buttons on these pages to stop responding. Diagnose and fix the root cause.

Check for these specific issues in BOTH files:

**A — Syntax errors:** Scan every `<script>` block for unclosed brackets, missing semicolons, undefined variables, or malformed function definitions. Fix any syntax errors found.

**B — Drag handle event leak:** If a `mousemove` event listener was added to `document` for the drag-to-resize handle, verify it is properly wrapped so it only fires during an active drag. The pattern must be:
```javascript
handle.addEventListener('mousedown', function(e) {
  // capture start state
  function onMove(e) { /* resize logic */ }
  function onUp() {
    document.removeEventListener('mousemove', onMove);
    document.removeEventListener('mouseup', onUp);
    document.body.style.userSelect = '';
  }
  document.addEventListener('mousemove', onMove);
  document.addEventListener('mouseup', onUp);
});
```
If the `removeEventListener` calls are missing or incorrect, fix them.

**C — Blocking modal overlays:** Check for any modal backdrop or overlay div (routing modal, preview modal, sign modal) that has `display:block` or `visibility:visible` in its default/initial state. All modals must default to `display:none`. Fix any that are visible by default.

**D — Z-index blocking:** Check for any element with `position:fixed` or `position:absolute` and a high `z-index` (>50) that could be overlapping interactive elements. Ensure all modal/overlay elements have `pointer-events:none` when hidden.

After diagnosing and fixing, verify the following still work by reading the file and confirming the function/handler exists:
- Right panel tab switching (`switchRightTab`)
- Route button click opens routing modal
- Left nav section links scroll to sections
- Wizard `goToStep()` function

---

## CHANGE 2 — Rebuild Step 11: Workflow Configuration (Interactive Stage Builder)

**File:** `templates/admin/wizard.html`

Replace the content inside the Step 11 panel (`id="step11"` or find by heading "Workflow Configuration") with a fully interactive workflow stage builder. Keep the step panel div wrapper and heading — only replace the inner content.

---

### Layout

Two-column layout inside the step panel:

**Left column (35% width):** Stage Library — all available stages to add  
**Right column (65% width):** Workflow Builder — the configured pipeline

---

### Section 1 — Template / Custom Toggle (keep at top)

Keep the existing two radio cards:
- **Use template** (default selected) — `"Choose from pre-built clinical workflow templates"`
- **Custom workflow** — `"Build a workflow from scratch"`

When "Use template" is selected, show a template dropdown below it:
- Standard Phone / Video
- Async Only
- Hybrid (Async + Sync)
- Chronic Care Management

When a template is selected from the dropdown, clicking a new button **`"Load Template →"`** (purple, small) auto-populates the workflow builder (right column) with the appropriate stages for that template. The stages for each template:

**Standard Phone / Video:**
1. Patient Intake (MA · SLA 2h · Required)
2. MA Review (MA · SLA 1h · Required)
3. Provider Assignment (System · SLA 30m · Required)
4. Consult — Phone/Video (Provider · SLA 24h · Required)
5. Provider Documentation (Provider · SLA 4h · Required)
6. Chart Closure (Provider · SLA 2h · Required)

**Async Only:**
1. Patient Intake (MA · SLA 2h · Required)
2. MA Review (MA · SLA 1h · Required)
3. Provider Assignment (System · SLA 30m · Required)
4. Async Review (Provider · SLA 48h · Required)
5. Provider Documentation (Provider · SLA 4h · Required)
6. Chart Closure (Provider · SLA 2h · Required)

**Hybrid (Async + Sync):**
1. Patient Intake (MA · SLA 2h · Required)
2. MA Review (MA · SLA 1h · Required)
3. Provider Assignment (System · SLA 30m · Required)
4. Async Review (Provider · SLA 48h · Required)
5. Consult — Phone/Video (Provider · SLA 24h · Optional)
6. Provider Documentation (Provider · SLA 4h · Required)
7. Chart Closure (Provider · SLA 2h · Required)

**Chronic Care Management:**
1. Patient Intake (MA · SLA 2h · Required)
2. Care Coordination Review (MA · SLA 4h · Required)
3. Provider Assignment (System · SLA 30m · Required)
4. Initial Consult — Video (Provider · SLA 24h · Required)
5. Lab Order (Provider · SLA 48h · Optional)
6. Lab Review (Provider · SLA 24h · Optional)
7. Follow-up Consult (Provider · SLA 72h · Optional)
8. Prescription/Rx (Provider · SLA 4h · Optional)
9. Provider Documentation (Provider · SLA 4h · Required)
10. Chart Closure (Provider · SLA 2h · Required)

---

### Section 2 — Left Column: Stage Library

Header: `"Available Stages"` in small caps gray label

A vertical list of stage cards. Each card:
- Background: white, border `1px solid #E5E7EB`, border-radius 8px, padding 10px 14px
- Stage name (bold, `#1F2937`)
- Role badge (small pill: gray bg, e.g., "MA", "Provider", "System", "Patient")
- A `"+ Add"` button (small, purple outline) on the right — clicking it adds the stage to the workflow builder
- If the stage is already in the workflow, the `"+ Add"` button changes to `"✓ Added"` (green text, no border) and is disabled

Available stages in the library:
1. Patient Intake — MA
2. Identity Verification — Patient
3. Insurance Verification — MA
4. MA Review — MA
5. Provider Assignment — System
6. Async Review — Provider
7. Consult — Phone/Video — Provider
8. Consult — Video Only — Provider
9. Lab Order — Provider
10. Lab Review — Provider
11. Prescription/Rx — Provider
12. Referral — Provider
13. Follow-up Consult — Provider
14. Care Coordination Review — MA
15. Patient Education — MA
16. Provider Documentation — Provider
17. Chart Closure — Provider

---

### Section 3 — Right Column: Workflow Builder

Header: `"Configured Workflow"` in small caps gray label + stage count badge (e.g., `"6 stages"`) + a `"Clear All"` link (red text, small, right-aligned)

The workflow is displayed as a vertical ordered list of stage cards. Each stage card:

```
┌─────────────────────────────────────────────────────┐
│  ⠿  [1]  Patient Intake                  [MA]  [×]  │
│       SLA: [  2  ] hrs   ○ Required  ○ Optional      │
└─────────────────────────────────────────────────────┘
        ↓ (connector arrow between stages)
┌─────────────────────────────────────────────────────┐
│  ⠿  [2]  MA Review                       [MA]  [×]  │
│       SLA: [  1  ] hrs   ● Required  ○ Optional      │
└─────────────────────────────────────────────────────┘
```

Stage card details:
- `⠿` drag handle icon on left (cursor: grab) — drag to reorder stages
- Stage number badge (auto-numbered, updates when reordered)
- Stage name (bold)
- Role badge (purple pill: `#EDE9FE` bg, `#6B21A8` text)
- `[×]` remove button on right (gray, turns red on hover)
- Below the name: SLA input (`<input type="number" min="1" max="720">` with "hrs" label) and Required/Optional radio buttons
- Stage card: white bg, border `1px solid #E5E7EB`, border-radius 8px, padding 12px 16px, margin-bottom 4px
- Connector arrow between cards: a centered downward arrow `↓` in gray `#9CA3AF`

**Drag-to-reorder:** Use HTML5 drag-and-drop (`draggable="true"` on each card). On dragstart, store the dragged index. On dragover, show a blue insertion line. On drop, reorder the array and re-render. After reorder, update all stage numbers.

**SLA input:** When the user changes the SLA hours value, update the stage's SLA in the in-memory workflow array. Validate: minimum 1, maximum 720.

**Required/Optional toggle:** Radio buttons. Required stages cannot be removed (disable the `[×]` button and show a tooltip "Required stages cannot be removed"). Optional stages can be removed.

If the workflow is empty, show a placeholder: `"No stages configured. Load a template or add stages from the library."` in gray italic.

---

### Section 4 — Workflow Summary Bar

Below the two columns, a summary bar showing:
`"Total stages: 6  ·  Est. total SLA: 33h 30m  ·  Roles involved: MA, Provider, System"`

This updates dynamically as stages are added, removed, or SLA values are changed.

---

### Section 5 — Workflow Simulation (bottom)

Keep the existing simulation section but make it functional.

Header: `"Workflow Simulation — Patient: Marcus Johnson · CST-2026-10849 · Testosterone Care"`

The simulation shows a horizontal stage tracker (same visual style as the patient portal Care Journey tracker):
- All configured stages shown left-to-right as circles with names
- The current active stage is highlighted in purple
- Completed stages show a `✓` checkmark
- Upcoming stages are gray

**Controls:**
- `"Complete stage & advance →"` button (purple) — advances the simulation to the next stage, marks current as complete, highlights next
- `"↺ Reset"` button (outline) — resets all stages back to the first stage

**Stage detail card** (appears below the tracker for the active stage):
```
Currently Active: [Stage Name]
Role: [MA / Provider / System]
SLA: [X hours]
Status: In Progress
Description: [brief role-appropriate description]
```

Stage descriptions to use:
- Patient Intake: "MA collects patient demographics, verifies identity, and confirms insurance eligibility"
- MA Review: "MA reviews intake submission, flags clinical gaps, and prepares chart for provider"
- Provider Assignment: "System matches patient to available provider based on licensure, availability, and care product rules"
- Async Review: "Provider reviews patient submission asynchronously and documents clinical findings"
- Consult — Phone/Video: "Provider conducts live consultation with patient via phone or video"
- Lab Order: "Provider orders required diagnostic labs through the integrated lab network"
- Lab Review: "Provider reviews returned lab results and updates assessment and plan"
- Prescription/Rx: "Provider submits prescription through integrated pharmacy network"
- Follow-up Consult: "Provider conducts follow-up consultation to review progress and adjust care plan"
- Provider Documentation: "Provider completes SOAP note, updates assessment and plan, and prepares chart for closure"
- Chart Closure: "Provider finalizes and signs chart, triggering billing submission and patient notification"

The simulation should pull the stages from the current workflow builder configuration — if the workflow has been customized, the simulation reflects those custom stages. If no stages are configured, show: `"Configure your workflow above to run the simulation."`

---

## FINAL STEP — QA Check

After completing all changes, run:

```bash
python3 /Users/justin.woller/Documents/project-phoenix-demo/qa_check.py
```

Paste the full output here before finishing.
