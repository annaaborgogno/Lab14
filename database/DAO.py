from database.DB_connect import DBConnect
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