import oracledb

class ConexionDB:

    def __init__(self):
        try:
            self.conexion = oracledb.connect(
                user="ALEX", 
                password="inacap123", 
                host="localhost",
                port=1521,
                service_name="xe"
            )
            self.cursor = self.conexion.cursor()
            print("Conexión exitosa a localhost.")
            
        except Exception as e:
            print(f"ERROR CRÍTICO DE CONEXIÓN: Detalle: {e}")
            self.conexion = None
            self.cursor = None

if __name__ == "__main__":
    db = ConexionDB()