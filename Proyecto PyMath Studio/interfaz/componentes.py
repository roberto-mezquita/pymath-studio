import math
import tkinter as tk
from pathlib import Path


# Paleta visual compartida por todas las ventanas.
COLOR_FONDO = "#15171A"
COLOR_SUPERFICIE = "#20242B"
COLOR_ENTRADA = "#F5F7FA"
COLOR_TEXTO = "#F7F9FC"
COLOR_TEXTO_OSCURO = "#1B1F24"
COLOR_TEXTO_SUAVE = "#C8D0DA"
COLOR_BORDE = "#3A414D"
COLOR_PRIMARIO = "#2F80ED"
COLOR_PRIMARIO_ACTIVO = "#1C67C7"
COLOR_SECUNDARIO = "#16A085"
COLOR_SECUNDARIO_ACTIVO = "#117A65"
COLOR_PELIGRO = "#C0392B"
COLOR_PELIGRO_ACTIVO = "#922B21"

FUENTE_TITULO = ("Arial", 28, "bold")
FUENTE_SUBTITULO = ("Arial", 12)
FUENTE_LABEL = ("Arial", 11, "bold")
FUENTE_TEXTO = ("Arial", 12)
FUENTE_BOTON = ("Arial", 12, "bold")
FUENTE_MONO = ("Consolas", 11)


def ruta_recurso(nombre_archivo):
    # Devuelve una ruta absoluta para cargar imagenes e iconos desde cualquier modulo.
    return Path(__file__).resolve().parent.parent / "recursos" / nombre_archivo


def configurar_ventana(ventana, titulo, geometria, minimo):
    # Aplica configuracion comun para que todas las ventanas tengan la misma identidad visual.
    ventana.title(titulo)
    ventana.geometry(geometria)
    ventana.minsize(*minimo)
    ventana.configure(bg=COLOR_FONDO)

    icono = ruta_recurso("icono.ico")
    if icono.exists():
        try:
            ventana.iconbitmap(str(icono))
        except tk.TclError:
            pass


def cargar_imagen_ajustada(nombre_archivo, ancho_maximo, alto_maximo):
    # Intenta redimensionar con Pillow; si no esta instalado, usa el escalado basico de Tkinter.
    ruta = ruta_recurso(nombre_archivo)

    try:
        from PIL import Image, ImageTk

        imagen_base = Image.open(ruta)
        imagen_base.thumbnail((ancho_maximo, alto_maximo), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(imagen_base)

    except Exception:
        imagen = tk.PhotoImage(file=str(ruta))
        factor = max(
            1,
            math.ceil(
                max(
                    imagen.width() / ancho_maximo,
                    imagen.height() / alto_maximo
                )
            )
        )

        if factor > 1:
            return imagen.subsample(factor, factor)

        return imagen


def crear_imagen(padre, nombre_archivo, ancho_maximo, alto_maximo, pady=(0, 0)):
    # Coloca una imagen ajustada al espacio disponible de la ventana.
    try:
        imagen = cargar_imagen_ajustada(nombre_archivo, ancho_maximo, alto_maximo)
    except Exception:
        return None

    etiqueta = tk.Label(
        padre,
        image=imagen,
        bg=COLOR_FONDO
    )
    etiqueta.image = imagen
    etiqueta.pack(pady=pady)
    return etiqueta


def crear_titulo(padre, titulo, subtitulo=None):
    # Crea el titulo principal y un texto de apoyo opcional.
    tk.Label(
        padre,
        text=titulo,
        font=FUENTE_TITULO,
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO
    ).pack(pady=(6, 4))

    if subtitulo:
        tk.Label(
            padre,
            text=subtitulo,
            font=FUENTE_SUBTITULO,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_SUAVE,
            wraplength=760,
            justify="center"
        ).pack(pady=(0, 16))


def crear_campo(padre, etiqueta, ancho=45, ayuda=None):
    # Agrupa una etiqueta, una caja de texto y una ayuda breve para evitar entradas confusas.
    marco = tk.Frame(
        padre,
        bg=COLOR_FONDO
    )
    marco.pack(fill="x", pady=7)

    tk.Label(
        marco,
        text=etiqueta,
        font=FUENTE_LABEL,
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO,
        anchor="w"
    ).pack(fill="x", pady=(0, 4))

    entrada = tk.Entry(
        marco,
        width=ancho,
        font=FUENTE_TEXTO,
        bg=COLOR_ENTRADA,
        fg=COLOR_TEXTO_OSCURO,
        insertbackground=COLOR_TEXTO_OSCURO,
        relief="flat",
        highlightthickness=1,
        highlightbackground=COLOR_BORDE,
        highlightcolor=COLOR_PRIMARIO
    )
    entrada.pack(fill="x", ipady=8)

    if ayuda:
        tk.Label(
            marco,
            text=ayuda,
            font=("Arial", 10),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_SUAVE,
            anchor="w",
            wraplength=760,
            justify="left"
        ).pack(fill="x", pady=(4, 0))

    return entrada


def crear_boton(padre, texto, comando, color=COLOR_PRIMARIO, color_activo=COLOR_PRIMARIO_ACTIVO, ancho=18):
    # Devuelve un boton con el mismo estilo para todos los modulos.
    return tk.Button(
        padre,
        text=texto,
        width=ancho,
        height=2,
        command=comando,
        bg=color,
        fg="white",
        activebackground=color_activo,
        activeforeground="white",
        font=FUENTE_BOTON,
        relief="flat",
        cursor="hand2"
    )


def crear_area_texto(padre, ancho=86, alto=16):
    # Area de salida para mostrar resultados y procedimientos paso a paso.
    texto = tk.Text(
        padre,
        width=ancho,
        height=alto,
        font=FUENTE_MONO,
        bg="#0F1115",
        fg=COLOR_TEXTO,
        insertbackground=COLOR_TEXTO,
        relief="flat",
        highlightthickness=1,
        highlightbackground=COLOR_BORDE,
        wrap="word"
    )
    texto.pack(fill="both", expand=True, pady=(12, 0))
    return texto
