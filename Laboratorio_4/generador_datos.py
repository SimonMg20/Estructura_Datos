"""Generación de puntos y consultas aleatorias."""

import random

LADO = 10_000.0
LIMITES = (0.0, 0.0, LADO, LADO)
SEMILLA = 42
RADIO = 500.0


def _generar(n, semilla, lado):
    rng = random.Random(semilla)
    return [(rng.random() * lado, rng.random() * lado) for _ in range(n)]


def generar_puntos(n, semilla=SEMILLA, lado=LADO):
    """Devuelve n puntos (x, y) en [0, lado) x [0, lado)."""
    return _generar(n, semilla, lado)


def generar_consultas(n, semilla=SEMILLA + 1, lado=LADO):
    """Devuelve n consultas (x, y) en [0, lado) x [0, lado)."""
    return _generar(n, semilla, lado)
