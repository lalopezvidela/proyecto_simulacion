from database import authenticate_user, create_tables, register_user


def run_gui():
    from login import SplashScreen

    app = SplashScreen()
    app.mainloop()


def run_console():
    print("========================================")
    print("SISTEMA DE SIMULACIÓN")
    print("Modo consola activado")
    print("========================================")

    create_tables()
    while True:
        print("\nOpciones:")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")
        option = input("Selecciona una opción: ").strip()

        if option == "1":
            username = input("Usuario: ").strip()
            password = input("Contraseña: ")
            if authenticate_user(username, password):
                print("Inicio de sesión correcto.")
                while True:
                    print("\nMenú principal")
                    print("1. Calculadora de simulación")
                    print("2. Simulación COVID")
                    print("3. Acerca del proyecto")
                    print("4. Cerrar sesión")
                    suboption = input("Selecciona una opción: ").strip()
                    if suboption == "4":
                        print("Sesión cerrada.")
                        break
                    print("Función en desarrollo para la siguiente fase del proyecto.")
            else:
                print("Usuario o contraseña incorrectos.")
        elif option == "2":
            full_name = input("Nombre completo: ").strip()
            username = input("Usuario: ").strip()
            email = input("Correo electrónico (opcional): ").strip()
            password = input("Contraseña: ")
            confirm_password = input("Confirmar contraseña: ")
            if password != confirm_password:
                print("Las contraseñas no coinciden.")
                continue
            if register_user(full_name, username, email, password):
                print("Cuenta creada correctamente.")
            else:
                print("No se pudo crear la cuenta.")
        elif option == "3":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    try:
        run_gui()
    except (ModuleNotFoundError, ImportError, SystemExit) as exc:
        print(exc)
        print("\nSe iniciará el modo consola porque la interfaz gráfica no está disponible en este entorno.")
        run_console()
