import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        storeId = int(self._view._ddStore.value)
        if storeId is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare uno store!", color="red"))

        self._model.buildGraph(storeId)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato!"))
    def handleCerca(self, e):
        pass

    def handleRicorsione(self, e):
        pass

    def fillDD(self):
        stores = self._model.getStores()
        for s in stores:
            self._view._ddStore.options.append(ft.dropdown.Option(data=s, text=s.store_id, on_click=self._readDD))
        self._view.update_page()

    def _readDD(self, e):
        if e.control.data is None:
            self._selectedStore = None
        else:
            self._selectedStore = e.control.data
            print(f"readDD called: {self._selectedStore}")