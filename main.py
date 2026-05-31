#Punto de entrada de GuardianClima ITBA

from dotenv import load_dotenv
load_dotenv()

from menus import mostrar_bienvenida, menu_acceso, menu_principal


def main():
    mostrar_bienvenida()

    while True:
        # Menu de acceso: devuelve username si el login es exitoso, None si sale
        usuario = menu_acceso()

        if usuario is None:
            # El usuario eligio "Salir" desde el menu de acceso
            break

        # Menu principal: corre hasta que el usuario cierre sesion
        menu_principal(usuario)

        # Al cerrar sesion, el bucle vuelve al menu de acceso
if __name__ == "__main__":
    main()
