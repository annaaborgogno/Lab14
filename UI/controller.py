import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        pass
    def handleCerca(self, e):
        pass

    def handleRicorsione(self, e):
        pass

    def fillDD(self):
        stores = self._model.getStores()
        for s in stores:
            self._view._ddStore.options.append(data=s, text=s.store_id, on_click=self._readDD)
        self._view.update_page()

    def _readDD(self, e):
        self._selectedStore = e.control.data
        print
