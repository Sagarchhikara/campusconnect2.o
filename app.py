from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('LOGINPAGE.html')

@app.route('/signup')
def signup():
    return render_template('SIGNUP.html')

@app.route('/c_programming')
def c_programming():
    return render_template('c_programming.html')

@app.route('/operating_system')
def operating_system():
    return render_template('operating_system.html')

@app.route('/scm')
def scm():
    return render_template('scm.html')

@app.route('/deca')
def deca():
    return render_template('deca.html')

@app.route('/dent')
def dent():
    return render_template('dent.html')

@app.route('/notes')
def notes():
    return "Notes page is under construction!"  # Replace with your actual implementation

if __name__ == '__main__':
    app.run(debug=True)
