import sqlite3
from sqlite3 import Error

DB_FILE = 'songs.db'


def get_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
    except Error as e:
        print(e)

    return conn


def query_db(query, args=(), one=False):
    cur = get_connection().cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r
