import hashlib


def hash_data(data):
  "Hashes data using SHA-256."
  return hashlib.sha256(data.encode('utf-8')).hexdigest()

def concatenar(n, m):
  transaccion = n + m
  return hash_data(transaccion)


def raiz_merkle(data):
  
  if not data:
    return None, []

  nivel = [hash_data(str(dato)) for dato in data]
  niveles = [nivel]
  while len(nivel) > 1:
    siguiente_nivel = []

    for posicion in range(0, len(nivel), 2):
      izquierdo = nivel[posicion]
      
      if posicion + 1 < len(nivel):
        derecho = nivel[posicion + 1]
      else:
        derecho = izquierdo
      siguiente_nivel.append(concatenar(izquierdo, derecho))
      

    nivel = siguiente_nivel
    niveles.append(nivel)

  return nivel[0],niveles

def mostrar_arbol(niveles, largo=6):
    """Dibuja el árbol de Merkle con slashes conectando padres e hijos."""
    labels = [[h[:largo] for h in nivel] for nivel in niveles] # extraer las primeras '6' caracteres de cada hash
    gap = 2
    espacio = largo + gap

    # posiciones (columna) de cada nodo, nivel por nivel, empezando por las hojas
    posiciones = [[i * espacio for i in range(len(labels[0]))]]

    for nivel_idx in range(1, len(labels)):
        pos_anterior = posiciones[-1]
        nueva_pos = []
        for k in range(len(labels[nivel_idx])):
            izq = pos_anterior[2 * k]
            der = pos_anterior[2 * k + 1] if 2 * k + 1 < len(pos_anterior) else izq # Si no hay un nodo derecho, se usa el izquierdo
            nueva_pos.append((izq + der) / 2)
        posiciones.append(nueva_pos)

    # se imprime desde la raíz hacia las hojas
    for nivel_idx in range(len(labels) - 1, -1, -1):
        pos_nivel = posiciones[nivel_idx]
        etiquetas = labels[nivel_idx]

        ancho_linea = int(max(pos_nivel)) + largo + 1
        linea = [" "] * ancho_linea
        for pos, etiqueta in zip(pos_nivel, etiquetas):
            col = int(pos)
            for offset, ch in enumerate(etiqueta):
                linea[col + offset] = ch
        print("".join(linea))

        if nivel_idx > 0:
            pos_hijos = posiciones[nivel_idx - 1]
            ancho_conexion = int(max(pos_hijos)) + largo + 1
            conexion = [" "] * ancho_conexion

            for k, pos_padre in enumerate(pos_nivel):
                izq_idx = 2 * k
                der_idx = 2 * k + 1 if 2 * k + 1 < len(pos_hijos) else izq_idx
                pos_izq, pos_der = pos_hijos[izq_idx], pos_hijos[der_idx]
                col_padre = int(pos_padre)

                if pos_izq != pos_der:
                    col_izq = int((pos_izq + col_padre) / 2)
                    col_der = int((pos_der + col_padre) / 2)
                    conexion[col_izq] = "/"
                    conexion[col_der] = "\\"
                else:
                    conexion[col_padre] = "|"
            print("".join(conexion))

def modificar_transaccion(datos, niveles_anteriores, pos, nuevo_valor):
    """Modifica un bloque de forma permanente y muestra el árbol antes y después."""
    
    raiz_anterior = niveles_anteriores[-1][0]   # Toma la raiz que es el primer elemento del último nivel
    valor_anterior = datos[pos]

    datos[pos] = nuevo_valor                    
    raiz_nueva, niveles_nuevos = raiz_merkle(datos)  

    print("===== ÁRBOL ANTERIOR =====")
    mostrar_arbol(niveles_anteriores)
    print("\nRaíz anterior: ", raiz_anterior)

    print(f"\n(Se cambió el dato en la posición {pos + 1}: "
          f"'{valor_anterior}' -> '{nuevo_valor}')")

    print("\n===== ÁRBOL NUEVO =====")
    mostrar_arbol(niveles_nuevos)
    print("\nRaíz nueva:    ", raiz_nueva)

    return raiz_nueva, niveles_nuevos

def verificar_transacciones(datos, verificar):
    """Verifica si una transacción está en el árbol de Merkle."""
    if hash_data(verificar) in [hash_data(dato) for dato in datos]:
        print(f"La transacción '{verificar}' está  en el árbol de Merkle.")
        print("Hash de la transacción:", hash_data(verificar))
    else:
        print(f"La transacción '{verificar}' NO está  en el árbol de Merkle.")
   
   


if __name__ == "__main__":
    cantidad = int(input("¿Cuántos datos desea ingresar? "))
    datos = []
    

    for posicion in range(cantidad):
        dato = input(f"Ingrese el dato {posicion+1 }: ")
        datos.append(dato)

    raiz, niveles = raiz_merkle(datos)
    eleccion = 0
    while(eleccion != 4):
      eleccion = int(input("¿Que desea hacer con las transacciones? \n1. Mostrar el arbol\n2. Modificar una transacción\n3.Verificar transacción\n4.Salir\n"))
      
      match eleccion:
        case 1:
            mostrar_arbol(niveles, largo=6)
            
            
        case 2: 
            pos_u = int(input(f"Ingrese la posición de la transacción a modificar: (1 - {cantidad}): "))
            pos = pos_u - 1
            nuevo_valor = input("Ingrese un nuevo valor para la transacción: ")
            
            raiz, niveles = modificar_transaccion(datos, niveles, pos, nuevo_valor)
            
          
        case 3:
            verificar = input("Ingrese la transacción a verificar: ")
            verificar_transacciones(datos, verificar)
          
        case 4:
            print("Saliendo del programa")

        case _:
            print("Opción inválida. Por favor, elija una opción válida.")
          
      

   


    


