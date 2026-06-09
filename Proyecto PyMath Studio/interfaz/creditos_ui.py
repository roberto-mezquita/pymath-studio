import tkinter as tk

from interfaz.componentes import COLOR_BORDE
from interfaz.componentes import COLOR_FONDO
from interfaz.componentes import COLOR_PRIMARIO
from interfaz.componentes import COLOR_PRIMARIO_ACTIVO
from interfaz.componentes import COLOR_SUPERFICIE
from interfaz.componentes import COLOR_TEXTO
from interfaz.componentes import COLOR_TEXTO_SUAVE
from interfaz.componentes import FUENTE_LABEL
from interfaz.componentes import FUENTE_TEXTO
from interfaz.componentes import configurar_ventana
from interfaz.componentes import crear_boton
from interfaz.componentes import crear_imagen
from interfaz.componentes import crear_titulo


INTEGRANTES = [
    "Hazel Martinez",
    "Natalie Menendez",
    "Jonathan Cardona",
    "Roberto Mezquita"
]


class VentanaCreditos:

    def __init__(self, master=None):
        # Muestra los integrantes que realizaron el proyecto.
        self.ventana = tk.Toplevel(master) if master else tk.Tk()
        configurar_ventana(
            self.ventana,
            "Creditos - PyMath Studio",
            "760x640",
            (650, 480)
        )

        contenedor = tk.Frame(
            self.ventana,
            bg=COLOR_FONDO
        )
        contenedor.pack(fill="both", expand=True, padx=46, pady=26)

        crear_imagen(
            contenedor,
            "logo.png",
            210,
            115,
            pady=(0, 4)
        )

        crear_titulo(
            contenedor,
            "Creditos",
            "Integrantes del equipo que realizaron el proyecto."
        )

        tarjeta = tk.Frame(
            contenedor,
            bg=COLOR_SUPERFICIE,
            highlightthickness=1,
            highlightbackground=COLOR_BORDE
        )
        tarjeta.pack(fill="x", pady=(8, 20), padx=42)

        tk.Label(
            tarjeta,
            text="Equipo desarrollador",
            font=FUENTE_LABEL,
            bg=COLOR_SUPERFICIE,
            fg=COLOR_TEXTO,
            anchor="center"
        ).pack(fill="x", pady=(18, 10))

        for indice, integrante in enumerate(INTEGRANTES, start=1):
            fila = tk.Frame(
                tarjeta,
                bg=COLOR_SUPERFICIE
            )
            fila.pack(fill="x", padx=32, pady=6)

            tk.Label(
                fila,
                text=f"{indice}.",
                width=4,
                font=FUENTE_TEXTO,
                bg=COLOR_SUPERFICIE,
                fg=COLOR_TEXTO_SUAVE,
                anchor="e"
            ).pack(side="left")

            tk.Label(
                fila,
                text=integrante,
                font=FUENTE_TEXTO,
                bg=COLOR_SUPERFICIE,
                fg=COLOR_TEXTO,
                anchor="w"
            ).pack(side="left", fill="x", expand=True, padx=(12, 0))

        tk.Label(
            tarjeta,
            text="PyMath Studio",
            font=FUENTE_TEXTO,
            bg=COLOR_SUPERFICIE,
            fg=COLOR_TEXTO_SUAVE
        ).pack(fill="x", pady=(12, 18))

        crear_boton(
            contenedor,
            "Cerrar",
            self.ventana.destroy,
            color=COLOR_PRIMARIO,
            color_activo=COLOR_PRIMARIO_ACTIVO,
            ancho=16
        ).pack(pady=(0, 4))

        if master is None:
            self.ventana.mainloop()
