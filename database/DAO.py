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
        query = """with tot_quantity as (select oi.order_id, sum(oi.quantity) as tot
                    from order_items oi 
                    group by oi.order_id)
                    
                    select distinctrow o.order_id, o2.order_id, o.order_date, o2.order_date, (tot_quantity.tot + oi2.tot_quantity.tot) as qtyOrder
                    from orders o, orders o2, order_items oi, order_items oi2 
                    where o.order_id = oi.order_id and o2.order_id = oi2.order_id 
                    and o.order_id != o2.order_id 
                    and o.order_date < o2.order_date
                    and o2.store_id = 1
                    and datediff(o2.order_date, o.order_date) <= 5 """

        cursor.execute(query, (storeId, numMin, ))

        res = []
        for row in cursor:
            res.append(Order(**row))
        cursor.close()
        conn.close()
        return res