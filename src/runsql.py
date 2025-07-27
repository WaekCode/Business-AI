import os
import sqlite3
from sqlite3 import Error

def open_conn(db_path):
    try:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path)
        return conn
    except Error as e:
        raise(e)

def read_sql(sql_path):
    try:
        f = open(sql_path,"r")
        out = f.read()
        f.close()
        return out
    except Error as e:
        raise(e)

def run_sql(conn, sql_code):
    try:
        cursor = conn.cursor()
        cursor.executescript(sql_code)
        return cursor.fetchall()
    except Error as e:
        raise(e)

def close_conn(conn):
    conn.close()

def main():
    print("Call functions from main for now")

if __name__ == "__main__":
    main()
