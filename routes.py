from flask import Flask, render_template, request, url_for, redirect
from User import User
from UserSystem import UserSystem


app = Flask(__name__)
user = None
userSystem = None
ERROR_STATEMENT = "What you trying to do bruh!"

@app.route('/', methods=["GET", "POST"])
def index():
    error = ""
    try:
        if request.method == "POST":
            global user
            user = User(request.form['zID'], request.form['zPass'])

            if user.authenticate() == True:
                print('User Authenticated')
                return redirect(url_for('courses', id=user.zID))
            else:
                    error = "Invalid. Try Again!"

            return render_template('index.html', error=error)
    except Exception as e:
        return render_template('index.html', error=ERROR_STATEMENT)
    #else:
    return render_template('index.html', error=error)

@app.route('/courses/<id>', methods=["GET", "POST"])
def courses(id):
    global user
    global userSystem
    userSystem = UserSystem(user)
    user.courses = userSystem.populateCourses()
    err = True
    error = ""
    try:
        if request.method == "POST":
            print('post request recieved')
            res = request.form.get('all')
            print(res)
            if 'True' == res:
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
                return redirect(url_for('processing', id=user.zID))


    except Exception as e:

        return render_template('courses.html', id=user.zID, courses=user.courses, error=e)

    return render_template('courses.html', id=user.zID, courses=user.courses, error=error)

@app.route('/processing/<id>', methods=["GET", "POST"])
def processing(id):
    return render_template('processing.html', id=user.zID)

@app.route('/duedates')
def duedates():
    return render_template('duedates.html')













if __name__ == '__main__':
    app.run(debug=True)
