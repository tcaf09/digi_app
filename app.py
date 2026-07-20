from flask import *
import sys
import logging

#---CONFIGURE APP---------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
logging.basicConfig(filename='logs/flask.log', level=logging.INFO)
sys.tracebacklimit = 10

#---VIEW FUNCTIONS----------------------------------------------------
@app.route('/')
def login():
    app.logger.info("Login")
    session['permission'] = 'admin'
    return "<b>Login Page</b>"

@app.route('/logout')
def logout():
    app.logger.info("Logout")
    session.clear()
    return redirect('/login')

@app.route('/register')
def register():
    app.logger.info("Register")
    return "Registration Page"

@app.route('/home')
def home():
    if 'permission' in session:
        if session['permission'] == 'admin':
            return "All glory to the administrator!"
    app.logger.info("Home")
    return "Home"

@app.route('/admin')
def admin():
    app.logger.info("admin")
    return "Admin"




#main method called web server application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) #runs a local server on port 5000
