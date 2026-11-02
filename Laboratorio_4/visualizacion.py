"""Visualización del quadtree y de una consulta."""

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle

import generador_datos as gd
import quadtree as qt


def _segmentos(nodo):
    if nodo.es_hoja:
        return
    xmin, ymin, xmax, ymax = nodo.limites
    xm = (xmin + xmax) / 2
    ym = (ymin + ymax) / 2
    yield [(xm, ymin), (xm, ymax)]
    yield [(xmin, ym), (xmax, ym)]
    for hijo in nodo.hijos.values():
        yield from _segmentos(hijo)


def dibujar(puntos, arbol, centro, radio=gd.RADIO, ax=None):
    """Dibuja puntos, divisiones, círculo, hallados y vecino más cercano."""
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 8))
    hallados, _ = arbol.rango(centro, radio)
    vecino, distancia, _ = arbol.vecino_mas_cercano(centro)
    ax.add_collection(
        LineCollection(list(_segmentos(arbol.raiz)), colors="lightgray", linewidths=0.4)
    )
    if puntos:
        xs, ys = zip(*puntos)
        ax.scatter(xs, ys, s=4, c="tab:blue", alpha=0.5, label="puntos")
    if hallados:
        xs, ys = zip(*hallados)
        ax.scatter(xs, ys, s=22, c="tab:green", label=f"rango ({len(hallados)})")
    ax.add_patch(
        Circle(centro, radio, fill=False, color="tab:red", linestyle="--", linewidth=1.4)
    )
    if vecino is not None:
        ax.plot([centro[0], vecino[0]], [centro[1], vecino[1]], ":", color="tab:orange")
        ax.scatter(
            [vecino[0]],
            [vecino[1]],
            marker="*",
            s=140,
            c="tab:orange",
            edgecolors="black",
            label=f"vecino ({distancia:.1f} m)",
        )
    ax.scatter([centro[0]], [centro[1]], marker="x", s=70, c="black", label="consulta")
    ax.set_xlim(arbol.raiz.limites[0], arbol.raiz.limites[2])
    ax.set_ylim(arbol.raiz.limites[1], arbol.raiz.limites[3])
    ax.set_aspect("equal")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title(f"Quadtree 2D: rango de {radio:.0f} m y vecino más cercano")
    ax.legend(loc="upper right", fontsize=8, markerscale=2)
    return ax


def main():
    """Genera datos, construye el árbol y muestra la figura."""
    puntos = gd.generar_puntos(10_000)
    arbol = qt.QuadTree(puntos, gd.LIMITES)
    dibujar(puntos, arbol, (5000.0, 5000.0), gd.RADIO)
    plt.show()


if __name__ == "__main__":
    main()
