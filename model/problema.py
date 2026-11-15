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
    # Verifica que no haya otra materia en el mismo dia y hora
    def choca(self, nodo, clase, franja, salon):
        profesor, grupo = self.cursos[clase]

        for clase_asignada, (dia_asignado, franja_asignada, salon_asignado) in nodo.estado.items():

            # Solo revisamos las clases del mismo dia y hora
            if (dia_asignado, franja_asignada) != franja:
                continue

            profesor_asignado, grupo_asignado = self.cursos[clase_asignada]

            # Un salon no puede tener dos clases a la vez
            if salon_asignado == salon:
                return True

            # Un profesor no puede dictar dos clases a la vez
            if profesor_asignado == profesor:
                return True

            # Un grupo no puede tener dos clases a la vez
            if grupo_asignado == grupo:
                return True

            # No permitir dos materias en el mismo dia y hora
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