import os
import sqlite3
import psycopg2
from psycopg2.extras import DictCursor
from flask import g
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')

def connect_db():
    import pdb; pdb.set_trace()
    connection = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
    connection.autocommit = True
    sql = connection.cursor
    return connection, sql

def get_db():
    db = connect_db()
    if not hasattr(g, 'postgres_db_conn'):
        g.postgres_db_conn = db[0]
    if not hasattr(g, 'postgres_db_cur'):
        g.postgres_db_cur = db[1]
            
    return g.postgres_db_cur

def init_db():
    import pdb; pdb.set_trace()

    db = connect_db()
    db[1].execute(open('schema.sql', 'r').read())
    db[1].close()
    db[0].close()
