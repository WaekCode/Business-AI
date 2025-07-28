import sys
from src import runsql
import sqlite3

def main():
    args = sys.argv[1:]
    if len(args) >= 1:
        out = runsql.read_sql(f"sql/{args[0]}.sql")
        db = runsql.open_conn(f"db/{args[0]}.db")
        out1 = runsql.run_sql(db, out)
        print(out1)
        if len(args) >= 2:
            out2 = runsql.run_sql(db, args[1])
            print(out2)
        print(db)
        runsql.close_conn(db)
    

if __name__ == "__main__":
    main()
