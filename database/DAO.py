from database.DB_connect import DBConnect
from model.arco import Arco
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

    def getEdges(self, numMin, storeId):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select o.order_id as order1_id, o2.order_id as order2_id, o.order_date as order1_date, o2.order_date as order2_date, (tq1.tot + tq2.tot) as qtyOrder
                    from orders o
                    join orders o2 on o.order_id != o2.order_id 
                    and o.order_date < o2.order_date
                    and datediff(o2.order_date, o.order_date) <= 5 
                    and o2.store_id = 1
                    join (select order_id, sum(quantity) as tot
                    from order_items  
                    group by order_id) tq1 on tq1.order_id = o.order_id
                    join (select order_id, sum(quantity) as tot
                    from order_items  
                    group by order_id) tq2 on tq2.order_id = o2.order_id"""

        cursor.execute(query, (numMin, storeId, ))

        res = []
        for row in cursor:
            res.append(Arco(**row))
        cursor.close()
        conn.close()
        return res