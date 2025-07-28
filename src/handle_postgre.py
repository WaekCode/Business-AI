import psycopg2

def main():
    conn = psycopg2.connect(
        dbname="ger",
        user="postgres",
        password="",
        host="localhost"
    )