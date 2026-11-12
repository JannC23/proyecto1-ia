import time


class ProfundidadIterativa:
    """Búsqueda en profundidad iterativa. Repite una búsqueda en
    profundidad con límite 0, 1, 2, ... hasta encontrar meta."""

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

        # Cada nivel asigna una clase, así que la meta está a profundidad len(cursos)
        limite_max = len(self.problema.cursos)
        for limite in range(limite_max + 1):
            solucion = self._buscar_con_limite(limite)
            if solucion is not None:
                break

        self.tiempo = time.perf_counter() - inicio
        return solucion

    def _buscar_con_limite(self, limite):
        """Búsqueda en profundidad (pila) sin expandir nodos en el límite."""
        pila = [self.problema.estado_inicial()]
        while pila:
            nodo = pila.pop()
            if self.problema.es_meta(nodo):
                return nodo
            if nodo.profundidad < limite:
                hijos = self.problema.sucesores(nodo)
                self.nodos_explorados += len(hijos)
                pila.extend(hijos)
        return None