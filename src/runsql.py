import os
import sqlite3
from sqlite3 import Error

def read_db(path,dbname):
    f = open(path,"r")
    out = f.read()
    f.close()
    try:
        os.makedirs("db", exist_ok=True)
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
        cursor.executescript(out)
        conn.close()
        return conn
    except OSError as e:
        raise(e)
    except sqlite3.OperationalError as e:
        raise(e)

def main():
    print("Call read.db from main")

if __name__ == "__main__":
    main()
