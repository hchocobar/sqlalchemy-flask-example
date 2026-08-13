"""
Aplicación principal Flask - API REST para gestión de estudiantes.

Expone endpoints CRUD para la entidad Student.
Los mensajes de respuesta están en español según las reglas del proyecto.
Los endpoints y campos están en inglés.
"""

import re
from datetime import date

from flask import Flask, jsonify, request

from database import init_db, db
from models import Student

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar base de datos
init_db(app)


def validar_email(email):
    """
    Valida el formato de un correo electrónico.

    Args:
        email: Cadena con el correo a validar.

    Returns:
        bool: True si el formato es válido, False en caso contrario.
    """
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None


def validar_fecha(fecha_str):
    """
    Valida que una cadena tenga el formato YYYY-MM-DD y sea una fecha válida.

    Args:
        fecha_str: Cadena con la fecha a validar.

    Returns:
        bool: True si la fecha es válida, False en caso contrario.
    """
    try:
        date.fromisoformat(fecha_str)
        return True
    except (ValueError, TypeError):
        return False


def validar_datos_estudiante(data, parcial=False):
    """
    Valida los datos recibidos para crear o actualizar un estudiante.

    Args:
        data: Diccionario con los datos del estudiante.
        parcial: Si es True, permite campos opcionales (para PATCH).

    Returns:
        tuple: (errores, datos_limpios) donde errores es un dict con
               los errores de validación o None si no hay errores.
    """
    errors = {}

    if not data:
        return {"message": "Los datos enviados no son válidos", "errors": {"_json": "No se recibieron datos JSON"}}, None

    if not parcial:
        # Validar campos obligatorios solo en creación y PUT
        if not data.get("name"):
            errors["name"] = "El nombre es obligatorio"

        if not data.get("email"):
            errors["email"] = "El correo electrónico es obligatorio"
    else:
        # En PATCH solo validamos lo que venga
        pass

    # Validar formato de email si se proporciona
    email = data.get("email")
    if email and not validar_email(email):
        errors["email"] = "El correo electrónico no tiene un formato válido"

    # Validar formato de fecha si se proporciona
    birth_date = data.get("birth_date")
    if birth_date and not validar_fecha(birth_date):
        errors["birth_date"] = "La fecha de nacimiento debe tener formato YYYY-MM-DD"

    # Verificar si el correo ya está registrado (solo si se proporciona email)
    if email and not errors.get("email"):
        existing = Student.query.filter(Student.email == email).first()
        if existing:
            errors["email"] = "El correo electrónico ya está registrado"
            return {"message": "El correo electrónico ya está registrado", "errors": errors}, None

    if errors:
        return {"message": "Los datos enviados no son válidos", "errors": errors}, None

    return None, data


# ---------------------------------------------------------------------------
# ENDPOINTS
# ---------------------------------------------------------------------------

@app.route("/students", methods=["POST"])
def crear_estudiante():
    """
    POST /students - Crea un nuevo estudiante.

    Cuerpo esperado: JSON con name (obligatorio), email (obligatorio),
                     birth_date, nationality, current_residence_city.
    """
    data = request.get_json(silent=True)
    error_response, datos_limpios = validar_datos_estudiante(data)

    if error_response:
        return jsonify(error_response), 400

    # Convertir birth_date de string a objeto date
    fecha_nac = None
    if datos_limpios.get("birth_date"):
        fecha_nac = date.fromisoformat(datos_limpios["birth_date"])

    nuevo_estudiante = Student(
        name=datos_limpios["name"],
        email=datos_limpios["email"],
        birth_date=fecha_nac,
        nationality=datos_limpios.get("nationality"),
        current_residence_city=datos_limpios.get("current_residence_city"),
    )

    try:
        db.session.add(nuevo_estudiante)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Ocurrió un error interno en el servidor"}), 500

    return jsonify({
        "message": "Estudiante creado correctamente",
        "student": nuevo_estudiante.to_dict(),
    }), 201


@app.route("/students", methods=["GET"])
def listar_estudiantes():
    """
    GET /students - Lista todos los estudiantes registrados.
    """
    try:
        estudiantes = Student.query.all()
    except Exception:
        return jsonify({"message": "Ocurrió un error interno en el servidor"}), 500

    return jsonify({
        "message": "Estudiantes obtenidos correctamente",
        "students": [e.to_dict() for e in estudiantes],
    }), 200


