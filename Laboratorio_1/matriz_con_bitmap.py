filas = 100000
columnas = 100000

# Cada bitmap representa una fila de la matriz
# 100.000 bits / 8 bits = 12.500 bytes por bitmap
bytes_por_bitmap = columnas // 8

# Crea un bitmap con todos los bits en 0
bitmap = bytes(bytes_por_bitmap)

#Almacena los 100.000 bitmaps en un archivo binario
with open("matriz.bitmap", "wb") as f: #"wb" se utiliza para escribir en binario
    for _ in range(filas):
        f.write(bitmap)