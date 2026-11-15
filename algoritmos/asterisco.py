import time
import heapq


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
        """Esto estima cuando puede faltar para llegar a la meta. 
         Si alguna clase pentiende ya no tiene Ninguna combinacion valida
          el nodo no se podria completar, asi que devolver infito podria seguir siendo admisible y permintiendonos asi descartarlo """
        pendientes = [c for c in self.problema.cursos if c not in nodo.estado]
        for clase in pendientes:
            tiene_opcion = False
            for franja in self.problema.franjas:
                for salon in self.problema.salones:
                    if not self.problema.choca(nodo, clase, franja, salon):
                        tiene_opcion = True
                        break
                if tiene_opcion:
                    break
            if not tiene_opcion:
                return float("inf")
        return len(pendientes)

  

    

    def resolver(self):
        """Devuelve el Nodo meta, o None si no hay solución.
        Deja nodos_explorados y tiempo (segundos) como atributos."""
        inicio = time.perf_counter()
        self.nodos_explorados = 0
        solucion = None

        raiz = self.problema.estado_inicial()
        mejor_g = {self._clave(raiz.estado): raiz.costo}  # Este seria el mejor g encontrado para cada estado.
        abierta = [] #Frontera es una sola cola de prioridad usando la libreria de heapq
        orden = 0 #Este seria el contador para desempatar sin comparar nodos

        h_raiz = self.heuristica(raiz)
        if h_raiz != float("inf"):
            heapq.heappush(abierta, (raiz.costo + h_raiz, -raiz.profundidad, orden, raiz))
            orden += 1

        while abierta:
            # Se elige de la frontera el nodo con menor prioridad A*.
            nodo = heapq.heappop(abierta)[-1]  # Se obtiene el nodo de la tupla (f(n), -profundidad, orden, nodo)

            if self.problema.es_meta(nodo):
                solucion = nodo
                break

            # Genera estados alcanzables y conserva solo los que mejoran su costo.
            hijos = self.problema.sucesores(nodo)
            self.nodos_explorados += len(hijos)
            for hijo in hijos:
                k = self._clave(hijo.estado)
                if hijo.costo < mejor_g.get(k, float("inf")):
                    if self.heurisica(hijo) == float("inf"):
                        continue  # No hay combinacion valida para este nodo entonces lo ignoramos con el conitnue
                    mejor_g[k] = hijo.costo
                    heapq.heappush(abierta, (hijo.costo + self.heuristica(hijo), -hijo.profundidad, orden, hijo))
                    orden += 1

        self.tiempo = time.perf_counter() - inicio
        return solucion