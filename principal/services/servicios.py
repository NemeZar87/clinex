from principal.repositories.repositorio import filtrar_medicos, guardar_gobierno_local, guardar_localidad
from principal.models import Localidad, GobiernoLocal
import requests

def obtener_medicos_filtrados(localidad=None, institucion=None, especialidad=None):
    return filtrar_medicos(localidad, institucion, especialidad)

def obtener_datos_api():
    URL = "https://infra.datos.gob.ar/georef-dev/localidades.json"
    response = requests.get(URL)
    data = response.json()

    localidades_limpias = []
    for loc in data.get("localidades", []):
        localidad = {
            "id": loc.get("id"),
            "nombre": loc.get("nombre"),
            "gobierno_local_id": (loc.get("gobierno_local") or {}).get("id"),
            "gobierno_local_nombre": (loc.get("gobierno_local") or {}).get("nombre"),
        }
        if localidad["id"] and localidad["nombre"]:
            localidades_limpias.append(localidad)
    return localidades_limpias

def guardar_gobierno_local(id, nombre):
    if not id or not nombre:
        return None
    gobierno, _ = GobiernoLocal.objects.get_or_create(id=id, defaults={"nombre": nombre})
    return gobierno

def guardar_localidad(id, nombre, gobierno_local):
    Localidad.objects.update_or_create(
        id=id,
        defaults={"nombre": nombre, "gobierno_local": gobierno_local}
    )

def guardar_localidades():
    localidades = obtener_datos_api()

    for loc in localidades:
        gobierno_local = guardar_gobierno_local(
            id=loc["gobierno_local_id"],
            nombre=loc["gobierno_local_nombre"]
        )
        guardar_localidad(
            id=loc["id"],
            nombre=loc["nombre"],
            gobierno_local=gobierno_local
        )
    return f"Se cargaron {len(localidades)} localidades correctamente."

def obtener_todas_localidades():
    return Localidad.objects.all().order_by("nombre")

def obtener_todos_gobiernos_locales():
    return GobiernoLocal.objects.all().order_by("nombre")
