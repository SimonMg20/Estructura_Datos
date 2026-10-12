import csv
import os
import random
import sys
import time
from estructuras import ABB, ArbolBPlus, EstructuraLista
from generador_aleat import generar_estudiantes
import numpy as np

sys.setrecursionlimit(30000)


def calcular_metricas(tiempos):
    if not tiempos or len(tiempos) == 0:
        return 0.0, 0.0
    arr = np.array(tiempos)
    q25, q75 = np.percentile(arr, [25, 75])
    iqr = q75 - q25
    limite_inferior = q25 - 1.5 * iqr
    limite_superior = q75 + 1.5 * iqr
    tiempos_filtrados = arr[
        (arr >= limite_inferior) & (arr <= limite_superior)
    ]
    if len(tiempos_filtrados) == 0:
        tiempos_filtrados = arr
    return float(np.mean(tiempos_filtrados)), float(
        np.std(tiempos_filtrados)
    )


def guardar_csv(nombre_archivo, datos):
    with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "Estructura",
                "Escenario",
                "N",
                "Promedio_s",
                "Std_s",
            ],
        )
        writer.writeheader()
        writer.writerows(datos)


def ejecutar_experimentos():
   

    print("=== INICIANDO BENCHMARK  ===")

    valores_N = [100, 500, 1000, 2500, 5000, 10000]
    M_busquedas = 15000
    K_listados = 300
    num_replicas = 5
    escenarios = ["aleatorio", "ordenado"]

    resultados_insercion = []
    resultados_busqueda = []
    resultados_listado = []

    for N in valores_N:
        print(f"\n Procesando N = {N} ...")

        for escenario in escenarios:
            tiempos_ins = {"Lista": [], "ABB": [], "BPlusTree": []}
            tiempos_bus = {"Lista": [], "ABB": [], "BPlusTree": []}
            tiempos_lis = {"Lista": [], "ABB": [], "BPlusTree": []}

            for replica in range(num_replicas):
                datos = generar_estudiantes(N)

                if escenario == "ordenado":
                    datos.sort(key=lambda x: x["id"])

                ids_busqueda = random.choices(
                    [est["id"] for est in datos], k=M_busquedas
                )

                # Instancias limpias por réplica
                estructuras = {
                    "Lista": EstructuraLista(),
                    "ABB": ABB(),
                    "BPlusTree": ArbolBPlus(),
                }

                # A. INSERCIÓN (Una sola pasada limpia por datos)
                for nombre, est in estructuras.items():
                    t0 = time.perf_counter_ns()
                    for est_data in datos:
                        est.insertar(est_data)
                    t1 = time.perf_counter_ns()
                    tiempos_ins[nombre].append((t1 - t0) / 1e9)

                # B. BÚSQUEDA
                for nombre, est in estructuras.items():
                    t0 = time.perf_counter_ns()
                    for id_target in ids_busqueda:
                        est.buscar(id_target)
                    t1 = time.perf_counter_ns()
                    tiempos_bus[nombre].append((t1 - t0) / 1e9)

                # C. LISTADO ORDENADO
                for nombre, est in estructuras.items():
                    t0 = time.perf_counter_ns()
                    for _ in range(K_listados):
                        _ = est.listar_en_orden()
                    t1 = time.perf_counter_ns()
                    tiempos_lis[nombre].append((t1 - t0) / 1e9)

            # Guardar promedios
            for nombre in ["Lista", "ABB", "BPlusTree"]:
                prom_ins, std_ins = calcular_metricas(tiempos_ins[nombre])
                resultados_insercion.append(
                    {
                        "Estructura": nombre,
                        "Escenario": escenario,
                        "N": N,
                        "Promedio_s": prom_ins,
                        "Std_s": std_ins,
                    }
                )

                prom_bus, std_bus = calcular_metricas(tiempos_bus[nombre])
                resultados_busqueda.append(
                    {
                        "Estructura": nombre,
                        "Escenario": escenario,
                        "N": N,
                        "Promedio_s": prom_bus,
                        "Std_s": std_bus,
                    }
                )

                prom_lis, std_lis = calcular_metricas(tiempos_lis[nombre])
                resultados_listado.append(
                    {
                        "Estructura": nombre,
                        "Escenario": escenario,
                        "N": N,
                        "Promedio_s": prom_lis,
                        "Std_s": std_lis,
                    }
                )

    guardar_csv("resultados_insercion.csv", resultados_insercion)
    guardar_csv("resultados_busqueda.csv", resultados_busqueda)
    guardar_csv("resultados_listado.csv", resultados_listado)




if __name__ == "__main__":
    ejecutar_experimentos()