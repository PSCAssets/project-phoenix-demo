# Project Phoenix Demo — QA Checklist v2
**Session:** June 19, 2026  
**Reviewer:** Justin Woller  
**Environment:** localhost:5000  
**Scope:** Changes made AFTER the first checklist (v1) — second round of this session

---

## 1. New Patient Wizard — Care Product Dropdown

**Path:** New Patient → Step 2 Care Product

- [ ] Dropdown shows **only two options**: Annual Wellness Visit · Weight Loss Program
- [ ] All other products (Testosterone, Skincare, ED Treatment, Women's Health, Hair Loss, Mental Health, A1C Management) are removed
- [ ] Selecting **Weight Loss Program** shows product card: "Lab results required before first consult"

---

## 2. New Patient Wizard — Demographics Step

**Path:** New Patient → Step 1 Demographics

- [ ] Step shows: First/Last Name, DOB, Sex, State of Residence, Phone, Email, Address (optional)
- [ ] **No "Insurance / Payment"** section on this step — it has been removed

---

## 3. New Patient Wizard — Contact & Insurance Step

**Path:** New Patient → Step 3 Contact & Insurance

- [ ] Section is headed "Insurance Coverage" with no Self-Pay / Subscription radio buttons
- [ ] Shows: Insurance Carrier, Member ID, Group Number, Plan Type fields
- [ ] At bottom: "Does the patient have active insurance?" Yes / No radio toggle

---

## 4. New Patient Wizard — Billing Step

**Path:** New Patient → Step 4 Billing

- [ ] Three payment method options: 🏥 Insurance · 💳 Self-Pay · 🔄 Subscription
- [ ] Selecting **Insurance** → shows green note: "Standard co-pay applies per plan terms"
- [ ] Selecting **Self-Pay** → expands card fields (Cardholder Name, Card Number, Exp, CVV)
- [ ] Selecting **Subscription** → shows blue note: "$0 cost-share"
- [ ] Billing Address section (Street, City, State, ZIP) is present on this step

---

## 5. New Patient Wizard — Request Consult (Lab Results Alert)

**Path:** New Patient → Step 2 Care Product → select Weight Loss Program → proceed to Step 6 Request Consult

- [ ] Yellow alert banner appears: "Lab Results Required Before Consultation"
- [ ] Alert shows **"📎 Upload Lab Results"** button (no "Skip — Labs Already Ordered")
- [ ] Clicking "Upload Lab Results" opens a file picker (PDF, JPG, PNG)
- [ ] After selecting a file → green badge appears: **"✓ Lab results attached"**
- [ ] "Order Labs Now" button still present

---

## 6. Patient Search — Auto-Populate

**Path:** Scheduler → Search Patient

- [ ] **Patient Records table is pre-populated on page load** — 10 patients visible without searching
- [ ] Search box filters the list as you type
- [ ] **Search button** also filters when clicked
- [ ] Member Lookup tab: 8 members pre-loaded on load

---

## 7. Scheduling Tool — Confirm Booking

**Path:** Scheduler → Open Scheduler → find a slot → click to book → Confirm Appointment modal → Confirm Booking

- [ ] Clicking "Confirm Booking" shows a **full-screen white overlay**: ✅ "Appointment Booked" + "Confirmation has been sent to the patient."
- [ ] Page **auto-redirects to Scheduler Dashboard** after ~2 seconds
- [ ] No lingering modal or partial state

---

## 8. PWN Health Patient Portal — Nav Buttons

**Path:** Select role → Patient (PWN portal) → `/pwn/portal`

- [ ] All 5 sidebar nav items are now **clickable and switch content**:

  - [ ] **Dashboard** → shows the two Genetic Counseling consult cards with Care Journey
  - [ ] **My Consultations** → shows both consults with full detail (consult type, care program, all journey steps) + Reschedule button
  - [ ] **Lab Results** → shows BRCA1/2 panel (Results Available) + Lynch Syndrome panel (Pending) + message/schedule shortcuts
  - [ ] **Messages** → 3 message threads that expand/collapse on click; each has reply textarea + Send button; Compose button at top
  - [ ] **Account Settings** → Personal Info, Contact Info, Notification Preferences (with working toggle switches)

- [ ] Lab Results → "View Results" button routes to Lab Results section
- [ ] Lab Results → "Send a Message" button routes to Messages section

---

## 9. PWN Health Portal — Logo Navigation

**Path:** Any page within `/pwn/portal`

- [ ] Clicking the **"◈ PWN Health"** logo in the top-left header navigates back to **localhost:5000** (role selection screen)
- [ ] Logo has a subtle hover opacity effect

---

## 10. Everlywell Patient Portal — Logo Navigation

**Path:** Select role → Patient → `/patient/portal`

- [ ] Clicking **"everlywell"** logo in the top-left header navigates back to **localhost:5000** (role selection screen)
- [ ] Logo has a subtle hover opacity effect

---

## Notes

- No server restart required for this round (no app.py changes)
- All changes are still uncommitted — let me know when ready to commit
