# generador.py
import random


def generar_estudiantes(n: int, ordenados: bool = False):
  nombres = [
      "Juan",
      "Carlos",
      "Andres",
      "Luis",
      "Santiago",
      "Ana",
      "Maria",
      "Laura",
      "Sofia",
      "Valentina",
  ]
  apellidos = [
      "Gomez",
      "Rodriguez",
      "Martinez",
      "Lopez",
      "Garcia",
      "Perez",
      "Sanchez",
      "Ramirez",
  ]

  ids = random.sample(range(100_000, 9_999_999), n)
  if ordenados:
    ids.sort()

  estudiantes = []
  for id_est in ids:
    estudiantes.append({
        "id": id_est,
        "nombre": f"{random.choice(nombres)} {random.choice(apellidos)}",
        "edad": random.randint(17, 30),
        "promedio": round(random.uniform(0.0, 5.0), 2),
    })

  return estudiantes