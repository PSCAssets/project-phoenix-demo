#!/usr/bin/env python3
"""
Project Phoenix — Prompt 5 / 6 / 7 Validation Script
Run from: ~/Documents/project-phoenix-demo/
Usage:   python3 validate_567.py
"""

import os
import sys
import subprocess
import time
from pathlib import Path

try:
    import requests
except ImportError:
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'requests', '-q'])
    import requests

BASE_DIR  = Path(__file__).parent
TEMPLATES = BASE_DIR / 'templates'
BASE_URL  = 'http://127.0.0.1:5001'
PASS, FAIL, WARN = '✅', '❌', '⚠️ '

results = []
_server = None

def _log(status, label, detail=''):
    results.append((status, label, detail))
    mark   = '  PASS' if status == PASS else ('  FAIL' if status == FAIL else '  WARN')
    suffix = f'  →  {detail}' if detail else ''
    print(f'{status}{mark}  {label}{suffix}')

def template_text(rel_path):
    p = TEMPLATES / rel_path
    if not p.exists():
        return None
    return p.read_text(encoding='utf-8', errors='ignore').lower()

def has(rel_path, *terms, label=None, require_all=True):
    text = template_text(rel_path)
    tag  = label or f'{rel_path}: contains "{", ".join(terms)}"'
    if text is None:
        _log(FAIL, tag, 'file not found')
        return False
    if require_all:
        ok = all(t.lower() in text for t in terms)
    else:
        ok = any(t.lower() in text for t in terms)
    missing = [t for t in terms if t.lower() not in text] if not ok else []
    _log(PASS if ok else FAIL, tag, f'missing: {missing}' if missing else '')
    return ok

def has_not(rel_path, term, label=None):
    text = template_text(rel_path)
    tag  = label or f'{rel_path}: must NOT contain "{term}"'
    if text is None:
        _log(FAIL, tag, 'file not found')
        return False
    ok = term.lower() not in text
    _log(PASS if ok else FAIL, tag, f'still present: "{term}"' if not ok else '')
    return ok

def file_exists(rel_path, label=None):
    p   = TEMPLATES / rel_path
    tag = label or f'File exists: {rel_path}'
    _log(PASS if p.exists() else FAIL, tag)
    return p.exists()

def route_ok(path, role, expected=200):
    try:
        s = requests.Session()
        s.post(f'{BASE_URL}/login', data={'role': role},
               allow_redirects=True, timeout=4)
        r = s.get(f'{BASE_URL}{path}', timeout=4, allow_redirects=False)
        ok = r.status_code == expected
        _log(PASS if ok else FAIL,
             f'Route {path} → {expected}',
             f'got {r.status_code}' if not ok else '')
        return ok
    except Exception as e:
        _log(FAIL, f'Route {path}', str(e))
        return False

def section(title):
    print(f'\n{"─" * 68}\n  {title}\n{"─" * 68}')

