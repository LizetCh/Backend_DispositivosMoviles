from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity
from flask_bcrypt import Bcrypt
import datetime

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


@usuarios_bp.route('/login', methods=['POST'])
def login():

    # obtener datos
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    # validacion
    if not email or not password:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    # obtener el cursor de la base de datos
    cursor = get_db_connection()

    try:
        # verificar si el usuario existe
        # , para que lo tome como tupla
        cursor.execute(
            'SELECT password, id_usuario FROM usuarios WHERE email = %s', (email,))
        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user[0], password):
            # Generamos el JWT
            expires = datetime.timedelta(minutes=60)

            access_token = create_access_token(
                identity=str(user[1]),
                expires_delta=expires
            )

            return jsonify({"access_token": access_token}), 200

        else:
            return jsonify({"error": "Credenciales incorrectas"}), 401

    except Exception as e:
        return jsonify({"error": f"Error al hacer login: {str(e)}"}), 500

    finally:
        cursor.close()


@usuarios_bp.route('/datos', methods=['GET'])
@jwt_required()
def datos():

    current_user = get_jwt_identity()

    cursor = get_db_connection()

    try:
        cursor.execute(
            'SELECT id_usuario, nombre, email FROM usuarios WHERE id_usuario = %s', (current_user,))
        user = cursor.fetchone()

        cursor.close()

        if user:
            user_info = {
                "id_usuario": user[0],
                "nombre": user[1],
                "email": user[2]
            }
            return jsonify(user_info), 200
        else:
            return jsonify({"error": "Usuario no encontrado"}), 404

    except Exception as e:
        return jsonify({"error": f"Error al obtener los datos del usuario: {str(e)}"}), 500
