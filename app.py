"""Main Flask application for the classroom demonstration."""
import csv
import io
import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for, Response
import database
from database import get_connection, initialize_database, load_sample_data
from validators import INDUSTRIES, validate_alumni, validate_student, validate_message
from profiles import create_student, create_alumni
from search import search_alumni
from matching import suggest_mentors
from mentoring_requests import create_request, update_request_status, list_requests
from reports import participation_report, report_csv

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "classroom-demo-key-change-me")
database.DATABASE_PATH = os.environ.get("DATABASE_PATH", str(database.DATABASE_PATH))
initialize_database()
load_sample_data()


@app.context_processor
def shared_template_data():
    connection = get_connection()
    students = connection.execute("SELECT id, name FROM students ORDER BY name").fetchall()
    alumni = connection.execute("SELECT id, name FROM alumni WHERE consent=1 ORDER BY name").fetchall()
    connection.close()
    return {"students": students, "alumni_choices": alumni, "current_role": session.get("role", "Student")}


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        role = request.form.get("role", "Student")
        if role not in ("Student", "Alumni", "Coordinator"):
            flash("Choose a valid demonstration role.")
            return redirect(url_for("home"))
        try:
            student_id = int(request.form.get("student_id", 1))
            alumni_id = int(request.form.get("alumni_id", 1))
        except ValueError:
            flash("Choose valid profile IDs.")
            return redirect(url_for("home"))
        connection = get_connection()
        student = connection.execute("SELECT id FROM students WHERE id=?", (student_id,)).fetchone()
        alumnus = connection.execute("SELECT id FROM alumni WHERE id=? AND consent=1", (alumni_id,)).fetchone()
        connection.close()
        if not student or not alumnus:
            flash("Choose an existing student and a consenting alumni profile.")
            return redirect(url_for("home"))
        session["role"] = role
        session["student_id"] = student_id
        session["alumni_id"] = alumni_id
        flash("Demonstration role and profile selected.")
        return redirect(url_for("home"))
    return render_template("home.html")


@app.route("/student", methods=["GET", "POST"])
def student_profile():
    if request.method == "POST":
        fields = [request.form.get(key, "") for key in ("name", "department", "interests", "target_industry")]
        valid, message = validate_student(*fields)
        if valid:
            session["student_id"] = create_student(*fields)
            flash("Student profile saved.")
            return redirect(url_for("home"))
        flash(message)
    return render_template("student.html")


@app.route("/alumni/register", methods=["GET", "POST"])
def alumni_register():
    if request.method == "POST":
        values = [request.form.get(key, "") for key in ("name", "graduation_year", "industry", "role", "expertise")]
        consent = request.form.get("consent") == "yes"
        valid, message = validate_alumni(*values)
        if valid:
            session["alumni_id"] = create_alumni(*values, consent)
            flash("Alumni profile saved.")
            return redirect(url_for("directory"))
        flash(message)
    return render_template("alumni_form.html", industries=INDUSTRIES)


@app.route("/alumni/<int:alumni_id>/consent", methods=["POST"])
def withdraw_consent(alumni_id):
    connection = get_connection()
    connection.execute("UPDATE alumni SET consent=0, consent_date=NULL WHERE id=?", (alumni_id,))
    connection.commit()
    changed = connection.total_changes
    connection.close()
    flash("Consent withdrawn; this profile is hidden." if changed else "Alumni profile was not found.")
    return redirect(url_for("directory"))


@app.route("/directory")
def directory():
    filters = {field: request.args.get(field, "") for field in ("industry", "expertise", "role", "graduation_year")}
    return render_template("directory.html", alumni=search_alumni(filters), filters=filters)


@app.route("/alumni/<int:alumni_id>")
def alumni_detail(alumni_id):
    connection = get_connection()
    alumnus = connection.execute("SELECT * FROM alumni WHERE id=? AND consent=1", (alumni_id,)).fetchone()
    connection.close()
    if not alumnus:
        flash("That consenting alumni profile was not found.")
        return redirect(url_for("directory"))
    return render_template("alumni_detail.html", alumnus=alumnus)


@app.route("/matches")
def matches():
    connection = get_connection()
    student = connection.execute("SELECT * FROM students WHERE id=?", (session.get("student_id", 1),)).fetchone()
    alumni = connection.execute("SELECT * FROM alumni WHERE consent=1").fetchall()
    connection.close()
    if not student:
        flash("Create or select a student profile first.")
        return redirect(url_for("student_profile"))
    return render_template("matches.html", student=student, suggestions=suggest_mentors(student, alumni))


@app.route("/requests/new/<int:alumni_id>", methods=["GET", "POST"])
def new_request(alumni_id):
    if request.method == "POST":
        try:
            student_id = int(request.form.get("student_id", session.get("student_id", 1)))
        except ValueError:
            flash("Choose a valid student profile.")
            return redirect(url_for("new_request", alumni_id=alumni_id))
        valid, message = validate_message(request.form.get("message", ""))
        if valid:
            success, message = create_request(student_id, alumni_id, request.form.get("message", ""))
            flash(message)
            return redirect(url_for("requests_page"))
        flash(message)
    connection = get_connection()
    alumnus = connection.execute("SELECT * FROM alumni WHERE id=? AND consent=1", (alumni_id,)).fetchone()
    connection.close()
    if not alumnus:
        flash("That alumnus cannot receive requests.")
        return redirect(url_for("directory"))
    return render_template("request_form.html", alumnus=alumnus)


@app.route("/requests")
def requests_page():
    return render_template("requests.html", requests=list_requests())


@app.route("/requests/<int:request_id>/status", methods=["POST"])
def request_status(request_id):
    success, message = update_request_status(request_id, request.form.get("status", ""))
    flash(message)
    return redirect(url_for("requests_page"))


@app.route("/reports")
def report_page():
    return render_template("reports.html", report=participation_report())


@app.route("/reports.csv")
def export_report():
    try:
        content = report_csv(participation_report())
    except (OSError, csv.Error) as error:
        flash("The report could not be created: " + str(error))
        return redirect(url_for("report_page"))
    return Response(content, mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=participation-report.csv"})


@app.errorhandler(404)
def not_found(error):
    return render_template("not_found.html"), 404


@app.errorhandler(sqlite3.Error)
@app.errorhandler(OSError)
def storage_error(error):
    return render_template("storage_error.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
