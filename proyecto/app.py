from flask import Flask, request, redirect, url_for, render_template
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    "host": "localhost",
    "user": "veterinario",
    "password": "123456789",
    "database": "veterinaria"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route("/")
def index():
    return render_template("index.html")

### 🐾 CRUD de Propietario ###
@app.route("/propietarios")
def listar_propietarios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Propietario")
    propietarios = cursor.fetchall()
    conn.close()
    return render_template("listar_propietarios.html", propietarios=propietarios)

@app.route("/propietarios/crear", methods=["GET", "POST"])
def crear_propietario():
    if request.method == "POST":
        dni = request.form["dni"]
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        direccion = request.form["direccion"]
        telefono = request.form["telefono"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Propietario (dni, nombre, apellido, direccion, telefono) VALUES (%s, %s, %s, %s, %s)",
            (dni, nombre, apellido, direccion, telefono),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("listar_propietarios"))
    return render_template("crear_propietario.html")

@app.route("/propietarios/editar/<string:dni>", methods=["GET", "POST"])
def editar_propietario(dni):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        direccion = request.form["direccion"]
        telefono = request.form["telefono"]
        cursor.execute(
            "UPDATE Propietario SET nombre=%s, apellido=%s, direccion=%s, telefono=%s WHERE dni=%s",
            (nombre, apellido, direccion, telefono, dni),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("listar_propietarios"))

    cursor.execute("SELECT * FROM Propietario WHERE dni = %s", (dni,))
    propietario = cursor.fetchone()
    conn.close()
    return render_template("editar_propietario.html", propietario=propietario)

@app.route("/propietarios/eliminar/<string:dni>", methods=["POST"])
def eliminar_propietario(dni):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Propietario WHERE dni = %s", (dni,))
    conn.commit()
    conn.close()
    return redirect(url_for("listar_propietarios"))

### 🐶 CRUD de Mascota ###
@app.route("/mascotas")
def listar_mascotas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Mascota")
    mascotas = cursor.fetchall()
    conn.close()
    return render_template("listar_mascotas.html", mascotas=mascotas)

