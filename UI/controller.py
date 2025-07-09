import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._selectedStore = None
        self._selectedOrder = None

    def handleCreaGrafo(self, e):
        store = self._selectedStore.store_id
        if store is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Selezionare uno store", color="red"))
            self._view.updat_page()
            return

        numInput = self._view._txtIntK.value

        if numInput == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un numero di giorni",  color="red"))
            return

        try:
            numGiorni = int(numInput)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un numero intero", color="red"))
            return
        self._model.buildGraph(store, numGiorni)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato", color="green"))
        self._view._ddNode.options.clear()
        for n in self._model._graph.nodes:
            self._view._ddNode.options.append(ft.dropdown.Option(data=n, text=n.order_id, on_click=self._getSelectedOrder))
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodes}, numero di archi {nEdges}"))
        self._view.update_page()

    def handleCerca(self, e):
        source = self._selectedOrder
        if source is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Selezionare un order id", color="red"))
            self._view.update_page()
            return
        lp = self._model.getLongestPath(source)
        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza: {source}, nodi seguenti:"))
        for n in lp:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()

    def handleRicorsione(self, e):
        source = self._selectedOrder
        if source is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Selezionare un order id", color="red"))
            self._view.update_page()
            return
        bestPath, bestWeight = self._model.getBestPath(source)
        self._view.txt_result.controls.append(ft.Text(f"Il cammino migliore è stato trovato, con peso {bestWeight}", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"I nodi che lo compongono sono:"))
        for n in bestPath:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()

    def fillDDStores(self):
        stores = self._model.getStores()
        for store in stores:
            self._view._ddStore.options.append(ft.dropdown.Option(data=store, text=store.store_id, on_click=self._getSelectedStore))
        self._view.update_page()

    def _getSelectedStore(self, e):
        if e.control.data is None:
            self._selectedStore = None
        else:
            self._selectedStore = e.control.data
            print(f"Store called: {self._selectedStore}")
        return self._selectedStore

    def _getSelectedOrder(self, e):
        if e.control.data is None:
            self._selectedOrder = None
        else:
            self._selectedOrder = e.control.data
            print(f"Order called: {self._selectedOrder}")
        return self._selectedOrder