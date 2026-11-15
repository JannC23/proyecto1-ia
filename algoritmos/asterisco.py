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
        """Esto nos ayuda a saber cuanto falta para llegar a la meta.
        si no tneemos combinacion valida el nodo no se completaria asi que infito podria ser admisible"""
      
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



    def _prioridad(self, nodo):
        # A* ordena por costo acumulado más estimación restante; fila y columna desempatan.
        g = nodo.costo  # costo acumulado desde el principio  
        h = self.heuristica(nodo) #Estimado de la supesta distancia hasta la meta
        return (g + h, -nodo.profundidad)  # desempata por profundidad 


    def resolver(self):
        """Devuelve el Nodo meta, o None si no hay solución.
        Deja nodos_explorados y tiempo (segundos) como atributos."""
        inicio = time.perf_counter()
        self.nodos_explorados = 0
        solucion = None

        raiz = self.problema.estado_inicial()
        mejor_g = {self._clave(raiz.estado): raiz.costo} #El mejor g que se cono por estado
        abierta = {}
        p_raiz = self._prioridad(raiz)
        if p_raiz[0] !=float("inf"):        #La priorirda se calcularioa una vez solo si insertamos
            abierta[self._clave(raiz.estado)] = (p_raiz, raiz)       
        

        while abierta:
            # Se elige de la frontera el nodo con menor prioridad A*.
            k_min = min(abierta, key=lambda k: abierta[k][0])
            nodo = abierta.pop(k_min)[1]  # Se saca de la frontera


            if self.problema.es_meta(nodo):
                solucion = nodo
                break

            # Genera estados alcanzables y conserva solo los que mejoran su costo.
            hijos = self.problema.sucesores(nodo)
            self.nodos_explorados += len(hijos)
            for hijo in hijos:
                k = self._clave(hijo.estado)

                if hijo.costo < mejor_g.get(k, float("inf")):
                    p = self._prioridad(hijo)
                    if p[0] == float("inf"):  # No se llega a la meta en este nodo, no se agrega a la frontera.
                        continue # no hay salida, entonces lo ignoramos
                    mejor_g[k] = hijo.costo
                    abierta[k] = (p, hijo)  # reemplazar cuando haya un costo mayor

        self.tiempo = time.perf_counter() - inicio
        return solucion
