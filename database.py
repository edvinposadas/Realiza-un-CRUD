"""
Funciones:
- get_db_connection(): abre (o crea) la conexión a la base de datos.
- init_db(): crea la tabla 'alumno' si aún no existe.
"""
import sqlite3

# Conexión a la base de datos (crea alumnos.db si no existe)
def get_db_connection():
    conn = sqlite3.connect('alumnos.db')  # Este será el archivo de base de datos
    conn.row_factory = sqlite3.Row       # Permite acceder a las columnas por nombre
    return conn

# Crear la tabla si no existe
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS alumno (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            edad INTEGER NOT NULL
        )
    ''')
    # Guardamos los cambios en el archivo de base de datos
    conn.commit()
     # Cerramos la conexión para liberar recursos
    conn.close()