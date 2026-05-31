#Interfaz de consola y menus de GuardianClima ITBA
#menu de acceso, menu principal y pantalla Acerca De.


from config import NOMBRE_APP, NOMBRE_GRUPO, NUMERO_GRUPO, INTEGRANTES
from auth import (
    login, registrar_usuario, usuario_existe,
    validar_password, sugerir_password_segura
)
from clima import opcion_consultar_clima
from historial import opcion_historial_personal, opcion_estadisticas_globales
from ia import opcion_consejo_ia


# ══════════════════════════════════════════════════════════════════════════════
# Utilidades de interfaz: 
# funciones para limpiar pantalla, imprimir separadores y titulos
# ══════════════════════════════════════════════════════════════════════════════

def limpiar_pantalla():
    print("\n" * 2)

def separador():
    print("-" * 60)

def titulo(texto):
    print("\n" + "=" * 60)
    print(f"  {texto}")
    print("=" * 60)


# ══════════════════════════════════════════════════════════════════════════════
# Pantalla de bienvenida
# ══════════════════════════════════════════════════════════════════════════════

def mostrar_bienvenida():
    print("\n" + "=" * 60)
    print("  *** GUARDIAN CLIMA ITBA ***")
    print("  Monitor climatico inteligente")
    print(f"  {NOMBRE_GRUPO}")
    print("=" * 60)
    print("  Consulta el clima de cualquier ciudad del mundo,")
    print("  guarda tu historial y recibe consejos de vestimenta")
    print("  personalizados con Inteligencia Artificial.")
    print("=" * 60)


# ══════════════════════════════════════════════════════════════════════════════
# Flujo de login
# ══════════════════════════════════════════════════════════════════════════════

def flujo_login():
    titulo("Iniciar Sesion")
    intentos = 0
    max_intentos = 3

    while intentos < max_intentos:
        username = input("\n  Usuario: ").strip()
        password = input("  Contraseña: ").strip()

        if login(username, password):
            print(f"\n  Bienvenido, {username}!")
            return username
        else:
            intentos += 1
            restantes = max_intentos - intentos
            if restantes > 0:
                print(f"  [!] Usuario o contraseña incorrectos. Intentos restantes: {restantes}")
            else:
                print("  [!] Demasiados intentos fallidos. Volviendo al menu principal.")

    return None


# ══════════════════════════════════════════════════════════════════════════════
# Flujo de registro de nuevo usuario
# ══════════════════════════════════════════════════════════════════════════════

def flujo_registro():
    titulo("Registrar Nuevo Usuario")

    # Elegir nombre de usuario
    while True:
        username = input("\n  Ingrese un nombre de usuario: ").strip()
        if not username:
            print("  [!] El nombre de usuario no puede estar vacio.")
            continue
        if ' ' in username:
            print("  [!] El nombre de usuario no puede contener espacios.")
            continue
        if usuario_existe(username):
            print(f"  [!] El usuario '{username}' ya existe. Elegir otro nombre.")
            continue
        break

    # Elegir contraseña con validacion de seguridad
    while True:
        print(f"\n  Registrando usuario: {username}")
        print("  La contraseña debe cumplir los siguientes criterios:")
        print("    - Al menos 8 caracteres")
        print("    - Al menos una letra mayuscula")
        print("    - Al menos un numero")
        print("    - Al menos un simbolo especial (!@#$%^&*...)")
        print("    - Sin espacios en blanco")

        password = input("\n  Ingrese una contraseña: ").strip()
        if not password:
            print("  [!] La contraseña no puede estar vacia.")
            continue

        errores = validar_password(password)

        if errores:
            print(f"\n  [!] Tu contraseña no cumple con:")
            for error in errores:
                print(f"      - Debe {error}")
            sugerir_password_segura()
            print("\n  Intentar con otra contraseña.")
            continue

        # Confirmar contraseña
        confirmacion = input("  Confirmar contraseña: ").strip()
        if password != confirmacion:
            print("  [!] Las contraseñas no coinciden. Intentar de nuevo.")
            continue

        break

    # Guardar usuario 
    registrar_usuario(username, password)
    print(f"\n  Usuario '{username}' registrado exitosamente.")
    print(f"  Contraseña guardada de forma segura (hash SHA-256).")
    print(f"  Iniciando sesion automaticamente...")
    return username


# ══════════════════════════════════════════════════════════════════════════════
# Acerca De: 
# descripcion detallada de la aplicacion, instrucciones de uso 
# explicacion de funcionamiento interno
# integracion de los modulos del curso (programacion, ciberseguridad, analisis de datos, IA, cloud)
# ══════════════════════════════════════════════════════════════════════════════

