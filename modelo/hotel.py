from modelo.usuario import Usuario
from modelo.habitacion import Habitacion
from datetime import datetime, timedelta
from modelo.reserva import Reserva

class Hotel:
    def __init__(self, nombre, ubicacion, instalaciones, servicios):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.instalaciones = instalaciones
        self.servicios = servicios

    def obtener_informacion_hotel(self):
        informacion = f"Información del Hotel {self.nombre}:\n"
        informacion += f"Ubicación: {self.ubicacion}\n"
        informacion += "Instalaciones:\n"
        for instalacion in self.instalaciones:
            informacion += f"- {instalacion}\n"
        informacion += "Servicios:\n"
        for servicio in self.servicios:
            informacion += f"- {servicio}\n"
        return informacion

def solicitar_fechas():
    while True:
        try:
            fecha_inicio_str = input("Ingresa la fecha de ingreso al hotel (formato: DD/MM/YYYY): ")
            fecha_fin_str = input("Ingresa la fecha de salida del hotel (formato: DD/MM/YYYY): ")

            fecha_inicio = datetime.strptime(fecha_inicio_str, "%d/%m/%Y").date()
            fecha_fin = datetime.strptime(fecha_fin_str, "%d/%m/%Y").date()

            if fecha_inicio >= fecha_fin:
                raise ValueError("La fecha de ingreso debe ser anterior a la fecha de salida.")

            return fecha_inicio, fecha_fin
        except ValueError as e:
            print(f"Error: {e}. Introduce las fechas nuevamente.")

def mostrar_habitaciones_disponibles(habitaciones):
    print("Habitaciones disponibles:")
    for habitacion in habitaciones:
        print(f"{habitacion.numero}: {habitacion.tipo} - Precio: ${habitacion.precio} por noche")

def elegir_habitacion(habitaciones):
    while True:
        try:
            mostrar_habitaciones_disponibles(habitaciones)
            seleccion = int(input("Elige el número de la habitación que deseas (0 para cancelar): "))

            if seleccion == 0:
                return None

            habitacion_elegida = next((habitacion for habitacion in habitaciones if habitacion.numero == seleccion), None)

            return habitacion_elegida
        except ValueError as e:
            print(f"Error: {e}. Introduce una opción válida.")

def realizar_reserva(usuario, fecha_inicio, fecha_fin, habitaciones):
    if fecha_inicio > fecha_fin:
        raise ValueError("La fecha de inicio debe ser anterior a la fecha de finalización.")

    for habitacion in habitaciones:
        for fecha in range((fecha_fin - fecha_inicio).days + 1):
            fecha_check = fecha_inicio + timedelta(days=fecha)
            habitacion.fechas_ocupadas.append(fecha_check)

    reserva = Reserva(usuario, fecha_inicio, fecha_fin, habitaciones)
    usuario.reservas.append(reserva)
    print("Reserva realizada exitosamente.")

def mostrar_estado_habitacion(numero_habitacion, habitaciones):
    habitacion = next((habitacion for habitacion in habitaciones if habitacion.numero == numero_habitacion), None)
    if habitacion:
        if habitacion.fechas_ocupadas:
            print(f"Habitación {numero_habitacion} está ocupada en las siguientes fechas:")
            for fecha in habitacion.fechas_ocupadas:
                print(f"- {fecha.strftime('%d/%m/%Y')}")
        else:
            print(f"Habitación {numero_habitacion} está desocupada.")
    else:
        print(f"No se encontró la habitación {numero_habitacion}.")

def cliente_verificar_estado_habitacion(habitaciones):
    numero_habitacion = int(input("Ingresa el número de la habitación que deseas verificar: "))
    mostrar_estado_habitacion(numero_habitacion, habitaciones)

def cliente_cancelar_reserva(usuario):
    if not usuario.reservas:
        print("No tienes reservas para cancelar.")
        return
    print("Tus reservas:")
    for i, reserva in enumerate(usuario.reservas, start=1):
        print(f"{i}. Habitaciones: {', '.join(str(h.numero) for h in reserva.habitaciones)}")
    opcion = int(input("Ingresa el número de la reserva que deseas cancelar (0 para cancelar): "))
    if opcion == 0:
        return
    if opcion > 0 and opcion <= len(usuario.reservas):
        reserva_a_cancelar = usuario.reservas.pop(opcion - 1)
        for habitacion in reserva_a_cancelar.habitaciones:
            for fecha in habitacion.fechas_ocupadas:
                habitacion.fechas_ocupadas.remove(fecha)
        print("Reserva cancelada exitosamente.")
    else:
        print("Opción no válida.")

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

    NUM_HABITACIONES = len(habitaciones)

    fecha_inicio, fecha_fin = solicitar_fechas()
    duracion_estadia = (fecha_fin - fecha_inicio).days

    print(f"Fecha de ingreso: {fecha_inicio.strftime('%d/%m/%Y')}")
    print(f"Fecha de salida: {fecha_fin.strftime('%d/%m/%Y')}")
    print(f"Duración de la estadía: {duracion_estadia} días")

    habitacion_elegida = elegir_habitacion(habitaciones)

    if habitacion_elegida:
        print(f"Habitación elegida: {habitacion_elegida.tipo} - Precio: ${habitacion_elegida.precio} por noche")
        costo_total = duracion_estadia * habitacion_elegida.precio
        print(f"Total a pagar por {duracion_estadia} días de hospedaje: ${costo_total}")
        usuario_actual = iniciar_sesion(input("Ingresa tu nombre de usuario: "), input("Ingresa tu contraseña: "))

        if usuario_actual:
            realizar_reserva(usuario_actual, fecha_inicio, fecha_fin, [habitacion_elegida])
        else:
            print("Inicio de sesión fallido. No se pudo realizar la reserva.")
    else:
        print("Selección cancelada por el usuario.")

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
