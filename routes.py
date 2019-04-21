from server import app, system, login_manager
from flask import Flask, render_template, request, url_for, redirect, send_file
from flask_login import UserMixin, login_user, login_required, current_user, logout_user

@login_manager.user_loader
def load_user(id):
    return system.get_user(id)

@app.route("/", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        id = request.form["zid"]
        password = request.form["password"]
        if system.authenticate_user(id, password):
            num_courses = system.populate_courses(current_user.id)
            if num_courses > 0:
                return redirect(url_for("courses"))
            else:
                error = "Sorry, no WebCMS3 courses were found"
        else:
            error = "Incorrect zID or password, please try again"
    return render_template("login.html", error = error)

@app.route("/courses", methods=["GET", "POST"])
@login_required
def courses():
    try:
        error = ""
        courses = system.get_courses(current_user.id)
        if request.method == "POST":
            any_selected = False
            for c in courses:
                c.selected = False
                if request.form.get(c.name):
                    c.selected = True
                    any_selected = True
            if any_selected:
                return redirect(url_for("events"))
            else:
                error = "You must select at least one course"
        return render_template("courses.html", courses = courses, error = error)
    except:
        return redirect(url_for("logout"))

@app.route('/events', methods=["GET", "POST"])
@login_required
def events():
    # try:
    error = ""
    if request.method == "POST":
        any_selected = False
        find_assignments = False
        find_exams = False
        find_milestones = False
        find_labs = False
        if request.form.get("assignments"):
            find_assignments = True
            any_selected = True
        if request.form.get("exams"):
            find_exams = True
            any_selected = True
        if request.form.get("milestones"):
            find_milestones = True
            any_selected = True
        if request.form.get("labs"):
            find_labs = True
            any_selected = True
        if any_selected:
            system.scrape_due_dates(current_user.id, find_assignments, find_exams, find_milestones, find_labs)
            return redirect(url_for("duedates"))
        else:
            error = "You must select at least one event"
    return render_template("events.html", error = error)
    # except:
    #     return redirect(url_for("logout"))

@app.route('/duedates', methods=["GET", "POST"])
@login_required
def duedates():
    # try:
    courses = system.get_courses(current_user.id)
    d = system.get_deadlines(current_user.id)
    message = ""
    if request.method == "POST":
        if "submit_gID" in request.form:
            message = system.gcal(request.form['gID'], d)
        elif "submit_eAdd" in request.form:
            message = system.sendEmail(current_user.id, request.form['eAdd'])
    else:
        system.createCalendar(current_user.id, d)
    return render_template('duedates.html', courses = courses, message = message)

    # except:
    #      return redirect(url_for("logout"))

@app.route('/logout')
@login_required
def logout():
    system.log_out_user(current_user.id)
    return redirect(url_for("login"))

@app.route('/calendar.<fileType>')
@login_required
def sendcalendar(fileType):
    # can never be too careful
    if fileType == "csv":
        return send_file("calendars/" + current_user.id + ".csv")
    if fileType == "ics":
        return send_file("calendars/" + current_user.id + ".ics")
