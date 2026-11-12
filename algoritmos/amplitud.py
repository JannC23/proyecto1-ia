from collections import deque
import time


class Amplitud:
    """Búsqueda en amplitud (BFS). problema debe tener estado_inicial(),
    es_meta(nodo) y sucesores(nodo)."""

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

        cola = deque([self.problema.estado_inicial()])
        while cola:
            nodo = cola.popleft()
            if self.problema.es_meta(nodo):
                solucion = nodo
                break
            hijos = self.problema.sucesores(nodo)
            self.nodos_explorados += len(hijos)
            cola.extend(hijos)

        self.tiempo = time.perf_counter() - inicio
        return solucion