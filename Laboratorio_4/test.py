"""Pruebas del proyecto."""

import math
import unittest

import fuerza_bruta as fb
import generador_datos as gd
import quadtree as qt


def _recolectar(nodo):
    if nodo.es_hoja:
        return list(nodo.puntos)
    puntos = []
    for hijo in nodo.hijos.values():
        puntos.extend(_recolectar(hijo))
    return puntos


def _hojas(nodo):
    if nodo.es_hoja:
        yield nodo
        return
    for hijo in nodo.hijos.values():
        yield from _hojas(hijo)


def _profundidad_maxima(nodo):
    if nodo.es_hoja:
        return nodo.profundidad
    return max(_profundidad_maxima(hijo) for hijo in nodo.hijos.values())


class PruebasGenerador(unittest.TestCase):
    def test_cantidad(self):
        self.assertEqual(len(gd.generar_puntos(1000)), 1000)
        self.assertEqual(len(gd.generar_consultas(100)), 100)

    def test_dentro_de_limites(self):
        for x, y in gd.generar_puntos(10_000):
            self.assertGreaterEqual(x, 0.0)
            self.assertGreaterEqual(y, 0.0)
            self.assertLess(x, gd.LADO)
            self.assertLess(y, gd.LADO)

    def test_semilla_reproducible(self):
        self.assertEqual(gd.generar_puntos(10), gd.generar_puntos(10))
        self.assertNotEqual(gd.generar_puntos(10), gd.generar_puntos(10, semilla=7))

    def test_consultas_distintas_de_puntos(self):
        self.assertNotEqual(gd.generar_puntos(5), gd.generar_consultas(5))


class PruebasFuerzaBruta(unittest.TestCase):
    def setUp(self):
        self.puntos = gd.generar_puntos(200, semilla=7)
        self.centro = (5000.0, 5000.0)

    def test_rango_coincide_con_filtro(self):
        radio = 500.0
        hallados, est = fb.rango(self.puntos, self.centro, radio)
        esperados = [
            p
            for p in self.puntos
            if (p[0] - self.centro[0]) ** 2 + (p[1] - self.centro[1]) ** 2 <= radio**2
        ]
        self.assertEqual(hallados, esperados)
        self.assertEqual(est["distancias_evaluadas"], len(self.puntos))

    def test_rango_incluye_borde(self):
        puntos = [(500.0, 0.0), (501.0, 0.0)]
        hallados, _ = fb.rango(puntos, (0.0, 0.0), 500.0)
        self.assertEqual(hallados, [(500.0, 0.0)])

    def test_vecino_mas_cercano(self):
        punto, distancia, est = fb.vecino_mas_cercano(self.puntos, self.centro)
        esperado = min(
            self.puntos,
            key=lambda p: (p[0] - self.centro[0]) ** 2 + (p[1] - self.centro[1]) ** 2,
        )
        d2 = (esperado[0] - self.centro[0]) ** 2 + (esperado[1] - self.centro[1]) ** 2
        self.assertEqual(punto, esperado)
        self.assertAlmostEqual(distancia, math.sqrt(d2))
        self.assertEqual(est["distancias_evaluadas"], len(self.puntos))

    def test_vecino_desempate_lexicografico(self):
        puntos = [(1.0, 0.0), (-1.0, 0.0)]
        punto, distancia, _ = fb.vecino_mas_cercano(puntos, (0.0, 0.0))
        self.assertEqual(punto, (-1.0, 0.0))
        self.assertEqual(distancia, 1.0)

    def test_lista_vacia(self):
        hallados, est = fb.rango([], (0.0, 0.0), 10.0)
        self.assertEqual(hallados, [])
        self.assertEqual(est["distancias_evaluadas"], 0)
        punto, distancia, _ = fb.vecino_mas_cercano([], (0.0, 0.0))
        self.assertIsNone(punto)
        self.assertEqual(distancia, math.inf)


