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
from logica.continuidad import analizar_continuidad
from utilidades.exportador import exportar_txt
from utilidades.validaciones import validar_vacio


class VentanaContinuidad:

    def __init__(self, master=None):
        # La ventana permite analizar continuidad sin depender de una cuenta.
        self.ventana = tk.Toplevel(master) if master else tk.Tk()
        configurar_ventana(
            self.ventana,
            "Continuidad - PyMath Studio",
            "980x740",
            (880, 650)
        )

        contenedor = tk.Frame(
            self.ventana,
            bg=COLOR_FONDO
        )
        contenedor.pack(fill="both", expand=True, padx=46, pady=24)

        crear_imagen(
            contenedor,
            "logo.png",
            210,
            115,
            pady=(0, 4)
        )

        crear_titulo(
            contenedor,
            "Analisis de Continuidad",
            "Calcula limites laterales, evalua el punto y determina si la funcion es continua."
        )

        self.entry_funcion = crear_campo(
            contenedor,
            "Funcion f(x)",
            ayuda="Ejemplo: (x^2 - 1)/(x - 1), sin(x)/x o 1/(x - 2)"
        )

        self.entry_punto = crear_campo(
            contenedor,
            "Punto a analizar",
            ancho=20,
            ayuda="Ejemplo: 1"
        )

        marco_botones = tk.Frame(
            contenedor,
            bg=COLOR_FONDO
        )
        marco_botones.pack(pady=(8, 0))

        boton_analizar = crear_boton(
            marco_botones,
            "Analizar continuidad",
            self.analizar,
            color=COLOR_SECUNDARIO,
            color_activo=COLOR_SECUNDARIO_ACTIVO
        )
        boton_analizar.grid(row=0, column=0, padx=8)

        boton_exportar = crear_boton(
            marco_botones,
            "Exportar TXT",
            self.exportar,
            color="#8E44AD",
            color_activo="#6C3483"
        )
        boton_exportar.grid(row=0, column=1, padx=8)

        self.texto = crear_area_texto(contenedor, alto=16)
        self._mostrar_mensaje_inicial()

        if master is None:
            self.ventana.mainloop()

    def _mostrar_mensaje_inicial(self):
        # Mensaje de espera antes de calcular.
        self.texto.delete("1.0", tk.END)
        self.texto.insert(
            tk.END,
            "Ingrese una funcion y un punto para ver el analisis de continuidad paso a paso."
        )

    def analizar(self):
        # Valida los datos, calcula limites laterales y muestra la conclusion.
        funcion = self.entry_funcion.get().strip()
        punto = self.entry_punto.get().strip()

        if not validar_vacio(funcion) or not validar_vacio(punto):
            messagebox.showerror(
                "Datos faltantes",
                "Ingrese una funcion y el punto que desea analizar."
            )
            return

        try:
            resultado, procedimiento = analizar_continuidad(
                funcion,
                punto
            )

            self.texto.delete("1.0", tk.END)
            for paso in procedimiento:
                self.texto.insert(tk.END, paso + "\n")

            self.texto.insert(
                tk.END,
                f"\nResultado final: {resultado}"
            )

            guardar_ejercicio({
                "tipo": "Continuidad",
                "funcion": f"{funcion} en x = {punto}",
                "resultado": resultado,
                "procedimiento": procedimiento,
                "fecha": datetime.now()
            })

        except Exception as error:
            messagebox.showerror(
                "Datos invalidos",
                f"No se pudo analizar la continuidad.\nDetalle: {error}"
            )

    def exportar(self):
        # Exporta el procedimiento mostrado en pantalla.
        contenido = self.texto.get("1.0", tk.END).strip()
        if not contenido or contenido.startswith("Ingrese una funcion"):
            messagebox.showwarning(
                "Sin resultado",
                "Primero analice una funcion para poder exportarla."
            )
            return

        exportar_txt(
            "resultado_continuidad.txt",
            contenido
        )

        messagebox.showinfo(
            "Correcto",
            "Resultado exportado en resultado_continuidad.txt"
        )
