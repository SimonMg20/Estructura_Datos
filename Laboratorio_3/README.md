# Laboratorio 3: Evaluación Experimental de Estructuras de Datos

**Estudiante:** Simón Montoya 


---
### 1. Objetivos del Experimento
* **Medición de Tiempos Exponenciales:** Evaluar experimentalmente el tiempo de ejecución de las operaciones de **Inserción**, **Búsqueda** y **Listado Ordenado** para tamaños de entrada $N \in \{100, 500, 1000, 2500, 5000, 10000\}$.
---
**Validación Teórica vs Experimental:** Contrastar si los tiempos reales se ajustan a las complejidades teóricas esperadas ($O(1)$, $O(\log N)$, $O(N)$, $O(N \log N)$ y $O(N^2)$).

## 2. Entorno Experimental

### 2.1 Hardware
* **Procesador:** 12th Gen Intel(R) Core(TM) i5-12500H @ 2.50 GHz 
* **Memoria RAM:** 16.0 GB DDR4/DDR5 (15.7 GB utilizables)
* **Arquitectura:** Sistema operativo de 64 bits, procesador basado en x64

### 2.2 Software y Librerías
* **Sistema Operativo:** Windows 11 Home / Pro (64 bits).
* **Lenguaje de Programación:** Python 3.13.x
* **Librerías Principales:**
  * `numpy`: Para el cálculo del promedio, desviación estándar y filtrado de *outliers* (IQR).
  * `pandas`: Para la lectura, manipulación y exportación de las tablas de datos CSV.
  * `matplotlib`: Para la generación y exportación de gráficas de alta resolución ($300\text{ DPI}$).
* **Ajuste de Entorno (Límite de Recursión):**

  import sys
  sys.setrecursionlimit(30000)
---
## 3. Metodología Experimental y Diseño de Pruebas

### 3.1 Generación de Datos y Escenarios de Prueba
Para evaluar el desempeño de las estructuras en condiciones reales y de estrés, se generaron registros sintéticos de estudiantes compuestos por un identificador único (`id`), un `nombre` y un `promedio`. Se plantearon dos escenarios de entrada:

* **Escenario Aleatorio (Caso Promedio):** Los registros se insertan en el orden en que son generados al azar. Representa el comportamiento habitual de un sistema donde la información ingresa sin un patrón predefinido.
* **Escenario Ordenado (Peor Caso):** Los datos se ordenan previamente por su `id` antes de ser insertados. Este escenario pone a prueba la resiliencia de las estructuras jerárquicas: mientras que el **Árbol B+** mantiene su balanceo, el **ABB** pierde su forma ramificada y degenera en una lista enlazada ($\mathcal{O}(N^2)$ en inserción).

---
### 3.2 Control del Ruido y Calibración del Tiempo
Para garantizar mediciones estables y representativas, se aplicaron tres mecanismos de calibración:

1. **Escalamiento del Trabajo ($M$ y $K$):** En lugar de medir operaciones aisladas, se ejecutaron bloques masivos de trabajo:
   * **Búsquedas:** Se realizaron $M = 15.000$ consultas aleatorias sobre la estructura.
   * **Listados:** Se iteró el recorrido completo $K = 300$ veces.
   Esto eleva el tiempo acumulado de las operaciones ineficientes por encima de **1.0 segundo**, eliminando el impacto del piso de ruido del procesador.
2. **Cronómetro de Alta Precision:** Se utilizó `time.perf_counter_ns()`, que captura el tiempo a nivel de nanosegundos directamente desde el hardware.
3. **Réplicas e Inspección Estadística (Filtro IQR):** Cada experimento se repitió $5$ veces. Para evitar que interrupciones ajenas al programa (como la recolección de basura de Python o picos de uso de CPU) alteren los resultados.

### 3.3 Tamaños de Entrada ($N$)
Se seleccionaron 6 tamaños de muestra representativos para observar la evolución asintótica de las curvas a medida que el problema escala:
* **Escala Menor:** $N = 100$ y $N = 500$
* **Escala Intermedia:** $N = 1.000$ y $N = 2.500$
* **Escala Masiva:** $N = 5.000$ y $N = 10.000$

