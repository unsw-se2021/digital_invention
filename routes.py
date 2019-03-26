from flask import Flask, render_template, request, url_for, redirect
from User import User
from UserSystem import UserSystem


app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    error = ""
    try:
        if request.method == "POST":
            user = User(request.form['zID'], request.form['zPass'])
            if user.authenticate() == True:
                print('User Authenticated')
                return redirect(url_for('courses', user=user))
            else:
                error = "Invalid. Try Again!"

            return render_template('index.html', error=error)
    except Exception as e:
        return render_template('index.html', error=error)
    #else:
    return render_template('index.html', error=error)

@app.route('/courses/<user>', methods=["GET", "POST"])
def courses(user):
    userSystem = UserSystem(user)
    user.courses = userSystem.populateCourses()
    return render_template('courses.html', user=user)

@app.route('/processing')
def processing():
    return render_template('processing.html')

@app.route('/duedates')
def duedates():
    return render_template('duedates.html')













if __name__ == '__main__':
    app.run(debug=True)
