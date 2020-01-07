from flask import render_template, g, request, session, redirect, url_for, Blueprint
import functools
from werkzeug.security import generate_password_hash, check_password_hash

from db import get_db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.before_app_request
def load_user():
    user = session.get('user')

    if user is None:
        g.user = None
    else:
        db = get_db()
        db.execute('select id, name, password, expert, admin from users where name = %s', (user, ))
        user_result = db.fetchone()
        g.user = user_result

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        db = get_db()

        db.execute('select id, name from users where name = %s', (name, ))
        existing_user = db.fetchone()

        if existing_user:
            return render_template('register.html', error='User already exists.')

        hashed_pw = generate_password_hash(request.form['password'], method='sha256')
        expert = False
        admin = False
        db.execute('insert into users (name, password, expert, admin) values (%s, %s, %s, %s)', (name, hashed_pw, expert, admin))
        
        return redirect(url_for('.login'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        error = {}
        db = get_db()
        db.execute('select id, name, password from users where name = %s', (name, ))
        user = db.fetchone()

        if user is None:
            error['name'] = 'User not found.'
        
        if check_password_hash(user['password'], password):
            session['user'] = user['name']
            return redirect(url_for('app.index'))
        else:
            error['password'] = 'Password incorrect.'
            return render_template('login.html', error=error, username=name)
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('app.index'))

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or not g.user['admin']:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def expert_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or not g.user['expert']:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
