from Database.connect_db import get_connection
from datetime import date as d


def insert_order(name:str,quantity:int, category:str):
    date = d.today().isoformat()
    data = {'name': name, 'date': date, 'quantity': quantity, 'category': category}
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(" INSERT INTO Orders(client_id,quantity,date,category) VALUES ((SELECT client_id FROM Clients Where client_name = :name), :quantity, :date, :category ) ", data)