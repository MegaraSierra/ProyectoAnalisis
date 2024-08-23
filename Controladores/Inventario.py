# app/controllers/inventario_controller.py

from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flaskext.mysql import MySQL

inventario_bp = Blueprint('inventario_bp', __name__, url_prefix='/inventario')

# Configuración de MySQL (puedes mover esto a un archivo de configuración si prefieres)
mysql = MySQL()

mysql_config = {
    'MYSQL_DATABASE_HOST': 'localhost',
    'MYSQL_DATABASE_PORT': 3306,
    'MYSQL_DATABASE_USER': 'root',
    'MYSQL_DATABASE_PASSWORD': '',
    'MYSQL_DATABASE_DB': 'avaco',
    'MYSQL_DATABASE_SOCKET': None
}

# Función para inicializar MySQL dentro del contexto de la aplicación
@inventario_bp.record
def on_load(state):
    mysql.init_app(state.app)
    state.app.config['MYSQL'] = mysql

@inventario_bp.route('/index')
def inventario_index():
    conectar = mysql.connect()
    cursor = conectar.cursor()
    cursor.execute("SELECT * FROM Inventario")
    inventario = cursor.fetchall()
    return render_template('inventario/index.html', lista=inventario)

@inventario_bp.route('/agregar', methods=['GET', 'POST'])
def inventario_agregar():
    if request.method == 'POST':
        InvCodigo = request.form["InvCodigo"]
        InvNombre = request.form["InvNombre"]
        InvDescripcion = request.form["InvDescripcion"]
        InvProveedor = request.form["InvProveedor"]
        InvCantidad = request.form["InvCantidad"]
        InvPrecio = request.form["InvPrecio"]

        conectar = mysql.connect()
        cursor = conectar.cursor()

        cursor.execute("INSERT INTO Inventario (InvCodigo, InvNombre, InvDescripcion, InvProveedor, InvCantidad, InvPrecio) VALUES (%s, %s, %s, %s, %s, %s)", (InvCodigo, InvNombre, InvDescripcion, InvProveedor, InvCantidad, InvPrecio))
        conectar.commit()
        return redirect(url_for('inventario_bp.inventario_index'))
    
    return render_template('inventario/agregar.html')

@inventario_bp.route('/editar/<string:id>', methods=['GET', 'POST'])
def inventario_editar(id):
    conectar = mysql.connect()
    cursor = conectar.cursor()
    cursor.execute("SELECT * FROM Inventario WHERE InvCodigo=%s", (id,))
    inventario = cursor.fetchone()

    if request.method == 'POST':
        InvCodigo = request.form["InvCodigo"]
        InvNombre = request.form["InvNombre"]
        InvDescripcion = request.form["InvDescripcion"]
        InvProveedor = request.form["InvProveedor"]
        InvCantidad = request.form["InvCantidad"]
        InvPrecio = request.form["InvPrecio"]

        cursor.execute("UPDATE Inventario SET InvCodigo=%s, InvNombre=%s, InvDescripcion=%s, InvProveedor=%s, InvCantidad=%s, InvPrecio=%s WHERE InvCodigo=%s", (InvCodigo, InvNombre, InvDescripcion, InvProveedor, InvCantidad, InvPrecio, id))
        conectar.commit()
        return redirect(url_for('inventario_bp.inventario_index'))
    
    return render_template('inventario/actualizar.html', Inv=inventario)

@inventario_bp.route('/eliminar/<string:id>', methods=['GET', 'POST'])
def inventario_eliminar(id):
    conectar = mysql.connect()
    cursor = conectar.cursor()
    cursor.execute("SELECT * FROM Inventario WHERE InvCodigo=%s", (id,))
    inventario = cursor.fetchone()

    if request.method == 'POST':
        cursor.execute("DELETE FROM Inventario WHERE InvCodigo=%s", (id,))
        conectar.commit()
        return redirect(url_for('inventario_bp.inventario_index'))
    
    return render_template('inventario/eliminar.html', Inv=inventario)
