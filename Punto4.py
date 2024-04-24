from sympy import symbols, Eq, solve, Matrix
import re

import itertools
import numpy as np
from scipy import linalg
from punto2 import *


def generate_vectors(l, n):
    # Genera todos los posibles valores para cada posición del vector
    possible_values = list(range(n+1))  # Valores de 0 a n
    # Genera todas las combinaciones posibles de valores para cada posición del vector
    all_combinations = itertools.product(possible_values, repeat=l)
    # Convierte las combinaciones en listas para obtener vectores
    vectors = [list(combination) for combination in all_combinations]
    
    return vectors

def find_control_mat(mat, q):
    # Se halla la matriz de control usando H = [-At | In-k]
    mat=np.array(mat)
    #k es el número de filas de la matriz
    #n es el número de columnas de la matriz
    k, n = mat.shape
    if k != n:
        # Se halla la matriz At
        At = np.array(mat[:, -(n-k):])
        At = np.transpose(At)
        # Se halla la matriz -At y se convierte en una lista, además se halla el módulo q
        for i in range(n-k):
            At[i] = (-1*At[i])%q
        At = At.tolist()
        # Hallo la matriz identidad que representa el resto de la generadora y se convierte en una lista
        I = np.eye(n-k).astype(int).tolist()
        H=[]
        # Se halla la matriz de control, uniéndose las matrices -At e I
        for i in range(n-k):
            H.append(At[i]+I[i]) 
        H = np.array(H)
        
        return H
    else:
        return 'El codigo no tiene Código Dual/Matriz de Control'

def dualcode_generator(H, q):
    H = np.array(H)
    k, n = H.shape
    #Genera el campo
    field=generate_vectors(k,q-1)
    code=[]
    for v in field:
        sum=np.array([0]*n)
        #Realiza las combinaciones
        for i in range(k):
            sum = sum + (H[i]*v[i])%q
        sum = (sum%q).tolist()
        #Se añaden los elementos al codigo
        if not sum in code:
            code.append(sum)
    # print('Codigo Dual:\n',code)
    return code

#Define el tipo de código dual
def auto_type(lineal, dual):
    isIn = all(elem in dual for elem in lineal)
    if len(lineal) == len(dual) and isIn:
        return 'El codigo es auto-dual'
    elif isIn:
        return 'El codigo es auto-ortogonal'
    else:
        return 'El codigo no se puede categorizar'
    
def codigo_dual(matriz, q):
    sup=list(matriz)
    if es_codigo_lineal_Zn(matriz, q) and revisar_Zn(matriz, q):
        # Se obtiene la forma escalonada reducida
        RREF_Zn = ToReducedRowEchelonForm_Zn(matriz, q)
        RREF_Zn = eliminar_filas_nulas(RREF_Zn)
        H=find_control_mat(RREF_Zn,q)
        if H.any():
            code=dualcode_generator(H,q)
            typo = auto_type(sup,code)
            return f"El código dual es: {code} \n {typo}"
    else:
        return "No es un subespacio vectorial o no pertenece a Zn"

# Código de resolución de sistema de ecuaciones para hallar la matriz de control
def resolver_sistema_ecuaciones(mat, term):
        # Crear símbolos para las variables
        n=len(mat[0])
        variables = symbols('A:{}'.format(chr(ord('A') + n-1)))
        # Crear ecuaciones a través de la multiplicación de matrices
        ecuaciones = [Eq(sum([mat[i][j] * variables[j] for j in range(len(variables))]), term[i]) for i in range(len(mat))]
        # Resolver el sistema de ecuaciones
        soluciones = solve(ecuaciones, variables)
        
        # Imprimir las soluciones. Se incluyen las variables independientes
        for var in variables:
            if var not in soluciones.keys():
                soluciones[var]= soluciones[var]=var 
        
        #Se coloca en un diccionario ordenado y se extraen los coeficientes
        soluciones = {key: str(value) for key, value in soluciones.items()}
        soluciones = {str(clave): valor for clave, valor in soluciones.items()}
        soluciones = {k: soluciones[k] for k in sorted(soluciones)}
        #print(soluciones)
        return extraer_coeficientes(soluciones)

