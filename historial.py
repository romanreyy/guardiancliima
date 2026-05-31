# Historial y estadisticas globales (modulo Analisis de Datos)
# lectura del CSV, historial personal por ciudad y estadisticas globales.


import csv
import os
from config import ARCHIVO_HISTORIAL


# ══════════════════════════════════════════════════════════════════════════════
# Lectura del historial global desde el archivo CSV. 
# Devuelve una lista de diccionarios.
# ══════════════════════════════════════════════════════════════════════════════

def leer_historial():
    if not os.path.exists(ARCHIVO_HISTORIAL):
        return []
    with open(ARCHIVO_HISTORIAL, newline='', encoding='utf-8') as f:
        muestra = f.read(1024)
        f.seek(0)
        dialecto = csv.Sniffer().sniff(muestra, delimiters=',\t')
        return list(csv.DictReader(f, dialect=dialecto))


# ══════════════════════════════════════════════════════════════════════════════
# Historial personal por ciudad: 
# Filtra el historial global por usuario logueado y ciudad ingresada.
# Muestra los resultados en un formato legible. Si no hay resultados, muestra un mensaje.
# ══════════════════════════════════════════════════════════════════════════════

def opcion_historial_personal(usuario_logueado):
    ciudad = input("\n  Ingrese el nombre de la ciudad a consultar: ").strip()
    if not ciudad:
        print("  [!] Debe ingresar el nombre de una ciudad.")
        return

    historial = leer_historial()

    # Filtrar por usuario logueado Y ciudad (comparacion sin distinguir mayusculas)
    resultados = [
        fila for fila in historial
        if fila["NombreDeUsuario"].lower() == usuario_logueado.lower()
        and fila["Ciudad"].lower() == ciudad.lower()
    ]

    print("\n" + "=" * 60)
    print(f"  Historial de {usuario_logueado} para '{ciudad}'")
    print("=" * 60)

    if not resultados:
        print(f"  No se encontraron consultas para '{ciudad}'.")
        print("  Primero consultar el clima de esa ciudad (Opcion 1).")
    else:
        print(f"  Total de consultas: {len(resultados)}\n")
        for fila in resultados:
            print(f"  {fila['Fecha']} {fila['Hora']}  |  "
                  f"{fila['Temperatura_C']} C  |  "
                  f"{fila['Condicion_Clima']}  |  "
                  f"Humedad: {fila['Humedad_Porcentaje']}%  |  "
                  f"Viento: {fila['Viento_kmh']} km/h")

    print("=" * 60)


# ══════════════════════════════════════════════════════════════════════════════
# Estadisticas globales:
# - Total de consultas realizadas por todos los usuarios.
# - Ciudad mas consultada y cantidad de consultas.
# - Temperatura promedio global de todas las consultas.
# - Conteo de consultas por ciudad (para graficos).
# - Muestra los resultados en un formato legible. Si no hay datos, muestra un mensaje.
# - Recuerda al usuario que el archivo CSV esta listo para abrir en Excel y generar los graficos.
# ══════════════════════════════════════════════════════════════════════════════

def calcular_estadisticas(historial):
    if not historial:
        return None

    # Total de consultas
    total = len(historial)

    # Ciudad mas consultada
    conteo_ciudades = {}
    for fila in historial:
        ciudad = fila["Ciudad"].lower()
        conteo_ciudades[ciudad] = conteo_ciudades.get(ciudad, 0) + 1
    ciudad_top = max(conteo_ciudades, key=conteo_ciudades.get)
    ciudad_top_count = conteo_ciudades[ciudad_top]

    # Temperatura promedio global
    try:
        temperaturas = [float(fila["Temperatura_C"]) for fila in historial]
        temp_promedio = round(sum(temperaturas) / len(temperaturas), 1)
    except (ValueError, ZeroDivisionError):
        temp_promedio = "N/A"

    return {
        "total":            total,
        "ciudad_top":       ciudad_top.capitalize(),
        "ciudad_top_count": ciudad_top_count,
        "temp_promedio":    temp_promedio,
        "conteo_ciudades":  conteo_ciudades,
    }

def opcion_estadisticas_globales():
    historial = leer_historial()

    print("\n" + "=" * 60)
    print("  Estadisticas Globales de Uso")
    print("=" * 60)

    if not historial:
        print("  Sin datos en el historial todavia.")
        print("  Consultar el clima primero (Opcion 1).")
        print("=" * 60)
        return

    stats = calcular_estadisticas(historial)

    print(f"  Total de consultas realizadas:  {stats['total']}")
    print(f"  Ciudad mas consultada:          {stats['ciudad_top']} ({stats['ciudad_top_count']} consultas)")
    print(f"  Temperatura promedio global:    {stats['temp_promedio']} C")

    print("\n  Consultas por ciudad:")
    for ciudad, count in sorted(stats["conteo_ciudades"].items(), key=lambda x: -x[1]):
        print(f"    {ciudad.capitalize():20}({count})")

    print("\n" + "-" * 60)
    print(f"  El archivo '{ARCHIVO_HISTORIAL}' esta listo para abrir en Excel")
    print("  y generar los graficos de barras, lineas y torta.")
    print("=" * 60)