@app.route("/mascotas/crear", methods=["GET", "POST"])
def crear_mascota():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == "POST":
        nombre = request.form["nombre"]
        tipo = request.form["tipo"]
        edad = request.form["edad"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        propietario_dni = request.form["propietario_dni"]

        cursor.execute(
            "INSERT INTO Mascota (nombre, tipo, edad, fecha_nacimiento, propietario_dni) VALUES (%s, %s, %s, %s, %s)",
            (nombre, tipo, edad, fecha_nacimiento, propietario_dni),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("listar_mascotas"))
    
    # Obtener la lista de propietarios
    cursor.execute("SELECT dni, nombre FROM Propietario")
    propietarios = cursor.fetchall()
    conn.close()
    
    return render_template("crear_mascota.html", propietarios=propietarios)

@app.route("/mascotas/editar/<int:id>", methods=["GET", "POST"])
def editar_mascota(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == "POST":
        nombre = request.form["nombre"]
        tipo = request.form["tipo"]
        edad = request.form["edad"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        cursor.execute(
            "UPDATE Mascota SET nombre=%s, tipo=%s, edad=%s, fecha_nacimiento=%s WHERE id=%s",
            (nombre, tipo, edad, fecha_nacimiento, id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("listar_mascotas"))

    cursor.execute("SELECT * FROM Mascota WHERE id = %s", (id,))
    mascota = cursor.fetchone()
    conn.close()
    return render_template("editar_mascota.html", mascota=mascota)

@app.route("/mascotas/eliminar/<int:id>", methods=["POST"])
def eliminar_mascota(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Mascota WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("listar_mascotas"))

### 🏥 CRUD de Consulta ###
@app.route("/consultas")
def listar_consultas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT fecha_consulta, diagnostico, veterinario_dni, mascota_id FROM Consulta")
    consultas = cursor.fetchall()
    conn.close()
    return render_template("listar_consultas.html", consultas=consultas)

@app.route("/consultas/crear", methods=["GET", "POST"])
def crear_consulta():
    if request.method == "POST":
        fecha_consulta = request.form["fecha_consulta"]
        diagnostico = request.form["diagnostico"]
        veterinario_dni = request.form["veterinario_dni"]
        mascota_id = request.form["mascota_id"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Consulta (fecha_consulta, diagnostico, veterinario_dni, mascota_id) VALUES (%s, %s, %s, %s)",
            (fecha_consulta, diagnostico, veterinario_dni, mascota_id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("listar_consultas"))
    
    # Obtener la lista de veterinarios
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT dni FROM Veterinario")
    veterinarios = cursor.fetchall()

    # Obtener la lista de mascotas
    cursor.execute("SELECT id, nombre FROM Mascota")
    mascotas = cursor.fetchall()
    conn.close()

    return render_template("crear_consulta.html", veterinarios=veterinarios, mascotas=mascotas)

@app.route("/consultas/editar/<int:id>", methods=["GET", "POST"])
def editar_consulta(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == "POST":
        fecha_consulta = request.form["fecha_consulta"]
        diagnostico = request.form["diagnostico"]
        veterinario_dni = request.form["veterinario_dni"]  # Modificar veterinario

        cursor.execute(
            "UPDATE Consulta SET fecha_consulta=%s, diagnostico=%s, veterinario_dni=%s WHERE id=%s",
            (fecha_consulta, diagnostico, veterinario_dni, id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("listar_consultas"))

    cursor.execute("SELECT * FROM Consulta WHERE id = %s", (id,))
    consulta = cursor.fetchone()
    
    # Obtener la lista de veterinarios
    cursor.execute("SELECT dni, nombre FROM Veterinario")
    veterinarios = cursor.fetchall()
    conn.close()

    return render_template("editar_consulta.html", consulta=consulta, veterinarios=veterinarios)

@app.route("/consultas/eliminar/<int:id>", methods=["POST"])
def eliminar_consulta(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Consulta WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("listar_consultas"))

@app.route("/personal")
def listar_personal():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Personal")
    personal = cursor.fetchall()
    conn.close()
    return render_template("listar_personal.html", personal=personal)

@app.route("/personal/crear", methods=["GET", "POST"])
def crear_personal():
    if request.method == "POST":
        dni = request.form["dni"]
        codigo = request.form["codigo"]
        nombre = request.form["nombre"]
        tipo = request.form["tipo"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Personal (dni, codigo, nombre, tipo) VALUES (%s, %s, %s, %s)",
            (dni, codigo, nombre, tipo),
        )
        conn.commit()

        if tipo == "Veterinario":
            fecha_alta = request.form["fecha_alta"]
            especialidad = request.form["especialidad"]
            cursor.execute(
                "INSERT INTO Veterinario (dni, fecha_alta, especialidad) VALUES (%s, %s, %s)",
                (dni, fecha_alta, especialidad),
            )
        elif tipo == "Auxiliar":
            cotizacion = request.form["cotizacion"]
            cursor.execute(
                "INSERT INTO Auxiliar (dni, cotizacion) VALUES (%s, %s)",
                (dni, cotizacion),
            )
        conn.commit()
        conn.close()
        return redirect(url_for("listar_personal"))
    return render_template("crear_personal.html")

@app.route("/personal/editar/<string:dni>", methods=["GET", "POST"])
def editar_personal(dni):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        codigo = request.form["codigo"]
        nombre = request.form["nombre"]
        tipo = request.form["tipo"]
        cursor.execute(
            "UPDATE Personal SET codigo=%s, nombre=%s, tipo=%s WHERE dni=%s",
            (codigo, nombre, tipo, dni),
        )
        conn.commit()

        if tipo == "Veterinario":
            fecha_alta = request.form["fecha_alta"]
            especialidad = request.form["especialidad"]
            cursor.execute(
                "UPDATE Veterinario SET fecha_alta=%s, especialidad=%s WHERE dni=%s",
                (fecha_alta, especialidad, dni),
            )
        elif tipo == "Auxiliar":
            cotizacion = request.form["cotizacion"]
            cursor.execute(
                "UPDATE Auxiliar SET cotizacion=%s WHERE dni=%s",
                (cotizacion, dni),
            )
        conn.commit()
        conn.close()
        return redirect(url_for("listar_personal"))

    cursor.execute("SELECT * FROM Personal WHERE dni = %s", (dni,))
    personal = cursor.fetchone()

    if personal["tipo"] == "Veterinario":
        cursor.execute("SELECT fecha_alta, especialidad FROM Veterinario WHERE dni = %s", (dni,))
        veterinario = cursor.fetchone()
        personal.update(veterinario)
    elif personal["tipo"] == "Auxiliar":
        cursor.execute("SELECT cotizacion FROM Auxiliar WHERE dni = %s", (dni,))
        auxiliar = cursor.fetchone()
        personal.update(auxiliar)

    conn.close()
    return render_template("editar_personal.html", personal=personal)

@app.route("/personal/eliminar/<string:dni>", methods=["POST"])
def eliminar_personal(dni):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Personal WHERE dni = %s", (dni,))
    conn.commit()
    conn.close()
    return redirect(url_for("listar_personal"))

if __name__ == "__main__":
    app.run(debug=True)
