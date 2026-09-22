from Database.connect_db import get_connection



def correct_order(quantity, order_id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE Orders SET quantity = ? WHERE order_id = ?", [quantity, order_id])
# correct_order(12,16)