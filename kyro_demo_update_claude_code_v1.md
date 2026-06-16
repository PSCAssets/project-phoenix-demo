# Project Phoenix — Demo Update: Kyro Gap Requirements
# Claude Code Build Prompt — v1

## Context

You are updating the Project Phoenix demo Flask app located at `~/Documents/project-phoenix-demo/`. This is a prototype demo with Flask routes, Jinja2 templates, and an existing visual design system. The goal is to make all 31 new requirements from the Kyro Gap Analysis visible and reviewable in the demo — no backend logic required, all changes are UI/mockup level.

**Design System to match:**
- Primary purple: `#6B21A8`
- Green: `#00A67E`
- Background: `#FAF7F2`
- Border: `#E5E0D8`
- Cards: `background:#fff; border:1px solid #E5E0D8; border-radius:10px; padding:20px`
- Font: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif`
- Never use alternating row shading — all table rows use plain white backgrounds

---

## AREA 1 — chart_video.html (14 requirements)

**File:** `templates/provider/chart_video.html`

### 1A. VID-001 — Join Window Countdown Banner
Above the video placeholder `div.video-placeholder`, add a status banner that shows:
```
⏱ Join window opens in 8 minutes — Patient tech check: ✅ Passed
```
Style: `background:#EFF6FF; border:1px solid #BFDBFE; border-radius:8px; padding:10px 16px; font-size:13px; color:#1D4ED8; margin-bottom:12px;`
Include a small "Re-send visit link via SMS" button (right-aligned, `font-size:11px; color:#6B21A8`) — this satisfies **VID-005**.

### 1B. VID-004 — Patient Tech Check Status Bar
Inside the join window banner (or directly below it), add a row of 4 status chips:
- ✅ Registration Complete
- ✅ Intake Submitted  
- ✅ Tech Check Passed
- ⏳ Patient Not Yet Joined

Style for chips: `display:inline-flex; align-items:center; gap:4px; background:#F0FDF4; border:1px solid #BBF7D0; color:#166534; font-size:11px; font-weight:600; padding:3px 10px; border-radius:20px; margin:2px`
For pending/failed: `background:#FEF2F2; border-color:#FECACA; color:#991B1B`

### 1C. VID-006 — Audio Fallback Button
In the `.video-controls-bar` inside `div#joinedOverlay`, add after the Share Screen button:
```html
<button class="btn btn-outline" onclick="switchToPhone()">📞 Switch to Phone</button>
```
Add a JS function `switchToPhone()` that shows an alert: `"Switching to phone fallback — patient will receive an automated call to (555) 867-5309"`.

### 1D. VID-002 — End-State Selector Modal
Replace the current `closeChart()` JS function behavior. When the provider clicks "Complete & Close Chart →", instead of showing the success banner immediately, show a modal overlay with three closure options:

Modal HTML (append before `{% endblock %}`):
```html
<div id="endStateModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:300;display:none;align-items:center;justify-content:center;">
  <div style="background:#fff;border-radius:12px;padding:28px;width:480px;max-width:90vw;">
    <div style="font-size:16px;font-weight:700;color:#111827;margin-bottom:6px;">Close Visit — Select Outcome</div>
    <div style="font-size:13px;color:#6B7280;margin-bottom:20px;">CST-2026-10849 · Marcus Johnson · Video Visit</div>
    <div style="display:flex;flex-direction:column;gap:10px;">
      <button onclick="closeVisit('completed')" style="background:#ECFDF5;border:1px solid #6EE7B7;color:#065F46;padding:14px 16px;border-radius:8px;text-align:left;cursor:pointer;font-size:13px;font-weight:600;">✅ Completed — Visit conducted and documented</button>
      <button onclick="closeVisit('noshow')" style="background:#FEF3C7;border:1px solid #FCD34D;color:#92400E;padding:14px 16px;border-radius:8px;text-align:left;cursor:pointer;font-size:13px;font-weight:600;">🚫 No-Show — Patient did not join within window</button>
      <button onclick="closeVisit('tech')" style="background:#FEF2F2;border:1px solid #FECACA;color:#991B1B;padding:14px 16px;border-radius:8px;text-align:left;cursor:pointer;font-size:13px;font-weight:600;">🔧 Tech Issue — Visit could not be completed due to technical failure</button>
    </div>
    <div style="margin-top:16px;text-align:right;">
      <button onclick="document.getElementById('endStateModal').style.display='none'" style="background:none;border:none;color:#6B7280;cursor:pointer;font-size:13px;">Cancel</button>
    </div>
  </div>
</div>
```

