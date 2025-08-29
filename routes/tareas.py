from flask import Blueprint, request, jsonify

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
    nombre = data.get('nombre')
    apellido = data.get('apellido')

    return jsonify({"saludo": f"Hola {nombre} {apellido} "})


# crear endpoint para actualizar (PUT)
@tareas_bp.route('/modificar/<int:user_id>', methods=['PUT'])
def modificar(user_id):

    # obtenemos datos del body
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')

    mensaje = f"Usuario con id: {user_id} modificado a {nombre} {apellido}"

    return jsonify({"saludo": mensaje})
