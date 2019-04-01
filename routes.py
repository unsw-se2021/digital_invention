from flask import Flask, render_template, request, url_for, redirect
from User import User
from UserSystem import UserSystem
from CourseSystem import CourseSystem
from EventSystem import EventSystem
#from


app = Flask(__name__)
#user = None
userSystem = UserSystem()
courseSystem = CourseSystem()
eventSystem = EventSystem()
ERROR_STATEMENT = "What you trying to do bruh!"




@app.route('/', methods=["GET", "POST"])
def index():
    error = ""
    try:
        if request.method == "POST":
            user = User(request.form['zID'], request.form['zPass'])

            if user.authenticate() == True:
                print('User Authenticated')
                userSystem.users = user
                return redirect(url_for('courses', id=user.zID))
            else:
                    error = "Invalid. Try Again!"

            return render_template('index.html', error=error)
    except Exception as e:
        return render_template('index.html', error=e)
    #else:
    return render_template('index.html', error=error)

@app.route('/courses/<id>', methods=["GET", "POST"])
def courses(id):
    user = userSystem.getUser(id)
    courseSystem.populateCourses(user)
    err = True
    error = ""
    try:
        if request.method == "POST":

            newCourse = request.form.get('addCourse')
            if (len(newCourse)) > 0:
                e = courseSystem.addNewCourse(user, newCourse)
                return render_template('courses.html', id=user.zID, courses=user.courses, error=e)

            if 'True' == request.form.get('all'):
                print('all selected')
                err = False
                for course in user.courses:
                    course.do = True
                    print(course.name)
            else:
                for course in user.courses:

                    if 'True' == request.form.get(course.name):
                        course.do = True
                        print('selected'+course.name)
                        err = False

            if err == True:
                return render_template('courses.html', id=user.zID, courses=user.courses, error=ERROR_STATEMENT)
            else:
                return redirect(url_for('events', id=user.zID))


    except Exception as e:

        return render_template('courses.html', id=user.zID, courses=user.courses, error=e)

    return render_template('courses.html', id=user.zID, courses=user.courses, error=error)


@app.route('/events/<id>', methods=["GET", "POST"])
def events(id):
    user = userSystem.getUser(id)
    eventSystem.populateEvents(user)
    err = ''
    try:
        if request.method == 'POST':
            if 'True' == request.form.get('all'):
                for c in user.courses:
                    for e in c.events:
                        e.do = True
                        err = 'Selected'
                        print('here')
            else:
                for c in user.courses:
                    for e in c.events:
                        if True == request.form.get(c.name+e.description+'do'):
                            e.do = True
                            err = 'Selected'
        if err == 'Selected':
            #print('here')
            return redirect(url_for('processing', id=user.zID))
        else:
            err = 'Nothing Selected!'
            return render_template('events.html', id=user.zID, courses=user.courses, error=err)

    except Exception as e:
        return render_template('events.html', id=user.zID, courses=user.courses, error=e)

    return render_template('events.html', id=user.zID, courses=user.courses, error=err)


@app.route('/processing/<id>', methods=["GET", "POST"])
def processing(id):
    user = userSystem.getUser(id)
    return render_template('processing.html', id=user.zID)

@app.route('/duedates')
def duedates():
    return render_template('duedates.html')













if __name__ == '__main__':
    app.run(debug=True)
