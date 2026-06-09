import tkinter as tk
from tkinter import messagebox

from database.historial_db import eliminar_historial
from database.historial_db import obtener_historial
from interfaz.componentes import COLOR_FONDO
from interfaz.componentes import COLOR_PELIGRO
from interfaz.componentes import COLOR_PELIGRO_ACTIVO
from interfaz.componentes import configurar_ventana
from interfaz.componentes import crear_area_texto
from interfaz.componentes import crear_boton
from interfaz.componentes import crear_imagen
from interfaz.componentes import crear_titulo


class VentanaHistorial:

    def __init__(self, master=None):
        # Muestra todos los ejercicios guardados, sin filtrar por cuenta.
        self.ventana = tk.Toplevel(master) if master else tk.Tk()
        configurar_ventana(
            self.ventana,
            "Historial - PyMath Studio",
            "980x700",
            (860, 620)
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
            "Historial de Ejercicios",
            "Consulta los ejercicios resueltos durante el uso de la aplicacion."
        )

        marco_botones = tk.Frame(
            contenedor,
            bg=COLOR_FONDO
        )
        marco_botones.pack(pady=(0, 8))

        boton_actualizar = crear_boton(
            marco_botones,
            "Actualizar",
            self.cargar_historial,
            ancho=14
        )
        boton_actualizar.grid(row=0, column=0, padx=8)

        boton_limpiar = crear_boton(
            marco_botones,
            "Limpiar historial",
            self.limpiar_historial,
            color=COLOR_PELIGRO,
            color_activo=COLOR_PELIGRO_ACTIVO,
            ancho=16
        )
        boton_limpiar.grid(row=0, column=1, padx=8)

        self.texto = crear_area_texto(contenedor, alto=18)
        self.cargar_historial()

        if master is None:
            self.ventana.mainloop()

    def cargar_historial(self):
        # Carga los registros guardados y los muestra con su procedimiento.
        self.texto.delete("1.0", tk.END)
        historial = obtener_historial()

        if not historial:
            self.texto.insert(
                tk.END,
                "Aun no hay ejercicios guardados."
            )
            return

        for indice, ejercicio in enumerate(historial, start=1):
            fecha = ejercicio.get("fecha", "Sin fecha")
            procedimiento = ejercicio.get("procedimiento", [])

            self.texto.insert(tk.END, f"Ejercicio {indice}\n")
            self.texto.insert(tk.END, f"Fecha: {fecha}\n")
            self.texto.insert(tk.END, f"Tipo: {ejercicio.get('tipo', 'Sin tipo')}\n")
            self.texto.insert(tk.END, f"Funcion / datos: {ejercicio.get('funcion', 'Sin datos')}\n")
            self.texto.insert(tk.END, f"Resultado: {ejercicio.get('resultado', 'Sin resultado')}\n")

            if procedimiento:
                self.texto.insert(tk.END, "Procedimiento:\n")
                for paso in procedimiento:
                    self.texto.insert(tk.END, f"{paso}\n")

            self.texto.insert(tk.END, "-" * 72 + "\n")

    def limpiar_historial(self):
        # Borra el historial completo solo despues de confirmar.
        confirmar = messagebox.askyesno(
            "Confirmar",
            "Desea eliminar todo el historial de ejercicios?"
        )

        if confirmar:
            eliminar_historial()
            self.cargar_historial()
