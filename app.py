import os
from dotenv import load_dotenv
from flask import Flask, render_template, g, request, session, redirect, url_for, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

from db import get_db

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
bp = Blueprint('app', __name__)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@bp.before_app_request
def load_user():
    print('loading user')
    user = session.get('user')

    if user is None:
        g.user = None
    else:
        db = get_db()
        user_query = db.execute('select id, name, password, expert, admin from users where name = ?', [user])
        user_result = user_query.fetchone()
        g.user = user_result['name']
    print(g.user)
        
@bp.route('/')
def index():
    return render_template('home.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        hashed_pw = generate_password_hash(request.form['password'], method='sha256')
        expert = 0
        admin = 0

        db = get_db()
        db.execute('insert into users (name, password, expert, admin) values (?, ?, ?, ?)', [name, hashed_pw, expert, admin])
        db.commit()
        return '<h1> User created! </h1>'
    
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        
        db = get_db()
        user_query = db.execute('select id, name, password from users where name = (?)', [name])
        user = user_query.fetchone()

        if user is None:
            return 'User not found', 404

        if check_password_hash(user['password'], password):
            session['user'] = user['name']
            return redirect(url_for('.index'))
        else:
            return render_template('login.html')
        
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('.index'))

@bp.route('/question')
def question():
    return render_template('question.html')

@bp.route('/answer')
def answer():
    return render_template('answer.html')

@bp.route('/ask')
def ask():
    return render_template('ask.html')

@bp.route('/unanswered')
def unanswered():
    return render_template('unanswered.html')

@bp.route('/users')
def users():
    return render_template('users.html')


if __name__ == '__main__':
    app.register_blueprint(bp)
    print(app.url_map)
    print('hello')
    app.run()
