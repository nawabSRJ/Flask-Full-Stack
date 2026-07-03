from flask import Blueprint, render_template, request, session, redirect, url_for
from werkzeug.security import check_password_hash
from app.db import get_db_connection
admin_bp = Blueprint('admin', __name__)


@admin_bp.get('/login')
def admin_login_page():
    return render_template('admin/login.html')



@admin_bp.post('/login')
def admin_login():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM admin WHERE email = %s ", (email,))
        admin = cur.fetchone()
    except Exception as e:
        return render_template('admin/login.html', error=f'Exception Occured : {e}')
    finally:
        conn.close()
    
    if not admin:
        return render_template('admin/login.html', error='Admin not found')
    
    if not check_password_hash(admin['password'], password):
        return render_template('admin/login.html', error='Incorrect Password')
    
    # session for admin
    session['admin'] = {
        'email' : admin['email']
    }
    
    return redirect(url_for('admin.admin_dashboard'))


@admin_bp.route('/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return render_template('admin/not_authorized.html')
    # fetch users data from database
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()
    except Exception as e:
        return render_template('admin/dashboard.html', error=f'Exception Occured : {e}')
    finally:
        conn.close()
    return render_template('admin/dashboard.html', users=users)


@admin_bp.post('/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin.admin_login_page'))


@admin_bp.post('/delete_user/<int:user_id>')
def delete_user(user_id):
    if 'admin' not in session:
        return render_template('admin/not_authorized.html')
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
    except Exception as e:
        return render_template('admin/dashboard.html', error=f'Exception Occured : {e}')
    finally:
        conn.close()
    
    return redirect(url_for('admin.admin_dashboard'))