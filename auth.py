
#Autenticacion de usuarios (modulo Ciberseguridad)
#login, registro, validacion de contraseña y hashing opcional.


import csv
import os
import hashlib
from config import ARCHIVO_USUARIOS, COLUMNAS_USUARIOS


# ══════════════════════════════════════════════════════════════════════════════
# Hashing incluido para las contraseñas con la libreria hashing lib que nos da Python.
# ══════════════════════════════════════════════════════════════════════════════

# Convierte una contraseña en un hash SHA-256 irreversible.
def hashear_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Verifica si la contraseña ingresada coincide con el hash guardado.
def verificar_hash(password_ingresada, hash_guardado):
    return hashlib.sha256(password_ingresada.encode()).hexdigest() == hash_guardado


# ══════════════════════════════════════════════════════════════════════════════
# Manejo de usuarios en CSV. 
# Lee y escribe en usuarios_simulados.csv para login y registro.
# ══════════════════════════════════════════════════════════════════════════════

def _leer_usuarios():
    if not os.path.exists(ARCHIVO_USUARIOS):
        return []
    with open(ARCHIVO_USUARIOS, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def _guardar_usuario(username, password_hash):
    archivo_existe = os.path.exists(ARCHIVO_USUARIOS)
    with open(ARCHIVO_USUARIOS, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNAS_USUARIOS)
        if not archivo_existe:
            writer.writeheader()
        writer.writerow({
            "username": username,
            "password_simulada": password_hash
        })


# ══════════════════════════════════════════════════════════════════════════════
# Funcion para validar la contraseña segun los criterios de seguridad. 
# Va a devolver una lista de erores si la contraseña no cumple con los criterios.
# Si la contraseña esta vacia es valida. 
# ══════════════════════════════════════════════════════════════════════════════

def validar_password(password):
    errores = []

    if len(password) < 8:
        errores.append("tener al menos 8 caracteres")

    if not any(c.isupper() for c in password):
        errores.append("contener al menos una letra mayuscula")

    if not any(c.isdigit() for c in password):
        errores.append("contener al menos un numero")

    if not any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for c in password):
        errores.append("contener al menos un simbolo especial (!@#$%^&*...)")

    if ' ' in password:
        errores.append("no contener espacios en blanco")

    return errores

#Sugerencia de contraseña segura para el usuario.
def sugerir_password_segura():
    print("\n  Sugerencias para una contraseña mas segura:")
    print("  - Combina letras mayusculas y minusculas (ej: GuArDiAn)")
    print("  - Agrega numeros en posiciones no obvias (no solo al final)")
    print("  - Usa simbolos especiales: !@#$%^&*")
    print("  - Evita palabras del diccionario o datos personales")
    print("  - Ejemplo de estructura segura: MiCiudad#2026!")


# ══════════════════════════════════════════════════════════════════════════════
# Log in de usuario.
# Verifica las cosas del usuario con usuarios_simulados.csv.
# Soporta tanto contraseñas en texto plano como hasheadas.
# ══════════════════════════════════════════════════════════════════════════════

def login(username, password):
    usuarios = _leer_usuarios()
    for fila in usuarios:
        if fila["username"] == username:
            guardado = fila["password_simulada"]
            # Detecta si es un hash o texto plano 
            es_hash = len(guardado) == 64 and all(c in "0123456789abcdef" for c in guardado)
            if es_hash:
                if verificar_hash(password, guardado):
                    return True
            else:
                if password == guardado:
                    return True
    return False


# ══════════════════════════════════════════════════════════════════════════════
# Registro
# ══════════════════════════════════════════════════════════════════════════════

# Verifica si el nombre de usuario ya existe en el CSV para evitar duplicados.
def usuario_existe(username):
    usuarios = _leer_usuarios()
    return any(fila["username"] == username for fila in usuarios)

# Registra un nuevo usuario con la contraseña hasheada. 
# Devuelve True si el registro fue exitoso.
def registrar_usuario(username, password):
    hash_password = hashear_password(password)
    _guardar_usuario(username, hash_password)
    return True