JS:
```js
function closeChart() {
  document.getElementById('endStateModal').style.display = 'flex';
}
function closeVisit(state) {
  document.getElementById('endStateModal').style.display = 'none';
  const messages = {
    completed: '✅ Visit documented as Completed. Chart closed for CST-2026-10849.',
    noshow: '🚫 No-Show recorded. Appointment slot released for rebooking. Patient notification queued.',
    tech: '🔧 Tech Issue logged. Visit marked for rescheduling. IT ticket auto-created.'
  };
  const banner = document.getElementById('successBanner');
  banner.textContent = messages[state];
  banner.classList.add('show');
  setTimeout(() => banner.classList.remove('show'), 5000);
}
```

This covers **VID-002** (end states) and **VID-003** (no-show workflow messaging).

### 1E. NOTE-001 — In-Visit Notepad Tab
In the right-side card (Session Notes), replace the single textarea with a two-tab interface:

```
[📋 Clinical Note] [📝 Scratchpad]
```

**Tab 1 — Clinical Note** (existing SOAP textarea)  
**Tab 2 — Scratchpad**: Plain textarea with placeholder: `"Quick notes, reminders, follow-up items — not included in the official chart record..."`
Style scratchpad background as `#FFFBEB` (light yellow) to visually differentiate from the official note.

Add tab-switching JS. Active tab style: `border-bottom:2px solid #6B21A8; color:#6B21A8; font-weight:700`

### 1F. AI-011 — Ambient Transcript Capture Toggle
In the call controls bar (`.call-controls` div, below the video), add after the Share Screen button:
```html
<button class="btn btn-outline-dark" id="ambientBtn" onclick="toggleAmbient(this)" style="font-size:12px;padding:6px 12px;">🎙 Ambient Off</button>
```
JS:
```js
let ambientOn = false;
function toggleAmbient(btn) {
  ambientOn = !ambientOn;
  btn.textContent = ambientOn ? '🎙 Ambient On' : '🎙 Ambient Off';
  btn.style.background = ambientOn ? '#EDE9FE' : '';
  btn.style.color = ambientOn ? '#6B21A8' : '';
  btn.style.borderColor = ambientOn ? '#A78BFA' : '';
}
```

### 1G. AI-008/009/010 — AI Scribe Section
Below the notes card, add a new card (collapsed by default, expands after `endVideoCall()` is called):

