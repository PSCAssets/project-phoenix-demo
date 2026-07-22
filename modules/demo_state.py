"""
Lightweight in-memory demo state for cross-portal live demo interactions.

This is intentionally NOT session-scoped: the whole point is that an action taken
in the Provider Portal (one browser tab / role) is visible in the Patient Portal
(a different tab / role) without a real backend or websocket layer. A single-process
module-level dict is sufficient for a demo app.

Currently used for: M08-NOT-011 / M08-NOTIFY-003 pre-call patient notification —
when a provider notifies the patient that a phone consult is starting in ~5 minutes,
the Everlywell Patient Portal (/patient/portal) reflects it live.
"""
import time

_NOTIFY_EXPIRY_SECONDS = 900  # 15 min safety auto-expiry so a stale demo flag doesn't linger

_state = {
    'phone_notify_active': False,
    'notify_time': None,
    'patient_name': 'Marcus Johnson',
    'provider_name': 'Dr. Sarah Lee',
}


def set_phone_notify():
    _state['phone_notify_active'] = True
    _state['notify_time'] = time.time()


def clear_phone_notify():
    _state['phone_notify_active'] = False
    _state['notify_time'] = None


def get_phone_notify():
    if _state['phone_notify_active'] and _state['notify_time']:
        if time.time() - _state['notify_time'] > _NOTIFY_EXPIRY_SECONDS:
            clear_phone_notify()
    return dict(_state)
