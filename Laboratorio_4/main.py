"""Punto de entrada: ejecuta, grafica y resume el proyecto."""

import os

import matplotlib.pyplot as plt

import analisis
import fuerza_bruta as fb
import generador_datos as gd
import quadtree as qt
import visualizacion


def _resumen_basico():
    puntos = gd.generar_puntos(10_000)
    arbol = qt.QuadTree(puntos, gd.LIMITES)
    centro = (5000.0, 5000.0)
    hallados, est_rango = arbol.rango(centro, gd.RADIO)
    vecino, distancia, est_vecino = arbol.vecino_mas_cercano(centro)
    esperados, _ = fb.rango(puntos, centro, gd.RADIO)
    vecino_fb, distancia_fb, _ = fb.vecino_mas_cercano(puntos, centro)

    print("=== Quadtree 2D: resumen ===")
    print(f"Puntos: {len(puntos)}   Nodos: {arbol.contar_nodos()}")
    print(
        f"Rango {gd.RADIO:.0f} m: {len(hallados)} hallados, "
        f"{est_rango['distancias_evaluadas']} distancias y "
        f"{est_rango['nodos_visitados']} nodos visitados"
    )
    print(
        f"Vecino: {vecino} a {distancia:.2f} m, "
        f"{est_vecino['distancias_evaluadas']} distancias y "
        f"{est_vecino['nodos_visitados']} nodos visitados"
    )
    coincide = sorted(hallados) == sorted(esperados) and (
        vecino,
        distancia,
    ) == (vecino_fb, distancia_fb)
    print(f"Coincide con fuerza bruta: {'si' if coincide else 'NO'}")
    return puntos, arbol, centro


def main():
    """Ejecuta el resumen, guarda la visualización y corre el análisis."""
    puntos, arbol, centro = _resumen_basico()

    os.makedirs(analisis.CARPETA, exist_ok=True)
    visualizacion.dibujar(puntos, arbol, centro, gd.RADIO)
    ruta = os.path.join(analisis.CARPETA, "visualizacion.png")
    plt.savefig(ruta, dpi=130, bbox_inches="tight")
    plt.close()
    print(f"Visualizacion guardada en {ruta}")

    print("\n=== Barrido de N ===")
    resultados = analisis.main()

    ultimo = resultados[-1]
    print("\n=== Resumen final ===")
    print(
        f"Rango (N={ultimo['n']}): "
        f"{ultimo['rango']['qt_tiempo'] * 1e3:.3f} ms quadtree vs "
        f"{ultimo['rango']['fb_tiempo'] * 1e3:.3f} ms fuerza bruta "
        f"(x{ultimo['rango']['fb_tiempo'] / ultimo['rango']['qt_tiempo']:.1f})"
    )
    print(
        f"Vecino (N={ultimo['n']}): "
        f"{ultimo['vecino']['qt_tiempo'] * 1e6:.1f} us quadtree vs "
        f"{ultimo['vecino']['fb_tiempo'] * 1e3:.3f} ms fuerza bruta "
        f"(x{ultimo['vecino']['fb_tiempo'] / ultimo['vecino']['qt_tiempo']:.1f})"
    )


if __name__ == "__main__":
    main()
