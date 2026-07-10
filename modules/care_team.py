from flask import Blueprint, render_template

bp = Blueprint("care_team", __name__)

@bp.route("/")
def dashboard():
    return render_template("care_team/dashboard.html")

@bp.route("/psr")
def psr_dashboard():
    return render_template("care_team/psr_dashboard.html")

@bp.route("/psr/queue")
def psr_queue():
    return render_template("care_team/psr_queue.html")

@bp.route("/psr/link-generator")
def psr_link_generator():
    return render_template("care_team/psr_dashboard.html")

@bp.route("/psr/thyroid-queue")
def psr_thyroid_queue():
    return render_template("care_team/thyroid_queue.html")

@bp.route("/psr/dxs-queue")
def psr_dxs_queue():
    return render_template("care_team/dxs_queue.html")

@bp.route("/psr/dxs-call/<consult_id>")
def psr_dxs_call(consult_id):
    return render_template("care_team/dxs_call.html")

@bp.route("/queue")
def queue():
    return render_template("care_team/queue.html")

@bp.route("/gaps")
def gaps_dashboard():
    return render_template("care_team/gaps_under_construction.html")
