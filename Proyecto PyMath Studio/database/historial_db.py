import json
from datetime import datetime
from pathlib import Path

from database.conexion import MONGO_ACTIVO
from database.conexion import ejercicios


ARCHIVO_LOCAL = Path(__file__).with_name("historial_local.json")


def _preparar_para_json(datos):
    # Convierte fechas a texto para que puedan guardarse en un archivo JSON.
    datos_limpios = dict(datos)
    fecha = datos_limpios.get("fecha")

    if isinstance(fecha, datetime):
        datos_limpios["fecha"] = fecha.strftime("%Y-%m-%d %H:%M:%S")

    return datos_limpios


def _leer_historial_local():
    # Lee el historial local cuando MongoDB no esta disponible.
    if not ARCHIVO_LOCAL.exists():
        return []

    with open(ARCHIVO_LOCAL, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def _guardar_historial_local(historial):
    # Escribe el historial completo en formato JSON.
    with open(ARCHIVO_LOCAL, "w", encoding="utf-8") as archivo:
        json.dump(historial, archivo, ensure_ascii=False, indent=4)


def guardar_ejercicio(datos):
    # Guarda un ejercicio en MongoDB o en un respaldo local.
    datos_limpios = _preparar_para_json(datos)

    if MONGO_ACTIVO and ejercicios is not None:
        ejercicios.insert_one(datos_limpios)
        return

    historial = _leer_historial_local()
    historial.append(datos_limpios)
    _guardar_historial_local(historial)


def obtener_historial():
    # Devuelve el historial completo, del mas reciente al mas antiguo.
    if MONGO_ACTIVO and ejercicios is not None:
        return list(
            ejercicios.find().sort("fecha", -1)
        )

    historial = _leer_historial_local()
    return list(reversed(historial))


def eliminar_historial():
    # Borra todos los registros del historial.
    if MONGO_ACTIVO and ejercicios is not None:
        ejercicios.delete_many({})
        return

    _guardar_historial_local([])
