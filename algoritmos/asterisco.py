import time


class AEstrella:
    """Usamos A* Que expande el nodo que la suma de g(n)(costo)
    y de la h(n) heuristica da f(n), expandimos el nodo que menor
    f(n) tiene. Formula que aplica A* f(n) = g(n) + h(n)
"""

    def __init__(self, problema):
        self.problema = problema
        self.nodos_explorados = 0  # Cuenta los nodos generados durante la búsqueda.
        self.tiempo = 0.0  # Guarda el tiempo total que tarda resolver().

    def _clave(self, estado):
        # El estado es un diccionario, que no es hashable: se convierte a tupla.
        # Si algún valor es una lista o un diccionario, hay que convertirlo también.
        return tuple(sorted(estado.items()))    

    def heuristica(self, nodo):
        """Nos pasa h(n) que es la heuristica del problema,
        la distancia de manhattan."""
        # Estima cuánto falta para llegar a la meta usando distancia Manhattan.
        pendiente = len(self.problema.clases) - len(nodo.estado)
        return pendiente * 1 

  

    def _prioridad(self, nodo):
        # A* ordena por costo acumulado más estimación restante; fila y columna desempatan.
        g = nodo.costo  # costo acumulado desde el principio  
        h = self.problema.heuristica(nodo) #Estimado de la supesta distancia hasta la meta
        return g + h # f(n) = g(n) + h(n)


    def resolver(self):
        """Devuelve el Nodo meta, o None si no hay solución.
        Deja nodos_explorados y tiempo (segundos) como atributos."""
        inicio = time.perf_counter()
        self.nodos_explorados = 0
        solucion = None

        raiz = self.problema.estado_inicial()
        abierta = {self._clave(raiz.estado): raiz}  #un solo nodo para el estado
        mejor_g = {raiz._clave(raiz.estado): raiz.costo} #El mejor g que se cono por estado

        while abierta:
            # Se elige de la frontera el nodo con menor prioridad A*.
            nodo = min(abierta.values(), key=self._prioridad)
            del abierta[self._clave(nodo.estado)]  # lo sacamos de la frontera

            if self.problema.es_meta(nodo):
                solucion = nodo
                break

            # Genera estados alcanzables y conserva solo los que mejoran su costo.
            hijos = self.problema.sucesores(nodo)
            self.nodos_explorados += len(hijos)
            for hijo in hijos:
                k = self._clave(hijo.estado)
                if hijo.costo < mejor_g.get(k, float("inf")):
                    mejor_g[k] = hijo.costo
                    abierta[k] = hijo  # reemplazar cuando haya un costo mayor

        self.tiempo = time.perf_counter() - inicio
        return solucion