---
## 4. Estructura del Proyecto e Instrucciones de Ejecución

### 4.1 Organización de Archivos y Destino de Resultados
Los datos procesados y visualizaciones resultantes se almacenan automáticamente en la raíz del proyecto y en subcarpetas dedicadas:

```text
Laboratorio_3/
├── estructuras.py          # Implementación de Lista, ABB y Árbol B+
├── generador.py            # Generación sintética de registros de estudiantes
├── medidor_tiempos.py      # Script del benchmark (Genera los CSVs)
├── graficar.py             # Generador de gráficas a partir de los CSVs
├── main.py                 # Orquestador del flujo completo
│
├── [Ruta de Salida Datos]
├── resultados_insercion.csv# Datos de tiempos para Inserción
├── resultados_busqueda.csv # Datos de tiempos para Búsqueda
├── resultados_listado.csv  # Datos de tiempos para Listado Ordenado
│
└── [Ruta de Salida Imágenes]
    └── graficas/           
        ├── lineal/         # Visualizaciones en escala lineal tradicional
        └── loglog/         # Visualizaciones en escala logarítmica (Log-Log)
```
---
## 5. Análisis de Resultados y Conclusiones

1. **Degeneración del ABB en el Peor Caso:**
   * Al recibir datos en orden estricto (Escenario Ordenado), el ABB no puede balancearse y se convierte en una estructura lineal (equivalente a una lista enlazada).
   * Esto provoca que el tiempo de inserción pase de ser eficiente a tener un comportamiento cuadrático $\mathcal{O}(N^2)$, aumentando drásticamente el tiempo de ejecución para $N = 10.000$. En el escenario aleatorio, al mantenerse balanceado, su tiempo es logarítmico $\mathcal{O}(\log N)$.

2. **Estabilidad y Alta Eficiencia del Árbol B+:**
   * El Árbol B+ mantiene su estructura balanceada independientemente de si los datos entran ordenados o desordenados, garantizando un tiempo de búsqueda e inserción siempre bajo ($\mathcal{O}(\log N)$).
   * Gracias a que sus hojas están enlazadas secuencialmente, la operación de **listado ordenado** es sumamente rápida, ya que no requiere recorrer el árbol de arriba a abajo repetidamente.

3. **Incapacidad de la Lista Secuencial para Búsquedas Masivas:**
   * Insertar en una lista es muy rápido, pero buscar requiere inspeccionar elemento por elemento ($\mathcal{O}(N)$).
   * Al someter la lista a $15.000$ búsquedas ($M=15.000$), el tiempo de procesamiento se dispara de forma lineal respecto a $N$, demostrando que no es una estructura viable para sistemas con altas consultas.

4. **Justificación de las Gráficas (Lineal vs. Log-Log):**
   * **Escala Lineal:** Muestra el impacto real en segundos y permite identificar cuándo una estructura supera el umbral de $1.0\text{ segundo}$. Sin embargo, aplasta visualmente a las estructuras extremadamente rápidas contra el eje cero.
   * **Escala Log-Log:** Elimina la compresión de datos y permite observar la tendencia y pendiente real de crecimiento de todas las estructuras (incluyendo las más rápidas como el Árbol B+) en una sola vista.



## 6. Declaración de Integridad Académica y Código de Honor
 Uso del modelo de Inteligencia Artificial **Gemini (Google)** como herramienta de soporte interactivo durante las siguientes fases del proyecto:

* **Soporte y Rol de la IA:** 
  * Asistencia en el diseño y refactorización de scripts de benchmarking (`medidor_tiempos.py` y `graficar.py`) para asegurar la captura de métricas precisas y filtrado estadístico mediante IQR.
  * Optimización de la maquetación y legibilidad de las gráficas (ajuste de escalas, tipografía, y visualización Log-Log).
  * Estructuración del documento `README.md`
