# Laboratorio 1 – Matriz 100.000x100.0000

**Estudiante:** Simon Montoya

## Objetivo

Resolver el problema de almacenamiento y lectura de una matriz de **100.000 × 100.000**, optimizando el consumo de RAM, la escritura en disco y la manipulación de los datos.

## Solución

La matriz contiene únicamente valores `0` y `1`, por lo que se utiliza un **bitmap**, almacenando cada valor como un bit en lugar de utilizar caracteres.

* La matriz tiene **100.000 filas**.
* Cada fila se representa mediante un bitmap de **100.000 bits**.
* Cada bitmap ocupa **12.500 bytes**.
* Los **100.000 bitmaps** se almacenan consecutivamente en un único archivo binario llamado `matriz.bitmap`.



## Archivos

### `matriz_con_bitmap.py`

Crea el archivo `matriz.bitmap`. Genera un bitmap completamente inactivo, con todos sus bits en `0`, y lo escribe 100.000 veces, representando las 100.000 filas.

### `matriz_lector.py`

Lee los primeros **12.500 bytes** del archivo, correspondientes a la primera fila, y permite verificar su cantidad de bytes y bits. 

## Verificación

Al ejecutar el lector se debe obtener:

```text
Bytes de la primera fila: 12500
Ceros de la primera fila: 100000
```

Esto confirma que la primera fila contiene **100.000 bits**, todos en `0`.

Los bitmaps no utilizan separadores entre filas, ya que cada uno tiene un tamaño fijo de **12.500 bytes**, permitiendo identificar dónde comienza y termina cada fila.
