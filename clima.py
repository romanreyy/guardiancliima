# Consulta de clima con OpenWeatherMap (modulo Cloud y Conectividad)
# Consulta a la API, visualizacion de datos y guardado en historial CSV.

import requests
import csv
import os
from datetime import datetime
from config import API_KEY_OWM, OWM_URL, OWM_TIMEOUT, ARCHIVO_HISTORIAL, COLUMNAS_HISTORIAL


# ══════════════════════════════════════════════════════════════════════════════
# Consulta a la API de OpenWeatherMap para obtener el clima actual de una ciudad.
# ══════════════════════════════════════════════════════════════════════════════

# Consulta el clima actual de una ciudad usando la API de OpenWeatherMap.
# Devuelve un diccionario con los datos del clima, o none si hay error.
def consultar_clima_owm(ciudad):
    if not API_KEY_OWM:
        print("\n  [!] Error: API Key de OpenWeatherMap no configurada.")
        print("      Configurar la variable de entorno API_KEY_OWM.")
        return None

    params = {
        'q':     ciudad,
        'appid': API_KEY_OWM,
        'units': 'metric',
        'lang':  'es'
    }

    print(f"\n  Consultando el clima para '{ciudad}'...")

    try:
        respuesta = requests.get(OWM_URL, params=params, timeout=OWM_TIMEOUT)
        respuesta.raise_for_status()
        return respuesta.json()

    except requests.exceptions.HTTPError:
        if respuesta.status_code == 404:
            print(f"  [!] Ciudad '{ciudad}' no encontrada. Verificar el nombre e intentar de nuevo.")
        elif respuesta.status_code == 401:
            print("  [!] API Key de OpenWeatherMap invalida. Verificar la configuracion.")
        else:
            print(f"  [!] Error HTTP al consultar el clima: {respuesta.status_code}")
        return None

    except requests.exceptions.ConnectionError:
        print("  [!] Sin conexion a internet. Verificar la red e intentar de nuevo.")
        return None

    except requests.exceptions.Timeout:
        print("  [!] La consulta tardo demasiado. Intentar de nuevo en unos segundos.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"  [!] Error inesperado al consultar el clima: {e}")
        return None

#Extrae y organiza los datos relevantes del JSON de OpenWeatherMap.
#Devuelve un diccionario limpio con los datos del clima.
def extraer_datos_clima(datos_json, ciudad):
    try:
        return {
            "ciudad":      ciudad,
            "temperatura": round(datos_json["main"]["temp"], 1),
            "sensacion":   round(datos_json["main"]["feels_like"], 1),
            "humedad":     datos_json["main"]["humidity"],
            "condicion":   datos_json["weather"][0]["description"].capitalize(),
            "viento":      round(datos_json["wind"]["speed"] * 3.6, 1),  # m/s a km/h
        }
    except KeyError:
        print("  [!] Error al procesar los datos del clima. Formato inesperado.")
        return None


# ══════════════════════════════════════════════════════════════════════════════
# Muestra los datos del clima de forma clara en la consola, con formato organizado.
# ══════════════════════════════════════════════════════════════════════════════

def mostrar_clima(datos):
    print("\n" + "=" * 50)
    print(f"  Clima actual en {datos['ciudad'].upper()}")
    print("=" * 50)
    print(f"  Temperatura:      {datos['temperatura']} C")
    print(f"  Sensacion termica:{datos['sensacion']} C")
    print(f"  Condicion:        {datos['condicion']}")
    print(f"  Humedad:          {datos['humedad']}%")
    print(f"  Viento:           {datos['viento']} km/h")
    print("=" * 50)


# ══════════════════════════════════════════════════════════════════════════════
# Guarda la consulta de clima en un archivo CSV llamado historial_global.csv.
# Si el archivo no existe, lo crea con una cabecera. 
# Cada nueva consulta se agrega como una nueva fila.
# ══════════════════════════════════════════════════════════════════════════════

def guardar_en_historial(usuario, datos):
    ahora = datetime.now()
    archivo_existe = os.path.exists(ARCHIVO_HISTORIAL)

    fila = {
        "NombreDeUsuario":    usuario,
        "Ciudad":             datos["ciudad"],
        "Fecha":              ahora.strftime("%d/%m/%Y"),
        "Hora":               ahora.strftime("%H:%M"),
        "Temperatura_C":      datos["temperatura"],
        "Condicion_Clima":    datos["condicion"],
        "Humedad_Porcentaje": datos["humedad"],
        "Viento_kmh":         datos["viento"],
    }

    with open(ARCHIVO_HISTORIAL, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNAS_HISTORIAL)
        if not archivo_existe:
            writer.writeheader()
        writer.writerow(fila)

    print(f"\n  Consulta guardada en {ARCHIVO_HISTORIAL}")


# ══════════════════════════════════════════════════════════════════════════════
# Flujo completo de la Opcion 1 del menu principal.
# Pide una ciudad, consulta el clima, lo muestra y lo guarda.
# Devuelve el diccionario con los datos del clima (lo usa en la IA), o None si hubo un error.
# ══════════════════════════════════════════════════════════════════════════════

def opcion_consultar_clima(usuario_logueado):
    ciudad = input("\n  Ingrese el nombre de la ciudad: ").strip()
    if not ciudad:
        print("  [!] Debe ingresar el nombre de una ciudad.")
        return None

    datos_json = consultar_clima_owm(ciudad)
    if datos_json is None:
        return None

    datos = extraer_datos_clima(datos_json, ciudad)
    if datos is None:
        return None

    mostrar_clima(datos)
    guardar_en_historial(usuario_logueado, datos)

    return datos
