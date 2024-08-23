# app.py

from flask import Flask
from flaskext.mysql import MySQL
from Controladores.Inventario import inventario_bp 
from Controladores.Soporte_Tecnico import SP_bp
from Controladores.Compras import compras_bp  # Asegúrate de importar compras_bp correctamente
from Controladores.Ventas import ventas_bp

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambia esto a algo único y secreto
# Configuración de MySQL
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'avaco1'
app.config['MYSQL_DATABASE_SOCKET'] = None

mysql = MySQL()
mysql.init_app(app)

# Registrando blueprints
app.register_blueprint(inventario_bp, url_prefix='/Inventario')
app.register_blueprint(SP_bp, url_prefix='/SP')
app.register_blueprint(compras_bp, url_prefix='/compras')  # Registrar el blueprint de compras
app.register_blueprint(ventas_bp, url_prefix='/ventas')   # Registra el blueprint de compras


if __name__ == '__main__':
    app.run(debug=True)
