import requests

def obtener_datos_api():
    URL = "https://infra.datos.gob.ar/georef-dev/localidades.json"
    response = requests.get(URL)
    
    if response.status_code == 200:
        data = response.json()

        localidades_limpias = []
        for loc in data["localidades"]:
            localidad = {
                "provincia": loc.get("provincia", {}).get("nombre"),  # provincia Buenos Aires
                "municio": loc.get("departamento", {}).get("nombre"),  # departamento
                "localidad": loc.get("nombre"),  # ej. Coronel Brandsen
            }
            localidades_limpias.append(localidad)
        
        return localidades_limpias
    else:
        print("Error al obtener datos de la API:", response.status_code)
        return []

