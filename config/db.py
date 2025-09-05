from flask_mysqldb import MySQL
import os  # cargar el sistema operativo
from dotenv import load_dotenv

# cargar de .env las variables de entorno
load_dotenv()

# creo una instancia de MySQL
mysql = MySQL()

# funcion para conectarme a la BD


def init_db(app):
    '''configuramos la base de datos con la instancia de flask'''
    app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
    app.config['MYSQL_USER'] = os.getenv('DB_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('DB_NAME')
    app.config['MYSQL_PORT'] = int(os.getenv('DB_PORT'))

    # inicializar la conexión
    mysql.init_app(app)

    # definimos el cursor


def get_db_connection():
    '''Devuelve un cursor para interactuar con la base de datos'''
    try:
        connection = mysql.connection
        return connection.cursor()
    except Exception as e:
        raise RuntimeError(f"Error al conectar a la base de datos: {e}")
