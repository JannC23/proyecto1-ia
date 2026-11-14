import importlib
import os

from model.lector import Lector
from model.problema import Problema


class Controlador:
    # clave: (nombre, modulo, posibles nombres de la clase)
    ALGORITMOS = {
        "amplitud": ("BFS", "algoritmos.amplitud", ["Amplitud"]),
        "profundidad": ("DFS", "algoritmos.profundidadIte", ["ProfundidadIterativa"]),
        "costo": ("UCS", "algoritmos.costo", ["CostoUniforme"]),
        "asterisco": ("A*", "algoritmos.asterisco", ["AEstrella"]),
    }
    ARCHIVOS = {
        "profesores": "cargar_profesores",
        "cursos": "cargar_cursos",
        "salones": "cargar_salones",
        "franjas": "cargar_franjas",
    }
    DIAS = ["lunes", "martes", "miercoles", "miércoles", "jueves", "viernes", "sabado", "sábado"]

    def __init__(self):
        self.lector = Lector()
        self.problema = None
        self.historial = {}     # estadisticas de cada algoritmo
        self.soluciones = {}    # nodo meta de cada algoritmo
        self.ultimo = None

    def get_algoritmos(self):
        return {k: v[0] for k, v in self.ALGORITMOS.items()}

    # carga un archivo, devuelve (ok, mensaje) para el indicador de la vista
    def cargar_archivo(self, tipo, ruta):
        if tipo not in self.ARCHIVOS:
            return False, "Tipo de archivo no válido"

        # si cambian los datos, lo anterior ya no sirve
        self.problema = None
        self.historial.clear()
        self.soluciones.clear()
        self.ultimo = None

        try:
            ok = getattr(self.lector, self.ARCHIVOS[tipo])(ruta)
        except Exception as e:
            # el lector solo atrapa FileNotFoundError
            ok = False
            self.lector.estado[tipo].update(leido=False, mensaje=f"No se pudo leer: {e}")
        return ok, self.lector.estado[tipo]["mensaje"]

    def get_estado_archivos(self):
        return self.lector.estado

    # carga los 4 archivos de la carpeta archivos/ (para consola y main.py)
    def cargar_datos(self, carpeta=None):
        if carpeta is None:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            carpeta = os.path.join(base, "archivos")
        for tipo in self.ARCHIVOS:
            ok, msg = self.cargar_archivo(tipo, os.path.join(carpeta, tipo + ".txt"))
            if not ok:
                return False, f"{tipo}: {msg}"
        return self.crear_problema()

    # carga, resuelve e imprime el horario por consola
    def ejecutar(self, algoritmo="amplitud"):
        ok, msg = self.cargar_datos()
        if ok:
            ok, msg = self.resolver(algoritmo)
        print(msg)
        if ok:
            print(self.get_estadisticas())
            for h in self.get_horario():
                print(h)
        return ok

    def crear_problema(self):
        ok, msg = self.lector.validar_datos()
        if not ok:
            return False, msg
        self.problema = Problema(self.lector.cursos, self.lector.franjas,
                                 self.lector.salones, self.lector.profesores)
        return True, ""

    def resolver(self, algoritmo):
        if algoritmo not in self.ALGORITMOS:
            return False, "Algoritmo no válido"
        if self.problema is None:
            ok, msg = self.crear_problema()
            if not ok:
                return False, msg

        nombre, modulo, clases = self.ALGORITMOS[algoritmo]
        est = {"algoritmo": nombre, "nodos_explorados": None,
               "tiempo_segundos": None, "solucion_encontrada": False, "error": ""}
        self.ultimo = algoritmo
        self.historial[algoritmo] = est
        self.soluciones[algoritmo] = None

        try:
            # se importa aqui para que un algoritmo roto no tumbe los demas
            mod = importlib.import_module(modulo)
            clase = next((getattr(mod, c) for c in clases if hasattr(mod, c)), None)
            if clase is None:
                raise AttributeError(f"{modulo} no tiene la clase {clases[0]}")
            buscador = clase(self.problema)

            solucion = buscador.resolver()
            est["tiempo_segundos"] = round(buscador.tiempo, 4)
            est["nodos_explorados"] = getattr(buscador, "nodos_explorados", None)
        except Exception as e:
            est["error"] = f"{nombre} falló: {type(e).__name__}: {e}"
            return False, est["error"]

        if solucion is not None:
            est["solucion_encontrada"] = True
            self.soluciones[algoritmo] = solucion
            return True, f"{nombre}: solución encontrada"
        return True, f"{nombre}: no hay solución"

    # estadisticas del ultimo algoritmo
    def get_estadisticas(self):
        return self.historial.get(self.ultimo, {})

    # tabla comparativa con todos los que ya se corrieron
    def get_estadisticas_todas(self):
        return [self.historial[k] for k in self.ALGORITMOS if k in self.historial]

    # lista de clases asignadas, ordenada por dia y franja
    def get_horario(self, algoritmo=None):
        solucion = self.soluciones.get(algoritmo or self.ultimo)
        if solucion is None:
            return []
        horario = []
        for clase, (dia, franja, salon) in solucion.estado.items():
            profesor, grupo = self.problema.cursos[clase]
            horario.append({"clase": clase, "dia": dia, "franja": franja,
                            "salon": salon, "profesor": profesor, "grupo": grupo})
        horario.sort(key=lambda h: (self._orden_dia(h["dia"]), h["franja"], h["salon"]))
        return horario

    # dias (columnas) y horas (filas) de la grilla, horas en el orden del archivo
    def get_dias(self):
        dias = list(dict.fromkeys(d for d, _ in self.lector.franjas))
        return sorted(dias, key=self._orden_dia)

    def get_horas(self):
        return list(dict.fromkeys(f for _, f in self.lector.franjas))

    def _orden_dia(self, dia):
        d = dia.lower()
        return self.DIAS.index(d) if d in self.DIAS else 99


if __name__ == "__main__":
    # prueba rapida por consola: python3 -m controller.controlador amplitud
    import sys
    Controlador().ejecutar(sys.argv[1] if len(sys.argv) > 1 else "amplitud")