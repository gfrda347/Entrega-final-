class Usuario:
    def __init__(self, nombre_usuario, contrasena):
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.reservas = [] 

    def cancelar_reserva(self, reserva):
        if reserva in self.reservas:
            self.reservas.remove(reserva)
            print("Reserva cancelada exitosamente.")
        else:
            print("No se encontró la reserva para cancelar.")