```html
<div id="aiScribeCard" style="display:none;margin-top:12px;" class="card">
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
    <span style="font-size:14px;font-weight:700;color:#111827;">🤖 AI Scribe — Note Draft</span>
    <span id="aiScribeStatus" style="font-size:11px;font-weight:600;background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:12px;">Generating...</span>
  </div>
  <div id="aiScribeContent" style="display:none;">
    <div style="font-size:11px;font-weight:700;color:#6B7280;margin-bottom:4px;">SUBJECTIVE</div>
    <div style="background:#F0F9FF;border:1px solid #BAE6FD;border-radius:6px;padding:10px;font-size:13px;color:#374151;margin-bottom:8px;font-style:italic;">Patient reports fatigue and low energy over the past 3 months. Denies chest pain or shortness of breath. Current on testosterone therapy.</div>
    <div style="font-size:11px;font-weight:700;color:#6B7280;margin-bottom:4px;">OBJECTIVE</div>
    <div style="background:#F0F9FF;border:1px solid #BAE6FD;border-radius:6px;padding:10px;font-size:13px;color:#374151;margin-bottom:8px;font-style:italic;">Patient presented via video visit. Appears in no acute distress. Labs reviewed: T levels within therapeutic range.</div>
    <div style="font-size:11px;font-weight:700;color:#6B7280;margin-bottom:4px;">ASSESSMENT</div>
    <div style="background:#F0F9FF;border:1px solid #BAE6FD;border-radius:6px;padding:10px;font-size:13px;color:#374151;margin-bottom:8px;font-style:italic;">Testosterone deficiency, managed. Fatigue likely related to sleep disruption. Continue current protocol.</div>
    <div style="font-size:11px;font-weight:700;color:#6B7280;margin-bottom:4px;">PLAN</div>
    <div style="background:#F0F9FF;border:1px solid #BAE6FD;border-radius:6px;padding:10px;font-size:13px;color:#374151;margin-bottom:16px;font-style:italic;">Continue testosterone therapy. Recheck in 90 days. Patient education on sleep hygiene provided.</div>
    <div style="display:flex;gap:8px;align-items:center;">
      <span id="aiNoteState" style="font-size:11px;font-weight:600;background:#FEF3C7;color:#92400E;padding:2px 10px;border-radius:12px;">Draft — Not Signed</span>
      <button onclick="approveAiNote()" style="background:#6B21A8;color:#fff;border:none;border-radius:6px;padding:6px 14px;font-size:12px;font-weight:600;cursor:pointer;">✅ Accept & Copy to Note</button>
      <button onclick="rejectAiNote()" style="background:#fff;border:1px solid #E5E0D8;color:#374151;border-radius:6px;padding:6px 14px;font-size:12px;font-weight:600;cursor:pointer;">✕ Discard Draft</button>
    </div>
  </div>
</div>
```

In `endVideoCall()`, add:
```js
document.getElementById('aiScribeCard').style.display = 'block';
setTimeout(() => {
  document.getElementById('aiScribeStatus').textContent = 'Draft Ready';
  document.getElementById('aiScribeStatus').style.background = '#DCFCE7';
  document.getElementById('aiScribeStatus').style.color = '#166534';
  document.getElementById('aiScribeContent').style.display = 'block';
}, 2000);
```

Add functions:
```js
function approveAiNote() {
  document.getElementById('aiNoteState').textContent = 'Accepted — Pending Signature';
  document.getElementById('aiNoteState').style.background = '#DCFCE7';
  document.getElementById('aiNoteState').style.color = '#166534';
}
function rejectAiNote() {
  document.getElementById('aiScribeCard').style.display = 'none';
}
```

### 1H. TRANS-001/002 — Live Translation Toggle
In the call controls bar, after the Ambient button, add:
```html
<div style="display:flex;align-items:center;gap:6px;margin-left:4px;">
  <button class="btn btn-outline-dark" id="transBtn" onclick="toggleTranslation()" style="font-size:12px;padding:6px 12px;">🌐 Translation Off</button>
  <select id="transLang" style="display:none;border:1px solid #E5E0D8;border-radius:6px;font-size:12px;padding:5px 8px;background:#fff;" onchange="selectLanguage(this)">
    <option value="">Select language...</option>
    <option value="es">Spanish</option>
    <option value="fr">French</option>
    <option value="zh">Mandarin</option>
    <option value="ar">Arabic</option>
    <option value="vi">Vietnamese</option>
  </select>
</div>
```
```js
function toggleTranslation() {
  const btn = document.getElementById('transBtn');
  const sel = document.getElementById('transLang');
  const isOn = btn.textContent.includes('Off');
  if (isOn) {
    btn.textContent = '🌐 Translation On';
    btn.style.background = '#EDE9FE';
    btn.style.color = '#6B21A8';
    sel.style.display = 'inline-block';
    // BAA notice
    if (!document.getElementById('baaNotice')) {
      const notice = document.createElement('div');
      notice.id = 'baaNotice';
      notice.style = 'font-size:11px;color:#92400E;background:#FEF3C7;border:1px solid #FCD34D;border-radius:6px;padding:6px 10px;margin-top:6px;';
      notice.textContent = '⚠️ Translation vendor processes PHI audio. BAA required before enabling (TRANS-002). Contact Compliance.';
      btn.parentElement.parentElement.appendChild(notice);
    }
  } else {
    btn.textContent = '🌐 Translation Off';
    btn.style.background = '';
    btn.style.color = '';
    sel.style.display = 'none';
  }
}
function selectLanguage(sel) {
  if (sel.value) alert('Live translation enabled: ' + sel.options[sel.selectedIndex].text + '\nAI-powered captions will appear below the patient video feed.');
}
```

