from database.DAO import DAO

class Model:
    def __init__(self):
        self._stores = []

    def getStores(self):
        self._stores = DAO.getStores()