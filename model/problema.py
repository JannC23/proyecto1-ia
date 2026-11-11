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

    def sucesores(self, nodo):
        hijos = []
        for i in self.cursos:
            if i not in nodo.estado:
                clase = i
                break
        
            
        
        return hijos