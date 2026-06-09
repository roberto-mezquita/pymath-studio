import math


def suma(a, b):
    # Suma dos numeros.
    return a + b


def resta(a, b):
    # Resta el segundo numero al primero.
    return a - b


def multiplicacion(a, b):
    # Multiplica dos numeros.
    return a * b


def division(a, b):
    # Evita dividir entre cero para no generar un resultado indefinido.
    if b == 0:
        raise ValueError("No se puede dividir entre cero.")

    return a / b


def potencia(a, b):
    # Eleva el primer numero a la potencia indicada por el segundo.
    return a ** b


def raiz(a):
    # Calcula la raiz cuadrada solo para numeros no negativos.
    if a < 0:
        raise ValueError("No se puede calcular la raiz cuadrada real de un numero negativo.")

    return math.sqrt(a)


def resolver_operacion(operacion, a, b=None):
    # Centraliza las operaciones para que la interfaz pueda mostrar un procedimiento claro.
    procedimientos = {
        "suma": (
            suma,
            "+",
            "Sumamos el primer numero con el segundo."
        ),
        "resta": (
            resta,
            "-",
            "Restamos el segundo numero al primero."
        ),
        "multiplicacion": (
            multiplicacion,
            "*",
            "Multiplicamos ambos numeros."
        ),
        "division": (
            division,
            "/",
            "Dividimos el primer numero entre el segundo."
        ),
        "potencia": (
            potencia,
            "^",
            "Elevamos el primer numero a la potencia del segundo."
        )
    }

    if operacion == "raiz":
        resultado = raiz(a)
        procedimiento = [
            "1. Identificamos la operacion solicitada: raiz cuadrada.",
            f"2. Tomamos el numero a = {a}.",
            f"3. Calculamos sqrt({a}) = {resultado}."
        ]
        return resultado, procedimiento

    if operacion not in procedimientos:
        raise ValueError("Operacion no reconocida.")

    funcion, simbolo, explicacion = procedimientos[operacion]
    resultado = funcion(a, b)

    procedimiento = [
        f"1. Identificamos la operacion solicitada: {operacion}.",
        f"2. Tomamos los valores a = {a} y b = {b}.",
        f"3. {explicacion}",
        f"   {a} {simbolo} {b} = {resultado}"
    ]

    return resultado, procedimiento
