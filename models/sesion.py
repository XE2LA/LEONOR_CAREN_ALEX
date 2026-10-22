from datetime import datetime

# Hceha con Gemini
class Sesion:
    def __init__(self, token: str, vencimiento: datetime, usuario = None):
        self.token = token
        self.vencimiento = vencimiento
        self.usuario = usuario  # Relación 0..1 con Usuarios

    def activar(self) -> bool:
        # Lógica para verificar si la sesión está activa y no ha expirado
        if datetime.now() <= self.vencimiento:
            return True
        return False