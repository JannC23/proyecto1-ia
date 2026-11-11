#definicion del nodo que tendra cada arbol de cada algoritmo. Es la base de todo
#se define el estado que es el diccionario de asignaciones hechas hasta el nodo actual
#padre es el nodo más arrina del nodo actual, empieza en None, porque la raiz no tiene padre
#costo el costo de movimiento que tendrá cada nodo, como hay algoritmos como amplitud que no usan costo, simplemente será 0
#accion es la ultima asignación de clase que se hizo desde el padre
#profundidad: el arbol tendra profundidad para conocer el camino de origen

class Nodo:
    def __init__(self, estado, padre=None, costo=0, accion=None):
        self.estado = estado
        self.padre = padre
        self.costo = costo
        self.profundidad = (padre.profundidad + 1) if padre is not None else 0
        self.accion = accion
        