"""Barrido de tamaños y rendimiento del quadtree."""

import gc
import os
import time
import tracemalloc

import matplotlib.pyplot as plt

import fuerza_bruta as fb
import generador_datos as gd
import quadtree as qt

TAMANOS = (1_000, 5_000, 10_000, 50_000, 100_000)
CONSULTAS = 50
RADIO = gd.RADIO
CARPETA = "graficas"


def memoria_arbol(puntos):
    gc.collect()
    tracemalloc.start()
    arbol = qt.QuadTree(puntos, gd.LIMITES)
    actual, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    del arbol
    return actual


def medir_consultas(consultas, funcion_qt, funcion_fb):
    inicio = time.perf_counter()
    distancias_qt = 0
    for consulta in consultas:
        distancias_qt += funcion_qt(consulta)[-1]["distancias_evaluadas"]
    tiempo_qt = (time.perf_counter() - inicio) / len(consultas)

    inicio = time.perf_counter()
    distancias_fb = 0
    for consulta in consultas:
        distancias_fb += funcion_fb(consulta)[-1]["distancias_evaluadas"]
    tiempo_fb = (time.perf_counter() - inicio) / len(consultas)

    return {
        "qt_tiempo": tiempo_qt,
        "fb_tiempo": tiempo_fb,
        "qt_distancias": distancias_qt / len(consultas),
        "fb_distancias": distancias_fb / len(consultas),
    }


def _medir(n, semilla):
    puntos = gd.generar_puntos(n, semilla=semilla)
    inicio = time.perf_counter()
    arbol = qt.QuadTree(puntos, gd.LIMITES)
    tiempo_construccion = time.perf_counter() - inicio
    consultas = gd.generar_consultas(CONSULTAS, semilla=semilla + 1)
    return {
        "n": n,
        "nodos": arbol.contar_nodos(),
        "memoria": memoria_arbol(puntos),
        "tiempo_construccion": tiempo_construccion,
        "rango": medir_consultas(
            consultas,
            lambda c: arbol.rango(c, RADIO),
            lambda c: fb.rango(puntos, c, RADIO),
        ),
        "vecino": medir_consultas(
            consultas,
            arbol.vecino_mas_cercano,
            lambda c: fb.vecino_mas_cercano(puntos, c),
        ),
    }


def ejecutar(tamanos=TAMANOS):
    """Ejecuta el barrido y devuelve los resultados por tamaño."""
    return [_medir(n, gd.SEMILLA + i) for i, n in enumerate(tamanos)]


def graficar(resultados, carpeta=CARPETA):
    """Guarda las gráficas del barrido en la carpeta indicada."""
    os.makedirs(carpeta, exist_ok=True)
    ns = [r["n"] for r in resultados]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    ax1.plot(ns, [r["nodos"] for r in resultados], "o-", color="tab:blue")
    ax1.set_title("Nodos del quadtree")
    ax1.set_xlabel("N")
    ax1.set_ylabel("nodos")
    ax1.grid(True, alpha=0.3)
    ax2.plot(ns, [r["memoria"] / (1024 * 1024) for r in resultados], "o-", color="tab:green")
    ax2.set_title("Memoria del quadtree")
    ax2.set_xlabel("N")
    ax2.set_ylabel("memoria (MiB)")
    ax2.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(carpeta, "tamano.png"), dpi=130)
    plt.close(fig)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    for ax, clave, titulo in (
        (ax1, "rango", "Rango: distancias evaluadas por consulta"),
        (ax2, "vecino", "Vecino: distancias evaluadas por consulta"),
    ):
        ax.plot(ns, [r[clave]["qt_distancias"] for r in resultados], "o-", label="quadtree")
        ax.plot(ns, [r[clave]["fb_distancias"] for r in resultados], "s--", label="fuerza bruta")
        ax.set_yscale("log")
        ax.set_title(titulo)
        ax.set_xlabel("N")
        ax.set_ylabel("distancias")
        ax.grid(True, which="both", alpha=0.3)
        ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(carpeta, "distancias.png"), dpi=130)
    plt.close(fig)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    ax1.plot(ns, [r["tiempo_construccion"] for r in resultados], "o-", color="tab:blue")
    ax1.set_title("Construcción del quadtree")
    ax1.set_xlabel("N")
    ax1.set_ylabel("tiempo (s)")
    ax1.grid(True, alpha=0.3)
    ax2.plot(ns, [r["rango"]["qt_tiempo"] for r in resultados], "o-", label="rango quadtree")
    ax2.plot(ns, [r["rango"]["fb_tiempo"] for r in resultados], "s--", label="rango fuerza bruta")
    ax2.plot(ns, [r["vecino"]["qt_tiempo"] for r in resultados], "o-.", label="vecino quadtree")
    ax2.plot(ns, [r["vecino"]["fb_tiempo"] for r in resultados], "s:", label="vecino fuerza bruta")
    ax2.set_yscale("log")
    ax2.set_title("Consultas: tiempo por consulta")
    ax2.set_xlabel("N")
    ax2.set_ylabel("tiempo (s)")
    ax2.grid(True, which="both", alpha=0.3)
    ax2.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(carpeta, "tiempos.png"), dpi=130)
    plt.close(fig)


def main():
    """Ejecuta el barrido, guarda las gráficas e imprime el resumen."""
    resultados = ejecutar()
    graficar(resultados)
    print(f"{'N':>7} {'nodos':>7} {'mem(MiB)':>9} {'constr(s)':>10} "
          f"{'rango_qt(us)':>13} {'rango_fb(us)':>13} "
          f"{'vec_qt(us)':>11} {'vec_fb(us)':>11}")
    for r in resultados:
        print(
            f"{r['n']:>7} {r['nodos']:>7} {r['memoria'] / (1024 * 1024):>9.2f} "
            f"{r['tiempo_construccion']:>10.4f} "
            f"{r['rango']['qt_tiempo'] * 1e6:>13.1f} {r['rango']['fb_tiempo'] * 1e6:>13.1f} "
            f"{r['vecino']['qt_tiempo'] * 1e6:>11.1f} {r['vecino']['fb_tiempo'] * 1e6:>11.1f}"
        )
    return resultados


if __name__ == "__main__":
    main()
