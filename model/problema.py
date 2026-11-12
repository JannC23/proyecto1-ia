from model.nodo import Nodo

class Problema:
    def __init__(self, cursos, franjas, salones, profesores):
        self.cursos = cursos
        self.franjas = franjas
        self.salones = salones
        self.profesores = profesores

    def estado_inicial(self):
        return Nodo({})

    def es_meta(self, nodo):
        return True if len(nodo.estado) == len(self.cursos) else False

    """Devuelve True si asignar 'clase' a (franja, salon) choca con alguna
    asignación ya hecha en nodo.estado (mismo día y franja, y mismo salón,
    profesor o grupo)."""
    def choca(self, nodo, clase, franja, salon):
        profesor, grupo = self.cursos[clase]
        for clase_asignada, (dia_asignado, franja_asignada, salon_asignado) in nodo.estado.items():
            if (dia_asignado, franja_asignada) != franja:
                continue
            profesor_asignado, grupo_asignado = self.cursos[clase_asignada]
            if (salon_asignado == salon or profesor_asignado == profesor
                    or grupo_asignado == grupo):
                return True
        return False

    """Devuelve la lista de nodos hijos válidos de 'nodo'."""
    def sucesores(self, nodo):
        hijos = []
        for i in self.cursos:
            if i not in nodo.estado:
                clase = i
                break
        for franja in self.franjas:
            for salon in self.salones:
                if not self.choca(nodo, clase, franja, salon):
                    nuevo_estado = dict(nodo.estado)
                    nuevo_estado[clase] = (franja[0], franja[1], salon)
                    hijos.append(Nodo(nuevo_estado, padre=nodo,
                                    costo=nodo.costo + 1,
                                    accion=(clase, franja[0], franja[1], salon)))
        return hijos