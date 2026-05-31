
# Configuracion y constantes globales de GuardianClima ITBA
# Se centralizan las rutas de archivos, API Keys y constantes del proyecto.
# Las API Keys se leen desde variables de entorno para no exponerlas en el codigo.

import os

# Leer las API Keys desde variables de entorno. Si no estan configuradas, quedan vacias.
API_KEY_OWM    = os.getenv("API_KEY_OWM", "")
API_KEY_GEMINI = os.getenv("API_KEY_GEMINI", "")

#Archivos CSV 
ARCHIVO_USUARIOS  = "usuarios_simulados.csv"
ARCHIVO_HISTORIAL = "historial_global.csv"

# Columnas de cada CSV
COLUMNAS_USUARIOS  = ["username", "password_simulada"]
COLUMNAS_HISTORIAL = [
    "NombreDeUsuario",
    "Ciudad",
    "Fecha",
    "Hora",
    "Temperatura_C",
    "Condicion_Clima",
    "Humedad_Porcentaje",
    "Viento_kmh"
]

#API de OpenWeatherMap
OWM_URL     = "https://api.openweathermap.org/data/2.5/weather"
OWM_TIMEOUT = 10  # segundos

#Constantes de la app
NOMBRE_APP   = "GuardianClima ITBA"
NUMERO_GRUPO = "Grupo 39"     
NOMBRE_GRUPO = "WeatherWear"     
INTEGRANTES  = [                   
    "Integrante Roman Rey",
    "Integrante Mailen Rodriguez",
    "Integrante Ezequiel Romero",
    "Integrante Lucia Manzano",
]
