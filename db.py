import os
import sqlite3
import psycopg2
from psycopg2.extras import DictCursor
from flask import g

DATABASE_URL = 'postgres://awaaiikhpibljm:2c38dec9c6bd5b1e5e6ff14ddee44984058b94db0db23ca27ce493428a3cd466@ec2-174-129-254-218.compute-1.amazonaws.com:5432/d4g4ajm4pu33kg'

def connect_db():
    connection = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
    connection.autocommit = True
    sql = connection.cursor()
    return connection, sql

def get_db():
    db = connect_db()
    if not hasattr(g, 'postgres_db_conn'):
        g.postgres_db_conn = db[0]
    if not hasattr(g, 'postgres_db_cur'):
        g.postgres_db_cur = db[1]
            
    return g.postgres_db_cur

def init_db():
    db = connect_db()
    db[1].execute(open('schema.sql', 'r').read())
    db[1].close()
    db[0].close()
