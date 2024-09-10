import re
from itertools  import cycle

def validar_soloString(dato):
    regex = r'[a-zA-Z]{3,}'
    if dato=="":
        return False
    if re.match(regex,dato):
        return True
    else:

        return False
def validar_numCelular(numero):
    regex = r"^(\+?56)?(\s?)(0?9)(\s?)[98765432]\d{7}$"#puede llevar o no +56 pero debe llevar 9 y el total de digitos debe ser 7 (sin contar  56)

    if re.match(regex,numero):
        return True
    else:
        return False

def validar_int(dato):
    try:
        valor = int(dato)
        if valor=="":
            return False
        if valor >= 0:
            return True
        else:
            return False
    except ValueError:
        return False



def validar_rut(cadena):
    try:
        # Dividimos la cadena por el guion
        partes = cadena.split('-')
        # El dÃgito verificador es la segunda parte de la cadena
        if len(partes) == 2:
            #digito verificador de la cadena recibida pasado a minuscula
            digito_verificador =  partes[1].lower() 
            reversed_digits = map(int, reversed(str(partes[0])))
            factors = cycle(range(2, 8))
            s = sum(d * f for d, f in zip(reversed_digits, factors))
            digito_verificador_calculado = (-s) % 11 if (-s) % 11 < 10 else 'k'
            if digito_verificador == str(digito_verificador_calculado):
                return True
            else:
                return  False
        else:
            return False
    except Exception:
        return False


def validar_email(email):
    regex = r'^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,4}$'
    if re.match(regex, email):
        return True
    else:
        return False
