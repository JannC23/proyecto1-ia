import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from controller.controlador import Controlador


class Vista:
    def __init__(self, ventana):
        # Configuramos la ventana principal y conectamos el controlador
        self.ventana = ventana
        self.ventana.title("Programación Académica Universitaria")
        self.ventana.geometry("1000x760")
        self.controlador = Controlador()

        # Guardamos los algoritmos que el usuario puede seleccionar
        self.algoritmos = {
            "Amplitud (BFS)": "amplitud",
            "Profundidad iterativa (DFS)": "profundidad",
            "Costo uniforme (UCS)": "costo",
            "A* (informado)": "asterisco"
        }

        # Creamos el espacio principal donde van los elementos
        principal = tk.Frame(ventana)
        principal.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(principal, text="PROGRAMACION ACADEMICA UNIVERSITARIA",
                font=("Arial", 16, "bold")).pack(pady=9)
        ttk.Separator(principal, orient="horizontal").pack(fill="x", pady=8)

        # Creamos los botones para cargar los archivos y mostrar si se leyeron
        self.rutas = {}
        self.estados = {}
        for tipo in ("profesores", "cursos", "salones", "franjas"):
            fila = tk.Frame(principal)
            fila.pack(fill="x", pady=2)
            tk.Label(fila, text="Cargar " + tipo + ".txt", width=22,
                    anchor="w").pack(side="left")
            tk.Button(fila, text="Examinar", width=12,
                    command=lambda t=tipo: self.cargar_archivo(t)).pack(side="left")
            self.rutas[tipo] = tk.Label(fila, text="ruta: ", width=55, anchor="w")
            self.rutas[tipo].pack(side="left", padx=10)
            self.estados[tipo] = tk.Label(fila, text="Sin cargar")
            self.estados[tipo].pack(side="left")

        ttk.Separator(principal, orient="horizontal").pack(fill="x", pady=9)

        # Creamos la lista de algoritmos y el boton para generar el horario
        fila_algoritmo = tk.Frame(principal)
        fila_algoritmo.pack(fill="x")
        tk.Label(fila_algoritmo, text="Algoritmo:").pack(side="left", padx=(0, 10))
        self.opcion = ttk.Combobox(fila_algoritmo, state="readonly", width=30,
                                values=list(self.algoritmos.keys()))
        self.opcion.set("A* (informado)")
        self.opcion.pack(side="left")
        tk.Button(fila_algoritmo, text="Generar Horario", width=20,
                command=self.generar_horario).pack(side="right")

        ttk.Separator(principal, orient="horizontal").pack(fill="x", pady=9)

        # Dejamos un espacio vacio donde se mostrara el horario generado
        tk.Label(principal, text="HORARIO GENERADO",
                font=("Arial", 13, "bold")).pack(pady=3)
        self.tabla_horario = tk.Frame(principal, height=80)
        self.tabla_horario.pack(fill="x", pady=5)
        self.tabla_horario.pack_propagate(False)

        ttk.Separator(principal, orient="horizontal").pack(fill="x", pady=9)

        # Creamos la parte donde se van a mostrar las estadisticas
        tk.Label(principal, text="ESTADISTICAS",
                font=("Arial", 13, "bold")).pack(pady=3)
        self.tabla_estadisticas = tk.Frame(principal)
        self.tabla_estadisticas.pack(fill="x", pady=5)
        self.mostrar_estadisticas()

    # Abre el explorador de archivos y manda el archivo al controlador
    def cargar_archivo(self, tipo):
        ruta = filedialog.askopenfilename(
            title="Seleccionar " + tipo + ".txt",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        if not ruta:
            return

        # Mostramos la ruta y si el archivo se cargo correctamente
        correcto, mensaje = self.controlador.cargar_archivo(tipo, ruta)
        self.rutas[tipo].config(text="ruta: " + ruta)
        self.estados[tipo].config(text="Leído" if correcto else "Error")
        self.limpiar_horario()
        self.mostrar_estadisticas()
        if not correcto:
            messagebox.showerror("Error", mensaje)

    # Borra el horario anterior para mostrar uno nuevo
    def limpiar_horario(self):
        for elemento in self.tabla_horario.winfo_children():
            elemento.destroy()
        self.tabla_horario.config(height=80)
        self.tabla_horario.pack_propagate(False)

    # Ejecuta el algoritmo seleccionado y muestra los resultados
    def generar_horario(self):
        algoritmo = self.algoritmos[self.opcion.get()]
        correcto, mensaje = self.controlador.resolver(algoritmo)
        self.mostrar_estadisticas()
        self.limpiar_horario()

        # Si ocurre un error o no hay solucion, mostramos un mensaje
        if not correcto:
            messagebox.showerror("Error", mensaje)
            return
        if not self.controlador.get_horario():
            messagebox.showinfo("Resultado", mensaje)
            return

        self.mostrar_horario()

    # Crea la tabla del horario con los dias, horas y materias
    def mostrar_horario(self):
        dias = self.controlador.get_dias()
        horas = self.controlador.get_horas()
        clases = self.controlador.get_horario()
        self.tabla_horario.pack_propagate(True)

        # Colocamos los dias en la parte superior de la tabla
        columnas = [" "] + dias
        for columna, nombre in enumerate(columnas):
            tk.Label(self.tabla_horario, text=nombre, relief="solid", borderwidth=1,
                    font=("Arial", 10, "bold")).grid(
                        row=0, column=columna, sticky="nsew")
            self.tabla_horario.grid_columnconfigure(columna, weight=1)

        # Colocamos las horas y las materias con su profesor y salon
        for fila, hora in enumerate(horas, start=1):
            tk.Label(self.tabla_horario, text=hora, relief="solid",
                    borderwidth=1, width=12).grid(row=fila, column=0, sticky="nsew")
            for columna, dia in enumerate(dias, start=1):
                asignadas = [c for c in clases if c["dia"] == dia and c["franja"] == hora]
                texto = "\n".join(c["clase"] + "\n" + c["profesor"] + "\n" + c["salon"]
                                    for c in asignadas)
                tk.Label(self.tabla_horario, text=texto, relief="solid", borderwidth=1,
                        width=22, height=max(3, len(asignadas) * 3),
                        justify="center").grid(row=fila, column=columna, sticky="nsew")

    # Muestra las estadisticas de los algoritmos que se han ejecutado
    def mostrar_estadisticas(self):
        for elemento in self.tabla_estadisticas.winfo_children():
            elemento.destroy()

        # Creamos los nombres de las columnas
        encabezados = ["Algoritmo", "Nodos", "Tiempo", "Solucion"]
        for columna, titulo in enumerate(encabezados):
            tk.Label(self.tabla_estadisticas, text=titulo, relief="solid", borderwidth=1,
                    font=("Arial", 10, "bold")).grid(row=0, column=columna, sticky="nsew")
            self.tabla_estadisticas.grid_columnconfigure(columna, weight=1)

        # Buscamos los resultados y los colocamos en la tabla
        resultados = {e["algoritmo"]: e for e in self.controlador.get_estadisticas_todas()}
        for fila, nombre in enumerate(("BFS", "DFS", "UCS", "A*"), start=1):
            dato = resultados.get(nombre)
            nodos = "" if not dato or dato["nodos_explorados"] is None else str(dato["nodos_explorados"])
            tiempo = "" if not dato or dato["tiempo_segundos"] is None else str(dato["tiempo_segundos"]) + "s"
            solucion = "" if not dato else ("Error" if dato["error"] else
                                                ("Sí" if dato["solucion_encontrada"] else "No"))
            for columna, valor in enumerate((nombre, nodos, tiempo, solucion)):
                tk.Label(self.tabla_estadisticas, text=valor, relief="solid",
                        borderwidth=1).grid(row=fila, column=columna, sticky="nsew")


# Inicia la ventana cuando ejecutamos este archivo directamente
if __name__ == "__main__":
    ventana = tk.Tk()
    Vista(ventana)
    ventana.mainloop()
