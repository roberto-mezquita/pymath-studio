import tkinter as tk

from interfaz.componentes import COLOR_FONDO
from interfaz.componentes import COLOR_SECUNDARIO
from interfaz.componentes import COLOR_SECUNDARIO_ACTIVO
from interfaz.componentes import configurar_ventana
from interfaz.componentes import crear_boton
from interfaz.componentes import crear_imagen
from interfaz.componentes import crear_titulo
from interfaz.continuidad_ui import VentanaContinuidad
from interfaz.creditos_ui import VentanaCreditos
from interfaz.graficas_ui import VentanaGraficas
from interfaz.historial_ui import VentanaHistorial
from interfaz.operaciones_ui import VentanaOperaciones


class MenuPrincipal:

    def __init__(self):
        # El menu reemplaza al antiguo inicio de sesion.
        self.ventana = tk.Tk()
        configurar_ventana(
            self.ventana,
            "PyMath Studio",
            "1100x720",
            (900, 620)
        )

        contenedor = tk.Frame(
            self.ventana,
            bg=COLOR_FONDO
        )
        contenedor.pack(fill="both", expand=True, padx=56, pady=30)

        crear_imagen(
            contenedor,
            "logo.png",
            330,
            180,
            pady=(0, 8)
        )

        crear_titulo(
            contenedor,
            "PyMath Studio",
            "Herramientas para practicar continuidad, operaciones, graficas, historial y creditos."
        )

        marco_botones = tk.Frame(
            contenedor,
            bg=COLOR_FONDO
        )
        marco_botones.pack(pady=18)

        # Cada boton abre un modulo en una ventana secundaria.
        botones = [
            ("Continuidad", self.abrir_continuidad, COLOR_SECUNDARIO, COLOR_SECUNDARIO_ACTIVO),
            ("Operaciones", self.abrir_operaciones, "#2F80ED", "#1C67C7"),
            ("Graficador", self.abrir_graficas, "#2F80ED", "#1C67C7"),
            ("Historial", self.abrir_historial, "#8E44AD", "#6C3483"),
            ("Creditos", self.abrir_creditos, "#D35400", "#A04000")
        ]

        for indice, (texto, comando, color, color_activo) in enumerate(botones):
            ultimo_sin_pareja = len(botones) % 2 == 1 and indice == len(botones) - 1
            boton = crear_boton(
                marco_botones,
                texto,
                comando,
                color=color,
                color_activo=color_activo,
                ancho=22
            )
            boton.grid(
                row=indice // 2,
                column=0 if ultimo_sin_pareja else indice % 2,
                columnspan=2 if ultimo_sin_pareja else 1,
                padx=14,
                pady=12,
                sticky="ew"
            )

        self.ventana.mainloop()

    def abrir_continuidad(self):
        VentanaContinuidad(self.ventana)

    def abrir_operaciones(self):
        VentanaOperaciones(self.ventana)

    def abrir_graficas(self):
        VentanaGraficas(self.ventana)

    def abrir_historial(self):
        VentanaHistorial(self.ventana)

    def abrir_creditos(self):
        VentanaCreditos(self.ventana)
