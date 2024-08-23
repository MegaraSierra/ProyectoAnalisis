# app/controllers/compras_controller.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import pymysql

compras_bp = Blueprint('compras_bp', __name__, url_prefix='/compras')

mysql = MySQL()

# Configuración de MySQL
mysql_config = {
    'MYSQL_DATABASE_HOST': 'localhost',
    'MYSQL_DATABASE_PORT': 3306,
    'MYSQL_DATABASE_USER': 'root',
    'MYSQL_DATABASE_PASSWORD': '',
    'MYSQL_DATABASE_DB': 'avaco',
    'MYSQL_DATABASE_SOCKET': None
}

@compras_bp.record
def on_load(state):
    mysql.init_app(state.app)
    state.app.config['MYSQL'] = mysql

@compras_bp.route('/index')
def compras_index():
    conectar = mysql.connect()
    cursor = conectar.cursor()
    cursor.execute("SELECT * FROM Compras")
    compras = cursor.fetchall()
    cursor.close()
    conectar.close()
    return render_template('compras/index.html', lista=compras)

@compras_bp.route('/agregar', methods=['GET', 'POST'])
def compras_agregar():
    conectar = mysql.connect()
    cursor = conectar.cursor()

    if request.method == 'POST':
        FechaCompra = request.form['FechaCompra'].split("T")[0] 
        ProveedorID = request.form['ProveedorID']
        
        try:
            cursor.execute("INSERT INTO Compras (FechaCompra, ProveedorID) VALUES (%s, %s)", (FechaCompra, ProveedorID))
            conectar.commit()
            flash('Compra agregada exitosamente.')
        except pymysql.err.IntegrityError:
            flash('Error: El ProveedorID no existe. Asegúrate de que el proveedor esté registrado.')
            conectar.rollback()
        finally:
            cursor.close()
            conectar.close()
        
        return redirect(url_for('compras_bp.compras_index'))

    cursor.execute("SELECT ProveedoresID, Nombre FROM Proveedores") 
    proveedores = cursor.fetchall()
    cursor.close()
    conectar.close()

    return render_template('compras/agregar.html', proveedores=proveedores)

@compras_bp.route('/editar/<string:id>', methods=['GET', 'POST'])
def compras_editar(id):
    conectar = mysql.connect()
    cursor = conectar.cursor()
    cursor.execute("SELECT * FROM Compras WHERE CompraID=%s", (id,))
    compra = cursor.fetchone()

    if request.method == 'POST':
        FechaCompra = request.form["FechaCompra"].split("T")[0]  # Solo la fecha
        ProveedorID = request.form["ProveedorID"]

        cursor.execute("UPDATE Compras SET FechaCompra=%s, ProveedorID=%s WHERE CompraID=%s", (FechaCompra, ProveedorID, id))
        conectar.commit()
        cursor.close()
        conectar.close()
        flash('Compra actualizada exitosamente.')  # Mensaje de éxito
        return redirect(url_for('compras_bp.compras_index'))

    cursor.execute("SELECT ProveedoresID, Nombre FROM Proveedores")  # Obtener proveedores
    proveedores = cursor.fetchall()
    cursor.close()
    conectar.close()

    return render_template('compras/editar.html', compra=compra, proveedores=proveedores)

@compras_bp.route('/eliminar/<string:id>', methods=['GET', 'POST'])
def compras_eliminar(id):
    conectar = mysql.connect()
    cursor = conectar.cursor()
    cursor.execute("SELECT * FROM Compras WHERE CompraID=%s", (id,))
    compra = cursor.fetchone()

    if request.method == 'POST':
        cursor.execute("DELETE FROM Compras WHERE CompraID=%s", (id,))
        conectar.commit()
        flash('Compra eliminada exitosamente.')  # Mensaje de éxito
        cursor.close()
        conectar.close()
        return redirect(url_for('compras_bp.compras_index'))
    
    cursor.close()
    conectar.close()
    return render_template('compras/eliminar.html', compra=compra)

@compras_bp.route('/')
def compras_root():
    return redirect(url_for('compras_bp.compras_index'))
