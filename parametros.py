from Punto4 import *
#Este archivo contiene las funciones que permiten analizar los parámetros de un código lineal.
def analisis_codigo_lineal(matriz_generadora, q):
  #Validación de la matriz generadora
  if not all(isinstance(fila, list) for fila in matriz_generadora):
    return "La matriz generadora debe ser una lista de listas."

  #Hallar los parámetros del código lineal
  dimension = len(matriz_generadora)
  print(matriz_generadora)
  longitud = len(matriz_generadora[0])
  distancia_minima = float('inf')
  
  #Hallar la distancia mínima
  for fila in matriz_generadora:
    peso = sum(1 for elemento in fila if elemento != 0)
    distancia_minima = min(distancia_minima, peso)

  cardinalidad = q ** dimension
  
  #Hallar los elementos del codigo
  elementos = dualcode_generator(matriz_generadora, q)
  
    

  return f"Longitud: {longitud}, Dimensión: {dimension}, Distancia mínima: {distancia_minima}, Cardinalidad: {cardinalidad}, Elementos: {elementos}"


