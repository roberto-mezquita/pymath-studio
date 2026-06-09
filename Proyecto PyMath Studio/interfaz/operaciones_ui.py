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
from logica.operaciones import resolver_operacion
from utilidades.validaciones import validar_numero


class VentanaOperaciones:

    def __init__(self, master=None):
        # Esta ventana resuelve operaciones basicas y explica el calculo.
        self.ventana = tk.Toplevel(master) if master else tk.Tk()
        configurar_ventana(
            self.ventana,
            "Operaciones - PyMath Studio",
            "920x680",
            (820, 600)
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
            "Operaciones Matematicas",
            "Ingrese dos numeros y elija la operacion. Para raiz cuadrada solo se usa el primer numero."
        )

        self.numero1 = crear_campo(
            contenedor,
            "Primer numero (a)",
            ancho=22,
            ayuda="Ejemplo: 8"
        )

        self.numero2 = crear_campo(
            contenedor,
            "Segundo numero (b)",
            ancho=22,
            ayuda="Ejemplo: 2"
        )

        marco_botones = tk.Frame(
            contenedor,
            bg=COLOR_FONDO
        )
        marco_botones.pack(pady=(8, 0))

        operaciones = [
            ("Sumar", "suma"),
            ("Restar", "resta"),
            ("Multiplicar", "multiplicacion"),
            ("Dividir", "division"),
            ("Potencia", "potencia"),
            ("Raiz", "raiz")
        ]

        # Se crea un boton por cada operacion disponible.
        for indice, (texto, operacion) in enumerate(operaciones):
            boton = crear_boton(
                marco_botones,
                texto,
                lambda operacion=operacion: self.realizar_operacion(operacion),
                color=COLOR_SECUNDARIO if indice < 3 else "#2F80ED",
                color_activo=COLOR_SECUNDARIO_ACTIVO if indice < 3 else "#1C67C7",
                ancho=16
            )
            boton.grid(
                row=indice // 3,
                column=indice % 3,
                padx=7,
                pady=7
            )

        self.resultado = crear_area_texto(contenedor, alto=10)
        self._mostrar_mensaje_inicial()

        if master is None:
            self.ventana.mainloop()

    def _mostrar_mensaje_inicial(self):
        # Indica que el area inferior mostrara el desarrollo del ejercicio.
        self.resultado.delete("1.0", tk.END)
        self.resultado.insert(
            tk.END,
            "El procedimiento de la operacion aparecera aqui."
        )

    def realizar_operacion(self, operacion):
        # Convierte las entradas a numeros, resuelve la operacion y guarda el resultado.
        numero1 = self.numero1.get().strip()
        numero2 = self.numero2.get().strip()

        if not validar_numero(numero1):
            messagebox.showerror(
                "Dato invalido",
                "Ingrese un primer numero valido."
            )
            return

        if operacion != "raiz" and not validar_numero(numero2):
            messagebox.showerror(
                "Dato invalido",
                "Ingrese un segundo numero valido."
            )
            return

        try:
            valor1 = float(numero1)
            valor2 = float(numero2) if operacion != "raiz" else None
            resultado, procedimiento = resolver_operacion(operacion, valor1, valor2)

            self.resultado.delete("1.0", tk.END)
            for paso in procedimiento:
                self.resultado.insert(tk.END, paso + "\n")

            self.resultado.insert(
                tk.END,
                f"\nResultado final: {resultado}"
            )

            guardar_ejercicio({
                "tipo": f"Operacion: {operacion}",
                "funcion": f"a = {valor1}, b = {valor2}",
                "resultado": str(resultado),
                "procedimiento": procedimiento,
                "fecha": datetime.now()
            })

        except Exception as error:
            messagebox.showerror(
                "No se pudo calcular",
                str(error)
            )
