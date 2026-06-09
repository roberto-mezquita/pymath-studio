def validar_vacio(texto):
    # Verifica que el campo tenga algun contenido real.
    return texto.strip() != ""


def validar_numero(numero):
    # Comprueba si el texto puede convertirse a numero decimal.
    try:
        float(numero)
        return True

    except ValueError:
        return False
