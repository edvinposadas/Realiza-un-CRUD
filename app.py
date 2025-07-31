"""
- GET  /           → Lista todos los alumnos.
- GET  /create     → Muestra el formulario para crear un nuevo alumno.
- POST /create     → Procesa el formulario y agrega el alumno a la base de datos.
- GET  /edit/<id>  → Muestra el formulario para editar el alumno con ID dado.
- POST /edit/<id>  → Procesa la edición y actualiza el alumno.
- POST /delete/<id>→ Elimina el alumno con ID dado.
"""
from flask import Flask, render_template, request, redirect, url_for
from database import get_db_connection

app = Flask(__name__)

# Ruta principal: Mostrar todos los alumnos
@app.route('/')
def index():
    conn = get_db_connection()
    alumnos = conn.execute('SELECT * FROM alumno').fetchall()
    conn.close()
    return render_template('index.html', alumnos=alumnos)

# Crear nuevo alumno
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']

        conn = get_db_connection()
        conn.execute('INSERT INTO alumno (nombre, apellido, edad) VALUES (?, ?, ?)',
                     (nombre, apellido, edad))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('create.html')

# Editar un alumno existente
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
     # Trae el alumno cuyo id coincide
    alumno = conn.execute('SELECT * FROM alumno WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']

        # Actualizamos el registro en la base de datos
        conn.execute('UPDATE alumno SET nombre = ?, apellido = ?, edad = ? WHERE id = ?',
                     (nombre, apellido, edad, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
            # Volvemos al listado tras la actualización
    return render_template('edit.html', alumno=alumno)

# Eliminar un alumno
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM alumno WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)