# Sistema de Asignación de Horarios Universitarios

## Descripción del problema

Una universidad necesita construir el horario académico de un semestre. Para ello debe asignar a cada clase una franja horaria y un salón, garantizando que no se presenten conflictos entre las restricciones del sistema.

Este problema pertenece a la familia de los **Problemas de Satisfacción de Restricciones (CSP)** y puede resolverse mediante técnicas de búsqueda en espacios de estados. El objetivo del proyecto es implementar y comparar estas 4 estrategias:

- **Búsqueda no informada:** amplitud, costo y profundidad iterativa
- **Búsqueda informada:** A*

## Definición formal del problema

**Variables:** cada clase que debe ser programada.

**Dominio de cada variable:** conjunto de combinaciones posibles (día, franja_horaria, salón).

### Restricciones duras (no pueden violarse)

- Un salón no puede tener dos clases en la misma franja horaria.
- Un profesor no puede dictar dos clases en la misma franja horaria.
- Un grupo de estudiantes no puede tener dos clases en la misma franja horaria.
- Cada clase debe asignarse exactamente una vez.

### Restricciones blandas (deseables pero no obligatorias, para quienes quieran ir más allá)

- Un profesor no tiene clases en franjas que marcó como no disponibles.
- Los grupos no tienen más de N clases consecutivas.

## Interfaz

1. **Panel de carga de archivos:** el usuario debe poder seleccionar cada archivo `.txt` desde un botón "Examinar". Debe mostrarse la ruta del archivo cargado y un indicador de si fue leído correctamente.
2. **Panel de configuración:** un menú desplegable (OptionMenu o Combobox) para seleccionar el algoritmo que quiere correr.
3. **Botón "Generar Horario":** al presionar, ejecuta el algoritmo seleccionado y actualiza los paneles de resultados.
4. **Tabla de horario (resultado principal):** mostrar el horario como una grilla visual donde:
   - Las filas son las franjas horarias.
   - Las columnas son los días.
   - Cada celda ocupada muestra: materia, profesor y salón.
   - Las celdas libres quedan en blanco o en gris.
5. **Panel de estadísticas:** una tabla comparativa con nodos explorados, tiempo y si encontró solución, para cada algoritmo.

### Boceto de la interfaz

```
+----------------------------------------------------------+
| PROGRAMACION ACADEMICA UNIVERSITARIA                     |
+----------------------------------------------------------+
| [Cargar profesores.txt] ruta: /archivos/profesores.txt   |
| [Cargar cursos.txt    ] ruta: /archivos/cursos.txt       |
| [Cargar salones.txt   ] ruta: /archivos/salones.txt      |
| [Cargar franjas.txt   ] ruta: /archivos/franjas.txt      |
+----------------------------------------------------------+
| Algoritmo: [ A* (informado) v ]    [Generar Horario]     |
+----------------------------------------------------------+
| HORARIO GENERADO                                         |
|       | Lunes     | Martes | Miercoles |                 |
| 07-09 | Calculo   | ---    | ---       |                 |
|       | Prof_A    |        |           |                 |
|       | Salon_101 |        |           |                 |
| 09-11 | Algebra   | ---    | ---       |                 |
|       | Prof_A    |        |           |                 |
|       | Salon_101 |        |           |                 |
+----------------------------------------------------------+
| ESTADISTICAS      Nodos    Tiempo    Solucion            |
| BFS               52       0.012s    Si                  |
| DFS               31       0.008s    Si                  |
| A*                14       0.003s    Si                  |
+----------------------------------------------------------+
```

## Restricciones de implementación

- Lenguaje permitido: **Python**.
- No se permite usar bibliotecas externas. Los algoritmos deben implementarse desde cero.
- El código debe estar documentado y estructurado en clases o módulos separados.

## Entregables

- **Informe:** representación del estado, espacio de búsqueda, heurísticas escogidas, justificación, pruebas y análisis, todo lo que considere pertinente.
- **Código fuente funcional.**

## Criterios de calificación

| Criterio | Peso |
|---|---|
| Implementación de algoritmos de búsqueda | 70% |
| Interfaz gráfica | 20% |
| Informe | 10% |

## Aclaraciones

- La detección de uso de IA generativa en cualquiera de los 3 ítems mencionados corresponderá a la anulación del proyecto, dependiendo del tamaño del uso.
- La nota es individual. El proyecto puede ser 5 en la revisión grupal, pero su nota depende de la sustentación de carácter individual que se hará. No es válido decir "yo no hice esta parte": es su obligación entender y ser capaz de responder cualquier pregunta o cambio que se pida al momento de la sustentación. Dependiendo de qué tan mal conteste o simplemente no conteste, puede repercutir en la pérdida total de esta nota (hasta 0 puede ser su nota).
- Debe estar listo para responder cualquier pregunta, ya sea teórica, de por qué tomaron una decisión, o de qué hace determinado fragmento o línea de código.
