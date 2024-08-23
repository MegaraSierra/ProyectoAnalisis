from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from flaskext.mysql import MySQL

SP_bp = Blueprint('SP_bp', __name__, url_prefix='/SP')

mysql = MySQL()

mysql_config = {
    'MYSQL_DATABASE_HOST': 'localhost',
    'MYSQL_DATABASE_PORT': 3306,
    'MYSQL_DATABASE_USER': 'root',
    'MYSQL_DATABASE_PASSWORD': '',
    'MYSQL_DATABASE_DB': 'avaco',
    'MYSQL_DATABASE_SOCKET': None
}

@SP_bp.record
def on_load(state):
    mysql.init_app(state.app)
    state.app.config['MYSQL'] = mysql

@SP_bp.route('/index')
def SP_index():
    try:
        conectar = mysql.connect()
        cursor = conectar.cursor()
        cursor.execute("SELECT * FROM Soporte_Tecnico")
        SP = cursor.fetchall()
        conectar.close()
        return render_template('SP/index.html', lista=SP)
    except Exception as e:
        flash(f"Error al cargar los datos: {str(e)}", 'error')
        return render_template('error.html')

@SP_bp.route('/agregar', methods=['GET', 'POST'])
def SP_agregar():
    try:
        if request.method == 'POST':
            SpCodigo = request.form["SpCodigo"]
            SpFecha = request.form["SpFecha"]
            SpCliente = request.form["SpCliente"]
            SpEquipo = request.form["SpEquipo"]
            SpMarca = request.form["SpMarca"]
            SpCantidad = request.form["SpCantidad"]
            SpProblema = request.form["SpProblema"]

            conectar = mysql.connect()
            cursor = conectar.cursor()

            cursor.execute("INSERT INTO Soporte_Tecnico (SpCodigo, SpFecha, SpCliente, SpEquipo, SpMarca, SpCantidad, SpProblema) VALUES (%s, %s, %s, %s, %s, %s, %s)", (SpCodigo, SpFecha, SpCliente, SpEquipo, SpMarca, SpCantidad, SpProblema))
            conectar.commit()
            conectar.close()
            return redirect(url_for('SP_bp.SP_index'))
        
        return render_template('SP/agregar.html')
    except Exception as e:
        flash(f"Error al agregar el registro: {str(e)}", 'error')
        return render_template('error.html')

@SP_bp.route('/editar/<string:id>', methods=['GET', 'POST'])
def SP_editar(id):
    try:
        conectar = mysql.connect()
        cursor = conectar.cursor()
        cursor.execute("SELECT * FROM Soporte_Tecnico WHERE SpCodigo=%s", (id,))
        SP = cursor.fetchone()

        if request.method == 'POST':
            SpCodigo = request.form["SpCodigo"]
            SpFecha = request.form["SpFecha"]
            SpCliente = request.form["SpCliente"]
            SpEquipo = request.form["SpEquipo"]
            SpMarca = request.form["SpMarca"]
            SpCantidad = request.form["SpCantidad"]
            SpProblema = request.form["SpProblema"]

            cursor.execute("UPDATE Soporte_Tecnico SET SpCodigo=%s, SpFecha=%s, SpCliente=%s, SpEquipo=%s, SpMarca=%s, SpCantidad=%s, SpProblema=%s WHERE SpCodigo=%s", (SpCodigo, SpFecha, SpCliente, SpEquipo, SpMarca, SpCantidad, SpProblema, id))
            conectar.commit()
            conectar.close()
            return redirect(url_for('SP_bp.SP_index'))
        
        conectar.close()
        return render_template('SP/actualizar.html', SP=SP)
    except Exception as e:
        flash(f"Error al editar el registro: {str(e)}", 'error')
        return render_template('error.html')

@SP_bp.route('/eliminar/<string:id>', methods=['GET', 'POST'])
def SP_eliminar(id):
    try:
        conectar = mysql.connect()
        cursor = conectar.cursor()
        cursor.execute("SELECT * FROM Soporte_Tecnico WHERE SpCodigo=%s", (id,))
        SP = cursor.fetchone()

        if request.method == 'POST':
            cursor.execute("DELETE FROM Soporte_Tecnico WHERE SpCodigo=%s", (id,))
            conectar.commit()
            conectar.close()
            return redirect(url_for('SP_bp.SP_index'))
        
        conectar.close()
        return render_template('SP/eliminar.html', SP=SP)
    except Exception as e:
        flash(f"Error al eliminar el registro: {str(e)}", 'error')
        return render_template('error.html')

# Ejemplo de manejo de errores global
@SP_bp.errorhandler(Exception)
def handle_exception(e):
    return render_template('error.html', error=str(e))

