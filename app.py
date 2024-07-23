import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import hashlib
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'marketmate2'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'logos')


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

@app.route('/store')
def store():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM stores')
    stores = cursor.fetchall()  # Fetch all store records

    return render_template('store.html', stores=stores)  # Pass stores data to the template



@app.route('/addstore', methods=['GET', 'POST'])
def addstore():
    if 'loggedin' in session:  # Ensure the user is logged in
        if request.method == 'POST':
            # Get form data
            storename = request.form.get('storename')
            address = request.form.get('address')
            category = request.form.get('category')
            fees = request.form.get('fees')
            logo = request.files.get('logo')  # Get uploaded image file
            user_id = session.get('id')  # Get logged-in user ID

            

            # Check if a file is uploaded
            if logo and logo.filename:
                # Sanitize the filename
                logo_filename = secure_filename(logo.filename)
                # Create the full path where the file will be saved
                logo_path = os.path.join(app.config['UPLOAD_FOLDER'], logo_filename)
                print(f"Saving file to: {logo_path}")

                try:
                    # Save the file to the static/logos directory
                    logo.save(logo_path)
                    # Store only the filename in the database
                    logo_filename_only = logo_filename
                except Exception as e:
                    print(f"Error saving file: {e}")
                    flash('Failed to save the logo. Please try again.')
                    return redirect(url_for('addstore'))
            else:
                logo_filename_only = ''  # Default to empty if no file is provided

            # Validation checks
            if not storename or not address or not category or not logo_filename_only:
                flash('Please fill out all fields!')
            elif not re.match(r'^[A-Za-z0-9\s]+$', storename):
                flash('Store name must contain only letters, numbers, and spaces!')
            
            
            elif float(fees) < 0:
                flash('Delivery fees must be a non-negative number!')
            else:
                try:
                    # Insert store into database
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute(
                        '''
                        INSERT INTO stores (name, address, deliveryfees,  category, logo, user_id)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ''',
                        (storename, address, fees, category, logo_filename_only, user_id)
                    )
                    mysql.connection.commit()
                    flash('Store created successfully!')
                    return redirect(url_for('store'))  # Redirect to the store list page
                except MySQLdb.Error as e:
                    flash('Failed to create store. Please try again.')
                    print(f"Database error: {e}")
        return render_template('addstore.html')
    else:
        flash('Please log in to create a store!')
        return redirect(url_for('login'))


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
