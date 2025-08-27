from flask import Blueprint, request, jsonify

# crear blueprint
tareas_bp = Blueprint('tareas', __name__)

# endpoint para obtener tareas


@tareas_bp.route('/obtener', methods=['GET'])
def get():
    return jsonify({"mensaje": "Estas son tus tareas"})
