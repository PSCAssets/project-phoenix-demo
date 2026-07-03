import os
import time
import sqlite3
import logging
import requests
from datetime import datetime, timedelta, timezone
from flask import Flask, render_template, session, redirect, url_for, request
from modules import provider, patient, admin, care_team, scheduler
import workflow_config

app = Flask(__name__)
app.secret_key = 'project-phoenix-demo-secret-2026'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)

# ── Demo Environment Gate ──────────────────────────────────────────────────
# Enabled on Render (DEMO_GATE=true) OR whenever not running locally.
# Falls back to checking FLASK_ENV / PORT so local `python app.py` is unaffected.
_IS_LOCAL = os.environ.get('FLASK_ENV') == 'development' or (
    not os.environ.get('RENDER') and os.environ.get('PORT', '5000') == '5000'
    and not os.environ.get('DEMO_GATE')
)
DEMO_GATE = not _IS_LOCAL
GATE_TIMEOUT_SECONDS = 15 * 60   # 15 minutes of inactivity
GATE_BYPASS_ROUTES   = {'gate_login', 'gate_login_post', 'static'}

_DB_PATH = os.path.join(os.path.dirname(__file__), 'project_phoenix.db')

# ── Seed page guides on startup (ensures Render has all content) ──────────────
try:
    from seed_page_guides import seed as _seed_page_guides
    _seed_page_guides(_DB_PATH)
except Exception as _e:
    print(f"[startup] page guide seed skipped: {_e}")

# ── Access log — SQLite (current session) + Supabase (permanent history) ──────
_SUPABASE_URL = os.environ.get('SUPABASE_URL', '').rstrip('/')
_SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')

def _sb_headers():
    return {
        'apikey':        _SUPABASE_KEY,
        'Authorization': f'Bearer {_SUPABASE_KEY}',
        'Content-Type':  'application/json',
        'Prefer':        'return=minimal',
    }

