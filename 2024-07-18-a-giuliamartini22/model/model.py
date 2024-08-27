import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._listChromosomes = None
        self._graph = nx.DiGraph()
        self.listGenes = []
        self.listEdges = []
        self._idMap = {}
        self.largest_cc = 0


    def buildGraph(self, crMin, crMax):
        self.listGenes = DAO.get_all_genes(crMin, crMax)
        self._graph.add_nodes_from(self.listGenes)
        print(len(self.listGenes))
        print(len(self._graph.nodes))
        for g in self.listGenes:
            self._idMap[(g.GeneID, g.Function)] = g
        #for g in self.listGenes:
        #    self.idMap[g] =
        #self.listEdges = DAO.get_all_edges()
        #for l in self.listEdges:
        #for l in self.listGenes:
        #    if l[0] in self.listGenes and l[1] in self.listGenes:
        #        self._graph.add_edge(l[0], l[1], weight = l[2])

        #print(len(self._graph.edges))
        #for()

        self.listEdges = DAO.getAllConnectedGenes(crMin, crMax)
        for c in self.listEdges:
            codiceGenefunzione1 = (c[0], c[1])
            codiceGenefunzione2 = (c[3], c[4])
            gene1 = self._idMap[codiceGenefunzione1]
            gene2 = self._idMap[codiceGenefunzione2]
            if(c[2] < c[5]):
                self._graph.add_edge(gene1, gene2, weight=c[6])
            elif (c[2] > c[5]):
                self._graph.add_edge(gene2, gene1, weight=c[6])
            elif(c[2] == c[5]):
                self._graph.add_edge(gene1, gene2, weight=c[6])
                self._graph.add_edge(gene2, gene1, weight=c[6])

    def archiUscentiMaggiori(self):
        listaUscenti = []
        listaBest = []
        for g in self.listGenes:
            pesoComplessivo = 0
            numSuccessori = 0
            for uscente in self._graph.successors(g):
                numSuccessori += 1
                pesoComplessivo += self._graph[g][uscente]["weight"]
            listaUscenti.append((g, numSuccessori, pesoComplessivo))
        listaUscenti.sort(key=lambda x: x[1], reverse=True)
        conta = 0
        for g in range(0, len(listaUscenti)):
            if(conta<=4):
                listaBest.append(listaUscenti[g])
                conta = conta + 1
        print(len(listaBest))
        return listaBest

    def archiEntrantiMaggiori(self):
        listaEntranti = []
        listaBest = []
        for g in self.listGenes:
            pesoComplessivo = 0
            numPredecessori = 0
            for entrante in self._graph.predecessors(g):
                numPredecessori += 1
                pesoComplessivo += self._graph[entrante][g]["weight"]
            listaEntranti.append((g, numPredecessori, pesoComplessivo))
        listaEntranti.sort(key=lambda x: x[1], reverse=True)
        conta = 0
        for g in range(0, len(listaEntranti)):
            if conta <= 4:
                listaBest.append(listaEntranti[g])
                conta = conta + 1
        print(len(listaBest))
        return listaBest

    def getComponentiDebolmenteConnesse(self):
        componenti = list(nx.weakly_connected_components(self._graph))
        return componenti

    def getComponentiFortementeConnesse(self):
        componenti = list(nx.strongly_connected_components(self._graph))
        return componenti

    def getChromosomes(self):
        self._listChromosomes = DAO.get_all_chromosomes()
        return self._listChromosomes

    def getNumNodi(self):
        return len(self._graph.nodes)

    def getNumArchi(self):
        return len(self._graph.edges)