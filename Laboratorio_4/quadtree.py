"""Quadtree 2D para consultas de logística."""

import math

NO = "NO"
NE = "NE"
SO = "SO"
SE = "SE"

_CUADRANTES = (NO, NE, SO, SE)


class Nodo:
    """Nodo con límites, puntos (si hoja) y hasta cuatro hijos."""

    def __init__(self, limites, profundidad=0):
        self.limites = limites
        self.profundidad = profundidad
        self.puntos = []
        self.hijos = {}

    @property
    def es_hoja(self):
        """Indica si el nodo no tiene hijos."""
        return not self.hijos


def _cuadrante(punto, limites):
    xmin, ymin, xmax, ymax = limites
    xm = (xmin + xmax) / 2
    ym = (ymin + ymax) / 2
    x, y = punto
    if x < xm:
        return SO if y < ym else NO
    return SE if y < ym else NE


def _distancia2_rect(centro, limites):
    cx, cy = centro
    xmin, ymin, xmax, ymax = limites
    dx = max(xmin - cx, 0.0, cx - xmax)
    dy = max(ymin - cy, 0.0, cy - ymax)
    return dx * dx + dy * dy


class QuadTree:
    """Quadtree 2D con capacidad de hoja y profundidad máxima."""

    def __init__(self, puntos, limites, capacidad=8, profundidad_max=20):
        self.capacidad = capacidad
        self.profundidad_max = profundidad_max
        self.raiz = Nodo(tuple(limites))
        for punto in puntos:
            self._insertar(self.raiz, (punto[0], punto[1]))

    def _insertar(self, nodo, punto):
        if nodo.es_hoja:
            nodo.puntos.append(punto)
            if len(nodo.puntos) > self.capacidad and nodo.profundidad < self.profundidad_max:
                self._dividir(nodo)
        else:
            self._insertar(nodo.hijos[_cuadrante(punto, nodo.limites)], punto)

    def _dividir(self, nodo):
        xmin, ymin, xmax, ymax = nodo.limites
        xm = (xmin + xmax) / 2
        ym = (ymin + ymax) / 2
        profundidad = nodo.profundidad + 1
        nodo.hijos = {
            NO: Nodo((xmin, ym, xm, ymax), profundidad),
            NE: Nodo((xm, ym, xmax, ymax), profundidad),
            SO: Nodo((xmin, ymin, xm, ym), profundidad),
            SE: Nodo((xm, ymin, xmax, ym), profundidad),
        }
        puntos, nodo.puntos = nodo.puntos, []
        for punto in puntos:
            self._insertar(nodo, punto)

    def rango(self, centro, radio):
        """Devuelve los puntos a distancia <= radio y las estadísticas."""
        cx, cy = centro
        r2 = radio * radio
        hallados = []
        estadisticas = {"distancias_evaluadas": 0, "nodos_visitados": 0}
        self._rango(self.raiz, cx, cy, r2, hallados, estadisticas)
        return hallados, estadisticas

    def _rango(self, nodo, cx, cy, r2, hallados, estadisticas):
        estadisticas["nodos_visitados"] += 1
        if _distancia2_rect((cx, cy), nodo.limites) > r2:
            return
        if nodo.es_hoja:
            for punto in nodo.puntos:
                estadisticas["distancias_evaluadas"] += 1
                dx = punto[0] - cx
                dy = punto[1] - cy
                if dx * dx + dy * dy <= r2:
                    hallados.append(punto)
        else:
            for hijo in nodo.hijos.values():
                self._rango(hijo, cx, cy, r2, hallados, estadisticas)

    def vecino_mas_cercano(self, consulta):
        """Devuelve el punto más cercano, su distancia en metros y las estadísticas."""
        cx, cy = consulta
        estado = [None, math.inf]
        estadisticas = {"distancias_evaluadas": 0, "nodos_visitados": 0}
        self._vecino(self.raiz, cx, cy, estado, estadisticas)
        punto, mejor_d2 = estado
        distancia = math.inf if punto is None else math.sqrt(mejor_d2)
        return punto, distancia, estadisticas

    def _vecino(self, nodo, cx, cy, estado, estadisticas):
        estadisticas["nodos_visitados"] += 1
        if _distancia2_rect((cx, cy), nodo.limites) > estado[1]:
            return
        if nodo.es_hoja:
            for punto in nodo.puntos:
                estadisticas["distancias_evaluadas"] += 1
                dx = punto[0] - cx
                dy = punto[1] - cy
                d2 = dx * dx + dy * dy
                mejor = estado[0]
                if d2 < estado[1] or (d2 == estado[1] and mejor is not None and punto < mejor):
                    estado[0] = punto
                    estado[1] = d2
            return
        hijos = sorted(
            (
                (_distancia2_rect((cx, cy), hijo.limites), hijo)
                for hijo in nodo.hijos.values()
            ),
            key=lambda par: par[0],
        )
        for distancia2, hijo in hijos:
            if distancia2 > estado[1]:
                break
            self._vecino(hijo, cx, cy, estado, estadisticas)

    def contar_nodos(self, nodo=None):
        """Cuenta los nodos (hojas e internos) del subárbol."""
        if nodo is None:
            nodo = self.raiz
        if nodo.es_hoja:
            return 1
        return 1 + sum(self.contar_nodos(hijo) for hijo in nodo.hijos.values())
