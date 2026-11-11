#lector de los archivos para procesar el contenido de los .txt

class Lector:
    def __init__(self):
        self.cursos = {}
        self.franjas = []
        self.salones = []
        self.profesores = {}

        self.estado = {
            "salones":    {"ruta": "", "leido": False, "mensaje": ""},
            "franjas":    {"ruta": "", "leido": False, "mensaje": ""},
            "cursos":     {"ruta": "", "leido": False, "mensaje": ""},
            "profesores": {"ruta": "", "leido": False, "mensaje": ""},
        }
    
    """Lee salones.txt y lo guarda en self.salones.
    Ignora lineas vacías y las que empiezan con #.
    Devuelve True si se leyo bien, False si no."""
    def cargar_salones(self, ruta):
        salones = []
        self.estado["salones"]["ruta"] = ruta
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                for linea in f:
                    linea_limpia = linea.strip()
                    if linea_limpia.startswith("#") or not linea_limpia:
                        continue
                    salones.append(linea_limpia)
        except FileNotFoundError:
            self.salones = []
            self.estado["salones"].update(leido=False, mensaje="No se encontró el archivo")
            return False
        
        self.salones = salones
        self.estado["salones"].update(leido=True, mensaje="Cargado exitosamente")
        return True

    """Lee franjas.txt (DIA FRANJA) y lo guarda en self.franjas como
    lista de tuplas (día, franja). Ignora líneas vacías y comentarios con '#'.
    Devuelve True si se leyó bien, False si no."""
    def cargar_franjas(self, ruta):
        franjas = []
        self.estado["franjas"]["ruta"] = ruta
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                for numero, linea in enumerate(f, start=1):
                    linea_limpia = linea.strip()
                    if linea_limpia.startswith("#") or not linea_limpia:
                        continue
                    campos = [c.strip() for c in linea_limpia.split("\t")]
                    if len(campos) != 2 or not all(campos):
                        self.franjas = []
                        self.estado["franjas"].update(leido=False, mensaje=f"Línea {numero} mal formada: se esperaban 2 campos (día y franja)")
                        return False
                    franjas.append(tuple(campos))
        except FileNotFoundError:
            self.franjas = []
            self.estado["franjas"].update(leido=False, mensaje="No se encontró el archivo")
            return False

        self.franjas = franjas
        self.estado["franjas"].update(leido=True, mensaje="Cargado exitosamente")
        return True

    """ Lee profesores.txt y lo guarda en self.profesores.
    Formato: PROFESOR Dia Franja;Dia Franja (elssegundo campo es opcional).
    Devuelve True si se leyó bien, False si no. """
    def cargar_profesores(self, ruta):
        profesores = {}
        self.estado["profesores"]["ruta"] = ruta
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                for numero, linea in enumerate(f, start=1):
                    linea_limpia = linea.strip()
                    if linea_limpia.startswith("#") or not linea_limpia:
                        continue

                    campos = [c.strip() for c in linea_limpia.split("\t")]
                    if len(campos) > 2 or not campos[0]:
                        self.profesores = {}
                        self.estado["profesores"].update(
                            leido=False,
                            mensaje=f"Línea {numero} mal formada: se esperaba PROFESOR o PROFESOR + no disponibilidad día + franja")
                        return False

                    no_disponibles = []
                    if len(campos) == 2 and campos[1]:
                        for pedazo in campos[1].split(";"):
                            partes = pedazo.split()
                            if len(partes) != 2:
                                self.profesores = {}
                                self.estado["profesores"].update(
                                    leido=False,
                                    mensaje=f"Línea {numero}: '{pedazo.strip()}' debe tener día y franja (ejemplo: Lunes 07-09)")
                                return False
                            no_disponibles.append(tuple(partes))

                    profesores[campos[0]] = no_disponibles
        except FileNotFoundError:
            self.profesores = {}
            self.estado["profesores"].update(leido=False, mensaje="No se encontró el archivo")
            return False

        self.profesores = profesores
        self.estado["profesores"].update(leido=True, mensaje="Cargado exitosamente")
        return True

    """Lee cursos.txt y lo guarda en self.cursos.
            Formato: CURSO PROFESOR GRUPO.
            Devuelve True si se leyó bien, False si no."""
    def cargar_cursos(self, ruta):
        cursos = {}
        self.estado["cursos"]["ruta"] = ruta
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                for numero, linea in enumerate(f, start=1):
                    linea_limpia = linea.strip()
                    if linea_limpia.startswith("#") or not linea_limpia:
                        continue

                    clave_curso, *resto_palabras = linea_limpia.split("\t")
                    clave_curso = clave_curso.strip()
                    resto_palabras = [c.strip() for c in resto_palabras]

                    if len(resto_palabras) != 2 or not clave_curso or not all(resto_palabras):
                        self.cursos = {}
                        self.estado["cursos"].update(
                            leido=False,
                            mensaje=f"Línea {numero} mal formada: se esperaban 3 campos (curso, profesor y grupo)")
                        return False

                    if clave_curso in cursos:
                        self.cursos = {}
                        self.estado["cursos"].update(
                            leido=False,
                            mensaje=f"Línea {numero}: la clase '{clave_curso}' está repetida")
                        return False

                    cursos[clave_curso] = (resto_palabras[0], resto_palabras[1])
        except FileNotFoundError:
            self.cursos = {}
            self.estado["cursos"].update(leido=False, mensaje="No se encontró el archivo")
            return False

        self.cursos = cursos
        self.estado["cursos"].update(leido=True, mensaje="Cargado exitosamente")
        return True

        """Comprueba que los 4 archivos estén leídos y que cada profesor de
        self.cursos exista en self.profesores.
        Devuelve (True, "") si todo es coherente, o (False, mensaje) si no."""
    def validar_datos(self):
        pendientes = [n for n, e in self.estado.items() if not e["leido"]]
        if pendientes:
            return False, "Faltan por leer: " + ", ".join(pendientes)

        for clase, (profesor, grupo) in self.cursos.items():
            if profesor not in self.profesores:
                return False, f"La clase '{clase}' usa al profesor '{profesor}', que no está en profesores.txt"

        return True, ""