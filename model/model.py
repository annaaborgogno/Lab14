import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self._stores = []
        self._nodes = []
        self._graph = nx.DiGraph()

    def getStores(self):
        self._stores = DAO.getStores()
        return self._stores

    def buildGraph(self, storeId):
        self._nodes = DAO.getNodes(storeId)
        self._graph.add_nodes_from(self._nodes)
