import flet as ft
from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._chromosomeMin = None
        self._chromosomeMax = None
        self._listCromosomes = None

    def handle_graph(self, e):
        self._chromosomeMin = self._view.dd_min_ch.value
        self._chromosomeMax = self._view.dd_max_ch.value
        if self._chromosomeMin is None or self._chromosomeMin > self._chromosomeMax:
            self._view.create_alert("Cromosoma nullo o non valido")
            return

        self._model.buildGraph(self._chromosomeMin, self._chromosomeMax)

        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Creato grafo con {self._model.getNumNodi()} vertici e {self._model.getNumArchi()} archi"))
        self._view.txt_result1.controls.append(
            ft.Text(f"Stampa dei 5 geni con il maggior numero di archi uscenti"))
        listaBestUscenti = self._model.archiUscentiMaggiori()
        for vertice in listaBestUscenti:
            self._view.txt_result1.controls.append(ft.Text(f"{vertice[0]} | archi uscenti: {vertice[1]} | peso totale: {vertice[2]}"))
        self._view.update_page()

        # STAMPA I 5 MIGLIORI PREDECESSORI E IL PESO TOTALE
        self._view.txt_result1.controls.append(
            ft.Text(f"Stampa dei 5 geni con il maggior numero di archi entranti"))
        listaBestEntranti = self._model.archiEntrantiMaggiori()
        for vertice in listaBestEntranti:
            self._view.txt_result1.controls.append(
                ft.Text(f"{vertice[0]} | archi entranti: {vertice[1]} | peso totale: {vertice[2]}"))
        self._view.update_page()

        # STAMPA IL NUMERO DI COMPONENTI DEBOLMENTE CONNESSE
        components = self._model.getComponentiDebolmenteConnesse()
        numComponents = len(components)
        self._view.txt_result1.controls.append(
            ft.Text(f"Il grafo ha {numComponents} componenti debolmente connesse"))
        # STAMPA LA COMPONENTE CON IL MAGGIORE NUMERO DI NODI
        largestComponent = max(components, key=len)
        largestSize = len(largestComponent)
        self._view.txt_result1.controls.append(
            ft.Text(f"La componente connessa piu grande è costituita da {largestSize} nodi"))
        self._view.txt_result1.controls.append(ft.Text(f"Nodi della componente debolmente connessa più grande : {largestComponent}"))

        self._view.update_page()

        # STAMPA IL NUMERO DI COMPONENTI FORTEMENTE CONNESSE
        componentsStrong = self._model.getComponentiFortementeConnesse()
        numComponentsStrong = len(componentsStrong)
        self._view.txt_result1.controls.append(
            ft.Text(f"Il grafo ha {numComponentsStrong} componenti FORTEMENTE connesse"))
        # STAMPA LA COMPONENTE CON IL MAGGIORE NUMERO DI NODI
        largestComponentStrong = max(componentsStrong, key=len)
        largestSizeStrong = len(largestComponentStrong)
        self._view.txt_result1.controls.append(
            ft.Text(f"La componente connessa piu grande è costituita da {largestSizeStrong} nodi"))
        self._view.txt_result1.controls.append(
            ft.Text(f"Nodi della componente FORTEMENTE connessa più grande : {largestComponentStrong}"))

        self._view.update_page()

        #STAMPA TUTTE LE COMPONENTI DEBOLMENTE CONNESSE DEL GRAFO
        #for id, component in enumerate(components):
        #    self._view.txt_result1.controls.append(ft.Text(f"Componente {id +1}: {component}"))
        #self._view.update_page()


    def handle_path(self, e):
        pass


    def fillDDCromosome(self):
        self._listCromosomes = self._model.getChromosomes()
        for s in self._listCromosomes:
            self._view.dd_min_ch.options.append(ft.dropdown.Option(s))
            self._view.dd_max_ch.options.append(ft.dropdown.Option(s))
        self._view.update_page()

    def read_chromosome(self, e):
        if e.control.value == "None":
            self._chromo = None
        else:
            self._chromo = e.control.value