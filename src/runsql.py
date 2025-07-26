import sqlite3
from sqlite3 import Error

def read_db(path):
    f = open(path,"r")
    out = f.readlines()
    f.close()
    return out

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()
