
#Consejo de vestimenta con Google Gemini (modulo Inteligencia Artificial)
#Uso de la libreria google-genai.


from google import genai
from config import API_KEY_GEMINI


# ══════════════════════════════════════════════════════════════════════════════
# Construccion del prompt para Gemini:
# Un buen prompt es claro, especifico, da contexto y define el formato esperado.    
# En este caso, el prompt le da a Gemini toda la informacion del clima actual de la ciudad. 
# Luego, le pide un consejo breve y practico sobre como vestirse, 
# mencionando una o dos prendas clave segun el clima e indicando si conviene llevar paraguas o no.
# Finalmente, se le pide que responda en español, 
# en un tono amigable y en maximo 4 oraciones.
# ══════════════════════════════════════════════════════════════════════════════

def construir_prompt(ciudad, temperatura, condicion, humedad, viento):
    return (
        f"Eres un asistente de moda practico y amigable. "
        f"El clima actual en {ciudad} es el siguiente: "
        f"temperatura de {temperatura} grados Celsius, "
        f"condicion climatica: {condicion}, "
        f"humedad del {humedad}%, "
        f"viento a {viento} km/h. "
        f"Dame un consejo breve y practico sobre como vestirse hoy. "
        f"Menciona una o dos prendas clave segun el clima "
        f"e indica si conviene llevar paraguas o no. "
        f"Responde en espanol, en un tono amigable y en maximo 4 oraciones."
    )


# ══════════════════════════════════════════════════════════════════════════════
# Llamada a la API de Google Gemini para generar el consejo de vestimenta.
# Se maneja la respuesta y los posibles errores de conexion o de API Key.
# El resultado se devuelve como texto para mostrar al usuario. Si hay error, se devuelve un mensaje de error.
# ══════════════════════════════════════════════════════════════════════════════

def obtener_consejo_gemini(ciudad, temperatura, condicion, humedad, viento):
    if not API_KEY_GEMINI:
        return "[!] API Key de Gemini no configurada. Configurar la variable de entorno API_KEY_GEMINI."

    try:
        cliente = genai.Client(api_key=API_KEY_GEMINI)
        prompt  = construir_prompt(ciudad, temperatura, condicion, humedad, viento)

        print("\n  Generando consejo de vestimenta con IA...")
        respuesta = cliente.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if respuesta.text:
            return respuesta.text
        else:
            return "La IA no pudo generar un consejo en este momento. Intentar de nuevo."

    except Exception as e:
        return f"[!] Error al contactar la API de Gemini: {e}"


# ══════════════════════════════════════════════════════════════════════════════
# Consejo IA: Flujo completo de la Opcion 4 del menu principal.
# ══════════════════════════════════════════════════════════════════════════════

def opcion_consejo_ia(ultima_consulta):
    print("\n" + "=" * 60)
    print("  Consejo IA: Como Me Visto Hoy")
    print("=" * 60)

    if not ultima_consulta:
        print("  No hay datos de clima disponibles.")
        print("  Primero consultar el clima de una ciudad (Opcion 1).")
        print("=" * 60)
        return

    ciudad      = ultima_consulta["ciudad"]
    temperatura = ultima_consulta["temperatura"]
    condicion   = ultima_consulta["condicion"]
    humedad     = ultima_consulta["humedad"]
    viento      = ultima_consulta["viento"]

    print(f"  Basado en el clima de {ciudad}:")
    print(f"  {temperatura} C  |  {condicion}  |  Humedad: {humedad}%  |  Viento: {viento} km/h")

    consejo = obtener_consejo_gemini(ciudad, temperatura, condicion, humedad, viento)

    print("\n  Consejo de vestimenta:")
    print("-" * 60)
    print(f"  {consejo}")
    print("=" * 60)