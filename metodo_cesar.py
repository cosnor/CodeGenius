#funcion para cifrar por el metodo cesar
def cifrado_cesar(frase:str, n: int)-> str:
    frase = convertir_a_mayusculas(frase)
    if validacion_caracteres(frase) is False:
        return "Error: la frase contiene caracteres no permitidos"
    lista_caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ " #mod 27
    frase_cifrada = ""
    for letra in frase:
        indice = lista_caracteres.index(letra)
        indice = (indice + n) % 27
        frase_cifrada += lista_caracteres[indice]
        
    return frase_cifrada

#funcion para descifrar por el metodo cesar
def descifrado_cesar(frase:str, n: int)-> str:
    frase = convertir_a_mayusculas(frase)
    if validacion_caracteres(frase) is False:
        return "Error: la frase contiene caracteres no permitidos"
    lista_caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ " #mod 27
    frase_descifrada = ""
    for letra in frase:
        indice = lista_caracteres.index(letra)
        indice = (indice - n) % 27
        frase_descifrada += lista_caracteres[indice]
        
    return frase_descifrada

#funcion para validar que la frase solo contenga caracteres permitidos
def validacion_caracteres(frase:str)-> bool:
    lista_caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ " #mod 27
    for letra in frase:
        if letra not in lista_caracteres:
            return False
    return True

#funcion para convertir la frase a mayusculas
def convertir_a_mayusculas(frase:str)-> str:
    return frase.upper()
