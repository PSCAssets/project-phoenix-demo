#!/usr/bin/env python3
"""
Patient Portal Isolation + Provider Eligibility Requirements — DB Commit Script v1
June 18, 2026
Source: Jessica Wheeler legal review + Justin Woller design sessions
Modules: M01, M03, M04
"""

import sqlite3
from datetime import date

DB_PATH = '/Users/justin.woller/Documents/project-phoenix-demo/project_phoenix.db'
TODAY = str(date.today())

requirements = [

    # ─────────────────────────────────────────────
    # M03 — Patient Portal
    # ─────────────────────────────────────────────

    ('M03-ECO-001', 'M03 - Patient Portal', 'Portal Ecosystem Model', 'Patient Portal',
     'Each care product must be classified into one of two portal ecosystems: Everlywell Platform or Isolated Partner — and the patient portal experience is determined entirely by the ecosystem of the care product the patient accesses.',
     'The platform supports two patient portal ecosystem types. Everlywell Platform: patient portal is branded as Everlywell; patient can access multiple Everlywell-ecosystem programs under one account via a program switcher; DTC and health plan clients are both eligible. Isolated Partner: patient portal is branded exclusively as the partner (e.g., PWN Health); no Everlywell branding appears anywhere; data from Isolated Partner programs is never shown in an Everlywell Platform portal and vice versa; the patient account in an Isolated Partner context is a separate isolated account. Ecosystem classification is set at the care product level in the Admin Portal wizard.',
     'Isolated Partner portal: no Everlywell branding, no cross-ecosystem data, no program switcher to Everlywell programs. Everlywell Platform portal: program switcher available if patient is enrolled in multiple Everlywell programs. A patient may have accounts in both ecosystems using the same email address but the accounts are never linked or merged.',
     'A patient with a PWN program and an Everlywell program uses the same email address to log into each but arrives at completely separate portal experiences via different entry points (subdomain or deep link).',
     'Attempting to access cross-ecosystem data via API or direct URL must be rejected at the server level, not just hidden in the UI. Ecosystem boundary is enforced server-side.',
     'High', 'Active', 'M03', 'Engineering / Legal', 'Jessica Wheeler legal review — Jun 18 2026', TODAY, TODAY, None),

    ('M03-ECO-002', 'M03 - Patient Portal', 'Portal Ecosystem Model', 'Patient Portal',
     'Patient portal data must be hard-isolated at the ecosystem level — consultation history, lab results, and account data from Isolated Partner programs must never appear in the Everlywell Platform portal, and vice versa.',
     'Hard data isolation is a legal requirement established by Jessica Wheeler. Consultation records, lab results, care product enrollments, and communication history associated with an Isolated Partner program (e.g., PWN) must be stored and served in complete isolation from Everlywell Platform records. Even if the same patient email address exists in both ecosystems, there is no data joining, blending, or cross-referencing. The patient chart for a PWN consult is never accessible from an Everlywell portal session. This isolation applies at the data layer — not just the UI.',
     'Data queries for patient portal sessions must be scoped to the session\'s ecosystem context. No ORM join, API endpoint, or data export can return records across ecosystem boundaries for a patient-facing session.',
     'A security audit must confirm that no patient-facing endpoint returns cross-ecosystem records. This is a HIPAA business associate agreement boundary as much as a product requirement.',
     'Cross-ecosystem data leak in any form (including aggregate statistics or suggested care products) is a compliance violation. Pen test and security review must include cross-ecosystem data boundary testing.',
     'High', 'Active', 'M03', 'Engineering / Legal / Compliance', 'Jessica Wheeler legal review — Jun 18 2026', TODAY, TODAY, None),

    ('M03-ECO-003', 'M03 - Patient Portal', 'Portal Ecosystem Model', 'Patient Portal',
     'Isolated Partner patient portal must be branded exclusively as the partner — no Everlywell name, logo, color, or reference may appear anywhere in the patient experience.',
     'When a patient accesses an Isolated Partner portal (e.g., PWN Health), the entire patient-facing experience — including login page, portal header, email communications, PDF documents, and in-app notifications — must reflect the partner branding only. Everlywell branding is not permitted in any form. The subdomain, logo, color scheme, and application name are all partner-specific. This is a contractual requirement for partners who have their own patient-facing brand relationships.',
     'Isolated Partner branding overrides all defaults. Logo, primary color, application name, and email sender name are all configured per partner in the Admin Portal. No fallback to Everlywell branding if a branding field is not configured — instead, the portal must not launch until branding is complete.',
     'A missing logo or color config on an Isolated Partner care product blocks the portal from being published until resolved.',
     'Email notifications sent to patients in an Isolated Partner program must use the partner\'s configured sender name and branding. Everlywell email domain must not be visible in the patient-facing from address for Isolated Partner programs.',
     'High', 'Active', 'M03', 'Engineering / Partnerships / Legal', 'Jessica Wheeler legal review — Jun 18 2026', TODAY, TODAY, None),

    ('M03-MIGR-001', 'M03 - Patient Portal', 'Patient Migration', 'Patient Portal',
     'Historical patients from the PWN platform will not be migrated to Project Phoenix patient portal accounts retroactively — portal access is created only when a patient receives a new consult on the Project Phoenix platform.',
     'No bulk import of PWN patient portal history is required. When a patient from the legacy PWN platform has a new consult created on Project Phoenix (for a care product in the PWN Isolated Partner ecosystem), the system creates a new persistent patient account at that point. The patient receives an account activation email to set their password. All prior PWN consults that were completed on the legacy platform remain on the legacy system and are not imported into Project Phoenix. Historical consults are not surfaced in the new portal.',
     'Patient account creation is triggered by the first new consult on Project Phoenix for that patient. Account creation email is sent to the patient\'s email on file. Account is associated with the partner ecosystem of the care product that triggered creation.',
     'If a patient already has an account in a different ecosystem (e.g., Everlywell Platform), the new Isolated Partner account is created independently — no merging occurs.',
     'Duplicate email across ecosystems is permitted and expected. The system must handle the same email address existing in both the Everlywell Platform and an Isolated Partner ecosystem without conflict.',
     'High', 'Active', 'M03', 'Engineering / Care Team Ops', 'Justin Woller — Jun 18 2026', TODAY, TODAY, None),

    ('M03-PROG-001', 'M03 - Patient Portal', 'Program Switcher', 'Patient Portal',
     'Patients enrolled in multiple programs within the Everlywell Platform ecosystem must be able to switch between programs from within the portal using a program selector.',
     'A program selector is displayed in the Everlywell Platform patient portal header when the patient is enrolled in more than one Everlywell-ecosystem program. The selector shows the currently active program and provides a dropdown to switch between enrolled programs. Programs include both DTC (direct-to-consumer) and health plan programs configured as Everlywell Platform ecosystem care products. When switching programs, the portal header branding updates to reflect the selected client configuration (logo, primary color if client-branded), and the visible care products, consult history, and results are scoped to the selected program. The patient\'s underlying account is the same — only the program context changes.',
     'Program selector shows: all active enrollments for the patient in the Everlywell Platform ecosystem. Switching programs updates: header client branding, available care products, consult history displayed, lab results displayed. Does not require re-authentication.',
     'Patient with only one program enrollment sees no program selector — single-program view is the default.',
     'Program switching is instantaneous from the patient perspective — no full page reload. Selected program context persists for the session.',
     'High', 'Active', 'M03', 'Engineering / UX', 'Justin Woller — Jun 18 2026', TODAY, TODAY, None),

    ('M03-ACCESS-001', 'M03 - Patient Portal', 'Data Access Rights', 'Patient Portal',
     'Patients must always retain access to their data in the portal, regardless of contract status, program end date, or partner relationship changes.',
     'A patient\'s access to their own consultation history, lab results, and health records in the patient portal is permanent. No contract expiration, client offboarding, or program sunset can remove a patient\'s ability to view their own historical data. If a care product is deactivated, patients with prior consults under that product retain read-only access to those records. If a partner (e.g., PWN) contract ends, the Isolated Partner portal remains accessible to patients in read-only mode for their historical records. Patients are never locked out of their own health data.',
     'Patient data access: permanent read-only regardless of program or partner status. New consult creation may be disabled when a program ends, but existing records remain accessible. Portal login continues to function for historical record access even after program deactivation.',
     'When a care product is deactivated, the system sends patients a notification explaining that new consults are no longer available but their records remain accessible.',
     'Data retention for patient records follows applicable state and federal health record retention laws regardless of contract status.',
     'High', 'Active', 'M03', 'Engineering / Legal / Compliance', 'Justin Woller + Jessica Wheeler — Jun 18 2026', TODAY, TODAY, None),

    # ─────────────────────────────────────────────
    # M04 — Admin Portal
    # ─────────────────────────────────────────────

    ('M04-ECO-001', 'M04 - Admin Portal', 'Care Product Configuration', 'Admin Portal',
     'Each care product must be assigned an ecosystem classification during setup: Everlywell Platform or Isolated Partner.',
     'The care product wizard includes an Ecosystem Classification step. Admin selects: Everlywell Platform (patient portal is under the Everlywell umbrella; program switcher eligible; Everlywell or client co-branding) or Isolated Partner (patient portal is completely isolated; partner branding only; no Everlywell branding; separate data boundary). This classification cannot be changed after the first patient account is created under that care product — it is a foundational data isolation setting. The Admin Portal displays a warning if an admin attempts to change the classification on an active care product.',
     'Ecosystem classification is required before a care product can be published. Attempting to publish without classification returns a validation error. Classification is immutable after first patient account creation.',
     'A care product in draft state (no patient accounts yet) can have its ecosystem classification changed by an admin with appropriate permissions.',
     'Changing ecosystem classification on a care product with active patient accounts is blocked at the UI and API level. Admin receives a clear error explaining why the change is locked.',
     'High', 'Active', 'M04', 'Engineering / Admin', 'Justin Woller + Jessica Wheeler — Jun 18 2026', TODAY, TODAY, None),

    ('M04-BRD-002', 'M04 - Admin Portal', 'Care Product Branding', 'Admin Portal',
     'Care product branding configuration must support logo upload and a full color palette in version 1.0.',
     'The Portal Branding step in the care product wizard allows admins to configure: (1) Logo — upload PNG or SVG file, max 2MB, displayed in patient portal header and email communications; (2) Primary Color — hex color picker, used for buttons, active states, and accents; (3) Secondary Color — hex color picker, used for backgrounds and secondary UI elements; (4) Header Background Color — hex color picker, used for the portal top navigation bar. For Everlywell Platform care products: branding is optional (defaults to Everlywell brand). For Isolated Partner care products: branding is required — portal cannot be published without a logo and primary color.',
     'Logo formats: PNG, SVG. Max 2MB. Primary, secondary, and header colors: hex input with preview swatch. Live preview panel in the wizard shows how the branding will appear in the portal header before saving.',
     'Invalid hex color values return a validation error inline. Logo files exceeding 2MB return an upload error with file size shown.',
     'Branding changes on a published care product take effect immediately for all active patient sessions on next page load.',
     'High', 'Active', 'M04', 'Engineering / Design', 'Justin Woller — Jun 18 2026', TODAY, TODAY, None),

    ('M04-PRV-010', 'M04 - Admin Portal', 'Provider Eligibility', 'Admin Portal',
     'Each care product must support a provider exclusion list that removes specific providers from eligibility for that care product while maintaining the default all-providers model.',
     'The default provider eligibility model is: all providers contracted with the platform are eligible to serve all commercial care products in the states where they hold active licenses. The care product wizard includes a Provider Eligibility step where admins can create an exclusion list — specific providers who should NOT be assigned to this care product. Excluded providers do not appear in the assignment pool for that care product. This model applies to all care product types including specialized products (e.g., Genetics). For Genetics or other restricted products, the admin excludes all non-qualified providers; for standard products, exclusions are rare exceptions.',
     'Provider exclusion list: admin searches for providers by name or NPI and adds them to the exclusion list. Excluded providers are hidden from assignment for that care product. All non-excluded providers remain eligible (subject to state licensing). Exclusion list is editable at any time.',
     'A provider added to the exclusion list after having active consults under that care product is excluded from new consult assignment but their existing assigned consults are not affected.',
     'Provider search in exclusion list supports: name, NPI number, specialty. Exclusion list displays current excluded providers with the ability to remove exclusions.',
     'High', 'Active', 'M04', 'Engineering / Admin / Credentialing', 'Justin Woller — Jun 18 2026', TODAY, TODAY, None),

    ('M04-PRV-011', 'M04 - Admin Portal', 'Provider Eligibility', 'Admin Portal',
     'Care products flagged as Medicare or Medicaid programs must use an explicit provider assignment model with state-level enrollment specification instead of the default all-providers model.',
     'When a care product is flagged as Medicare or Medicaid in the care product wizard, the provider eligibility model switches from default-all with exclusions to explicit assignment. The admin must explicitly add providers to the eligible list for that care product and specify which states each provider is enrolled in for that Medicare or Medicaid program. Only providers explicitly assigned with an active enrollment in the patient\'s state are eligible for consult assignment on Medicare/Medicaid care products. This explicit assignment can also be managed from the provider profile section of the Admin Portal.',
     'Medicare/Medicaid care product: provider eligibility list is empty by default. Admin adds providers and specifies per-provider enrolled states. Assignment engine filters to providers with active enrollment in the patient\'s state. Providers without enrollment in the patient\'s state are not shown in the assignment pool.',
     'A Medicare/Medicaid care product with no eligible providers configured cannot be published — admin receives a validation error requiring at least one provider assignment before publishing.',
     'If an admin publishes a Medicare/Medicaid care product and all assigned providers subsequently become ineligible (e.g., enrollments all expire), the care product is automatically suspended and admin is notified.',
     'High', 'Active', 'M04', 'Engineering / Credentialing / Compliance', 'Justin Woller — Jun 18 2026', TODAY, TODAY, None),

    ('M04-PRV-012', 'M04 - Admin Portal', 'Provider Eligibility', 'Admin Portal',
     'Provider profiles in the Admin Portal must display and allow management of Medicare and Medicaid enrollment status per state.',
     'The provider profile section of the Admin Portal includes a Medicare/Medicaid Enrollment tab. For each provider, admins can view and manage: Medicare enrollment status per state (Active, Pending, Expired, Not Enrolled), Medicaid enrollment status per state (Active, Pending, Expired, Not Enrolled), enrollment effective date, and enrollment expiration date. Changes made in the provider profile automatically update the provider\'s eligibility across all Medicare/Medicaid care products that reference them. This is the second place (alongside the care product wizard) where Medicare/Medicaid provider assignments can be managed.',
     'Provider profile Medicare/Medicaid tab shows a state-by-state enrollment matrix. Each cell: Medicare status, Medicaid status. Admin can add, update, or remove enrollment records per state. Changes take effect immediately on provider eligibility.',
     'Editing enrollment status requires admin-level permissions. Changes are logged to the audit trail with timestamp and admin ID.',
     'Provider profile enrollment tab is read-accessible to Care Team coordinators for reference but only editable by credentialing admins.',
     'High', 'Active', 'M04', 'Engineering / Admin / Credentialing', 'Justin Woller — Jun 18 2026', TODAY, TODAY, None),

    ('M04-PRV-013', 'M04 - Admin Portal', 'Provider Eligibility', 'Admin Portal',
     'The system must automatically remove a provider from Medicare and Medicaid care product eligibility when their enrollment in a given state expires.',
     'When a Medicare or Medicaid enrollment record reaches its expiration date, the system automatically: (1) removes the provider from the eligible assignment pool for all Medicare/Medicaid care products in that state; (2) generates an admin notification identifying the provider, the expired enrollment, and the affected care products; (3) logs the automatic removal to the provider\'s audit trail. The provider is not manually removed — the system enforces this automatically based on the expiration date stored in the provider profile. Re-enrollment requires an admin to update the enrollment record with a new effective and expiration date, which automatically restores eligibility.',
     'Automated enforcement runs daily. Enrollments expiring within 30 days trigger a warning notification to credentialing admins. On expiration date: provider removed from pool, admin notified, audit log entry created. Provider is removed from assignment queue for affected care products — existing active consults assigned to that provider are not affected.',
     'A 30-day advance warning gives credentialing teams time to renew before automatic removal.',
     'If enrollment expiration data is not present for a Medicare/Medicaid provider assignment, the system flags the record as "Expiration Unknown" and generates an admin alert to populate the date.',
     'High', 'Active', 'M04', 'Engineering / Credentialing / Compliance', 'Justin Woller — Jun 18 2026', TODAY, TODAY, None),

    # ─────────────────────────────────────────────
    # M01 — Roles & Responsibilities
    # ─────────────────────────────────────────────

    ('M01-PRV-001', 'M01 - Roles & Responsibilities', 'Provider Eligibility Model', 'Admin Portal',
     'The default provider eligibility model for all commercial care products is all licensed providers — every provider contracted with the platform is eligible for all commercial care products in the states where they hold active licenses.',
     'Provider Network 2.0 establishes an inclusive default: a provider does not need to be explicitly opted in to a care product to be eligible for assignment. Eligibility is determined by: active contract status, active state license in the patient\'s state, and absence from the care product\'s exclusion list. This model eliminates the need for manual per-provider per-care-product approvals for standard commercial programs. It assumes all contracted providers are qualified for all commercial care products unless specifically excluded.',
     'Provider is eligible for assignment if: (1) contract status is Active, (2) active license in patient\'s state exists, (3) provider is not on the care product\'s exclusion list. All three conditions must be true. Commercial care products only — Medicare/Medicaid care products use explicit assignment model.',
     'A provider added to a care product exclusion list remains eligible for all other care products they are not excluded from.',
     'If a state license expires, the provider is automatically ineligible for new consult assignment in that state across all care products. Existing assigned consults are not affected.',
     'High', 'Active', 'M01', 'Provider Operations / Engineering', 'Justin Woller — Jun 18 2026', TODAY, TODAY, None),

    ('M01-PRV-002', 'M01 - Roles & Responsibilities', 'Provider Eligibility Model', 'Admin Portal',
     'Specialized care products (e.g., Genetics) use the same exclusion list model as commercial care products, but in practice the exclusion list contains all non-qualified providers, effectively creating a qualified-provider-only pool.',
     'There is no separate whitelist model for specialized care products. The exclusion list mechanism (M04-PRV-010) is the single provider eligibility tool for all non-Medicare/Medicaid care products. For specialized programs where only a small subset of providers are qualified (e.g., Genetics programs requiring Genetic Counselor or genetics-trained provider), the admin excludes all providers who do not hold the required qualification. The result is functionally equivalent to a whitelist but uses the same consistent exclusion mechanism across the platform. Documentation on the care product should note the qualification requirement so credentialing admins know who to exclude.',
     'Genetics or other specialized care product: admin adds all non-qualified providers to exclusion list. Assignment engine sees only qualified providers as eligible. No separate mechanism required.',
     'When a new provider is contracted with the platform, they are automatically eligible for all standard commercial care products but must be explicitly excluded from specialized care products they are not qualified for. Credentialing admins are notified of new provider onboarding so they can review exclusion list applicability.',
     'A specialized care product with all available providers excluded cannot be assigned to any consult — admin is warned when exclusion count approaches total provider count.',
     'High', 'Active', 'M01', 'Provider Operations / Engineering', 'Justin Woller — Jun 18 2026', TODAY, TODAY, None),

]

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

inserted = 0
skipped = 0
for req in requirements:
    req_id = req[0]
    c.execute('SELECT req_id FROM requirements WHERE req_id = ?', (req_id,))
    if c.fetchone():
        print(f'  SKIP (exists): {req_id}')
        skipped += 1
    else:
        c.execute('''INSERT INTO requirements
            (req_id, module_id, section, portal, user_story, requirement, rule, acceptance, edge_cases,
             priority, status, jira_epic, owner, source, date_added, last_updated, exported_version)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', req)
        print(f'  INSERTED: {req_id}')
        inserted += 1

conn.commit()
conn.close()

print(f'\nDone. Inserted: {inserted} | Skipped: {skipped} | Total attempted: {len(requirements)}')
