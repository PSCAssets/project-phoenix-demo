# Project Phoenix Demo — Patient Portal Isolation + Provider Eligibility v1
# June 18, 2026
# Run this entire prompt in Claude Code from: ~/Documents/project-phoenix-demo/

---

## CONTEXT

This script builds three demo experiences:
1. PWN Health isolated patient portal (separate branded login + portal)
2. Everlywell patient portal with program switcher (3 programs)
3. Admin Portal care product wizard updates (ecosystem classification, branding, provider eligibility)

Do not modify `project_phoenix.db`. After all changes, run the QA check at the bottom.

---

## CHANGE 1 — PWN Health Patient Portal (New Isolated Experience)

Create a new patient portal template and route for the PWN Health isolated ecosystem.

**New file:** `templates/patient/portal_pwn.html`

**New Flask route:** Add to `app.py` (or wherever patient routes are defined):
```python
@app.route('/pwn/portal')
def pwn_portal():
    return render_template('patient/portal_pwn.html')

@app.route('/pwn/login')
def pwn_login():
    return render_template('patient/login_pwn.html')
```

---

### PWN Login Page (`templates/patient/login_pwn.html`)

Full-page login. PWN branding throughout. No Everlywell references anywhere.

**Design:**
- Background: `#0A2F5C` (deep navy blue — PWN brand color)
- Centered card: white, border-radius 12px, max-width 420px, padding 40px
- Logo area: Show "PWN Health" as a styled text logo — `font-size: 28px`, `font-weight: 700`, `color: #0A2F5C`, with a small DNA helix icon (⬡ or use ◈) in teal `#00BFB3` to the left
- Tagline below logo: `"Your Health. Your Results."` — gray `#6B7280`, italic, 14px
- Form: Email input, Password input, "Sign In" button (full width, `#0A2F5C` bg, white text)
- Below button: `"Need help? Contact PWN Support"` — small gray link
- Footer: `"Powered by a HIPAA-compliant telehealth platform"` — tiny gray text, NO Everlywell mention

**Demo credentials shown on page (for demo purposes):**
```
Demo Patient: jennifer.adams@email.com
Password: demo1234
```

Show these in a light gray info box below the form: `"Demo Access: jennifer.adams@email.com / demo1234"`

On "Sign In" click (no actual auth needed — just navigate to PWN portal):
```javascript
document.getElementById('loginBtn').addEventListener('click', function() {
  window.location.href = '/pwn/portal';
});
```

---

### PWN Patient Portal (`templates/patient/portal_pwn.html`)

Full patient portal experience. PWN branding. One patient's data.

**Header:**
- Background: `#0A2F5C` (navy)
- Left: PWN Health logo (text + ◈ icon as above)
- Center: `"Patient Portal"`
- Right: Patient name `"Jennifer Adams"` + Logout link (white text)
- No Everlywell branding anywhere

**Patient banner (below header):**
```
Jennifer Adams  |  DOB: 03/14/1985  |  Member ID: PWN-847291
```
Light navy background `#EFF6FF`, border-bottom `1px solid #BFDBFE`.

**Main content — two-column layout:**

**Left sidebar (250px):** Navigation
- Dashboard (active)
- My Consultations
- Lab Results
- Messages
- Account Settings

Active state: `#0A2F5C` left border, navy text.

**Main area:** Show the patient's active consult card

```
┌─────────────────────────────────────────────────────────────────┐
│  MY CONSULTATIONS                                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  🧬  Genetic Counseling — Pre-Test                       │   │
│  │  Status: ● Consultation Scheduled                        │   │
│  │  Provider: Dr. Sarah Lee                                 │   │
│  │  Scheduled: June 24, 2026 at 2:00 PM EST               │   │
│  │  Consult ID: PWN-CST-2026-00481                         │   │
│  │                                                          │   │
│  │  CARE JOURNEY                                            │   │
│  │  ✓ Request Received → ✓ Intake Complete →               │   │
│  │  ● Consultation Scheduled → ○ Results Review            │   │
│  │                                                          │   │
│  │  [Join Video Consultation]  [View Details]              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  🧬  Genetic Counseling — Post-Test                      │   │
│  │  Status: ● Results Available                             │   │
│  │  Provider: Dr. Sarah Lee                                 │   │
│  │  Completed: May 10, 2026                                 │   │
│  │  Consult ID: PWN-CST-2026-00312                         │   │
│  │                                                          │   │
│  │  [View Results]  [Download Report]                      │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**Consult card styling:**
- White background, border `1px solid #E5E7EB`, border-radius 8px, padding 20px
- Status pill: scheduled = blue `#DBEAFE`/`#1D4ED8`, results = green `#D1FAE5`/`#065F46`
- "Join Video Consultation" button: `#0A2F5C` background, white text
- "View Results" button: `#0A2F5C` outline, navy text

