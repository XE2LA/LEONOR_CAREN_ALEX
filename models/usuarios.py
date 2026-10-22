from .sesion import Sesion
from datetime import datetime, timedelta

class Usuarios:
    def __init__(self, id_usuario: int, rut: str ,nombre: str, correo: str, password_hash: str, privilegio: str):
        self.id_usuario = id_usuario
        self.rut = rut
        self.nombre = nombre
        self.correo = correo
        self.password_hash = password_hash
        self.privilegio = privilegio
        
    def __str__(self):
        return f"Usuario(id_usuario={self.id_usuario}, rut={self.rut}, nombre={self.nombre}, correo={self.correo}, privilegio={self.privilegio})"

    # Hecha con Gemini
    def validarDatos(self, password_ingresado: str) -> bool:
        # Aquí compararías el password_ingresado con self.password_hash (usando hashing seguro en un caso real)
        # Para ejemplificar, asumimos una validación básica:
        return self.password_hash == password_ingresado

    def iniciarSesion(self, password_ingresado: str) -> Sesion | None:
        if self.validarDatos(password_ingresado):
            # Generar un token de ejemplo y definir vencimiento (por ejemplo, 2 horas)
            token_generado = f"token_secreto_{self.id_usuario}_{datetime.now().timestamp()}"
            vencimiento_sesion = datetime.now() + timedelta(hours=2)
            
            # Se crea y retorna la sesión asociada a este usuario (relación 1 a 0..1)
            nueva_sesion = Sesion(token=token_generado, vencimiento=vencimiento_sesion, usuario=self)
            return nueva_sesion
        
        print("Credenciales inválidas.")
        return None