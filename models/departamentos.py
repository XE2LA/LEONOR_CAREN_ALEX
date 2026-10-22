class Departamentos:
    def __init__(self, id_departamento:int, nombre_depa:str, gerente:str):
        self.__id_departamento = id_departamento
        self.__nombre_depa = nombre_depa
        self.__gerente = gerente

    def get_id_departamento(self):
        return self.__id_departamento

    def set_id_departamento(self, id_departamento: int):
        self.__id_departamento = id_departamento

    def get_nombre_depa(self):
        return self.__nombre_depa

    def set_nombre_depa(self, nombre_depa: str):
        self.__nombre_depa = nombre_depa

    def get_gerente(self):
        return self.__gerente

    def set_gerente(self, gerente: str):
        self.__gerente = gerente

    def __str__(self):
        return (
            f"ID: {self.__id_departamento} | "
            f"Departamento: {self.__nombre_depa} | Gerente: {self.__gerente}"
        )

    def obtenerDescripcion(self):
        return str(self)