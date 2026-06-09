import tkinter as tk
from datetime import datetime
from tkinter import messagebox

from database.historial_db import guardar_ejercicio
from interfaz.componentes import COLOR_FONDO
from interfaz.componentes import COLOR_SECUNDARIO
from interfaz.componentes import COLOR_SECUNDARIO_ACTIVO
from interfaz.componentes import configurar_ventana
from interfaz.componentes import crear_area_texto
from interfaz.componentes import crear_boton
from interfaz.componentes import crear_campo
from interfaz.componentes import crear_imagen
from interfaz.componentes import crear_titulo
from logica.graficador import graficar_funcion
from utilidades.validaciones import validar_numero
from utilidades.validaciones import validar_vacio


class VentanaGraficas:

    def __init__(self, master=None):
        # Ventana dedicada a graficar funciones de una variable.
        self.ventana = tk.Toplevel(master) if master else tk.Tk()
        configurar_ventana(
            self.ventana,
            "Graficador - PyMath Studio",
            "940x660",
            (820, 590)
        )

        contenedor = tk.Frame(
            self.ventana,
            bg=COLOR_FONDO
        )
        contenedor.pack(fill="both", expand=True, padx=46, pady=24)

        crear_imagen(
            contenedor,
            "logo.png",
            200,
            110,
            pady=(0, 4)
        )

        crear_titulo(
            contenedor,
            "Graficador Matematico",
            "Ingrese una funcion y el intervalo que desea observar en el eje x."
        )

        self.entry_funcion = crear_campo(
            contenedor,
            "Funcion f(x)",
            ayuda="Ejemplo: sin(x), x^2 - 4 o 1/x"
        )

        self.entry_minimo = crear_campo(
            contenedor,
            "Valor minimo de x",
            ancho=20,
            ayuda="Ejemplo: -10"
        )
        self.entry_minimo.insert(0, "-10")

        self.entry_maximo = crear_campo(
            contenedor,
            "Valor maximo de x",
            ancho=20,
            ayuda="Ejemplo: 10"
        )
        self.entry_maximo.insert(0, "10")

        boton = crear_boton(
            contenedor,
            "Graficar funcion",
            self.graficar,
            color=COLOR_SECUNDARIO,
            color_activo=COLOR_SECUNDARIO_ACTIVO
        )
        boton.pack(pady=(8, 0))

        self.texto = crear_area_texto(contenedor, alto=6)
        self.texto.insert(
            tk.END,
            "Al graficar se abrira una ventana de Matplotlib con la curva solicitada."
        )

        if master is None:
            self.ventana.mainloop()

    def graficar(self):
        # Valida la funcion y el intervalo antes de abrir la grafica.
        funcion = self.entry_funcion.get().strip()
        minimo = self.entry_minimo.get().strip()
        maximo = self.entry_maximo.get().strip()

        if not validar_vacio(funcion):
            messagebox.showerror(
                "Dato faltante",
                "Ingrese una funcion para graficar."
            )
            return

        if not validar_numero(minimo) or not validar_numero(maximo):
            messagebox.showerror(
                "Intervalo invalido",
                "Ingrese valores numericos para el minimo y maximo de x."
            )
            return

        try:
            minimo = float(minimo)
            maximo = float(maximo)
            resumen = graficar_funcion(funcion, minimo, maximo)

            self.texto.delete("1.0", tk.END)
            self.texto.insert(tk.END, resumen)

            guardar_ejercicio({
                "tipo": "Grafica",
                "funcion": funcion,
                "resultado": f"Intervalo [{minimo}, {maximo}]",
                "procedimiento": [
                    f"1. Se interpreto la funcion f(x) = {funcion}.",
                    f"2. Se evaluo la funcion entre x = {minimo} y x = {maximo}.",
                    "3. Se dibujo la curva en una ventana de Matplotlib."
                ],
                "fecha": datetime.now()
            })

        except Exception as error:
            messagebox.showerror(
                "No se pudo graficar",
                f"Revise la funcion o el intervalo.\nDetalle: {error}"
            )
