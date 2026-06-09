from sympy import E
from sympy import acos
from sympy import asin
from sympy import atan
from sympy import cos
from sympy import exp
from sympy import log
from sympy import pi
from sympy import sin
from sympy import sqrt
from sympy import symbols
from sympy import tan
from sympy.parsing.sympy_parser import convert_xor
from sympy.parsing.sympy_parser import implicit_multiplication_application
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations


x = symbols("x")

TRANSFORMACIONES = standard_transformations + (
    implicit_multiplication_application,
    convert_xor
)

NOMBRES_PERMITIDOS = {
    "x": x,
    "pi": pi,
    "e": E,
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "asin": asin,
    "acos": acos,
    "atan": atan,
    "sqrt": sqrt,
    "log": log,
    "ln": log,
    "exp": exp
}


def interpretar_expresion(texto):
    # Acepta escritura comun como x^2, 2x o sin(x) y la convierte a SymPy.
    return parse_expr(
        texto,
        local_dict=NOMBRES_PERMITIDOS,
        transformations=TRANSFORMACIONES
    )