---

## AREA 2 — queue.html (2 requirements)

**File:** `templates/provider/queue.html`

### 2A. COLLAB-011 — Readiness Signals on Provider Queue
For each visit row in the queue table, add a readiness signal column. Find the existing table row structure and add a new `<td>` column titled **"Readiness"** with the following chip set:

```html
<td>
  <div style="display:flex;gap:3px;flex-wrap:wrap;">
    <span style="font-size:10px;background:#DCFCE7;color:#166534;padding:2px 7px;border-radius:10px;font-weight:600;">✅ Reg</span>
    <span style="font-size:10px;background:#DCFCE7;color:#166534;padding:2px 7px;border-radius:10px;font-weight:600;">✅ Intake</span>
    <span style="font-size:10px;background:#DCFCE7;color:#166534;padding:2px 7px;border-radius:10px;font-weight:600;">✅ Tech</span>
    <span style="font-size:10px;background:#FEF3C7;color:#92400E;padding:2px 7px;border-radius:10px;font-weight:600;">⏳ Joined</span>
  </div>
</td>
```

Vary the states across the existing queue rows so different patients show different readiness states (one showing failed tech check in red, one showing all green, one showing patient already joined).

### 2B. VID-005 — Re-send Visit Link Action
In each video visit row (identify rows where visit type is Video), add a quick action button:
```html
<button onclick="resendLink()" style="background:none;border:1px solid #6B21A8;color:#6B21A8;border-radius:6px;padding:3px 10px;font-size:11px;font-weight:600;cursor:pointer;">📱 Re-send Link</button>
```
```js
function resendLink() {
  alert('SMS visit link re-sent to patient (555) 867-5309.\nLink expires in 60 minutes.');
}
```

---

## AREA 3 — ma_queue.html (2 requirements)

**File:** `templates/provider/ma_queue.html`

### 3A. COLLAB-010 — MA Intake Queue Routing
At the top of the MA queue list (before the first patient row), add a highlighted routing banner:

```html
<div style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:8px;padding:10px 14px;margin-bottom:12px;font-size:12px;color:#1D4ED8;">
  <strong>📋 MA Intake Queue</strong> — 3 patients awaiting intake before provider assignment.
  New video/phone visits route here first. Complete intake to release to provider queue.
</div>
```

On each patient row, add an **"Intake Required"** badge next to the patient name:
```html
<span style="font-size:10px;background:#FEF3C7;color:#92400E;border:1px solid #FCD34D;border-radius:10px;padding:2px 7px;font-weight:600;margin-left:6px;">Intake Required</span>
```

### 3B. VID-004 — Tech Check Status on MA Queue
Add a "Tech Check" column to the MA queue table showing the same chip patterns as in queue.html Area 2A. Include at least one row showing "❌ Tech Check Failed" in red, with a "Re-send tech check link" micro-action button.

---

## AREA 4 — chart.html (1 requirement)

**File:** `templates/provider/chart.html`

### 4A. COLLAB-012 — Internal Care Team Messaging Thread
Find the chart tabs section (or the right sidebar if applicable). Add a new tab or section labeled **"Care Team"** (icon: 💬). 

Inside, render a simple internal messaging thread UI:

