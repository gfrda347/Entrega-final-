from modelo.usuario import Usuario
from modelo.habitacion import Habitacion
from view.console import cliente_verificar_estado_habitacion, cliente_cancelar_reserva
from datetime import datetime, timedelta

def main():
    
    usuarios = [
        Usuario("victor", "doble123"),
        Usuario("santiago", "12345"),
        Usuario("gabriel", "profe")
    ]

    habitaciones = [
        Habitacion(1, "Doble", 100),
        Habitacion(2, "Individual", 50),
        Habitacion(3, "Suite", 200)
    ]

    while True:
        print("\nMenú de Cliente:")
        print("1. Verificar estado de una habitación")
        print("2. Cancelar una reserva")
        print("3. Salir")
        opcion_cliente = int(input("Ingresa el número de la opción que deseas realizar: "))

        if opcion_cliente == 1:
            cliente_verificar_estado_habitacion(habitaciones)
        elif opcion_cliente == 2:
            if usuario_actual:
                cliente_cancelar_reserva(usuario_actual)
            else:
                print("Debes iniciar sesión para cancelar una reserva.")
        elif opcion_cliente == 3:
            print("¡Gracias por visitar nuestro hotel! Hasta luego.")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
