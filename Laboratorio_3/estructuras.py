

# ==========================================
# 1. IMPLEMENTACIÓN BASADA EN LISTA
# ==========================================
class EstructuraLista:

  def __init__(self):
    self.lista = []

  def insertar(self, estudiante: dict):
    # Inserción al final O(1)
    self.lista.append(estudiante)

  def buscar(self, id_estudiante: int):
    # Búsqueda lineal O(N)
    for est in self.lista:
      if est["id"] == id_estudiante:
        return est
    return None

  def listar_en_orden(self):
    # Para listar en orden por ID, ordenamos la lista O(N log N)
    return sorted(self.lista, key=lambda x: x["id"])


# ==========================================
# 2. ÁRBOL BINARIO DE BÚSQUEDA (ABB)
# ==========================================
class NodoABB:

  def __init__(self, estudiante: dict):
    self.estudiante = estudiante
    self.id = estudiante["id"]
    self.izq = None
    self.der = None


class ABB:

  def __init__(self):
    self.raiz = None

  def insertar(self, estudiante: dict):
    nuevo = NodoABB(estudiante)
    if self.raiz is None:
      self.raiz = nuevo
      return

    actual = self.raiz
    while True:
      if nuevo.id < actual.id:
        if actual.izq is None:
          actual.izq = nuevo
          break
        actual = actual.izq
      elif nuevo.id > actual.id:
        if actual.der is None:
          actual.der = nuevo
          break
        actual = actual.der
      else:
        # ID duplicado (no debería ocurrir según nuestro generador)
        break

  def buscar(self, id_estudiante: int):
    actual = self.raiz
    while actual:
      if id_estudiante == actual.id:
        return actual.estudiante
      elif id_estudiante < actual.id:
        actual = actual.izq
      else:
        actual = actual.der
    return None

  def listar_en_orden(self):
    # Recorrido in-order para obtener la lista ordenada por ID O(N)
    resultado = []

    def _in_order(nodo):
      if nodo:
        _in_order(nodo.izq)
        resultado.append(nodo.estudiante)
        _in_order(nodo.der)

    _in_order(self.raiz)
    return resultado


# ==========================================
# 3. ÁRBOL B+ (B+ TREE)
# ==========================================
class NodoBPlus:

  def __init__(self, es_hoja=False):
    self.es_hoja = es_hoja
    self.claves = []  # Lista de IDs
    self.hijos = (
        []
    )  # Punteros a nodos hijos (internos) o punteros a datos (hojas)
    self.siguiente = None  # Enlace al siguiente nodo hoja (secuencial)


class ArbolBPlus:

  def __init__(self, orden=4):
    self.raiz = NodoBPlus(es_hoja=True)
    self.orden = orden  # Número máximo de hijos/claves

  def buscar(self, id_estudiante: int):
    actual = self.raiz
    while not actual.es_hoja:
      i = 0
      while i < len(actual.claves) and id_estudiante >= actual.claves[i]:
        i += 1
      actual = actual.hijos[i]

    # Llegamos a la hoja, buscamos el valor
    for i, clave in enumerate(actual.claves):
      if clave == id_estudiante:
        return actual.hijos[i]  # Guarda el diccionario del estudiante
    return None

  def insertar(self, estudiante: dict):
    clave = estudiante["id"]
    raiz_actual = self.raiz

    if len(raiz_actual.claves) == self.orden - 1:
      nueva_raiz = NodoBPlus(es_hoja=False)
      nueva_raiz.hijos.append(self.raiz)
      self._dividir_hijo(nueva_raiz, 0)
      self.raiz = nueva_raiz
      self._insertar_no_lleno(self.raiz, clave, estudiante)
    else:
      self._insertar_no_lleno(raiz_actual, clave, estudiante)

  def _insertar_no_lleno(self, nodo, clave, estudiante):
    if nodo.es_hoja:
      i = 0
      while i < len(nodo.claves) and clave > nodo.claves[i]:
        i += 1
      nodo.claves.insert(i, clave)
      nodo.hijos.insert(i, estudiante)
    else:
      i = len(nodo.claves) - 1
      while i >= 0 and clave < nodo.claves[i]:
        i -= 1
      i += 1
      if len(nodo.hijos[i].claves) == self.orden - 1:
        self._dividir_hijo(nodo, i)
        if clave > nodo.claves[i]:
          i += 1
      self._insertar_no_lleno(nodo.hijos[i], clave, estudiante)

  def _dividir_hijo(self, padre, i):
    orden = self.orden
    hijo = padre.hijos[i]
    nuevo_nodo = NodoBPlus(es_hoja=hijo.es_hoja)

    mid = len(hijo.claves) // 2

    if hijo.es_hoja:
      nuevo_nodo.claves = hijo.claves[mid:]
      nuevo_nodo.hijos = hijo.hijos[mid:]
      hijo.claves = hijo.claves[:mid]
      hijo.hijos = hijo.hijos[:mid]

      nuevo_nodo.siguiente = hijo.siguiente
      hijo.siguiente = nuevo_nodo

      padre.claves.insert(i, nuevo_nodo.claves[0])
      padre.hijos.insert(i + 1, nuevo_nodo)
    else:
      clave_promovida = hijo.claves[mid]
      nuevo_nodo.claves = hijo.claves[mid + 1 :]
      nuevo_nodo.hijos = hijo.hijos[mid + 1 :]

      hijo.claves = hijo.claves[:mid]
      hijo.hijos = hijo.hijos[: mid + 1]

      padre.claves.insert(i, clave_promovida)
      padre.hijos.insert(i + 1, nuevo_nodo)

  def listar_en_orden(self):
    # Aprovecha las hojas enlazadas linealmente O(N)
    resultado = []
    actual = self.raiz
    while not actual.es_hoja:
      actual = actual.hijos[0]

    while actual:
      resultado.extend(actual.hijos)
      actual = actual.siguiente
    return resultado