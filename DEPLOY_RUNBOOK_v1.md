# Project Phoenix Demo — Full Deploy Runbook
**Date:** June 19, 2026  
**Run these commands in Claude Code from your terminal.**

---

## Step 1 — Run All Apply Scripts (in order)

Open Claude Code and paste each command one at a time. Wait for "operations complete" before running the next.

```bash
cd ~/Documents/project-phoenix-demo
```

### 1a. Login screen — QA Reviewer + GC Admin users
```bash
python3 apply_login_new_users_v1.py
```

### 1b. Book Appointment modal (6-step scheduler)
```bash
python3 apply_book_appointment_modal_v1.py
```

### 1c. Admin Wizard — Pre-Consult Checklist + QA Stage steps
```bash
python3 apply_wizard_new_steps_v1.py
```

### 1d. Provider Chart — Clinical Resources + Linked Consults tabs
```bash
python3 apply_chart_new_tabs_v1.py
```

### 1e. Members DB admin screen
```bash
python3 apply_members_db_admin_v1.py
```

---

## Step 2 — Run QA Check

```bash
python3 /Users/justin.woller/Documents/project-phoenix-demo/qa_check.py
```

Paste the full output here before proceeding. Fix any failures before continuing.

---

## Step 3 — Commit + Push to GitHub

```bash
cd ~/Documents/project-phoenix-demo
git add -A
git commit -m "feat: complete demo build — wizard steps, chart tabs, members DB, scheduler modal, login users, deployment files"
git push origin main
```

---

## Step 4 — Trigger Render Deploy

After the push, Render should auto-detect and deploy. To verify or manually trigger:

1. Go to your Render dashboard: https://dashboard.render.com
2. Find the `project-phoenix-demo` service
3. If it doesn't start deploying automatically within 60 seconds, click **Manual Deploy → Deploy latest commit**

**Watch the build logs for these lines — they confirm success:**
```
==> Installing dependencies with pip install -r requirements.txt
==> Running start command: gunicorn app:app ...
[INFO] Starting gunicorn
[INFO] Listening at: http://0.0.0.0:XXXX
```

---

## Step 5 — Verify the Live URL

Once Render shows **Live**, open your service URL and confirm:

| Check | URL path | Expected |
|---|---|---|
| Login screen | `/` | Shows 11 user cards including Rachel Chen + Dana Cooper |
| QA Reviewer dashboard | `/login/qa_reviewer` | QA queue with Pending/Completed tables |
| GC Admin dashboard | `/login/gc_admin` | 3-tab GC Admin portal |
| Book Appointment modal | `/scheduler/search-patient` | 6-step modal opens on "Book Appointment" |
| Admin Wizard | `/admin/care-product/new` | Pre-Consult Checklist + QA Stage visible in left nav |
| Provider Chart | `/provider/chart` | 5 tabs in right panel: Documentation, Communication, Zendesk, 📚 Clinical Resources, 🔗 Linked Consults |
| Members DB | `/admin/members-db` | Health plan eligibility screen with stats + import |

---

## Troubleshooting

**Render build fails with "No module named gunicorn"**  
→ Confirm `gunicorn==23.0.0` is in requirements.txt (it was added in this runbook) and re-push.

**App crashes on startup ("no such table")**  
→ The SQLite DB file must be committed to the repo. Run:
```bash
git add project_phoenix.db
git commit -m "chore: include demo database"
git push origin main
```

**Pages return 404 for new routes**  
→ The apply scripts modify files in `/templates/` — confirm the scripts all completed (check "operations complete" output). Then re-push.

**Render not auto-deploying after push**  
→ Confirm "Auto-Deploy" is ON in Render service settings (Settings → Auto-Deploy → Yes).

---

## What Was Added in This Build

| Script | Files Changed | Requirements |
|---|---|---|
| apply_login_new_users_v1.py | index.html, app.py, provider.py, +2 dashboards | QA Reviewer + GC Admin login + dashboards |
| apply_book_appointment_modal_v1.py | scheduler/search_patient.html | 6-step Book Appointment modal, Member Lookup tab |
| apply_wizard_new_steps_v1.py | admin/wizard.html | M04-CHK-001, M04-QA-001, M04-NIH-001 |
| apply_chart_new_tabs_v1.py | provider/chart.html | M02-CLB-001, M02-LNK-001 |
| apply_members_db_admin_v1.py | admin/members_db.html, admin.py | M10-ELG-001 |
| requirements.txt | — | Added gunicorn==23.0.0 |
| Procfile | — | Render/Heroku start command |
| render.yaml | — | Render service config |
