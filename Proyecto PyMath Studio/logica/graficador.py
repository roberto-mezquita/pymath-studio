import matplotlib.pyplot as plt
import numpy as np

from utilidades.expresiones import interpretar_expresion
from utilidades.expresiones import x
from sympy import lambdify


def graficar_funcion(funcion_texto, minimo=-10, maximo=10):
    # Convierte la entrada en una funcion que NumPy puede evaluar.
    if minimo >= maximo:
        raise ValueError("El valor minimo de x debe ser menor que el valor maximo.")

    funcion = interpretar_expresion(funcion_texto)
    funcion_numpy = lambdify(
        x,
        funcion,
        "numpy"
    )

    # Genera suficientes puntos para que la curva se vea suave.
    valores_x = np.linspace(
        minimo,
        maximo,
        600
    )

    with np.errstate(all="ignore"):
        valores_y = funcion_numpy(valores_x)

    if np.isscalar(valores_y):
        valores_y = np.full_like(
            valores_x,
            valores_y,
            dtype=float
        )
    else:
        valores_y = np.asarray(
            valores_y,
            dtype=float
        )

    # Solo se grafican valores finitos para evitar lineas incorrectas en asintotas.
    mascara = np.isfinite(valores_y)
    if not np.any(mascara):
        raise ValueError("La funcion no tiene valores reales finitos en ese intervalo.")

    plt.figure(figsize=(8.5, 5.5))
    plt.plot(
        valores_x[mascara],
        valores_y[mascara],
        color="#2F80ED",
        linewidth=2
    )
    plt.axhline(0, color="#555555", linewidth=1)
    plt.axvline(0, color="#555555", linewidth=1)
    plt.title(f"Grafica de f(x) = {funcion}")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True, linestyle="--", alpha=0.45)
    plt.tight_layout()
    plt.show()

    return (
        f"Funcion graficada: f(x) = {funcion}\n"
        f"Intervalo usado: [{minimo}, {maximo}]\n"
        "La ventana de Matplotlib muestra la curva con ejes y cuadricula para facilitar la lectura."
    )
