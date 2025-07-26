import sys
import src.runsql
import sqlite3

def main():
    args = sys.argv[1:]
    if len(args) > 0:
        db = src.runsql.read_db(args[0])
        print(db)

if __name__ == "__main__":
    main()
