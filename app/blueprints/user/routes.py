import os
import uuid
from flask import Blueprint, render_template, request, flash, current_app, redirect, url_for, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db_connection

user_bp = Blueprint('user', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# -------------------------------- Helper Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_user(data):
    if int(data['age']) < 3 or int(data['age']) > 100:
        return 'Age must be between 3 and 100'
    
    if data['password'] != data['c_passwd']:
        return 'Passwords do not match'

    if len(data['password']) < 8:
        return 'Password must be at least 8 characters long'

    if len(data['phone']) != 10 or not data['phone'].isdigit():
        return 'Phone number must be 10 digits long'
    
    return False    # No errors

# --------------------------------- ROUTES
@user_bp.get('/login')
def login_page():
    return render_template('user/login.html')

@user_bp.get('/signup')
def signup_page():
    return render_template('user/signup.html')



@user_bp.post('/signup')
def user_signup():
    # grab all the values
    data = dict(
    name = request.form.get('name'),
    email = request.form.get('email'),
    password = request.form.get('password'),
    c_passwd = request.form.get('confirm_password'),
    phone = request.form.get('phone'),
    age = request.form.get('age'),
    gender = request.form.get('gender'),
    course = request.form.get('course'),
    )
    
    error = validate_user(data)
    if error:
        return render_template('user/signup.html', error=error)
    
    # photo upload handling
    photo_filename = None # default if no pic uploaded
    file = request.files.get('user_photo')
    if file and file.filename != '':
        if not allowed_file(file.filename):
             return render_template('user/signup.html', error='Only image files are allowed (png, jpg, jpeg, gif)')
        
        flash(f'Flash : Photo {file.filename} has been uploaded!')

        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        # current_app is a flask context variable that gives access to the app's config
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file.save(os.path.join(upload_folder, unique_filename))
        photo_filename = unique_filename    # only saving the photo filename to DB

    
    # push data to db
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id from users WHERE email = %s OR phone = %s", (data['email'], data['phone'])
            )
            existing = cur.fetchone()
            if existing:
                return render_template('user/signup.html', error='Email or Phone already exists')
            
            hashed_password = generate_password_hash(data['password'])
            cur.execute(
                """INSERT INTO users(name, email, password, phone, age, gender, course, photo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (data['name'], data['email'], hashed_password, data['phone'], int(data['age']), data['gender'], data['course'], photo_filename)
            )
    except Exception as e:
        return render_template('user/signup.html', error=f'Exception occurred : {e}')
    finally:
        conn.close()
    
    return redirect(url_for('user.login_page'))



@user_bp.post('/login')
def user_login():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
    
    except Exception as e:
        return render_template('user/login.html', error=f'Exception occurred : {e}')

    finally:
        conn.close()
    

    if not user:
        return render_template('user/login.html', error='User does not exist')

    if not check_password_hash(user['password'], password):
        return render_template('user/login.html', error='Incorrect Password')

    # create session for user 
    session['user'] = {
        'name' : user['name'],
        'email' : user['email'],
        'age' : user['age'],
        'course' : user['course'],
        'gender' : user['gender'],
        'phone' : user['phone'],
        'photo' : user['photo']
    }
    return redirect(url_for('user.dashboard'))


@user_bp.get('/dashboard')
def dashboard():
    if 'user' not in session:
        return render_template('user/not_authorized.html')
    return render_template('user/dashboard.html', user=session.get('user'))

@user_bp.post('/logout')
def logout():
    session.clear()
    return redirect(url_for('user.login_page'))