```html
<div style="display:flex;flex-direction:column;gap:0;border:1px solid #E5E0D8;border-radius:8px;overflow:hidden;">
  <!-- Header -->
  <div style="background:#F9FAFB;padding:10px 14px;border-bottom:1px solid #E5E0D8;font-size:12px;font-weight:700;color:#374151;">
    💬 Internal Care Team — CST-2026-10849 · Marcus Johnson
    <span style="font-size:10px;font-weight:400;color:#9CA3AF;margin-left:6px;">Visible to care team only — not in patient record</span>
  </div>
  <!-- Thread -->
  <div style="padding:12px;display:flex;flex-direction:column;gap:10px;max-height:260px;overflow-y:auto;">
    <div style="display:flex;gap:8px;">
      <div style="width:28px;height:28px;border-radius:50%;background:#00A67E;color:#fff;font-size:10px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;">SR</div>
      <div>
        <div style="font-size:11px;color:#6B7280;margin-bottom:2px;">Sarah R. (MA) · 9:14 AM</div>
        <div style="background:#F3F4F6;border-radius:8px;padding:8px 12px;font-size:13px;color:#374151;">Patient confirmed insurance. Intake form submitted. Ready for provider.</div>
      </div>
    </div>
    <div style="display:flex;gap:8px;flex-direction:row-reverse;">
      <div style="width:28px;height:28px;border-radius:50%;background:#6B21A8;color:#fff;font-size:10px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;">DR</div>
      <div style="text-align:right;">
        <div style="font-size:11px;color:#6B7280;margin-bottom:2px;">Dr. Chen · 9:18 AM</div>
        <div style="background:#EDE9FE;border-radius:8px;padding:8px 12px;font-size:13px;color:#374151;">Thanks. Please check if prior labs are attached — I need the testosterone panel from March.</div>
      </div>
    </div>
  </div>
  <!-- Compose -->
  <div style="border-top:1px solid #E5E0D8;padding:10px 14px;display:flex;gap:8px;">
    <input type="text" placeholder="Message care team..." style="flex:1;border:1px solid #E5E0D8;border-radius:6px;padding:7px 10px;font-size:13px;outline:none;">
    <button style="background:#6B21A8;color:#fff;border:none;border-radius:6px;padding:7px 14px;font-size:12px;font-weight:600;cursor:pointer;">Send</button>
  </div>
</div>
```

If adding as a new chart tab, add the tab trigger alongside existing tabs and show/hide the content with JS matching the existing tab pattern.

---

## AREA 5 — New: Coordinator Dashboard (3 requirements)

**New file:** `templates/admin/coordinator.html`

Create a full coordinator dashboard page extending `base.html` (or matching the admin layout from `templates/admin/dashboard.html`). This must be a full-page template, not a fragment.

**Route to add in `modules/admin.py`:**
```python
@bp.route("/coordinator")
def coordinator():
    return render_template("admin/coordinator.html")
```

**Content — 3 sections (stacked vertically with section headers):**

**Section 1 — COORD-001: Today View**
A table of all scheduled visits today across all providers:
- Columns: Time | Patient | Visit Type | Provider | Role | Status | Readiness
- Include 8–10 sample rows with varied statuses: Scheduled, In Progress, Completed, No-Show
- Color-code Status column: green=Completed, yellow=In Progress, blue=Scheduled, red=No-Show

**Section 2 — COORD-002: Escalations & SLA Monitor**
A panel with two sub-areas:
- **Active SLA Breaches** (red border card): 2 example rows — patient waiting >20 min, async response overdue by 4 hours
- **Escalation Queue**: 2 rows — "Provider license expiring in 7 days" (warning), "3 consults unassigned > 30 min" (critical)

**Section 3 — COORD-003: Read-Only Schedule View**
A simple day-view grid showing 3 provider columns (Dr. Chen, Dr. Martinez, NP Williams) with appointment blocks from 8 AM to 5 PM. Show 3–4 appointment blocks per provider using colored rectangles. Label: "Read-Only — Contact scheduler to make changes."

**Nav link:** In the admin sidebar/nav, add a "Coordinator" link pointing to `/admin/coordinator`.

---

## AREA 6 — gc_dashboard.html (4 requirements)

**File:** `templates/provider/gc_dashboard.html`

### 6A. GCW-003 — GC Pre-Test Consult Appointment Type
In the upcoming appointments or scheduling section of the GC dashboard, add a row (or card) showing a new appointment type:

```
🧬 Pre-Test Consult — 45 min — Video · Alex Rivera · Jun 18, 2:30 PM
[Start Session] [Send Prep Materials]
```

Add a small badge: `Pre-Test` in teal (`#0D9488` background, white text).

