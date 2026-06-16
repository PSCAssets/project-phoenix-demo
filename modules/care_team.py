from flask import Blueprint, render_template

bp = Blueprint("care_team", __name__)

@bp.route("/")
def dashboard():
    return render_template("care_team/dashboard.html")
