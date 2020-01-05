from dotenv import load_dotenv
from flask import Flask, render_template, g, request
from werkzeug.security import generate_password_hash, check_password_hash

from db import get_db

load_dotenv()

app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/question')
def question():
    return render_template('question.html')

@app.route('/answer')
def answer():
    return render_template('answer.html')

@app.route('/ask')
def ask():
    return render_template('ask.html')

@app.route('/unanswered')
def unanswered():
    return render_template('unanswered.html')

@app.route('/users')
def users():
    return render_template('users.html')


if __name__ == '__main__':
    app.run()
