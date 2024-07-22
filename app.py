from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'marketmate2'

mysql = MySQL(app)

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def check_password(hashed_password, password):
    return hashed_password == hashlib.md5(password.encode()).hexdigest()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/logged')
def logged():
    return render_template('loggedhomepage.html')

@app.route('/header')
def header():
    return render_template('header.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()

        if account and check_password(account['password'], password):
            session['loggedin'] = True
            session['id'] = account['id']
            session['firstname'] = account['firstname']
            session['lastname'] = account['lastname']
            session['email'] = account['email']
            flash('Logged in successfully!')
            return redirect(url_for('logged'))
        else:
            flash('Incorrect email or password!')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'email' in request.form and 'role' in request.form and 'address' in request.form and 'phone' in request.form and 'password' in request.form:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        role = request.form['role']
        address = request.form['address']
        phone = request.form['phone']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()

        if account:
            flash('Account already exists with this email!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', firstname):
            flash('First name must contain only characters and numbers!')
        elif not re.match(r'[A-Za-z0-9]+', lastname):
            flash('Last name must contain only characters and numbers!')
        elif not re.match(r'[0-9]+', phone):
            flash('Phone number must contain only numbers!')
        else:
            hashed_password = hash_password(password)
            cursor.execute('INSERT INTO users (firstname, lastname, email, role, address, phone, password) VALUES (%s, %s, %s, %s, %s, %s, %s)', (firstname, lastname, email, role, address, phone, hashed_password))
            mysql.connection.commit()
            flash('You have successfully registered!')
            return redirect(url_for('login'))
    elif request.method == 'POST':
        flash('Please fill out the form!')

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
