from conexion import ConexionDB

class proyecto: 
    def __init__(self, id_proyecto:int, nombre_proyecto:str, descripcion:str, fecha_inicio:str):
        self.__id_proyecto = id_proyecto
        self.__nombre_proyecto = nombre_proyecto
        self.__descripcion = descripcion
        self.__fecha_inicio = fecha_inicio

    def get_id_proyecto(self):
        return self.__id_proyecto

    def set_id_proyecto(self, id_proyecto: int):
        self.__id_proyecto = id_proyecto

    def get_nombre_proyecto(self):
        return self.__nombre_proyecto

    def set_nombre_proyecto(self, nombre_proyecto: str):
        self.__nombre_proyecto = nombre_proyecto

    def get_descripcion(self):
        return self.__descripcion

    def set_descripcion(self, descripcion: str):
        self.__descripcion = descripcion

    def get_fecha_inicio(self):
        return self.__fecha_inicio

    def set_fecha_inicio(self, fecha_inicio: str):
        self.__fecha_inicio = fecha_inicio
        
    def __str__(self):
        return (
            f"ID: {self.__id_proyecto} | Nombre: {self.__nombre_proyecto} | "
            f"Descripción: {self.__descripcion} | "
            f"Fecha de inicio: {self.__fecha_inicio}"
        )
