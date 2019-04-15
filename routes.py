from flask import Flask, render_template, request, url_for, redirect, send_file
from User import User
from UserSystem import UserSystem
from CourseSystem import CourseSystem
from EventSystem import EventSystem
from Deadline import Deadline
from DeadlineSystem import DeadlineSystem


app = Flask(__name__)
#user = None
userSystem = UserSystem()
courseSystem = CourseSystem()
eventSystem = EventSystem()
deadlineSystem = DeadlineSystem()
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

@app.route('/duedates/<id>/', methods=["GET", "POST"])
def duedates(id):
    error=""
    user = userSystem.getUser(id)
    ### Test
    test_string = 'Final exam1,2019-04-14T09:00:00,Worth 20%,UNSW=Final exam2,2019-04-14T09:00:00,Worth 20%,UNSW=Final exam3,2019-04-15T09:00:00,Worth 20%,UNSW'
    tt = test_string.split('=')
    d = []
    for t in tt:
        t = (t.split(','))
        d.append(Deadline(t[0], t[1], t[2], t[3]))
    ### Endtest
    deadlineSystem.createCalender(user.zID, d)
    '''
    try:
        if request.method == 'POST':
            if show != None:
                redirect(url_for('duedatesShow', id=user.zID, show=))
            else:
                return render_template('duedates.html', id=user.zID, error=error)

    except Exception as e:
        return render_template('duedates.html', id=user.zID, error=e)
    '''
    return render_template('duedates.html', id=user.zID, error=error)

@app.route('/duedates/<id>/<show>', methods=["GET", "POST"])
def duedatesShow(id, show):
    error=""
    user = userSystem.getUser(id)
    test_string = 'Final exam1,2019-04-14T09:00:00,Worth 20%,UNSW=Final exam2,2019-04-14T09:00:00,Worth 20%,UNSW=Final exam3,2019-04-15T09:00:00,Worth 20%,UNSW'
    tt = test_string.split('=')
    d = []
    for t in tt:
        t = (t.split(','))
        d.append(Deadline(t[0], t[1], t[2], t[3]))
    ### Endtest
    deadlineSystem.createCalender(user.zID, d)
    try:
        if request.method == 'POST':
            if 'gid' == show:
                error = deadlineSystem.gcal(request.form['gID'], d)
            elif 'eadd' == show:
                error = deadlineSystem.sendEmail(user.zID, request.form['eAdd'])
            else:
                render_template('duedates.html', id=user.zID, error=error, show=show)
    except Exception as e:
        render_template('duedates.html', id=user.zID, error=e, show=show)

    return render_template('duedates.html', id=user.zID, error=error, show=show)


@app.route('/getFile/<id>/<fileType>')
def getFile(id, fileType):
    user = userSystem.getUser(id)
    # Create File
    # deadlineSystem.createCalender(user.zID, deadlines, 'fileType')
    return send_file((user.zID+'.'+fileType), attachment_filename=(user.zID+'.'+fileType))













if __name__ == '__main__':
    app.run(debug=True)