def _init_access_log():
    """Create access_log table in SQLite if it doesn't exist (session cache)."""
    try:
        with sqlite3.connect(_DB_PATH) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS access_log (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp  TEXT    NOT NULL,
                    name       TEXT    NOT NULL,
                    email      TEXT    NOT NULL,
                    ip         TEXT,
                    login_num  INTEGER DEFAULT 1
                )
            ''')
            conn.commit()
    except Exception as e:
        logging.error('access_log init failed: %s', e)

_init_access_log()

def _record_gate_access(name, email, ip):
    """Write login to Supabase (permanent) + SQLite (session cache)."""
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    login_num = 1

    # ── 1. Supabase write (permanent across redeploys) ──────────────────────
    if _SUPABASE_URL and _SUPABASE_KEY:
        try:
            # Get prior login count for this email
            resp = requests.get(
                f'{_SUPABASE_URL}/rest/v1/access_log',
                params={'email': f'eq.{email}', 'select': 'id'},
                headers=_sb_headers(), timeout=5
            )
            login_num = len(resp.json()) + 1 if resp.ok else 1
            requests.post(
                f'{_SUPABASE_URL}/rest/v1/access_log',
                json={'timestamp': ts, 'name': name, 'email': email,
                      'ip': ip, 'login_num': login_num},
                headers=_sb_headers(), timeout=5
            )
            logging.info('Supabase write OK — %s login #%d', email, login_num)
        except Exception as e:
            logging.warning('Supabase write failed: %s', e)

    # ── 2. SQLite write (session cache / fallback) ───────────────────────────
    try:
        with sqlite3.connect(_DB_PATH) as conn:
            cur = conn.cursor()
            if login_num == 1:  # Supabase unavailable — count locally
                cur.execute('SELECT COUNT(*) FROM access_log WHERE email = ?', (email,))
                login_num = (cur.fetchone()[0] or 0) + 1
            cur.execute(
                'INSERT INTO access_log (timestamp, name, email, ip, login_num) '
                'VALUES (?,?,?,?,?)',
                (ts, name, email, ip, login_num)
            )
            conn.commit()
    except Exception as e:
        logging.error('SQLite access_log write failed: %s', e)

    # ── 3. Email notification ────────────────────────────────────────────────
    try:
        requests.post(
            'https://api.resend.com/emails',
            headers={'Authorization': 'Bearer re_8PxamR2S_LnumH7ac2B4EmDqeHTKzpWxe',
                     'Content-Type': 'application/json'},
            json={'from': 'onboarding@resend.dev',
                  'to': ['justin.woller@everlywell.com'],
                  'subject': f'Phoenix Demo Login — {name}',
                  'html': (f'<p><b>Name:</b> {name}</p><p><b>Email:</b> {email}</p>'
                           f'<p><b>IP:</b> {ip}</p><p><b>Login #:</b> {login_num}</p>'
                           f'<p><b>Time:</b> {ts}</p>')},
            timeout=5)
    except Exception as e:
        logging.warning('Resend email failed: %s', e)

    logging.info('DEMO_ACCESS | %s | %s | login #%d | ip:%s', ts, email, login_num, ip)
    return ts, login_num

def _record_persona_switch(role, display_name):
    """Log which demo persona was accessed during a session."""
    gate_name  = session.get('gate_name', 'Unknown')
    gate_email = session.get('gate_email', 'unknown@everlywell.com')
    if not gate_email or gate_email == 'unknown@everlywell.com':
        return  # not a gated session, skip
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr or 'unknown').split(',')[0].strip()
    record = {
        'timestamp':     ts,
        'name':          gate_name,
        'email':         gate_email,
        'ip':            ip,
        'login_num':     0,
        'activity_type': f'persona: {display_name}',
    }
    # Write to Supabase
    if _SUPABASE_URL and _SUPABASE_KEY:
        try:
            sb_resp = requests.post(
                f'{_SUPABASE_URL}/rest/v1/access_log',
                json=record, headers=_sb_headers(), timeout=5
            )
            if not sb_resp.ok:
                logging.warning('Supabase persona write %s: %s', sb_resp.status_code, sb_resp.text)
            else:
                logging.info('Supabase persona write OK — %s → %s', gate_email, display_name)
        except Exception as e:
            logging.warning('Supabase persona log failed: %s', e)
    # Write to SQLite
    try:
        with sqlite3.connect(_DB_PATH) as conn:
            conn.execute(
                'INSERT INTO access_log (timestamp, name, email, ip, login_num) VALUES (?,?,?,?,?)',
                (ts, gate_name, gate_email, ip, 0)
            )
            conn.commit()
    except Exception:
        pass
    logging.info('PERSONA | %s | %s → %s', ts, gate_email, display_name)


# ── Page guide (Phoenix icon help modal) ──────────────────────────────────
@app.context_processor
def inject_page_guide():
    import json
    endpoint = request.endpoint or ''
    try:
        conn = sqlite3.connect(_DB_PATH)
        row = conn.execute(
            '''SELECT title, header_color, section_what, section_solves, section_key
               FROM page_guides WHERE page_key = ? AND is_active = 1''',
            [endpoint]
        ).fetchone()
        conn.close()
        if row:
            guide = {
                'title':        row[0],
                'header_color': row[1],
                'section_what':    json.loads(row[2]) if row[2] else [],
                'section_solves':  json.loads(row[3]) if row[3] else [],
                'section_key':     json.loads(row[4]) if row[4] else [],
            }
            return dict(page_guide=guide)
    except Exception:
        pass
    return dict(page_guide=None)


# ── Role-based sidebar nav (injected into every template) ──────────────────
@app.context_processor
def inject_sidebar_nav():
    from flask import request as _req
    role  = session.get('role', '')
    _path = _req.path

    # Admin and patient blueprints always suppress the global g-sidebar (they have their own)
    if _req.blueprint in ('admin', 'patient'):
        return dict(sidebar_nav=[], user_role=role)
    # care_team blueprint: suppress g-sidebar for any role that shouldn't see it there
    if _req.blueprint == 'care_team' and role not in ('care_team', 'care_team_gaps', 'provider_psr'):
        return dict(sidebar_nav=[], user_role=role)

    # Index page (login screen) — no sidebar
    if _req.endpoint == 'index':
        return dict(sidebar_nav=[], user_role=role, page_guide=None)

    ICONS = {
        'home':      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9,22 9,12 15,12 15,22"/></svg>',
        'clipboard': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/><path d="M9 12h6M9 16h4"/></svg>',
        'users':     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>',
        'calendar':  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
        'message':   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>',
        'bell':      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9M13.73 21a2 2 0 01-3.46 0"/></svg>',
        'settings':  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z"/></svg>',
        'check':     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/></svg>',
        'flask':     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6m-3 0v7l-4 8a1 1 0 00.9 1.5h8.2a1 1 0 00.9-1.5l-4-8V3"/></svg>',
        'clock':     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12,6 12,12 16,14"/></svg>',
        'pill':      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.5 20.5l10-10a4.95 4.95 0 00-7.07-7.07l-10 10a4.95 4.95 0 007.07 7.07z"/><line x1="8.5" y1="8.5" x2="15.5" y2="15.5"/></svg>',
        'chart-bar': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="12" width="4" height="9"/><rect x="10" y="7" width="4" height="14"/><rect x="17" y="3" width="4" height="18"/></svg>',
        'phone':     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81 19.79 19.79 0 01.22 1.18 2 2 0 012.18 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.91 7.09a16 16 0 006 6l.56-.56a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 14.92z"/></svg>',
        'link':      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg>',
        'document':  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14,2 14,8 20,8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10,9 9,9 8,9"/></svg>',
        'person-search': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="10" cy="7" r="4"/><path d="M2 21v-2a4 4 0 014-4h4"/><circle cx="17" cy="17" r="3"/><path d="M21 21l-1.5-1.5"/></svg>',
    }

    RAW = {
        'provider_md': [
            ('Dashboard',     '/provider/',              'home',      ['/provider/', '/provider/dashboard', '/provider/chart']),
            ('Patient Queue', '/provider/queue',          'users',     ['/provider/queue']),
            ('My Schedule',   '/provider/schedule',       'calendar',  ['/provider/schedule']),
            ('Prescriptions', '/provider/prescriptions',  'pill',      ['/provider/prescriptions']),
            ('Oversight',     '/provider/oversight',      'check',     ['/provider/oversight']),
            ('Lab Auth',      '/provider/lab-auth',       'flask',     ['/provider/lab-auth']),
            ('Messages',      '/provider/messages',       'message',   ['/provider/messages']),
            ('Alerts',        '/provider/notifications',  'bell',      ['/provider/notifications', '/provider/alerts']),
            ('Settings',      '/provider/settings',       'settings',  ['/provider/settings']),
        ],
        'provider_np': [
            ('Dashboard',     '/provider/np',            'home',      ['/provider/np']),
            ('Patient Queue', '/provider/queue',          'users',     ['/provider/queue']),
            ('My Schedule',   '/provider/schedule',       'calendar',  ['/provider/schedule']),
            ('Prescriptions', '/provider/prescriptions',  'pill',      ['/provider/prescriptions']),
            ('Messages',      '/provider/messages',       'message',   ['/provider/messages']),
            ('Alerts',        '/provider/notifications',  'bell',      ['/provider/notifications', '/provider/alerts']),
            ('Settings',      '/provider/settings',       'settings',  ['/provider/settings']),
        ],
        'provider_rn': [
            ('My Dashboard',    '/provider/rn',              'home',      ['/provider/rn']),
            ('RN Queue',        '/provider/rn/queue',         'clipboard', ['/provider/rn/queue']),
            ('Titer Queue',     '/provider/rn/titers',        'clipboard', ['/provider/rn/titers']),
            ('DXS Audit',       '/provider/rn/audit',         'clipboard', ['/provider/rn/audit']),
            ('Patient Queue',   '/provider/queue',            'users',     ['/provider/queue']),
            ('Patient Mgmt', '/provider/patient-management', 'person-search', ['/provider/patient-management', '/scheduler/search-patient']),
            ('My Schedule',     '/provider/staff-schedule',   'calendar',  ['/provider/staff-schedule']),
            ('On-Call Schedule','/provider/rn/oncall',        'calendar',  ['/provider/rn/oncall']),
            ('Timesheet',       '/provider/timesheet',        'clock',     ['/provider/timesheet']),
            ('Messages',        '/provider/messages',         'message',   ['/provider/messages']),
            ('Alerts',          '/provider/notifications',    'bell',      ['/provider/notifications', '/provider/alerts']),
            ('Settings',        '/provider/settings',         'settings',  ['/provider/settings']),
        ],
        'provider_ma': [
            ('My Dashboard',  '/provider/ma',              'home',      ['/provider/ma']),
            ('MA Queue',      '/provider/ma/queue',         'clipboard', ['/provider/ma/queue']),
            ('Titer Queue',   '/provider/rn/titers',        'clipboard', ['/provider/rn/titers']),
            ('On-Call Sched.','/provider/rn/oncall',        'calendar',  ['/provider/rn/oncall']),
            ('DXS Audit',     '/provider/rn/audit',         'clipboard', ['/provider/rn/audit']),
            ('PCP Follow-Up', '/provider/ma/followup',      'clipboard', ['/provider/ma/followup']),
            ('Referral Tracker', '/provider/ma/referrals', 'clipboard', ['/provider/ma/referrals']),
            ('Patient Queue', '/provider/queue',            'users',     ['/provider/queue']),
            ('Patient Mgmt', '/provider/patient-management', 'person-search', ['/provider/patient-management', '/scheduler/search-patient']),
            ('Network Schedule', '/provider/schedule',    'calendar',  ['/provider/schedule']),
            ('My Schedule',   '/provider/staff-schedule',  'calendar',  ['/provider/staff-schedule']),
            ('Timesheet',     '/provider/timesheet',        'clock',     ['/provider/timesheet']),
            ('Messages',      '/provider/messages',         'message',   ['/provider/messages']),
            ('Alerts',        '/provider/notifications',    'bell',      ['/provider/notifications', '/provider/alerts']),
            ('Settings',      '/provider/settings',         'settings',  ['/provider/settings']),
        ],
        'provider_gca': [
            ('My Dashboard',   '/provider/gca',              'home',      ['/provider/gca']),
            ('Consult Prep',   '/provider/gca/consult-prep', 'clipboard', ['/provider/gca/consult-prep']),
            ('Patient Mgmt', '/provider/patient-management', 'person-search', ['/provider/patient-management', '/scheduler/search-patient']),
            ('Blurb Library',  '/provider/blurbs',           'document',  ['/provider/blurbs']),
            ('Messages',       '/provider/messages',         'message',   ['/provider/messages']),
            ('Settings',       '/provider/settings',         'settings',  ['/provider/settings']),
        ],
        'provider_doh': [
            ('Dashboard',      '/provider/doh',              'home',      ['/provider/doh']),
            ('Report Queue',   '/provider/doh/queue',        'clipboard', ['/provider/doh/queue', '/provider/doh/report']),
            ('History',        '/provider/doh/history',      'clock',     ['/provider/doh/history']),
            ('Settings',       '/provider/settings',         'settings',  ['/provider/settings']),
        ],
        'provider_manager': [
            ('Dashboard',      '/provider/manager',              'home',        ['/provider/manager']),
            ('MA Queue',       '/provider/ma/queue',             'users',       ['/provider/ma/queue']),
            ('PCP Follow-Up',  '/provider/ma/followup',          'clipboard',   ['/provider/ma/followup']),
            ('Referral Tracker','/provider/ma/referrals',        'clipboard',   ['/provider/ma/referrals']),
            ('RN Queue',       '/provider/rn/queue',             'users',       ['/provider/rn/queue']),
            ('Titer Queue',    '/provider/rn/titers',            'clipboard',   ['/provider/rn/titers']),
            ('On-Call Sched.', '/provider/rn/oncall',            'calendar',    ['/provider/rn/oncall']),
            ('DXS Audit',      '/provider/rn/audit',             'clipboard',   ['/provider/rn/audit']),
            ('Patient Queue',   '/provider/queue',                'clipboard',   ['/provider/queue']),
            ('Patient Mgmt',   '/provider/patient-management',  'person-search',['/provider/patient-management', '/scheduler/search-patient']),
            ('Network Schedule','/provider/schedule',            'calendar',    ['/provider/schedule']),
            ('Timekeeping',    '/provider/manager/timekeeping',  'clock',       ['/provider/manager/timekeeping']),
            ('Team Schedule',  '/provider/staff-schedule',       'calendar',    ['/provider/staff-schedule']),
            ('Messages',       '/provider/messages',             'message',     ['/provider/messages']),
            ('Alerts',         '/provider/notifications',        'bell',        ['/provider/notifications']),
            ('Settings',       '/provider/settings',             'settings',    ['/provider/settings']),
        ],
        'provider_gc': [
            ('Dashboard',     '/provider/gc',            'home',      ['/provider/gc']),
            ('GC Queue',      '/provider/gc/queue',       'users',     ['/provider/gc/queue']),
            ('Patient Mgmt', '/provider/patient-management', 'person-search', ['/provider/patient-management', '/scheduler/search-patient']),
            ('My Schedule',   '/provider/schedule',      'calendar',  ['/provider/schedule']),
            ('Messages',      '/provider/messages',       'message',   ['/provider/messages']),
            ('Alerts',        '/provider/gc/notifications',  'bell',      ['/provider/gc/notifications']),
            ('Settings',      '/provider/settings',       'settings',  ['/provider/settings']),
        ],
        'care_team': [
            ('My Dashboard',  '/care-team/',             'home',      ['/care-team/']),
            ('CT Queue',      '/care-team/queue',        'clipboard', ['/care-team/queue']),
            ('Patient Queue', '/provider/queue',          'users',     ['/provider/queue']),
            ('Schedule',      '/provider/schedule',       'calendar',  ['/provider/schedule']),
            ('Messages',      '/provider/messages',       'message',   ['/provider/messages']),
            ('Settings',      '/provider/settings',       'settings',  ['/provider/settings']),
        ],
        'care_team_gaps': [
            ('Dashboard',     '/care-team/gaps',         'home',      ['/care-team/gaps']),
        ],
        'provider_psr': [
            ('Dashboard',      '/care-team/psr',                  'home',      ['/care-team/psr']),
            ('Call Queue',     '/care-team/psr/queue',            'phone',     ['/care-team/psr/queue']),
            ('Thyroid Program','/care-team/psr/thyroid-queue',    'clipboard', ['/care-team/psr/thyroid-queue']),
            ('GC Queue',       '/provider/gc/queue',              'users',     ['/provider/gc/queue']),
            ('Patient Queue',  '/provider/queue',                 'users',     ['/provider/queue']),
            ('Patient Mgmt',   '/provider/patient-management',    'clipboard', ['/provider/patient-management']),
            ('Network Schedule','/provider/schedule',             'calendar',  ['/provider/schedule']),
            ('Messages',       '/provider/messages',              'message',   ['/provider/messages']),
            ('Settings',       '/provider/settings',              'settings',  ['/provider/settings']),
        ],
        'scheduler': [
            ('Dashboard',     '/scheduler/',             'home',      ['/scheduler/']),
            ('Schedule',      '/scheduler/schedule',      'calendar',  ['/scheduler/schedule', '/provider/schedule']),
            ('Messages',      '/provider/messages',       'message',   ['/provider/messages']),
            ('Settings',      '/provider/settings',       'settings',  ['/provider/settings']),
        ],
    }

    raw_items = RAW.get(role, [])
    nav_items = []
    for label, href, icon_key, active_paths in raw_items:
        is_active = any(_path == p or _path.startswith(p + '/') or _path.startswith(p + '?') for p in active_paths)
        # special case: /provider/rn is only active for rn_dashboard, not /provider/rn/queue
        if href == '/provider/rn' and _path.startswith('/provider/rn/'):
            is_active = False
        if href == '/provider/ma' and _path.startswith('/provider/ma/'):
            is_active = False
        nav_items.append({'label': label, 'href': href, 'icon': ICONS[icon_key], 'active': is_active})

    return dict(sidebar_nav=nav_items, user_role=role)

@app.before_request
def enforce_demo_gate():
    if not DEMO_GATE:
        return
    if request.endpoint in GATE_BYPASS_ROUTES:
        return
    # Check inactivity timeout — expire gate_verified after 15 min of no activity
    if session.get('gate_verified'):
        last = session.get('gate_last_activity', 0)
        if time.time() - last > GATE_TIMEOUT_SECONDS:
            # Session timed out — clear gate flags but keep name/email for pre-fill
            _prev_name  = session.get('gate_name', '')
            _prev_email = session.get('gate_email', '')
            session.clear()
            session['gate_prefill_name']  = _prev_name
            session['gate_prefill_email'] = _prev_email
            return redirect(url_for('gate_login', next=request.url, timeout='1'))
        # Refresh activity timestamp on every request
        session['gate_last_activity'] = time.time()
        return
    return redirect(url_for('gate_login', next=request.url))

@app.route('/demo-access', methods=['GET'])
def gate_login():
    timeout = request.args.get('timeout', '')
    # Pre-fill from previous session if they timed out
    prefill_name  = session.pop('gate_prefill_name',  '')
    prefill_email = session.pop('gate_prefill_email', '')
    return render_template('gate_login.html',
        error   = 'Your session expired after 15 minutes of inactivity. Please sign in again.' if timeout else '',
        timeout = bool(timeout),
        name    = prefill_name,
        email   = prefill_email,
        next    = request.args.get('next', ''))

@app.route('/demo-access', methods=['POST'])
def gate_login_post():
    name     = request.form.get('name', '').strip()
    email    = request.form.get('email', '').strip().lower()
    next_url = request.form.get('next', '').strip()
    error = ''
    if not name:
        error = 'Please enter your name.'
    elif not email.endswith('@everlywell.com'):
        error = 'Please use your @everlywell.com email address.'
    if error:
        return render_template('gate_login.html', error=error, name=name, email=email, next=next_url)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr or 'unknown').split(',')[0].strip()
    ts, login_num = _record_gate_access(name, email, ip)
    session.permanent = True
    session['gate_verified']      = True
    session['gate_name']          = name
    session['gate_email']         = email
    session['gate_timestamp']     = ts
    session['gate_login_num']     = login_num
    session['gate_last_activity'] = time.time()
    return redirect(next_url or url_for('index'))

@app.route('/demo-access/log')
def gate_access_log():
    """Access log dashboard — usage stats + full login history (SQLite-backed)."""
    # Try Supabase first (permanent history), fall back to SQLite (session cache)
    rows = []
    if _SUPABASE_URL and _SUPABASE_KEY:
        try:
            resp = requests.get(
                f'{_SUPABASE_URL}/rest/v1/access_log',
                params={'select': '*', 'order': 'id.asc'},
                headers={
                    'apikey':        _SUPABASE_KEY,
                    'Authorization': f'Bearer {_SUPABASE_KEY}',
                },
                timeout=10
            )
            if resp.ok:
                rows = resp.json()
                logging.info('Dashboard: loaded %d rows from Supabase', len(rows))
        except Exception as e:
            logging.warning('Supabase read failed, falling back to SQLite: %s', e)

    if not rows:
        try:
            with sqlite3.connect(_DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute('SELECT * FROM access_log ORDER BY id ASC')
                rows = [dict(r) for r in cur.fetchall()]
                logging.info('Dashboard: loaded %d rows from SQLite fallback', len(rows))
        except Exception as e:
            logging.error('SQLite read also failed: %s', e)
            rows = []

    # Build per-user summary in Python (iterate oldest→newest)
    user_map = {}
    for r in reversed(rows):
        e = r['email']
        if e not in user_map:
            user_map[e] = {
                'email':          e,
                'name':           r['name'],
                'total_sessions': 0,
                'first_seen':     r['timestamp'],
                'last_seen':      r['timestamp'],
            }
        user_map[e]['total_sessions'] += 1
        user_map[e]['last_seen'] = r['timestamp']

    user_rows    = sorted(user_map.values(), key=lambda x: (-x['total_sessions'], x['last_seen']))
    total_logins = len(rows)
    unique_users = len(user_rows)
    most_active  = user_rows[0] if user_rows else None
    last_login   = rows[0]['timestamp'] if rows else '—'

    return render_template('gate_access_log.html',
        entries      = rows,
        users        = user_rows,
        total_logins = total_logins,
        unique_users = unique_users,
        most_active  = most_active,
        last_login   = last_login,
    )
# ──────────────────────────────────────────────────────────────────────────

ROLE_NAMES = {
    'provider_md':      'Dr. Sarah Lee, MD',
    'provider_np':      'Maria Rodriguez, NP',
    'provider_rn':      'Jennifer Martinez, Lead RN',
    'provider_ma':      'Michael Torres, MA',
    'provider_gc':      'Lisa Park, MS CGC',
    'provider_gca':     'Priya Sharma, GCA',
    'provider_doh':     'Crystal Veliz, DOH Coordinator',
    'scheduler':        'David Nguyen',
    'care_team':        'Alex Kim',
    'patient':          'Marcus Johnson',
    'admin':            'Chris Navarro',
    'qa_reviewer':      'Quinn Patel, QA Reviewer',
    'gc_admin':         'Morgan Ellis, GC Admin',
    'provider_manager': 'Riley Perrone, Team Manager',
    'provider_psr':     'Melanie Marmo, PSS Manager',
    'care_team_gaps':   'Missy Lemieux',
}

ROLE_DESTINATIONS = {
    'provider_md':      'provider.dashboard',
    'provider_np':      'provider.np_dashboard',
    'provider_rn':      'provider.rn_dashboard',
    'provider_ma':      'provider.ma_dashboard',
    'provider_gc':      'provider.gc_dashboard',
    'provider_gca':     'provider.gca_dashboard',
    'provider_doh':     'provider.doh_dashboard',
    'scheduler':        'scheduler.dashboard',
    'care_team':        'care_team.dashboard',
    'admin':            'admin.dashboard',
    'qa_reviewer':      'provider.qa_reviewer_dashboard',
    'gc_admin':         'provider.gc_admin_dashboard',
    'patient':          'patient.dashboard',
    'provider_manager': 'provider.manager_dashboard',
    'provider_psr':     'care_team.psr_dashboard',
    'care_team_gaps':   'care_team.gaps_dashboard',
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login/<role>")
def login(role):
    if role not in ROLE_DESTINATIONS:
        return redirect(url_for('index'))
    display = ROLE_NAMES.get(role, role)
    session.permanent = True
    session['role'] = role
    session['display_name'] = display
    _record_persona_switch(role, display)
    return redirect(url_for(ROLE_DESTINATIONS[role]))

@app.route("/login", methods=["POST"])
def login_post():
    role = request.form.get("role", "")
    if role not in ROLE_DESTINATIONS:
        return redirect(url_for('index'))
    display = ROLE_NAMES.get(role, role)
    session.permanent = True
    session['role'] = role
    session['display_name'] = display
    _record_persona_switch(role, display)
    return redirect(url_for(ROLE_DESTINATIONS[role]))

@app.route("/switch-user", methods=["POST"])
def switch_user():
    role = request.form.get("role", "")
    if role in ROLE_DESTINATIONS:
        display = ROLE_NAMES.get(role, role)
        gate_name  = session.get('gate_name')
        gate_email = session.get('gate_email')
        gate_ts    = session.get('gate_timestamp')
        gate_num   = session.get('gate_login_num')
        session.clear()
        session.permanent = True
        session['role']             = role
        session['display_name']     = display
        session['gate_name']        = gate_name
        session['gate_email']       = gate_email
        session['gate_timestamp']   = gate_ts
        session['gate_login_num']   = gate_num
        session['gate_verified']    = True
        session['gate_last_activity'] = time.time()
        _record_persona_switch(role, display)
        return redirect(url_for(ROLE_DESTINATIONS[role]))
    return redirect(url_for('index'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

# Change 1 — PWN Health isolated patient portal
@app.route('/pwn/login')
def pwn_login():
    return render_template('patient/login_pwn.html')

@app.route('/pwn/portal')
def pwn_portal():
    return render_template('patient/portal_pwn.html')

# Change 2 — Everlywell multi-program patient portal
@app.route('/patient/login')
def patient_login_page():
    return render_template('patient/login.html')

@app.route('/patient/portal')
def patient_portal_page():
    return render_template('patient/portal.html')

# M02 — Provider Portal (includes async consultation workflow)
app.register_blueprint(provider.bp, url_prefix="/provider")

# M03 — Patient Portal
app.register_blueprint(patient.bp, url_prefix="/patient")

# M04 — Admin Portal
app.register_blueprint(admin.bp, url_prefix="/admin")

# Care Team Portal
app.register_blueprint(care_team.bp, url_prefix="/care-team")

# Scheduler
app.register_blueprint(scheduler.bp, url_prefix="/scheduler")

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
