from flask import Blueprint, render_template, request, redirect, url_for
from flaskext.mysql import MySQL

ventas_bp = Blueprint('ventas_bp', __name__, url_prefix='/ventas')

# Configuración de MySQL
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
@ventas_bp.record
def on_load(state):
    mysql.init_app(state.app)
    state.app.config['MYSQL'] = mysql

@ventas_bp.route('/index')
def ventas_index():
    conectar = mysql.connect()
    cursor = conectar.cursor()
    cursor.execute("SELECT * FROM Ventas")
    ventas = cursor.fetchall()
    return render_template('ventas/index.html', lista=ventas)

@ventas_bp.route('/agregar', methods=['GET', 'POST'])
def ventas_agregar():
    if request.method == 'POST':
        id_venta = request.form["id_venta"]
        fecha = request.form["fecha"]
        cliente = request.form["cliente"]
        total = request.form["total"]
        estado = request.form["estado"]

        conectar = mysql.connect()
        cursor = conectar.cursor()
        cursor.execute("INSERT INTO Ventas (id_venta, fecha, cliente, total, estado) VALUES (%s, %s, %s, %s, %s)",
                       (id_venta, fecha, cliente, total, estado))
        conectar.commit()
        return redirect(url_for('ventas_bp.ventas_index'))
    
    return render_template('ventas/agregar.html')

@ventas_bp.route('/editar/<string:id>', methods=['GET', 'POST'])
def ventas_editar(id):
    conectar = mysql.connect()
    cursor = conectar.cursor()
    cursor.execute("SELECT * FROM Ventas WHERE id_venta=%s", (id,))
    venta = cursor.fetchone()

    if request.method == 'POST':
        id_venta = request.form["id_venta"]
        fecha = request.form["fecha"]
        cliente = request.form["cliente"]
        total = request.form["total"]
        estado = request.form["estado"]

        cursor.execute("UPDATE Ventas SET fecha=%s, cliente=%s, total=%s, estado=%s WHERE id_venta=%s",
                       (fecha, cliente, total, estado, id_venta))
        conectar.commit()
        return redirect(url_for('ventas_bp.ventas_index'))
    
    return render_template('ventas/editar.html', venta=venta)

@ventas_bp.route('/eliminar/<string:id>', methods=['GET', 'POST'])
def ventas_eliminar(id):
    conectar = mysql.connect()
    cursor = conectar.cursor()
    cursor.execute("SELECT * FROM Ventas WHERE id_venta=%s", (id,))
    venta = cursor.fetchone()

    if request.method == 'POST':
        cursor.execute("DELETE FROM Ventas WHERE id_venta=%s", (id,))
        conectar.commit()
        return redirect(url_for('ventas_bp.ventas_index'))
    
    return render_template('ventas/eliminar.html', venta=venta)

def obtener_clientes():
    conectar = mysql.connect()
    cursor = conectar.cursor()
    cursor.execute("SELECT id_cliente, nombre_cliente FROM Clientes")  # Asegúrate de que estos nombres coincidan con tu base de datos
    clientes = cursor.fetchall()
    cursor.close()
    conectar.close()
    return clientes

def obtener_productos():
    conectar = mysql.connect()
    cursor = conectar.cursor()
    cursor.execute("SELECT id_producto, nombre_producto FROM Productos")  # Asegúrate de que estos nombres coincidan con tu base de datos
    productos = cursor.fetchall()
    cursor.close()
    conectar.close()
    return productos
