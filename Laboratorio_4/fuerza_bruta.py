"""Búsquedas por fuerza bruta para contrastar el quadtree."""

import math


def rango(puntos, centro, radio):
    """Devuelve los puntos a distancia <= radio y las estadísticas."""
    cx, cy = centro
    r2 = radio * radio
    hallados = []
    evaluadas = 0
    for x, y in puntos:
        evaluadas += 1
        dx = x - cx
        dy = y - cy
        if dx * dx + dy * dy <= r2:
            hallados.append((x, y))
    return hallados, {"distancias_evaluadas": evaluadas, "nodos_visitados": 1}


def vecino_mas_cercano(puntos, consulta):
    """Devuelve el punto más cercano, su distancia en metros y las estadísticas."""
    cx, cy = consulta
    mejor = None
    mejor_d2 = math.inf
    evaluadas = 0
    for x, y in puntos:
        evaluadas += 1
        dx = x - cx
        dy = y - cy
        d2 = dx * dx + dy * dy
        if d2 < mejor_d2 or (d2 == mejor_d2 and mejor is not None and (x, y) < mejor):
            mejor = (x, y)
            mejor_d2 = d2
    if mejor is None:
        return None, math.inf, {"distancias_evaluadas": 0, "nodos_visitados": 1}
    return mejor, math.sqrt(mejor_d2), {
        "distancias_evaluadas": evaluadas,
        "nodos_visitados": 1,
    }
