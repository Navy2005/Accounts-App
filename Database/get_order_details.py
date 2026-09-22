from Database.connect_db import get_connection

def get_Client_orders(client_name,month_number,category):
    with get_connection() as conn:
        cur=conn.cursor()
        cur.execute('''
                    SELECT Orders.order_id, Orders.date, Orders.quantity
                    FROM Orders
                    JOIN Clients ON orders.client_id = Clients.client_id
                    WHERE Clients.client_name = ?
                      AND strftime('%m', orders.date) = ?
                      AND category = ?
                    ORDER BY Orders.date
                    ''', (client_name, month_number, category))
        return cur.fetchall()

def get_client_orders_with_category(client_name,month_number):
    with get_connection() as conn:
        cur=conn.cursor()
        cur.execute('''
                    SELECT Orders.order_id, Orders.date, Orders.quantity, Orders.category
                    FROM Orders
                    JOIN Clients ON orders.client_id = Clients.client_id
                    WHERE Clients.client_name = ?
                      AND strftime('%m', orders.date) = ?
                    ORDER BY Orders.date
                    ''', (client_name, month_number))
        return cur.fetchall()



def get_order_id_list(client_name,month_number,category):
    with get_connection() as conn:
        cur=conn.cursor()
        cur.execute('''SELECT DISTINCT order_id FROM Orders 
                    JOIN Clients ON Orders.client_id = Clients.client_id
                    WHERE Clients.client_name = ? 
                    AND strftime('%m',date) = ? 
                    AND category = ?''', [client_name, month_number, category])
        return [row[0] for row in cur.fetchall()]


# def get_monthly_orders(client_name, month_number, category):
#     """
#     Fetches (date, quantity) tuples for a client in a given month,
#     sorted in ascending order by date.
#     """
#     with get_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute( '''
#                        SELECT orders.date, orders.quantity
#                        FROM orders
#                                 JOIN Clients ON orders.client_id = Clients.client_id
#                        WHERE Clients.client_name = ?
#                          AND strftime('%m', orders.date) = ?
#                            AND category = ?
#                        ORDER BY orders.date ASC
#                        ''' , (client_name, month_number, category))
#
#         return cursor.fetchall()