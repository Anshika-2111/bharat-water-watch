import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'water_watch.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn