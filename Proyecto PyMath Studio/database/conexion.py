try:
    from pymongo import MongoClient
except Exception:
    MongoClient = None


MONGO_ACTIVO = False
cliente = None
base_datos = None
ejercicios = None


if MongoClient is not None:
    try:
        # La conexion se prueba al iniciar para saber si se puede usar MongoDB.
        cliente = MongoClient(
            "mongodb://localhost:27017/",
            serverSelectionTimeoutMS=800
        )
        cliente.admin.command("ping")

        base_datos = cliente["pymathstudio"]
        ejercicios = base_datos["ejercicios"]
        MONGO_ACTIVO = True

    except Exception:
        # Si MongoDB no esta disponible, el historial usara un archivo local.
        MONGO_ACTIVO = False
