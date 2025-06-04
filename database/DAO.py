from database.DB_connect import DBConnect
from model.order import Order
from model.store import Store


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getStores():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select *
                from stores s """
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Store(**row))
        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getNodes(storeId):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select *
                from orders o 
                where o.store_id = %s"""
        cursor.execute(query, (storeId, ))

        res = []
        for row in cursor:
            res.append(Order(**row))
        cursor.close()
        conn.close()
        return res

    def getEdges(self, storeId, numMin):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select distinctrow o.order_id, o2.order_id, o.order_date, o2.order_date, (oi.quantity + oi2.quantity) as qtyOrder
                    from orders o, orders o2, order_items oi, order_items oi2 
                    where o.order_id = oi.order_id and o2.order_id = oi2.order_id 
                    and o.order_id != o2.order_id 
                    and o.order_date < o2.order_date
                    and o2.store_id = %s
                    and datediff(o2.order_date, o.order_date) <= %s """
        cursor.execute(query, (storeId, numMin, ))

        res = []
        for row in cursor:
            res.append(Order(**row))
        cursor.close()
        conn.close()
        return res