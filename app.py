import os
from dotenv import load_dotenv
from flask import Flask, render_template, g, request, session, redirect, url_for, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

from db import get_db
from views.auth import auth_bp
from views.app import app_bp

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

app.register_blueprint(app_bp)
app.register_blueprint(auth_bp)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
    
if __name__ == '__main__':
    app.run()
