from conexion import ConexionDB


class R_tiempo:
    def __init__(
        self,
        id_registro: int | None,
        fecha: str,
        cantidad_horas: int,
        descripcion_tarea: str,
        id_empleado: int,
        id_proyecto: int,
    ):
        self.id_registro = id_registro
        self.fecha = fecha
        self.cantidad_horas = cantidad_horas
        self.descripcion_tarea = descripcion_tarea
        self.id_empleado = id_empleado
        self.id_proyecto = id_proyecto

    def guardar(self) -> bool:
        db = ConexionDB()
        if not db.conexion:
            return False

        try:
            if self.id_registro is None:
                db.cursor.execute(
                    """
                    INSERT INTO registro_tiempo (
                        fecha, cantidad_horas, descripcion_tarea,
                        id_empleado, id_proyecto
                    )
                    VALUES (
                        TO_DATE(:1, 'YYYY-MM-DD'), :2, :3, :4, :5
                    )
                    """,
                    (
                        self.fecha,
                        self.cantidad_horas,
                        self.descripcion_tarea,
                        self.id_empleado,
                        self.id_proyecto,
                    ),
                )
            else:
                db.cursor.execute(
                    """
                    INSERT INTO registro_tiempo (
                        id_registro, fecha, cantidad_horas, descripcion_tarea,
                        id_empleado, id_proyecto
                    )
                    VALUES (
                        :1, TO_DATE(:2, 'YYYY-MM-DD'), :3, :4, :5, :6
                    )
                    """,
                    (
                        self.id_registro,
                        self.fecha,
                        self.cantidad_horas,
                        self.descripcion_tarea,
                        self.id_empleado,
                        self.id_proyecto,
                    ),
                )

            db.conexion.commit()
            return True
        except Exception as e:
            db.conexion.rollback()
            print(f"Error al registrar las horas: {e}")
            return False
        finally:
            db.cursor.close()
            db.conexion.close()

    def __str__(self):
        return (
            f"Registro de tiempo: {self.id_registro}, Fecha: {self.fecha}, "
            f"Horas: {self.cantidad_horas}, Tarea: {self.descripcion_tarea}, "
            f"ID empleado: {self.id_empleado}, ID proyecto: {self.id_proyecto}"
        )