# Código de formateo de la expresión. Sepaea los coeficientes de las variables. Con este formato (coeficiente)variable)
def extraer_coeficientes(diccionario):
    nuevo_diccionario = {}
    f ={}
    for key, value in diccionario.items():
        # Encuentra todos los coeficientes y variables en la expresión
        coeficientes = re.findall(r'([-+]?\d*\.?\d*)\*?([A-Za-z]+)', value)
        f[key] = extraer_fracciones(value)
        # Formatea los coeficientes como (coeficiente)variable
        #coeficientes_formateados = [(f"({c})" if c != '-' else '(-1)') + v for c, v in coeficientes]
        coeficientes = [(f"({c})" if c != '+' else '(1)') + v for c, v in coeficientes]
        # Forma la nueva expresión
        nueva_expresion = '+'.join(coeficientes)
        nueva_expresion = nueva_expresion.replace('()', '(1)')
        nueva_expresion = nueva_expresion.replace('(-)', '(-1)')
        nuevo_diccionario[key] = nueva_expresion
    #print(nuevo_diccionario)
    #print(f)
        #Cuando encuentra un paréntesis, se añade la fracción
    for clave, valores in f.items():
        
        if f[clave]:
            pos=[]
            #print(nuevo_diccionario[clave])
            for i, char in enumerate(nuevo_diccionario[clave]):
                if char == ')':
                    if i > 0 and nuevo_diccionario[clave][i-1].isdigit():
                        # Verificar si hay un '/' antes del número
                        if i > 1 and nuevo_diccionario[clave][i-2] == '/':
                            pos.append(i)

            for i in range(len(pos)):
                nuevo_diccionario[clave] = nuevo_diccionario[clave][:pos[i]+(i*2)] + f'/{f[clave][i]})' + nuevo_diccionario[clave][pos[i]+1+(i*2):]
    return nuevo_diccionario

# Extrae las fracciones de la expresión, las formatea y las añade a la expresión
def extraer_fracciones(cadena):
    simbolos = []
    i = 0
    while i < len(cadena):
        if cadena[i].isalpha():
            j = i + 1
            while j < len(cadena) and cadena[j] != '+' and cadena[j] != '-':
                if cadena[j] == '/':
                    j += 1
                    simbolo = ''
                    while j < len(cadena) and cadena[j] != '+' and cadena[j] != '-':
                        simbolo += cadena[j]
                        j += 1
                    simbolos.append(simbolo)
                else:
                    j += 1
            i = j
        else:
            i += 1
    return simbolos

# Convierte a Zp los coeficientes
def convertir_coef (dicc, q):
    for clave, valor in dicc.items():
        subs = re.findall(r'\((.*?)\)', valor)
        for i in range(len(subs)):
            if '/' not in subs[i]:
                dicc[clave]=dicc[clave].replace(f'({subs[i]})',str(int(subs[i])%q))
            else:
                parts=subs[i].split('/')
                num=str((int(parts[0])%q * pow(int(parts[1]), -1, q))%q)
                dicc[clave]=dicc[clave].replace(f'({subs[i]})',num)
    return dicc



def mat_control(sis):
    #Se crea la matriz de control
    #Se buscan las posiciones de las variables
    #Representan sacar el factor común de las variables, para hallar los elementos de la matriz
    H=[]
    for clave in sis:
        cl=str(clave)
        x=[]
        for clave in sis:
            v=str(sis[clave])
            if cl in v:
                pos=v.find(cl)
                x.append(int(v[pos-1]))
            else:
                x.append(0)
        t=all(e == 0 for e in x)
        if not t:
            H.append(x)
    return H

#! Algoritmo Matriz Generadora a Matriz de Control
"""
    Para obtener la matriz de control:  
    1. Se debe resolver el sistema de ecuaciones Gx^t=0.
    2. Se deben convertir los coeficientes a Zp.
    3. Se obtiene la matriz de control.
"""

def matriz_control(mat, q):
    if revisar_Zn(mat, q):
        # Se obtiene la forma escalonada reducida
        RREF_Zn = ToReducedRowEchelonForm_Zn(mat, q)
        RREF_Zn = eliminar_filas_nulas(RREF_Zn)
        H=find_control_mat(RREF_Zn,q)
        if H.any():
            return f"La matriz de control es: {H}"
    else:
        return "No pertenece a Zn"



