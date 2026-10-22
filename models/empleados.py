from .usuarios import Usuarios
from .r_tiempo import R_tiempo
from conexion import ConexionDB

class Empleado(Usuarios):
    def __init__(
        self, 

        id_usuario:str, 
        rut:str,
        nombre:str,
        correo:str, 
        password_hash:str, 
        privilegio:str, 

        id_departamento:int, 
        direccion:str, 
        num_telefonico:str, 
        fecha_contrato:str, 
        salario:float, 
        id_proyecto:int
        ):
        
        super().__init__(id_usuario, rut, nombre, correo, password_hash, privilegio)
        self.id_departamento = id_departamento
        self.direccion = direccion
        self.num_telefonico = num_telefonico
        self.fecha_contrato = fecha_contrato
        self.salario = salario
        self.id_proyecto = id_proyecto

    def __str__(self):
        return f"Empleado: {self.nombre}, RUT: {self.rut}, Correo: {self.correo}, Privilegio: {self.privilegio}, Departamento ID: {self.id_departamento}, Dirección: {self.direccion}, Teléfono: {self.num_telefonico}, Fecha de Contrato: {self.fecha_contrato}, Salario: {self.salario}, Proyecto ID: {self.id_proyecto}"

    def registrarHoras(self, rt: R_tiempo):
        db = ConexionDB()
        if not db.conexion:
            return
        try:
            sql = """
                INSERT INTO registro_tiempo (id_registro, fecha, cantidad_horas, descripcion_tarea, id_empleado, id_proyecto)
                VALUES (:1, TO_DATE(:2, 'YYYY-MM-DD'), :3, :4, :5, :6)
            """
            db.cursor.execute(sql, (
                rt.id_registro,
                rt.fecha,
                rt.cantidad_horas,
                rt.descripcion_tarea,
                self.id_usuario,
                rt.id_proyecto
            ))
            db.conexion.commit()
            print("Horas registradas correctamente.")
        except Exception as e:
            db.conexion.rollback()
            print(f"Error al registrar las horas: {e}")
        finally:
            db.cursor.close()
            db.conexion.close()