from flask import *
import sys
import logging
from interfaces.databaseinterface import Database

#---CONFIGURE APP---------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
logging.basicConfig(filename='logs/flask.log', level=logging.INFO)
sys.tracebacklimit = 10
DATABASE = Database('database/test.db', log=app.logger)

@app.route('/backdoor')
def backdoor():
    results = DATABASE.ViewQuery('SELECT * FROM users')
    return jsonify(results)

#---VIEW FUNCTIONS----------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email') #name of the input
        password = request.form.get('password') #name of input
        results = DATABASE.ViewQuery('SELECT * FROM users WHERE email = ? and password = ?', (email,password))
        if results:
            session['userid'] = results[0]['userid']
            session['permission'] = results[0]['permission']
            flash("Login successful!")
            return redirect('/home')
        else:
            flash("Invalid credentials. Please try again.")
    app.logger.info("Login")
    return render_template('login.html')

@app.route('/logout')
def logout():
    app.logger.info("Logout")
    session.clear()
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash("Passwords do not match. Please try again.")
        else:
            results = DATABASE.ViewQuery('SELECT * FROM users WHERE email = ?', (email,))
            if not results:
                DATABASE.ModifyQuery('INSERT INTO users (email, password, firstname, lastname) VALUES (?, ?, ?, ?)', (email, password, firstname, lastname))
                flash("Registration successful. Please login.")
                return redirect('/')
            else:
                flash("Email already exists. Please try again.")    
    app.logger.info("Register")
    return render_template('register.html')

@app.route('/home')
def home():
    app.logger.info("Home")
    return render_template('home.html')

@app.route('/admin')
def admin():
    app.logger.info("admin")
    return "Admin"

#main method called web server application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) #runs a local server on port 5000
