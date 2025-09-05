from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from flask_bcrypt import Bcrypt

from config.db import get_db_connection

import os
from dotenv import load_dotenv

# cargamos las variables de entorno
load_dotenv()

# creamos el blueprint
usuarios_bp = Blueprint('usuarios', __name__)

# inicializamos Bcrypt
bcrypt = Bcrypt()


@usuarios_bp.route('/registrar', methods=['POST'])
def registrar():
    # obtener del body los datos
    data = request.get_json()

    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')

    # validacion
    if not nombre or not email or not password:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    # obtener el cursos de la bd
    cursor = get_db_connection()

    try:
        # verificamos que el usuario no existe
        cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))

        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({'error': 'Ese usuario ya existe'}), 400

        # hash de la password
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')

        # insertar el registro de nuevo usuario en la base de datos

        cursor.execute('''
        INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)''',
                       (nombre, email, hashed_password))

        # guardamos el nuevo registro
        cursor.connection.commit()

        return jsonify({"mensaje": "Usuario registrado"}), 201

    except Exception as e:
        return jsonify({"error": f"Error al registrar al usuario: {str(e)}"}), 500
    finally:
        cursor.close()
