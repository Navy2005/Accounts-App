import sqlite3 as sql


def get_connection():
    conn = sql.connect("D:\\Accounts App\\Database\\app_data.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
