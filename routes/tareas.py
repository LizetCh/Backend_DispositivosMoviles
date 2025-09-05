from flask import Blueprint, request, jsonify
from config.db import get_db_connection

# crear blueprint
tareas_bp = Blueprint('tareas', __name__)

# endpoint para obtener tareas


@tareas_bp.route('/obtener', methods=['GET'])
def get():
    return jsonify({"mensaje": "Estas son tus tareas"})

# endpoint para crear tarea (POST) datos desde el bpdy


@tareas_bp.route('/crear', methods=['POST'])
def crear():
    data = request.get_json()

    descripcion = data.get('descripcion')

    if not descripcion:
        return jsonify({"error": "Debes teclear una descripción"}), 400

    # obtenemos el cursor

    cursor = get_db_connection()

    # hacemos el insert
    try:
        cursor.execute(
            'INSERT INTO appTareas (descripcion) VALUES (%s)', (descripcion,))
        cursor.connection.commit()
        return jsonify({"mensaje": "Tarea creada"}), 201
    except Exception as e:
        return jsonify({"error": f"No se pudo crear la tarea: {str(e)}"}), 500
    finally:
        cursor.close()


# crear endpoint para actualizar (PUT)
@tareas_bp.route('/modificar/<int:user_id>', methods=['PUT'])
def modificar(user_id):

    # obtenemos datos del body
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')

    mensaje = f"Usuario con id: {user_id} modificado a {nombre} {apellido}"

    return jsonify({"saludo": mensaje})
