import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self._stores = []
        self._nodes = []
        self._edges = []
        self._graph = nx.DiGraph()
        self._idMap = {}

    def getStores(self):
        self._stores = DAO.getStores()
        return self._stores

    def buildGraph(self, numMin, storeId):
        self._nodes = DAO.getNodes(storeId)
        self._graph.add_nodes_from(self._nodes)
        for n in self._nodes:
            self._idMap[n.order_id] = n
        self.addAllEdges(numMin, storeId)

    def addAllEdges(self, numMin, storeId):
        self._edges = DAO.getEdges(numMin, storeId)
        for e in self._edges:
            if e.order1_id in self._idMap and e.order2_id in self._idMap:
                o1 = self._idMap[e.order1_id]
                o2 = self._idMap[e.order2_id]
                peso = e.qtyOrder
                self._graph.add_edge(o1, o2, weight=peso)