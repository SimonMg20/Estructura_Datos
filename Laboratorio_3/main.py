# main.py
import os
import sys
import time

# Importamos los módulos con las nuevas funciones ajustadas
import graficar
import medidor_tiempos


def ejecutar_laboratorio():
    print("=" * 65)
    print("  INICIANDO LABORATORIO: COMPARATIVO DE ESTRUCTURAS DE DATOS")
    print("=" * 65)

    inicio_total = time.time()

    # Paso 1: Ejecutar las mediciones de tiempo (en segundos)
    print("\n[PASO 1/2] Ejecutando benchmarks de rendimiento...")
    medidor_tiempos.ejecutar_experimentos()

    # Paso 2: Generar las gráficas a partir del CSV obtenido
    print("\n[PASO 2/2] Generando gráficas de rendimiento en segundos...")
    graficar.generar_graficas()

    tiempo_total = time.time() - inicio_total

    print("\n" + "=" * 65)
    print(
        f"  ¡EJECUCIÓN COMPLETADA EXITOSAMENTE EN {tiempo_total:.2f} SEGUNDOS!"
    )
    print("  - Datos exportados a: 'resultados_benchmark.csv'")
    print("  - Visualizaciones guardadas en: carpeta 'graficas/'")
    print("=" * 65)


if __name__ == "__main__":
    ejecutar_laboratorio()