@app.route("/students/<int:student_id>", methods=["GET"])
def obtener_estudiante(student_id):
    """
    GET /students/<id> - Obtiene un estudiante por su ID.
    """
    try:
        estudiante = Student.query.get(student_id)
    except Exception:
        return jsonify({"message": "Ocurrió un error interno en el servidor"}), 500

    if not estudiante:
        return jsonify({"message": "Estudiante no encontrado"}), 404

    return jsonify({
        "message": "Estudiante encontrado correctamente",
        "student": estudiante.to_dict(),
    }), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def actualizar_estudiante(student_id):
    """
    PUT /students/<id> - Actualiza completamente un estudiante.

    Todos los campos se actualizan. Los campos obligatorios deben estar presentes.
    """
    try:
        estudiante = Student.query.get(student_id)
    except Exception:
        return jsonify({"message": "Ocurrió un error interno en el servidor"}), 500

    if not estudiante:
        return jsonify({"message": "Estudiante no encontrado"}), 404

    data = request.get_json(silent=True)
    error_response, datos_limpios = validar_datos_estudiante(data)

    if error_response:
        return jsonify(error_response), 400

    # Convertir birth_date de string a objeto date
    fecha_nac = None
    if datos_limpios.get("birth_date"):
        fecha_nac = date.fromisoformat(datos_limpios["birth_date"])

    estudiante.name = datos_limpios["name"]
    estudiante.email = datos_limpios["email"]
    estudiante.birth_date = fecha_nac
    estudiante.nationality = datos_limpios.get("nationality")
    estudiante.current_residence_city = datos_limpios.get("current_residence_city")

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Ocurrió un error interno en el servidor"}), 500

    return jsonify({
        "message": "Estudiante actualizado correctamente",
        "student": estudiante.to_dict(),
    }), 200


@app.route("/students/<int:student_id>", methods=["PATCH"])
def actualizar_estudiante_parcial(student_id):
    """
    PATCH /students/<id> - Actualiza parcialmente un estudiante.

    Solo se actualizan los campos proporcionados en el cuerpo de la solicitud.
    """
    try:
        estudiante = Student.query.get(student_id)
    except Exception:
        return jsonify({"message": "Ocurrió un error interno en el servidor"}), 500

    if not estudiante:
        return jsonify({"message": "Estudiante no encontrado"}), 404

    data = request.get_json(silent=True)
    error_response, datos_limpios = validar_datos_estudiante(data, parcial=True)

    if error_response:
        return jsonify(error_response), 400

    # Actualizar solo los campos proporcionados
    if "name" in datos_limpios:
        estudiante.name = datos_limpios["name"]
    if "email" in datos_limpios:
        estudiante.email = datos_limpios["email"]
    if "birth_date" in datos_limpios:
        estudiante.birth_date = date.fromisoformat(datos_limpios["birth_date"])
    if "nationality" in datos_limpios:
        estudiante.nationality = datos_limpios["nationality"]
    if "current_residence_city" in datos_limpios:
        estudiante.current_residence_city = datos_limpios["current_residence_city"]

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Ocurrió un error interno en el servidor"}), 500

    return jsonify({
        "message": "Estudiante actualizado correctamente",
        "student": estudiante.to_dict(),
    }), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def eliminar_estudiante(student_id):
    """
    DELETE /students/<id> - Elimina un estudiante por su ID.
    """
    try:
        estudiante = Student.query.get(student_id)
    except Exception:
        return jsonify({"message": "Ocurrió un error interno en el servidor"}), 500

    if not estudiante:
        return jsonify({"message": "Estudiante no encontrado"}), 404

    try:
        db.session.delete(estudiante)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Ocurrió un error interno en el servidor"}), 500

    return jsonify({"message": "Estudiante eliminado correctamente"}), 200


# ---------------------------------------------------------------------------
# Manejo de errores globales
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(error):
    """Maneja rutas no encontradas."""
    return jsonify({"message": "Recurso no encontrado"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Maneja errores internos del servidor."""
    return jsonify({"message": "Ocurrió un error interno en el servidor"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)