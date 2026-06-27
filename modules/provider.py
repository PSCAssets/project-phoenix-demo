from flask import Blueprint, render_template, session, request
from workflow_config import DEMO_CONSULT_WORKFLOW, STAGE_CATALOG, WORKFLOW_TEMPLATES

bp = Blueprint("provider", __name__)

CONSULT_TYPE_LABELS = {'phone': 'Phone', 'video': 'Video', 'async': 'Async', 'lab': 'Lab'}


def _build_chart_context(type_param, product_param='a1c'):
    consult_type_label = CONSULT_TYPE_LABELS.get(type_param, 'Async')
    wf = DEMO_CONSULT_WORKFLOW
    tpl = WORKFLOW_TEMPLATES.get(wf['template'], {})
    workflow_stages = [STAGE_CATALOG[s] for s in tpl.get('stages', []) if s in STAGE_CATALOG]
    if product_param == 'awv':
        consult = {
            'care_product': 'Annual Wellness Visit',
            'patient_name': 'D.R.',
            'patient_age': 68,
            'consult_id': 'C-20260601-022',
            'client': 'Elevance',
        }
    else:
        consult = {
            'care_product': 'A1C Management',
            'patient_name': 'M.G.',
            'patient_age': 63,
            'consult_id': 'C-20260528-010',
            'client': 'Humana',
        }
    return dict(
        consult_type=consult_type_label,
        consult_type_label=consult_type_label,
        workflow_state=wf,
        workflow_stages=workflow_stages,
        consult=consult,
    )



@bp.route("/home")
def provider_home():
    """Role-aware dashboard redirect — fixes nav persistence across all provider pages."""
    from flask import redirect
    role = session.get('role', 'provider_md')
    dest_map = {
        'provider_np': '/provider/np',
        'provider_rn': '/provider/rn',
        'provider_gc': '/provider/gc',
        'provider_ma': '/provider/ma',
    }
    return redirect(dest_map.get(role, '/provider/'))


@bp.route("/")
def dashboard():
    return render_template("provider/dashboard.html")

@bp.route("/queue")
def queue():
    role = session.get('role', 'provider_md')
    show_own_only = role in ('provider_md', 'provider_np')
    provider_name = {
        'provider_md': 'Dr. S. Lee',
        'provider_np': 'Jamie Rivera',
    }.get(role, '')
    return render_template("provider/queue.html", show_own_only=show_own_only, provider_name=provider_name)

@bp.route("/chart/<int:patient_id>")
def chart(patient_id):
    type_param = request.args.get('type', 'async')
    view_only = request.args.get('view_only') == '1'
    product_param = request.args.get('product', 'a1c')
    ctx = _build_chart_context(type_param, product_param)
    return render_template("provider/chart.html", patient_id=patient_id, view_only=view_only, **ctx)

@bp.route("/chart")
def chart_default():
    type_param = request.args.get('type', 'async')
    view_only = request.args.get('view_only') == '1'
    product_param = request.args.get('product', 'a1c')
    ctx = _build_chart_context(type_param, product_param)
    return render_template("provider/chart.html", patient_id=1, view_only=view_only, **ctx)

@bp.route("/consultation")
def consultation_workflow():
    return render_template("provider/consultation_workflow.html")

@bp.route("/consultation/<int:consult_id>")
def consultation_review(consult_id):
    return render_template("provider/consultation_review.html", consult_id=consult_id)

@bp.route("/rn")
def rn_dashboard():
    return render_template("provider/rn_dashboard.html")

@bp.route("/rn/queue")
def rn_queue():
    return render_template("provider/rn_queue.html")

@bp.route("/ma")
def ma_dashboard():
    return render_template("provider/ma_dashboard.html")

@bp.route("/ma/queue")
def ma_queue():
    return render_template("provider/ma_queue.html")

@bp.route("/np")
def np_dashboard():
    return render_template("provider/np_dashboard.html")

@bp.route("/gc")
def gc_dashboard():
    return render_template("provider/gc_dashboard.html")

@bp.route("/schedule")
def schedule():
    return render_template("provider/schedule.html")

@bp.route("/messages")
def messages():
    return render_template("provider/messages.html")

@bp.route("/alerts")
def alerts():
    return render_template("provider/alerts.html")

@bp.route("/settings")
def settings():
    role = session.get('role', 'provider_md')
    role_labels = {
        'provider_md': 'Physician (MD)',
        'provider_np': 'Nurse Practitioner (NP)',
        'provider_rn': 'Registered Nurse (RN)',
        'provider_gc': 'Genetic Counselor (GC)',
        'provider_ma': 'Medical Assistant (MA)',
        'provider_do': 'Physician (DO)',
        'scheduler': 'Scheduler',
        'gc_admin': 'GC Admin',
        'qa_reviewer': 'QA Reviewer',
    }
    return render_template("provider/settings.html", role_label=role_labels.get(role, 'Provider'))

@bp.route("/lab-orders")
def lab_orders():
    return render_template("provider/lab_orders.html")

@bp.route("/oversight")
def oversight():
    return render_template("provider/oversight.html")

@bp.route("/lab-auth")
def lab_auth():
    return render_template("provider/lab_auth.html")

@bp.route("/future-visits")
def future_visits():
    return render_template("provider/future_visits.html")

@bp.route("/chart/<int:patient_id>/async")
def chart_async(patient_id):
    return render_template("provider/chart_async.html", patient_id=patient_id)

@bp.route("/chart/<int:patient_id>/phone")
def chart_phone(patient_id):
    return render_template("provider/chart_phone.html", patient_id=patient_id)

@bp.route("/chart/<int:patient_id>/video")
def chart_video(patient_id):
    return render_template("provider/chart_video.html", patient_id=patient_id)

@bp.route("/new-patient")
def new_patient():
    return render_template("provider/new_patient.html")

@bp.route("/notifications")
def notifications():
    return render_template("provider/notifications.html")

@bp.route("/pharmacy")
def pharmacy():
    return render_template("provider/pharmacy.html")

@bp.route("/billing")
def billing():
    return render_template("provider/billing.html")


@bp.route("/qa-reviewer")
def qa_reviewer_dashboard():
    return render_template("provider/qa_reviewer_dashboard.html")

@bp.route("/gc-admin")
def gc_admin_dashboard():
    return render_template("provider/gc_admin_dashboard.html")

@bp.route("/prescriptions")
def prescriptions():
    return render_template("provider/prescriptions.html")

@bp.route("/timesheet")
def timesheet():
    return render_template("provider/timesheet.html")

@bp.route("/manager")
def manager_dashboard():
    return render_template("provider/manager_dashboard.html")

@bp.route("/manager/timekeeping")
def manager_timekeeping():
    return render_template("provider/manager_timekeeping.html")

@bp.route("/ma/followup")
def ma_followup():
    return render_template("provider/ma_followup.html")

@bp.route("/staff-schedule")
def staff_schedule():
    return render_template("provider/staff_schedule.html")

@bp.route("/gca")
def gca_dashboard():
    return render_template("provider/gca_dashboard.html")

@bp.route("/gca/consult-prep")
def gca_consult_prep_queue():
    return render_template("provider/gca_consult_prep.html")
