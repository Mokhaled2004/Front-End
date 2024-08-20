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
app.config['PP_UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'pps')  # Add new folder for profile pictures
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Specify allowed file types

mysql = MySQL(app)

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def check_password(hashed_password, password):
    return hashed_password == hashlib.md5(password.encode()).hexdigest()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/logged')
def logged():
    return render_template('loggedhomepage.html')


@app.route('/modifycategory')
def modifycategory():
    return render_template('modifycategory.html')

@app.route('/header')
def header():
    return render_template('header.html')
@app.route('/editstore/<int:store_id>', methods=['GET', 'POST'])
def editstore(store_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Fetch store data based on the store ID
    cursor.execute('SELECT * FROM stores WHERE id = %s', (store_id,))
    store = cursor.fetchone()

    # Check if the store exists
    if not store:
        flash('Store not found!')
        return redirect(url_for('profile'))

    if request.method == 'POST':
        # Handle form data for updating the store
        name = request.form.get('sname')
        address = request.form.get('address')
        delivery_fees = request.form.get('dfees')
        category = request.form.get('category')
        logo = request.files.get('pp')

        if logo and allowed_file(logo.filename):
            logo_filename = secure_filename(logo.filename)
            logo_path = os.path.join(app.config['LOGO_UPLOAD_FOLDER'], logo_filename)
            try:
                logo.save(logo_path)
                logo_filename_only = logo_filename
            except Exception as e:
                flash('Failed to save the logo. Please try again.')
                return redirect(url_for('editstore', store_id=store_id))

        else:
            logo_filename_only = store['logo']  # Use existing logo if none is uploaded

        try:
            cursor.execute('''
                UPDATE stores
                SET name = %s, address = %s, deliveryfees = %s, category = %s, logo = %s
                WHERE id = %s
            ''', (name, address, delivery_fees, category, logo_filename_only, store_id))
            mysql.connection.commit()
            flash('Store updated successfully!')
            return redirect(url_for('profile'))
        except MySQLdb.Error as e:
            flash('Failed to update store. Please try again.')
            print(f"Database error: {e}")

    cursor.close()

    # Pass the entire store object to the template
    return render_template('editstore.html', store=store)




@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # Ensure the user is logged in
    if 'loggedin' in session:
        user_id = session['id']  # Get the logged-in user's ID

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Fetch user data based on the session user ID
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()

        # Fetch user's stores
        cursor.execute('SELECT * FROM stores WHERE user_id = %s', (user_id,))
        stores = cursor.fetchall()

        # Handle profile update
        if request.method == 'POST':
            # Get updated profile data from the form
            firstname = request.form.get('fname')
            lastname = request.form.get('lname')
            email = request.form.get('email')
            password = request.form.get('password')
            address = request.form.get('address')
            role = request.form.get('role')
            pp = request.files.get('pp')  # Get uploaded profile picture

            # Update profile picture if a new one is uploaded
            if pp and allowed_file(pp.filename):
                pp_filename = secure_filename(pp.filename)
                pp_path = os.path.join(app.config['PP_UPLOAD_FOLDER'], pp_filename)
                
                try:
                    # Save the new profile picture
                    pp.save(pp_path)
                    pp_filename_only = pp_filename
                except Exception as e:
                    flash('Failed to save the profile picture. Please try again.')
                    return redirect(url_for('profile'))

            else:
                pp_filename_only = user['pp']  # Use existing profile picture if none is uploaded

            # Validate input
            if not all([firstname, lastname, email, role, address, password]):
                flash('Please fill out all fields!')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address!')
            elif not re.match(r'[A-Za-z0-9]+', firstname):
                flash('First name must contain only characters and numbers!')
            elif not re.match(r'[A-Za-z0-9]+', lastname):
                flash('Last name must contain only characters and numbers!')
            elif not re.match(r'[0-9]+', address):
                flash('Phone number must contain only numbers!')
            else:
                # Hash the password before storing it
                hashed_password = hash_password(password)
                try:
                    # Update user information in the database
                    cursor.execute('''
                        UPDATE users
                        SET firstname = %s, lastname = %s, email = %s, role = %s, address = %s, password = %s, pp = %s
                        WHERE id = %s
                    ''', (firstname, lastname, email, role, address, hashed_password, pp_filename_only, user_id))
                    mysql.connection.commit()
                    flash('Profile updated successfully!')

                    # Refresh the page to display updated data
                    return redirect(url_for('profile'))

                except MySQLdb.Error as e:
                    flash('Failed to update profile. Please try again.')
                    print(f"Database error: {e}")

        cursor.close()
        return render_template('account.html', user=user, stores=stores)

    else:
        flash('Please log in to view your profile!')
        return redirect(url_for('login'))




@app.route('/store')
def store():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Fetch all store records
    cursor.execute('SELECT * FROM stores')
    stores = cursor.fetchall()
    
    # Fetch unique categories
    cursor.execute('SELECT DISTINCT category FROM stores')
    categories = cursor.fetchall()
    
    cursor.close()
    
    # Extract category names from the list of dictionaries
    category_list = [cat['category'] for cat in categories]
    
    return render_template('store.html', stores=stores, categories=category_list)


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
            if logo and allowed_file(logo.filename):
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
            elif not re.match(r'^[0-9]+$', fees):
                flash('Delivery fees must be a valid number!')
            elif float(fees) < 0:
                flash('Delivery fees must be a non-negative number!')
            else:
                try:
                    # Insert store into database
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute(
                        '''
                        INSERT INTO stores (name, address, deliveryfees, category, logo, user_id)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ''',
                        (storename, address, fees, category, logo_filename_only, user_id)
                    )
                    mysql.connection.commit()
                    cursor.close()
                    flash('Store created successfully!')
                    return redirect(url_for('store'))  # Redirect to the store list page
                except MySQLdb.Error as e:
                    flash('Failed to create store. Please try again.')
                    print(f"Database error: {e}")
        return render_template('createstore.html')
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
            return redirect(url_for('home'))
        else:
            flash('Incorrect email or password!')
        cursor.close()

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        role = request.form.get('role')
        address = request.form.get('address')
        phone = request.form.get('phone')
        password = request.form.get('password')

        if not all([firstname, lastname, email, role, address, phone, password]):
            flash('Please fill out the form!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', firstname):
            flash('First name must contain only characters and numbers!')
        elif not re.match(r'[A-Za-z0-9]+', lastname):
            flash('Last name must contain only characters and numbers!')
        elif not re.match(r'[0-9]+', phone):
            flash('Phone number must contain only numbers!')
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            account = cursor.fetchone()

            if account:
                flash('Account already exists with this email!')
            else:
                hashed_password = hash_password(password)
                try:
                    cursor.execute(
                        'INSERT INTO users (firstname, lastname, email, role, address, phone, password) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (firstname, lastname, email, role, address, phone, hashed_password)
                    )
                    mysql.connection.commit()
                    flash('You have successfully registered!')
                    return redirect(url_for('login'))
                except MySQLdb.Error as e:
                    flash('Registration failed. Please try again.')
                    print(f"Database error: {e}")
            cursor.close()

    return render_template('register.html')

@app.route('/logout')
def logout():
    # Clear session data to log out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('firstname', None)
    session.pop('lastname', None)
    session.pop('email', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
