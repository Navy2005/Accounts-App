from Database.connect_db import get_connection


def GetClientList():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Clients")
        return cur.fetchall()


def get_client_id_by_client_name(client_name):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT client_id FROM Clients WHERE client_name = ?", [client_name])
        return cur.fetchone()