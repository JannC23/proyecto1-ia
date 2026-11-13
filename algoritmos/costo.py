import time 
import itertools
import time

class costo:
    """Busqueda por costo uniforme, va expandiendo el nodo con 
    menor costo, hasta llegar a la meta, sin antes expandir los
    nodos con igual costo que la meta"""

    def __init__(self, problema):
        self.problema = problema
        self.nodos_explorados = 0
        self.tiempo = 0.0

    def resolver(self):
        """Devuelve el Nodo meta, o None si no hay solución.
        Deja nodos_explorados y tiempo (segundos) como atributos."""

        inicio = time.perf_counter()
        self.nodos_explorados = 0
        solucion = None

        
        contador = itertools.count()  # desempate para heapq
        raiz = self.problema.estado_inicial()
        abierta = [(raiz.costo, next(contador), raiz)]
        mejor_g = {raiz.estado: raiz.costo}
        cerrada = set()

        while abierta:
            _, _, nodo = heapq.heappop(abierta)
            if nodo.estado in cerrada:
                continue  # entrada obsoleta (lazy deletion)
            if self.problema.es_meta(nodo):
                solucion = nodo
                break
            cerrada.add(nodo.estado)

            hijos = self.problema.sucesores(nodo)
            self.nodos_explorados += len(hijos)
            for hijo in hijos:
                if hijo.costo < mejor_g.get(hijo.estado, float("inf")):
                    mejor_g[hijo.estado] = hijo.costo
                    heapq.heappush(abierta, (hijo.costo, next(contador), hijo))

        self.tiempo = time.perf_counter() - inicio
        return solucion