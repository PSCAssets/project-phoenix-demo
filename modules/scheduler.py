from flask import Blueprint, render_template

bp = Blueprint("scheduler", __name__)

@bp.route("/")
def dashboard():
    return render_template("provider/scheduler.html")

@bp.route("/schedule")
def schedule():
    return render_template("scheduler/schedule.html")

@bp.route("/search-patient")
def search_patient():
    return render_template("scheduler/search_patient.html")
