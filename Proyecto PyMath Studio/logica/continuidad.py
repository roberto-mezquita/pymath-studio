from sympy import limit
from sympy import nan
from sympy import oo
from sympy import S
from sympy import simplify
from sympy import zoo

from utilidades.expresiones import interpretar_expresion
from utilidades.expresiones import x


def _es_valor_finito(valor):
    # Una funcion continua necesita un limite finito y un valor definido.
    return valor not in (oo, -oo, zoo, nan) and valor.is_finite is not False


def _son_equivalentes(valor_a, valor_b):
    # Compara expresiones matematicas aunque esten escritas de forma distinta.
    try:
        return simplify(valor_a - valor_b) == 0
    except Exception:
        return valor_a == valor_b


def _formatear_redefinicion(funcion, punto, valor):
    # Representa la funcion corregida para una discontinuidad removible.
    return (
        "F(x) = {\n"
        f"   {funcion}, si x != {punto}\n"
        f"   {valor}, si x = {punto}\n"
        "}"
    )


def analizar_continuidad(funcion_texto, punto_texto):
    # Interpreta la funcion y el punto con el mismo parser matematico.
    funcion = interpretar_expresion(funcion_texto)
    punto = simplify(interpretar_expresion(str(punto_texto)))

    if punto.has(x):
        raise ValueError("El punto de analisis debe ser un valor numerico.")

    procedimiento = [
        "1. Interpretamos la funcion y el punto de analisis.",
        f"   f(x) = {funcion}",
        f"   Punto: x = {punto}",
        "2. Calculamos el limite cuando x se acerca por la izquierda."
    ]

    limite_izquierdo = limit(
        funcion,
        x,
        punto,
        dir="-"
    )
    procedimiento.append(f"   Limite izquierdo: {limite_izquierdo}")

    procedimiento.append("3. Calculamos el limite cuando x se acerca por la derecha.")
    limite_derecho = limit(
        funcion,
        x,
        punto,
        dir="+"
    )
    procedimiento.append(f"   Limite derecho: {limite_derecho}")

    procedimiento.append("4. Evaluamos la funcion exactamente en el punto.")
    valor_funcion = simplify(funcion.subs(x, punto))
    procedimiento.append(f"   f({punto}) = {valor_funcion}")

    limites_iguales = _son_equivalentes(limite_izquierdo, limite_derecho)
    limite_finito = _es_valor_finito(limite_izquierdo) and _es_valor_finito(limite_derecho)
    valor_definido = _es_valor_finito(valor_funcion)
    valor_coincide = limites_iguales and _son_equivalentes(limite_izquierdo, valor_funcion)
    limite_general = simplify(limite_izquierdo) if limites_iguales else S.NaN

    procedimiento.append("5. Comparamos los resultados obtenidos.")
    procedimiento.append(f"   Limite por la izquierda: {limite_izquierdo}")
    procedimiento.append(f"   Limite por la derecha: {limite_derecho}")
    procedimiento.append(f"   Valor de la funcion en el punto: {valor_funcion}")

    if limites_iguales and limite_finito and valor_definido and valor_coincide:
        resultado = f"La funcion es continua en x = {punto}."
        procedimiento.append("   Los limites laterales son iguales y coinciden con f(x).")
        procedimiento.append("   No es necesario redefinir la funcion.")

    elif limites_iguales and limite_finito:
        resultado = (
            f"La funcion es discontinua removible en x = {punto}. "
            f"Para hacerla continua se redefine f({punto}) = {limite_general}."
        )
        procedimiento.append("   El limite existe, pero el valor de la funcion no coincide o no esta definido.")
        procedimiento.append("6. Redefinimos la funcion usando el valor del limite.")
        procedimiento.append(f"   Limite comun: {limite_general}")
        procedimiento.append("   Funcion redefinida:")
        procedimiento.append(_formatear_redefinicion(funcion, punto, limite_general))

    else:
        resultado = (
            f"La funcion es discontinua no removible en x = {punto}. "
            "No puede hacerse continua redefiniendo solo el valor en ese punto."
        )
        procedimiento.append("   Los limites laterales no coinciden o alguno no es finito.")
        procedimiento.append("6. Revisamos si se puede redefinir la funcion.")
        procedimiento.append(
            "   No existe un limite comun finito, por eso no hay un valor unico para f(x) en ese punto."
        )
        procedimiento.append("   Funcion redefinida: no aplica para corregir esta discontinuidad.")

    return resultado, procedimiento
