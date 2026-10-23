
import os
from functools import wraps
from datetime import datetime, timezone

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, jsonify
)
from firebase_admin import auth, db
from firebase_config import verify_firebase_token

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

if not app.secret_key:
    raise RuntimeError(
        "Set SECRET_KEY in your terminal before running the application."
    )

STATUSES = ["Pending", "In Progress", "Completed"]
WASTE_TYPES = [
    "Household", "Plastic", "Construction",
    "Electronic", "Garden", "Other"
]


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            if request.path.startswith("/api/"):
                return jsonify({"error": "Please log in."}), 401
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


@app.route("/")
def home():
    return redirect(url_for("register"))

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/session", methods=["POST"])
def create_session():
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return jsonify({"error": "Missing Firebase ID token."}), 401

    try:
        decoded = verify_firebase_token(header.split(" ", 1)[1])
        user = auth.get_user(decoded["uid"])

        session.clear()
        session["user_id"] = user.uid
        session["user_name"] = user.display_name or user.email or "User"

        return jsonify({"success": True}), 200

    except Exception:
        app.logger.exception("Firebase authentication failed")
        return jsonify({"error": "Authentication failed. Please log in again."}), 401


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("You have logged out.", "success")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def index():
    reports_data = db.reference("wasteReports").get() or {}
    reports = []

    for report_id, report in reports_data.items():
        if not isinstance(report, dict):
            continue

        report = dict(report)
        report["id"] = report_id
        reports.append(report)

    reports.sort(
        key=lambda report: report.get("createdAt", ""),
        reverse=True
    )

    counts = {
        "total": len(reports),
        "pending": sum(r.get("status") == "Pending" for r in reports),
        "progress": sum(r.get("status") == "In Progress" for r in reports),
        "completed": sum(r.get("status") == "Completed" for r in reports),
    }

    return render_template(
        "index.html",
        reports=reports,
        counts=counts,
        user_name=session.get("user_name")
    )


@app.route("/report", methods=["POST"])
@login_required
def create_report():
    location = request.form.get("location", "").strip()
    waste_type = request.form.get("waste_type", "").strip()
    description = request.form.get("description", "").strip()

    if not location or not description or waste_type not in WASTE_TYPES:
        flash("Please complete all fields correctly.", "error")
        return redirect(url_for("index"))

    report = {
        "userId": session["user_id"],
        "reporter": session["user_name"],
        "location": location,
        "wasteType": waste_type,
        "description": description,
        "status": "Pending",
        "createdAt": datetime.now(timezone.utc).isoformat()
    }

    db.reference("wasteReports").push(report)
    flash("Waste report saved to Firebase.", "success")
    return redirect(url_for("index"))


@app.route("/report/<report_id>/status", methods=["POST"])
@login_required
def update_status(report_id):
    status = request.form.get("status", "")
    report_ref = db.reference(f"wasteReports/{report_id}")
    report = report_ref.get()

    if not report:
        flash("Report not found.", "error")
    elif status not in STATUSES:
        flash("Invalid status.", "error")
    elif report.get("userId") != session["user_id"]:
        flash("You can only update your own reports.", "error")
    else:
        report_ref.update({"status": status})
        flash("Report status updated in Firebase.", "success")

    return redirect(url_for("index"))


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.environ.get("PORT", "5000")),
        debug=False
    )
