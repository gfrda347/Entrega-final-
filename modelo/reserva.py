from datetime import datetime, timedelta
from modelo.usuario import Usuario
from modelo.habitacion import Habitacion

class Reserva:
    def __init__(self, usuario, fecha_inicio, fecha_fin, habitaciones):
        self.usuario = usuario
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.habitaciones = habitaciones

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
            
            if habitacion_elegida is None:
                raise ValueError("Número de habitación no válido. Introduce un número de habitación válido.")
            
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

def mostrar_estado_habitacion(numero_habitacion):
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

def cliente_verificar_estado_habitacion():
    numero_habitacion = int(input("Ingresa el número de la habitación que deseas verificar: "))
    mostrar_estado_habitacion(numero_habitacion)

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
                print("Reserva cancelada exitosamente.")
    else:
        print("Opción no válida.")
