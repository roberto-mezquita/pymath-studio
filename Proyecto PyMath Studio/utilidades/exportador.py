def exportar_txt(nombre_archivo, contenido):
    # Guarda el contenido visible de un ejercicio en un archivo de texto.
    with open(
        nombre_archivo,
        "w",
        encoding="utf-8"
    ) as archivo:
        archivo.write(contenido)
