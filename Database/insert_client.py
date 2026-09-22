from Database.connect_db import get_connection


def InsertClient(name: str):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO Clients (client_name) VALUES (?)", [name])