### 6B. GCW-004 — GC Scheduling Parity  
Add a "Schedule New" button in the GC dashboard header area matching the style used elsewhere. When clicked, show a simple scheduling panel (can be a collapsed div that toggles) with appointment type dropdown that includes: `Pre-Test Consult (45 min)` | `Post-Test Consult (30 min)` | `Follow-Up (20 min)`.

### 6C. M10-GCW-004 — GeneDx Assisted Ordering
In the active patient chart area (or as a new card below the patient list), add a GeneDx ordering section:

```html
<div class="card" style="margin-top:12px;">
  <div style="font-size:14px;font-weight:700;color:#111827;margin-bottom:8px;">🧬 GeneDx Lab Order</div>
  <div style="font-size:13px;color:#6B7280;margin-bottom:12px;">Assisted ordering workflow — order will be submitted to GeneDx on provider sign-off.</div>
  <div style="display:flex;gap:10px;flex-wrap:wrap;">
    <select style="border:1px solid #E5E0D8;border-radius:6px;padding:7px 10px;font-size:13px;flex:1;">
      <option>Select test panel...</option>
      <option>Comprehensive Carrier Screen (CCS)</option>
      <option>Expanded Carrier Screen (ECS)</option>
      <option>Preconception Genetic Screen</option>
      <option>Single-Gene BRCA1/2</option>
    </select>
    <button style="background:#6B21A8;color:#fff;border:none;border-radius:6px;padding:7px 18px;font-size:13px;font-weight:600;cursor:pointer;">Submit Order →</button>
  </div>
  <div style="margin-top:10px;font-size:11px;color:#9CA3AF;">Last order: Apr 12, 2026 — Comprehensive Carrier Screen — Resulted</div>
</div>
```

### 6D. M09-CAL-005 — Calendar Abstraction Indicator
In the GC dashboard settings or schedule header, add a small system indicator:
```
📅 Calendar Backend: Google Calendar (abstraction layer active — swap-ready)
```
Style as a subtle gray annotation (`font-size:11px; color:#9CA3AF`).

---

## AREA 7 — patient/enroll.html (1 requirement)

**File:** `templates/patient/enroll.html`

### 7A. IDV-001 — Vouched IAL2 Identity Verification Step
Find the enrollment step flow (look for a step indicator or form sections). Add a new step called **"Identity Verification"** (or insert it before the final confirmation step if steps already exist):

```html
<div style="background:#fff;border:1px solid #E5E0D8;border-radius:10px;padding:20px;margin-bottom:16px;">
  <div style="font-size:14px;font-weight:700;color:#111827;margin-bottom:4px;">🪪 Identity Verification — IAL2</div>
  <div style="font-size:13px;color:#6B7280;margin-bottom:14px;">Federal IAL2 verification is required before you can receive a prescription. This takes about 2 minutes.</div>
  <div style="display:flex;flex-direction:column;gap:8px;">
    <div style="display:flex;align-items:center;gap:10px;padding:10px;background:#F9FAFB;border-radius:8px;">
      <span style="font-size:20px;">📸</span>
      <div>
        <div style="font-size:13px;font-weight:600;color:#374151;">Step 1 — Government ID Scan</div>
        <div style="font-size:12px;color:#6B7280;">Take a photo of your driver's license or passport</div>
      </div>
      <span style="margin-left:auto;font-size:11px;background:#DCFCE7;color:#166534;padding:2px 8px;border-radius:10px;font-weight:600;">✅ Verified</span>
    </div>
    <div style="display:flex;align-items:center;gap:10px;padding:10px;background:#F9FAFB;border-radius:8px;">
      <span style="font-size:20px;">🤳</span>
      <div>
        <div style="font-size:13px;font-weight:600;color:#374151;">Step 2 — Selfie Liveness Check</div>
        <div style="font-size:12px;color:#6B7280;">Take a live selfie to match your ID photo</div>
      </div>
      <span style="margin-left:auto;font-size:11px;background:#DCFCE7;color:#166534;padding:2px 8px;border-radius:10px;font-weight:600;">✅ Verified</span>
    </div>
  </div>
  <div style="margin-top:12px;padding:10px;background:#ECFDF5;border:1px solid #6EE7B7;border-radius:8px;font-size:12px;color:#065F46;font-weight:600;">
    ✅ Identity verified via Vouched (IAL2) — Jun 16, 2026 10:42 AM
  </div>
  <div style="margin-top:6px;font-size:11px;color:#9CA3AF;">Powered by Vouched · IAL2 compliant · Results retained per HIPAA retention policy</div>
</div>
```

