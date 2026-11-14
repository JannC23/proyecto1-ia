import time 


class CostoUniforme:
    """Busqueda por costo uniforme, va expandiendo el nodo con 
    menor costo, hasta llegar a la meta, sin antes expandir los
    nodos con igual costo que la meta"""

    def __init__(self, problema):
        self.problema = problema
        self.nodos_explorados = 0
        self.tiempo = 0.0

    def _clave(self, estado):
        return tuple(sorted(estado.items())) #la clave es para que esta tupla sea hashable y se pueda usar como clave en un diccionario

    def _prioridad(self,nodo):  #Para poder desempatar
        return nodo.costo

    def resolver(self):
        """Devuelve el Nodo meta, o None si no hay solución.
        Deja nodos_explorados y tiempo (segundos) como atributos."""

        inicio = time.perf_counter()
        self.nodos_explorados = 0
        solucion = None

        raiz = self.problema.estado_inicial()
        abierta = {self._clave(raiz.estado): raiz}  #Un solo nodo por estado
        mejor_g = {self._clave(raiz.estado): raiz.costo}


        while abierta:
            nodo = min(abierta.values(), key=self._prioridad)  #Saca el nodo minimo
            del abierta[self._clave(nodo.estado)] 

            if self.problema.es_meta(nodo): #si es meta, guarda esta slucion y rompe el while
                solucion = nodo
                break
            

            hijos = self.problema.sucesores(nodo)   #Hijos del nodo actual
            self.nodos_explorados += len(hijos)  #Expande los hijos y aumenta el contador de nodos explorados
            for hijo in hijos:
                k = self._clave(hijo.estado)
                if hijo.costo < mejor_g.get(k, float("inf")):
                    mejor_g[k] = hijo.costo
                    abierta[k] = hijo  #Remplazamos si ya tenia mayor costo

        self.tiempo = time.perf_counter() - inicio
        return solucion