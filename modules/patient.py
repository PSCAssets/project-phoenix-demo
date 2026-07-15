from flask import Blueprint, render_template, request

bp = Blueprint("patient", __name__)

@bp.route("/")
def dashboard():
    return render_template("patient/dashboard.html")

@bp.route("/enroll")
def enroll():
    return render_template("patient/enroll.html")

@bp.route("/care-plan")
def care_plan():
    return render_template("patient/care_plan.html")

@bp.route("/health-profile")
def health_profile():
    return render_template("patient/health_profile.html")

@bp.route("/messages")
def messages():
    return render_template("patient/messages.html")

@bp.route("/async-consult")
def async_consult():
    return render_template("patient/async_consult.html")

@bp.route("/video-consult")
def video_consult():
    return render_template("patient/video_consult.html")

@bp.route("/consultations")
def consultations():
    return render_template("patient/consultations.html")

@bp.route("/consultation/<int:consult_id>")
def consultation_detail(consult_id):
    return render_template("patient/consultation_stub.html", consult_id=consult_id)

@bp.route("/appointments")
def appointments():
    return render_template("patient/appointments.html")

@bp.route("/labs")
def labs():
    return render_template("patient/labs.html")

@bp.route("/documents")
def documents():
    return render_template("patient/documents.html")

@bp.route("/settings")
def settings():
    return render_template("patient/settings.html")

@bp.route("/labs/detail")
def lab_detail():
    lab = request.args.get('lab', 'testosterone')
    return render_template("patient/lab_detail.html", lab=lab)

@bp.route("/dashboard")
def dashboard_alias():
    return render_template("patient/dashboard.html")