---

## AREA 8 — New: Pharmacy Fulfillment (3 requirements)

**New file:** `templates/provider/pharmacy.html`

Create a full pharmacy fulfillment page. Extend `base.html`. Match the provider portal layout (sidebar + topbar from other provider templates).

**Route to add in `modules/provider.py`:**
```python
@bp.route("/pharmacy")
def pharmacy():
    return render_template("provider/pharmacy.html")
```

**Content:**

**Page title:** "Pharmacy Fulfillment — Marcus Johnson · CST-2026-10849"

**Section 1 — PHARM-001: GoGoMeds Mail Pharmacy**
A card showing:
- Patient selection: Mail delivery (GoGoMeds)
- Prescription: Testosterone Cypionate 200mg/mL — 10mL Vial
- Status badge: `🟢 Transmitted to GoGoMeds` (green)
- Expected delivery: Jun 19–21, 2026
- Tracking: "Available after shipment"
- Button: "View Order Details"

**Section 2 — PHARM-002: Local Pharmacy via DoseSpot**
A card with a pharmacy search:
- Input: "Search nearby pharmacy..." with ZIP code field
- Results table showing 3 pharmacies (CVS, Walgreens, Rite Aid) with address, hours, accepts-controlled checkbox
- "Select" button per row
- Selected pharmacy highlighted in purple border

**Section 3 — PHARM-003: Event-Driven Fulfillment Log**
A timeline/audit section:
- Show 3 events in a vertical timeline:
  1. `consult-closed-with-prescription` — Jun 16 11:04 AM — Trigger event fired
  2. `rx-transmitted-to-pharmacy` — Jun 16 11:04 AM — GoGoMeds API call successful
  3. `fulfillment-confirmed` — Jun 16 11:47 AM — Pharmacist confirmed receipt
- Each event has a timestamp, event name in `font-family:monospace`, and status chip

**Nav link:** In the provider sidebar, add "Pharmacy" link pointing to `/provider/pharmacy`.

---

## AREA 9 — New: Billing Records (3 requirements)

**New file:** `templates/provider/billing.html`

Create a billing records page. Extend `base.html`. Match provider portal layout.

**Route to add in `modules/provider.py`:**
```python
@bp.route("/billing")
def billing():
    return render_template("provider/billing.html")
```

**Content:**

**Page title:** "Billing & Compensation — Jun 2026"

**Section 1 — COMP-001: Platform Billing Records**
A table with columns: Consult ID | Date | Patient | Visit Type | Billing Type | Amount | Status
- Include 5–6 sample rows mixing Cash-Pay and Partner billing types
- Status chips: `Paid` (green), `Pending` (yellow), `Sent to Athena` (blue), `Rejected` (red)
- Total row at the bottom

**Section 2 — COMP-002: Provider Compensation Split**
A card showing the compensation breakdown for a selected consult:
- Consult: CST-2026-10849
- Gross consult fee: $150.00
- Platform fee (20%): -$30.00
- Provider share (80%): $120.00
- Pay period: Jun 16–30, 2026
- Show as a simple stacked bar visual (use CSS width percentages)

**Section 3 — COMP-003: Athena Push Status**
A table showing recent Athena push events:
- Columns: Consult ID | Pushed At | Billing Code | Status | Response
- 3 rows: one Success, one Pending, one Failed (with retry button)
- Failed row: red background tint, "🔁 Retry Push" button

**Nav link:** In the provider sidebar, add "Billing" link pointing to `/provider/billing`.

---

## Final Step — Run QA Check

After completing all changes, run:

```bash
python3 /Users/justin.woller/Documents/project-phoenix-demo/qa_check.py
```

Paste the full output here. Fix any errors before marking this complete. All templates must pass validation.
