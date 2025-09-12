from flask import Blueprint, request, jsonify
from config.db import get_db_connection
from flask_jwt_extended import jwt_required, get_jwt_identity

# crear blueprint
tareas_bp = Blueprint('tareas', __name__)

# endpoint para obtener tareas


@tareas_bp.route('/obtener', methods=['GET'])
@jwt_required()
def get():

    # obtenemos la identidad del usuario
    current_user = get_jwt_identity()

    # conectamos a la bd
    cursor = get_db_connection()

    # Ejecutar consulta
    cursor.execute('''
                    SELECT a.usuario_id, a.descripcion, u.nombre, u.email, a.creado_en 
                   FROM tareas as a 
                   JOIN usuarios as u
                   ON a.usuario_id = u.id_usuario
                   WHERE a.usuario_id = %s
                   ''', (current_user,))

    lista = cursor.fetchall()
    cursor.close()

    if not lista:
        return jsonify({"mensaje": "El usuario no tiene tareas creadas"}), 404
    else:
        return jsonify({"tareas": lista}), 200

# endpoint para crear tarea (POST) datos desde el bpdy


@tareas_bp.route('/crear', methods=['POST'])
@jwt_required()
def crear():

    # obtener identidad
    current_user = get_jwt_identity()

    # obtenermos datos del body
    data = request.get_json()

    descripcion = data.get('descripcion')

    if not descripcion:
        return jsonify({"error": "Debes teclear una descripción"}), 400

    # obtenemos el cursor

    cursor = get_db_connection()

    # hacemos el insert
    try:
        cursor.execute(
            'INSERT INTO tareas (descripcion, usuario_id) VALUES (%s, %s)', (descripcion, current_user))
        cursor.connection.commit()
        return jsonify({"mensaje": "Tarea creada"}), 201
    except Exception as e:
        return jsonify({"error": f"No se pudo crear la tarea: {str(e)}"}), 500
    finally:
        cursor.close()


# crear endpoint para actualizar (PUT)
@tareas_bp.route('/modificar/<int:id_tarea>', methods=['PUT'])
@jwt_required()
def modificar(id_tarea):

    # obtenemos la identidad del usuario
    current_user = get_jwt_identity()

    # obtenemos datos del body
    data = request.get_json()
    descripcion = data.get('descripcion')

    # verificar si existe la tarea
    cursor = get_db_connection()
    cursor.execute(
        'SELECT id_tarea, usuario_id FROM tareas WHERE id_tarea = %s', (id_tarea,))
    tarea = cursor.fetchone()

    # verificamos que la tarea existe
    if not tarea:
        cursor.close()
        return jsonify({"error": "No se encontró tarea con ese ID"}), 404

    # verificamos que sea del usuario
    if tarea[1] != int(current_user):
        cursor.close()
        return jsonify({"error": "No tienes permiso para modificar esta tarea"}), 401

    # actualizar los datos
    try:
        cursor.execute('''
                       UPDATE tareas SET descripcion = %s 
                       WHERE id_tarea = %s''', (descripcion, id_tarea,))

        cursor.connection.commit()
        return jsonify({"mensaje": "Datos actualizados correctamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error al actualizar la tarea: {str(e)}"}), 500

    finally:
        cursor.close()