def mostrar_acerca_de():
    titulo(f"Acerca de {NOMBRE_APP}")

    print("""
  DESCRIPCION
  GuardianClima ITBA es una aplicacion de consola en Python que
  permite consultar el clima de cualquier ciudad, guardar un
  historial global de consultas, ver estadisticas y recibir
  consejos de vestimenta mediante Inteligencia Artificial.

  COMO USAR EL MENU DE ACCESO
  - Opcion 1: Ingresar usuario y contraseña para acceder.
  - Opcion 2: Crear una cuenta nueva con validacion de contraseña.
  - Opcion 3: Salir de la aplicacion.

  COMO USAR EL MENU PRINCIPAL
  - Opcion 1: Ingresa una ciudad y consulta el clima actual.
              Los datos se guardan en historial_global.csv.
  - Opcion 2: Ingresa una ciudad y ve tu historial personal
              de consultas para esa ciudad.
  - Opcion 3: Ve estadisticas globales de todos los usuarios
              (ciudad top, total de consultas, temperatura promedio).
  - Opcion 4: Recibe un consejo de vestimenta generado por IA
              basado en el ultimo clima que consultaste.
  - Opcion 5: Esta pantalla.
  - Opcion 6: Cerrar sesion y volver al menu de acceso.

  COMO FUNCIONA INTERNAMENTE
  - Registro: se pide usuario y contraseña. La contraseña se
    valida con 5 criterios de seguridad. Si no cumple, se informa
    que regla fallo y se sugiere como mejorarla. Al registrarse
    exitosamente, la contraseña se guarda como hash SHA-256.
  
  - ADVERTENCIA DE SEGURIDAD: el almacenamiento en CSV es una
    simulacion educativa. En aplicaciones reales NUNCA se guarda
    la contraseña en texto plano; se usa hashing (bcrypt, SHA-256)
    o autenticacion con tokens. Nosotros implementamos SHA-256
    como mejora de seguridad sobre la consigna base.

  - Clima: se conecta a OpenWeatherMap via HTTPS con la libreria
    requests. Los datos se muestran en pantalla y se guardan
    en historial_global.csv con fecha, hora y usuario.

  - Estadisticas: se lee historial_global.csv completo y se
    calculan ciudad mas consultada, total de consultas y
    temperatura promedio global. El CSV puede abrirse en Excel
    para generar graficos de barras, lineas y torta.

  - IA: se arma un prompt con los datos climaticos del usuario
    y se envia a Google Gemini via HTTPS. La respuesta con el
    consejo de vestimenta se muestra en pantalla.

  MODULOS DEL CURSO INTEGRADOS
  - Programacion: funciones modulares, diccionarios, CSV, control
  - Ciberseguridad: validacion de contraseña, hashing SHA-256
  - Analisis de Datos: historial CSV, estadisticas, graficos Excel
  - Inteligencia Artificial: Google Gemini API, prompt engineering
  - Cloud y Conectividad: GitHub + APIs externas via HTTPS
    """)

    separador()
    print(f"  Grupo: {NUMERO_GRUPO}")
    print(f"  Nombre del grupo: {NOMBRE_GRUPO}")
    print("  Integrantes:")
    for nombre in INTEGRANTES:
        print(f"    - {nombre}")
    print("=" * 60) 


# ══════════════════════════════════════════════════════════════════════════════
# Menu de acceso: 
# opciones para iniciar sesion, registrar nuevo usuario o salir
# ══════════════════════════════════════════════════════════════════════════════

def menu_acceso():
    while True:
        titulo("Menu de Acceso")
        print("  1. Iniciar Sesion")
        print("  2. Registrar Nuevo Usuario")
        print("  3. Salir")
        separador()

        opcion = input("  Seleccione una opcion: ").strip()

        if opcion == "1":
            username = flujo_login()
            if username:
                return username

        elif opcion == "2":
            username = flujo_registro()
            if username:
                return username  # auto-login tras registro exitoso

        elif opcion == "3":
            print("\n  Hasta luego!")
            return None

        else:
            print("  [!] Opcion invalida. Ingrese 1, 2 o 3.")


# ══════════════════════════════════════════════════════════════════════════════
# Menu principal:
# consultar clima, historial personal, estadisticas globales, consejo IA, acerca de, cerrar sesion
# ══════════════════════════════════════════════════════════════════════════════

def menu_principal(usuario_logueado):
    ultima_consulta = None  # guarda el ultimo clima consultado en esta sesion

    while True:
        titulo(f"Menu Principal — {usuario_logueado}")
        print("  1. Consultar Clima Actual y Guardar en Historial")
        print("  2. Ver Mi Historial Personal de Consultas por Ciudad")
        print("  3. Estadisticas Globales de Uso")
        print("  4. Consejo IA: Como Me Visto Hoy")
        print("  5. Acerca De...")
        print("  6. Cerrar Sesion")
        separador()

        opcion = input("  Seleccione una opcion: ").strip()

        if opcion == "1":
            datos = opcion_consultar_clima(usuario_logueado)
            if datos:
                ultima_consulta = datos  # guardar en memoria para la IA

        elif opcion == "2":
            opcion_historial_personal(usuario_logueado)

        elif opcion == "3":
            opcion_estadisticas_globales()

        elif opcion == "4":
            opcion_consejo_ia(ultima_consulta)

        elif opcion == "5":
            mostrar_acerca_de()

        elif opcion == "6":
            print(f"\n  Sesion de {usuario_logueado} cerrada. Hasta luego!")
            return  # vuelve al menu de acceso

        else:
            print("  [!] Opcion invalida. Ingrese un numero del 1 al 6.")

        input("\n  Presione Enter para continuar...")
