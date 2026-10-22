from conexion import ConexionDB

class proyecto: 
    def __init__(self, id_proyecto:int, nombre_proyecto:str, descripcion:str, fecha_inicio:str):
        self.id_proyecto = id_proyecto
        self.nombre_proyecto = nombre_proyecto
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        
    def __str__(self):
        return f"ID: {self.id_proyecto} | Nombre: {self.nombre_proyecto} | Descripcion: {self.descripcion} | Fecha de inicio: {self.fecha_inicio}"
