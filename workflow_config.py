STAGE_CATALOG = {
    'SYS-01': {
        'id': 'SYS-01', 'name': 'Intake received', 'type': 'system', 'role': 'System',
        'queue': None, 'default_sla_hours': None,
        'trigger': 'Patient submits consult intake form', 'is_conditional': False,
    },
    'SYS-03': {
        'id': 'SYS-03', 'name': 'Awaiting lab results', 'type': 'system_wait', 'role': 'System (wait)',
        'queue': None, 'default_sla_hours': None,
        'trigger': 'Lab results received via integration upload', 'is_conditional': True,
        'condition': 'Blocking wait — chart paused and removed from all queues. SLA clock paused. Resumes automatically when lab results are received.',
    },
    'SYS-06': {
        'id': 'SYS-06', 'name': 'Results released', 'type': 'system', 'role': 'System',
        'queue': None, 'default_sla_hours': None,
        'trigger': 'Results released to patient portal (CURES Act 21-day default unless held by provider)',
        'is_conditional': False,
    },
    'SYS-07': {
        'id': 'SYS-07', 'name': 'Consult closed', 'type': 'system', 'role': 'System',
        'queue': None, 'default_sla_hours': None,
        'trigger': 'All required fields signed and closed', 'is_conditional': False,
    },
    'HUM-01': {
        'id': 'HUM-01', 'name': 'Intake review', 'type': 'human', 'role': 'MA',
        'queue': 'ma_queue', 'default_sla_hours': 4,
        'trigger': 'MA marks intake complete and confirms patient eligibility', 'is_conditional': False,
    },
    'HUM-02': {
        'id': 'HUM-02', 'name': 'Clinical review', 'type': 'human', 'role': 'MD / NP',
        'queue': 'provider_queue', 'default_sla_hours': 24,
        'trigger': 'Provider reviews chart and begins clinical response', 'is_conditional': False,
    },
    'HUM-03': {
        'id': 'HUM-03', 'name': 'Lab review', 'type': 'human', 'role': 'MD / NP',
        'queue': 'provider_queue', 'default_sla_hours': 24,
        'trigger': 'Provider reviews and annotates lab results', 'is_conditional': True,
        'condition': 'Triggered when lab results required but not yet reviewed by provider',
    },
    'HUM-03b': {
        'id': 'HUM-03b', 'name': 'Lab ordered', 'type': 'human', 'role': 'MD / NP',
        'queue': 'provider_queue', 'default_sla_hours': 24,
        'trigger': 'Provider creates lab requisition', 'is_conditional': False,
    },
    'HUM-04': {
        'id': 'HUM-04', 'name': 'Treatment plan', 'type': 'human', 'role': 'MD / NP',
        'queue': 'provider_queue', 'default_sla_hours': 24,
        'trigger': 'SOAP note drafted with Rx or clinical recommendation', 'is_conditional': False,
    },
    'HUM-04gc': {
        'id': 'HUM-04gc', 'name': 'Counseling plan', 'type': 'human', 'role': 'GC',
        'queue': 'provider_queue', 'default_sla_hours': 24,
        'trigger': 'Counseling summary and recommendations finalized', 'is_conditional': False,
    },
    'HUM-05': {
        'id': 'HUM-05', 'name': 'Chart close', 'type': 'human', 'role': 'MD / NP',
        'queue': 'provider_queue', 'default_sla_hours': 4,
        'trigger': 'Provider signs SOAP note', 'is_conditional': False,
    },
    'HUM-05gc': {
        'id': 'HUM-05gc', 'name': 'Chart close (GC)', 'type': 'human', 'role': 'GC',
        'queue': 'provider_queue', 'default_sla_hours': 4,
        'trigger': 'GC signs and closes chart', 'is_conditional': False,
    },
    'HUM-07': {
        'id': 'HUM-07', 'name': 'QA review', 'type': 'human', 'role': 'GC / Supervisor',
        'queue': 'provider_queue', 'default_sla_hours': 24,
        'trigger': 'Second reviewer approves clinical content before chart close', 'is_conditional': False,
    },
    'HUM-08': {
        'id': 'HUM-08', 'name': 'Pre-visit prep', 'type': 'human', 'role': 'MA',
        'queue': 'ma_queue', 'default_sla_hours': 2,
        'trigger': 'Chart prepped and patient confirmed for upcoming visit', 'is_conditional': False,
    },
    'HUM-09': {
        'id': 'HUM-09', 'name': 'Consult in progress', 'type': 'human', 'role': 'MD / NP',
        'queue': 'provider_queue', 'default_sla_hours': None,
        'trigger': 'Call or video session completed and documented', 'is_conditional': False,
    },
    'HUM-11': {
        'id': 'HUM-11', 'name': 'Results review', 'type': 'human', 'role': 'MD / NP',
        'queue': 'provider_queue', 'default_sla_hours': 48,
        'trigger': 'Provider reviews and annotates results in chart', 'is_conditional': False,
    },
    'HUM-12': {
        'id': 'HUM-12', 'name': 'Appointment booked', 'type': 'human', 'role': 'Scheduler',
        'queue': 'scheduler_queue', 'default_sla_hours': 48,
        'trigger': 'Appointment confirmed on calendar by scheduler', 'is_conditional': False,
    },
}

