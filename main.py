import sys
import src.runsql
import sqlite3

def main():
    args = sys.argv[1:]
    if len(args) >= 1:
        db = src.runsql.read_db(f"sql/{args[0]}.sql", f"db/{args[0]}.db")
        print(db)

if __name__ == "__main__":
    main()
