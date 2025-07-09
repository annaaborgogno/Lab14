from database.DB_connect import DBConnect
from model.edge import Edge
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
                    from stores s"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Store(**row))
        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getNodes(store):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from orders o
                    where o.store_id = %s"""
        cursor.execute(query, (store, ))

        res = []
        for row in cursor:
            res.append(Order(**row))
        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getEdges(store, numGiorni):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select o1.order_id as o1Id, o2.order_id as o2Id, (tq1.tot + tq2.tot) as peso
                    from orders o1
                    join orders o2 on o1.order_id != o2.order_id
                    and o1.store_id = o2.store_id
                    and o1.store_id = %s
                    and o1.order_date < o2.order_date
                    and datediff(o2.order_date, o1.order_date) < %s
                    join (select order_id, sum(quantity) as tot
                    from order_items 
                    group by order_id) as tq1 on tq1.order_id = o1.order_id 
                    join (select order_id, sum(quantity) as tot
                    from order_items 
                    group by order_id) as tq2 on tq2.order_id = o2.order_id"""
        cursor.execute(query, (store, numGiorni, ))

        res = []
        for row in cursor:
            res.append(Edge(**row))
        cursor.close()
        conn.close()
        return res