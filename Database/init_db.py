from Database.connect_db import get_connection


def init_db():
    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS
                        Clients
                    (
                        client_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_name TEXT NOT NULL
                    )
        """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS
                        Orders
                    (
                        order_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_id INTEGER NOT NULL,
                        quantity  INTEGER NOT NULL,
                        date      TEXT    NOT NULL,
                        category  TEXT    NOT NULL CHECK ( category in ('Photoshoot', 'Printout') ),
                        FOREIGN KEY (client_id) references Clients (client_id)
                    )
        """)
