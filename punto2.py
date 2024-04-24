import math
#Calcular las bases del codigo
def ToReducedRowEchelonForm_Zn(M, n):
    # Verificar si la matriz es vacía
    if not M:
        return None

    # Inicialización de variables
    lead = 0
    rowCount = len(M)
    columnCount = len(M[0])

    # Iterar sobre cada fila de la matriz
    for r in range(rowCount):
        # Si el índice de la columna líder excede el número de columnas,
        # la matriz ya está en su forma reducida
        if lead >= columnCount:
            return M
        # Encontrar la fila con el valor líder no nulo más abajo
        i = r
        while M[i][lead] == 0:
            i += 1
            # Si se alcanza la última fila, resetear 'i' y pasar a la siguiente columna
            if i == rowCount:
                i = r
                lead += 1
                # Si se ha alcanzado la última columna, la matriz está en su forma reducida
                if columnCount == lead:
                    return M
        # Intercambiar la fila actual con la fila encontrada
        M[i], M[r] = M[r], M[i]
        # Normalizar la fila para que el líder sea 1
        lv = M[r][lead]
        M[r] = [(mrx * pow(lv, -1, n)) % n for mrx in M[r]]
        # Eliminar todos los otros valores en la columna líder
        for i in range(rowCount):
            if i != r:
                lv = M[i][lead]
                M[i] = [(iv - (lv * rv) % n) % n for rv, iv in zip(M[r], M[i])]
        # Pasar a la siguiente columna
        lead += 1

    return M

#all: revisa si todos los elementos son verdaderos con esa condición
def eliminar_filas_nulas(matriz):
    matriz_filtrada = [vector for vector in matriz if not all(elemento == 0 for elemento in vector)]
    return matriz_filtrada

#Revisa si pertenece y si tiene la misma longitud
def revisar_Zn(matriz, n):
  #Está en Zn?
  posible = [i for i in range(n)]
  for i in range(len(matriz)):
    for j in range(len(matriz[0])): #revisar
      if matriz[i][j] not in posible :
        return False
  #Tiene la misma longitud?
  for i in range(len(matriz)):
    for j in range(len(matriz)): #revisar
      if len(matriz[i]) != len(matriz[j]):
        return False
  return True

#Validar si es un codigo lineal
def suma_modulo(vector1, vector2, n):
    return [(x + y) % n for x, y in zip(vector1, vector2)]

def multiplicacion_escalar_modulo(vector, escalar, n):
    return [(x * escalar) % n for x in vector]

def es_codigo_lineal_Zn(vectores, n):
    # Verificar la existencia de al menos un vector
    if not vectores:
        return False

    # Verificar la dimensión de los vectores
    dim = len(vectores[0])
    for vector in vectores:
        if len(vector) != dim:
            return False

    # Verificar la existencia del vector cero
    vector_cero = [0] * dim
    if vector_cero not in vectores:
        return False

    # Verificar la cerradura bajo la suma
    for i in range(len(vectores)):
        for j in range(len(vectores)):
            suma = suma_modulo(vectores[i], vectores[j], n)
            if suma not in vectores:
                return False

    # Verificar la cerradura bajo la multiplicación por un escalar
    for vector in vectores:
        for escalar in range(n):
            multiplicacion = multiplicacion_escalar_modulo(vector, escalar, n)
            if multiplicacion not in vectores:
                return False

    return True

def matriz_generadora(matriz, n):
    if es_codigo_lineal_Zn(matriz, n) and revisar_Zn(matriz, n):
        RREF_Zn = ToReducedRowEchelonForm_Zn(matriz, n)
        RREF_Zn = eliminar_filas_nulas(RREF_Zn)
        return f"La matriz generadora del codigo es: {RREF_Zn}\nEl codigo es un [{len(matriz[0])}, {math.log(len(matriz), n)}]{n}-codigo"
    else:
        return "No es un subespacio vectorial o no pertenece a Zn"
    
