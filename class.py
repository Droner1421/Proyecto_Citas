
class Paciente:
    def __init__(self, id_paciente, nombre, telefono, direccion):
        self.id_paciente = id_paciente
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion

class Cita:
    def __init__(self, id_cita, id_paciente, hora, fecha, motivo):
        self.id_cita = id_cita
        self.id_paciente = id_paciente
        self.hora = hora
        self.fecha = fecha
        self.motivo = motivo

class personal:
    def __init__(self, id, nombre, tipo_usuario, usuario, contrasena):
        self.id = id
        self.nombre = nombre
        self.tipo_usuario = tipo_usuario
        self.usuario = usuario
        self.contrasena = contrasena

