class Departamentos:
    def __init__(self, id_departamento:int, nombre_depa:str, gerente:str):
        self.id_departamento = id_departamento
        self.nombre_depa = nombre_depa
        self.gerente = gerente

    def __str__(self):
        return f"Departamento: {self.nombre_depa}, Gerente: {self.gerente}"

    def obtenerDescripcion(self):
        pass