**Care Journey tracker:** Horizontal dots connected by lines. Completed = navy filled circle with ✓. Active = teal `#00BFB3` filled circle. Upcoming = gray empty circle. Stage names below each dot in 11px gray.

**Footer:** `"© PWN Health. All rights reserved. | Privacy Policy | Terms of Use"` — No Everlywell mention.

---

## CHANGE 2 — Everlywell Patient Portal with Program Switcher

Update the existing Everlywell patient portal (or create if it doesn't exist at `templates/patient/portal.html`) to include a program switcher with 3 programs.

**New Flask route (if not exists):**
```python
@app.route('/patient/portal')
def patient_portal():
    return render_template('patient/portal.html')

@app.route('/patient/login')
def patient_login():
    return render_template('patient/login.html')
```

---

### Everlywell Patient Portal (`templates/patient/portal.html`)

**Header:**
- Background: white, border-bottom `1px solid #E5E7EB`, height 64px
- Left: Everlywell logo text — `"everlywell"` in `#1F2937`, font-weight 700, 22px
- Center: **Program Switcher** — a styled dropdown showing current program
- Right: `"Marcus Johnson"` + Logout

**Program Switcher (center of header):**

A styled select/dropdown showing the active program. When clicked, shows all 3 programs.

```
Current: [▼ Everlywell Direct — Men's Health]
```

Dropdown options:
1. `"Everlywell Direct — Men's Health"` (Testosterone Care) — default active
2. `"Everlywell Direct — Weight Management"` (GLP-1 / Weight Loss)
3. `"Humana A1C Program"` (powered by Everlywell)

**Styling of the switcher:**
- Pill-shaped button, border `1.5px solid #6B21A8`, text `#6B21A8`, background white, border-radius 20px, padding 8px 16px
- Dropdown: white card, border `1px solid #E5E7EB`, border-radius 8px, shadow, min-width 280px
- Each option: padding 12px 16px, hover `#F9FAFB`
- Active option: purple left border `3px solid #6B21A8`, bold text

**Program-switching behavior (JavaScript):**

When the user selects a program, update:
1. The switcher button label
2. The header's client sub-branding area (below main header)
3. The consult content shown in the main panel

```javascript
const programs = {
  'mens-health': {
    label: 'Everlywell Direct — Men\'s Health',
    subheader: 'Men\'s Testosterone Program',
    subheaderColor: '#6B21A8',
    consults: [...] // see below
  },
  'weight': {
    label: 'Everlywell Direct — Weight Management',
    subheader: 'GLP-1 Weight Management Program',
    subheaderColor: '#0891B2',
    consults: [...]
  },
  'humana': {
    label: 'Humana A1C Program',
    subheader: 'Powered by Everlywell | Humana Member Program',
    subheaderColor: '#047857',
    consults: [...]
  }
};
```

Add a **client sub-banner** below the main header (12px height, colored bar matching the program):
- Men's Health: `#EDE9FE` background, `"Men's Testosterone Program"` in `#6B21A8`
- Weight Management: `#CFFAFE` background, `"GLP-1 Weight Management Program"` in `#0891B2`
- Humana: `#D1FAE5` background, `"Humana A1C Program — Powered by Everlywell"` in `#047857` with a small Humana badge

---

### Program Content

**Men's Health (default):**
```
Testosterone Care Consultation
Status: ● In Progress
Provider: Dr. Sarah Lee
Consult ID: CST-2026-10849
Last Updated: Today

CARE JOURNEY
✓ Intake → ✓ MA Review → ● Provider Consultation → ○ Documentation → ○ Complete

[View Chart Details]  [Message Provider]
```

**Weight Management:**
```
GLP-1 / Weight Management Consultation
Status: ● Awaiting Provider Review
Provider: Assigned upon review
Consult ID: CST-2026-11203
Submitted: June 17, 2026

CARE JOURNEY
✓ Intake → ● MA Review → ○ Provider Review → ○ Prescription → ○ Complete

[View Status]  [Complete Intake]
```

**Humana A1C Program:**
```
Hemoglobin A1C Care Consultation
Status: ✓ Completed
Provider: Dr. Marcus Webb
Consult ID: HMN-2026-00847
Completed: June 1, 2026

CARE JOURNEY
✓ Intake → ✓ MA Review → ✓ Provider Review → ✓ Documentation → ✓ Complete

[View Results]  [Schedule Follow-up]
```

**Humana program** shows the Humana sub-banner prominently and adds a footer note: `"This program is provided through your Humana health plan benefit. Contact Humana Member Services for coverage questions."`

---

### Everlywell Login Page (`templates/patient/login.html`)

If the login page doesn't exist, create it:
- White background
- Centered card, max-width 420px
- Everlywell logo text, purple `#6B21A8`
- Tagline: `"Access your health consultations"`
- Email + Password inputs
- `"Sign In"` button (purple)
- Demo credentials box: `"Demo: marcus.johnson@email.com / demo1234"`
- On Sign In → `/patient/portal`

---

## CHANGE 3 — Admin Portal Wizard: Ecosystem + Branding + Provider Eligibility Steps

**File:** `templates/admin/wizard.html`

Add or update three steps in the care product wizard to reflect the new configuration model. Find the existing wizard steps and insert/update the following. Keep the step numbering consistent with whatever currently exists — add these as new steps in the logical sequence (after Basic Info, before or after existing branding-related steps).

---

### Step: Ecosystem Classification

Add a wizard step titled **"Ecosystem Classification"** with this content:

```
Portal Ecosystem

Configure how this care product's patient portal is managed.

○  Everlywell Platform
   Patient portal is under the Everlywell umbrella. Patients can
   access multiple programs via the program switcher. Everlywell
   or client co-branding applies.

○  Isolated Partner  ← selected for demo
   Patient portal is completely isolated. Partner branding only —
   no Everlywell references. Patient data is hard-isolated from
   the Everlywell ecosystem. Required for white-label contracts.

⚠️  This setting cannot be changed once the first patient account
    is created under this care product.
```

Styling:
- Radio cards: white bg, border `1px solid #E5E7EB`, border-radius 8px, padding 16px
- Selected card: border `2px solid #6B21A8`, bg `#FAFAF9`
- Warning box: yellow `#FEF3C7` bg, amber `#92400E` text, border-radius 6px, padding 12px

---

### Step: Portal Branding

Update or add a **"Portal Branding"** wizard step:

```
Client Branding Configuration

Logo
[  Upload Logo  ] PNG or SVG, max 2MB
[preview area — shows uploaded logo or placeholder]

Primary Color     [████] #0A2F5C  (for demo: PWN navy)
Secondary Color   [████] #00BFB3  (for demo: PWN teal)
Header Background [████] #0A2F5C

Live Preview:
┌─────────────────────────────────────────────────────┐
│  ◈ PWN Health          Patient Portal    J. Adams ↗ │
└─────────────────────────────────────────────────────┘
(updates as colors change)

For Isolated Partner ecosystems, logo and primary color are required
before this care product can be published.
```

Implement the color pickers as `<input type="color">` fields with a hex text input alongside. Update the Live Preview div in real-time using JavaScript as the user changes colors.

---

### Step: Provider Eligibility

Add a **"Provider Eligibility"** wizard step:

```
Provider Eligibility Configuration

Program Type
○ Commercial (default — all licensed providers eligible)
● Medicare Program
○ Medicaid Program

─────────────────────────────────────────────────────
MEDICARE PROGRAM — Provider Assignment

Assigned Providers                         [+ Add Provider]
┌────────────────────────────────────────────────────┐
│  Dr. Sarah Lee   NPI: 1234567890                   │
│  Licensed States: CA, TX, FL, NY, CO               │
│  Medicare Enrollment: ● Active (exp. 12/31/2027)  │
│                                               [×]  │
├────────────────────────────────────────────────────┤
│  Dr. Marcus Webb   NPI: 0987654321                 │
│  Licensed States: CA, TX, AZ, NV                   │
│  Medicare Enrollment: ● Active (exp. 06/30/2027)  │
│                                               [×]  │
└────────────────────────────────────────────────────┘

─────────────────────────────────────────────────────
EXCLUSION LIST (for specialized care products)

Providers excluded from this care product:    [+ Add Exclusion]
(empty for demo — placeholder text:
"No exclusions. All licensed providers are eligible by default.")
```

For **Commercial** type: show only the Exclusion List section (Medicare/Medicaid assignment hidden).
For **Medicare/Medicaid** type: show the explicit provider assignment table. Hide the exclusion list section (not applicable for Medicare/Medicaid).

Toggle between sections using JavaScript on program type radio change.

Provider enrollment status pill: Active = green `#D1FAE5`/`#065F46`, Expired = red `#FEE2E2`/`#991B1B`.

---

## CHANGE 4 — Add Navigation Links to Demo Home

**File:** `templates/index.html` or the main demo landing page (wherever the portal links are shown)

Add two patient portal demo links to the demo navigation:

```
PATIENT PORTAL DEMOS
[  PWN Health Portal (Isolated)  ]   →  /pwn/login
[  Everlywell Portal (Multi-Program)  ]   →  /patient/login
```

Button styles:
- PWN: `#0A2F5C` background, white text
- Everlywell: `#6B21A8` background, white text

If the demo home page already has a portal links section, add these to it. If not, add a new "Patient Portal" section in the demo navigation grid.

---

## FINAL STEP — QA Check

After completing all changes, run:

```bash
python3 /Users/justin.woller/Documents/project-phoenix-demo/qa_check.py
```

Paste the full output here before finishing.