WORKFLOW_TEMPLATES = {
    'standard_async_v2': {
        'name': 'Standard async workflow v2',
        'applicable': 'Weight management, testosterone care, skincare, ED, thyroid — most async products',
        'description': 'Patient submits intake → MA intake review → provider clinical review → optional lab review → treatment plan → chart close.',
        'consult_types': ['async'],
        'stages': ['SYS-01', 'HUM-01', 'HUM-02', 'HUM-03', 'HUM-04', 'HUM-05'],
        'scale': 'This async template supports unlimited concurrent consults — providers see only their assigned charts, queued by SLA urgency. The conditional lab review stage automatically pauses and resumes the SLA clock without manual intervention.',
    },
    'standard_phone_video': {
        'name': 'Standard phone / video',
        'applicable': 'Weight management (phone/video), testosterone (phone), A1C treat, ED (video)',
        'description': 'Scheduler books appointment → MA preps chart → provider conducts live consult → SOAP note → chart close.',
        'consult_types': ['phone', 'video'],
        'stages': ['HUM-12', 'HUM-08', 'HUM-09', 'HUM-04', 'HUM-05'],
        'scale': 'Appointment-based workflows are coordinated through the scheduler queue, then flow into the provider queue after the visit. SLA tracking begins at appointment booking and pauses during the live session.',
    },
    'lab_required_async': {
        'name': 'Lab-required async',
        'applicable': 'BRCA counseling, hereditary cancer panel, carrier screening, STI treatment',
        'description': 'Patient submits → MA review → provider orders lab → system wait for results → results review → results released → chart close.',
        'consult_types': ['async'],
        'stages': ['SYS-01', 'HUM-01', 'HUM-03b', 'SYS-03', 'HUM-11', 'SYS-06', 'HUM-05'],
        'scale': 'The blocking wait stage (SYS-03) removes the chart from all queues and pauses SLA. This prevents provider burnout from charts that cannot progress. The chart auto-reappears in the queue when lab results are received via integration.',
    },
    'genetic_counseling_specialty': {
        'name': 'Genetic counseling / specialty',
        'applicable': 'BRCA counseling with GC, carrier screening with counseling, rare disease specialty',
        'description': 'Patient submits → MA intake review → GC clinical review → QA approval (two-eye check) → counseling plan → chart close.',
        'consult_types': ['async'],
        'stages': ['SYS-01', 'HUM-01', 'HUM-02', 'HUM-07', 'HUM-04gc', 'HUM-05gc'],
        'scale': 'Genetic counseling workflows require a two-eye QA check before plan delivery. The QA stage routes to a GC supervisor queue, ensuring all genetic findings are reviewed by a second licensed counselor before patient disclosure.',
    },
}


def get_template_stages(template_key):
    tpl = WORKFLOW_TEMPLATES.get(template_key)
    if not tpl:
        return []
    return [STAGE_CATALOG[s] for s in tpl['stages'] if s in STAGE_CATALOG]


DEMO_CONSULT_WORKFLOW = {
    'consult_id': 'CST-2026-10849',
    'patient_name': 'Marcus Johnson',
    'care_product': 'Testosterone Care',
    'template': 'standard_async_v2',
    'current_stage_index': 1,
    'stages_completed': ['SYS-01'],
    'current_stage': 'HUM-01',
}
