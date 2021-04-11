
def ValidarIdentificacion(cadena): # Valida que el telefono o identificacion no se ingresen numeros
    valido = 0
    for i in range(len(cadena)):
        if cadena[i].islower() or cadena[i].isupper():
            valido += 1
    if valido > 0:
        return True        

def ValodarCantidadIdentificacion(cadena):
    long = len(cadena)
    if long > 9 or long < 9:
        return True

def ValidarVacio(cadena):
    lonCadena = len(cadena)
    if lonCadena == 0:
        return True
        
def ValidarContrasenna(cadena):
    cadena = len(cadena)
    if cadena < 8:
        return True




        