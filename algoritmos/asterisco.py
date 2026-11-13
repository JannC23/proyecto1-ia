import time


class aste:
    """Usamos A* Que expande el nodo que la suma de g(n)(costo)
    y de la h(n) heuristica da f(n), expandimos el nodo que menor
    f(n) tiene. Formula que aplica A* f(n) = g(n) + h(n)
"""

    def __init__(self, problema):
        self.problema = problema
        self.nodos_explorados = 0
        self.tiempo = 0.0

    def heuristica(self, nodo):
        """Nos pasa h(n) que es la heuristica del problema,
        la distancia de manhattan"""
        fila, col = nodo.estado
        meta_fila, meta_col = self.problema.meta()
        return abs(fila - meta_fila) + abs(col - meta_col)   

    def _prioridad(self, nodo):
        g = nodo.costo 
        h = self.problema.heuristica(nodo)
        f = g + h  #La funcion principal en la que vamos a basar este algoritmo
        fila,  col = nodo.estado 
        return (f, fila, col)


    def resolver(self):
        """Devuelve el Nodo meta, o None si no hay solución.
        Deja nodos_explorados y tiempo (segundos) como atributos."""
        inicio = time.perf_counter()
        self.nodos_explorados = 0
        solucion = None

        raiz = self.problema.estado_inicial()
        abierta = {raiz.estado: raiz} 
        mejor_g = {raiz.estado: raiz costo}

        while abierta:
            nodo min(abierta.values(), key=self._prioridad)
            del abierta[nodo.estado]

            if self.problema.es_meta(nodo):
                solucion = nodo
                break

            hijos = self.problema.sucesores(nodo)
            self.nodos_explorados += len(hijos)
            for hijo in hijos:
                if hijo.costo < mejor_g.get(hijo.estado, float("inf")):
                    mejor_g[hijo.estado] = hijo.costo
                    abierta[hijo.estado] = hijo  # reemplazar cuando haya un costo mayor

        self.tiempo = time.perf_counter() - inicio
        return solucion