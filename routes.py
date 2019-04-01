from server import app, system, login_manager
from flask import Flask, render_template, request, url_for, redirect
from flask_login import UserMixin, login_user, login_required, current_user, logout_user

@login_manager.user_loader
def load_user(id):
    return system.get_user(id)

@app.route("/", methods=["GET", "POST"])
def login():
    error = False
    if request.method == "POST":
        id = request.form["zid"]
        password = request.form["password"]
        if system.authenticate_user(id, password):
            system.populate_courses(current_user.id)
            return redirect(url_for("courses"))
        else:
            error = True
    return render_template("login.html", error = error)

@app.route("/courses", methods=["GET", "POST"])
@login_required
def courses():
    try:
        courses = system.get_courses(current_user.id)
        if request.method == "POST":
            for c in courses:
                if request.form.get(c.name):
                    c.selected = True
                else:
                    c.selected = False

            # fix course choice error!!

            return redirect(url_for("events"))

        return render_template("courses.html", courses = courses)
    except:
        return redirect(url_for("logout"))

@app.route('/events', methods=["GET", "POST"])
@login_required
def events():
    try:
        if request.method == "POST":
            # write to necessary stuff
            system.scrape_due_dates(current_user.id)
            return redirect(url_for("duedates"))

        return render_template("events.html")
    except:
        return redirect(url_for("logout"))

@app.route('/duedates', methods=["GET", "POST"])
@login_required
def duedates():
    try:
        courses = system.get_courses(current_user.id)
        return render_template('duedates.html', courses = courses)
    except:
        return redirect(url_for("logout"))

@app.route('/logout')
@login_required
def logout():
    system.log_out_user(current_user.id)
    return redirect(url_for("login"))