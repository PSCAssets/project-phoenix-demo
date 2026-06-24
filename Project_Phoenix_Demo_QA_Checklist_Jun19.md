# Project Phoenix Demo — QA Checklist
**Session:** June 19, 2026  
**Reviewer:** Justin Woller  
**Environment:** localhost:5000  
**Scope:** All changes from today's v5 + v6 fix session

---

## ⚠️ BEFORE YOU START — Server Restart Required

`app.py` was modified (scheduler name changed). You must:

1. Stop the Flask server (Ctrl+C)
2. Restart: `python app.py`
3. Clear your browser session or open an incognito window
4. Log in fresh — old sessions still carry "Morgan Hayes"

---

## 1. Scheduler Dashboard

**Login:** Select → Scheduler (David Nguyen)

- [ ] Top bar shows **"David Nguyen"** (not Morgan Hayes)
- [ ] Avatar initials show **"DN"**
- [ ] Greeting says **"Good morning, David"**
- [ ] Three stat cards visible: Today's Appointments · Pending Reschedules · Unassigned Slots
- [ ] Three action cards: Search Patient · New Patient · Open Scheduler

---

## 2. Scheduler — Patient Search

**Path:** Scheduler Dashboard → Search Patient (or `/scheduler/search-patient`)

- [ ] Patient rows appear in results after searching
- [ ] Each patient row has a **"Schedule Consult"** button (not "Reschedule")
- [ ] Clicking **"Schedule Consult"** opens the 6-step booking modal
- [ ] Modal populates with the selected patient's name and info
- [ ] Booking modal steps work: Demographics → Care Product → Contact & Insurance → Billing → Health Profile → Request Consult

---

## 3. New Patient Wizard

**Path:** Scheduler Dashboard → New Patient (or `/provider/new-patient`)

- [ ] Page loads directly into the **wizard** — no "Who are you adding?" selection screen
- [ ] First step shown is **Demographics** (step 1 of 6)
- [ ] Step navigation shows: **Demographics → Care Product → Contact & Insurance → Billing → Health Profile → Request Consult**
- [ ] **Care Product step** includes: Annual Wellness Visit and Weight Loss Program in the dropdown
- [ ] **Contact & Insurance step** does NOT have a Billing Address section
- [ ] **Billing step** is present and separate (after Contact & Insurance)

### Request Consult step (step 6):
- [ ] Two radio cards shown: **📅 Schedule Appointment** and **⚡ Submit into Queue — Real Time**
- [ ] Clicking "Schedule Appointment" expands date/time/duration/provider fields below
- [ ] Clicking "Submit into Queue — Real Time" expands the real-time queue section with:
  - Green badge showing estimated wait time: **"4–8 MIN EST. WAIT"**
  - Text: "2 providers currently active"
  - Consult type selector
  - Routing note

### Lab Results Alert:
- [ ] Go back to Care Product step — select **Weight Loss Program**
- [ ] Navigate forward to Request Consult step
- [ ] ⚠️ **Yellow/amber alert banner appears** at top: "Lab Results Required Before Consultation"
- [ ] Select a different care product (e.g., Annual Wellness Visit) → alert disappears

---

## 4. Provider Portal Nav Link

**Path:** Any page with the top nav bar

- [ ] Click **"Provider Portal"** in the top navigation
- [ ] Should land on **localhost:5000** (role selection index page), NOT the MD dashboard

---

## 5. GC Dashboard

**Login:** Select → Taylor Brooks, GC

- [ ] Left sidebar shows: Dashboard · Queue · Schedule · Messages · Alerts · Settings · Oversight
- [ ] **No "Lab Orders"** item in the sidebar nav

---

## 6. GC Schedule

**Path:** GC Dashboard → Schedule (or `/provider/schedule` while logged in as GC)

- [ ] Calendar/schedule view loads without JavaScript errors (check browser console)
- [ ] Appointment blocks show **genetics-specific names**: BRCA Genetic Counseling · Hereditary Cancer Review · Blueprint Genetics · etc. (not generic "Annual Visit" etc.)
- [ ] Click an appointment block → modal opens
- [ ] Modal **title** shows the genetics appointment name (e.g., "BRCA Genetic Counseling"), not the base name

### Appointment Detail Modal:
- [ ] Footer buttons all appear on **one row** without wrapping: Close · ✎ Edit · Open Chart → · ⚡ Conduct Consult Now
- [ ] Click **"Conduct Consult Now"** → Real-Time Queue modal opens **in front of** (on top of) the appointment detail modal
- [ ] Close the RTQ modal → appointment modal is still visible underneath

---

## 7. GC Queue

**Path:** GC Dashboard → Queue

- [ ] Nav bar matches GC Dashboard nav (same items, same style)
- [ ] Queue table columns: Program · DOB · Gender (no "Readiness" column)
- [ ] Program names show genetics-specific names: Blueprint Genetics · GeneDx · CareFirst

---

## 8. Provider Chart (MD/NP view)

**Login:** Select → Dr. Sarah Lee, MD or Jamie Rivera, NP

**Path:** Provider Dashboard → open any patient chart

- [ ] Left sidebar nav has **one expand arrow** (▷) at the top — not two identical buttons
- [ ] Clicking the arrow toggles the panel expand/collapse

---

## 9. DB Update (for your records)

- [ ] Requirement **M09-RT-002** added to the DB: "System must display estimated wait time when submitting patient to real-time queue, based on active providers, queue depth, and average handle time. Must show a range. Zero-provider state blocks submission."
- Priority: High · Status: Draft · Source: Jun 19 demo review

---

## 10. Known Items NOT Yet Built

These are in requirements but not yet demoed — no need to check now:

- RN/MA/CT action board / role-specific work queue widget (M02-QUEUE-001/002)
- GC SLA notifications with genetics-specific names
- Nav consistency: Oversight item in GC Queue sidebar

---

## Notes

- **Do NOT push to GitHub** until you've completed this checklist and approved locally
- All changes are uncommitted — let me know when you're ready to commit
