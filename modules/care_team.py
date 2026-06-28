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

@bp.route("/gaps")
def gaps_dashboard():
    return render_template("care_team/gaps_under_construction.html")
