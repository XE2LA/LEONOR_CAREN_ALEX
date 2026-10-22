from conexion import ConexionDB
from .empleados import Empleado
from .departamentos import Departamentos
from .proyectos import proyecto

class Admin(Empleado):
    def __init__(self, 
        id_usuario: int, 
        rut: str, 
        nombre: str, 
        correo: str, 
        password_hash: str, 
        privilegio: str, 
        id_departamento: int, 
        direccion: str, 
        num_telefonico: str, 
        fecha_contrato: str, 
        salario: float, 
        id_proyecto: int,
        dept_cargo: str):

        super().__init__(
            id_usuario, rut, nombre, correo, password_hash, 
            privilegio, id_departamento, direccion, num_telefonico, 
            fecha_contrato, salario, id_proyecto
        )
        self.dept_cargo = dept_cargo 

    # --- CRUD EMPLEADOS / USUARIOS ---
    def crear_usuario_segun_privilegio(self, datos, privilegio):
        db = ConexionDB()
        if not db.conexion:
            return
        
        try:
            sql_usuario = """
                INSERT INTO usuarios (rut, nombre, correo, password_hash, privilegio, id_departamento)
                VALUES (:1, :2, :3, :4, :5, :6)
            """
            db.cursor.execute(sql_usuario, (
                datos['rut'], datos['nombre'], datos['correo'], 
                datos['password_hash'], privilegio, datos['id_departamento']
            ))
            
            id_usuario_generado = db.cursor.lastrowid 

            sql_empleado = """
                INSERT INTO empleados (id_usuario, direccion, num_telefonico, fecha_contrato, salario, id_proyecto)
                VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5, :6)
            """
            db.cursor.execute(sql_empleado, (
                id_usuario_generado, datos['direccion'], datos['num_telefonico'], 
                datos['fecha_contrato'], datos['salario'], datos['id_proyecto']
            ))

            if privilegio.lower() == 'admin':
                sql_admin = """
                    INSERT INTO admins (id_usuario, nivel_acceso, dept_cargo)
                    VALUES (:1, :2, :3)
                """
                db.cursor.execute(sql_admin, (
                    id_usuario_generado, datos['nivel_acceso'], datos['dept_cargo']
                ))

            db.conexion.commit()
            print("Registro exitoso en el sistema.")
        except Exception as e:
            db.conexion.rollback()
            print(f"Error crÃtico al registrar el usuario: {e}")
        finally:
            db.cursor.close()
            db.conexion.close()

    def leer_empleados(self):
        db = ConexionDB()
        if not db.conexion:
            return []
        try:
            db.cursor.execute("SELECT id_usuario, rut, nombre, correo, privilegio, id_departamento, direccion, num_telefonico, fecha_contrato, salario, id_proyecto FROM empleados")
            return db.cursor.fetchall()
        except Exception as e:
            print(f"Error al listar empleados: {e}")
            return []
        finally:
            db.cursor.close()
            db.conexion.close()

    def actualizar_empleado(self, id_usuario, nuevos_datos):
        db = ConexionDB()
        if not db.conexion:
            return
        try:
            sql_usuario = """
                UPDATE usuarios 
                SET rut = :1, nombre = :2, correo = :3, password_hash = :4, privilegio = :5, id_departamento = :6
                WHERE id_usuario = :7
            """
            db.cursor.execute(sql_usuario, (
                nuevos_datos['rut'], nuevos_datos['nombre'], nuevos_datos['correo'], 
                nuevos_datos['password_hash'], nuevos_datos['privilegio'], nuevos_datos['id_departamento'], 
                id_usuario
            ))

            sql_empleado = """
                UPDATE empleados 
                SET direccion = :1, num_telefonico = :2, fecha_contrato = TO_DATE(:3, 'YYYY-MM-DD'), salario = :4, id_proyecto = :5
                WHERE id_usuario = :6
            """
            db.cursor.execute(sql_empleado, (
                nuevos_datos['direccion'], nuevos_datos['num_telefonico'], 
                nuevos_datos['fecha_contrato'], nuevos_datos['salario'], 
                nuevos_datos['id_proyecto'], id_usuario
            ))

            if nuevos_datos['privilegio'].lower() == 'admin':
                sql_admin = """
                    UPDATE admins 
                    SET nivel_acceso = :1, dept_cargo = :2
                    WHERE id_usuario = :3
                """
                db.cursor.execute(sql_admin, (
                    nuevos_datos['nivel_acceso'], nuevos_datos['dept_cargo'], id_usuario
                ))

            db.conexion.commit()
        except Exception as e:
            db.conexion.rollback()
            print(f"Error al actualizar el empleado: {e}")
        finally:
            db.cursor.close()
            db.conexion.close()

    def eliminar_empleado(self, id_usuario):
        db = ConexionDB()
        if not db.conexion:
            return
        try:
            db.cursor.execute("DELETE FROM admins WHERE id_usuario = :1", (id_usuario,))
            db.cursor.execute("DELETE FROM empleados WHERE id_usuario = :1", (id_usuario,))
            db.cursor.execute("DELETE FROM usuarios WHERE id_usuario = :1", (id_usuario,))
            db.conexion.commit()
        except Exception as e:
            db.conexion.rollback()
            print(f"Error al eliminar el empleado: {e}")
        finally:
            db.cursor.close()
            db.conexion.close()
    
    # --- CRUD PROYECTOS (Usando la clase proyecto) ---
    def crear_proyecto(self, proj: proyecto):
        db = ConexionDB()
        if not db.conexion:
            return
        try:
            sql = """
                INSERT INTO proyectos (id_proyecto, nombre_proyecto, descripcion, fecha_inicio)
                VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'))
            """
            db.cursor.execute(sql, (
                proj.get_id_proyecto(),
                proj.get_nombre_proyecto(),
                proj.get_descripcion(),
                proj.get_fecha_inicio()
            ))
            db.conexion.commit()
            print("Proyecto creado usando la clase proyecto.")
        except Exception as e:
            db.conexion.rollback()
            print(f"Error al crear el proyecto: {e}")
        finally:
            db.cursor.close()
            db.conexion.close()

    def leer_proyecto(self):
        db = ConexionDB()
        if not db.conexion:
            return []
        try:
            db.cursor.execute("SELECT id_proyecto, nombre_proyecto, descripcion, fecha_inicio FROM proyectos")
            resultados = db.cursor.fetchall()
            lista_proyectos = [proyecto(row[0], row[1], row[2], str(row[3])) for row in resultados]
            return lista_proyectos
        except Exception as e:
            print(f"Error al listar proyectos: {e}")
            return []
        finally:
            db.cursor.close()
            db.conexion.close()

    def actualizar_proyecto(self, proj: proyecto):
        db = ConexionDB()
        if not db.conexion:
            return
        try:
            sql = """
                UPDATE proyectos 
                SET nombre_proyecto = :1, descripcion = :2, fecha_inicio = TO_DATE(:3, 'YYYY-MM-DD')
                WHERE id_proyecto = :4
            """
            db.cursor.execute(sql, (
                proj.get_nombre_proyecto(),
                proj.get_descripcion(),
                proj.get_fecha_inicio(),
                proj.get_id_proyecto()
            ))
            db.conexion.commit()
        except Exception as e:
            db.conexion.rollback()
            print(f"Error al actualizar el proyecto: {e}")
        finally:
            db.cursor.close()
            db.conexion.close()

    def eliminar_proyecto(self, id_proyecto):
        db = ConexionDB()
        if not db.conexion:
            return
        try:
            sql = "DELETE FROM proyectos WHERE id_proyecto = :1"
            db.cursor.execute(sql, (id_proyecto,))
            db.conexion.commit()
        except Exception as e:
            db.conexion.rollback()
            print(f"Error al eliminar el proyecto: {e}")
        finally:
            db.cursor.close()
            db.conexion.close()

    # --- CRUD DEPARTAMENTOS (Usando la clase Departamentos) ---
    def crear_departamento(self, depto: Departamentos):
        db = ConexionDB()
        if not db.conexion:
            return
        try:
            sql = """
                INSERT INTO departamentos (id_departamento, nombre_depa, gerente)
                VALUES (:1, :2, :3)
            """
            db.cursor.execute(sql, (
                depto.get_id_departamento(),
                depto.get_nombre_depa(),
                depto.get_gerente()
            ))
            db.conexion.commit()
            print("Departamento creado usando la clase Departamentos.")
        except Exception as e:
            db.conexion.rollback()
            print(f"Error al crear el departamento: {e}")
        finally:
            db.cursor.close()
            db.conexion.close()

    def leer_departamento(self):
        db = ConexionDB()
        if not db.conexion:
            return []
        try:
            db.cursor.execute("SELECT id_departamento, nombre_depa, gerente FROM departamentos")
            resultados = db.cursor.fetchall()
            lista_departamentos = [Departamentos(row[0], row[1], row[2]) for row in resultados]
            return lista_departamentos
        except Exception as e:
            print(f"Error al listar departamentos: {e}")
            return []
        finally: 
            db.cursor.close()
            db.conexion.close()

    def actualizar_departamento(self, depto: Departamentos):
        db = ConexionDB()
        if not db.conexion:
            return
        try:
            sql = """
                UPDATE departamentos
                SET nombre_depa = :1, gerente = :2
                WHERE id_departamento = :3
            """
            db.cursor.execute(sql, (
                depto.get_nombre_depa(),
                depto.get_gerente(),
                depto.get_id_departamento()
            ))
            db.conexion.commit()
        except Exception as e:
            db.conexion.rollback()
            print(f"Error al actualizar el departamento: {e}")
        finally:
            db.cursor.close()
            db.conexion.close()
    
    def eliminar_departamento(self, id_departamento):
        db = ConexionDB()
        if not db.conexion:
            return
        try:
            sql = "DELETE FROM departamentos WHERE id_departamento = :1"
            db.cursor.execute(sql, (id_departamento,))
            db.conexion.commit()
        except Exception as e:
            db.conexion.rollback()
            print(f"Error al eliminar el departamento: {e}")
        finally:
            db.cursor.close()
            db.conexion.close()