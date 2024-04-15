def codigo_desde_matriz_generadora(matriz_generadora):
    longitud_codigo = len(matriz_generadora[0])   
    dimension_codigo = len(matriz_generadora)   
    distancia_minima = calcular_distancia_minima(matriz_generadora)
    cardinalidad = 2 ** (longitud_codigo - dimension_codigo)
    return longitud_codigo, dimension_codigo, distancia_minima, cardinalidad

def calcular_distancia_minima(matriz_generadora):
    distancia_minima = float('inf')
    for i in range(len(matriz_generadora[0])):
        for j in range(i + 1, len(matriz_generadora[0])):
            distancia = calcular_distancia_entre_columnas(matriz_generadora, i, j)
            if distancia < distancia_minima and distancia != 0:
                distancia_minima = distancia
    return distancia_minima

def calcular_distancia_entre_columnas(matriz_generadora, col1, col2):
    distancia = 0
    for fila in matriz_generadora:
        if fila[col1] != fila[col2]:
            distancia += 1
    return distancia

# # # Ejemplo de matriz generadora
# matriz_generadora_lista = [[1,0,0]  ,[0,1,1]]

# longitud_codigo, dimension_codigo, distancia_minima, cardinalidad = codigo_desde_matriz_generadora(matriz_generadora_lista)

# print("Elementos del código:")
# for fila in matriz_generadora_lista:
#    print(fila)
   
# print("\nParámetros del código:")
# print("Longitud del código:", longitud_codigo)
# print("Dimensión del código:", dimension_codigo)
# print("Distancia mínima del código:", distancia_minima)
# print("\nCardinalidad del código:", cardinalidad)