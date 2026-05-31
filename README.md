# GuardianClima ITBA
 
Aplicacion de consola en Python para consultar el clima de cualquier ciudad del mundo, guardar un historial global de consultas, generar estadisticas y recibir consejos de vestimenta personalizados con Inteligencia Artificial.


## Integrantes

- Integrante Roman Rey
- Integrante Ezequiel Romero
- Integrante Mailen Rodriguez
- Integrante Lucia Manzano
**Grupo:** Grupo 39
**Nombre:** WeatherWear
 
## Requisitos previos
 
- Python 3.8 o superior
- Conexion a internet
- API Key de OpenWeatherMap (gratuita)
- API Key de Google Gemini (gratuita)

## Cómo descargar el proyecto desde GitHub

### Opción 1 — Clonar con Git (recomendado)
```bash
git clone https://github.com/romanreyy/guardiancliima.git
cd guardiancliima
```

### Opción 2 — Descargar ZIP
1. Ir a la página del repositorio en GitHub
2. Clic en el botón verde **"Code"**
3. Clic en **"Download ZIP"**
4. Descomprimir el archivo descargado
5. Abrir la carpeta en la terminal

---
Luego de descargar, seguir los pasos de **Instalación de librerias** y **Configuración de API Keys** de este README.

## Instalacion de librerias
 
```bash
pip3 install requests google-genai python-dotenv
```
 
## Configuracion de API Keys
 
### Paso 1 — Obtener las API Keys
 
**OpenWeatherMap (clima):**
1. Crear cuenta gratuita en https://openweathermap.org
2. Ir al perfil -> "My API Keys"
3. Copiar la key generada automaticamente
4. Nota: puede tardar hasta 2 horas en activarse la primera vez
**Google Gemini (IA):**
1. Ir a https://aistudio.google.com con una cuenta Gmail personal
2. Hacer clic en "Get API Key" -> "Create API key in new project"
3. Copiar la key generada
4. Nota: requiere configurar billing en Google Cloud (no genera cargos con uso normal)
### Paso 2 — Crear el archivo .env
 
Crear un archivo llamado `.env` en la raiz del proyecto con el siguiente contenido:
 
```
API_KEY_OWM=tu_clave_openweathermap
API_KEY_GEMINI=tu_clave_gemini
```
 
Reemplazar los valores con las keys reales obtenidas en el paso anterior.
 
### Paso 3 — Agregar dotenv a main.py
 
Asegurarse de que las primeras lineas de `main.py` sean:
 
```python
from dotenv import load_dotenv
load_dotenv()
```
 
## Ejecucion

**En Mac:**
```bash
python3 main.py
```
 
**En Windows:** 
```bash
python main.py
```
 
## Flujo de la aplicacion
 
```
Inicio
  └── Menu de Acceso
        ├── 1. Iniciar Sesion      -> valida credenciales contra usuarios_simulados.csv
        ├── 2. Registrar Usuario   -> valida contraseña con 5 criterios de seguridad
        └── 3. Salir
 
  └── Menu Principal (post-login)
        ├── 1. Consultar Clima     -> OpenWeatherMap API -> guarda en historial_global.csv
        ├── 2. Ver Historial       -> filtra historial por usuario y ciudad
        ├── 3. Estadisticas        -> ciudad top, total consultas, temperatura promedio
        ├── 4. Consejo IA          -> Google Gemini API -> consejo de vestimenta
        ├── 5. Acerca De           -> info del proyecto, equipo y advertencia de seguridad
        └── 6. Cerrar Sesion       -> vuelve al Menu de Acceso
```
 
## Estructura del proyecto
 
```
guardiancliima/
├── main.py          # Punto de entrada de la aplicacion
├── config.py        # API Keys, rutas de CSV y constantes globales
├── auth.py          # Login, registro, validacion de contraseña y hashing SHA-256
├── clima.py         # Consulta de clima via OpenWeatherMap API
├── historial.py     # Historial personal por ciudad y estadisticas globales
├── ia.py            # Consejo de vestimenta via Google Gemini API
├── menus.py         # Interfaz de consola, menus y pantalla Acerca De
├── README.md        # Este archivo
├── .gitignore       # Excluye .env, CSVs y cache de Python
└── (generados al ejecutar)
    ├── usuarios_simulados.csv   # Usuarios registrados con hash SHA-256
    └── historial_global.csv     # Historial de consultas de todos los usuarios
```
 
## Archivos CSV generados
 
### usuarios_simulados.csv
Almacena los usuarios registrados. Las contraseñas se guardan como hash SHA-256 (no en texto plano).
 
| username | password_simulada |
|----------|------------------|
| juan     | a3f9b2c4d1e8...  |
 
### historial_global.csv
Almacena todas las consultas de clima de todos los usuarios. Este archivo se puede abrir en Excel o Google Sheets para generar los graficos requeridos (barras, lineas, torta).
 
| NombreDeUsuario | Ciudad | Fecha | Hora | Temperatura_C | Condicion_Clima | Humedad_Porcentaje | Viento_kmh |
|----------------|--------|-------|------|---------------|-----------------|-------------------|------------|
 
## Criterios de validacion de contraseña
 
La funcion `validar_password()` en `auth.py` verifica:
1. Longitud minima de 8 caracteres
2. Al menos una letra mayuscula
3. Al menos un numero
4. Al menos un simbolo especial (!@#$%^&*...)
5. Sin espacios en blanco
Si la contraseña no cumple alguno de estos criterios, la app informa exactamente que regla fallo y sugiere como crear una contraseña mas segura.
 
## Seguridad

El almacenamiento de usuarios en CSV es una **simulacion educativa**. En aplicaciones reales nunca se guarda la contraseña en texto plano ni en un archivo CSV accesible. Las practicas seguras incluyen:
- Hashing con bcrypt o SHA-256 
- Almacenamiento en base de datos con acceso controlado
- Autenticacion con tokens

## Modulos del curso integrados
 
| Modulo | Como se implementa |
|--------|-------------------|
| Programacion | Funciones modulares, diccionarios, CSV, control de flujo, manejo de errores |
| Ciberseguridad | Validacion de contraseña con 5 criterios, hashing SHA-256, advertencia sobre CSV inseguro |
| Analisis de Datos | historial_global.csv con estadisticas calculadas en Python, exportable para graficos Excel |
| Inteligencia Artificial | Google Gemini API con prompt disenado por el equipo, consejo de vestimenta personalizado |
| Cloud y Conectividad | GitHub como repositorio remoto + OpenWeatherMap y Gemini consumidos via HTTPS |