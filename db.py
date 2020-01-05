import sqlite3
import os
from flask import g

DATABASE_PATH = os.environ.get('DATABASE_PATH')

def connect_db():
    sql = sqlite3.connect(DATABASE_PATH)
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