class PruebasQuadTree(unittest.TestCase):
    def test_hoja_en_capacidad(self):
        puntos = [(10.0 * i, 10.0 * i) for i in range(8)]
        arbol = qt.QuadTree(puntos, (0, 0, 1000, 1000))
        self.assertTrue(arbol.raiz.es_hoja)
        self.assertEqual(len(arbol.raiz.puntos), 8)
        self.assertEqual(arbol.contar_nodos(), 1)

    def test_divide_al_superar_capacidad(self):
        puntos = [(10.0 * i, 10.0 * i) for i in range(9)]
        arbol = qt.QuadTree(puntos, (0, 0, 1000, 1000))
        self.assertFalse(arbol.raiz.es_hoja)
        self.assertEqual(set(arbol.raiz.hijos), {qt.NO, qt.NE, qt.SO, qt.SE})
        self.assertEqual(arbol.raiz.puntos, [])
        self.assertEqual(sorted(_recolectar(arbol.raiz)), sorted(puntos))

    def test_limites_de_hijos(self):
        arbol = qt.QuadTree([(10.0, 10.0), (90.0, 90.0)], (0, 0, 100, 100), capacidad=1)
        self.assertEqual(arbol.raiz.hijos[qt.NO].limites, (0, 50, 50, 100))
        self.assertEqual(arbol.raiz.hijos[qt.NE].limites, (50, 50, 100, 100))
        self.assertEqual(arbol.raiz.hijos[qt.SO].limites, (0, 0, 50, 50))
        self.assertEqual(arbol.raiz.hijos[qt.SE].limites, (50, 0, 100, 50))

    def test_bordes_semiabiertos(self):
        puntos = [(50.0, 50.0), (50.0, 25.0), (25.0, 50.0), (25.0, 25.0)]
        arbol = qt.QuadTree(puntos, (0, 0, 100, 100), capacidad=1)
        self.assertEqual(arbol.raiz.hijos[qt.NE].puntos, [(50.0, 50.0)])
        self.assertEqual(arbol.raiz.hijos[qt.SE].puntos, [(50.0, 25.0)])
        self.assertEqual(arbol.raiz.hijos[qt.NO].puntos, [(25.0, 50.0)])
        self.assertEqual(arbol.raiz.hijos[qt.SO].puntos, [(25.0, 25.0)])

    def test_profundidad_maxima_corta_duplicados(self):
        arbol = qt.QuadTree([(500.0, 500.0)] * 100, (0, 0, 1000, 1000), profundidad_max=3)
        self.assertEqual(len(_recolectar(arbol.raiz)), 100)
        self.assertEqual(_profundidad_maxima(arbol.raiz), 3)

    def test_hojas_respetan_capacidad(self):
        arbol = qt.QuadTree(gd.generar_puntos(1000, semilla=5), gd.LIMITES)
        for hoja in _hojas(arbol.raiz):
            self.assertLessEqual(len(hoja.puntos), arbol.capacidad)

    def test_todos_los_puntos_presentes(self):
        puntos = gd.generar_puntos(2000, semilla=3)
        arbol = qt.QuadTree(puntos, gd.LIMITES)
        recolectados = _recolectar(arbol.raiz)
        self.assertEqual(len(recolectados), len(puntos))
        self.assertEqual(sorted(recolectados), sorted(puntos))


class PruebasRango(unittest.TestCase):
    def setUp(self):
        self.puntos = gd.generar_puntos(5000, semilla=11)
        self.arbol = qt.QuadTree(self.puntos, gd.LIMITES)

    def test_coincide_con_fuerza_bruta(self):
        for centro in gd.generar_consultas(50, semilla=12):
            hallados, _ = self.arbol.rango(centro, 500.0)
            esperados, _ = fb.rango(self.puntos, centro, 500.0)
            self.assertEqual(sorted(hallados), sorted(esperados))

    def test_estadisticas(self):
        centro = (5000.0, 5000.0)
        hallados, est = self.arbol.rango(centro, 500.0)
        esperados, _ = fb.rango(self.puntos, centro, 500.0)
        self.assertEqual(set(est), {"distancias_evaluadas", "nodos_visitados"})
        self.assertGreater(est["nodos_visitados"], 0)
        self.assertEqual(sorted(hallados), sorted(esperados))

    def test_poda_evalua_menos_que_fuerza_bruta(self):
        _, est = self.arbol.rango((5000.0, 5000.0), 500.0)
        self.assertLess(est["distancias_evaluadas"], len(self.puntos))
        self.assertLess(est["nodos_visitados"], self.arbol.contar_nodos())

    def test_borde_incluido(self):
        puntos = [(500.0, 0.0), (500.0001, 0.0)]
        arbol = qt.QuadTree(puntos, (0, 0, 1000, 1000), capacidad=1)
        hallados, _ = arbol.rango((0.0, 0.0), 500.0)
        self.assertEqual(hallados, [(500.0, 0.0)])

    def test_radio_cero(self):
        arbol = qt.QuadTree([(10.0, 10.0), (20.0, 20.0)], (0, 0, 100, 100), capacidad=1)
        hallados, _ = arbol.rango((10.0, 10.0), 0.0)
        self.assertEqual(hallados, [(10.0, 10.0)])

    def test_centro_fuera_del_area(self):
        arbol = qt.QuadTree([(0.0, 0.0), (100.0, 100.0)], (0, 0, 100, 100), capacidad=1)
        hallados, _ = arbol.rango((-10.0, -10.0), 15.0)
        self.assertEqual(hallados, [(0.0, 0.0)])


