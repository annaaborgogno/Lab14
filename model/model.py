import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._stores = []
        self._nodes = []
        self._edges = []
        self._idMap = {}
        self._graph = nx.DiGraph()
        self._bestPath = []
        self._bestWeight = 0

    def getStores(self):
        self._stores = DAO.getStores()
        return self._stores

    def getNodes(self, store):
        self._nodes = DAO.getNodes(store)
        return self._nodes

    def getEdges(self, store, numGiorni):
        self._edges = DAO.getEdges(store, numGiorni)
        return self._edges #tutti gli edges

    def buildGraph(self, store, numGiorni):
        self._graph.clear()
        self._nodes = []
        self._edges = []
        self._idMap = {}
        self.getNodes(store)
        for n in self._nodes:
            self._idMap[n.order_id] = n
        self._graph.add_nodes_from(self._nodes)
        self.addAllEdges(store, numGiorni)
        return self._graph

    def getGraphDetails(self):
        nNodes = self._graph.number_of_nodes()
        nEdges = self._graph.number_of_edges()
        return nNodes, nEdges


    def addAllEdges(self, store, numGiorni):
        self.getEdges(store, numGiorni)
        for e in self._edges:
            if e.o1Id in self._idMap and e.o2Id in self._idMap:
                u = self._idMap[e.o1Id]
                v = self._idMap[e.o2Id]
                self._graph.add_edge(v, u, weight=e.peso)

    def getLongestPath(self, source):
        longest_path = []
        tree = nx.dfs_tree(self._graph, source)
        nodes = list(tree.nodes())
        for node in nodes:
            temp = [node]

            while temp[0] != source:
               pred = nx.predecessor(tree, source, temp[0]) #restituisce una lista di predecessori
               #lungo il cammino da source al nodo target (temp[0]) nel grafo G
               temp.insert(0, pred[0]) #uso pred[0] perché in un albero dfs ogni nodo ha un solo predecessore
               # quindi sto inserendo in posizione 0 il nodo predecessore, perché sto cercando i nodi a ritroso, con append otterrei il cammino al contrario

            if len(temp) > len(longest_path):
                longest_path = copy.deepcopy(temp)

        return longest_path[1:]

#procedura ricorsiva che calcoli un percorso di peso massimo a partire da un nodo sorgente
    def getBestPath(self, source):
        self._bestPath = []
        self._bestWeight = 0
        parziale = [source]
        self._ricorsione(parziale)
        return self._bestPath, self._bestWeight

    def _ricorsione(self, parziale):
        if self._calcolaPeso(parziale) > self._bestWeight:
                self._bestPath = copy.deepcopy(parziale)
                self._bestWeight = self._calcolaPeso(parziale)

        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:
                if len(parziale) == 1:
                    parziale.append(n)
                    self._ricorsione(parziale)
                    parziale.pop()

                elif len(parziale) >= 2 and self._graph[parziale[-1]][n]["weight"]<self._graph[parziale[-2]][parziale[-1]]["weight"]: #peso strettamente decrescente
                        parziale.append(n)
                        self._ricorsione(parziale)
                        parziale.pop()


    def _calcolaPeso(self, listOfNodes):
        pesoTot = 0
        for i in range(1, len(listOfNodes)):
            u = listOfNodes[i - 1]
            v = listOfNodes[i]
            pesoTot += self._graph[u][v]["weight"]
        return pesoTot