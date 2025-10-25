import pymysql
import pandas as pd

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="localfoodwaste",
        cursorclass=pymysql.cursors.DictCursor
    )

def run_query(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params or ())
    rows = cur.fetchall()
    conn.close()
    return pd.DataFrame(rows)

def run_modify(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params or ())
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return affected