class PruebasVecino(unittest.TestCase):
    def setUp(self):
        self.puntos = gd.generar_puntos(5000, semilla=31)
        self.arbol = qt.QuadTree(self.puntos, gd.LIMITES)

    def test_coincide_con_fuerza_bruta(self):
        for consulta in gd.generar_consultas(50, semilla=32):
            esperado, distancia_esperada, _ = fb.vecino_mas_cercano(self.puntos, consulta)
            punto, distancia, _ = self.arbol.vecino_mas_cercano(consulta)
            self.assertEqual(punto, esperado)
            self.assertEqual(distancia, distancia_esperada)

    def test_distancia_en_metros(self):
        arbol = qt.QuadTree([(3.0, 4.0)], (0, 0, 10, 10))
        punto, distancia, _ = arbol.vecino_mas_cercano((0.0, 0.0))
        self.assertEqual(punto, (3.0, 4.0))
        self.assertEqual(distancia, 5.0)

    def test_consulta_sobre_un_punto(self):
        arbol = qt.QuadTree([(10.0, 10.0), (20.0, 20.0), (30.0, 30.0)], (0, 0, 100, 100))
        punto, distancia, _ = arbol.vecino_mas_cercano((20.0, 20.0))
        self.assertEqual(punto, (20.0, 20.0))
        self.assertEqual(distancia, 0.0)

    def test_estadisticas_y_poda(self):
        _, _, est = self.arbol.vecino_mas_cercano((5000.0, 5000.0))
        self.assertEqual(set(est), {"distancias_evaluadas", "nodos_visitados"})
        self.assertGreater(est["nodos_visitados"], 0)
        self.assertLess(est["distancias_evaluadas"], len(self.puntos))
        self.assertLess(est["nodos_visitados"], self.arbol.contar_nodos())

    def test_lista_vacia(self):
        arbol = qt.QuadTree([], (0, 0, 10, 10))
        punto, distancia, est = arbol.vecino_mas_cercano((0.0, 0.0))
        self.assertIsNone(punto)
        self.assertEqual(distancia, math.inf)
        self.assertEqual(est["distancias_evaluadas"], 0)


class PruebasComparacion(unittest.TestCase):
    def test_rango_exacto_en_varios_tamanos(self):
        for n, semilla in ((1000, 41), (5000, 42), (10000, 43)):
            puntos = gd.generar_puntos(n, semilla=semilla)
            arbol = qt.QuadTree(puntos, gd.LIMITES)
            for centro in gd.generar_consultas(150, semilla=semilla + 1):
                with self.subTest(n=n, centro=centro):
                    hallados, _ = arbol.rango(centro, 500.0)
                    esperados, _ = fb.rango(puntos, centro, 500.0)
                    self.assertEqual(sorted(hallados), sorted(esperados))

    def test_vecino_exacto_en_varios_tamanos(self):
        for n, semilla in ((1000, 51), (5000, 52), (10000, 53)):
            puntos = gd.generar_puntos(n, semilla=semilla)
            arbol = qt.QuadTree(puntos, gd.LIMITES)
            for consulta in gd.generar_consultas(150, semilla=semilla + 1):
                with self.subTest(n=n, consulta=consulta):
                    punto, distancia, _ = arbol.vecino_mas_cercano(consulta)
                    esperado, dist_esperada, _ = fb.vecino_mas_cercano(puntos, consulta)
                    self.assertEqual(punto, esperado)
                    self.assertEqual(distancia, dist_esperada)

    def test_rango_resultados_dentro_del_radio(self):
        puntos = gd.generar_puntos(2000, semilla=61)
        arbol = qt.QuadTree(puntos, gd.LIMITES)
        radio = 500.0
        for centro in gd.generar_consultas(100, semilla=62):
            hallados, _ = arbol.rango(centro, radio)
            for x, y in hallados:
                d2 = (x - centro[0]) ** 2 + (y - centro[1]) ** 2
                self.assertLessEqual(d2, radio * radio)

    def test_poda_no_evalua_mas_que_fuerza_bruta(self):
        puntos = gd.generar_puntos(5000, semilla=71)
        arbol = qt.QuadTree(puntos, gd.LIMITES)
        nodos = arbol.contar_nodos()
        for centro in gd.generar_consultas(50, semilla=72):
            _, est_rango = arbol.rango(centro, 500.0)
            _, _, est_vecino = arbol.vecino_mas_cercano(centro)
            self.assertLessEqual(est_rango["distancias_evaluadas"], len(puntos))
            self.assertLessEqual(est_rango["nodos_visitados"], nodos)
            self.assertLessEqual(est_vecino["distancias_evaluadas"], len(puntos))
            self.assertLessEqual(est_vecino["nodos_visitados"], nodos)


if __name__ == "__main__":
    unittest.main()
