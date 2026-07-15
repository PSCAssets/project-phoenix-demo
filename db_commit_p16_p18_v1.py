"""
db_commit_p16_p18_v1.py
Inserts 18 requirements from Prompts 16–18 (Discovery Phase Jun 2026)
into project_phoenix.db. Skips any req_id that already exists.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "project_phoenix.db")
SOURCE  = "Prompt 16–18 / Discovery Phase Jun 2026"
DATE    = "2026-06-15"

REQUIREMENTS = [
    # ── M02 ──────────────────────────────────────────────────────────────
    {
        "req_id":   "M02-RBAC-001",
        "module_id": "M02 - Provider Portal",
        "section":  "Role-Based Access Control",
        "portal":   "Provider",
        "user_story": "As a platform admin, I need each provider role (MD, NP, RN, MA, GC) "
                      "to see only the UI surfaces and actions appropriate to their license, "
                      "so that scope-of-practice boundaries are enforced at the UI layer.",
        "requirement": "The provider portal must gate all sidebar navigation items, action "
                       "buttons, and data panels by session role. Roles: provider_md, "
                       "provider_np, provider_rn, provider_ma, provider_gc. Each role maps "
                       "to a distinct dashboard template with its own sidebar and permitted routes.",
        "rule":     "Session role is set at login and must be re-validated on every protected "
                    "route. No role-escalation is permitted client-side.",
        "acceptance": "1. Logging in as each of the 5 provider roles renders the correct "
                      "dashboard template. 2. Direct URL access to a role-restricted route "
                      "redirects to role selection. 3. Sidebar items not available to a role "
                      "are absent from the DOM (not merely hidden via CSS).",
        "edge_cases": "Expired session must redirect to login, not leak the last role's view.",
        "priority": "Critical",
        "status":   "Defined",
        "jira_epic": "PHXP-M02",
        "owner":    "Platform Engineering",
    },
    {
        "req_id":   "M02-NAV-001",
        "module_id": "M02 - Provider Portal",
        "section":  "Navigation / Sidebar",
        "portal":   "Provider",
        "user_story": "As any provider, I need clear visual feedback on which sidebar item "
                      "is currently active and easy tooltip identification of collapsed icons, "
                      "so I can navigate efficiently in both expanded and collapsed sidebar states.",
        "requirement": "Every provider sidebar must: (a) apply a 3 px solid #6B21A8 right-border "
                       "to the active nav item; (b) expose a `title` attribute on every icon "
                       "link; (c) collapse to 48 px and expand to 200 px without layout shift; "
                       "(d) render a house SVG (not a grid) for the Dashboard home item.",
        "rule":     "Active state is determined by the current route, set inline per template. "
                    "The Everlywell logo in all portals (including the admin wizard) must link "
                    "to / (role selection).",
        "acceptance": "1. Active sidebar item has visible purple right-border. 2. Hovering a "
                      "collapsed icon shows tooltip via title attr. 3. Dashboard icon is a house "
                      "silhouette. 4. Logo click from any page routes to /.",
        "edge_cases": "Sidebar expanded state must survive page navigation (persisted via "
                      "body class toggle, not localStorage in v1).",
        "priority": "High",
        "status":   "Defined",
        "jira_epic": "PHXP-M02",
        "owner":    "Frontend Engineering",
    },
    {
        "req_id":   "M02-COM-001",
        "module_id": "M02 - Provider Portal",
        "section":  "Chart View / Breadcrumb",
        "portal":   "Provider",
        "user_story": "As a provider viewing a patient chart, I need a breadcrumb back-link "
                      "that navigates to my role-appropriate dashboard, not a hardcoded queue URL.",
        "requirement": "The chart breadcrumb back-link must read '← Back to Dashboard' and "
                       "href='/provider/' for all roles accessing the chart view.",
        "rule":     "The breadcrumb must not reference 'Queue' as the back destination; "
                    "all roles return to their dashboard via /provider/.",
        "acceptance": "1. Clicking '← Back to Dashboard' from chart returns to the provider "
                      "dashboard. 2. Link text does not contain 'Queue'.",
        "edge_cases": "Browser back button is out of scope; only the in-app link is tested.",
        "priority": "Medium",
        "status":   "Defined",
        "jira_epic": "PHXP-M02",
        "owner":    "Frontend Engineering",
    },
    {
        "req_id":   "M02-COM-002",
        "module_id": "M02 - Provider Portal",
        "section":  "Chart View / Read-Only Access",
        "portal":   "Provider",
        "user_story": "As a provider accessing a chart that is not assigned to me, I need a "
                      "clear visual warning that I am in read-only mode so I don't accidentally "
                      "believe my changes will be saved.",
        "requirement": "When a chart is accessed with ?view_only=1 (unassigned chart access "
                       "from the queue), a yellow banner must appear below the concurrent-viewer "
                       "banner reading: 'Viewing only — This consult is not assigned to you. "
                       "Chart is read-only. Changes will not be saved.'",
        "rule":     "The view_only flag is set server-side by the /provider/chart route when "
                    "?view_only=1 is present in the query string. The banner is rendered "
                    "conditionally via Jinja2 {% if view_only %}.",
        "acceptance": "1. Navigating to /provider/chart?view_only=1 shows the yellow banner. "
                      "2. Navigating without the param shows no banner. 3. Banner uses amber "
                      "color scheme (#FFFBEB bg, #FDE68A border, #92400E text).",
        "edge_cases": "Concurrent-viewer banner and view-only banner can both be visible "
                      "simultaneously; they must not overlap.",
        "priority": "High",
        "status":   "Defined",
        "jira_epic": "PHXP-M02",
        "owner":    "Frontend Engineering",
    },
    {
        "req_id":   "M02-COM-003",
        "module_id": "M02 - Provider Portal",
        "section":  "Chart View / Workflow Strip",
        "portal":   "Provider",
        "user_story": "As a provider opening a patient chart, I need to see the current "
                      "workflow stage at a glance so I know what work is required before "
                      "I dive into clinical content.",
        "requirement": "A workflow progress strip must appear between the demographics header "
                       "and the consult-type banner. It shows stage circles (✓ done, numbered "
                       "active/pending), connecting lines, current stage name, assigned role, "
                       "and SLA chip when applicable. Data is sourced from DEMO_CONSULT_WORKFLOW "
                       "and WORKFLOW_TEMPLATES via the provider.py chart route.",
        "rule":     "Completed stages use #1A1D23 fill; active stage uses #1D4ED8 with glow "
                    "ring; pending stages are outlined only. Strip height is fixed at 52 px.",
        "acceptance": "1. Chart renders workflow strip with correct stage count for the "
                      "template. 2. Completed stages show ✓. 3. Active stage is blue with "
                      "ring. 4. SLA chip shows '6h remaining' for the demo consult.",
        "edge_cases": "If workflow_stages is empty (unknown template), strip renders nothing "
                      "rather than throwing a Jinja2 error.",
        "priority": "High",
        "status":   "Defined",
        "jira_epic": "PHXP-M02",
        "owner":    "Frontend Engineering",
    },
    {
        "req_id":   "M02-COM-004",
        "module_id": "M02 - Provider Portal",
        "section":  "Session Persistence / Display Name",
        "portal":   "Provider",
        "user_story": "As any authenticated user, I need my display name shown consistently "
                      "in the top navigation bar regardless of which role I'm logged in as, "
                      "so the UI always reflects who I actually am.",
        "requirement": "The base.html nav-user-name element must render "
                       "{{ session.get('display_name', 'Demo User') }} rather than a "
                       "hardcoded if/elif chain keyed on role. Provider dashboard left panels "
                       "(sidebar avatar, sidebar name label, topbar avatar, greeting) must "
                       "all derive from session.get('display_name').",
        "rule":     "Hardcoded role-to-name mappings in base.html are prohibited after this "
                    "change. Each dashboard template computes initials from display_name "
                    "using Jinja2 string splitting.",
        "acceptance": "1. Switching roles shows the correct display_name in the nav bar "
                      "without a hardcoded fallback name appearing. 2. NP dashboard sidebar "
                      "avatar, sidebar name, topbar avatar, and greeting are all session-driven. "
                      "3. Fallback values are role-appropriate strings, not another provider's name.",
        "edge_cases": "If display_name contains a credential suffix (e.g. ', NP'), initials "
                      "must be derived from the name portion only (split on comma first).",
        "priority": "High",
        "status":   "Defined",
        "jira_epic": "PHXP-M02",
        "owner":    "Frontend Engineering",
    },
    {
        "req_id":   "M02-COM-005",
        "module_id": "M02 - Provider Portal",
        "section":  "Workflow Configuration / Admin Wizard Step 9",
        "portal":   "Admin",
        "user_story": "As a platform admin creating a new care product, I need to configure "
                      "the clinical workflow pipeline (stages, SLAs, roles) in the setup wizard "
                      "so that the correct multi-step handoff sequence is enforced for that product.",
        "requirement": "Wizard Step 9 must provide: (a) workflow mode selector (Simple / "
                       "Standard / Custom); (b) template picker with 4 pre-built templates; "
                       "(c) visual pipeline of stage chips with role color coding; (d) stage "
                       "settings side-panel with SLA, required fields, and notes; (e) simulation "
                       "mode that steps through stages with a progress bar; (f) scalability "
                       "callout. Stage data sourced from workflow_config.py STAGE_CATALOG.",
        "rule":     "workflow_config.py must not be modified by wizard UI changes. The wizard "
                    "embeds JS copies of STAGE_CATALOG and WORKFLOW_TEMPLATES for client-side "
                    "rendering within the existing {% raw %} script block.",
        "acceptance": "1. Template picker updates pipeline on change. 2. Clicking a stage "
                      "opens settings panel. 3. Simulation advances through all stages. "
                      "4. Scalability callout is visible below the pipeline.",
        "edge_cases": "Custom mode with zero stages must not break pipeline render.",
        "priority": "High",
        "status":   "Defined",
        "jira_epic": "PHXP-M02",
        "owner":    "Product / Platform Engineering",
    },
    {
        "req_id":   "M02-COM-006",
        "module_id": "M02 - Provider Portal",
        "section":  "NP Dashboard / Nav Parity",
        "portal":   "Provider",
        "user_story": "As a Nurse Practitioner, I need my dashboard sidebar to contain the "
                      "same navigation items as the MD dashboard so I can access all provider "
                      "functions available to my role.",
        "requirement": "The NP dashboard sidebar must include: Dashboard (active), Patient "
                       "Queue → /provider/queue, My Schedule → /provider/schedule, Messages, "
                       "Notifications/Alerts, Settings, and Provider Oversight → /provider/oversight. "
                       "This matches the MD provider_md sidebar nav set.",
        "rule":     "NP role (provider_np) is treated as a clinical role with the same nav "
                    "surface as MD in Phase 1. Role-specific data differences are handled "
                    "in the dashboard body, not the sidebar.",
        "acceptance": "1. NP sidebar renders all 7 nav items. 2. Provider Oversight link "
                      "navigates to /provider/oversight. 3. Active item has purple right-border.",
        "edge_cases": "If session role is provider_np but display_name is missing, the "
                      "fallback 'Maria Rodriguez, NP' must not appear as another role's name.",
        "priority": "Medium",
        "status":   "Defined",
        "jira_epic": "PHXP-M02",
        "owner":    "Frontend Engineering",
    },
    # ── M02-MA ───────────────────────────────────────────────────────────
    {
        "req_id":   "M02-MA-001",
        "module_id": "M02 - Provider Portal",
        "section":  "MA Dashboard / Workflow Stages",
        "portal":   "Provider",
        "user_story": "As a Medical Assistant, I need to see the current workflow stage for "
                      "each consult in my work queue so I can prioritize intake tasks appropriately.",
        "requirement": "The MA dashboard active consult table must include a 'Stage' column "
                       "displaying a color-coded badge per consult. Amber (#FEF3C7/#92400E) "
                       "for intake/prep stages; blue (#DBEAFE/#1D4ED8) for clinical stages.",
        "rule":     "Stage badge data is static demo data in v1. Column is inserted between "
                    "Care Product and Urgency columns.",
        "acceptance": "1. MA dashboard table renders Stage column. 2. At least one amber "
                      "and one blue badge are present. 3. Column header reads 'Stage'.",
        "edge_cases": "If consult has no stage assigned, cell renders empty rather than "
                      "showing an error badge.",
        "priority": "Medium",
        "status":   "Defined",
        "jira_epic": "PHXP-M02",
        "owner":    "Frontend Engineering",
    },
    # ── M02-QUEUE ────────────────────────────────────────────────────────
    {
        "req_id":   "M02-QUEUE-001",
        "module_id": "M02 - Provider Portal",
        "section":  "Queue / Column Structure",
        "portal":   "Provider",
        "user_story": "As a provider or MA reviewing the master queue, I need a clean, "
                      "focused column layout that shows the most clinically relevant information "
                      "without extraneous status or assignment columns cluttering the view.",
        "requirement": "Queue table column order (v2): icon | Patient | Age | Consult ID | "
                       "Type | Care Product | State | Wait Time | SLA Status | Actions. "
                       "Removed columns: Assigned To, Workflow Stage, Status. SLA Status "
                       "cell is blank (no badge) when SLA is healthy (on-track). Age column "
                       "is the 3rd column (after Patient).",
        "rule":     "The data-assigned, data-sla, data-type, data-product, data-status "
                    "attributes on <tr> elements are retained for JS filter logic even though "
                    "the Assigned To column is removed from the visible table.",
        "acceptance": "1. Queue renders exactly 10 columns (including icon and actions). "
                      "2. 'Assigned To', 'Workflow Stage', and 'Status' headers are absent. "
                      "3. Age column shows patient age (e.g. '34y'). "
                      "4. SLA Status cell is empty for the 4 on-track rows.",
        "edge_cases": "Column removal must not break the existing JS filter, chip, or "
                      "row-click navigation functions.",
        "priority": "High",
        "status":   "Defined",
        "jira_epic": "PHXP-M02",
        "owner":    "Frontend Engineering",
    },
    {
        "req_id":   "M02-QUEUE-002",
        "module_id": "M02 - Provider Portal",
        "section":  "Queue / Route Action",
        "portal":   "Provider",
        "user_story": "As a queue manager or supervising provider, I need to route an "
                      "unassigned consult to a specific provider or pool without leaving "
                      "the queue view, so I can manage assignments efficiently inline.",
        "requirement": "Each queue row must include a 'Route' button in the Actions cell. "
                       "Clicking Route inserts an inline form row immediately below the "
                       "consult row containing: (a) a provider/pool dropdown; (b) a free-text "
                       "routing note field; (c) Confirm and Cancel buttons. Only one route "
                       "form may be open at a time. Confirm requires a selection. Cancel "
                       "removes the form. No page navigation occurs.",
        "rule":     "Route form rows are generated dynamically via JS (not static HTML). "
                    "Form rows must not appear in the allRows NodeList used by applyFilters(). "
                    "Route form <tr> must carry class='route-form-row' and colspan=10.",
        "acceptance": "1. Route button appears on all 14 rows. 2. Clicking Route shows "
                      "inline form below that row. 3. Clicking Route again (or another "
                      "route btn) dismisses the previous form. 4. Confirm without selection "
                      "shows alert. 5. Confirm with selection dismisses form. 6. Cancel "
                      "dismisses form.",
        "edge_cases": "Route form row must not trigger row-click chart navigation.",
        "priority": "High",
        "status":   "Defined",
        "jira_epic": "PHXP-M02",
        "owner":    "Frontend Engineering",
    },
    {
        "req_id":   "M02-QUEUE-003",
        "module_id": "M02 - Provider Portal",
        "section":  "Queue / Patient Name Links",
        "portal":   "Provider",
        "user_story": "As a provider, I need to click a patient's name in the queue to open "
                      "their chart directly, and I need visual indication if the chart is "
                      "read-only because the consult isn't assigned to me.",
        "requirement": "All patient name cells in the queue must be <a> links styled as "
                       "`.patient-link` (inherits row color, underlines on hover, purple on "
                       "hover). Assigned consults link to /provider/chart?type=X. Unassigned "
                       "consults link to /provider/chart?type=X&view_only=1. The row-click "
                       "JS handler must also propagate view_only for unassigned rows and "
                       "must skip navigation when clicking an <a> tag directly.",
        "rule":     "Unassigned = data-assigned='unassigned'. Type param is derived from "
                    "data-type on the row (phone→phone, video→video, all others→async). "
                    "The existing row-click handler is updated to check for link clicks "
                    "and to append &view_only=1 for unassigned rows.",
        "acceptance": "1. All 14 patient name cells are <a> links. 2. Unassigned names "
                      "include view_only=1 in href. 3. Clicking assigned name does not "
                      "add view_only param. 4. Row-click (non-link, non-button area) "
                      "also respects view_only for unassigned rows.",
        "edge_cases": "Clicking the patient name link must not fire the row-click handler "
                      "a second time (link propagates its own navigation).",
        "priority": "High",
        "status":   "Defined",
        "jira_epic": "PHXP-M02",
        "owner":    "Frontend Engineering",
    },
    # ── M04 ──────────────────────────────────────────────────────────────
    {
        "req_id":   "M04-PERM-001",
        "module_id": "M04 - Admin Portal",
        "section":  "Admin / Care Product Wizard Permissions",
        "portal":   "Admin",
        "user_story": "As a platform admin, I need the Care Product Setup Wizard to restrict "
                      "creation actions to admin-role sessions so that provider-role users "
                      "cannot accidentally create or modify care product configurations.",
        "requirement": "The Care Product Wizard (/admin/care-product/new) is accessible only "
                       "to sessions with role='admin'. The wizard's admin sidenav logo must "
                       "link to / (role selection) so admins can switch context.",
        "rule":     "Route-level access control is enforced in admin.py blueprint. "
                    "The nav-logo in wizard.html must be wrapped in <a href='/'> not a <div>.",
        "acceptance": "1. Non-admin sessions attempting /admin/care-product/new are "
                      "redirected. 2. Admin logo click navigates to /. 3. Wizard step "
                      "navigation retains admin session.",
        "edge_cases": "Mid-wizard session expiry must redirect to login, not silently "
                      "submit partial config.",
        "priority": "High",
        "status":   "Defined",
        "jira_epic": "PHXP-M04",
        "owner":    "Platform Engineering",
    },
    {
        "req_id":   "M04-NAV-001",
        "module_id": "M04 - Admin Portal",
        "section":  "Admin / Wizard Navigation",
        "portal":   "Admin",
        "user_story": "As a platform admin working through the care product wizard, I need "
                      "the wizard step nav and breadcrumb to always be accessible and correctly "
                      "indicate my current position in the 10-step setup flow.",
        "requirement": "The Care Product Wizard must render: (a) a fixed left step-nav panel "
                       "with active/done/pending states; (b) a sticky breadcrumb bar with "
                       "Admin › Care Products › New Care Product; (c) previous/next navigation "
                       "buttons with progress bar; (d) step 9 (Workflow Configuration) fully "
                       "interactive with template picker, pipeline, stage panel, and simulation.",
        "rule":     "Step navigation JS (goToStep) must show/hide step panels without "
                    "page reload. Step 9 JS functions must live inside the existing "
                    "{% raw %} script block to avoid Jinja2 template conflicts.",
        "acceptance": "1. All 10 step panels are accessible via sidebar click. 2. Step 9 "
                      "renders workflow template picker with 4 options. 3. Progress bar "
                      "updates on step change. 4. Back/Next buttons wrap correctly at "
                      "step boundaries.",
        "edge_cases": "Refreshing on a step other than step 1 must not break wizard state "
                      "(v1: all state is ephemeral JS, no persistence required).",
        "priority": "Medium",
        "status":   "Defined",
        "jira_epic": "PHXP-M04",
        "owner":    "Frontend Engineering",
    },
    # ── M09 ──────────────────────────────────────────────────────────────
    {
        "req_id":   "M09-APPT-001",
        "module_id": "M09 - Scheduling",
        "section":  "Scheduling / Appointment Workflow",
        "portal":   "Provider",
        "user_story": "As a scheduler or care team member, I need to book synchronous "
                      "appointments (phone/video) for patients through a multi-path scheduling "
                      "tool so that providers and patients are matched with appropriate "
                      "availability slots.",
        "requirement": "The scheduling tool must support three booking paths: (A) Patient "
                       "First — select patient → care product → provider → slot; (B) Provider "
                       "First — select provider → date → patient → slot; (C) Date First — "
                       "select date → care product → available providers → slot. All paths "
                       "must terminate in a confirmation step with consult type (phone/video), "
                       "duration, and provider name displayed.",
        "rule":     "Scheduling is only applicable for synchronous consult types (phone, "
                    "video). Async and refill consults do not require scheduled slots. "
                    "State/license matching must be validated before slot options are shown.",
        "acceptance": "1. All three booking paths complete without errors. 2. Confirmation "
                      "step shows provider, date/time, consult type, and patient. 3. "
                      "Out-of-state providers are filtered from slot results.",
        "edge_cases": "Double-booking the same provider slot must show an error, not create "
                      "a duplicate appointment.",
        "priority": "High",
        "status":   "Defined",
        "jira_epic": "PHXP-M09",
        "owner":    "Scheduling Team",
    },
    # ── M11 ──────────────────────────────────────────────────────────────
    {
        "req_id":   "M11-TIER-001",
        "module_id": "M11 - Care Tiers & Escalation",
        "section":  "Care Tiers / Definition",
        "portal":   "Provider",
        "user_story": "As a clinical operations lead, I need care products to be classified "
                      "into tiers (async-only, hybrid, full synchronous) so that routing "
                      "logic, SLA targets, and provider assignments can be configured "
                      "per tier.",
        "requirement": "The platform must support three care tier classifications: Tier 1 "
                       "(Async-Only — no scheduled visits, e.g. STI Treatment, Refill); "
                       "Tier 2 (Hybrid — async intake with optional synchronous follow-up, "
                       "e.g. A1C Management, Weight Management); Tier 3 (Full Sync — "
                       "requires scheduled visit, e.g. initial Testosterone Care consult). "
                       "Tier is set at the care product level in the admin wizard.",
        "rule":     "Tier determines which consult types are available at booking. Tier 1 "
                    "products must not be bookable as phone/video in the scheduling tool. "
                    "Tier 3 products must require a scheduled slot before prescribing.",
        "acceptance": "1. Admin wizard Step 2 (Provider Type) exposes a tier selector. "
                      "2. Tier 1 products are absent from the scheduler's synchronous "
                      "booking flow. 3. Tier 3 products block Rx actions until a visit "
                      "is confirmed.",
        "edge_cases": "Care product tier change after active consults exist must not "
                      "retroactively alter in-flight consult type.",
        "priority": "High",
        "status":   "In Design",
        "jira_epic": "PHXP-M11",
        "owner":    "Clinical Operations / Product",
    },
    {
        "req_id":   "M11-TIER-002",
        "module_id": "M11 - Care Tiers & Escalation",
        "section":  "Care Tiers / Escalation Path",
        "portal":   "Provider",
        "user_story": "As a provider managing an async consult, I need a structured escalation "
                      "path to upgrade a consult to a synchronous visit when the clinical "
                      "situation warrants it, without losing the async context already "
                      "captured.",
        "requirement": "Providers must be able to escalate any Tier 1 or Tier 2 async consult "
                       "to a synchronous visit via a queue 'Route' or 'Escalate' action. "
                       "Escalation must: (a) retain all prior async data in the chart; "
                       "(b) create a scheduling request visible to schedulers; (c) update "
                       "the consult's workflow stage to 'Pre-visit prep'.",
        "rule":     "Escalation is not auto-approved; it creates a pending scheduling request "
                    "that a scheduler must confirm. The original async consult record is "
                    "not deleted.",
        "acceptance": "1. Escalate button appears on eligible async queue rows. 2. Clicking "
                      "Escalate creates a scheduling request record. 3. Chart retains all "
                      "pre-escalation data. 4. Workflow stage updates to 'Pre-visit prep'.",
        "edge_cases": "Escalating a consult already in 'Pre-visit prep' stage must show "
                      "a warning rather than creating a duplicate request.",
        "priority": "High",
        "status":   "In Design",
        "jira_epic": "PHXP-M11",
        "owner":    "Clinical Operations / Product",
    },
    {
        "req_id":   "M11-TIER-003",
        "module_id": "M11 - Care Tiers & Escalation",
        "section":  "Care Tiers / SLA by Tier",
        "portal":   "Provider",
        "user_story": "As a clinical operations manager, I need SLA targets to be configurable "
                      "per care tier so that higher-acuity synchronous tiers have tighter "
                      "response windows than async-only products.",
        "requirement": "SLA targets must be tier-aware: Tier 1 default SLA = 24 h response; "
                       "Tier 2 default SLA = 4 h for async intake, 2 h for scheduled follow-up; "
                       "Tier 3 default SLA = 1 h pre-visit prep. SLA configuration is set "
                       "in the admin SLA Config page (/admin/sla-config) and applied per "
                       "care product via tier mapping.",
        "rule":     "SLA breach triggers a queue SLA badge change and an in-app notification "
                    "to the assigned provider and their supervisor. SLA config changes apply "
                    "to new consults only, not retroactively.",
        "acceptance": "1. Admin SLA Config page shows tier-level SLA fields. 2. A Tier 1 "
                      "consult past 24 h shows 'Overdue' badge. 3. A Tier 3 consult past "
                      "1 h shows 'Overdue' badge. 4. SLA change does not alter existing "
                      "in-flight consult SLA countdown.",
        "edge_cases": "Care products with no tier assigned default to Tier 2 SLA targets "
                      "until tier is explicitly set by admin.",
        "priority": "Medium",
        "status":   "In Design",
        "jira_epic": "PHXP-M11",
        "owner":    "Clinical Operations / Product",
    },
]

# ── fixed columns ─────────────────────────────────────────────────────────
FIXED = {
    "source":           SOURCE,
    "date_added":       DATE,
    "last_updated":     DATE,
    "exported_version": "v1",
}


def main():
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    cur.execute("SELECT req_id FROM requirements")
    existing = {row[0] for row in cur.fetchall()}

    inserted = []
    skipped  = []

    for req in REQUIREMENTS:
        rid = req["req_id"]
        if rid in existing:
            skipped.append(rid)
            continue

        row = {**req, **FIXED}
        # ensure all columns present (fill missing with None)
        columns = [
            "req_id", "module_id", "section", "portal", "user_story",
            "requirement", "rule", "acceptance", "edge_cases", "priority",
            "status", "jira_epic", "owner", "source", "date_added",
            "last_updated", "exported_version",
        ]
        values = [row.get(c) for c in columns]
        placeholders = ", ".join("?" * len(columns))
        col_names    = ", ".join(columns)
        cur.execute(
            f"INSERT INTO requirements ({col_names}) VALUES ({placeholders})",
            values,
        )
        inserted.append(rid)

    conn.commit()
    conn.close()

    # ── report ────────────────────────────────────────────────────────────
    print("=" * 66)
    print("  PROJECT PHOENIX — DB COMMIT  db_commit_p16_p18_v1.py")
    print(f"  Source : {SOURCE}")
    print(f"  Date   : {DATE}")
    print("=" * 66)

    modules = {}
    for rid in inserted:
        mod = rid.split("-")[0] + "-" + rid.split("-")[1] if "-" in rid else rid[:3]
        mod = rid[:3]          # M02 / M04 / M09 / M11
        modules.setdefault(mod, []).append(rid)

    if inserted:
        print(f"\n  ✅  INSERTED  ({len(inserted)} rows)")
        for mod, ids in sorted(modules.items()):
            print(f"\n  Module {mod}  ({len(ids)} req{'s' if len(ids)>1 else ''})")
            for rid in ids:
                req = next(r for r in REQUIREMENTS if r["req_id"] == rid)
                print(f"    + {rid:<20}  [{req['priority']:<8}]  {req['section']}")
    else:
        print("\n  (no new rows inserted)")

    if skipped:
        print(f"\n  ⏭   SKIPPED  ({len(skipped)} already exist)")
        for rid in skipped:
            print(f"    · {rid}")

    print()
    print("-" * 66)
    print(f"  Total attempted : {len(REQUIREMENTS)}")
    print(f"  Inserted        : {len(inserted)}")
    print(f"  Skipped         : {len(skipped)}")
    print("-" * 66)

    # Module breakdown (all requirements, including pre-existing)
    conn2 = sqlite3.connect(DB_PATH)
    cur2  = conn2.cursor()
    cur2.execute(
        "SELECT module_id, COUNT(*) FROM requirements GROUP BY module_id ORDER BY module_id"
    )
    rows = cur2.fetchall()
    conn2.close()
    print("\n  DATABASE MODULE BREAKDOWN (total)")
    for mod_id, count in rows:
        print(f"    {mod_id:<45}  {count:>3} req{'s' if count>1 else ''}")
    print("=" * 66)


if __name__ == "__main__":
    main()
