from conexion import ConexionDB
from models.usuarios import Usuarios
from models.empleados import Empleado
from models.admins import Admin
from models.proyectos import proyecto
from models.r_tiempo import R_tiempo


def obtener_nombre_gerente(cursor, rut):
    cursor.execute(
        """
        SELECT nombre
        FROM usuarios
        WHERE rut = :1 AND LOWER(privilegio) = 'admin'
        """,
        (rut,)
    )
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None


# Parte hecha con Gemini
def main():
    correo = input("Ingrese su correo: ")
    password = input("Ingrese su contraseña: ")
    
    db = ConexionDB()
    if not db.conexion:
        print("No se pudo conectar a la base de datos.")
        return
    
    try:
        sql = """
            SELECT u.id_usuario, u.rut, u.nombre, u.correo, u.password_hash, u.privilegio,
                   e.id_departamento, e.direccion, e.num_telefonico, e.fecha_contrato, e.salario, e.id_proyecto,
                   a.dept_cargo
            FROM usuarios u
            LEFT JOIN empleados e ON u.id_usuario = e.id_usuario
            LEFT JOIN admins a ON u.id_usuario = a.id_usuario
            WHERE u.correo = :1
        """
        db.cursor.execute(sql, (correo,))
        resultado = db.cursor.fetchone()
        
        if not resultado:
            print("Credenciales inválidas.")
            return
        
        id_usuario, rut, nombre, correo_db, password_hash, privilegio, id_departamento, direccion, num_tel, fecha_cont, salario, id_proy, dept_cargo = resultado
        
        usuario = Usuarios(
            id_usuario=id_usuario,
            rut=rut,
            nombre=nombre,
            correo=correo_db,
            password_hash=password_hash,
            privilegio=privilegio
        )
        
        sesion = usuario.iniciarSesion(password)
        
        if not sesion:
            print("Credenciales inválidas.")
            return
            
        print("Sesion iniciada correctamente.")
        
        es_admin = privilegio.lower() == 'admin'
        if es_admin:
            empleado_obj = Admin(
                id_usuario=id_usuario,
                rut=rut,
                nombre=nombre,
                correo=correo_db,
                password_hash=password_hash,
                privilegio=privilegio,
                id_departamento=id_departamento if id_departamento is not None else 0,
                direccion=direccion if direccion is not None else "",
                num_telefonico=num_tel if num_tel is not None else "",
                fecha_contrato=str(fecha_cont) if fecha_cont is not None else "",
                salario=float(salario) if salario is not None else 0.0,
                id_proyecto=id_proy if id_proy is not None else 0,
                dept_cargo=dept_cargo if dept_cargo is not None else ""
            )
        else:
            empleado_obj = Empleado(
                id_usuario=id_usuario,
                rut=rut,
                nombre=nombre,
                correo=correo_db,
                password_hash=password_hash,
                privilegio=privilegio,
                id_departamento=id_departamento if id_departamento is not None else 0,
                direccion=direccion if direccion is not None else "",
                num_telefonico=num_tel if num_tel is not None else "",
                fecha_contrato=str(fecha_cont) if fecha_cont is not None else "",
                salario=float(salario) if salario is not None else 0.0,
                id_proyecto=id_proy if id_proy is not None else 0
            )

        while True:
            print("\nMenú principal:")
            if es_admin:
                print("1. Gestionar proyectos")
                print("2. Gestionar departamentos")
                print("3. Crear un usuario")
                print("4. Ver todos los empleados")
                print("5. Generar informe de horas")
                print("6. Registrar horas")
                print("7. Actualizar o eliminar un empleado/admin")
                print("8. Cerrar sesión")
                opcion = input("Seleccione una opción (1/2/3/4/5/6/7/8): ").strip()

                try:
                    if opcion == '1':
                        print("\nGestión de proyectos:")
                        print("1. Crear proyecto")
                        print("2. Eliminar proyecto")
                        print("3. Actualizar proyecto")
                        accion = input("Seleccione una opción (1/2/3): ").strip()

                        if accion == '1':
                            proyecto_nuevo = proyecto(
                                int(input("ID del proyecto: ")),
                                input("Nombre del proyecto: "),
                                input("Descripción: "),
                                input("Fecha de inicio (YYYY-MM-DD): ")
                            )
                            empleado_obj.crear_proyecto(proyecto_nuevo)
                        elif accion == '2':
                            id_proyecto = int(input("ID del proyecto a eliminar: "))
                            empleado_obj.eliminar_proyecto(id_proyecto)
                        elif accion == '3':
                            proyecto_actualizado = proyecto(
                                int(input("ID del proyecto a actualizar: ")),
                                input("Nuevo nombre del proyecto: "),
                                input("Nueva descripción: "),
                                input("Nueva fecha de inicio (YYYY-MM-DD): ")
                            )
                            empleado_obj.actualizar_proyecto(proyecto_actualizado)
                        else:
                            print("Opción inválida. Seleccione 1, 2 o 3.")
                    elif opcion == '2':
                        print("\nGestión de departamentos:")
                        print("1. Crear departamento")
                        print("2. Eliminar departamento")
                        print("3. Actualizar departamento")
                        accion = input("Seleccione una opción (1/2/3): ").strip()

                        if accion == '1':
                            id_departamento = int(input("ID del departamento: "))
                            nombre_depa = input("Nombre del departamento: ")
                            rut_gerente = input(
                                "RUT del administrador gerente: "
                            ).strip()
                            gerente = obtener_nombre_gerente(db.cursor, rut_gerente)
                            if gerente:
                                empleado_obj.crear_departamento(
                                    id_departamento, nombre_depa, gerente
                                )
                            else:
                                print(
                                    "No se encontró un administrador con ese RUT."
                                )
                        elif accion == '2':
                            id_departamento = int(
                                input("ID del departamento a eliminar: ")
                            )
                            empleado_obj.eliminar_departamento(id_departamento)
                        elif accion == '3':
                            id_departamento = int(
                                input("ID del departamento a actualizar: ")
                            )
                            nuevo_nombre_depa = input(
                                "Nuevo nombre del departamento: "
                            )
                            rut_gerente = input(
                                "RUT del nuevo administrador gerente: "
                            ).strip()
                            nuevo_gerente = obtener_nombre_gerente(
                                db.cursor, rut_gerente
                            )
                            if nuevo_gerente:
                                empleado_obj.actualizar_departamento(
                                    id_departamento,
                                    nuevo_nombre_depa,
                                    nuevo_gerente
                                )
                            else:
                                print(
                                    "No se encontró un administrador con ese RUT."
                                )
                        else:
                            print("Opción inválida. Seleccione 1, 2 o 3.")
                    elif opcion == '3':
                        nuevo_privilegio = input(
                            "Ingrese el privilegio del nuevo usuario "
                            "(admin / empleado): "
                        ).strip().lower()

                        if nuevo_privilegio not in ('admin', 'empleado'):
                            print(
                                "Privilegio inválido. Debe ser 'admin' o "
                                "'empleado'."
                            )
                            continue

                        datos = {
                            'rut': input("RUT: "),
                            'nombre': input("Nombre: "),
                            'correo': input("Correo: "),
                            'password_hash': input("Contraseña (hash): "),
                            'id_departamento': int(input("ID Departamento: ")),
                            'direccion': input("Dirección: "),
                            'num_telefonico': input("Número telefónico: "),
                            'fecha_contrato': input(
                                "Fecha de contrato (YYYY-MM-DD): "
                            ),
                            'salario': float(input("Salario: ")),
                            'id_proyecto': int(input("ID Proyecto: "))
                        }

                        if nuevo_privilegio == 'admin':
                            datos['dept_cargo'] = input("Departamento a cargo: ")

                        empleado_obj.crear_usuario_segun_privilegio(
                            datos, nuevo_privilegio
                        )
                    elif opcion == '4':
                        empleados = empleado_obj.leer_empleados()
                        if empleados:
                            print("\nEmpleados registrados:")
                            for empleado in empleados:
                                (
                                    id_empleado, rut_empleado, nombre_empleado,
                                    correo_empleado, privilegio_empleado,
                                    departamento, direccion_empleado,
                                    telefono_empleado, fecha_contrato, salario,
                                    id_proyecto_empleado
                                ) = empleado
                                print(
                                    f"ID: {id_empleado} | RUT: {rut_empleado} | "
                                    f"Nombre: {nombre_empleado} | "
                                    f"Correo: {correo_empleado} | "
                                    f"Privilegio: {privilegio_empleado} | "
                                    f"Departamento: {departamento} | "
                                    f"Dirección: {direccion_empleado} | "
                                    f"Teléfono: {telefono_empleado} | "
                                    f"Contrato: {fecha_contrato} | "
                                    f"Salario: {salario} | "
                                    f"Proyecto: {id_proyecto_empleado}"
                                )
                        else:
                            print("No hay empleados registrados.")
                    elif opcion == '5':
                        id_informe = int(input("ID del informe: "))
                        id_empleado_informe = int(
                            input("ID del empleado para el informe: ")
                        )
                        empleado_obj.generar_informe(
                            id_informe, id_empleado_informe
                        )
                    elif opcion == '6':
                        registro = R_tiempo(
                            id_registro=int(input("ID del registro: ")),
                            fecha=input("Fecha (YYYY-MM-DD): ").strip(),
                            cantidad_horas=int(input("Cantidad de horas: ")),
                            descripcion_tarea=input("Descripción de la tarea: "),
                            id_empleado=id_usuario,
                            id_proyecto=int(input("ID del proyecto: "))
                        )
                        empleado_obj.registrarHoras(registro)
                    elif opcion == '7':
                        print("\nGestión de empleados y administradores:")
                        print("1. Actualizar")
                        print("2. Eliminar")
                        accion = input("Seleccione una opción (1/2): ").strip()

                        empleados = empleado_obj.leer_empleados()
                        if not empleados:
                            print("No hay empleados registrados.")
                            continue

                        print("\nUsuarios disponibles:")
                        for fila_empleado in empleados:
                            print(
                                f"ID: {fila_empleado[0]} | "
                                f"Nombre: {fila_empleado[2]} | "
                                f"RUT: {fila_empleado[1]} | "
                                f"Privilegio: {fila_empleado[4]}"
                            )

                        id_objetivo = int(input("ID del usuario: "))
                        if id_objetivo == id_usuario:
                            print("No puedes actualizar o eliminar tu propia cuenta.")
                            continue

                        if accion == '1':
                            datos_actualizados = {
                                'rut': input("Nuevo RUT: ").strip(),
                                'nombre': input("Nuevo nombre: ").strip(),
                                'correo': input("Nuevo correo: ").strip(),
                                'password_hash': input(
                                    "Nueva contraseña/hash: "
                                ).strip(),
                                'privilegio': input(
                                    "Privilegio (admin/empleado): "
                                ).strip().lower(),
                                'id_departamento': int(
                                    input("ID del departamento: ")
                                ),
                                'direccion': input("Dirección: ").strip(),
                                'num_telefonico': input("Teléfono: ").strip(),
                                'fecha_contrato': input(
                                    "Fecha de contrato (YYYY-MM-DD): "
                                ).strip(),
                                'salario': float(input("Salario: ")),
                                'id_proyecto': int(input("ID del proyecto: "))
                            }
                            if datos_actualizados['privilegio'] not in (
                                'admin', 'empleado'
                            ):
                                print(
                                    "Privilegio inválido. Debe ser admin o empleado."
                                )
                                continue
                            if datos_actualizados['privilegio'] == 'admin':
                                datos_actualizados['dept_cargo'] = input(
                                    "Departamento a cargo: "
                                ).strip()
                            empleado_obj.actualizar_empleado(
                                id_objetivo, datos_actualizados
                            )
                        elif accion == '2':
                            confirmar = input(
                                "Esto también eliminará sus registros horarios "
                                "e informes. Escribe ELIMINAR para confirmar: "
                            ).strip()
                            if confirmar == "ELIMINAR":
                                empleado_obj.eliminar_empleado(id_objetivo)
                            else:
                                print("Eliminación cancelada.")
                        else:
                            print("Opción inválida. Seleccione 1 o 2.")
                    elif opcion == '8':
                        print("Sesión cerrada.")
                        break
                    else:
                        print("Opción inválida. Seleccione una opción del 1 al 8.")
                except ValueError:
                    print("Dato inválido. Intente nuevamente.")
            else:
                print("1. Registrar horas")
                print("2. Cerrar sesión")
                opcion = input("Seleccione una opción (1/2): ").strip()
                if opcion == '1':
                    registro = R_tiempo(
                        id_registro=int(input("ID del registro: ")),
                        fecha=input("Fecha (YYYY-MM-DD): ").strip(),
                        cantidad_horas=int(input("Cantidad de horas: ")),
                        descripcion_tarea=input("Descripción de la tarea: "),
                        id_empleado=id_usuario,
                        id_proyecto=int(input("ID del proyecto: "))
                    )
                    empleado_obj.registrarHoras(registro)
                elif opcion == '2':
                    print("Sesión cerrada.")
                    break
                else:
                    print("Opción inválida. Seleccione 1 o 2.")
            
    except Exception as e:
        print(f"Error en el proceso: {e}")
    finally:
        db.cursor.close()
        db.conexion.close()

if __name__ == "__main__":
    main()