with open("matriz.bitmap", "rb") as f:  # "rb": lectura en modo binario.
    datos = f.read(12500)              # Lee los 12.500 bytes de la primera fila.

print("Bytes de la primera fila:", len(datos))

print("Ceros de la primera fila:", len(datos) * 8)