def start_server():
    global _server
    env = {**os.environ, 'PORT': '5001', 'FLASK_RUN_PORT': '5001'}
    _server = subprocess.Popen(
        [sys.executable, 'app.py'],
        cwd=str(BASE_DIR), env=env,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    for _ in range(14):
        time.sleep(0.5)
        try:
            requests.get(f'{BASE_URL}/', timeout=1)
            print('  Server ready.\n')
            return True
        except Exception:
            pass
    print('  ⚠️  Server did not start — route checks will fail.\n')
    return False

def stop_server():
    if _server:
        _server.terminate()
        try:
            _server.wait(timeout=5)
        except Exception:
            _server.kill()

def check_prompt5():
    section('PROMPT 5 — Patient Portal')
    section('5A · Dashboard')
    has_not('patient/dashboard.html', 'provider',
            label='Nav: no provider name in patient nav bar')
    has('patient/dashboard.html', 'view appointment',
        label='Care card: "View Appointment" button for booked appt')
    has_not('patient/dashboard.html', 'line-through',
            label='Checklist: no strikethrough styling on completed items')
    has('patient/dashboard.html', 'async',
        label='Care card: Async consult type badge visible')
    has('patient/dashboard.html', 'video',
        label='Care card: Video consult type badge visible')
    section('5B · Messages')
    has('patient/messages.html', 'care messages',
        label='Two-tab split: "Care Messages" tab present')
    has('patient/messages.html', 'support',
        label='Two-tab split: "Support" tab present')
    section('5C · Labs')
    has('patient/labs.html', 'hba1c', '6.8',
        label='Labs: HbA1c 6.8% result row present')
    has('patient/labs.html', 'elevated',
        label='Labs: ELEVATED badge present')
    has('patient/labs.html', 'maria rodriguez',
        label='Labs: ordered by Maria Rodriguez NP')
    has('patient/labs.html', 'f59e0b', label='Labs: amber color on elevated result',
        require_all=False)
    section('5D · Health Profile — required sections')
    for term, lbl in [
        ('medical history','Medical History'),('current medications','Current Medications'),
        ('allergies','Allergies'),('family history','Family History'),
        ('social history','Social History'),('vitals','Vitals History'),
        ('preferred pharmacy','Preferred Pharmacy'),('emergency contact','Emergency Contact'),
    ]:
        has('patient/health_profile.html', term, label=f'Health Profile: {lbl} section')
    has('patient/health_profile.html', 'prediabetes',
        label='Health Profile: demo condition Prediabetes')
    has('patient/health_profile.html', 'metformin',
        label='Health Profile: demo medication Metformin')
    has('patient/health_profile.html', 'penicillin',
        label='Health Profile: demo allergy Penicillin')
    section('5E · Documents page')
    file_exists('patient/documents.html')
    has('patient/documents.html', 'telehealth consent',
        label='Documents: consent form row present')
    has('patient/documents.html', 'lab results',
        label='Documents: lab results row present')
    section('5F · Settings page')
    file_exists('patient/settings.html')
    has('patient/settings.html', 'notification',
        label='Settings: Notification preferences section')
    has('patient/settings.html', 'password',
        label='Settings: Change Password section')
    has('patient/settings.html', 'two-factor', 'sms',
        label='Settings: 2FA and SMS preferences', require_all=False)
    section('5G · Patient Routes')
    for path in ['/patient/dashboard','/patient/messages','/patient/labs',
                 '/patient/health-profile','/patient/documents','/patient/settings']:
        route_ok(path, role='patient')

def check_prompt6():
    section('PROMPT 6 — Admin Portal Restructure')
    section('6A · New admin templates exist')
    for t in ['admin/care_products.html','admin/users.html','admin/credentialing.html',
              'admin/integrations.html','admin/sla_config.html','admin/notifications.html',
              'admin/audit_log.html','admin/reports.html']:
        file_exists(t)
    section('6B · Care Products')
    has('admin/care_products.html', 'weight management', 'testosterone', 'brca',
        label='Care Products: demo products listed')
    has('admin/care_products.html', 'communication settings',
        label='Care Products: Communication Settings section')
    has('admin/care_products.html', 'provider notification',
        label='Care Products: provider notification on booking toggle')
    has('admin/care_products.html', 'add care product',
        label='Care Products: Add Care Product button')
    section('6C · User Management')
    has('admin/users.html', 'sarah lee', 'maria rodriguez', 'david nguyen',
        label='Users: demo users present')
    has('admin/users.html', 'invite user', label='Users: Invite User button/modal')
    has('admin/users.html', 'deactivate', label='Users: Deactivate action per row')
    section('6D · Provider Credentialing')
    has('admin/credentialing.html', 'verifiable',
        label='Credentialing: Verifiable source label')
    has('admin/credentialing.html', 'expiring', 'active',
        label='Credentialing: status labels')
    has('admin/credentialing.html', 'ca-md-123456',
        label='Credentialing: demo license CA-MD-123456')
    has('admin/credentialing.html', 'sync now',
        label='Credentialing: Sync Now button')
    section('6E · Integration Health')
    has('admin/integrations.html', 'athena', 'verifiable', 'billing',
        label='Integrations: Athena, Verifiable, Billing rows')
    has('admin/integrations.html', 'degraded',
        label='Integrations: Billing Platform degraded status')
    has('admin/integrations.html', 'last sync',
        label='Integrations: last sync timestamp')
    section('6F · SLA Configuration')
    has('admin/sla_config.html', 'warning threshold', 'breach threshold',
        label='SLA Config: threshold columns')
    has('admin/sla_config.html', 'weight management', label='SLA Config: Weight Management row')
    has('admin/sla_config.html', 'escalation', label='SLA Config: escalation rule column')
    section('6G · Notification Templates')
    has('admin/notifications.html', 'appointment confirmation',
        label='Notifications: Appointment Confirmation template')
    has('admin/notifications.html', 'provider booking notification',
        label='Notifications: Provider Booking Notification template')
    has('admin/notifications.html', 'sla', label='Notifications: SLA alert templates')
    has('admin/notifications.html', 'preview', label='Notifications: Preview button')
    section('6H · Audit Log')
    has('admin/audit_log.html', 'book_appointment', 'sign_chart',
        label='Audit Log: demo action type rows')
    has('admin/audit_log.html', 'export', label='Audit Log: Export CSV button')
    has('admin/audit_log.html', 'david nguyen', label='Audit Log: David Nguyen entry')
    section('6I · Reports')
    has('admin/reports.html', 'provider activity', 'patient enrollment',
        label='Reports: two report cards present')
    has('admin/reports.html', 'sla compliance', label='Reports: SLA Compliance card')
    has('admin/reports.html', '95.8', label='Reports: 95.8% demo figure')
    section('6J · Admin Routes')
    for path in ['/admin/care-products','/admin/users','/admin/credentialing',
                 '/admin/integrations','/admin/sla-config','/admin/notifications',
                 '/admin/audit-log','/admin/reports']:
        route_ok(path, role='admin')

def check_prompt7():
    section('PROMPT 7 — Provider Settings / Chart / Lab Auth / New Patient')
    section('7A · Provider Settings')
    has('provider/settings.html', 'profile', 'licenses', 'security',
        'notifications', 'preferences', label='Settings: all 5 tabs present')
    has('provider/settings.html', 'verifiable',
        label='Settings Licenses: Verifiable source label')
    has('provider/settings.html', 'ca-md-123456',
        label='Settings Licenses: demo license CA-MD-123456')
    has('provider/settings.html', 'expiring',
        label='Settings Licenses: expiring warning label')
    has('provider/settings.html', 'signature',
        label='Settings Profile: signature section')
    has('provider/settings.html', 'out of office',
        label='Settings Profile: out-of-office toggle')
    has('provider/settings.html', 'session timeout',
        label='Settings Security: session timeout preference')
    has('provider/settings.html', 'quiet hours',
        label='Settings Notifications: quiet hours section')
    has('provider/settings.html', 'two-factor', 'sms',
        label='Settings Security: 2FA section', require_all=False)
    has_not('provider/settings.html', 'active consults',
            label='Settings: no leftover dashboard widget content')
    section('7B · Patient Chart')
    has('provider/chart.html', 'subjective', 'objective', 'assessment', 'plan',
        label='Chart: all 4 SOAP sections present')
    has('provider/chart.html', 'review & sign', label='Chart: Review & Sign button')
    has('provider/chart.html', 'sign & close', label='Chart: Sign & Close Chart button')
    has_not('provider/chart.html', 'start consult',
            label='Chart: Start Consult button removed')
    has('provider/chart.html', '6.8', 'hba1c',
        label='Chart SOAP note: HbA1c 6.8% in objective section')
    section('7C · Lab Authorization — Oversight')
    has('provider/oversight.html', 'select all', label='Oversight: Select All checkbox')
    has('provider/oversight.html', 'authorize selected',
        label='Oversight: Authorize Selected button')
    has('provider/oversight.html', 'disabled',
        label='Oversight: disabled state when nothing selected')
    has('provider/oversight.html', 'confirm', label='Oversight: confirmation dialog')
    section('7D · New Patient Intake')
    has('provider/new_patient.html', 'existing patient',
        label='New Patient: Existing Patient path option')
    has('provider/new_patient.html', 'new patient registration',
        label='New Patient: New Patient Registration path option')
    has('provider/new_patient.html', 'insurance', 'billing',
        label='New Patient: Insurance + Billing steps')
    has('provider/new_patient.html', 'schedule appointment', 'real-time queue',
        label='New Patient: both booking options')
    has('provider/new_patient.html', 'phone', 'video', 'async',
        label='New Patient: all 3 consult type buttons')
    has_not('provider/new_patient.html', 'standard',
            label='New Patient: Standard priority removed')
    has_not('provider/new_patient.html', 'urgent',
            label='New Patient: Urgent priority removed')
    has('provider/new_patient.html', 'send intake questionnaire',
        label='New Patient: Async → Send Intake Questionnaire action')
    section('7E · Provider Route Regression')
    for path in ['/provider/settings','/provider/chart',
                 '/provider/oversight','/provider/new-patient']:
        route_ok(path, role='provider_md')

def print_summary():
    passed = [r for r in results if r[0] == PASS]
    failed = [r for r in results if r[0] == FAIL]
    total  = len(results)
    width  = 68
    print(f'\n{"═"*width}\n  VALIDATION SUMMARY\n{"═"*width}')
    print(f'  Total checks : {total}')
    print(f'  {PASS} Passed    : {len(passed)}')
    print(f'  {FAIL} Failed    : {len(failed)}')
    if failed:
        print(f'\n  ── Failed checks ──────────────────────────────────')
        for _, label, detail in failed:
            suffix = f'  →  {detail}' if detail else ''
            print(f'  {FAIL}  {label}{suffix}')
    print(f'\n{"═"*width}')
    if not failed:
        print('  🎉  ALL CHECKS PASSED — Prompts 5, 6, 7 look good.')
    else:
        print(f'  ⚠️   {len(failed)} check(s) failed. Fix and re-run.')
    print(f'{"═"*width}\n')
    return len(failed) == 0

if __name__ == '__main__':
    print('\n' + '═'*68)
    print('  PROJECT PHOENIX — Prompt 5 / 6 / 7 Validation')
    print('  Template content checks  +  live route checks')
    print('═'*68)
    print('\n▶ Starting Flask on port 5001 for route checks ...')
    start_server()
    try:
        check_prompt5()
        check_prompt6()
        check_prompt7()
    finally:
        stop_server()
    success = print_summary()
    sys.exit(0 if success else 1)
