import sys
from src import runsql
import sqlite3

def main():
    args = sys.argv[1:]
    if len(args) >= 1:
        db = runsql.open_conn(f"db/{args[0]}.db")
        runsql.run_sql(db, f"sql/{args[0]}.sql")
        print(db)
        runsql.close_conn(db)

if __name__ == "__main__":
    main()
