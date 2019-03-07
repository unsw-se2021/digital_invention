from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/processing')
def processing():
    return render_template('processing.html')

@app.route('/duedates')
def duedates():
    return render_template('duedates.html')













if __name__ == '__main__':
    app.run(debug=True)
